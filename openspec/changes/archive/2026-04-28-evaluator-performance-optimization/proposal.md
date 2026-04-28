## Why

The 10 MCMC evaluators are called millions of times during optimization. Several of them use Python-level loops or `np.vectorize` (which is just a Python loop with overhead) where pure NumPy operations are possible, and use `np.intersect1d` or boolean-mask scans where cheaper alternatives exist. Eliminating these hotspots reduces per-evaluation cost without changing any scoring logic.

## What Changes

- Add a performance test (`tests/generation/evaluation/test_performance.py`) that times `evaluate_candidate` over many iterations and records wall-clock time — no hard assertions, so it runs correctly on any machine
- Create `improvement.md` at the repo root documenting baseline timing and the measured improvement after each optimization step
- Optimize six evaluators in order of impact:
  1. `AsCleanEvaluator` — replace Python for-loop + boolean mask with vectorized `np.searchsorted`
  2. `WeekDayEvaluator` — replace Python list comprehension with direct NumPy arithmetic
  3. `WeekClumpingEvaluator` — replace `np.vectorize` wrapper with direct integer arithmetic
  4. `MonthEvaluator` — replace `np.vectorize` wrapper with `np.searchsorted` against month boundaries
  5. `TypeSpreadEvaluator` — replace index arrays + `np.intersect1d` per type×group with boolean masks
  6. `HolidayEvaluator` / `JfHolidayEvaluator` — convert `blocked_dates` from Python list to sorted `np.ndarray`; replace `np.intersect1d` with `np.isin`

## Capabilities

### New Capabilities

- `performance-test`: Repeatable timing benchmark for full `evaluate_candidate` evaluation loop, runnable on any machine
- `improvement-doc`: `improvement.md` records measured timing for baseline and each optimization step

### Modified Capabilities

- `evaluator-performance`: Six evaluators made faster; scoring formulas and output values are unchanged

## Non-goals

- No changes to sampling, candidate generation, or the MCMC acceptance criterion
- No new dependencies
- No hard timing assertions in tests

## Impact

- All existing evaluator tests must continue to pass after each step
- `improvement.md` is a documentation artifact, not a test output — it is written by hand after measuring each step
