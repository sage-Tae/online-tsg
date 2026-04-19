# Review Response Summary — v2.1.9 → v2.1.10

Date: 2026-04-19
Scope: EJOR Highlights desk-check compliance (P2, primary) plus four
package-polish items (P3-a–d). No theoretical, experimental, CSV, or
figure-data changes. Main manuscript remains 30 pages; Supplementary
remains 6 pages; new Highlights PDF is 1 page.

## Motivation

EJOR's Editorial Manager receives Highlights in a dedicated upload
slot, not as a section inside the manuscript. A submission without
a separate Highlights file fails the Managing-Editor mechanical
check at "Highlights missing" before any reviewer touches it.
v2.1.9's Highlights were inside `main.tex` only, and additionally
contained four math-mode bullets and two undefined abbreviations
(`Online TSG`, `LP`) — so even if the in-manuscript location were
accepted, the content itself violated EJOR's Highlights content
rules (≤ 85 characters / no formulae / no undefined abbreviations).

Four further package-polish items were flagged in the external
review of v2.1.9 and are resolved in the same iteration to avoid
churn:

- P3-a: `REPRODUCIBILITY.md` submission-verification example
  pointed at the v2.1.8 ZIP filename.
- P3-b: six active-text occurrences of "Appendix B" / "Appendix C"
  in `REPRODUCIBILITY.md` were not rewritten during the v2.1.8
  split and still addressed the moved appendices by their
  pre-v2.1.8 names.
- P3-c: `README.md` repository-tree listed two internal working
  files (`phase1_design.md`, `phase3_narrative.md`) that are not
  shipped in the ZIP.
