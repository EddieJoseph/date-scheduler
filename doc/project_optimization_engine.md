# Project Optimization Engine

## Algorithm: Metropolis-Hastings MCMC

**Entry:** `schedule.optimize()` → `date_scheduler.iterate()`

**Core loop** (in `date_scheduler.py`):
1. Generate candidate by mutating current state via Sampler
2. Score candidate: `score = ∏ evaluator.evaluate(candidate)` (multiplicative — any 0 vetoes)
3. Accept if `min(1, score_new/score_old)^0.7 > rand()` (modified Metropolis-Hastings, exponent 0.7)
4. Track global best separately from chain state

**Multi-process staged strategy** (in `schedule.py`):
- 8 defined stages with varying iteration counts, then an infinite refinement loop
- `multithreaded_iteration()` runs 32 worker processes in parallel, returns the globally best

**`generate_candidate()`** modes:
- Global (`limit=False`): resample ALL non-fixed events independently
- Local (`limit=True`): mutate 1–3 randomly selected events; 50% chance to swap two dates directly

## Samplers (`src/ej/scheduler/generation/sampling/`)

| Class | Behavior |
|---|---|
| `NoChangeDateSampler` | Identity (no change) |
| `UniformSampler` | Random uniform shift mod 365 |
| `NormalDateSampler(mean, variance)` | Gaussian offset mod 365 |
| `CombinedSampler(samplers, weights)` | Weighted mixture |
| `FilteredCombinedSampler(...)` | Like Combined but rejection-samples blocked dates |

**Production sampler:** `FilteredCombinedSampler` with three `NormalDateSampler` instances:
- Small σ²=3 (weight 0.6), Medium σ²=30 (weight 0.3), Large σ²=150 (weight 0.1)
- Blocked dates: all holidays (non-JF), all Fridays, all Saturdays, all Sundays

## Evaluators (`src/ej/scheduler/generation/evaluation/`)

| Evaluator | Penalty Formula | What it enforces |
|---|---|---|
| `TypeSpreadEvaluator` | `1/(1+√(variance/10000))` per (type,group) | Even spacing of same-type events within each group |
| `AsCleanEvaluator` | `0.6^violations` | ≥3 working days between consecutive AS events |
| `HolidayEvaluator` | `0.8^violations` | Non-fixed events avoid holidays |
| `JfHolidayEvaluator` | `0.8^violations` | TYPE='J' events avoid JF-specific holidays |
| `WeekendEvaluator` | `0.6^violations` | Non-SAT events off Fri/Sat/Sun; SAT events on Saturdays only |
| `SameDayEvaluator` | `0.3^violations` | No 2+ non-INFO events on same day |
| `WeekClumpingEvaluator` | `0.99^(>2/wk) × 0.9^(>3/wk) × 0.5^(>5/wk)` | Spread events across weeks |
| `MonthEvaluator` | `0.85^(month_delta)` | Events with MONTH constraint stay in correct month |
| `AssiEvaluator` | `0.5^violations` | ASI/ASIKVK sequence ORDER must be non-decreasing |
| `WeekDayEvaluator` | `1/(1+√(variance/10))` per (type,group) | Balance weekday spread (Mon–Thu) for KP/F/ASI types |

**Note:** `TypeSpreadEvaluator.set_types(sampling_data_holder)` must be called to initialize type-ID mappings before the optimization loop starts.
