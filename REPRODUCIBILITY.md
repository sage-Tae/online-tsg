# Reproducibility Guide — Online TSG (v2.1.8)

This document describes how to reproduce the empirical results in the paper *"Online Traveling Salesman Games: Temporal Nucleolus and the Fragility of the Core under Dynamic Arrivals"* (major revision, v2.1.8).

## Paper Info

- **Version**: v2.1.8 (major revision; supersedes v2.0, v2.1.0, v2.1.2, v2.1.3, v2.1.4, v2.1.5, v2.1.6, v2.1.7)
- **Pages**: main manuscript 30 pages (EJOR-compliant), Supplementary Materials 6 pages
- **Experimental instances**: 596 total
  - Main study: 525 (5 sizes × 7 patterns × 5 seeds × 3 policies)
  - Scale-up: 45 (3 sizes × 3 patterns × 5 seeds × NN)
  - Scale invariance: 24 (sensitivity study, Supplementary Materials §S2)
  - Restricted Core LP certification: 2 seed-123 near-complement cases (Supplementary Materials §S3) under the corrected feasibility family F

## EJOR Submission Layout

The paper is submitted in two files, per EJOR's 30-page main-manuscript cap:

- `paper/main.pdf` (30 pages) — Manuscript slot in Editorial Manager.
- `paper/supplementary.pdf` (6 pages) — Supplementary Material slot. Contains:
  - §S1 Per-pattern Core-existence breakdown (formerly Appendix A)
  - §S2 Scale invariance empirical verification (formerly Appendix B)
  - §S3 Restricted Core LP methodology and mechanism classification tables (formerly Appendix C)

Both share `references.bib`. The main manuscript is self-contained: restricted-LP methodology is summarized in §6.8 and the body refers to Supplementary Materials §S1–§S3 by section number.

## Environment Setup

### Required
- Python 3.9 or later
- LaTeX distribution (TeX Live / MacTeX / MiKTeX) — for compiling the paper

### Python Dependencies

Install via pip:

```bash
pip install -r code/requirements.txt
```

Required packages:
- `numpy`, `scipy`, `pandas`, `matplotlib` (standard scientific stack)
- `pulp>=2.7` (Core LP solver, used in Appendix C restricted LP)
- `elkai>=1.2` (LKH TSP solver for n > 15)

## Seeds

All experiments use the seed set `{7, 42, 99, 123, 256}`, declared in `code/src/config.py`. Re-running with the same seeds produces bit-identical numerical results for every aggregate statistic reported in the paper.

## Reproducing Experiments

### 1. Main study (525 policy-instance pairs)

```bash
cd code/experiments
python3 run_main.py --output logs/policy_comparison_v2_full.csv
```

- **Runtime**: ~13 minutes on a laptop.
- **Output CSV columns** (18): n, pattern, seed, policy, L, rho, tau, C_N_online, c_star_N, r, r_star, r_ss, n_feasible, k, core_nonempty, core_epsilon, theorem11_applicable, theorem11_fires.
- **Source for**: Tables 5-7, Section 6.4 strata, all figures (after Step 1.5 augment below).

### 1.5. Augment summary CSV with `r_sss` and `empty_mechanism` columns

`run_main.py` produces 18 columns. Figure regeneration, the 4-mechanism taxonomy, and the Table 6 `r***` column all require two additional columns: `r_sss` (balanced-complement threshold, Proposition 12) and `empty_mechanism` (4-way classification: single / balanced / near / intermediate / core_nonempty). These are computed by a post-processing script that reads and overwrites the same CSV in place:

```bash
cd code
python3 scripts/augment_summary.py
```

- **Input / output**: `code/experiments/logs/policy_comparison_v2_full.csv` (read and overwritten; the script hard-codes this path).
- **Runtime**: ~15 minutes (reruns the simulator for each of 525 rows to recover `coalition_costs` needed for the binding-size classification).
- **Output columns after Step 1.5** (20 total): the original 18 plus `r_sss` and `empty_mechanism`.
- **Required by**: `make_figures_v3.py` (Step 5) and the Appendix C restricted-LP analysis in `scripts/residual_binding_analysis.py`. Must be run before those downstream steps; idempotent on re-runs.

### 2. Scale-up study (45 instances)

```bash
cd code/experiments
python3 run_scaleup_v2.py
```

