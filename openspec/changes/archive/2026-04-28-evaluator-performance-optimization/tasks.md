## 1. Performance Test and Baseline

- [x] 1.1 Create `tests/generation/evaluation/test_performance.py` — build a realistic candidate array (~70 events with representative type/group distribution), instantiate all 10 evaluators as the optimizer does, run `evaluate_candidate` for 5000 iterations, and print/record wall-clock time per evaluator and total. No assertions on timing values.
- [x] 1.2 Run the performance test, record the baseline timings in `improvement.md` (total time and per-evaluator breakdown).

## 2. Optimize AsCleanEvaluator

- [x] 2.1 Replace `get_diff_np` Python for-loop + `compare` boolean-mask scan with two vectorized `np.searchsorted` calls on the sorted `self.week_days` array: `np.searchsorted(self.week_days, as_dates[1:]) - np.searchsorted(self.week_days, as_dates[:-1])`.
- [x] 2.2 Run all existing `AsCleanEvaluator` tests — must pass unchanged.
- [x] 2.3 Run performance test and record updated timings in `improvement.md`.

## 3. Optimize WeekDayEvaluator

- [x] 3.1 Replace the Python list comprehension `[self.get_week_day(date) for date in ...]` in `evaluate_type` with direct NumPy arithmetic: `(dates[:, DATE] + self.offset) % 7`.
- [x] 3.2 Run all existing `WeekDayEvaluator` tests — must pass unchanged.
- [x] 3.3 Run performance test and record updated timings in `improvement.md`.

## 4. Optimize WeekClumpingEvaluator

- [x] 4.1 Replace `np.vectorize(self.get_week)` and the vectorized call with direct integer arithmetic: `(dates[:, DATE] + self.wd_offset) // 7`. Remove the `vectorized_get_week` attribute.
- [x] 4.2 Run all existing `WeekClumpingEvaluator` tests — must pass unchanged.
- [x] 4.3 Run performance test and record updated timings in `improvement.md`.

## 5. Optimize MonthEvaluator

- [x] 5.1 Replace `np.vectorize(get_month_from_day_of_year)` and the vectorized call with `np.searchsorted(MONTH_BOUNDS, dates_f[:, DATE]) + 1` where `MONTH_BOUNDS = np.array([31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])`. Remove the `vectorized_get_month` attribute.
- [x] 5.2 Run all existing `MonthEvaluator` tests — must pass unchanged.
- [x] 5.3 Run performance test and record updated timings in `improvement.md`.

## 6. Optimize TypeSpreadEvaluator

- [x] 6.1 Replace `np.where(...)[0]` index arrays for gb/kb/rb/ng with boolean masks computed once per `evaluate()` call. In `generate_score_np` (or inline), replace `np.intersect1d(indexes1, indexes2)` with combined boolean mask indexing: `dates[mask_type & mask_group]`.
- [x] 6.2 Run all existing `TypeSpreadEvaluator` tests — must pass unchanged.
- [x] 6.3 Run performance test and record updated timings in `improvement.md`.

## 7. Optimize HolidayEvaluator and JfHolidayEvaluator

- [x] 7.1 In `HolidayEvaluator.__init__`, convert `self.blocked_dates` from a Python list to `np.array(..., dtype=np.int16)` after building it. Replace `np.intersect1d(...)` in `evaluate` with `np.sum(np.isin(dates_f[:, DATE], self.blocked_dates))`.
- [x] 7.2 Apply the same change to `JfHolidayEvaluator`.
- [x] 7.3 Run all existing holiday evaluator tests — must pass unchanged.
- [x] 7.4 Run performance test and record final timings in `improvement.md`.

## 8. Final Verification

- [x] 8.1 Run the full test suite (`python -m pytest`) — all tests must pass.
- [x] 8.2 Review `improvement.md` — confirm each optimization step shows a measurable reduction in the affected evaluator's time.
