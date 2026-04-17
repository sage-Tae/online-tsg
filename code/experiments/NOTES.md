# Experiment notes

## rev-consistency-numbers (175-instance aggregation fix)

The legacy `experiments/run_all.py` pipeline skips `static_nucleolus`
when `n > 8` (LP would enumerate $2^n-1$ coalitions), leaving
`C_N_static = None` and hence `r = NaN`, `r_star = NaN` in the
resulting `results/summary.csv`. `pandas.mean()` silently drops NaNs,
so the paper's original "Table 6" aggregates ($\bar r^* = 3.320$,
$\bar r^{**} = 1.283$, etc.) were actually computed over the 70
instances with $n \in \{5, 7\}$ only, not the declared 175.

The full-175 re-run in `experiments/run_policy_comparison.py` computes
$c^\ast(N)$ directly via `src.tsp.exact_tsp` for every instance, so all
175 rows have valid $r$ and $r_\ast$ values.

## c(S) definition fix (β): time-aware → pure-distance

**Cause.** The legacy `exact_tsp` was time-aware (took `max(arrival,
travel) + waiting` accumulation), which is inconsistent with the
paper's Section 3.2 definition ("c(S) irrespective of time"). This was
scenario Case 1 in the diagnostic.

**Action.** Replaced `exact_tsp` with a pure-distance Held--Karp
(shortest Hamiltonian cycle on the depot + customers set). The
time-aware function was renamed `exact_tsp_time_aware` and is used
only inside the online simulator for realized $C(N)_{\text{online}}$
accumulation.

**Impact summary** (175-instance NN, time-aware vs pure-distance):

| quantity          | time-aware c*  | pure-distance c* |
|-------------------|----------------|------------------|
| Core rate         | 89.1%          | 89.1%   (no change) |
| Thm 11 applicable | 66             | 66      (no change) |
| Thm 11 fires      | 12             | 12      (no change) |
| empty Core        | 19             | 19      (no change) |
| k-regime parts    | 95 / 14 / 66   | 95 / 14 / 66 (no change) |
| $\bar r$ (NN)     | 1.191          | 1.359  |
| $\bar r^{**}$     | 1.343          | 1.344  |
| $\bar r^{*}$      | 4.945          | 4.351  |
| ratio $r^*/r^{**}$| 3.68           | 3.24   |

**Interpretation.** Core existence structure is invariant to the c(S)
definition; only $\bar r$ shifts upward (numerator is time-aware
$C_{\text{online}}$, denominator is pure-distance $c^*$). The sequential
patterns (B5 especially, $\bar r = 1.81$) make the "big r but Core
survives" observation sharper: even when arrivals cause substantial
idling the complement mechanism stays blocked by $k < n-1$.

The previous time-aware CSV is backed up as
`experiments/logs/policy_comparison_old_time_aware.csv`.
