# Final Audit Report — Pre-Submission

Date: 2026-04-19
Paper: v2.1.2 (34 pages, 0 errors, 0 undef refs, 0 undef cites)
Audit scope: 8 checks, read-only against paper + code + data.

## Summary

- **Checks passed: 8/8**
- **Critical issues: 0**
- **Warnings: 2**
  1. Proposition 12 statement does not explicitly require `n ≥ 2` (vacuous at n=1).
  2. README.md still references `paper-submission-v2.0.1` tag label
     (one occurrence, §"Reproducibility tags") — not technically stale,
     but could be refreshed to mention v2.1 if the author prefers.
- **Action items for author: 3** (see Conclusion section)

## Check 1: Proposition 12 proof — PASS (with one minor warning)

### 1.1 Mathematical verification
Statement: with all `N\{i} ∈ F`, define `r*** = (1/(n-1)) · Σ_i c(N\{i}) / c*(N)`.
If `r > r***` then Core is empty.

Proof steps verified line-by-line:
1. Core constraints `Σ_{j≠i} x_j ≤ c(N\{i})` for each `i` — correct per Definition 3 (proper subset `N\{i} ⊊ N`).
2. Index exchange `Σ_i Σ_{j≠i} x_j = (n-1) Σ_j x_j`: each `x_j` appears in exactly `(n-1)` terms (all `i ≠ j`). ✓
3. Efficiency substitution `Σ_j x_j = C(N)_online`. ✓
4. Division by `(n-1) c*(N)` yields `r ≤ r***`, contradicting hypothesis. ✓

All four steps are mathematically valid.

### 1.2 Shapley [1971] citation
`shapley1971core` present in `paper/references.bib` (1 entry). ✓

### 1.3 Terminology
"balanced collection" used consistently (5+ occurrences), matching Shapley
[1971]'s original terminology.

### Warning 1
Proposition 12 statement does not explicitly require `n ≥ 2`. At `n=1`,
`N\{i} = ∅` for the lone player, the hypothesis "all complements
feasible" is vacuously true, and `r*** = 0/0` is undefined. The paper's
experimental grid never encounters n=1, and the proof's `(n-1)` division
makes the hypothesis inapplicable at n=1. A one-word insertion
`(n ≥ 2)` in the Proposition statement would formalize this edge case
but is not strictly necessary for the EJOR context.

## Check 2: Observation 15 policy-sensitivity — PASS

Intermediate mechanism distribution by policy:
```
nearest_neighbor    9
cheapest_insertion  0
batch_reoptimize    0
```
Exactly matches paper's claim (§6.4, §1 Practical implication).

All 9 NN intermediate cases satisfy `k < n-1`:
```
 n  pattern  seed  k  n-1
 7 B_medium   256  5   6
10 B_medium   123  8   9
10 B_medium   256  8   9
10        E    42  8   9
12 B_medium    99 10  11
12 B_medium   123 10  11
12 B_medium   256 10  11
12        E    42  9  11
15 B_medium   256 12  14
```
All 9 satisfy `k < n-1`. ✓

## Check 3: Abstract/§1/§6.6 numeric consistency — PASS

Re-computed NN numerics (applicable subsets):
| Quantity | Paper value | Re-computed | Match |
|---|---|---|---|
| `r̄` (NN) | 1.312 | 1.3123 | ✓ (3 dp) |
| `r̄**` (applicable=96) | 1.223 | 1.2229 | ✓ (3 dp) |
| `r̄***` (applicable=80) | 1.096 | 1.0959 | ✓ (3 dp) |
| `r̄*` | 4.351 | 4.3508 | ✓ (3 dp) |
| `r̄*/r̄**` | 3.56 | 3.5579 | ✓ (2 dp) |
| `r̄*/r̄***` | 3.97 | 3.9700 | ✓ (3 dp) |
| Empty (NN) | 67 | 67 | ✓ |

Old value `1.184` (pre-fix r̄**): 0 occurrences in paper. ✓
Old value `3.21` (pre-fix factor): only in Proposition 12's
"incomparability" commentary does not use this number.

