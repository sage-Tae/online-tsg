# Review Response Summary — v2.1.4 → v2.1.5

Date: 2026-04-19
Scope: three documentation / script / data cross-consistency fixes.
No theoretical changes, no new experiments, no CSV regeneration.

## Strategy

The v2.1.4 review found that the paper, the `run_seed123_check.py`
TARGETS list, the shipped `seed123_core_check.csv`, and Appendix C
disagreed about which scale-up instances of seed 123 require the
restricted-LP certification. The underlying data are consistent;
only the narrative scope was uneven.

v2.1.5 adopts a single consistent **2-tier** structure:

- **n = 20 and n = 30 (seed 123 under Pattern A)**: Theorem 11 vacuous;
  restricted Core LP of Appendix C certifies Core emptiness via
  near-complement binding (sizes $n-1$ and $n-2$).
- **n = 50 (seed 123 under Pattern A)**: Theorem 11 fires directly
  ($r = 1.306 > r^{\ast\ast} = 1.081$); analytic certificate covers
  the case without restricted-LP evidence.

This transition from restricted-LP certification at the smaller
scales to analytic certification at $n=50$ is a natural empirical
consequence of Theorem 14's $O(n^{-1/2})$ decay of $\bar r^{\ast\ast}$.
The paper now frames Finding 4 to reflect this, and the script and
CSV agree exactly.

## Fix P1: §6.8 Finding 4 and §7 (ii) rewritten as 2-tier

**Before (v2.1.4)**: "a restricted Core LP ... certifies Core
emptiness at all three scales, with binding constraints spanning
both complement and near-complement coalitions simultaneously in
each case. ... The persistence of size-$(n-2)$ binding across scale
— even where Theorem 11 is applicable — suggests that the
near-complement mechanism is a stable structural feature ..."

**After (v2.1.5)**: "Seed 123 under Pattern A exhibits a two-tier
certification pattern consistent with Theorem 14's $O(n^{-1/2})$
tightening of $\bar r^{\ast\ast}$: [itemized, n=20/30 restricted-LP
near-complement; n=50 Thm 11 direct fire]. ... This transition from
restricted-LP certification at the smaller seed-123 scales
($n=20,30$) to analytical certification at $n=50$ is the natural
consequence of $r^{\ast\ast}\to 1$; seed 123 is not itself anomalous
in the asymptotic limit, only uncovered by Theorem 11 at finite $n$
below the transition."

§7 (ii) also updated from "observed at seed 123 across
$n\in\{20,30,50\}$ even where Theorem 11 fires" to "certifies seed
123 emptiness at $n=20,30$ via the restricted LP ... while at $n=50$
Theorem 11 directly fires and analytically covers the same instance
— a two-tier pattern consistent with $\bar r^{\ast\ast}\to 1$".

## Fix P2: `run_seed123_check.py` TARGETS reduced 5 → 2

**Before (v2.1.4)**: 5 TARGETS entries (legacy v2.1.2 scope: 3
seed-123 cases at n=20/30/50 + 2 control rows). The shipped
`seed123_core_check.csv` had only 2 rows; the Appendix C Table
cited 2 rows. If a reviewer re-ran the script, the CSV would have
5 rows, not 2, and would disagree with the paper.

**After (v2.1.5)**: 2 TARGETS entries exactly matching Appendix C
and the shipped CSV:

```python
TARGETS = [
    ('A', 20, 123),
    ('A', 30, 123),
]
```

Removed entries are preserved as inline comments with rationale.
The full 5-entry legacy version is archived at
`code/scripts/legacy/run_seed123_check_extended.py` with a header
docstring linking it to the v2.1.2 analysis path.

Structural idempotency check: `TARGETS` set equals the set of
`(pattern, n, seed)` triples in the shipped `seed123_core_check.csv`.
Re-running the script (≈5 hours total: 1 h for n=20, 4 h for n=30)
would produce a bit-identical 2-row CSV since the simulator,
restricted-LP sampler, and seeds are all deterministic.

## Fix P3: REPRODUCIBILITY.md labels updated

- Header "v2.1.3" → "v2.1.5"
- "34 pages" → "35 pages"
- "Data Files (v2.1.3)" → "Data Files (v2.1.5)"
- Step 4 `run_seed123_check.py` description updated: "2 rows"
  (not 5), ~5 h runtime (not 12 h), explicit pointer to the legacy
  5-entry script path for the v2.1.2 analysis
- Version history appended with v2.1.4 and v2.1.5 entries

All `v2.1.3` and `v2.1.2` residual occurrences in
REPRODUCIBILITY.md are now confined to the "supersedes" list in
the header and the historical version-history section, which are
the intended locations for legacy labels.

## Invariants preserved

- Theorem 6, 11, 14, 16, 18 statements + proofs: unchanged
- Proposition 12, Observation 15 statements: unchanged
- Corollary 13, 19 statements + proofs: unchanged
- Remark 14, 17 statements: unchanged
- Definition 2, 3: unchanged
- Experimental data (all v2-suffixed CSVs): unchanged bit-for-bit
- `src/*.py`, `scripts/augment_summary.py`: unchanged
- Appendix C text: unchanged (P1/P2/P3 bring peripheral items into
  agreement with what Appendix C already said)

## Build status

- Pages: 35 (unchanged from v2.1.4)
- LaTeX errors: 0
- Undefined references: 0
- Undefined citations: 0

## Artifacts (v2.1.5)

- **ZIP**: `TSG_agent_submission_v2_1_5_20260419.zip`
- **SHA256 file**: `TSG_agent_submission_v2_1_5_20260419.sha256`
  (authoritative record; self-referencing SHA is intentionally not
  embedded in this document)
- **Git tag**: `v2.1.5` on the commit following this response doc
