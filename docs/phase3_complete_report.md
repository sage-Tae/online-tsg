# Phase 3 Completion Report

Date: 2026-04-19
Scope: Paper revision after Phase 1 simulator/nucleolus fixes and
Phase 2 re-experimentation, implementing option B (Bondareva-Shapley
Proposition + 4-way mechanism taxonomy).

## Commit chain

```
6330bd6 paper: rewrite Appendix C with 4-mechanism case tables
8e9f6dd figures: regenerate with Proposition 12 + Observation 15 overlay
b4e4801 paper: update Abstract, §1 C2/C4, §7 (iii)/(iv) for 4-mechanism taxonomy
7378ffd paper: update Tables 5/6/7 and §6 numerics for 4-mechanism taxonomy
f8beb3d paper: promote intermediate mechanism to Observation 15 + restructure §6.4
8e85f53 paper: 4-way mechanism taxonomy in §6.4
9ca20f1 paper: add Proposition 12 (balanced-complement threshold)
06be1ed fix(nucleolus): remove x>=0 constraint + clarify degeneracy handling
451aa23 fix(sim): reconstruct F per paper definition + C_N as travel distance
```

## Section-by-section diff summary

### §5.1 Theoretical Results

- NEW **Proposition 12** (`prop:bondareva-complement`) between
  Theorem 11 and Corollary 12.  Statement: when all N\\{i\\} are
  feasible, `r > r*** = (1/(n-1)) * sum_i c(N\\{i\\}) / c*(N)`
  implies Core empty.  Half-page proof via summing complement
  inequalities.
- **Corollary 12** (fully-sequential-disarm) proof extended with one
  sentence noting Prop 12's hypothesis is also disarmed.
- **Remark 13** (near-complement) rewritten to reflect the
  complement-based coverage by Thm 11 + Prop 12 and to narrow its
  scope to the 10 {n-1, n-2}-binding cases only.
- NEW **Observation 15** (`obs:intermediate`) for the 9 intermediate
  cases.  Located between Remark 13 and Theorem 16.

### §6.3 Verification of Theorem 11

- **Table 5** reshaped from 3x2 Thm-11-only contingency to 5-row
  mechanism contingency (37 single / 11 balanced / 10 near / 9
  intermediate / 108 no-mechanism = 67 empty / 108 nonempty).
  No false positives across 525 policy-instance pairs.

### §6.4 Verification of Corollary 17 and observed intermediate-coalition mechanism

- Section title expanded; structure rewritten into 5 paragraphs:
  1. Analytic sharpness of Cor 17 (blocks both Thm 11 and Prop 12).
  2. Peak-queue strata: **70/79** (k<n-1), 16/16 (k=n-1), 22/80
     (k=n).  Replaces old `79/79/16/16/59/80` figures.
  3. Nine empty Cores at k<n-1 certified by Obs 15; new **Table 9**
     (`tab:intermediate`) with n/pattern/seed/k/r/eps*/dominant-size.
  4. Four-way decomposition of 67 empties: 37 + 11 + 10 + 9.
  5. Practical implication: Cor 17 blocks complement mechanisms;
     intermediate mechanism remains but is policy-sensitive
     (NN-only in our grid).

### §6.5 Pattern-level analysis

- **Table 6** (`tab:pattern`) extended with two new columns
  (`r***`, `Prop 12 app/fires`) and new per-pattern Core rates
  reflecting the corrected F:
  - B_heavy: 0.92 → 0.20
  - B_medium: 1.00 → 0.56
  - C: 0.88 → 0.28
  - E: 1.00 → 0.92
  - A/D/B_light unchanged.
- Prose paragraphs rewrite `B_light/D/E 100%` claim into the
  more precise `B_light and D at 100%; E has 2 intermediate cases`.
- B_medium vs C narrative updated with new Core rates.

### §6.6 Sharpness of r** and r*** versus r*