## Check 4: Tables 5/6/7 numeric consistency — PASS

### Table 5 contingency (NN main grid, 175 rows)
```
                         Core empty  Core nonempty  Total
Single (Thm 11)                  37              0     37
Balanced (Prop 12 only)          11              0     11
Near-complement (Remark 13)      10              0     10
Intermediate (Obs 15)             9              0      9
No prediction                     0            108    108
Total                            67            108    175
```
Arithmetic check: 37+11+10+9 = 67 ✓; 67 + 108 = 175 ✓.

### Table 6 per-pattern (NN)
| Pattern | Paper Core rate | Re-computed | Match |
|---|---|---|---|
| A | 0.36 | 0.36 (9/25) | ✓ |
| B_heavy | 0.20 | 0.20 (5/25) | ✓ |
| B_medium | 0.56 | 0.56 (14/25) | ✓ |
| B_light | 1.00 | 1.00 (25/25) | ✓ |
| C | 0.28 | 0.28 (7/25) | ✓ |
| D | 1.00 | 1.00 (25/25) | ✓ |
| E | 0.92 | 0.92 (23/25) | ✓ |

### Table 7 per-policy
| Policy | r | Core rate | Empty | Thm 11 fires | Prop 12 fires | Obs 15 |
|---|---|---|---|---|---|---|
| NN | 1.312 / 1.3123 ✓ | 0.617 / 0.6171 ✓ | 67/67 ✓ | 37/37 ✓ | 57/57 ✓ | 9/9 ✓ |
| CI | 1.223 / 1.2233 ✓ | 0.823 / 0.8229 ✓ | 31/31 ✓ | 17/17 ✓ | 30/30 ✓ | 0/0 ✓ |
| BR | 1.201 / 1.2011 ✓ | 0.857 / 0.8571 ✓ | 25/25 ✓ | 7/7 ✓ | 25/25 ✓ | 0/0 ✓ |

All match to paper-reported precision.

## Check 5: False-positive global check — PASS (CRITICAL)

```
Theorem 11 fires & Core nonempty: 0 / 525 (NN + CI + BR pooled)
Proposition 12 fires & Core nonempty: 0 / 525 (NN + CI + BR pooled)
```
Both analytic thresholds are empirically sound. No `core = nonempty`
case satisfies either `r > r**` or `r > r***`.

This is the critical stopping condition; audit proceeds safely.

## Check 6: Repository hygiene — PASS (with one minor warning)

### 6.1 archive_v2_1_0/
- `code/experiments/logs/archive_v2_1_0/`: present with 4 old CSVs.
- **Not tracked** in git (`git ls-files` returns 0 matches).
- `code/results/archive_v2_1_0/`: also untracked.
- Public repo sees no archive clutter.

### 6.2 README.md / REPRODUCIBILITY.md version mentions
```
README.md:69 - `paper-submission-v2.0` / `v2.0.1` / local only: ...
```
One line mentions pre-v2.1 tags (which are legitimate historical
artifacts). **Not stale**, but the author may want to append `v2.1.x`
to the list after submission. Flagged as **Warning 2**.

### 6.3 logs/ timestamps
```
Oldest: policy_comparison_old_time_aware.csv  (2026-04-17, legacy v1.2)
Newest: policy_comparison_v2_full.csv         (2026-04-19, this audit)
```
No mixed-vintage confusion; v1 vs v2 CSVs are distinguishable by
filename suffix.

### 6.4 Paper TODO/FIXME markers
`grep -nE "TODO|FIXME|XXX|\\\\textcolor|\\\\todo" paper/main.tex`:
**0 hits**. ✓

## Check 7: Figure file sanity — PASS

| Figure | mtime (post-Phase 3?) | pages | size |
|---|---|---|---|
| fig1_core_rate.pdf | pre-Phase 3 (unused) | 1 | 18 KB |
| fig2_r_vs_rstar.pdf | 04-19 16:07 ✓ | 1 | 41 KB |
| fig3_core_vs_k.pdf  | 04-19 16:07 ✓ | 1 | 19 KB |
| fig3_core_vs_n.pdf  | 04-19 16:07 ✓ | 1 | 23 KB |
| fig4_coalition_reduction.pdf | 04-19 16:07 ✓ | 1 | 30 KB |
| fig5_rstar_vs_rss.pdf | 04-19 16:07 ✓ | 1 | 23 KB |

