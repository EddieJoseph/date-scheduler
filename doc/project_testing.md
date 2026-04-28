# Project Testing

## Approach

The project uses **pytest** with a dedicated `tests/` directory at the project root. Tests are fully isolated from production code and require no external files.

Three file-loading constructors accept either a file path or a pre-loaded DataFrame, eliminating the need for mocking in tests:
- `HolidayEvaluator(holidays_source: str | pd.DataFrame, year)`
- `JfHolidayEvaluator(holidays_source: str | pd.DataFrame, year)`
- `FilteredCombinedSampler(samplers, weights, year, holidays_source: str | pd.DataFrame)`

Production callers in `schedule.py` are unaffected — they still pass path strings.

## Running Tests

```bash
# Run all tests
python -m pytest

# Verbose output
python -m pytest -v

# Specific area
python -m pytest tests/evaluation/
python -m pytest tests/sampling/
```

## Test Structure

```
tests/
  conftest.py              shared fixtures
  evaluation/
    test_type_spread_evaluator.py
    test_as_clean_evaluator.py
    test_holiday_evaluator.py
    test_jf_holiday_evaluator.py
    test_month_evaluator.py
    test_same_day_evaluator.py
    test_weekend_evaluator.py
    test_week_clumping_evaluator.py
    test_week_day_evaluator.py
    test_assi_evaluator.py
  sampling/
    test_normal_date_sampler.py
    test_filtered_combined_sampler.py
  generation/
    test_date_scheduler.py
    test_sampling_data_holder.py
```

`pytest.ini` at the project root sets `testpaths = tests` and `pythonpath = src`.

## Shared Fixtures (`tests/conftest.py`)

**`make_events(n, **kwargs)`** — the primary fixture. Returns a `(N, 16)` int16 numpy array. Column names from `SamplingRows` enum can be overridden as keyword arguments:

```python
# 3 events on days 10, 100, 200; event 2 is fixed
events = make_events(3, date=[10, 100, 200], fixed=[0, 0, 1])
```

Column defaults: `date=0`, `month=-1`, `type=0`, all flags `0`, `fixed=0`, `id` auto-increments, `order=-1`, `include=1`.

**`holidays_df()`** — minimal in-memory DataFrame matching `HolidayRowNames` schema (NAME, START, END, ONLY_JF). No file loading.

```python
def holidays_df():
    return pd.DataFrame({
        "name": ["New Year"], "start": [date(2026, 1, 1)],
        "end": [date(2026, 1, 1)], "only_jf": [False]
    })
```

## Writing a New Evaluator Test

1. Import the evaluator and `pytest`
2. Use `make_events()` to construct a scenario
3. Assert the score using `pytest.approx` for floats

```python
from ej.scheduler.generation.evaluation.week_clumping_evaluator import WeekClumpingEvaluator

def test_spread_events_score_one(make_events):
    events = make_events(4, date=[10, 60, 150, 280])
    assert WeekClumpingEvaluator(2026).evaluate(events) == pytest.approx(1.0)

def test_clumped_week_degrades_score(make_events):
    events = make_events(4, date=[7, 8, 9, 10])  # all same week
    assert WeekClumpingEvaluator(2026).evaluate(events) < 1.0
```

Each test file typically covers: happy path (score ≈ 1.0), violation cases (score degrades by the expected penalty factor), and edge cases (empty array, all-fixed events, boundary dates).

## Coverage Status

| Area | Status |
|---|---|
| `SamplingDataHolder` DataFrame↔numpy round-trip | ✅ Covered |
| All 10 Evaluators | 🔲 Planned |
| `NormalDateSampler`, `CombinedSampler` | 🔲 Planned |
| `FilteredCombinedSampler` | 🔲 Planned |
| `date_scheduler.evaluate_candidate()` | 🔲 Planned |
| `date_scheduler.generate_candidate()` | 🔲 Planned |
| Phase 2 output generation (Excel, PDF, ICS) | ⬜ Not planned |
| CLI interface (`cli_interface.py`) | ⬜ Not planned |
| End-to-end optimize + generate pipeline | ⬜ Not planned |

## Notes on the Existing Test File

`src/ej/scheduler/generation/test_sampling_data_holder.py` will be migrated to `tests/generation/test_sampling_data_holder.py`. Its Excel fixture dependency (`input/performance_test.xlsx`, currently missing) will be replaced with an in-memory DataFrame constructed via `conftest.py`.
