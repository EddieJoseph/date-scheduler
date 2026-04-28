## Why

The 10 MCMC evaluators have no tests, making it impossible to verify that each scoring function penalizes the right conditions or to safely refactor the optimization engine. Adding evaluator tests closes this gap and establishes a baseline for future constraint changes.

## What Changes

- Add `tests/generation/evaluation/` directory with one test file per evaluator (10 files + `__init__.py`)
- Add `make_sdh` fixture to `tests/conftest.py` to construct `SamplingDataHolder` from `make_scheduler_data` in one step
- Each evaluator gets four test layers: perfect-input → 1.0, known-violation → exact score, comparison (good > bad), and date edge cases (year-end, month boundaries, exact thresholds)
- Holiday evaluators (`HolidayEvaluator`, `JfHolidayEvaluator`) use `unittest.mock.patch` on `pd.read_excel` so no real file is needed; `blocked_dates` is set directly after construction
- Tier 2 evaluators (`AssiEvaluator`, `SameDayEvaluator`, `TypeSpreadEvaluator`, `WeekDayEvaluator`) wire their setup methods through a real `SamplingDataHolder`
- All tests use year 2025 for consistency

## Capabilities

### New Capabilities

- `evaluator-tests`: Functional test coverage for all 10 MCMC evaluators — absolute scores, formula verification, comparison ordering, and date-boundary edge cases

### Modified Capabilities

- `test-infrastructure`: Add `make_sdh` fixture to shared conftest

## Impact

- New test files only; no production code changes
- Requires `unittest.mock` (stdlib) — no new dependencies
- `pytest` test suite grows by ~10 files / ~100+ test cases
