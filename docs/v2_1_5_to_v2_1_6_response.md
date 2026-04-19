# Review Response Summary — v2.1.5 → v2.1.6

Date: 2026-04-19
Scope: three submission-ZIP rebuildability fixes.
No theoretical changes, no new experiments, no CSV regeneration, no figure regeneration.

## Motivation

Clean-room verification of the v2.1.5 submission ZIP revealed that a
fresh reviewer who extracts `TSG_agent_submission_v2_1_5_20260419.zip`
and runs the prescribed `pdflatex → bibtex → pdflatex → pdflatex`
sequence in `paper/` cannot rebuild `main.pdf`. The failure is a
`! LaTeX Error: File 'figX.pdf' not found.` coming from the
`\graphicspath` directive in `main.tex`, which points at a
`../figures/` location that exists in the development tree (as a
symlink to `../code/figures/`) but is not shipped in the ZIP.

v2.1.6 fixes this path sensitivity and updates two residual
documentation items so that the ZIP is self-rebuildable and
self-consistent.

## Fix P1: `paper/main.tex` `\graphicspath` made self-contained

**Before (v2.1.5)**: `\graphicspath{{../figures/}}`

**After (v2.1.6)**: `\graphicspath{{../figures/}{../code/figures/}}`

The two-entry list preserves the existing local-development workflow
(where `figures/` at the repo root is a symlink to `code/figures/`)
while adding `../code/figures/` as a direct fallback, which is the
path shipped inside the ZIP. `pdflatex` tries the directories in
order and picks the first match, so behaviour on the development
tree is unchanged.

## Fix P2: `REPRODUCIBILITY.md` Data-Files table corrected

**Before (v2.1.5)**:

```
| `seed123_core_check.csv` | 5 | Near-complement certification (Appendix C) |
```

**After (v2.1.6)**:

```
| `seed123_core_check.csv` | 2 | Near-complement certification (Appendix C; n=20
  and n=30 seed 123 under Pattern A — legacy 5-row version at
  `logs/legacy/seed123_core_check_extended.csv`) |
```

The shipped CSV has had 2 rows since v2.1.4 and the paper's Appendix C
Table cites exactly those 2 rows; only this Data-Files summary still
carried the legacy `5` from the v2.1.2 scope. Paper narrative, script
TARGETS (`run_seed123_check.py`), and the Appendix C table were
already consistent at 2 in v2.1.5 — this is purely a table sync fix.

## Fix P3: `scripts/verify_zip_rebuild.sh` added

A new top-level script automates the clean-room rebuild test so that
future submissions cannot regress on P1-class bugs:

```
Usage: scripts/verify_zip_rebuild.sh <path-to-submission.zip>
```

The script extracts the ZIP into a temporary directory, runs the
standard 3-pass LaTeX sequence, parses page count and
error / undefined-reference / undefined-citation counts from the
log, and exits 0 only if pages = 35 with 0 errors, 0 undef refs,
and 0 undef cites. Result on
`TSG_agent_submission_v2_1_6_20260419.zip`:

```
Clean-room rebuild: PASS (35 pages)
```

## Also touched (version-metadata sync)

- `README.md` header `Current version: v2.1.4` → `v2.1.6`; version
  history block gains v2.1.5 and v2.1.6 entries.
- `REPRODUCIBILITY.md` header `v2.1.5` → `v2.1.6`; supersedes list
  gains `v2.1.5`; version-history block marks v2.1.5 as intermediate
  and appends a v2.1.6 entry.

## Invariants preserved

- Theorem 6, 11, 14, 16, 18 statements + proofs: unchanged
- Proposition 12, Observation 15 statements: unchanged
- Corollary 13, 19 statements + proofs: unchanged
- Remark 14, 17 statements: unchanged
- Definition 2, 3: unchanged
- Paper body text (sections 1–7, Appendix A/B/C): unchanged
- Experimental data (all v2-suffixed CSVs): unchanged bit-for-bit
- Figures (all five PDFs in `code/figures/`): unchanged bit-for-bit
- `src/*.py`, `scripts/augment_summary.py`,
  `experiments/run_seed123_check.py`: unchanged

The only files modified in v2.1.6 are:

1. `paper/main.tex` (one `\graphicspath` line)
2. `REPRODUCIBILITY.md` (version labels + one table row)
3. `README.md` (version labels)
4. `scripts/verify_zip_rebuild.sh` (new file)
5. `docs/v2_1_5_to_v2_1_6_response.md` (this file)

## Build status

- Pages: 35 (unchanged from v2.1.5)
- LaTeX errors: 0
- Undefined references: 0
- Undefined citations: 0
- Clean-room ZIP rebuild: PASS

## Artifacts (v2.1.6)

- **ZIP**: `TSG_agent_submission_v2_1_6_20260419.zip`
- **SHA256 file**: `TSG_agent_submission_v2_1_6_20260419.sha256`
  (authoritative record; self-referencing SHA is intentionally not
  embedded in this document)
- **Git tag**: `v2.1.6` on the commit following this response doc