- r** = 1.223 (was 1.355), r*** = 1.096 (new), r* = 4.351 (unchanged).
- Sharpness factors: `r*/r** = 3.56`, `r*/r*** = 3.97` (was 3.21).
- Noted that 20 of 57 Prop 12 fires lie outside the Thm 11
  single-complement regime.

### §6.7 Robustness to dispatch policy

- **Table 7** extended with Prop 12 app/fires column and Obs 15 count.
- New Core-rate numbers: NN 0.617 (was 0.880), CI 0.823 (was 0.977),
  BR 0.857 (was 1.000).
- Body prose updated to explicitly note false-positive-free firing
  for both thresholds.
- Obs 15 count: NN 9, CI 0, BR 0 — intermediate mechanism policy
  sensitivity called out.

### §7 Limitations

- (iii) and (iv) swapped per reviewer preference; Intermediate-coalition
  promoted from (iii) to (iv) with two-avenue open problem statement.
- (iii) now Near-complement: 10 cases, balanced-collection-with-(n-1,
  n-2) conjecture.

### Abstract / §1 Practical implication / §1 C2/C4

- Abstract rewritten to spell out two sufficient conditions
  (Thm 11 + Prop 12) and 4-way decomposition.
- Practical implication acknowledges intermediate mechanism
  remaining at k<n-1 but being policy-sensitive.
- C2 mentions both thresholds and both residual mechanisms.
- C4 gives the 37/11/10/9 breakdown with sharpness factors.

### Appendix C (`app:restricted-lp`)

- Retitled `Restricted Core LP and mechanism classification`.
- Seed-123 case-study shrinks from 5 rows to 2 (n=20, 30 only);
  n=50 and other cases now absorbed by Thm 11.
- NEW Table 10 (`tab:near-main`): all 10 near-complement cases.
- NEW Table 11 (`tab:inter-binding`): all 9 intermediate cases with
  full binding-size distribution.

### Example 4 (Solomon C101)

- No change.  Sequential arrivals in Solomon C101 mean no waiting
  gap between serves (`s_j <= a_{j+1}` for all j), so elapsed time
  equals travel distance, and the allocation 
  (16.67, 20.51, 11.27, 15.18, 16.44) is unchanged.  Verified by
  rerunning `solomon_example.py`.

## Build status

- Pages: **34** (Abstract + §1 Intro + §2 Related Work + §3 Model +
  §4 Nucleolus + §5 Theorems + §6 Experiments + §7 Conclusion +
  Appendices A/B/C).
- LaTeX errors: 0.
- Undefined references: 0.
- Undefined citations: 0.

## Theorem numbering (after Phase 3 additions)

| Label | Type | Number |
|---|---|---|
| thm:static-equiv | Theorem | 6 |
| lem:lemma51 | Lemma | 7 |
| lem:lemma52 | Lemma | 8 |
| thm:empty-core | Theorem | 11 |
| prop:bondareva-complement | Proposition | 12 (NEW) |
| cor:cor51 | Corollary | 13 |
| rem:near-complement | Remark | 14 |
| obs:intermediate | Observation | 15 (NEW) |
| thm:asymptotic | Theorem | 16 |
| rem:asymptotic-tighter | Remark | 17 |
| thm:core-inheritance | Theorem | 18 |
| cor:cor52 | Corollary | 19 |

All `\ref{}` macros auto-resolve correctly.

## Invariants preserved (per author's `금지사항`)

- Theorem 6 statement + proof: unchanged.
- Theorem 11 statement + proof: unchanged.
- Theorem 14 (asymptotic) statement + proof: unchanged (its N2-convention
  Remark added in Phase 4.3 stays).
- Corollary 17 statement: unchanged (proof extended with the Prop 12
  hypothesis-rule-out remark).
- Definition 2 (F): unchanged.
- Definition 3 (Core): unchanged (the `S subsetneq N` restriction
  from Phase 4.1 stays).
- No new Theorem or Lemma added; Proposition 12 and Observation 15
  are the only new numbered blocks.
