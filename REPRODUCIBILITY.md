# Reproducibility Guide

This repository accompanies the paper **"Online Traveling Salesman Games: Temporal Nucleolus and the Fragility of the Core under Dynamic Arrivals"** (Jeong & Tae). This guide lets a third party rebuild the paper, re-run all experiments, and verify every numerical claim.

## Environment

| Component | Version used |
|---|---|
| OS | macOS (Darwin 25.3.0, arm64) |
| Python | 3.9.6 |
| numpy | 2.0.2 |
| scipy | 1.13.1 |
| pandas | 2.3.3 |
| matplotlib | 3.8+ |
| elkai (LKH) | 1.2+ |
| TeX | TeX Live 2026 (BasicTeX + `caption`, `natbib`, etc.) |

Install Python dependencies:
```bash
cd code
pip install -r requirements.txt
```

## Repository layout

```
TSG_agent/
├── paper/
│   ├── main.tex           # paper source (23 pages)
│   ├── references.bib     # 32 bibliography entries (Phase B audited)
│   └── main.pdf           # compiled output
├── code/
│   ├── src/               # algorithm implementations
│   │   ├── simulator.py   # instance generator + arrival patterns
│   │   ├── tsp.py         # Held-Karp + LKH wrapper
│   │   ├── nucleolus.py   # Temporal Nucleolus sequential LP
│   │   ├── policies.py    # NN, cheapest-insertion, batch reoptimize
│   │   ├── policy_simulator.py
│   │   ├── metrics.py     # r, r*, r**, k, etc.
│   │   └── tsp_scaleup.py # LKH-based scale-up
│   ├── experiments/       # run scripts
│   │   ├── run_all.py
│   │   ├── run_policy_comparison.py
│   │   ├── run_scaleup.py
│   │   ├── validate_theory.py
│   │   ├── logs/          # canonical data: policy_comparison.csv, scaleup.csv
│   │   └── NOTES.md
│   ├── results/           # legacy summaries (superseded by experiments/logs/)
│   └── figures/           # figure generation scripts + PDF outputs
├── figures/               # symlink → code/figures (for paper graphicspath)
└── docs/                  # verification artifacts
```

## Seeds

All experiments use the seed set `{7, 42, 99, 123, 256}`, hard-coded in `src/simulator.py`. Re-running with the same seeds produces byte-identical numerical results for all aggregate statistics.

## Canonical data files

The paper's reported numbers are computed from:
- `code/experiments/logs/policy_comparison.csv` — 525 rows = 175 instances × 3 policies (NN, CI, BR). Source for Tables 5, 6, 7 and Corollary 16 statistics.
- `code/experiments/logs/scaleup.csv` — 45 rows (3 patterns × 3 sizes × 5 seeds). Source for Table 8.

`code/results/summary.csv` is legacy (70 instances; NaN-heavy) and is **not** the basis for the paper. See `experiments/NOTES.md`.

## How to reproduce

### 1. Numerical tables (main study + scale-up)

```bash
cd code
python experiments/run_policy_comparison.py   # regenerates policy_comparison.csv
python experiments/run_scaleup.py             # regenerates scaleup.csv
```

Expected runtime: ~30–60 minutes on a modern laptop.

### 2. Figures

```bash
cd code/figures
python make_figures.py            # fig1_core_rate, fig3_core_vs_n, fig5_rstar_vs_rss (legacy slice)
python make_figures_rev2.py       # fig2_r_vs_rstar, fig3_core_vs_k, fig4_coalition_reduction, fig5_rstar_vs_rss (final)
python solomon_example.py         # Example 4 (Solomon C101) numbers
```

The paper uses the `_rev2` outputs for fig2–fig5; `fig1_core_rate` and `fig3_core_vs_n` come from `make_figures.py` only.

### 3. Paper build (23 pages)

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Required TeX packages: `natbib`, `mathtools`, `multirow`, `enumitem`, `authblk`, `setspace`, `caption`, `amsmath`, `amssymb`, `amsthm`, `graphicx`, `booktabs`, `hyperref`, `xcolor`, `geometry`.

## Verification checkpoints

35 distinct numerical claims from the paper have been independently reproduced from the canonical CSVs:

| Section | Checkpoints | Status |
|---|---|---|
| Example 4 (Solomon C101) | 5 | ✓ 3-decimal match |
| Theorem 11 contingency (Table 5) | 5 | ✓ exact integer match |
| Corollary 16 regimes | 3 | ✓ 95/95, 14/14, 47/66 |
| Table 6 pattern-level | 8 | ✓ Δ ≤ 0.001 |
| Table 7 dispatch policies | 3 | ✓ exact |
| Table 8 scale-up | 9 | ✓ exact |
| Derived ratios | 2 | ✓ |
| **Total** | **35** | **35/35** |

Full report: [`docs/verification_report_pre_freeze.md`](docs/verification_report_pre_freeze.md).

## Known limitations of the environment

- `pdfinfo` is not bundled with BasicTeX. Page count is read from `pdflatex` output (`main.pdf (N pages`) instead.
- LKH is invoked via the `elkai` Python wrapper; direct LKH binary calls are not required.
- The symlink `figures → code/figures` is checked into git to satisfy `main.tex`'s `\graphicspath{{../figures/}}`.

## License

TBD (to be added before public release)
