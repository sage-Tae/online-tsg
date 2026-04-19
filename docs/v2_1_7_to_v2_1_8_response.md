# Review Response Summary — v2.1.7 → v2.1.8

Date: 2026-04-19
Scope: EJOR 30-page compliance. The three appendices are moved
from `paper/main.tex` into a new `paper/supplementary.tex`; the
main manuscript is trimmed to exactly 30 pages; cross-references
are rewritten to address the Supplementary by section number;
`verify_zip_rebuild.sh` is extended to build and validate both
PDFs. No theoretical, experimental, figure, or CSV changes.

## Motivation

EJOR's Guide for Authors caps the main manuscript at 30 pages
(abstract, figures/tables, body, references, and appendices
inclusive). v2.1.7's `main.pdf` was 35 pages. The three appendices
all fall into EJOR's explicit "Supplementary Material" categories:

- Appendix A (per-pattern Core-existence breakdown): "Complete data
  and detailed results for result replication."
- Appendix B (scale-invariance verification): "Long descriptions of
  empirical settings / additional empirical verification."
- Appendix C (restricted Core LP methodology + case tables):
  "Very technical or repetitive proofs" and "Complete data ... for
  result replication."

Moving the three appendices to a separate Supplementary file is
therefore precisely the EJOR-recommended remedy.

## Fix 1: new `paper/supplementary.tex`

A standalone document sharing `references.bib` with the main
manuscript. Renumbers with an `S` prefix (`\renewcommand{\thesection}{S\arabic{section}}`
and matching for figures / tables) so the main manuscript can cite
items as "Supplementary Figure~S1", "Supplementary Table~S1",
"Supplementary Materials §S3", etc.

Structure:

- **§S1 Per-pattern Core-existence breakdown** (formerly Appendix A).
  Contains Figure~S1 (core-existence rate vs coalition size).
- **§S2 Scale invariance: empirical verification** (formerly
  Appendix B). Contains Table~S1 (24-instance $\alpha$-scaling grid).
- **§S3 Restricted Core LP and mechanism classification** (formerly
  Appendix C). Contains the restricted-LP methodology paragraphs,
  the 2-row scale-up seed-123 certification table, Table~S2 (10 main-grid
  near-complement cases), and Table~S3 (9 intermediate-coalition cases).

