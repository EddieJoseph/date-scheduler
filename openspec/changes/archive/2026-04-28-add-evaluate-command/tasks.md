## 1. Core evaluate module

- [x] 1.1 Create `src/ej/scheduler/evaluate.py` with an `evaluate_schedule(input_file, holidays_file, year)` function that instantiates all 10 evaluators, loads the schedule via `SchedulerData` + `SamplingDataHolder`, calls `evaluator.evaluate(candidate)` on each, and returns a list of `(name, score)` tuples plus the combined product
- [x] 1.2 Print results as an aligned table to stdout: one row per evaluator, then a separator line and the combined score

## 2. CLI integration

- [x] 2.1 Add `evaluate` subparser to `cli_interface.py` with `-i/--input`, `-y/--year`, `-H/--holidays` arguments (all required), mirroring the `optimize` command's argument style
- [x] 2.2 Wire the subparser to call `evaluate_schedule` from `evaluate.py` and exit cleanly

## 3. Verification

- [x] 3.1 Run `python -m ej.scheduler.cli_interface evaluate -i input/2026_dates_combined_1.3.xlsx -y 2026 -H <holidays_file>` and confirm all 10 evaluator scores and combined score are printed
- [x] 3.2 Confirm the input Excel file is unchanged after the command runs
