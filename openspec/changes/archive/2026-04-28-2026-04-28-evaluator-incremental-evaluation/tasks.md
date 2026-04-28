# Tasks

## Sampler interface

- [x] Add return type `tuple[np.ndarray, set[int]]` to `Sampler.sample()` base — (candidate, changed_row_indices)
- [x] Update `NoChangeDateSampler.sample()` to return `(candidate, set())`
- [x] Update `NormalDateSampler.sample()` to return `(candidate, {changed_index})`
- [x] Update `FilteredCombinedSampler.sample()` to propagate changed indices from the chosen sub-sampler

## Evaluator base class

- [x] Add `evaluate_incremental(candidate, changed_indices, cache: dict) -> tuple[float, dict]` to `Evaluator` base — default: call `evaluate(candidate)`, return `(score, {})`
- [x] Define cache type: `dict[int, float]` mapping subset-index → cached score

## TypeSpreadEvaluator

- [x] Implement `evaluate_incremental`: for each subset, check `bool(precomputed_subsets[i] intersect changed_indices)`; reuse cached score if no overlap, recompute and update cache otherwise
- [x] Return updated cache alongside score

## WeekDayEvaluator

- [x] Implement `evaluate_incremental`: same pattern as TypeSpreadEvaluator using precomputed_subsets from the precomputed-indices change

## MCMC loop (schedule.py)

- [x] Change sampler call to unpack `(candidate, changed_indices)`
- [x] Initialize per-evaluator cache dict at loop start
- [x] Pass `changed_indices` and cache to `evaluate_incremental`; update caches on acceptance
- [x] Ensure global-best tracking still works correctly with the new interface

## Validation

- [x] Run `python -m pytest` — all tests must pass (evaluators still callable with plain `evaluate()`)
- [x] Run the performance test and record results in `improvement.md`
