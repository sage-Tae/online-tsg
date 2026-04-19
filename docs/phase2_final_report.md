# Phase 2 Final Report — Post-Correction Experiment Results

Date: 2026-04-19
Scope: results after Phase 1 fixes to `simulator.py`, `policy_simulator.py`
       (F reconstruction + C_N = travel distance), `nucleolus.py`
       (x>=0 removed), plus `r_sss` and `empty_mechanism` augmentation.

## Headline numbers (NN, 175 main grid)

| Metric | v2.0.3 (pre-fix) | v2.1.1 (post-fix) |
|---|---|---|
| Theorem 11 applicable | 80 | 96 |
| Theorem 11 fires | 14 | **37** |
| Core empty | 21 | **67** |
| Core rate | 0.880 | **0.617** |
| mean r | 1.326 | 1.312 |
| mean r** (applicable) | 1.355 | 1.184 |
| mean r*** (balanced, NEW) | n/a | 1.096 |
| mean r* | 4.351 | 4.351 (unchanged) |
| r* / r** | 3.21 | 3.67 |

## 4-way mechanism distribution

| Policy | core_nonempty | single_complement | balanced_complement | near_complement | intermediate | total empty |
|---|---|---|---|---|---|---|
| NN  | 108 | 37 | 11 | 10 | 9 | 67 |
| CI  | 144 | 17 |  4 | 10 | 0 | 31 |
| BR  | 150 |  7 |  4 | 14 | 0 | 25 |

- **intermediate mechanism appears only under NN** (9/175) — CI and BR escape it.
- NN's 67 empties break into 37 single + 11 balanced + 10 near + 9 intermediate.

## Per-pattern Core rate (NN)

| Pattern | Core rate | single | balanced | near | intermediate |
|---|---|---|---|---|---|
| A        | 0.36 | 9 | 3 | 4 | 0 |
| B_heavy  | 0.20 | 15 | 3 | 2 | 0 |
| B_medium | 0.56 | 3 | 1 | 0 | **7** |
| B_light  | 1.00 | 0 | 0 | 0 | 0 |
| C        | 0.28 | 10 | 4 | 4 | 0 |
| D        | 1.00 | 0 | 0 | 0 | 0 |
| E        | 0.92 | 0 | 0 | 0 | **2** |

- The 9 intermediate cases concentrate in **B_medium (7)** and **E (2)**.
- B_light and D remain 100% Core-nonempty — queue stays shallow, no
  coalition above size 1 (rarely above size 2) is feasible.
- B_heavy and C drop dramatically from previous v2.0.3 values (0.92 and
  0.88 respectively) — the new F surfaces many complement violations
  that the old dispatch-time enumeration missed.

## r_sss (balanced-complement threshold, NEW)

Definition: `r_sss = (1/(n-1)) * sum_i c(N\{i}) / c*(N)`, defined when
every complement `N\{i}` is feasible (240/525 rows, 80 per policy).

Bondareva-Shapley check: `r > r_sss` ⇒ Core empty.
- 112 of 240 applicable rows satisfy `r > r_sss`.
- **0 false positives** — all 112 observed Core-empty.
- 51 of 112 are detected by `r > r_sss` but **not** by Thm 11
  (`r <= r_ss`). These are the balanced + near-complement cases that
  single-complement Thm 11 misses.

Relation to r_ss: empirically `mean r_sss = 1.096 < mean r_ss = 1.184`;
r_sss is a *tighter* threshold since averaging across complements
picks up balanced-collection violations that single-complement min misses.

## Scale-up (n ∈ {20, 30, 50})

### (a) 4-way distribution in scale-up

| Pattern | n | Thm 11 fires | Core nonempty | Notes |
|---|---|---|---|---|
| A        | 20 | 3/5 | 0/5 | seeds {99, 123} Thm 11 vacuous, Core empty |
| A        | 30 | 4/5 | intractable* | seed 123 Thm 11 vacuous |
| A        | 50 | 5/5 | intractable* | all fire incl. seed 123 |
| B_medium | 20 | 0/5 | 5/5 | r_ss undefined (no complement feasible) |
| B_medium | 30 | 0/5 | 5/5 | same |
| B_medium | 50 | 0/5 | 5/5 | same |
| C        | 20 | 5/5 | 0/5 | all fires |
| C        | 30 | 5/5 | 0/5 | all fires |
| C        | 50 | 5/5 | 0/5 | all fires |

