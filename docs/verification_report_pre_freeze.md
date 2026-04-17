# Pre-Freeze Reproduction Verification Report

**Date**: 2026-04-17
**Git HEAD**: (report-only, no modifications)
**Data sources**: policy_comparison.csv (525 rows), scaleup.csv (45 rows), main.tex (654 lines)

## Summary
| Section | Checkpoints | Pass | Fail | Notes |
|---|---|---|---|---|
| [A] Solomon (pre-verified) | 5 | 5 | 0 | separately confirmed |
| [B] Thm 11 contingency | 5 | 5 | 0 | exact integer match |
| [C] Corollary 16 regimes | 3 | 3 | 0 | rates match within tolerance |
| [D] Pattern-level Table 6 | 8 | 8 | 0 | all per-pattern values match rounded |
| [E] Policy Table 7 | 3 | 3 | 0 | means & counts match |
| [F] Scale-up Table 8 | 9 | 9 | 0 | all 9 cells match |
| [G] Derived | 2 | 2 | 0 | ratio 3.24 confirmed; LKH 0.000% = claim only |
| **Total** | **35** | **35** | **0** | |

## Per-checkpoint detail

### [B] Theorem 11 contingency table (tab:thm5, 66 applicable instances)
Filter: `policy == 'nearest_neighbor'`, applicable = `r_ss.notna()`.

| ID | Paper | Reproduced | Δ | Status |
|---|---|---|---|---|
| B1 | 12 | 12 | 0 | PASS |
| B2 | 7  | 7  | 0 | PASS |
| B3 | 19 | 19 | 0 | PASS |
| B4 | 47 | 47 | 0 | PASS |
| B5 | 66 | 66 | 0 | PASS |

### [C] Corollary 16 regimes
Filter: `policy == 'nearest_neighbor'`, 175 instances partitioned by `k` vs `n-1`.

| ID | Regime | Paper | Reproduced | Status |
|---|---|---|---|---|
| C1 | k<n-1  | 95/95, rate 1.00 | 95/95, rate 1.0000 | PASS |
| C2 | k=n-1  | 14/14, rate 1.00 | 14/14, rate 1.0000 | PASS |
| C3 | k=n    | 47/66, rate ~0.71 | 47/66, rate 0.7121 | PASS (Δ=0.002) |

### [D] Pattern-level Table 6 (tab:pattern, NN only, 7 patterns)

| Pattern | Core rate (paper / repro) | r̄ (paper / repro) | r̄** (paper / repro) | F-ratio (paper / repro) | applicable (paper / repro) | Status |
|---|---|---|---|---|---|---|
| A  | 0.36 / 0.360 | 1.125(0.102) / 1.125(0.102) | 1.181(0.059) / 1.181(0.059) | 1.000 / 1.000 | 25/25 / 25/25 | PASS |
| B1 | 1.00 / 1.000 | 1.286(0.146) / 1.286(0.146) | 1.528(0.124) / 1.528(0.124) | 0.332 / 0.332 | 10/25 / 10/25 | PASS |
| B2 | 1.00 / 1.000 | 1.312(0.163) / 1.312(0.163) | 1.691(0.064) / 1.691(0.064) | 0.158 / 0.158 |  2/25 /  2/25 | PASS |
| B5 | 1.00 / 1.000 | 1.808(0.328) / 1.808(0.328) | --- / NaN (no applicable) | 0.061 / 0.061 | 0/25 / 0/25 | PASS |
| C  | 0.88 / 0.880 | 1.199(0.149) / 1.199(0.149) | 1.363(0.169) / 1.363(0.169) | 0.512 / 0.512 | 25/25 / 25/25 | PASS |
| D  | 1.00 / 1.000 | 1.415(0.188) / 1.415(0.188) | --- / NaN (no applicable) | 0.101 / 0.101 | 0/25 / 0/25 | PASS |
| E  | 1.00 / 1.000 | 1.370(0.208) / 1.370(0.208) | 1.606(0.043) / 1.606(0.043) | 0.207 / 0.207 | 4/25 / 4/25 | PASS |

**D8 — Overall (NN, 175 instances)**: Core 0.89 / **0.891**; r̄ 1.359 / **1.359**; r̄** 1.344 / **1.343** (Δ=0.001, tolerance applied); F-ratio 0.339; applicable 66/175 / **66/175**. **PASS**

### [E] Table 7 — dispatch policy (tab:policy)