- P3-d: `README.md` header title and BibTeX citation still used
  the pre-rewrite subtitle ("Empty Cores, and Complement-Coalition
  Mechanisms") while the actual paper title changed at v2.1.8 to
  "Temporal Nucleolus and the Fragility of the Core under Dynamic
  Arrivals".

## Fix P2 — EJOR Highlights as separate file (primary)

### Before (v2.1.9, in-manuscript at main.tex lines 54–61)

Five bullets, four of which contained `$...$` math mode and two of
which contained undefined abbreviations:

```
\section*{Highlights}
\begin{itemize}
\item Online TSG: coalitions restricted to feasibility under arrival dynamics.
\item Temporal Nucleolus via sequential LP over the feasibility family $\F$.
\item Sufficient emptiness bound $r>r^{\ast\ast}$, tight for complement coalitions.
\item Structural safeguard $k<n-1$ blocks the complement-coalition mechanism.
\item Asymptotic tightening $r^{\ast\ast}\to 1$ at $O(n^{-1/2})$ confirmed to $n=50$.
\end{itemize}
```

Audit: all 5 bullets ≤ 85 characters, but 4 math-mode violations
and 2 abbreviation violations.

### After (v2.1.10, separate file Draft C with bullet 3 author-adjusted)

Three new files at `paper/`:

- **`highlights.tex`**: standalone LaTeX source; compiles to 1 page,
  0 errors, 0 undefined refs/cites. Paged off (`\pagenumbering{gobble}`),
  minimal preamble, no bibliography.
- **`highlights.pdf`**: 1-page PDF built by the same 3-pass pipeline
  as the rest of the paper (actually 1-pass suffices here — no bib).
- **`highlights.txt`**: plain-text 5-bullet version for direct
  paste-in to the Editorial-Manager Highlights text box.

Final five bullets (author-selected Draft C with author-adjusted
bullet 3):

| # | Chars | Bullet |
|---|-------|--------|
| 1 | 73 | Online Traveling Salesman Game: coalitions restricted by arrival dynamics |
| 2 | 77 | Temporal Nucleolus computed by sequential linear programming over this family |
| 3 | 64 | Tight emptiness threshold for the complement-coalition mechanism |
| 4 | 75 | Bounded customer queue structurally blocks both complement-based mechanisms |
| 5 | 76 | Threshold tightens to one at the classical square-root rate; tested to fifty |

All 5 bullets ≤ 85 characters (max 77). Zero math-mode dollars,
zero abbreviations that are not already expanded inside the same
bullet (Online Traveling Salesman Game is spelled out; "linear
programming" is spelled out). Bullet 3 was author-adjusted from
the original Draft C "Single-complement emptiness threshold is
tight for complement-coalition games" (77 chars, semantically
redundant use of "complement") to "Tight emptiness threshold for
the complement-coalition mechanism" (64 chars) — saves characters
and avoids the redundancy.

Draft alternatives presented to author, formula/abbreviation/char
pre-verified before presentation:

- Draft A (minimal, 3 bullets): max 75 chars.
- Draft B (balanced, 4 bullets): max 78 chars.
- Draft C (preserve 5 bullets): max 77 chars. **Chosen.**

main.tex disposition: the author chose **Option I** (remove from
main.tex entirely; Highlights live only in the separate file).
This matches EJOR convention and eliminates future sync drift
between the two copies.

main.tex `\section*{Highlights}` block (lines 54–61 of v2.1.9)
replaced by a 3-line comment pointing to the new files.
`main.pdf` now starts at the Abstract; page count unchanged at 30.

## Fix P3-a — REPRODUCIBILITY submission-verification ZIP path

`REPRODUCIBILITY.md` line 219:

- Before: `bash scripts/verify_zip_rebuild.sh TSG_agent_submission_v2_1_8_20260419.zip`
- After:  `bash scripts/verify_zip_rebuild.sh TSG_agent_submission_v2_1_10_20260419.zip`

Grep for any residual `v2_1_[0-9]_20260419.zip` reference outside
historical context returns zero hits.

## Fix P3-b — Active "Appendix B/C" → "Supplementary Materials §S2/§S3"

Six active-text occurrences in `REPRODUCIBILITY.md` were rewritten
from pre-v2.1.8 appendix names to the current supplementary names:

| Line | Context | Before | After |
|------|---------|--------|-------|
| ~43  | Python Dependencies bullet | `in Appendix C restricted LP` | `in the Supplementary Materials §S3 restricted LP` |
| ~75  | Step 1.5 required-by | `Appendix C restricted-LP analysis` | `Supplementary Materials §S3 restricted-LP analysis` |
| ~88  | Step 3 heading | `Scale invariance (24 instances, Appendix B)` | `Scale invariance (24 instances, Supplementary Materials §S2)` |
| ~98  | Step 3 source-for | `Appendix B, Table B.1` | `Supplementary Materials §S2, Table S1` |
| ~143 | Scale-Invariance body | `(Appendix B, sensitivity_v2.csv)` | `(Supplementary Materials §S2, sensitivity_v2.csv)` |
| ~147 | Near-complement body | `and Appendix C` | `and Supplementary Materials §S3` |

Historical-context occurrences inside the "## Version History"
block (v2.0, v2.1.4, v2.1.5 entries) are intentionally preserved
because they describe the pre-v2.1.8 structure of the paper.

## Fix P3-c — README tree drops unshipped internal working files

`README.md` repo-tree lines 62–63 listed `phase1_design.md` and
`phase3_narrative.md`, neither of which is in the submission ZIP.
Both entries deleted. The tree now also includes a new `scripts/`
entry pointing to the gate-check pair (`verify_zip_rebuild.sh`,
`verify_doc_consistency.sh`), which was present in the repo since
v2.1.6 but not shown in the tree.

## Fix P3-d — README title and citation sync

Two occurrences of the pre-v2.1.8 subtitle updated:

- Line 5 (header blockquote):
  `Online Traveling Salesman Games: Temporal Nucleolus, Empty Cores, and Complement-Coalition Mechanisms`
  → `Online Traveling Salesman Games: Temporal Nucleolus and the Fragility of the Core under Dynamic Arrivals`
- Lines 100–101 (BibTeX citation `title` field): same replacement.

`grep "Empty Cores\|Complement-Coalition Mechanisms" README.md`
returns zero hits post-fix.

## Infrastructure updates

### `scripts/verify_zip_rebuild.sh`

Extended to also build and validate `highlights.pdf`:

- New `HIGH_OK` flag mirroring the existing `SUPP_OK` pattern.
- No page cap on highlights (EJOR imposes none at the document
  level; the per-bullet character cap is enforced by
  content, not by LaTeX).
- The final PASS/FAIL requires all three (`main`, `supplementary`,
  `highlights`) to succeed.

Result on `TSG_agent_submission_v2_1_10_20260419.zip`:

```
=== Clean-room rebuild ===
  main.pdf: PASS (30 pages, limit 30)
  supplementary.pdf: PASS (6 pages)
  highlights.pdf: PASS (1 pages)
Clean-room rebuild: PASS
```

### `scripts/verify_doc_consistency.sh`

- `CURRENT_VERSION` bumped v2.1.9 → v2.1.10.
- Stale-version-label regex widened `v2\.1\.[0-8]` → `v2\.1\.[0-9]`
  so v2.1.9 mentions outside historical context get caught in
  future iterations. The `\b` word-boundary in the pattern
  continues to exempt `v2.1.10` from being matched.

## Version-label sync

- REPRODUCIBILITY.md: header / supersedes list / EJOR-layout
  section (now "three files"), Data-Files heading, Legacy-CSVs
  sentence, Submission-Verification ZIP path, Version-History
  timeline (v2.1.9 marked (intermediate); new v2.1.10 entry).
- README.md: Current-version line, version-history block,
  Key-results heading, Reproducibility-tags section consolidated
  (v2.1.2–v2.1.9 into the "intermediate iterations" line; v2.1.10
  as "(current, major revision)").

## Invariants preserved

- Theorem 6, 11, 14, 16, 18 statements and proofs: unchanged.
- Proposition 12, Observation 15 statements: unchanged.
- Corollary 13, 19 statements and proofs: unchanged.
- Remark 14, 17 statements: unchanged.
- Definitions 2, 3: unchanged.
- Main manuscript body (past the Highlights removal at the
  top): unchanged.
- `paper/supplementary.tex` and `paper/supplementary.pdf`:
  unchanged bit-for-bit.
- All experimental CSVs: unchanged bit-for-bit.
- All figure PDFs in `code/figures/`: unchanged bit-for-bit
  from v2.1.9 (no regeneration in this iteration).
- `src/*.py`, `scripts/augment_summary.py`,
  `scripts/residual_binding_analysis.py`: unchanged.

Files modified in v2.1.10:

1. `paper/main.tex` — Highlights block replaced by a 3-line
   comment.
2. `paper/highlights.tex` (new).
3. `paper/highlights.pdf` (new — build artifact; gitignored).
4. `paper/highlights.txt` (new).
5. `REPRODUCIBILITY.md` — P3-a, P3-b, EJOR-layout extension,
   compile instructions for highlights, version labels.
6. `README.md` — P3-c, P3-d, version labels, reproducibility-tags
   consolidation.
7. `scripts/verify_zip_rebuild.sh` — highlights.pdf build block.
8. `scripts/verify_doc_consistency.sh` — CURRENT_VERSION +
   stale-version regex widening.
9. `.gitignore` — highlights LaTeX aux files.
10. `docs/v2_1_9_to_v2_1_10_response.md` (this file).

## Verification before tagging

```
scripts/verify_zip_rebuild.sh TSG_agent_submission_v2_1_10_20260419.zip
  main.pdf: PASS (30 pages, limit 30)
  supplementary.pdf: PASS (6 pages)
  highlights.pdf: PASS (1 pages)
Clean-room rebuild: PASS

scripts/verify_doc_consistency.sh
Doc consistency check: PASS (current version = v2.1.10,
  main 30 pages / supplementary 6 pages, seed123 = 2 rows)

Highlights audit:
  All 5 bullets ≤ 85 characters (max 77)
  All 5 bullets math-mode-free
  All 5 bullets abbreviation-free (qualified on first use)

Package polish checks:
  grep 'Empty Cores\|Complement-Coalition Mechanisms' README.md  -> 0
  grep 'phase[13]_.*\.md\|phase3_results_summary.json' README.md -> 0
  grep 'Appendix [BC]' REPRODUCIBILITY.md (active text)          -> 0
  grep 'v2_1_[0-9]_20260419.zip' REPRODUCIBILITY.md              -> 1 (v2.1.10)
```

## Build status

- Pages: main 30 / supplementary 6 / highlights 1
- LaTeX errors: 0 / 0 / 0
- Undefined references: 0 / 0 / 0
- Undefined citations: 0 / 0 / 0
- Clean-room ZIP rebuild: PASS
- Doc consistency check: PASS

## Artifacts (v2.1.10)

- **ZIP**: `TSG_agent_submission_v2_1_10_20260419.zip`
- **SHA256 file**: `TSG_agent_submission_v2_1_10_20260419.sha256`
  (authoritative record; self-referencing SHA is intentionally not
  embedded in this document)
- **Git tag**: `v2.1.10` on the commit following this response doc
