## Why

After the precomputed-indices change, the dominant per-evaluation cost in TypeSpreadEvaluator and WeekDayEvaluator will be the `np.var` / `np.diff` computations on per-(type,group) date subsets. In MCMC, however, typically only 1–2 events move per proposal step. The scores for all unaffected (type,group) subsets are identical to the previous candidate and don't need to be recomputed. Tracking which rows changed allows each evaluator to reuse cached per-subset scores and recompute only the 1–4 subsets that contain a changed row — reducing evaluator cost from O(subsets) to O(1) per step.

## What Changes

- **Sampler interface**: each sampler returns the mutated candidate together with the set of row indices it changed
- **Evaluator base class**: add an optional `evaluate_incremental(candidate, changed_indices, cache)` method; default implementation falls back to full `evaluate()`
- **TypeSpreadEvaluator**: implement `evaluate_incremental` — cache per-subset scores; recompute only subsets that overlap `changed_indices`
- **WeekDayEvaluator**: implement `evaluate_incremental` — same pattern
- **MCMC loop** (`schedule.py`): thread changed-index sets from sampler to evaluators; maintain per-evaluator score caches across accepted steps
- **Benchmark + improvement.md**: record results

## Capabilities

### Modified Capabilities

- `evaluator-performance`: incremental evaluation makes TypeSpreadEvaluator and WeekDayEvaluator near-O(1) per MCMC step
- `sampler-interface`: samplers now return `(candidate, changed_indices)` instead of just `candidate`
- `mcmc-loop`: loop manages per-evaluator caches and passes change information

## Non-goals

- No change to scoring formulas or output values
- No new dependencies
- Other evaluators (WeekClumping, Month, etc.) keep their existing full-scan implementations unless profiling shows them as new bottlenecks

## Impact

- All existing tests must pass
- Expected speedup: 5–10× on the two evaluators, 3–5× overall composite, assuming 1–2 date changes per step
- Requires a compatibility shim so the old `evaluate(candidate)` signature still works for tests
