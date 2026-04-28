## Context

The optimizer (`schedule.py`) already instantiates all 10 evaluators and scores schedules via `evaluate_candidate()` in `date_scheduler.py`. The evaluate command is purely a thin CLI wrapper over this existing machinery — read the file, build the array, call each evaluator, print results.

Current evaluator instantiation in `schedule.py`:
```python
type_spread_evaluator = TypeSpreadEvaluator()
holiday_evaluator = HolidayEvaluator(holiday_file_path, year)
jf_holiday_evaluator = JfHolidayEvaluator(holiday_file_path, year)
as_evaluator = AsCleanEvaluator(year)
weekend_evaluator = WeekendEvaluator(year)
week_clumping_evaluator = WeekClumpingEvaluator(year)
same_day_evaluator = SameDayEvaluator()
month_evaluator = MonthEvaluator()
assi_evaluator = AssiEvaluator()
week_day_evaluator = WeekDayEvaluator(year)
```

## Goals / Non-Goals

**Goals:**
- Read an Excel schedule and score it without modifying it
- Show per-evaluator scores and combined product on stdout
- Reuse existing evaluator and data-loading code without duplication

**Non-Goals:**
- Modifying the schedule or suggesting improvements
- Writing results to a file
- Exposing any evaluator parameters via CLI flags

## Decisions

**D1: New `evaluate.py` module, not extending `schedule.py`**  
The optimize function is tightly coupled to the MCMC loop. Extracting evaluator setup into a shared helper would require refactoring `schedule.py`. Instead, a new `evaluate.py` mirrors the evaluator instantiation pattern — acceptable duplication for a small, stable list.  
Alternative: Extract a `build_evaluators(holiday_path, year)` factory in a shared module. Not worth the refactor for 10 lines.

**D2: Call each evaluator individually rather than via `evaluate_candidate()`**  
`evaluate_candidate()` returns only the combined product. For per-evaluator scores we call `evaluator.evaluate(candidate)` on each and accumulate the product ourselves — same logic, explicit loop.

**D3: Plain stdout table, no file output**  
The command is for interactive inspection. A simple printed table (aligned columns) is sufficient. No JSON/CSV flag needed at this stage.

## Risks / Trade-offs

- [Duplication of evaluator list] If a new evaluator is added to `schedule.py`, `evaluate.py` must be updated manually → Mitigation: the evaluator list is short and stable; a comment in both files is sufficient.
- [No incremental evaluation] `evaluate` uses full `evaluator.evaluate()`, not the incremental variant. This is correct — we're scoring a complete static schedule, not a mutated candidate.

## Migration Plan

No data migration. New subcommand is purely additive — existing `optimize` and `generate` commands are unchanged.