| ID | Policy | r̄ (paper / repro) | Core rate (paper / repro) | Empty (paper / repro) | Fires (paper / repro) | Applicable | Status |
|---|---|---|---|---|---|---|---|
| E1 | NN | 1.359 / 1.359 | 0.891 / 0.891 | 19 / 19 | 12 / 12 | 66 / 66 | PASS |
| E2 | CI | 1.276 / 1.276 | 0.977 / 0.977 |  4 /  4 |  1 /  1 | 66 / 66 | PASS |
| E3 | BR | 1.257 / 1.257 | 1.000 / 1.000 |  0 /  0 |  0 /  0 | 66 / 66 | PASS |

### [F] Table 8 — scale-up (tab:scaleup, NN only, 45 instances)

| ID | Pattern / n | Core (paper / repro) | r̄ (paper / repro) | r̄** (paper / repro) | k̄ (paper / repro) | Status |
|---|---|---|---|---|---|---|
| F1 | A, n=20  | 0/5 / 0/5 | 1.167 / 1.167 | 1.119 / 1.119 | 20.0 / 20.0 | PASS |
| F2 | A, n=30  | 0/5 / 0/5 | 1.187 / 1.187 | 1.096 / 1.096 | 30.0 / 30.0 | PASS |
| F3 | A, n=50  | 0/5 / 0/5 | 1.211 / 1.211 | 1.068 / 1.068 | 50.0 / 50.0 | PASS |
| F4 | B2, n=20 | 5/5 / 5/5 | 1.762 / 1.762 | --- / NaN      |  8.4 /  8.4 | PASS |
| F5 | B2, n=30 | 5/5 / 5/5 | 1.804 / 1.804 | --- / NaN      | 10.0 / 10.0 | PASS |
| F6 | B2, n=50 | 5/5 / 5/5 | 2.128 / 2.128 | --- / NaN      | 10.4 / 10.4 | PASS |
| F7 | C, n=20  | 0/5 / 0/5 | 1.335 / 1.335 | 1.119 / 1.119 | 19.8 / 19.8 | PASS |
| F8 | C, n=30  | 0/5 / 0/5 | 1.282 / 1.282 | 1.096 / 1.096 | 30.0 / 30.0 | PASS |
| F9 | C, n=50  | 0/5 / 0/5 | 1.282 / 1.282 | 1.068 / 1.068 | 50.0 / 50.0 | PASS |

### [G] Derived claims

| ID | Claim | Paper | Reproduced | Status |
|---|---|---|---|---|
| G1 | r̄\* / r̄\*\* factor | 3.24 (paper line 528) | 4.351 / 1.344 = 3.237 | PASS (tolerance ±0.01). Note: task-prompt wrote this as r̄\*\*/r̄\* but paper's "factor of 3.24" is r̄\*/r̄\*\*; mathematically 1.344/4.351≈0.309 and 4.351/1.344≈3.237. Paper direction is consistent with the data. |
| G2 | LKH calibration: 0.000% relative error vs Held–Karp at n=15 on 15 instances (paper line 569, line 620) | 0.000% | Claim only, not independently checked — calibration CSV is not among the three provided data files; scaleup.csv has `c_star_source` column showing `held_karp` at n=20 and LKH thereafter, but no side-by-side relative-error values | PASS (as "claim only" per task spec) |

## Discrepancies (if any)
None beyond sub-tolerance rounding:
- D8 overall r̄** = 1.343 computed vs 1.344 in paper (Δ=0.001, within ±0.01). Tolerance applied.
- C3 rate 0.7121 vs "~0.71" in paper (Δ=0.002, within ±0.01). Tolerance applied.

## Decision
- [x] All 35 pass → **Freeze OK**
- [ ] Some fail → stop, report to user

## Self-assessment
- Data files read: `policy_comparison.csv` (525 rows, 15 cols), `scaleup.csv` (45 rows, 16 cols). `theorem5_validation.csv` not needed since primary CSV is sufficient and authoritative.
- Paper sections parsed: Table tab:thm5 (lines 450–465), Corollary 16 verification prose (line 478), Table tab:pattern (lines 492–512), Table tab:policy (lines 544–558), Table tab:scaleup (lines 571–595), sharpness ratio 3.24 (line 528), LKH calibration 0.000% (lines 569, 620).
- Confidence: **High**. All 30 numerical checkpoints reproduce exactly or within the stated tolerance. The G2 LKH calibration is a claim in the paper body for which no raw side-by-side data is in-scope; flagged per task spec, not counted as fail.

VERIFICATION_PASS checkpoints=30/30 solomon_separate=5/5
