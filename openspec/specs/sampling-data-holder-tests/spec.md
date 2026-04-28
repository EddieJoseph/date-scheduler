## ADDED Requirements

### Requirement: Test file location and framework
The `SamplingDataHolder` test file SHALL live at `tests/generation/test_sampling_data_holder.py` and use pytest-style functions (not `unittest.TestCase`). The file at `src/ej/scheduler/generation/test_sampling_data_holder.py` SHALL be deleted.

#### Scenario: Tests run via pytest
- **WHEN** `python -m pytest tests/generation/` is run
- **THEN** all tests in `test_sampling_data_holder.py` are collected and executed

### Requirement: sort_np_data test
The test SHALL verify that `sort_np_data` sorts rows by a given column index in ascending order.

#### Scenario: Sort by column 1
- **WHEN** `sort_np_data([[7,8,3],[1,2,9],[4,5,6]], 1)` is called
- **THEN** the result is `[[1,2,9],[4,5,6],[7,8,3]]`

#### Scenario: Sort by column 2
- **WHEN** `sort_np_data([[7,8,3],[1,2,9],[4,5,6]], 2)` is called
- **THEN** the result is `[[7,8,3],[4,5,6],[1,2,9]]`

### Requirement: switch_dates test
The test SHALL verify that `switch_dates` swaps only the DATE column of two rows while leaving all other columns on each row unchanged.

#### Scenario: Switch rows 1 and 2
- **WHEN** `switch_dates([[1,1,1],[2,2,2],[3,3,3]], 1, 2)` is called
- **THEN** the result is `[[1,1,1],[2,3,3],[3,2,2]]` (DATE values swap, rest stays with original row)

### Requirement: change_date test
The test SHALL verify that `change_date` updates only the DATE column of the specified row.

#### Scenario: Change date of row 0
- **WHEN** `change_date([[1,1,1],[2,2,2],[3,3,3]], 0, 4)` is called
- **THEN** row 0 column 0 becomes 4, all other values unchanged

### Requirement: SamplingDataHolder round-trip test
The test SHALL verify that converting a `SchedulerData` DataFrame to numpy and back yields a DataFrame equal to the original. Uses `make_scheduler_data` fixture — no Excel file.

#### Scenario: Round-trip preserves DataFrame
- **WHEN** a `SamplingDataHolder` is constructed from a `SchedulerData` and `get_scheduler_data()` is called
- **THEN** the exported DataFrame equals the original input DataFrame (same values, same column order)
