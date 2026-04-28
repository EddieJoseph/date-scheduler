## 1. Project Configuration

- [x] 1.1 Create `pytest.ini` at project root with `testpaths = tests` and `pythonpath = src`

## 2. Test Infrastructure

- [x] 2.1 Create `tests/__init__.py` and `tests/generation/__init__.py`
- [x] 2.2 Create `tests/conftest.py` with `make_events(n, **kwargs)` fixture returning `(N, 16)` int16 numpy array
- [x] 2.3 Add `make_scheduler_data` fixture to `tests/conftest.py` that builds a valid in-memory `SchedulerData` with all 22 columns required by `SamplingDataHolder`

## 3. Migrate Tests

- [x] 3.1 Create `tests/generation/test_sampling_data_holder.py` with pytest-style tests for `sort_np_data`, `switch_dates`, and `change_date`
- [x] 3.2 Add round-trip test `test_round_trip` using `make_scheduler_data` fixture (replaces `test_get_scheduler_data`)
- [x] 3.3 Delete `src/ej/scheduler/generation/test_sampling_data_holder.py`

## 4. Verify

- [x] 4.1 Run `python -m pytest -v` and confirm all tests pass with no warnings about missing files
