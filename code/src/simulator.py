"""Online TSG Simulator.
C(N)_online = 총 소요 시간 (depot 출발 ~ depot 복귀, 대기 포함).
차량 정책: Nearest Neighbor.
"""

import sys
from itertools import combinations
from src.tsp import tsp_cost, dist


class OnlineTSGSimulator:
    def __init__(self, customers, arrival_times, speed=1.0, depot=(0, 0)):
        self.customers = customers
        self.arrival_times = arrival_times
        self.speed = speed
        self.depot = depot
        self.positions = dict(customers)

    def run(self):
        depot = self.depot
        positions = self.positions
        early_times = self.arrival_times
        all_ids = sorted(self.customers.keys())

        arrivals = sorted(all_ids, key=lambda i: early_times[i])

        U_t = set()
        V_t = set()
        coalition_costs = {}
        events = []
        route = []

        vehicle_pos = depot
        current_time = 0.0
        arrival_idx = 0

        while len(V_t) < len(all_ids):
            # Process arrivals up to current_time
            while arrival_idx < len(arrivals):
                cid = arrivals[arrival_idx]
                if early_times[cid] <= current_time + 1e-9:
                    U_t.add(cid)
                    events.append({
                        'type': 'ARRIVE', 'time': early_times[cid],
                        'customer': cid, 'vehicle_pos': vehicle_pos
                    })
                    arrival_idx += 1
                else:
                    break

            # Record feasible coalitions
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
                                cost, _ = tsp_cost(depot, list(subset), positions,
                                                   early_times, self.speed)
                                coalition_costs[fs] = cost

            if not U_t:
                if arrival_idx < len(arrivals):
                    current_time = early_times[arrivals[arrival_idx]]
                    continue
                else:
                    break

            # NN: serve nearest unserved
            best_id = None
            best_d = float('inf')
            for cid in U_t:
                d = dist(vehicle_pos, positions[cid])
                if d < best_d:
                    best_d = d
                    best_id = cid

            travel_time = best_d / self.speed
            arrival_time_at_cust = current_time + travel_time
            serve_time = max(arrival_time_at_cust, early_times[best_id])

            current_time = serve_time
            vehicle_pos = positions[best_id]

            U_t.remove(best_id)
            V_t.add(best_id)
            route.append((best_id, serve_time))
            events.append({
                'type': 'SERVE', 'time': serve_time,
                'customer': best_id, 'vehicle_pos': vehicle_pos
            })

        # Return to depot - total time
        return_time = dist(vehicle_pos, depot) / self.speed
        total_time = current_time + return_time

        # Grand coalition
        grand = frozenset(all_ids)
        if grand not in coalition_costs:
            cost, _ = tsp_cost(depot, all_ids, positions, early_times, self.speed)
            coalition_costs[grand] = cost

        # Singletons
        for cid in all_ids:
            fs = frozenset([cid])
            if fs not in coalition_costs:
                cost, _ = tsp_cost(depot, [cid], positions, early_times, self.speed)
                coalition_costs[fs] = cost

        return {
            'events': events,
            'route': route,
            'coalition_costs': coalition_costs,
            'C_N': total_time,  # 총 소요 시간 = online cost
            'players': all_ids
        }
