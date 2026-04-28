## Context

The `optimize` command runs a multi-phase MCMC loop that can take many hours. Phases 1–4 are fixed one-shot batches; phase 5+ is an open-ended loop of up to 1000 iterations. After every stage the best result is saved to an Excel file (`{prefix}N.xlsx`). Currently, any interruption discards all progress.

The output prefix (`-o data`) acts as a namespaced file family: `data1.xlsx`, `data2.xlsx`, `data_pretty1.xlsx`, etc. This existing convention is the natural anchor for state persistence.

## Goals / Non-Goals

**Goals:**
- Allow resuming from the last completed stage with no data loss beyond the in-progress batch
- Make `--resume` safe to use unconditionally (no-op when folder is empty)
- Provide a `clear` command to reset the output folder to a clean state

**Non-Goals:**
- Checkpointing mid-batch (within a `batch_iterations` call)
- Persisting the RNG state for exact reproducibility across resume
- Migrating existing output files that predate the state file

## Decisions

### D1: State stored as JSON alongside output files

State is written to `{prefix}_state.json` (e.g., `data_state.json`) after every stage save.

Fields:
```json
{ "last_stage": 7, "last_phase": 5 }
```

`last_stage` is the integer index of the last saved xlsx file. `last_phase` is 1–4 for the four fixed phases, 5 for the open-ended loop.

**Alternatives considered:**
- Encode state in the filename (e.g., `data_stage7.xlsx`): avoids a new file type but requires fragile filename parsing to reconstruct state.
- Single "latest" symlink/pointer file: cross-platform issues on Windows.

JSON alongside output is consistent, human-readable, and trivially parseable.

### D2: `--resume` is idempotent when no state exists

If `{prefix}_state.json` is absent or unreadable, `--resume` falls through to a normal fresh run using `-i`. This means users can always pass `--resume` defensively without risk.

### D3: Phase 5+ loop always restarts from iteration 0 on resume

The open-ended loop is "keep improving until stopped." Tracking remaining iterations adds complexity with no practical benefit — the user controls termination via Ctrl+C regardless.

### D4: `-i` remains required on the CLI, but is ignored on successful resume

Keeping `-i` required avoids a special-case argparse path and ensures the argument is always present. When a state file is found, the input is overridden silently; the specified `-i` file is never read. This is noted in the `--resume` help text.

### D5: `clear` uses glob on `{prefix}*.xlsx` plus explicit state file deletion

`glob.glob(f"{prefix}*.xlsx")` cleanly captures all raw and pretty stage files regardless of how many stages were run. The state file is deleted separately. No confirmation prompt.

## Risks / Trade-offs

- **Stale state after manual file deletion** → If a user deletes xlsx files but not the state file, resume will attempt to load a missing file and fail with a clear error. Mitigation: check that the target xlsx exists before resuming; fall back to fresh run if missing.
- **Prefix collision** → If two runs share the same prefix in the same folder, the state file is overwritten. Mitigation: out of scope — this is the same risk that already exists for the xlsx files.
- **Windows path handling** → `glob.glob` and `os.path` handle Windows paths correctly; no special casing needed.

## Migration Plan

No migration needed. Existing output folders without a `_state.json` file behave exactly as before: `--resume` treats them as empty and starts fresh.
