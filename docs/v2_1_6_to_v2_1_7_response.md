# Review Response Summary — v2.1.6 → v2.1.7

Date: 2026-04-19
Scope: two documentation-polish fixes (REPRODUCIBILITY.md, README.md)
plus a new automated consistency-check script. No paper-source,
theoretical, experimental, figure, or CSV changes.

## Why this iteration exists: a methodology shift

Reviewer feedback on v2.1.4, v2.1.5, and v2.1.6 each flagged stale
labels at different locations inside the same two files (`README.md`
and `REPRODUCIBILITY.md`). Every previous fix was line-local
(“change the `5` on line 161”, “bump the header”), so each round
closed one specific hit but left the neighbouring stale pointers
intact. v2.1.7 explicitly changes method:

- **Semantic sweep**: the two documents were read end-to-end and
  every mention of version / page count / row count / metric /
  directory layout was evaluated against the v2.1.7 current-state
  table, not just scanned for the specific offending token.
- **Automated safety net**: `scripts/verify_doc_consistency.sh`
  now reproduces the sweep as a 5-category grep check. A future
  tagging attempt that regresses on any category fails loudly at
  the script level, before the submission ZIP is built.

The pair is intended to terminate the "stale label in README or
REPRODUCIBILITY" review cycle permanently.

## Fix P1: REPRODUCIBILITY.md semantic sweep

The single substantive correction is a **section-heading** stale
label that had survived three rounds of body-text fixes because it
lived in a heading rather than a sentence:

**Before (v2.1.6)**: `### 4. Restricted Core LP certification (5 instances, Appendix C)`

**After (v2.1.7)**: `### 4. Restricted Core LP certification (2 instances, Appendix C)`

The underlying step already referenced 2 rows (v2.1.5 body text) and
the shipped CSV is 2 rows, but the `§4` heading still advertised the
legacy v2.1.2 scope. Heading-local edits had been missed by the
line-number-based fix pattern in earlier rounds.

Also applied in the same sweep (cosmetic / version-label):

- Header `v2.1.6` → `v2.1.7` (line 1, line 3, line 7).
- `## Data Files (v2.1.6)` → `## Data Files (v2.1.7)` (line 152).
- "does not require restricted-LP treatment in v2.1.6" → v2.1.7 (line 97).
- "not the basis for v2.1.6's reported numbers" → v2.1.7 (line 167).
- Version-history block: v2.1.6 marked `(intermediate)`, new v2.1.7
  entry appended.
- New `## Submission Verification` section added, describing
  `scripts/verify_zip_rebuild.sh` and `scripts/verify_doc_consistency.sh`
  as the two pre-tag gates.

## Fix P3: README.md semantic sweep

- `**Current version: v2.1.6**` → `v2.1.7` (line 9).
- Version-history block: v2.1.7 entry appended (line 19).
- `## Key results (sanity checkpoints, v2.0)` → `(sanity checkpoints, v2.1.7)`
  (line 28). The table below was already on v2.1.7 numerics
  (67 = 37+11+10+9, 70/79 safeguard, sharpness 3.56/3.97);
  only the heading label lagged.
- **Repository structure block (line 55)**: the top-level
  `figures/` symlink previously listed as a tree entry was
  replaced with an inline annotation explaining that it is
  **dev-only** and NOT shipped in the submission ZIP. This matches
  the actual `TSG_agent_submission_v2_1_*.zip` layout, which
  references figures via `paper/main.tex`'s `\graphicspath`
  second entry `../code/figures/` (the fix introduced in v2.1.6).
- **Reproducibility tags section**:
  - Old entry `v2.1.2 (current, major revision): ...` replaced by
    two consolidated entries:
    - `v2.1.2 / v2.1.3 / v2.1.4 / v2.1.5 / v2.1.6 (intermediate
      major-revision iterations)` — one-sentence rollup pointing
      to the version-history block for per-iteration scope.
    - `v2.1.7 (current, major revision)` — describes this iteration
      and the new consistency-check script.
  - The v1 / v2.0 "superseded by v2.1.2" notes widened to
    "superseded by v2.1.2 and subsequent iterations" so the
    sentence does not imply v2.1.2 is still the live tip.

No other numerical / textual content in README was modified — the
reviewed key-results table values remain the v2.1.7-current values.

