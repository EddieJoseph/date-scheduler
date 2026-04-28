## Why

The single existing test file lives inside `src/`, uses `unittest.TestCase`, and depends on a missing Excel fixture — meaning all but three tests fail silently. Moving to a proper pytest layout with in-memory fixtures makes the suite runnable and sets the foundation for expanding coverage.

## What Changes

- Add `pytest.ini` at project root (sets `testpaths = tests`, `pythonpath = src`)
- Add `tests/conftest.py` with `make_events` and `make_scheduler_data` fixtures
- Add `tests/generation/test_sampling_data_holder.py` in pytest style, with in-memory fixtures replacing all Excel file paths
- Delete `src/ej/scheduler/generation/test_sampling_data_holder.py`
- Drop private-method tests (`_get_id_for_value`, `_get_value_for_id`); keep and port utility tests (`sort_np_data`, `switch_dates`, `change_date`) and the round-trip test (`test_get_scheduler_data`)

## Capabilities

### New Capabilities

- `test-infrastructure`: pytest.ini + conftest.py fixtures that make tests runnable without external files
- `sampling-data-holder-tests`: migrated, pytest-style tests for `SamplingDataHolder` and its numpy utility functions

### Modified Capabilities

## Impact

- `src/ej/scheduler/generation/test_sampling_data_holder.py` — deleted
- `tests/` directory — created from scratch
- `pytest.ini` — new file at project root
- No changes to production code
