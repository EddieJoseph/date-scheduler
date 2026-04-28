## ADDED Requirements

### Requirement: Clear command removes all output files for a prefix
The CLI SHALL expose a `clear` subcommand that accepts `-o/--output` (the same output prefix as `optimize`). It SHALL delete all files matching `{prefix}*.xlsx` and `{prefix}_state.json` without prompting for confirmation.

#### Scenario: Clear deletes all stage files and state
- **WHEN** the user runs `clear -o data` and files `data1.xlsx`, `data2.xlsx`, `data_pretty1.xlsx`, `data_state.json` exist
- **THEN** all four files SHALL be deleted and no files matching `data*.xlsx` or `data_state.json` SHALL remain

#### Scenario: Clear on empty folder succeeds silently
- **WHEN** the user runs `clear -o data` and no matching files exist
- **THEN** the command SHALL complete without error and without output

### Requirement: Clear output prefix mirrors optimize output prefix
The `-o/--output` argument of `clear` SHALL use the same path semantics as `optimize -o`, so that the same prefix value passed to `optimize` can be passed directly to `clear`.

#### Scenario: Prefix with directory component
- **WHEN** the user runs `clear -o output/data`
- **THEN** files in the `output/` directory matching `data*.xlsx` and `data_state.json` SHALL be deleted
