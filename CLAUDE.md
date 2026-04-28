# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.


## Documentation
- [Project Overview](doc/project_overview.md) — Domain, two-phase workflow, four organizational groups (JF/RB/KB/GB)
- [Project Architecture](doc/project_architecture.md) — Data flow, key classes (SchedulerData, SamplingDataHolder), source layout
- [Project Optimization Engine](doc/project_optimization_engine.md) — MCMC algorithm, 10 evaluators, 5 samplers, staged strategy
- [Project Output Generation](doc/project_output_generation.md) — Phase 2: Excel, PDF (LaTeX templates), ICS, change-diff PDF
- [Project Testing](doc/project_testing.md) — Test approach, structure, fixtures, coverage status
- [Project Setup and Dependencies](doc/project_setup.md) — Python 3.11, requirements.txt, lualatex system dep, CLI invocation


## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run optimization (phase 1)
python -m ej.scheduler.cli_interface optimize -i <input_file> -y <year> -o <output_prefix> -H <holidays_file> [--random-seed <seed>]

# Generate reports (phase 2)
python -m ej.scheduler.cli_interface generate -i <input_prefix> -H <holidays_file> -a <additional_dates_file> -y <year> -v <version> -o <old_versions> -p <output_path>

# Run tests
python -m pytest
```

PDF generation requires `lualatex.exe` to be on PATH.

## Architecture

This is a two-phase CLI tool that optimizes firestation event schedules for Milizfeuerwehr Basel-Stadt.

**Phase 1 — Optimize** (`schedule.py`): Reads an Excel input file into a pandas DataFrame via `SchedulerData`, converts it to a numpy array (`SamplingDataHolder`, 16 columns, dates as day-of-year integers), then runs a multi-process MCMC loop. Each iteration mutates dates via a `Sampler`, scores the result by composing all `Evaluator` scores multiplicatively (each returns 0–1), and accepts the candidate via a Metropolis-Hastings criterion (`min(1, p'/p) > rand()**0.7`). The global best is tracked separately from the chain state. The best result is saved back to Excel.

**Phase 2 — Generate** (`generate_output.py`): Reads the optimized Excel, then produces three output formats: a formatted Excel file, PDF reports (via LaTeX string-replacement templates in `pdf/templates/`), and `.ics` calendar files.

### Key abstractions

- **`SchedulerData`** (`util/scheduler_config.py`): Wraps the pandas DataFrame; handles Excel I/O and is the shared data object passed through both phases.
- **`SamplingDataHolder`** (`generation/sampling_data_holder.py`): Converts the DataFrame to/from a numpy array for the hot optimization loop. Column semantics are defined in `util/row_names.py`.
- **`Sampler`** (`generation/sampling/`): Abstract base with three implementations — `NoChangeDateSampler`, `NormalDateSampler` (Gaussian offset with configurable variance), and `FilteredCombinedSampler` (weighted combination that excludes holidays).
- **`Evaluator`** (`generation/evaluation/`): Ten constraint evaluators (type spread, holiday avoidance, weekend distribution, clustering penalties, etc.). All compose via multiplication so any zero-score evaluator vetoes the schedule.

### Organizational groups

Events are tagged for four groups: JF (Jugendfeuerwehr), RB, KB, GB. Group-specific filtering lives in `util/group_utils.py`; report generation produces separate outputs per group.

### Data flow summary

```
Excel input → DataFrame → numpy array → optimization loop → DataFrame → Excel + PDF (LaTeX) + ICS
```
