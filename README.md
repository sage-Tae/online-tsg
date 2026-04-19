# Online Traveling Salesman Games

Code and data for the paper:

> **Online Traveling Salesman Games: Temporal Nucleolus, Empty Cores, and Complement-Coalition Mechanisms**
> Seyun Jeong (POSTECH) and Hyunchul Tae (KITECH)
> Submitted to *European Journal of Operational Research*, 2026

**Current version: v2.1.8** (major revision, April 19, 2026)

Version history:
- v2.0.x — initial submission (v2.0, v2.0.1, v2.0.2, v2.0.3)
- v2.1.0 — first-round review response (superseded; F-generation bug)
- v2.1.2 — F-generation fix + 4-mechanism taxonomy (Proposition 12, Observation 15)
- v2.1.3 — documentation sync (Conclusion, Figure 1 caption, README, Nucleolus scope, B_medium caveat)
- v2.1.4 — reproducibility polish (augment step, seed123 CSV alignment, §6.8 Summary tone-down, version labels)
- v2.1.5 — seed 123 scale-up alignment (Finding 4 two-tier pattern, `run_seed123_check.py` TARGETS 5 → 2, REPRODUCIBILITY labels)
- v2.1.6 — ZIP-rebuildability fix (`\graphicspath` extended for clean-room extraction, Data-Files table `seed123_core_check.csv` 5 → 2 rows, `scripts/verify_zip_rebuild.sh` added)
- v2.1.7 — documentation semantic-sweep consistency pass (REPRODUCIBILITY §4 heading `5 instances` → `2 instances`, README version/Reproducibility-tags/repo-tree synced, `scripts/verify_doc_consistency.sh` added)
- v2.1.8 — EJOR 30-page compliance split (Appendix A/B/C moved to a separate `paper/supplementary.pdf`; main manuscript trimmed to 30 pages; §2 Related Work consolidated; `scripts/verify_zip_rebuild.sh` extended to validate both PDFs)

## Overview

We introduce the **Online Traveling Salesman Game (Online TSG)**, a cooperative
game in which customers arrive over time and costs must be allocated only
among coalitions realizable under revealed arrival dynamics. This repository
contains all code, seeds, and raw results needed to reproduce the paper's
numerical claims.

## Key results (sanity checkpoints, v2.1.8)

| Paper location | Quantity | Value |
|---|---|---|
| Example 4 (Solomon C101) | TNu allocation | (16.67, 20.51, 11.27, 15.18, 16.44) |
| Table 5 | Theorem 11 single-complement fires (NN, 96 applicable) | 37/37 (no false positives) |
| Table 5 | Proposition 12 balanced-complement fires (NN, 80 applicable) | 57/57 (no false positives) |
| §6.4 | Four-mechanism decomposition of 67 NN empties | 37 + 11 + 10 + 9 |
| Corollary 17 (§6.4) | k < n−1 Core empirical nonempty rate | 70/79 (88.6%; 9 intermediate-mechanism exceptions) |
| §6.6 | Sharpness ratio r̄*/r̄**, r̄*/r̄*** | 3.56 (4.351/1.223), 3.97 (4.351/1.096) |
| Supplementary §S2 | Scale invariance (r relative std across α) | 0.00e+00 |
| Supplementary §S3 | Near-complement cases (Supp. Table S2) | 10 |
| Supplementary §S3 | Intermediate cases (Supp. Table S3) | 9 |

## Repository structure

```
.
├── paper/             # main.tex + supplementary.tex + references.bib (main.pdf + supplementary.pdf built locally)
├── code/
│   ├── src/           # algorithm implementations (Held-Karp, LKH, TNu LP, policies,
│   │                  #  config.py, generators.py, core_lp_restricted.py)
│   ├── experiments/   # v2 runners + logs (policy_comparison_v2_full.csv,
│   │                  #  scaleup_v2.csv, sensitivity_v2.csv, seed123_core_check.csv)
│   ├── figures/       # figure generation + PDF outputs (make_figures_v3.py)
│   └── requirements.txt
├── docs/              # verification artifacts
│                      # (dev-only: a `figures/` symlink to `code/figures/`
│                      #  exists locally for the paper's graphicspath, but
│                      #  is NOT shipped in the submission ZIP — the ZIP
│                      #  references `code/figures/` directly)
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

- `paper-submission-v1` / `v1.1` / `v1.2`: prior submission states (L = 10 coordinate convention); superseded by v2.1.2 and subsequent iterations.
- `paper-submission-v2.0` / `v2.0.1` / `v2.0.2` / `v2.0.3` / `v2.1.0` (local only): intermediate revisions under Steele N2 convention; superseded by v2.1.2 and subsequent iterations.
- `v2.1.2` / `v2.1.3` / `v2.1.4` / `v2.1.5` / `v2.1.6` / `v2.1.7` (intermediate major-revision iterations): 4-mechanism taxonomy, Proposition 12, Observation 15, corrected feasibility family F, then a sequence of documentation-polish and ZIP-rebuildability fixes capped by the v2.1.7 end-to-end consistency sweep. See the version-history block above for per-iteration scope. Restore any locally via `git checkout <tag>`.
- `v2.1.8` (current, major revision): EJOR 30-page compliance split. The three appendices are moved from `paper/main.tex` into a new `paper/supplementary.tex` (§S1 per-pattern Core-existence, §S2 scale invariance, §S3 restricted Core LP + classification tables). The main manuscript is trimmed to exactly 30 pages (`\bibsep` compression + §2 Related Work consolidated from 5 subsections to 3); the Supplementary is 6 pages. Body references rewritten as "Supplementary Materials §S*" and "Supplementary Figure/Table S*". §6.8 adds a self-contained one-paragraph summary of the restricted-LP methodology. `scripts/verify_zip_rebuild.sh` extended to build and validate both `main.pdf` (≤30-page hard cap) and `supplementary.pdf`. Theorem/proof statements, CSV data, and figure PDFs are unchanged. Restore locally via `git checkout v2.1.8`.

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
