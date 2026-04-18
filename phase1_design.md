# Phase 1 Design Document — Online TSG Revision

**Version**: 1.0  
**Date**: 2026-04-18  
**Scope**: Foundation for full re-experimentation (Phase 2-6)

---

## 1. Dimensionless Framework

### 1.1 Normalization (N2: Steele Convention)

Customer coordinates sampled uniformly from `[0, L]²` with:
- **L = √n** (n-dependent square size)
- **speed = 1** (unit distance per unit time)
- **Customer density ≡ 1 per unit area** (invariant under n)

Rationale:
- Follows Steele (1997) Euclidean TSP textbook convention
- Yields n-invariant average inter-customer travel time ≈ β_BHH ≈ 0.7124
- Theorem 13's asymptotic form is most natural: c*(N) ~ β_BHH · n (asymptotic)
- Depot remains at origin (0, 0)

### 1.2 Dimensional Structure

Three physical scales characterize the system:
- **L**: spatial extent
- **v**: vehicle speed  
- **τ**: mean inter-arrival interval

Dimensional analysis yields one dimensionless control parameter:

```
ρ = (L/v) / τ
  = (characteristic travel time) / (mean arrival interval)
```

All theoretical bounds and empirical statistics depend only on `(n, ρ)`.

### 1.3 Scale Invariance

Under joint rescaling:
```
(L, v, τ) → (αL, αv, ατ)  ∀α > 0
```
all observables (r, r**, r*, k, Core stability) are preserved.

Note: Individual rescaling (e.g., L alone) does NOT preserve observables.

---

## 2. Arrival Pattern Taxonomy

### 2.1 Pattern Definitions (ρ-based)

Given base travel time ≈ 0.7124 in N2 convention, intervals computed as `τ = 0.7124 / ρ`.

| Pattern | Structure | ρ | Interval τ | Regime |
|---------|-----------|---|-----------|--------|
| A | All simultaneous (t=0) | ∞ | 0 | Saturated |
| B_heavy | Sequential uniform | 4.0 | 0.178 | Queue piles up (near saturation) |
| B_medium | Sequential uniform | 2.0 | 0.356 | Balanced |
| B_light | Sequential uniform | 0.5 | 1.425 | Queue drains |
| C | Clustered (2 batches) | 2.0 | 0.356 | Medium + spatial interleave |
| D | Reverse zig-zag | 1.0 | 0.712 | Medium + worst-case NN |
| E | Poisson random | 1.0 | 0.712 | Medium + stochastic |

### 2.2 Pattern Mapping from Previous Paper

| Previous name | New name | ρ relationship |
|---|---|---|
| A (simultaneous) | A | ∞ (unchanged semantically) |
| B1 (λ=1) | B_heavy | ρ=4.0 |
| B2 (λ=2) | B_medium | ρ=2.0 |
| B5 (λ=5) | B_light | ρ=0.5 |
| C (clustered) | C | ρ=2.0 |
| D (reverse) | D | ρ=1.0 |
| E (random) | E | ρ=1.0 |

**Important**: The previous paper's λ values (1, 2, 5) were interval lengths in 
the old L=10 convention. In N2 convention, these correspond to different ρ 
regimes (effectively flipped ordering: smaller interval → heavier load).

### 2.3 Coverage Check

Pattern set covers the ρ-spectrum:
- **ρ = ∞** : A (k = n saturation)
- **ρ = 4.0** : B_heavy (k close to n, Theorem 11 applicable)
- **ρ = 2.0** : B_medium, C (intermediate regime)
- **ρ = 1.0** : D, E (balanced)
- **ρ = 0.5** : B_light (k small, Corollary 16 protection)

Plus Structure diversity: sequential / clustered / reversed / stochastic.

---

## 3. Experimental Grid

### 3.1 Main Study

- **n**: {5, 7, 10, 12, 15} (5 sizes)
- **patterns**: {A, B_heavy, B_medium, B_light, C, D, E} (7 patterns)
- **seeds**: {7, 42, 99, 123, 256} (5 seeds)
- **policies**: {NN, CI, BR}

Total: 175 instances × 3 policies = 525 policy-instance pairs (same as before).

### 3.2 Scale-up Study

- **n**: {20, 30, 50}
- **patterns**: {A, B_medium, C} (representative regimes)
- **seeds**: same 5 seeds
- **policy**: NN only

Total: 45 instances.

### 3.3 Sensitivity Verification (NEW - Appendix B)

Scale invariance empirical check:
- Fix: n ∈ {10, 20}, pattern ∈ {B_heavy, B_medium, C}, seed=42
- Vary: α ∈ {0.5, 1.0, 2.0, 5.0}
- Apply: `(L, v, τ) → (α·L, v, α·τ)` (note: keeping v=1 fixed is equivalent 
  to joint rescaling, since ρ = (L/v)/τ only depends on L/τ)
- Expected: all statistics (r, r**, k, core_nonempty) identical across α

Total: 6 configurations × 4 alphas = 24 additional instances.