*: for A at n ≥ 30 the Core LP has 2^n constraints, intractable to
enumerate.  The restricted LP (Appendix C path) certifies emptiness;
Thm 11 certifies the 4 of 5 seeds at n=30 that fire and all 5 at n=50.

### (b) Pattern C phase-transition check (reviewer's question)

Pattern C at n=15 (main grid): Core rate 1.00 (all 5 seeds nonempty),
r = 1.199 < r** = 1.363 on average.  At n=20 (scale-up): **Core rate
0.00**, r = 1.334 > r** = 1.119.

Phase transition confirmed between n=15 and n=20 as r overtakes r**.

### (c) Seed 123 status

| Pattern | n | r | r** | fires | Current mechanism |
|---|---|---|---|---|---|
| A | 20 | 1.077 | 1.112 | False | near-/intermediate (prev. Appendix C case) |
| A | 30 | 1.038 | 1.088 | False | same (LP intractable) |
| A | 50 | 1.306 | 1.081 | **True** | single_complement (now absorbed) |
| C | 20 | 1.350 | 1.112 | True | single_complement |
| C | 30 | 1.210 | 1.088 | True | single_complement |
| C | 50 | 1.346 | 1.081 | True | single_complement |

The v2.0.3 paper used seed 123 as the Appendix C "near-complement"
case study at n ∈ {20, 30, 50}.  With corrected F:
- At **n=50**, seed 123 is now absorbed by Thm 11 fires.
- At **n=20, 30**, seed 123 remains Thm 11 vacuous; the restricted LP
  still certifies emptiness.
- Pattern C seed 123 fires at every scale-up n (moved out of Appendix C).

Only **two** genuine "near-complement beyond Thm 11" cases at seed 123
remain in scale-up (n=20, 30 under A).

### (d) Pattern A Thm 11 fires n=30/50

- n=30: 4/5 (seed 123 still doesn't fire)
- n=50: **5/5** — the paper's current claim that all A n=50 seeds fire
  is now correct under the fixed F.

### (e) B_medium intermediate mechanism at scale-up

Under the current `run_scaleup_v2.py`, Core LP for B_medium is
effectively restricted to `{singletons, feasible complements, N}`
(complements are infeasible here, so only singletons + N remain),
which makes Core trivially nonempty.  **This path does not detect
intermediate mechanism at scale-up.**

Main-grid evidence (n=12 B_medium seed=99/123/256, n=15 B_medium
seed=256) shows intermediate-coalition Core emptiness at n≤15.  To
probe whether this persists at larger n, `run_scaleup_v2.py` would
need to sample intermediate-size coalitions (as `run_seed123_check.py`
already does).  Not executed in this phase.

**Status**: B_medium scale-up Core nonempty is a *limit of the
scale-up LP*, not a verified Core-nonemptiness.  Recommend including
this caveat in Phase 3 narrative.

## False-positive checks (all passed)

| Policy | Thm 11 fires | Core empty | False positives |
|---|---|---|---|
| NN | 37 | 37 | 0 |
| CI | 17 | 17 | 0 |
| BR |  7 |  7 | 0 |

| Threshold | applicable | fires | Core empty | False positives |
|---|---|---|---|---|
| r_ss  | 240 |  61 |  61 | 0 |
| r_sss | 240 | 112 | 112 | 0 |

Both single-complement and balanced-complement thresholds are
empirically sound (no false positives).

## Scale invariance

Not re-verified in this phase; `run_sensitivity_v2.py` not yet
re-executed against the corrected simulator.  The scale invariance
property is a function of `(L, v, tau)` joint scaling and is unchanged
by the F reconstruction fix (same simulation, same F per configuration).
Expected to remain bit-identical; to be confirmed after running
`run_sensitivity_v2.py`.

## Data integrity

- `experiments/logs/policy_comparison_v2_full.csv`: 525 rows,
  columns: base 18 + `r_sss` + `empty_mechanism` (20 cols total).
- `experiments/logs/scaleup_v2.csv`: 45 rows unchanged in schema.
- Archive: `experiments/logs/archive_v2_1_0/` holds pre-fix CSVs.
