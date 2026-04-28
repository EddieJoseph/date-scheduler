## Why

The optimizer produces a combined score internally, but there is no way to score an existing schedule file without running a full optimization. An `evaluate` command lets users inspect how well a given schedule satisfies all constraints — both the per-evaluator breakdown and the combined product — without modifying anything.

## What Changes

- Add a new `evaluate` subcommand to the CLI alongside `optimize` and `generate`
- The command reads an Excel schedule file, scores it against all 10 evaluators, and prints results to stdout
- Arguments: `-i/--input` (Excel file), `-y/--year` (int), `-H/--holidays` (holidays file) — same pattern as `optimize`
- Output: a table of per-evaluator scores and the combined multiplicative score

## Capabilities

### New Capabilities
- `evaluate-command`: CLI subcommand that scores an existing schedule file using all 10 evaluators and reports individual and combined scores

### Modified Capabilities

## Impact

- `src/ej/scheduler/cli_interface.py` — new subcommand wired in
- New module `src/ej/scheduler/evaluate.py` (or equivalent) holding the evaluate logic
- Reuses existing evaluator instantiation pattern from `schedule.py` and `evaluate_candidate()` from `date_scheduler.py`
- No changes to evaluators, samplers, or output generation