---

## 4. Theoretical Reconciliation

### 4.1 Theorem 11 Revisited

r > r** ⇒ Core empty (unchanged).

Under N2, in the limit:
```
r** - 1 = min_i δ_i / c*(N)
       ≤ (2·L·√2) / (β_BHH · L · √n · (1+o(1)))
       = 2√2 / (β_BHH · √n) (1+o(1))
       = O(n^(-1/2))
```
L cancels exactly, confirming the rate is normalization-independent.

### 4.2 Corollary 16 Revisited

k < n-1 ⇒ Complement mechanism blocked (unchanged, pure combinatorial).

### 4.3 Theorem 13 Revisited

Under N2: c*(N) ~ β_BHH · √n · L = β_BHH · n (since L = √n).

So r** - 1 = O(1/n^(1/2)) where the 1/√n rate comes from δ_i = O(L) = O(√n) 
in numerator divided by c*(N) = O(n) in denominator. Yielding:

```
r** - 1 = O(√n / n) = O(n^(-1/2))  ✓
```

Same rate as before, just cleaner expressions.

---

## 5. Implementation Plan (Phase 2 Preview)

### 5.1 Code Changes Required

1. **`code/src/generators.py`** (new module extracted from run_all.py):
   - `generate_customers(n, seed, L=None)`: default L=√n
   - `generate_arrivals(n, pattern, positions, seed, rho=None)`: ρ-based

2. **`code/experiments/run_main.py`** (rewrite run_all.py):
   - Use new generators
   - Emit additional CSV columns: `L`, `rho`, `tau`

3. **`code/experiments/run_scaleup.py`** (new or updated):
   - 3 patterns × 3 n values × 5 seeds

4. **`code/experiments/run_sensitivity.py`** (NEW):
   - Scale invariance verification
   - Vary α, check statistics stability

### 5.2 CSV Schema Addition

New columns in outputs:
```
L, rho, tau, alpha (for sensitivity)
```

Existing columns (n, pattern, seed, policy, r, k, etc.) preserved for 
backward compatibility.

### 5.3 Figure Script Updates

All `code/figures/*.py` need:
- Pattern name mapping (B1 → B_heavy, etc.)
- Potentially new figure: ρ-regime plot

---

## 6. Paper Revision Plan (Phase 5 Preview)

### 6.1 New Section 6.1 (Design)

Must include:
1. N2 normalization statement with Steele citation
2. Dimensionless framework (ρ definition)
3. Scale invariance statement and verification pointer (Appendix B)
4. Pattern taxonomy with ρ values explicit

### 6.2 Section 6.4 (Cor 16 verification)

Seed 123 case handling: explain that intermediate-coalition mechanism 
(distinct from Theorem 11) can still fire. Table data corrected.

### 6.3 Section 6.8 (Scale-up)

Table 8 statements aligned with actual data. "in each case" claim weakened 
where false (seed 123 case explicitly discussed).

### 6.4 New Appendix B (Scale Invariance)

Empirical verification of joint rescaling invariance:
- Table B.1: same statistics across α = 0.5, 1.0, 2.0, 5.0
- Confirmation that (n, ρ) are sufficient dimensional control parameters

### 6.5 Overall Tone Adjustment

- "Platform design principle" language → "suggestive evidence"
- Claims distinguish theoretical (universal) from empirical (observed in grid)

---

## 7. Success Criteria for Phase 6 Verification

Revised checkpoints (expanded from 35 to ~50):

Original 35 checkpoints (recomputed with new data):
- Example 4 allocation (5)
- Theorem 11 contingency (5)
- Corollary 16 regimes (3)
- Pattern-level stats (8)
- Dispatch policy (3)
- Scale-up cells (9)
- Derived claims (2)

NEW checkpoints:
- Pattern name consistency (paper ↔ code, 7)
- ρ value correctness (7)
- Scale invariance empirical (6 configs × stable statistics)
- Seed 123 / outlier cases correctly described in paper (1-3)

---

## 8. Risk Log

| Risk | Mitigation |
|---|---|
| Re-experiment takes much longer than estimated | Keep old results frozen (paper-submission-v1.2 tag); revert if time runs out |
| Core theorem empirical numbers change qualitatively | Document changes in revision notes; may need to reconsider Remark 14 etc. |
| Figure regeneration fails on some pattern | Test all 5 figures early (Phase 2.5) |
| Co-author disagreement on design choices | Stop for consultation before committing to Phase 3 runs |

---

## 9. Decision Log (Immutable)

- **2026-04-18**: N2 normalization adopted (L=√n, Steele convention)
- **2026-04-18**: Scale invariance defined as joint rescaling (L, v, τ) → (αL, αv, ατ)
- **2026-04-18**: Pattern complete renaming: A / B_heavy / B_medium / B_light / C / D / E
- **2026-04-18**: ρ values fixed: A=∞, B_heavy=4, B_medium=2, B_light=0.5, C=2, D=1, E=1

---

*End of Phase 1 Design Document.*
