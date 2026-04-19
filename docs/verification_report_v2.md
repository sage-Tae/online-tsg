# Verification Report (v2.0.3)

**Date**: 2026-04-19
**Paper version**: v2.0.3 (EJOR major revision submission)
**Data sources**:
- `code/experiments/logs/policy_comparison_v2_full.csv` (525 rows, 3 policies)
- `code/experiments/logs/scaleup_v2.csv` (45 rows)
- `code/experiments/logs/sensitivity_v2.csv` (24 rows)
- `code/experiments/logs/seed123_core_check.csv` (5 rows)

## Summary of key reproducibility checkpoints

All values reproduced directly from the CSVs above; status ✓ means
the paper's stated value matches the CSV computation exactly.

| Claim (paper section) | Paper value | CSV-reproduced | Status |
|---|---|---|---|
| Theorem 11 applicable instances (NN, main grid) | 80 | 80 | ✓ |
| Theorem 11 fires without false positives | 14 / 14 | 14 / 14 | ✓ |
| Core empty instances, total (NN main) | 21 | 21 | ✓ |
| Near-complement instances (r ≤ r**, empty) | 7 | 7 | ✓ |
| Corollary 17: k < n−1 ⇒ Core nonempty | 79 / 79 (100%) | 79 / 79 | ✓ |
| k = n − 1: Core nonempty | 16 / 16 (100%) | 16 / 16 | ✓ |
| k = n: Core nonempty | 59 / 80 (73.8%) | 59 / 80 (0.7375) | ✓ |
| r̄ (NN overall) | 1.326 | 1.3258 | ✓ |
| r̄** (NN applicable) | 1.355 | 1.3549 | ✓ |
| r̄* (NN) | 4.351 | 4.3508 | ✓ |
| Sharpness ratio r̄* / r̄** (§6.6) | 3.21 | 3.2113 | ✓ |
| Scale-invariance max rel. std of r (Appendix B) | 0.00 | 0.00e+00 | ✓ |
| Scale-up Pattern A Thm 11 fires (n = 20, 30, 50) | 3, 4, 5 | 3, 4, 5 | ✓ |
| LKH vs Held-Karp calibration error at n = 15 | 0.000% | 1.26 × 10⁻¹⁶ | ✓ |

## Quick reproduction

```bash
python3 - <<'PY'
import pandas as pd

df = pd.read_csv('code/experiments/logs/policy_comparison_v2_full.csv')
nn = df[df['policy']=='nearest_neighbor']
print('Thm 11 applicable :', int(nn['theorem11_applicable'].sum()))
print('Thm 11 fires      :', int(nn['theorem11_fires'].sum()))
print('Core empty total  :', int((~nn['core_nonempty']).sum()))
near = nn[nn['theorem11_applicable'] & ~nn['theorem11_fires'] & ~nn['core_nonempty']]
print('Near-complement   :', len(near))

for name, cond in [('k<n-1', nn['k']<nn['n']-1),
                   ('k=n-1', nn['k']==nn['n']-1),
                   ('k=n',   nn['k']==nn['n'])]:
    s = nn[cond]
    print(f'{name:<6}: {s["core_nonempty"].sum():2}/{len(s):2} nonempty')

r_star = nn['r_star'].dropna().mean()
r_ss   = nn[nn['theorem11_applicable']]['r_ss'].mean()
print(f'r*/r** = {r_star/r_ss:.4f}')
PY
```

```bash
python3 - <<'PY'
import pandas as pd
a = pd.read_csv('code/experiments/logs/scaleup_v2.csv')
a = a[a['pattern']=='A']
for n in [20, 30, 50]:
    print(f'n={n}: {int(a[a["n"]==n]["theorem11_fires"].sum())}/5 fire')
PY
```

## Prior verification artifact

An earlier report (`verification_report_pre_freeze.md`) was generated
against pre-major-revision data (`policy_comparison.csv`, patterns
B1/B2/B5, L = 10 convention, 625 instances, 35 checkpoints at 12/12
and 95/95). That report has been retired in favor of this v2.0.3
version. The canonical data for the paper is the `*_v2.csv` / CSV family
listed above; legacy CSVs remain in `code/experiments/logs/` for
historical reference only.

## See also

- `REPRODUCIBILITY.md` — environment setup and full run commands
- `phase1_design.md` — experimental design rationale (N2 convention)
- `phase3_narrative.md` — paper revision narrative
- `phase3_results_summary.json` — aggregated numerics used in paper