- **Runtime**: ~110 minutes (LKH for n ∈ {30, 50}).
- **Output**: `logs/scaleup_v2.csv` covering n ∈ {20, 30, 50} × {A, B_medium, C} × 5 seeds under NN dispatch.
- **Source for**: Table 8 and Section 6.8 findings.

### 3. Scale invariance (24 instances, Appendix B)

```bash
cd code/experiments
python3 run_sensitivity_v2.py
```

- **Runtime**: ~55 minutes.
- **Output**: `logs/sensitivity_v2.csv` with α ∈ {0.5, 1.0, 2.0, 5.0} variants across 6 (n, pattern) configurations.
- **Expected result**: bit-identical r, r**, k within each (n, pattern) group across α.
- **Source for**: Appendix B, Table B.1.

### 4. Restricted Core LP certification (2 instances, Appendix C)

```bash
cd code/experiments
python3 run_seed123_check.py
```

- **Runtime**: ~5 hours total for the 2 shipped rows (n=20 seed 123 Pattern A ≈ 1 h, n=30 seed 123 Pattern A ≈ 4 h; both dominated by LKH calls on ~10,000 sampled coalitions each). Requires augmented summary CSV from Step 1.5 for cross-checks.
- **Output**: `logs/seed123_core_check.csv` (2 rows: n=20 and n=30 seed 123 under Pattern A — exactly the Appendix C Table). TARGETS in the script match this scope; `logs/run_seed123_check.log` records execution traces.
- **Source for**: Supplementary Materials §S3 "Scale-up certification" 2-row table. The n=50 seed 123 case is analytically covered by Theorem 11 firing directly (Finding 4) and does not require restricted-LP treatment in v2.1.8.
- **Legacy scope**: the v2.1.4-and-earlier 5-entry TARGETS list (adding n=50 seed 123 and two control rows for Theorem-11-fires sanity checks) is preserved at `code/scripts/legacy/run_seed123_check_extended.py`.

### 5. Figures regeneration

```bash
cd code/figures
python3 make_figures_v3.py
```

- **Runtime**: ~10 seconds.
- **Output**: 5 PDF figures in `code/figures/` (`fig2_r_vs_rstar`, `fig3_core_vs_k`, `fig3_core_vs_n`, `fig4_coalition_reduction`, `fig5_rstar_vs_rss`).
- **Input**: `policy_comparison_v2_full.csv` **after Step 1.5 augment** (requires the `r_sss` and `empty_mechanism` columns; running this step on the 18-column raw output will fail).

## Design Framework (N2 Convention)

Customers are sampled uniformly in [0, L]² with **L = √n** (Steele 1997 convention, fixing customer density at 1 per unit area). Vehicle speed is normalized to 1. See Section 6.1 of the paper and `code/src/config.py`.

### Arrival Patterns (ρ-based)

| Pattern | ρ | Interval τ | Structure |
|---------|---|-----------|-----------|
| A | ∞ | 0 | Simultaneous |
| B_heavy | 4.0 | 0.178 | Sequential uniform |
| B_medium | 2.0 | 0.356 | Sequential uniform |
| B_light | 0.5 | 1.425 | Sequential uniform |
| C | 2.0 | 0.356 | Clustered interleave |
| D | 1.0 | 0.712 | Reverse zig-zag |
| E | 1.0 | 0.712 | Poisson random |

where ρ = (L/v)/τ is the dimensionless load parameter and τ = β_BHH / ρ with β_BHH ≈ 0.7124 the Beardwood–Halton–Hammersley constant.

### Scale Invariance

All observables (r, r**, k, Core status) are invariant under the joint rescaling (L, v, τ) → (αL, αv, ατ) for any α > 0. Empirical verification: `r` relative standard deviation = 0.00e+00 across α ∈ {0.5, 1.0, 2.0, 5.0} for all 6 tested configurations (Appendix B, `sensitivity_v2.csv`).

### Near-complement Mechanism

For Pattern A at seed = 123 (n ∈ {20, 30}), Theorem 11 is vacuous (r ≤ r**) yet the Core is empty. Certification via a restricted Core LP over 10,000 sampled coalitions shows binding constraints at sizes both (n-1) and (n-2) simultaneously. See `code/src/core_lp_restricted.py`, `code/experiments/run_seed123_check.py`, and Appendix C.

## Key Source Modules

