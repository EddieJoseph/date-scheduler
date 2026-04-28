## Why

The optimization process can run for many hours; an interruption (crash, power loss, manual stop) discards all progress and forces a full restart. Users need a way to continue from the last saved checkpoint and to reset the output folder cleanly between runs.

## What Changes

- `optimize` command gains a `--resume` flag that automatically loads the last saved stage from the output folder and skips already-completed phases; if the output folder is empty it behaves identically to a fresh run
- A JSON state file (`{prefix}_state.json`) is written after every stage save, recording the last completed stage index and phase
- A new `clear` CLI command deletes all output files (raw xlsx, pretty xlsx, state file) for a given output prefix

## Capabilities

### New Capabilities

- `optimize-resume`: Resume an interrupted optimization run from the last checkpoint, or start fresh if no checkpoint exists
- `optimize-clear`: Clear all generated output files for a given output prefix

### Modified Capabilities

<!-- none -->

## Impact

- `src/ej/scheduler/schedule.py`: `optimize()` gains `resume` parameter; new `save_state()` helper; state written alongside every `save_to()` call
- `src/ej/scheduler/cli_interface.py`: `--resume` flag on `optimize` subparser; new `clear` subparser and dispatch
- Output folder: gains `{prefix}_state.json` as a new file type
