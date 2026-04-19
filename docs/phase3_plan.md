# Phase 3 Plan — Paper Revision After Phase 1 Code Corrections

Status: **PLAN ONLY.** No `paper/main.tex` or `paper/references.bib`
modification in this document; that is deferred to Phase 3 proper
after author review.

## Numbers to update (from `phase2_final_report.md`)

### Abstract and §1 C4

| Claim (v2.0.3 paper text) | v2.0.3 value | v2.1.1 value |
|---|---|---|
| "Thm 11 applicable" (NN main) | 80 | 96 |
| "Thm 11 predicts emptiness in _ instances" | 14 | **37** |
| "all confirmed empty (no false positives)" | 14/14 | 37/37 |
| "79 of 79" (k<n-1 safeguard) | 79/79 | (re-check, see §6.4) |
| "mean threshold r** = _" | 1.355 | **1.184** |
| "sharper than r* by factor _" | 3.21 | **3.67** (4.351 / 1.184) |
| Seven near-complement cases | 7 | (new 4-way decomposition needed) |

### §6.6 Sharpness

- `r_ss_mean` : 1.355 → **1.184**
- `r_star_mean`: 4.351 → 4.351 (coordinate-only quantity; unchanged)
- sharpness factor r*/r**: 3.21 → **3.67**
- NEW: introduce `r_sss = (1/(n-1)) * sum c(N\{i}) / c*(N)` with
  `r_sss_mean ≈ 1.096`, a tighter threshold than `r_ss`.

### §6.4 Corollary 16 verification

k-regime partition needs recount under corrected F.  Pending re-count
with:
- k < n-1 count  : should be similar (k is a dispatch quantity,
                   mostly unaffected by F reconstruction)
- k = n-1 count
- k = n count and Core-rate within it

From v2.0.3: k<n-1: 79/175 Core 100%, k=n-1: 16/175 Core 100%,
k=n: 80/175 Core 73.8%.  With corrected F the k=n regime's Core-rate
likely drops (more empties detected); k<n-1 may also now show some
empties due to intermediate mechanism (e.g. B_medium n=12 seed=99 has
k=10 < n-1=11, Core empty via intermediate).

### §6.5 Table 6 (per-pattern, NN)

Paper currently states B_medium, B_light, D, E are 100% Core-stable.
This is false under corrected F for B_medium and E:

| Pattern | Old Core rate (v2.0.3) | New Core rate (v2.1.1) |
|---|---|---|
| A        | 0.36 | 0.36 (unchanged) |
| B_heavy  | 0.92 | **0.20** |
| B_medium | 1.00 | **0.56** (7 intermediate + 3 single + 1 balanced) |
| B_light  | 1.00 | 1.00 (unchanged) |
| C        | 0.88 | **0.28** |
| D        | 1.00 | 1.00 (unchanged) |
| E        | 1.00 | **0.92** (2 intermediate) |

This is the **largest narrative change**: B_heavy and C shift from
"mostly safe" to "mostly empty" under new F.

### §6.7 Table 7 (dispatch-policy robustness)

| Policy | r_mean | Core rate | empty | Thm 11 fires |
|---|---|---|---|---|
| BR | 1.201 | 0.857 | 25 | 7 |
| CI | 1.223 | 0.823 | 31 | 17 |
| NN | 1.312 | 0.617 | 67 | 37 |

Monotonic ordering (worse policy → more empty Cores) holds, but
absolute numbers shift.

### §6.8 Table 8 + Findings

Scale-up table Pattern A row "5/5 fire at n=50" stays; the "all r_i
exceed r**" Table 8 caption (already in v2.0.2 reviewer fix) remains
accurate.  Footnote markers remain.

Finding 4 (near-complement at seed 123) needs rewriting:
- Old: "At seed 123 under Pattern A, Thm 11 vacuous at n=20 and n=30,
   fires at n=50" — still accurate for A seed 123
- Add: seed 123 under C fires at every scale-up n (3/3 single_complement)
- The "Appendix C mechanism" reduces from 5 case studies to 2 (A n=20,
  A n=30, both seed 123).

### §4.2 Algorithmic details paragraph

v2.0.3 text (already tone-downed): "Our implementation fixes all
constraints tight ... a full rank-aware implementation ... is
straightforward to layer on top..." — stays accurate with new
nucleolus.py docstring.

### §3.2 Table 1 "realized online cost"

Current paper says "total travel distance of the tour actually
executed".  Now the code matches this exactly (Phase 1.2 fix).  No
change needed unless the v2.0.3 text had a residual elapsed-time
phrasing (cross-check during Phase 3 proper).

### §5.3 Over-claims