| File | Role |
|---|---|
| `code/src/config.py` | Design constants (N2, ρ map, seeds, patterns) |
| `code/src/generators.py` | Position and arrival-time generators |
| `code/src/simulator.py` | Online TSG simulator (legacy paths) |
| `code/src/policies.py` | Dispatch policies (NN, cheapest-insertion, batch-reopt) |
| `code/src/policy_simulator.py` | Policy-aware simulator (used by v2 runners) |
| `code/src/nucleolus.py` | Temporal Nucleolus sequential LP |
| `code/src/metrics.py` | Competitive ratio and auxiliary metrics |
| `code/src/tsp.py` | Held–Karp exact TSP for small n |
| `code/src/tsp_scaleup.py` | LKH wrapper (via `elkai`) for large n |
| `code/src/core_lp_restricted.py` | Restricted Core LP (Supplementary Materials §S3) |

## Data Files (v2.1.8)

All in `code/experiments/logs/`:

| File | Rows | Description |
|---|---|---|
| `policy_comparison_v2_full.csv` | 525 | Main study |
| `scaleup_v2.csv` | 45 | Scale-up study |
| `sensitivity_v2.csv` | 24 | Scale invariance verification (Supplementary Materials §S2) |
| `seed123_core_check.csv` | 2 | Near-complement certification (Supplementary Materials §S3; n=20 and n=30 seed 123 under Pattern A — legacy 5-row version at `logs/legacy/seed123_core_check_extended.csv`) |
| `run_main_v2_full.log` | — | Execution log of main study |
| `run_scaleup_v2.log` | — | Execution log of scale-up |
| `run_sensitivity_v2.log` | — | Execution log of sensitivity |
| `run_seed123_check.log` | — | Execution log of restricted LP |

Legacy CSVs (`policy_comparison.csv`, `scaleup.csv`, etc.) correspond to the v1.2 submission and are retained for historical reference; they are **not** the basis for v2.1.8's reported numbers.

## Design Documents

- `phase1_design.md` — Experimental design rationale (N2 convention, pattern taxonomy)
- `phase3_narrative.md` — Paper revision narrative with section-by-section plan
- `phase3_results_summary.json` — Aggregated numerical results used in the paper

## Compiling the Paper

Two PDFs must be built: `main.pdf` (the 30-page manuscript) and `supplementary.pdf` (the 6-page Supplementary Materials).

```bash
cd paper

# Main manuscript
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# Supplementary materials
pdflatex -interaction=nonstopmode supplementary.tex
bibtex supplementary
pdflatex -interaction=nonstopmode supplementary.tex
pdflatex -interaction=nonstopmode supplementary.tex
```

Expected output: `paper/main.pdf` (30 pages, 0 errors, 0 undefined references or citations) and `paper/supplementary.pdf` (6 pages, 0 errors, 0 undefined references or citations).

Required TeX packages: `natbib`, `mathtools`, `multirow`, `enumitem`, `authblk`, `setspace`, `caption`, `amsmath`, `amssymb`, `amsthm`, `graphicx`, `booktabs`, `hyperref`, `xcolor`, `geometry`.

## EJOR Submission

Upload to Editorial Manager in the following slots:

