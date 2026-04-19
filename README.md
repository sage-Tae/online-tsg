# Online Traveling Salesman Games

Code and data for the paper:

> **Online Traveling Salesman Games: Temporal Nucleolus, Empty Cores, and Complement-Coalition Mechanisms**
> Seyun Jeong (POSTECH) and Hyunchul Tae (KITECH)
> Submitted to *European Journal of Operational Research*, 2026

**Current version: v2.1.4** (major revision, April 19, 2026)

Version history:
- v2.0.x — initial submission (v2.0, v2.0.1, v2.0.2, v2.0.3)
- v2.1.0 — first-round review response (superseded; F-generation bug)
- v2.1.2 — F-generation fix + 4-mechanism taxonomy (Proposition 12, Observation 15)
- v2.1.3 — documentation sync (Conclusion, Figure 1 caption, README, Nucleolus scope, B_medium caveat)
- v2.1.4 — reproducibility polish (augment step, seed123 CSV alignment, §6.8 Summary tone-down, version labels)

## Overview

We introduce the **Online Traveling Salesman Game (Online TSG)**, a cooperative
game in which customers arrive over time and costs must be allocated only
among coalitions realizable under revealed arrival dynamics. This repository
contains all code, seeds, and raw results needed to reproduce the paper's
numerical claims.

## Key results (sanity checkpoints, v2.0)

| Paper location | Quantity | Value |
|---|---|---|
| Example 4 (Solomon C101) | TNu allocation | (16.67, 20.51, 11.27, 15.18, 16.44) |
| Table 5 | Theorem 11 single-complement fires (NN, 96 applicable) | 37/37 (no false positives) |
| Table 5 | Proposition 12 balanced-complement fires (NN, 80 applicable) | 57/57 (no false positives) |
| §6.4 | Four-mechanism decomposition of 67 NN empties | 37 + 11 + 10 + 9 |
| Corollary 17 (§6.4) | k < n−1 Core empirical nonempty rate | 70/79 (88.6%; 9 intermediate-mechanism exceptions) |
| §6.6 | Sharpness ratio r̄*/r̄**, r̄*/r̄*** | 3.56 (4.351/1.223), 3.97 (4.351/1.096) |
| Appendix B | Scale invariance (r relative std across α) | 0.00e+00 |
| Appendix C | Near-complement cases (Table 10) | 10 |
| Appendix C | Intermediate cases (Table 11) | 9 |

## Repository structure

```
.
├── paper/             # LaTeX source + references.bib (main.pdf built locally)
├── code/
│   ├── src/           # algorithm implementations (Held-Karp, LKH, TNu LP, policies,
│   │                  #  config.py, generators.py, core_lp_restricted.py)
│   ├── experiments/   # v2 runners + logs (policy_comparison_v2_full.csv,
│   │                  #  scaleup_v2.csv, sensitivity_v2.csv, seed123_core_check.csv)
│   ├── figures/       # figure generation + PDF outputs (make_figures_v3.py)
│   └── requirements.txt
├── docs/              # verification artifacts
├── figures/           # symlink → code/figures (for paper graphicspath)
├── phase1_design.md   # experimental design rationale
├── phase3_narrative.md # paper revision narrative
├── REPRODUCIBILITY.md # full reproduction guide
└── LICENSE
```

## Quick start

```bash
# Install dependencies
pip install -r code/requirements.txt

# Regenerate all figures from v2 experiment data
cd code/figures
python3 make_figures_v3.py

# Reproduce main study (~13 min)
cd ../experiments
python3 run_main.py --output logs/policy_comparison_v2_full.csv
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for full environment details,
random seeds, and mapping between paper tables/figures and scripts.

## Reproducibility tags

- `paper-submission-v1` / `v1.1` / `v1.2`: prior submission states (L = 10 coordinate convention); superseded by v2.1.2.
- `paper-submission-v2.0` / `v2.0.1` / `v2.0.2` / `v2.0.3` / `v2.1.0` (local only): intermediate revisions under Steele N2 convention; superseded by v2.1.2.
- `v2.1.2` (current, major revision): 4-mechanism taxonomy (single / balanced / near / intermediate complement), Proposition 12 (balanced-complement threshold via Bondareva-Shapley), Observation 15 (intermediate-coalition mechanism), and corrected feasibility family F generation per paper Definition 2 (post-hoc reconstruction rather than dispatch-iteration enumeration). Restore locally via `git checkout v2.1.2`.

## Citation

If you use this code or build on the results, please cite:

```bibtex
@article{jeong2026online,
  author = {Jeong, Seyun and Tae, Hyunchul},
  title  = {Online Traveling Salesman Games: Temporal Nucleolus,
            Empty Cores, and Complement-Coalition Mechanisms},
  year   = {2026},
  note   = {Under review at European Journal of Operational Research}
}
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Contact

- Seyun Jeong, POSTECH (Department of Industrial and Management Engineering)
- Hyunchul Tae, KITECH (Korea Institute of Industrial Technology)
