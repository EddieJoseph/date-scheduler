## ADDED Requirements

### Requirement: Optimize command supports resume flag
The `optimize` CLI subcommand SHALL accept a `--resume` flag. When present, the command SHALL attempt to load the last checkpoint from the output folder before running the optimization loop.

#### Scenario: Resume flag accepted by CLI
- **WHEN** the user runs `optimize` with `--resume` alongside the standard required arguments
- **THEN** the command SHALL start without error

### Requirement: State file written after every stage
After each call to `save_to()` during optimization, the system SHALL write a JSON state file at `{prefix}_state.json` containing `last_stage` (integer) and `last_phase` (integer 1–5).

#### Scenario: State file created after first stage
- **WHEN** phase 1 completes and `{prefix}1.xlsx` is saved
- **THEN** `{prefix}_state.json` SHALL exist with `{"last_stage": 1, "last_phase": 1}`

#### Scenario: State file updated on each subsequent stage
- **WHEN** any later stage N completes and `{prefix}N.xlsx` is saved
- **THEN** `{prefix}_state.json` SHALL contain `{"last_stage": N, "last_phase": P}` where P reflects the current phase

### Requirement: Resume loads last checkpoint when state file exists
When `--resume` is passed and `{prefix}_state.json` exists and the referenced xlsx file is present, the system SHALL load `{prefix}{last_stage}.xlsx` as the starting data and skip all phases up to and including `last_phase`.

#### Scenario: Resume into fixed phase
- **WHEN** state file contains `last_phase: 2` and `{prefix}2.xlsx` exists
- **THEN** phases 1 and 2 SHALL be skipped and optimization SHALL continue from phase 3

#### Scenario: Resume into open loop
- **WHEN** state file contains `last_phase: 5` and `{prefix}N.xlsx` exists
- **THEN** phases 1–4 SHALL be skipped and the open-ended loop SHALL run from iteration 0 using `{prefix}N.xlsx` as input

### Requirement: Resume falls back to fresh run when no state exists
When `--resume` is passed but `{prefix}_state.json` is absent or the referenced xlsx file is missing, the system SHALL proceed as a fresh run using the `-i` input file.

#### Scenario: No state file present
- **WHEN** `--resume` is passed and `{prefix}_state.json` does not exist
- **THEN** optimization SHALL start fresh from the `-i` input file with all phases running

#### Scenario: State file references missing xlsx
- **WHEN** `{prefix}_state.json` exists but `{prefix}{last_stage}.xlsx` is not found
- **THEN** optimization SHALL start fresh from the `-i` input file with all phases running
