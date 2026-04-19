# Review Response Summary — v2.1.3 → v2.1.4

Date: 2026-04-19
Scope: five documentation / reproducibility polish fixes; no
theoretical changes, no new experiments, no code logic changes.

## Fix 1: REPRODUCIBILITY.md gains `augment_summary.py` step

**Gap (v2.1.3)**: the reproducibility pipeline jumped from
`run_main.py` (which emits an 18-column CSV) directly to
`make_figures_v3.py` (which reads 20-column CSV with `r_sss` and
`empty_mechanism` added). A fresh reader following the guide would hit
a `KeyError` at figure regeneration.

**Fix**: REPRODUCIBILITY.md now includes Step 1.5 between Main study
and Scale-up:

> `python3 scripts/augment_summary.py`
> reads and overwrites `code/experiments/logs/policy_comparison_v2_full.csv`
> in place, adding `r_sss` (Proposition 12 threshold) and
> `empty_mechanism` (4-way classification) columns. ~15 min runtime;
> idempotent; required before Step 4 (restricted-LP) and Step 5
> (figures).

Step 4 and Step 5 entries now carry a "requires augmented CSV" note.

## Fix 2: `seed123_core_check.csv` aligned with Appendix C (2 rows)

**Gap**: v2.1.2 had 5 rows in the CSV (the original v2.1.2 case
study), but the v2.1.2 Appendix C table was pared down to 2 rows
(n=20 and n=30 seed 123 under Pattern A). The other 3 rows (n=50
seed 123, n=20 seed 7, n=30 seed 42) were absorbed into the
Theorem 11 fires count and never re-cited.

**Fix (Option A)**: CSV shrunk to the 2 rows that match Appendix C's
table. The 3 legacy control rows are preserved at
`code/experiments/logs/legacy/seed123_core_check_extended.csv` with
`**/logs/legacy/` in `.gitignore` so they (a) stay locally available
for a reviewer who wants to retrace the v2.1.2 analysis path, and
(b) do not enter the submission ZIP or clutter the public repo.

Grep verification beforehand confirmed no paper / figure / script
references the 3 legacy rows.

## Fix 3: §6.8 Summary B_medium nonemptiness tone-down

**Gap**: Finding 3 and the Table 8 footnote were tone-downed in
v2.1.3, but the §6.8 Summary paragraph still read "whenever $\bar
k<n-1$ the Core is nonempty irrespective of the realized competitive
ratio". This still overclaimed, because `run_scaleup_v2.py` uses a
restricted LP at n > 15, not full $2^n-1$ enumeration.

**Fix**: §6.8 Summary now reads:

> "$\bar k<n-1$ analytically rules out both complement-based
> mechanisms (Theorem 11 and Proposition 12), and no Core violation
> is observed in our sampled restricted LP even at $\bar r$ as high
> as 1.39 at n=50 for B_medium. The absence of violation in the
> sampled LP does not constitute a full-F proof of Core nonemptiness
> (cf. §7 (ii) restricted-LP caveat), but it is consistent with the
> main-grid observation that intermediate-coalition empty Cores
> vanish under cheapest-insertion and batch re-optimization (§6.7)."

The strong claim is replaced by the analytical claim (complement
mechanisms blocked) plus the empirical observation (no sampled-LP
violation) with an explicit caveat.

## Fix 4: README.md current-version label and history

**Gap**: README still carried "major revision v2.0" in the header;
only `paper-submission-v2.0` / `v2.0.1` were listed in the
reproducibility-tag section.

**Fix**: README header now says:

> Current version: v2.1.4 (major revision, April 19, 2026)
>
> Version history:
> - v2.0.x — initial submission (v2.0, v2.0.1, v2.0.2, v2.0.3)
> - v2.1.0 — first-round review response (superseded; F-generation bug)
> - v2.1.2 — F-generation fix + 4-mechanism taxonomy (Proposition 12, Observation 15)
> - v2.1.3 — documentation sync (Conclusion, Figure 1 caption, README, Nucleolus scope, B_medium caveat)
> - v2.1.4 — reproducibility polish (augment step, seed123 CSV alignment, §6.8 Summary tone-down, version labels)

## Fix 5: SHA256 recorded correctly (this document)

The v2.1.3 response document mistakenly listed the intermediate
(pre-docs-commit) SHA `5ee13578...` rather than the final v2.1.3 ZIP
SHA `3a5312c3...`. This v2.1.4 response document records the final
v2.1.4 ZIP SHA below; the prior `review_response_summary.md` is
retained unchanged as an append-only history (its SHA field remains
internally consistent with the intermediate ZIP it was computed
against, even if superseded by v2.1.4).

## Invariants preserved

- Theorem 6, 11, 16, 18 statements + proofs: unchanged
- Proposition 12, Observation 15 statements: unchanged
- Corollary 13, 19 statements + proofs: unchanged
- Remark 14, 17 statements: unchanged
- Definition 2, 3: unchanged
- Experimental data (policy_comparison_v2_full.csv, scaleup_v2.csv,
  sensitivity_v2.csv): unchanged bit-for-bit; only the 5-row
  seed123_core_check.csv was trimmed to its 2 cited rows (legacy
  copy retained untracked).
- Source code (`src/*.py`, `scripts/augment_summary.py`): unchanged

## Build status

- Pages: 34 (unchanged)
- LaTeX errors: 0
- Undefined references: 0
- Undefined citations: 0

## Artifacts (v2.1.4)

- **ZIP**: `TSG_agent_submission_v2_1_4_20260419.zip` (742 KB, 66 files)
- **SHA256 file**: `TSG_agent_submission_v2_1_4_20260419.sha256`
- **SHA256**: recorded in the accompanying `TSG_agent_submission_v2_1_4_20260419.sha256` file (hash self-referencing issue: embedding the final ZIP SHA inside a document that the ZIP itself contains is impossible, so the authoritative record is the separate `.sha256` file).
- **Git tag**: `v2.1.4` on commit `b00813e`
