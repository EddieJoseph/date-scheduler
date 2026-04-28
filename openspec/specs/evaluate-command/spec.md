## Requirements

### Requirement: CLI evaluate subcommand
The system SHALL expose an `evaluate` subcommand in the CLI that accepts `-i/--input` (Excel schedule file path), `-y/--year` (integer year), and `-H/--holidays` (holidays file path) arguments. All three arguments are required.

#### Scenario: Invoked with all required arguments
- **WHEN** user runs `python -m ej.scheduler.cli_interface evaluate -i <file> -y <year> -H <holidays>`
- **THEN** the command exits with code 0 and prints scoring results to stdout

#### Scenario: Missing required argument
- **WHEN** user omits any of `-i`, `-y`, or `-H`
- **THEN** the CLI prints a usage error and exits with a non-zero code

### Requirement: Per-evaluator scores printed to stdout
The system SHALL print each evaluator's name and its individual score (0.0–1.0) to stdout in a human-readable aligned table.

#### Scenario: All evaluators score above zero
- **WHEN** the schedule satisfies all constraints
- **THEN** each row shows the evaluator name and a score between 0.0 and 1.0 inclusive

#### Scenario: One evaluator scores zero
- **WHEN** the schedule violates a hard constraint for one evaluator
- **THEN** that evaluator's row shows 0.0 and the combined score also shows 0.0

### Requirement: Combined score printed to stdout
The system SHALL print the multiplicative product of all evaluator scores as a single combined score after the per-evaluator table.

#### Scenario: Combined score matches product of individual scores
- **WHEN** individual evaluator scores are printed
- **THEN** the combined score equals the product of all individual scores

### Requirement: All ten evaluators used
The system SHALL instantiate and run the same set of ten evaluators used by the `optimize` command: TypeSpreadEvaluator, HolidayEvaluator, JfHolidayEvaluator, AsCleanEvaluator, WeekendEvaluator, WeekClumpingEvaluator, SameDayEvaluator, MonthEvaluator, AssiEvaluator, WeekDayEvaluator.

#### Scenario: Evaluate runs all evaluators
- **WHEN** the evaluate command is run on a valid schedule file
- **THEN** scores for all ten evaluators are shown in the output

### Requirement: Schedule file is not modified
The system SHALL read the input Excel file without writing any changes to it or producing any output files.

#### Scenario: File unchanged after evaluation
- **WHEN** evaluate command completes successfully
- **THEN** the input Excel file's last-modified timestamp and contents are unchanged
