# Project Architecture

## Data Flow

```
Excel input
  → SchedulerData (pandas DataFrame)
  → SamplingDataHolder (numpy int16 array [n×16])
  → MCMC optimize loop (schedule.py / date_scheduler.py)
  → best DataFrame
  → Excel + PDF (LaTeX + lualatex) + ICS
```

## Key Abstractions

**`SchedulerData`** — `src/ej/scheduler/util/scheduler_config.py`
- Wraps a pandas DataFrame; handles Excel I/O (`create_from(path)`, `save_to(year, path)`)
- Shared data object passed through both phases

**`SamplingDataHolder`** — `src/ej/scheduler/generation/sampling_data_holder.py`
- Converts DataFrame ↔ compact numpy int16 array for the hot MCMC loop
- 16 columns (indexed by `SamplingRows` enum): DATE, MONTH, TYPE, AS, KB, GB, RB, MOT, ASI, KADER, OFF, SAT, FIXED, ID, ORDER, INCLUDE
- DATE stored as day-of-year (0–364); TYPE stored as mapped integer
- Maintains bidirectional type/ID dictionaries

**`RowNames` enum** — `src/ej/scheduler/util/row_names.py`
- Canonical column name strings for DataFrame access
- Also defines `HolidayRowNames` and `Groups` enums

**`SchedulerConfig`** — `src/ej/scheduler/util/scheduler_config.py`
- Container: `year`, list of `Evaluator` objects, one `Sampler` object

**`Sampler` hierarchy** — `src/ej/scheduler/generation/sampling/`
- Base: `sampler.py`
- Implementations: `NoChangeDateSampler`, `NormalDateSampler`, `UniformSampler`, `CombinedSampler`, `FilteredCombinedSampler`

**`Evaluator` hierarchy** — `src/ej/scheduler/generation/evaluation/`
- Base: `evaluator.py` — `evaluate(np_array) → float [0,1]`
- 10 implementations: TypeSpread, AsClean, Holiday, JfHoliday, Weekend, SameDay, WeekClumping, Month, Assi, WeekDay

## Source Layout

```
src/ej/scheduler/
  cli_interface.py          CLI entry point (argparse)
  schedule.py               Phase 1: MCMC orchestrator
  generate_output.py        Phase 2: report orchestrator
  plotter.py                Score convergence plot (matplotlib)
  generation/
    date_scheduler.py       MCMC iterate(), evaluate_candidate(), generate_candidate()
    sampling_data_holder.py DataFrame ↔ numpy array
    test_sampling_data_holder.py  Only test file
    sampling/               5 Sampler implementations
    evaluation/             10 Evaluator implementations
  reporting/
    excel/convert_output.py
    ics/ics_generation.py
    pdf/calendar_pdf_generation.py
    pdf/programm_pdf_generation.py
    pdf/change_table_generation.py
    new_enumerator.py       Event numbering logic
  util/
    scheduler_config.py     SchedulerData, SchedulerConfig
    row_names.py            RowNames, HolidayRowNames, Groups enums
    group_utils.py          Group-specific event filtering
    date_utils.py           Day-of-year conversions, weekday helpers
    file_generation_utils.py  LaTeX umlaut escaping, group filters
    convert_input.py        One-time config→init conversion script
```
