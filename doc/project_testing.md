# Project Testing

## Existing Tests

**Single test file:** `src/ej/scheduler/generation/test_sampling_data_holder.py`

**Framework:** `unittest.TestCase`, executed via `pytest`:
```bash
python -m pytest src/ej/scheduler/generation/test_sampling_data_holder.py
```

**Requires:** real Excel test data at `input/performance_test.xlsx`

**7 test methods** — all test `SamplingDataHolder`:

| Test | What it covers |
|---|---|
| `test_get_id_for_value` | Value→ID mapping is consistent and unique across types |
| `test_get_value_for_id` | ID→Value reverse mapping; None for invalid IDs/types |
| `test_get_data_frame` | `get_np_data()` runs without error (smoke test) |
| `test_get_scheduler_data` | **Round-trip**: Excel → numpy → DataFrame == original (critical data-integrity test) |
| `test_sort_np_data` | Row-wise sorting by column preserves all columns |
| `test_switch_dates` | Row swapping between two indices |
| `test_change_date` | Single-cell date mutation |

## Coverage Gaps

No tests exist for:
- Any of the 10 **Evaluators** (correctness of scoring logic)
- Any of the 5 **Samplers** (distribution, constraint filtering)
- **Phase 2 output generation** (Excel, PDF, ICS)
- **CLI interface** (`cli_interface.py`)
- **End-to-end optimize + generate pipeline**
- `date_scheduler.iterate()` / `generate_candidate()` / `evaluate_candidate()`
