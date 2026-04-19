# Review Response Summary — v2.1.2 → v2.1.3

Date: 2026-04-19
Scope: five post-review sync fixes; **no theoretical changes, no new
experiments**. Only narrative/claim alignment with existing v2.1.2 data.

## Fix 1: §7 Conclusion rewritten (Stale numerics removed)

**Before (v2.1.2)**:
- "empirical Core nonemptiness in 79 of 79 such instances"
- "factor of 3.21" (single scalar)
- "¯r** = 1.355" implicit
- Near-complement-only framing

**After (v2.1.3)**:
- "70 of 79 (k<n-1 empirical nonempty rate)" with explicit 9-case
  intermediate-mechanism caveat
- "factor of 3.56 relative to r** (¯r**=1.223) and 3.97 relative to
  r*** (¯r***=1.096)"
- Four-mechanism decomposition of 67 empty Cores: 37 single + 11
  balanced + 10 near + 9 intermediate
- Platform-design implication explicitly notes Observation 15's
  NN-only policy sensitivity (CI/BR produce zero intermediate cases)

## Fix 2: Figure 1 caption + script bug

**Before**:
- "Seven additional empty-Core instances" (v2.0 decomposition)
- `make_figures_v3.py` line 76: `f'... see Fig {None}'` (broken
  f-string interpolation yields literal "Fig None")

**After**:
- Caption: "10 near-complement (Remark 13) + 9 intermediate
  (Observation 15); 11 balanced-complement (Proposition 12) at/below
  diagonal. See §6.4 for full four-mechanism decomposition."
- Script: `see Appendix C` (literal valid cross-reference)
- fig2_r_vs_rstar.pdf regenerated

## Fix 3: README.md + REPRODUCIBILITY.md synchronized

### README.md — Sanity-checkpoint table

Before: 4 rows (Example 4, Thm 11 14/14, Cor 17 79/79, Sharpness 3.21).

After: 8 rows including
- Thm 11 fires: `37/37`
- Prop 12 fires: `57/57`
- Four-mechanism decomposition: `37 + 11 + 10 + 9 = 67`
- Cor 17 empirical: `70/79 (88.6%; 9 intermediate exceptions)`
- Sharpness: `3.56 (r̄*/r̄**)` and `3.97 (r̄*/r̄***)`
- Appendix C near-complement cases (10) and intermediate cases (9).

### REPRODUCIBILITY.md — Version header and Data Files

- Version header `v2.0 → v2.1.3`, 29 pages → 34, 599 instances → 596.
- Data Files section header `(v2.0)` → `(v2.1.3)`.
- Version History section extended to list v2.0, v2.1.0, v2.1.2,
  v2.1.3 with per-version changelog.

## Fix 4: §4.2 Nucleolus algorithmic-details tone-down (two-tier scope)

**Before** (strong claim, mismatched code):
"Our PuLP/CBC implementation identifies tight constraints via the
primal optimal and checks linear independence via Gaussian
elimination on the corresponding constraint coefficient vectors;
tight constraints that are linearly dependent on the currently fixed
set are deferred to subsequent LPs, matching the Kopelowitz–
Guajardo–Jörnsten procedure."

**After** (two-tier; matches nucleolus.py):
"This paper's Core-stability results (Sections 5 and 6) depend only
on the first-stage LP of the cascade: the Temporal Core is nonempty
iff ε₁★ ≤ 0, and its sign is independent of tie-breaking. For
Core-existence judgment, which is the focus of this paper, the
first-stage LP alone therefore suffices. For the full Temporal
Nucleolus point, the sequential cascade of Guajardo and Jörnsten
[2015] is applied. Our implementation adopts a simplified variant
that fixes all tight constraints at each stage, which is sufficient
under primal non-degeneracy; handling primal degeneracy via
rank-aware tight-constraint selection, due to Kopelowitz [1967] and
clarified by Guajardo and Jörnsten [2015], is a straightforward
extension and does not affect any of the Core stability results in
§5–6."

This aligns the paper's claim with `code/src/nucleolus.py`
(docstring: "This implementation fixes ALL tight constraints at each
stage (simplified Kopelowitz)").

## Fix 5: §6.8 Finding 3 + Table 8 footnote + §7 (ii) restricted-LP caveat

**Before**:
Finding 3: "every instance retains a nonempty Core"
§7 (ii): "Core nonemptiness observed in every instance"

These overclaim because `run_scaleup_v2.py` at n > 15 does not
enumerate full F (uses restricted LP from Appendix C); the absence of
observed violation is not a proof of Core nonemptiness.

**After**:
- Finding 3: "no Core violation is observed in our sampled LP for any
  of the 15 instances"; intermediate mechanism acknowledged as
  logically possible but not ruled out.
- Table 8 footnote added: "At n>15 the Core-existence judgment is
  made via the restricted LP of Appendix C rather than full 2^n-1
  enumeration; the absence of an observed violation in the sampled
  LP (e.g., all B_medium rows) does not constitute a proof of full
  Core nonemptiness."
- §7 (ii) expanded: "At n>15 the Core-existence judgment is based on
  the restricted LP of Appendix C rather than full 2^n-1
  enumeration, which limits the strength of the B_medium
  nonemptiness claim: absence of an observed violation in the
  sampled LP does not constitute a proof of full Core nonemptiness."

Pattern A and C scale-up rows are unaffected because their Core
emptiness claims are backed by Thm 11 / Prop 12 / restricted LP (all
certify empty, not nonempty).

## Verification (grep all 0)

| Pattern | v2.1.2 hits | v2.1.3 hits |
|---|---|---|
| `79 of 79` / `79/79` | >0 | **0** |
| `factor of 3.21` / `factor 3.21` | >0 | **0** |
| `1.355` | >0 | **0** |
| `14/14` / `14 of 14` | >0 | **0** |
| `7 additional` / `Seven additional` (paper/main.tex only) | >0 | **0** |
| `Fig {None}` / `Fig None` (make_figures_v3.py) | >0 | **0** |

## Build

- Pages: 34 (unchanged)
- LaTeX errors: 0
- Undefined references: 0
- Undefined citations: 0

## Invariants preserved

No modification to:
- Theorem 6, 11, 16, 18 statements + proofs
- Corollary 13, 19 statements + proofs
- Proposition 12 statement (already `Let n ≥ 2`)
- Observation 15 statement
- Remark 14, 17 statements
- Definition 2, 3
- Experimental data (policy_comparison_v2_full.csv, scaleup_v2.csv,
  sensitivity_v2.csv, seed123_core_check.csv unchanged)

## Artifacts

- `TSG_agent_submission_v2_1_3_20260419.zip` (737 KB, 65 files)
- `TSG_agent_submission_v2_1_3_20260419.sha256`
  SHA256: `5ee13578d2717e8272a19765507cfaccad4b19c72b25adbce03fe6034838863c`
- Git tag: `v2.1.3` on commit `2cf6397`