**Uncertain — flagged for author review (not modified)**: README
§6.6 row shows sharpness denominators `r̄** = 1.223` and
`r̄*** = 1.096` (ratios 3.56 and 3.97 respectively, which match the
published sharpness factors). The brief used `Mean r** = 1.184` as
the current value. `4.351/1.184 ≈ 3.67 ≠ 3.56`, so either the
published sharpness is conditional on a different subset than the
whole-grid mean, or one of the two numbers is stale. Since the two
denominators `1.223`/`1.096` are internally consistent with the
factor `3.56`/`3.97` and match the paper's Table 6, I did not edit
them; please confirm before the next iteration whether the
`1.184` vs `1.223` difference reflects a subsetting clarification
or an oversight.

## Fix: `scripts/verify_doc_consistency.sh` (new)

A 5-category grep check, run from the repo root:

1. **Stale version labels**: any `v2.1.[0-6]` mention outside
   historical / `supersedes` / legacy / prior-submission context.
2. **Stale page counts**: `23 pages`, `29 pages`, `30 pages`,
   `34 pages` outside version-history blocks.
3. **Stale seed123 row counts**: `5 instances` / `five cases` /
   `5 rows` / etc., with word boundaries so `525 rows` and
   `45 instances` are not false-positives, and the
   `5 → 2` transition phrasing is allowed.
4. **Orphan top-level figures/**: any `├── figures/` or
   `└── figures/` at the root of the repo-tree block in README
   (nested `│   ├── figures/` under `code/` is allowed).
5. **Stale metrics**: `1.355` (retired r̄** factor) and `3.21`
   (retired sharpness value).

Historical-context filtering is two-stage:

- Block-level: lines inside `## Version History` /
  `Version history:` / `## Reproducibility tags` blocks (up to the
  next top-level heading) are skipped entirely.
- Line-level: within non-historical text, lines containing
  `supersedes` / `legacy` / `-and-earlier` / `prior submission` /
  `historical` are also excluded.

Result on the v2.1.7 tree:

```
=== Stale version labels (non-historical) === (none)
=== Stale page counts ===                    (none)
=== Stale seed123 row counts ===             (none)
=== Orphan top-level figures/ in repo tree === (none)
=== Stale metrics (1.355 / 3.21) ===         (none)
Doc consistency check: PASS (current version = v2.1.7, 35 pages, seed123 = 2 rows)
```

## Invariants preserved

- Theorem 6, 11, 14, 16, 18 statements + proofs: unchanged
- Proposition 12, Observation 15 statements: unchanged
- Corollary 13, 19 statements + proofs: unchanged
- Remark 14, 17 statements: unchanged
- Definition 2, 3: unchanged
- `paper/main.tex`, `paper/main.pdf`, `paper/references.bib`:
  unchanged bit-for-bit from v2.1.6
- All experimental CSVs: unchanged bit-for-bit
- All figure PDFs in `code/figures/`: unchanged bit-for-bit
- `src/*.py`, `scripts/augment_summary.py`,
  `scripts/residual_binding_analysis.py`,
  `experiments/run_seed123_check.py`,
  `scripts/verify_zip_rebuild.sh`: unchanged

The only files touched in v2.1.7:

1. `README.md` — semantic sweep.
2. `REPRODUCIBILITY.md` — semantic sweep.
3. `scripts/verify_doc_consistency.sh` — new file.
4. `docs/v2_1_6_to_v2_1_7_response.md` — this file.

## Verification before tagging

```
scripts/verify_zip_rebuild.sh TSG_agent_submission_v2_1_7_20260419.zip
→ Clean-room rebuild: PASS (35 pages)

scripts/verify_doc_consistency.sh
→ Doc consistency check: PASS (current version = v2.1.7, 35 pages, seed123 = 2 rows)
```

## Build status

- Pages: 35 (unchanged from v2.1.6, paper source untouched)
- LaTeX errors: 0
- Undefined references: 0
- Undefined citations: 0
- Clean-room ZIP rebuild: PASS
- Doc consistency check: PASS

## Artifacts (v2.1.7)

- **ZIP**: `TSG_agent_submission_v2_1_7_20260419.zip`
- **SHA256 file**: `TSG_agent_submission_v2_1_7_20260419.sha256`
  (authoritative record; self-referencing SHA is intentionally not
  embedded in this document)
- **Git tag**: `v2.1.7` on the commit following this response doc
