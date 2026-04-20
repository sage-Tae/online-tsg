# Online Traveling Salesman Games

> **Online Traveling Salesman Games: Temporal Nucleolus and the Fragility of the Core under Dynamic Arrivals**
> Seyun Jeong and Hyunchul Tae (Korea Institute of Industrial Technology)
> Submitted to *European Journal of Operational Research*, 2026

Current: v2.2.5 (April 2026)

## Overview

The Online Traveling Salesman Game is a cooperative game in which customers arrive over time and costs are allocated only among coalitions consistent with the realized arrival sequence. This repository contains the code and data used in the paper.

## Repository structure

```
.
├── code/
│   ├── src/
│   ├── experiments/
│   ├── figures/
│   ├── scripts/
│   ├── tests/
│   └── requirements.txt
├── paper/
├── README.md
├── REPRODUCIBILITY.md
└── LICENSE
```

## Quick start

```bash
pip install -r code/requirements.txt
cd code/experiments && python3 run_main.py --output logs/policy_comparison_v2_full.csv
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for environment details, seeds, and table mappings.

## Citation

```bibtex
@article{jeong2026online,
  author = {Jeong, Seyun and Tae, Hyunchul},
  title  = {Online Traveling Salesman Games: Temporal Nucleolus and the Fragility of the Core under Dynamic Arrivals},
  year   = {2026},
  note   = {Under review at European Journal of Operational Research}
}
```

## License

MIT — see [LICENSE](LICENSE).

## Contact

- Seyun Jeong, Korea Institute of Industrial Technology (KITECH) — jeongsseyyun@kitech.re.kr
- Hyunchul Tae, Korea Institute of Industrial Technology (KITECH), corresponding author — sage@kitech.re.kr
