# Tasks

## TypeSpreadEvaluator

- [x] Add `self.precomputed_subsets: list[np.ndarray]` in `set_types()` — one index array per (type, group) pair with ≥ 2 events; filter out singletons and empty subsets
- [x] Rewrite `evaluate()` to extract `dates = candidate[:, DATE]` once, then loop over `self.precomputed_subsets` doing `generate_score_np(dates[indices])`
- [x] Remove the four per-call group masks (mask_gb, mask_kb, mask_rb, mask_ng) from `evaluate()` — they are no longer needed there

## WeekDayEvaluator

- [x] Add `self.precomputed_subsets: list[np.ndarray]` initialized in `__init__`; populate in `add_type()` — one index array per (type, group) pair with ≥ 1 event
- [x] Rewrite `evaluate()` to extract `date_col = dates[:, DATE]` once, then loop over `self.precomputed_subsets` calling `evaluate_type_indexed(date_col[indices])`
- [x] Rename `evaluate_type(dates: ndarray)` → `evaluate_type_indexed(date_values: ndarray)` that receives a 1-D array of day-of-year integers instead of a 2-D submatrix
- [x] Replace `np.var(weekday_count)` in `evaluate_type_indexed` with an inline 4-element variance formula (avoids numpy dispatch on a 4-element array)

## Validation

- [x] Run `python -m pytest` — all tests must pass
- [x] Run the performance test and record results in `improvement.md`
