# Reproducibility Guide — Online TSG (v2.0)

This document describes how to reproduce the empirical results in the paper *"Online Traveling Salesman Games: Temporal Nucleolus, Empty Cores, and Complement-Coalition Mechanisms"* (major revision, v2.0).

## Paper Info

- **Version**: v2.0 (major revision)
- **Pages**: 29
- **Experimental instances**: 599 total
  - Main study: 525 (5 sizes × 7 patterns × 5 seeds × 3 policies)
  - Scale-up: 45 (3 sizes × 3 patterns × 5 seeds × NN)
  - Scale invariance: 24 (sensitivity study, Appendix B)
  - Restricted Core LP certification: 5 (seed 123 cases, Appendix C)

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
- **Source for**: Tables 5–7, Section 6.4 strata, all figures.

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

### 4. Restricted Core LP certification (5 instances, Appendix C)

```bash
cd code/experiments
python3 run_seed123_check.py
```

- **Runtime**: ~12 hours (n=30 and n=50 Pattern A dominated by LKH calls on ~10,000 sampled coalitions each).
- **Output**: `logs/seed123_core_check.csv` + `logs/run_seed123_check.log`.
- **Source for**: Appendix C, Table C.1.

### 5. Figures regeneration

```bash
cd code/figures
python3 make_figures_v3.py
```

- **Runtime**: ~10 seconds.
- **Output**: 5 PDF figures in `code/figures/` (`fig2_r_vs_rstar`, `fig3_core_vs_k`, `fig3_core_vs_n`, `fig4_coalition_reduction`, `fig5_rstar_vs_rss`).
- **Input**: `policy_comparison_v2_full.csv`.

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
| `code/src/core_lp_restricted.py` | Restricted Core LP (Appendix C) |

## Data Files (v2.0)

All in `code/experiments/logs/`:

| File | Rows | Description |
|---|---|---|
| `policy_comparison_v2_full.csv` | 525 | Main study |
| `scaleup_v2.csv` | 45 | Scale-up study |
| `sensitivity_v2.csv` | 24 | Scale invariance verification (Appendix B) |
| `seed123_core_check.csv` | 5 | Near-complement certification (Appendix C) |
| `run_main_v2_full.log` | — | Execution log of main study |
| `run_scaleup_v2.log` | — | Execution log of scale-up |
| `run_sensitivity_v2.log` | — | Execution log of sensitivity |
| `run_seed123_check.log` | — | Execution log of restricted LP |

Legacy CSVs (`policy_comparison.csv`, `scaleup.csv`, etc.) correspond to the v1.2 submission and are retained for historical reference; they are **not** the basis for v2.0's reported numbers.

## Design Documents

- `phase1_design.md` — Experimental design rationale (N2 convention, pattern taxonomy)
- `phase3_narrative.md` — Paper revision narrative with section-by-section plan
- `phase3_results_summary.json` — Aggregated numerical results used in the paper

## Compiling the Paper

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Expected output: `paper/main.pdf`, 29 pages, 0 errors, 0 undefined references or citations.

Required TeX packages: `natbib`, `mathtools`, `multirow`, `enumitem`, `authblk`, `setspace`, `caption`, `amsmath`, `amssymb`, `amsthm`, `graphicx`, `booktabs`, `hyperref`, `xcolor`, `geometry`.

## Version History

- **v1.2** (initial submission): 23 pages, 625 instances, L = 10 coordinate convention.
- **v2.0** (major revision): 29 pages, 599 instances, N2 convention (L = √n, Steele 1997), near-complement mechanism (new Remark + Appendix C), scale invariance verification (new Appendix B), pattern re-parameterization to ρ-based taxonomy.
