## Why

TypeSpreadEvaluator (50%) and WeekDayEvaluator (26%) together consume ~75% of total evaluation time. Both evaluators share the same structural problem: every call to `evaluate()` recreates boolean masks over the full candidate array to partition rows by (type × group), even though type and group membership never change between MCMC candidates — only DATE values do. Moving mask creation out of the hot loop into a one-time setup eliminates the dominant overhead in both evaluators.

## What Changes

- **TypeSpreadEvaluator**: precompute integer index arrays for each (type, group) combination at `set_types()` time; skip singleton subsets; in `evaluate()` index only the DATE column using precomputed arrays
- **WeekDayEvaluator**: precompute integer index arrays at `add_type()` time; skip empty subsets; in `evaluate()` index only the DATE column; replace `np.var` on the 4-element weekday-count array with a fixed-formula inline computation
- **Benchmark + improvement.md**: run the existing performance test and record results after each sub-step

## Capabilities

### Modified Capabilities

- `evaluator-performance`: TypeSpreadEvaluator and WeekDayEvaluator made faster; scoring formulas and output values are unchanged

## Non-goals

- No changes to sampling, the MCMC loop, or any other evaluator
- No new dependencies
- No architectural changes — evaluator interface is unchanged

## Impact

- All existing evaluator tests must continue to pass
- Expected speedup: 30–50% on TypeSpreadEvaluator, 30–50% on WeekDayEvaluator, net total composite reduction of ~20–30%
