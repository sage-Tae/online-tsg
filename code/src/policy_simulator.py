"""Online TSG simulator parameterized by dispatch policy.

Same event semantics as src.simulator.OnlineTSGSimulator but the choice
of next customer from U_t is delegated to a policy callback. C(N)_online
is the total elapsed time including waiting, matching the project
convention in src.simulator.
"""

import sys
from itertools import combinations

from src.tsp import tsp_cost, dist


def run_with_policy(positions, arrival_times, policy_fn,
                    depot=(0, 0), speed=1.0, coalition_cache=None):
    """Run the online TSG with the given dispatch policy.

    Returns dict with C_N (total elapsed time), coalition_costs, route,
    events, serve_times, k (= max |U_t| observed), and players.
    """
    all_ids = sorted(positions.keys())
    arrivals = sorted(all_ids, key=lambda i: arrival_times[i])

    # cache may be shared across multiple policy runs for the same instance
    if coalition_cache is None:
        coalition_cache = {}

    U_t = set()
    V_t = set()
    coalition_costs = {}  # subsets actually encountered in F during this run
    events = []
    route = []
    serve_times = {}
    k_max = 0

    vehicle_pos = depot
    current_time = 0.0
    arrival_idx = 0

    while len(V_t) < len(all_ids):
        # arrivals up to current_time
        while arrival_idx < len(arrivals):
            cid = arrivals[arrival_idx]
            if arrival_times[cid] <= current_time + 1e-9:
                U_t.add(cid)
                events.append({'type': 'ARRIVE', 'time': arrival_times[cid],
                               'customer': cid, 'vehicle_pos': vehicle_pos})
                arrival_idx += 1
            else:
                break

        # coalition enumeration only; k is measured later at service events
        if U_t:
            if len(U_t) > 15:
                print(f"  WARNING: |U_t|={len(U_t)} > 15, skipping subset enumeration",
                      file=sys.stderr)
            else:
                u_list = sorted(U_t)
                for size in range(1, len(u_list) + 1):
                    for subset in combinations(u_list, size):
                        fs = frozenset(subset)
                        if fs not in coalition_costs:
                            if fs in coalition_cache:
                                coalition_costs[fs] = coalition_cache[fs]
                            else:
                                cost, _ = tsp_cost(depot, list(subset),
                                                   positions, arrival_times,
                                                   speed)
                                coalition_costs[fs] = cost
                                coalition_cache[fs] = cost

        if not U_t:
            if arrival_idx < len(arrivals):
                current_time = arrival_times[arrivals[arrival_idx]]
                continue
            else:
                break

        # delegate to policy
        best_id = policy_fn(vehicle_pos, U_t, positions, depot,
                            arrival_times, current_time, speed)

        best_d = dist(vehicle_pos, positions[best_id])
        travel_time = best_d / speed
        arrival_at_cust = current_time + travel_time
        serve_time = max(arrival_at_cust, arrival_times[best_id])

        # Sweep in all arrivals up to serve_time (so peak-queue count covers
        # arrivals that occurred during travel/wait) and measure k at the
        # service-event instant, matching the k = max_t |U_t| definition.
        while arrival_idx < len(arrivals):
            cid = arrivals[arrival_idx]
            if arrival_times[cid] <= serve_time + 1e-9:
                if cid not in V_t:
                    U_t.add(cid)
                events.append({'type': 'ARRIVE', 'time': arrival_times[cid],
                               'customer': cid, 'vehicle_pos': vehicle_pos})
                arrival_idx += 1
            else:
                break
        if len(U_t) > k_max:
            k_max = len(U_t)

        current_time = serve_time
        vehicle_pos = positions[best_id]

        U_t.remove(best_id)
        V_t.add(best_id)
        route.append((best_id, serve_time))
        serve_times[best_id] = serve_time
        events.append({'type': 'SERVE', 'time': serve_time,
                       'customer': best_id, 'vehicle_pos': vehicle_pos})

    return_time = dist(vehicle_pos, depot) / speed
    total_time = current_time + return_time

    grand = frozenset(all_ids)
    if grand not in coalition_costs:
        if grand in coalition_cache:
            coalition_costs[grand] = coalition_cache[grand]
        else:
            cost, _ = tsp_cost(depot, all_ids, positions, arrival_times, speed)
            coalition_costs[grand] = cost
            coalition_cache[grand] = cost
    for cid in all_ids:
        fs = frozenset([cid])
        if fs not in coalition_costs:
            if fs in coalition_cache:
                coalition_costs[fs] = coalition_cache[fs]
            else:
                cost, _ = tsp_cost(depot, [cid], positions, arrival_times,
                                   speed)
                coalition_costs[fs] = cost
                coalition_cache[fs] = cost

    return {
        'events': events,
        'route': route,
        'serve_times': serve_times,
        'coalition_costs': coalition_costs,
        'C_N': total_time,
        'players': all_ids,
        'k': k_max,
    }