Current text (v2.0.3 fixed): "immune to the complement-coalition
empty-Core mechanism" etc.  Still accurate; phrasing compatible with
new intermediate-mechanism observations.

## §7 Limitations (iii) + (iv) — draft rewrite

**Current (v2.0.3):**
- (iii) Intermediate-coalition mechanism — open problem, conjectured
  Shapley-1971 balanced collections.
- (iv) Near-complement mechanism — open analytic condition, empirical
  evidence at seed 123.

**Proposed draft (v2.1.1, do not yet insert):**

(iii) *Intermediate-coalition mechanism (empirically observed).*
Section 6.4's partition shows 9 of the 175 main-grid instances under
NN admit an empty Core without any feasible complement coalition
`N\{i}` (r** undefined), via simultaneous tight inequalities on
coalitions of size 2..n-2.  Seven of these occur under Pattern
`B_medium`, two under Pattern E, each at `n ∈ {7,10,12,15}`.  A
sufficient analytic condition involves balanced collections of
intermediate-size feasible coalitions in the sense of
Shapley [1971, Bondareva 1963]; the specific collection weights
realizing the empty LP remain open.

(iv) *Near- and balanced-complement mechanism.* 21 of the 67 empty
Cores under NN satisfy `r <= r**` (Theorem 11 vacuous) yet empty via a
balanced collection of feasible complements `N\{i}`: 11 cases fall in
the pure balanced-complement regime (tight constraints exclusively at
size n-1) and 10 mix size (n-1) with (n-2).  The aggregate
balanced-complement threshold

    r*** = (1/(n-1)) * sum_i c(N\{i}) / c*(N),   defined when all
    N\{i} are feasible,

is a sufficient condition: in 112 of 240 applicable instances `r > r***`
holds, all 112 with empty Core (no false positives across 525 policy-
instance pairs).  r*** is strictly tighter than r** whenever the
complement costs are heterogeneous; its analytic asymptotic behaviour
and its precise relationship to r** are natural next questions.

## Figures to regenerate

- fig2_r_vs_rstar: new scatter points reflecting 96 applicable (not
  80), 67 empty (not 21).
- fig3_core_vs_k: new k-regime strata with corrected Core rates.
- fig3_core_vs_n: per-pattern Core rate vs n.  B_heavy/B_medium/C
  curves drop sharply.
- fig4_coalition_reduction: |F|/(2^n-1) distributions.  These should
  INCREASE because F is now larger.
- fig5_rstar_vs_rss: histograms of r** and r*.  mean r** moves from
  1.355 to 1.184.

## Appendix C (Restricted LP case studies)

Previous table had 5 rows.  Under corrected F:
- Seed 123 A n=20 : still near-complement mechanism
- Seed 123 A n=30 : still near-complement mechanism
- Seed 123 A n=50 : now absorbed by Thm 11 (drop or keep as boundary
  illustration)
- Seed 7    A n=20 : now Thm 11 fires (drop)
- Seed 42   A n=30 : now Thm 11 fires (drop)

Appendix C table shrinks from 5 rows to 2 near-complement cases.
Alternatively, reorganize around the 30 residual cases (Phase 2
report): give size-distribution histograms for representative
intermediate, near-complement, and balanced-complement cases.

## Decision points for author (submitted with this plan)

1. **Mechanism taxonomy**: 4-way partition
   (single_complement / balanced_complement / near_complement /
    intermediate) adopted throughout §6 and §7, or simpler 2-way
   (Thm 11 / rest)?
2. **Remark 13 role**: Retain as Remark, or promote to Observation
   now that 9+10+11 = 30 residual cases (vs. 7 in v2.0.3) support a
   more concrete statement?
3. **r_sss introduction**: Add as Definition/Proposition in §5 and
   use in §6.6 sharpness comparison, or confine to §6.4 discussion?
4. **§6.5 Table 6 B_medium/E**: Admit intermediate mechanism breaks
   B_medium's 100% claim?  Or re-sample at higher n (run_scaleup_v2
   with intermediate coalition sampling) to see if it persists?

## Scripts / data that will be regenerated in Phase 3

- `figures/make_figures_v3.py` — rerun (reads augmented CSV).
- `run_sensitivity_v2.py` — rerun for scale-invariance sanity check.
- Potentially new `run_seed123_check.py` with reduced-case scope
  (2 near-complement cases instead of 5).

## Out of scope for Phase 3 (noted for completeness)

- Extending run_scaleup_v2 with intermediate-coalition sampling.
- Full rank-aware Kopelowitz-Guajardo-Jornsten nucleolus.
- Any theorem/lemma additions to §5.

Phase 3 proper begins after author reviews this plan and the 4-way
classification decision is made.
