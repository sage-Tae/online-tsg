# Online Traveling Salesman Games

Code and data for the paper:

> **Online Traveling Salesman Games: Temporal Nucleolus and the Fragility
> of the Core under Dynamic Arrivals**
> Seyun Jeong (POSTECH) and Hyunchul Tae (KITECH)
> Submitted to *European Journal of Operational Research*, 2026

## Overview

We introduce the **Online Traveling Salesman Game (Online TSG)**, a cooperative
game in which customers arrive over time and costs must be allocated only
among coalitions realizable under revealed arrival dynamics. This repository
contains all code, seeds, and raw results needed to reproduce the paper's
numerical claims.

## Key results (sanity checkpoints)

| Paper location | Quantity | Value |
|---|---|---|
| Example 4 (Solomon C101) | TNu allocation | (16.67, 20.51, 11.27, 15.18, 16.44) |
| Table 5 | Theorem 11 predicted-empty accuracy | 12/12 (no false positives) |
| Corollary 16 | k < n−1 Core stability rate | 95/95 (100%) |
| Table 6 overall | Sharpness ratio r̄**/r̄* | 3.24 |

## Repository structure

```
.
├── paper/             # LaTeX source + references.bib + compiled PDF
├── code/
│   ├── src/           # algorithm implementations (Held-Karp, LKH, TNu LP, policies)
│   ├── experiments/   # run scripts + canonical logs (policy_comparison.csv, scaleup.csv)
│   ├── figures/       # figure generation + PDF outputs
│   └── requirements.txt
├── docs/              # verification artifacts (35/35 reproduction PASS)
├── figures/           # symlink → code/figures (for paper graphicspath)
├── REPRODUCIBILITY.md # full reproduction guide
└── LICENSE
```

## Quick start

```bash
# Install dependencies
cd code
pip install -r requirements.txt

# Fastest sanity check (~5 seconds)
python3 figures/solomon_example.py
# Expected: allocation (16.670, 20.508, 11.268, 15.175, 16.438), slack 52.293

# Regenerate all figures from saved experiment data
python3 figures/make_figures_rev2.py
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for full environment details,
random seeds, and mapping between paper tables/figures and scripts.

## Pre-freeze verification

This codebase has been verified to reproduce all 35 numerical checkpoints
in the paper. See [docs/verification_report_pre_freeze.md](docs/verification_report_pre_freeze.md).

## Reproducibility tags

- `paper-submission-v1`: exact code state at EJOR submission
- `paper-submission-v1.1`: same + repository URL added to main.tex

Restore submission-time state:
```bash
git checkout paper-submission-v1
```

## Citation

If you use this code or build on the results, please cite:

```bibtex
@article{jeong2026online,
  author = {Jeong, Seyun and Tae, Hyunchul},
  title  = {Online Traveling Salesman Games: Temporal Nucleolus
            and the Fragility of the Core under Dynamic Arrivals},
  year   = {2026},
  note   = {Under review at European Journal of Operational Research}
}
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Contact

- Seyun Jeong, POSTECH (Department of Industrial and Management Engineering)
- Hyunchul Tae, KITECH (Korea Institute of Industrial Technology)