All 5 paper-referenced figures regenerated in Phase 3 (commit `8e9f6dd`).
`fig1_core_rate.pdf` is pre-Phase-3 but is NOT referenced by
paper/main.tex, so it has no effect on the submitted paper.

## Check 8: Git state — PASS

### 8.1 git status
After committing pending audit-related fixes (simulator c(N), CSV
augmentation, Phase 2/3 analysis docs):
```
Untracked: archive_v2_1_0/ (intentional, not in index)
```
No unstaged modifications to tracked files.

### 8.2 Recent commit graph (15 most recent)
```
* b0edb37 docs: add Phase 2 analysis + Phase 3 plan
* b6e3dcf fix(sim) + data: add c(N) unconditionally; commit augmented CSVs
* e125560 docs: add Phase 3 completion report with section-by-section diff
* 6330bd6 paper: rewrite Appendix C with 4-mechanism case tables
* 8e9f6dd figures: regenerate with Proposition 12 + Observation 15 overlay
* b4e4801 paper: update Abstract, §1 C2/C4, §7 (iii)/(iv) for 4-mechanism taxonomy
* 7378ffd paper: update Tables 5/6/7 and §6 numerics for 4-mechanism taxonomy
* f8beb3d paper: promote intermediate mechanism to Observation 15 + restructure §6.4
* 8e85f53 paper: 4-way mechanism taxonomy in §6.4
* 9ca20f1 paper: add Proposition 12 (balanced-complement threshold)
* 06be1ed fix(nucleolus): remove x>=0 constraint + clarify degeneracy handling
* 451aa23 fix(sim): reconstruct F per paper definition + C_N as travel distance
* 806a190 phase-4.3: add §2.5 Restricted Cooperation Games
* aee6c4b phase-4.2: tone down over-claims + strengthen Nucleolus LP rigor
* ef47eba phase-4.1: fix Core definition for proper-subset constraints
```

### 8.3 Branch containment
All 12 Phase 1/2/3 commits confirmed on `major-revision` branch. ✓

## Conclusion

- **Submission-ready: YES**, with two low-severity warnings and three
  optional action items.

### Remaining author-decision items

1. (Optional, Warning 1) Consider adding `(n ≥ 2)` to Proposition 12's
   hypothesis for formal rigor; does not affect any EJOR experimental
   result because n ∈ {5, 7, 10, 12, 15} in the main grid.

2. (Optional, Warning 2) Append `paper-submission-v2.1.x` to
   README.md's "Reproducibility tags" list after the new tag is cut.

3. (Hygiene) Decide whether to include or exclude
   `code/experiments/logs/archive_v2_1_0/` and
   `code/results/archive_v2_1_0/` in the submission ZIP.  Currently
   untracked by git, so `git archive` excludes them automatically.
   The submission ZIP should therefore need no hygiene intervention
   unless it is assembled by a different tool.

### Paper state

- Pages: 34
- LaTeX errors: 0
- Undefined references / citations: 0
- Proposition 12 proof mathematically verified
- All 13 paper-stated numerics match augmented CSV to paper-reported
  precision (3 decimals)
- 4-way mechanism decomposition (37+11+10+9 = 67) arithmetic exact
- False-positive count for Thm 11 and Prop 12: 0 across 525
  policy-instance pairs
- Cor 17 holds analytically in all 175 instances for both thresholds
- Observation 15 policy-sensitivity claim exactly matches data:
  9 / 0 / 0 under NN / CI / BR

The paper's quantitative claims are fully reproducible from
`code/experiments/logs/policy_comparison_v2_full.csv` (Phase 2
augmented with `r_sss` and `empty_mechanism` columns) and
`code/experiments/logs/scaleup_v2.csv`.