- **Manuscript**: `paper/main.pdf` (30 pages; under EJOR's 30-page cap).
- **Supplementary Material**: `paper/supplementary.pdf` (6 pages).
- **Source files** (if requested): `paper/main.tex`, `paper/supplementary.tex`, `paper/references.bib`, and `code/figures/*.pdf`.

## Submission Verification

Two helper scripts at the repository root guard against regressions between iterations:

```bash
# Clean-room rebuild test: extract ZIP to a tmp dir and verify BOTH main.pdf
# (≤30 pages) and supplementary.pdf compile with 0 errors / 0 undef refs /
# 0 undef cites.
bash scripts/verify_zip_rebuild.sh TSG_agent_submission_v2_1_8_20260419.zip

# Documentation consistency check: grep-based stale-label sweep over
# README.md and REPRODUCIBILITY.md (version labels outside historical
# context, page counts, seed123 row counts, orphan top-level figures/,
# legacy metric values). Every category must report "(none)".
bash scripts/verify_doc_consistency.sh
```

Both are expected to pass on a clean `v2.1.8` checkout. Use them on every future iteration before tagging a new version.

## Version History

- **v1.2** (initial submission): 23 pages, 625 instances, L = 10 coordinate convention.
- **v2.0** (intermediate major revision): 29 pages, 599 instances, N2 convention (L = √n, Steele 1997), near-complement mechanism (Remark + Appendix C), scale invariance verification (Appendix B), pattern re-parameterization to ρ-based taxonomy.
- **v2.1.0** (intermediate; responded to 5 fundamental critiques): 30 pages, §2.5 Restricted Cooperation Games added, Definition 3 proper-subset constraints, over-claim tone-downs, Nucleolus algorithmic details.
- **v2.1.2** (intermediate; post-F-generation fix): 34 pages, corrected feasibility family F via post-hoc reconstruction per paper Definition 2, Proposition 12 (balanced-complement threshold), Observation 15 (intermediate-coalition mechanism), 4-mechanism taxonomy.
- **v2.1.3** (intermediate): 34 pages. Sync fixes: Conclusion and README numerics aligned to v2.1.2 data, Figure 1 caption corrected (broken "Fig None" reference fixed, four-mechanism decomposition explicit), Nucleolus §4.2 algorithmic-details tone-downed to two-tier scope (first-stage LP for Core judgment; simplified cascade for Nucleolus point under non-degeneracy), B_medium nonemptiness claim at n>15 restricted-LP-caveated.
- **v2.1.4** (intermediate): 35 pages. Reproducibility polish: Step 1.5 `augment_summary.py` documented; seed123 CSV aligned with Appendix C (2 rows; 3 legacy rows retained untracked); §6.8 Summary tone-down.
- **v2.1.5** (intermediate): 35 pages. Scale-up near-complement scope aligned across paper/script/CSV. Finding 4 rewritten as a two-tier pattern (restricted LP at n=20, 30; Theorem 11 fires directly at n=50), consistent with Theorem 14's $O(n^{-1/2})$ tightening. `run_seed123_check.py` TARGETS reduced from 5 to 2 to match Appendix C (legacy 5-entry version retained at `code/scripts/legacy/run_seed123_check_extended.py`).
- **v2.1.6** (intermediate): 35 pages. Submission-ZIP rebuildability fix. `paper/main.tex` `\graphicspath` extended from `{../figures/}` to `{../figures/}{../code/figures/}` so that a clean-room extraction of the submission ZIP — which ships `paper/` and `code/figures/` but not a top-level `figures/` symlink — compiles without `! LaTeX Error: File ... not found`. `REPRODUCIBILITY.md` Data-Files table `seed123_core_check.csv` row corrected from `5` to `2` to match Appendix C and the shipped CSV. `scripts/verify_zip_rebuild.sh` added as an automated clean-room rebuild check (extract ZIP to tmp → 3-pass LaTeX → verify 35 pages). No theoretical, experimental, or figure changes.
- **v2.1.7** (intermediate): 35 pages. Documentation semantic-sweep consistency pass. `REPRODUCIBILITY.md` §4 heading "Restricted Core LP certification (5 instances, Appendix C)" corrected to "(2 instances, Appendix C)" — the last residual `5 instances` label from the v2.1.2 scope, which had survived prior line-local fixes because it lived in a section heading rather than body text. `README.md` header current-version label bumped to v2.1.7, version history appended, and `Reproducibility tags` section updated so that the `(current, major revision)` marker follows the active tag rather than `v2.1.2`. Both files given an end-to-end semantic review rather than a pattern-local edit. `scripts/verify_doc_consistency.sh` added: automated stale-label grep check (version labels / page counts / seed123 row counts / orphan top-level `figures/` / stale metrics) so that future iterations fail loudly at the same class of issue. No theoretical, experimental, figure, CSV, or paper-source changes.
- **v2.1.8** (current): main manuscript 30 pages (EJOR-compliant), Supplementary Materials 6 pages. EJOR 30-page compliance split: the three appendices (per-pattern Core-existence, scale-invariance verification, restricted Core LP methodology + classification tables) are moved out of `main.tex` into a new `paper/supplementary.tex` (sections §S1, §S2, §S3). Main-body references rewritten as `Supplementary Materials §S1–§S3` and `Supplementary Figure/Table S*`. §6.8 gains a one-paragraph self-contained summary of the restricted-LP methodology so the main manuscript does not depend on the supplement to explain its scale-up certifications. §2 Related Work consolidated from five subsections to three (Static+Dynamic merged; Online+Nucleolus merged; Restricted Cooperation kept) and bibliography `\bibsep` compressed so the references fit on page 30. `scripts/verify_zip_rebuild.sh` extended to build and validate both `main.pdf` (≤30 pages hard cap) and `supplementary.pdf`. Theorem/Proposition/Corollary/Remark/Observation statements and proofs are unchanged; experimental CSVs and figure PDFs are unchanged bit-for-bit.
