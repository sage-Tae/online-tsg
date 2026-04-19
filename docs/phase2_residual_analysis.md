# Phase 2 Residual Binding Analysis

- Data: /Users/sage/Documents/claude/TSG_agent/code/experiments/logs/policy_comparison_v2_full.csv
- NN policy, 175 instances, 30 residual (Core empty & Thm 11 vacuous)

## Group counts

- Group 1 (r\*\* undefined): 9
- Group 2 (r \<= r\*\*): 21
- Group 3 (sanity; should be 0): 0

## Group 1 interpretation tally

- `intermediate`: 9

## Group 2 interpretation tally

- `complement-only`: 11
- `near-complement`: 10

## Combined tally across residual (Group 1 + 2)

- `complement-only`: 11
- `intermediate`: 9
- `near-complement`: 10

## Decision rubric

- near-complement / complement-only: **21** of 30
- intermediate / mixed:              **9** of 30

**Judgement (mixed):** a meaningful subset of residual cases is intermediate; consider elevating this beyond Remark.
