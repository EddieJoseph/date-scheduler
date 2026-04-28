# Evaluator Performance Improvement

Benchmark: 5000 iterations of `evaluate_candidate` on a synthetic 70-event candidate array (year 2025, Python 3.11.9).
Times are wall-clock milliseconds for all 5000 iterations combined.

## Baseline

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 2657.9 | 58.0% |
| WeekDayEvaluator | 732.1 | 16.0% |
| WeekClumpingEvaluator | 485.8 | 10.6% |
| AssiEvaluator | 143.3 | 3.1% |
| WeekendEvaluator | 143.6 | 3.1% |
| MonthEvaluator | 113.1 | 2.5% |
| AsCleanEvaluator | 116.5 | 2.5% |
| JfHolidayEvaluator | 73.0 | 1.6% |
| HolidayEvaluator | 63.8 | 1.4% |
| SameDayEvaluator | 55.6 | 1.2% |
| **Total composite** | **5293.7** | |

## After Step 2: AsCleanEvaluator (searchsorted)

AsCleanEvaluator: 116.5 ms → 38.9 ms (−67%)

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 2796.1 | 59.6% |
| WeekDayEvaluator | 770.8 | 16.4% |
| WeekClumpingEvaluator | 491.7 | 10.5% |
| AssiEvaluator | 142.6 | 3.0% |
| WeekendEvaluator | 150.1 | 3.2% |
| MonthEvaluator | 112.9 | 2.4% |
| AsCleanEvaluator | 38.9 | 0.8% |
| JfHolidayEvaluator | 71.6 | 1.5% |
| HolidayEvaluator | 61.2 | 1.3% |
| SameDayEvaluator | 56.3 | 1.2% |
| **Total composite** | **6976.5** | |

## After Step 3: WeekDayEvaluator (vectorized arithmetic)

WeekDayEvaluator: 770.8 ms → 745.1 ms (−3%). Modest gain because filtered sub-arrays per type×group are small.

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 2841.4 | 59.7% |
| WeekDayEvaluator | 745.1 | 15.7% |
| WeekClumpingEvaluator | 521.3 | 11.0% |
| AssiEvaluator | 150.8 | 3.2% |
| WeekendEvaluator | 145.0 | 3.0% |
| MonthEvaluator | 115.8 | 2.4% |
| AsCleanEvaluator | 37.7 | 0.8% |
| JfHolidayEvaluator | 82.9 | 1.7% |
| HolidayEvaluator | 59.9 | 1.3% |
| SameDayEvaluator | 59.8 | 1.3% |
| **Total composite** | **5550.0** | |

## After Step 4: WeekClumpingEvaluator (integer arithmetic)

WeekClumpingEvaluator: 521.3 ms → 68.0 ms (−87%). Removing `np.vectorize` (Python loop overhead) is a major win.

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 2785.6 | 67.2% |
| WeekDayEvaluator | 654.5 | 15.8% |
| WeekClumpingEvaluator | 68.0 | 1.6% |
| AssiEvaluator | 161.9 | 3.9% |
| WeekendEvaluator | 142.7 | 3.4% |
| MonthEvaluator | 111.0 | 2.7% |
| AsCleanEvaluator | 39.2 | 0.9% |
| JfHolidayEvaluator | 68.5 | 1.7% |
| HolidayEvaluator | 60.0 | 1.4% |
| SameDayEvaluator | 56.3 | 1.4% |
| **Total composite** | **4591.7** | |

## After Step 5: MonthEvaluator (searchsorted)

MonthEvaluator: 111.0 ms → 76.3 ms (−31%). Note: `side='right'` required to match the original strict `<` boundary logic.

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 2708.0 | 66.4% |
| WeekDayEvaluator | 657.2 | 16.1% |
| WeekClumpingEvaluator | 90.1 | 2.2% |
| AssiEvaluator | 173.3 | 4.2% |
| WeekendEvaluator | 141.6 | 3.5% |
| MonthEvaluator | 76.3 | 1.9% |
| AsCleanEvaluator | 36.8 | 0.9% |
| JfHolidayEvaluator | 77.5 | 1.9% |
| HolidayEvaluator | 60.4 | 1.5% |
| SameDayEvaluator | 59.1 | 1.4% |
| **Total composite** | **5123.4** | |

## After Step 6: TypeSpreadEvaluator (boolean masks)

TypeSpreadEvaluator: 2708.0 ms → 1596.8 ms (−41%). Replacing `np.where`+`np.intersect1d` with combined boolean mask indexing eliminates the index materialisation cost.

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 1596.8 | 50.9% |
| WeekDayEvaluator | 758.3 | 24.2% |
| WeekClumpingEvaluator | 79.8 | 2.5% |
| AssiEvaluator | 179.5 | 5.7% |
| WeekendEvaluator | 175.8 | 5.6% |
| MonthEvaluator | 77.6 | 2.5% |
| AsCleanEvaluator | 44.9 | 1.4% |
| JfHolidayEvaluator | 87.7 | 2.8% |
| HolidayEvaluator | 69.8 | 2.2% |
| SameDayEvaluator | 68.5 | 2.2% |
| **Total composite** | **3232.0** | |

## After Step 7: HolidayEvaluator / JfHolidayEvaluator (np.isin)

HolidayEvaluator: 69.8 ms → 50.9 ms (−27%). JfHolidayEvaluator: 87.7 ms → 64.3 ms (−27%).
Overall total composite: 5293.7 ms → 2992.9 ms (−43%).

| Evaluator | Time (ms) | Share |
|---|---|---|
| TypeSpreadEvaluator | 1333.5 | 50.3% |
| WeekDayEvaluator | 683.0 | 25.7% |
| WeekClumpingEvaluator | 75.1 | 2.8% |
| AssiEvaluator | 141.0 | 5.3% |
| WeekendEvaluator | 145.7 | 5.5% |
| MonthEvaluator | 62.7 | 2.4% |
| AsCleanEvaluator | 38.3 | 1.4% |
| JfHolidayEvaluator | 64.3 | 2.4% |
| HolidayEvaluator | 50.9 | 1.9% |
| SameDayEvaluator | 58.7 | 2.2% |
| **Total composite** | **2992.9** | |