Theorem / Proposition / Corollary / Remark / Observation references
inside the Supplementary point at the main manuscript by explicit
number (e.g., "main manuscript, Theorem~11", "main manuscript,
Remark~14") because LaTeX cannot cross-reference across separate
documents.

Clean-room compile: 6 pages, 0 errors, 0 undefined refs / cites.

## Fix 2: `paper/main.tex` — appendices removed

The entire `\appendix` block (lines 754–898 of the v2.1.7 source,
roughly 145 lines corresponding to ~5 formatted pages) is deleted.
The `\appendix` directive itself is also removed.

## Fix 3: main-body cross-references rewritten

Every reference from the main body to an appendix item is replaced
by a hard-coded `Supplementary Materials §S*` / `Supplementary
Figure~S*` / `Supplementary Table~S*` reference (LaTeX cannot
auto-resolve `\ref` across separate documents, so the numbers are
hard-coded — stable because supplementary uses explicit S-prefix
numbering):

| Location (v2.1.7 line) | Before | After |
|---|---|---|
| §1 Abstract C4 (line 83) | `(Appendix~\ref{app:scale-invariance})` | `(Supplementary Materials, §S2)` |
| §2.5 Restricted Cooperation discussion (line 361) | `Appendix~\ref{app:restricted-lp} gives …` | `Supplementary Materials §S3 gives …` |
| §6.1 Design (line 463) | `We verify … in Appendix~\ref{app:scale-invariance}` | `We verify … in Supplementary Materials §S2` |
| §6.4 per-pattern (line 545) | `Appendix~\ref{app:aux} (Figure~\ref{fig:core-n})` | `Supplementary Materials §S1 (Supplementary Figure~S1)` |
| §6.4 nine $k<n-1$ (line 547) | `… deferred to Appendix~\ref{app:restricted-lp}` | `… deferred to Supplementary Materials §S3` |
| §6.8 Table 8 caption (line 677) | `… restricted Core LP (Appendix~\ref{app:restricted-lp})` | `… restricted Core LP (Supplementary Materials §S3)` |
| §6.8 Table 8 footnote (line 698) | two `Appendix~\ref{app:restricted-lp}` occurrences | two `Supplementary Materials §S3` |
| §6.8 Finding 4 (line 711) | `the Appendix~\ref{app:restricted-lp} case study` | `the Supplementary Materials §S3 case study` |
| §6.8 intractability (line 716) | `restricted Core LP of Appendix~\ref{app:restricted-lp}` | `restricted Core LP of Supplementary Materials §S3` |
| §7 Limitations (ii) (line 731) | three `Appendix~\ref{app:restricted-lp}` occurrences | three `Supplementary Materials §S3` |

A `grep -E "app:|Appendix" paper/main.tex` on the v2.1.8 source
returns zero hits.

## Fix 4: §6.8 self-contained methodology paragraph

Per the EJOR guideline that the main manuscript remain
interpretable without the Supplement, §6.8 "Solver and calibration"
gains one sentence summarizing the restricted-LP method so that
readers of the main PDF understand the scale-up certification
without flipping to the Supplement:

> Where the full Core LP is intractable to enumerate (pattern A at
> $n\ge 30$), we use a restricted Core LP over a sample
> $\mathcal{S}\subseteq\mathcal{F}$ consisting of all singletons,
> all feasible complements $N\setminus\{i\}$, the grand coalition,
> and 10,000 randomly sampled intermediate-size coalitions. A
> strictly positive first-stage LP optimum certifies Core emptiness
> on the sample, a one-sided certificate for the full Temporal Core
> (it cannot conclude nonemptiness). Full methodology and the
> near-complement / intermediate-coalition case tables are in
> Supplementary Materials §S3.

## Fix 5: 30-page compression

After appendix removal the manuscript still compiled to 31 pages
(references tail spilling onto page 31). Two low-risk compressions
applied:

1. **§2 Related Work consolidated from 5 subsections to 3**: merged
   "Static TSG/VRG" with "Dynamic and Rolling-Horizon Cooperative
   Games" into "Cooperative Routing Games: Static, Dynamic, and
   Rolling-Horizon"; merged "Online Cooperative Games" with
   "Nucleolus Computation" into "Online Cooperative Games and
   Nucleolus Computation". Content preserved verbatim, only the
   two removed subsection headings and intervening blank lines are
   dropped.
2. **`\setlength{\bibsep}{0pt plus 0.3ex}`** added just before
   `\bibliography{references}` — a standard natbib tightening that
   removes the default inter-entry vertical skip.

After these, `main.pdf` compiles to exactly 30 pages, 0 errors,
0 undefined refs / cites.

## Fix 6: `scripts/verify_zip_rebuild.sh` extended

The script previously built only `main.pdf` and checked for exactly
35 pages. It now:

- Builds both `main.pdf` and (if present) `supplementary.pdf`
  via the 3-pass `pdflatex → bibtex → pdflatex → pdflatex` sequence.
- Applies a **≤30-page hard cap** to `main.pdf` (upper bound, not
  exact equality, so minor content edits that keep the paper within
  limit don't trigger false failures).
- Applies no page cap to `supplementary.pdf` (the EJOR regulation
  only caps the main manuscript).
- Reports both PDFs' status and fails if either has undefined
  refs/cites, LaTeX errors, or a missing output.

Result on `TSG_agent_submission_v2_1_8_20260419.zip`:

```
=== Clean-room rebuild ===
  main.pdf: PASS (30 pages, limit 30)
  supplementary.pdf: PASS (6 pages)
Clean-room rebuild: PASS
```

## Fix 7: `scripts/verify_doc_consistency.sh` updated

- Current-version target bumped v2.1.7 → v2.1.8.
- Stale-page-count grep list changed from `{23, 29, 30, 34}` to
  `{23, 29, 34, 35}` — 30 is now the current main-manuscript page
  count, 35 is the retired v2.1.7 value.
- Stale-version-label regex widened from `v2\.1\.[0-6]` to
  `v2\.1\.[0-7]` so v2.1.7 mentions outside historical context get
  caught in future iterations.
- Success message now reports both `main` and `supplementary`
  expected page counts.

Result on the v2.1.8 tree: all five categories `(none)`.

## Fix 8: README.md + REPRODUCIBILITY.md updated

- Version labels synced to v2.1.8 in the standard locations.
- New `## EJOR Submission Layout` / `## EJOR Submission` sections
  describing the two-file upload procedure.
- Key-results table in README: `Appendix B/C` references updated to
  `Supplementary §S2/§S3`, with supplementary table numbers
  (`Supp. Table S2`, `Supp. Table S3`).
- Repository-tree annotation updated to reflect
  `main.pdf + supplementary.pdf` two-PDF build.
- Compile instructions in REPRODUCIBILITY include the supplementary
  3-pass sequence.
- Version-history blocks extended with the v2.1.8 entry.

## Invariants preserved

- **Theorem 6, 11, 14, 16, 18** statements and proofs: unchanged.
- **Proposition 12, Observation 15** statements: unchanged.
- **Corollary 13, 19** statements and proofs: unchanged.
- **Remark 14, 17** statements: unchanged.
- **Definitions 2, 3**: unchanged.
- All **experimental CSVs** (`policy_comparison_v2_full.csv`,
  `scaleup_v2.csv`, `sensitivity_v2.csv`, `seed123_core_check.csv`):
  unchanged bit-for-bit.
- All **figure PDFs** in `code/figures/`: unchanged bit-for-bit.
- All **Python source** under `code/src/`, `code/experiments/`,
  `code/scripts/`: unchanged.
- The **paragraph content of the moved appendices** is unchanged;
  only cross-references inside the moved blocks were rewritten from
  `Theorem~\ref{thm:empty-core}` etc. to "the main manuscript's
  Theorem~11" for standalone readability of the Supplement.

## Build status

- `main.pdf`: 30 pages, 0 errors, 0 undefined refs / cites.
- `supplementary.pdf`: 6 pages, 0 errors, 0 undefined refs / cites.
- Clean-room ZIP rebuild: PASS.
- Doc consistency check: PASS (current version = v2.1.8, main 30
  pages / supplementary 6 pages, seed123 = 2 rows).

## Artifacts (v2.1.8)

- **ZIP**: `TSG_agent_submission_v2_1_8_20260419.zip`
  (contains `paper/main.pdf`, `paper/main.tex`, `paper/supplementary.pdf`,
   `paper/supplementary.tex`, `paper/references.bib`, full `code/`
   tree, `scripts/verify_zip_rebuild.sh`,
   `scripts/verify_doc_consistency.sh`, `docs/`, `README.md`,
   `REPRODUCIBILITY.md`, `LICENSE`.)
- **SHA256 file**: `TSG_agent_submission_v2_1_8_20260419.sha256`
  (authoritative record; self-referencing SHA is intentionally not
  embedded in this document).
- **Git tag**: `v2.1.8` on the commit following this response doc.
