## Context

One test file exists at `src/ej/scheduler/generation/test_sampling_data_holder.py`. It uses `unittest.TestCase` and loads a real Excel file that is not checked into the repository — making four of six tests permanently broken. The documented testing approach (in `doc/project_testing.md`) specifies pytest, a `tests/` directory at the project root, and in-memory fixtures that eliminate file I/O.

## Goals / Non-Goals

**Goals:**
- Make all tests runnable with `python -m pytest` and no external files
- Establish the directory structure and fixtures described in `doc/project_testing.md`
- Delete the misplaced test file from `src/`

**Non-Goals:**
- Adding new test coverage beyond what already exists (that is the next step)
- Modifying any production code

## Decisions

### Drop private method tests

`test_get_id_for_value` and `test_get_value_for_id` test `_get_id_for_value`, a private method. The round-trip test (`test_get_scheduler_data`) already validates that the string↔int mapping works end-to-end. Private method tests break on internal refactors even when behavior is correct.

**Alternative considered:** Keep them as regression guards. Rejected because the public contract test covers the same ground more durably.

### Use `SchedulerData.__init__` directly for test fixtures

`SchedulerData.__init__(dates: DataFrame, score: float)` already accepts an in-memory DataFrame. Tests construct a minimal DataFrame directly and pass it to `SchedulerData(df, 0.0)` — no file I/O, no mocking needed.

**Alternative considered:** Add a `SchedulerData.create_from_df()` factory. Rejected — the constructor already serves this purpose.

### Two fixtures in `conftest.py`

- `make_scheduler_data` — builds a valid `SchedulerData` from keyword overrides. Used by `SamplingDataHolder` tests.
- `make_events` — builds a `(N, 16)` int16 numpy array directly. Used by evaluator tests (future). Both live in `tests/conftest.py` so they're available across all test subdirectories.

### Minimal DataFrame schema for `make_scheduler_data`

`SamplingDataHolder._convert_from_dataframe` reads 16 columns. `_convert_to_dataframe` (needed for the round-trip test) additionally reads `name`, `time`, `theme`, `called_up`, `responsible`, `details`. The fixture must include all 22 columns. Defaults: boolean flags `False`, `month` and `order` as `NaN`, `type` as `"A"`, `id` as `"event-0"`.

## Risks / Trade-offs

- `_convert_from_dataframe` iterates with `iterrows()` using the DataFrame's index as the row index into `np_data`. The test DataFrame must have a clean 0-based index — call `reset_index(drop=True)` after construction.
- `test_get_scheduler_data` compares `initial_df.equals(export_df)` after a round-trip. Column order and dtypes must match exactly. The fixture must produce columns in the same order that `_convert_to_dataframe` emits them.
