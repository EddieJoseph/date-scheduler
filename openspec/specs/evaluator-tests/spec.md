### Requirement: AsCleanEvaluator tests
Tests SHALL verify `AsCleanEvaluator(2025)` scoring for AS-flagged events. Days are 0-indexed (0 = Jan 1, 2025). `compare(d1, d2)` counts weekdays in the half-open interval `[d1, d2)`.

#### Scenario: Perfect score — no AS events
- **WHEN** the candidate array contains no rows with `AS=1`
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Perfect score — AS events well-separated
- **WHEN** two AS events have at least 3 weekdays between them (e.g. days 0 and 5)
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one pair below threshold
- **WHEN** two AS events have exactly 2 weekdays between them (e.g. days 0 and 2, which are Wed and Fri — only 2 weekdays in `[0,2)`)
- **THEN** `evaluate()` returns `pytest.approx(0.6 ** 1)`

#### Scenario: Comparison — well-separated beats clustered
- **WHEN** dataset A has AS events at days 0 and 10 (many weekdays apart) and dataset B has AS events at days 0 and 1
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — AS events near year-end
- **WHEN** two AS events are placed at days 360 and 364 (last days of 2025)
- **THEN** `evaluate()` returns a value between 0 and 1 without error

---

### Requirement: AssiEvaluator tests
Tests SHALL verify `AssiEvaluator` ordering constraints on ASI-type events. Setup via `SamplingDataHolder` using types `'ASI'` or `'ASIKVK'`.

#### Scenario: Perfect score — ASI events in ascending order
- **WHEN** ASI events have ORDER values `[1, 2, 3]`
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one order violation
- **WHEN** ASI events have ORDER values `[1, 3, 2]` (one descending diff)
- **THEN** `evaluate()` returns `pytest.approx(0.5 ** 1)`

#### Scenario: Exact formula — two order violations
- **WHEN** ASI events have ORDER values `[3, 2, 1]` (two descending diffs)
- **THEN** `evaluate()` returns `pytest.approx(0.5 ** 2)`

#### Scenario: Comparison — ordered beats reversed
- **WHEN** dataset A has ORDER `[1, 2, 3, 4]` and dataset B has ORDER `[4, 3, 2, 1]`
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — ASI events with ORDER = -1 are excluded
- **WHEN** some ASI events have `ORDER=-1` (sentinel for "no constraint")
- **THEN** those events do not contribute to the violation count

---

### Requirement: HolidayEvaluator tests
Tests SHALL verify `HolidayEvaluator` penalizes non-fixed events on blocked dates. `pd.read_excel` is patched to return an empty DataFrame; `blocked_dates` is set directly on the instance.

#### Scenario: Perfect score — no events on blocked dates
- **WHEN** `blocked_dates = [50, 51, 52]` and no event falls on those days
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one non-fixed event on a blocked date
- **WHEN** `blocked_dates = [10]` and one non-fixed event has `DATE=10`
- **THEN** `evaluate()` returns `pytest.approx(0.8 ** 1)`

#### Scenario: Fixed events are not penalized
- **WHEN** `blocked_dates = [10]` and one event has `DATE=10` but `FIXED=1`
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Comparison — fewer hits scores higher
- **WHEN** dataset A has 0 events on blocked dates and dataset B has 2 events on blocked dates
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — blocked date at day 0 (Jan 1)
- **WHEN** `blocked_dates = [0]` and a non-fixed event is placed at day 0
- **THEN** `evaluate()` returns `pytest.approx(0.8 ** 1)`

#### Scenario: Edge case — blocked date at day 364 (Dec 31)
- **WHEN** `blocked_dates = [364]` and a non-fixed event is placed at day 364
- **THEN** `evaluate()` returns `pytest.approx(0.8 ** 1)`

---

### Requirement: JfHolidayEvaluator tests
Tests SHALL verify `JfHolidayEvaluator` penalizes only JF-type events on JF-blocked dates. `pd.read_excel` is patched; `blocked_dates` and `jf_type` are set directly on the instance after construction.

#### Scenario: Perfect score — no JF events on blocked dates
- **WHEN** `blocked_dates = [50]` and no JF event falls on day 50
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Non-JF events on blocked dates are not penalized
- **WHEN** `blocked_dates = [50]` and only a non-JF event falls on day 50
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one JF event on a blocked date
- **WHEN** `blocked_dates = [50]` and one non-fixed JF event has `DATE=50`
- **THEN** `evaluate()` returns `pytest.approx(0.8 ** 1)`

#### Scenario: Comparison — fewer JF hits scores higher
- **WHEN** dataset A has 0 JF events on blocked dates and dataset B has 2
- **THEN** `evaluate(A) > evaluate(B)`

---

### Requirement: MonthEvaluator tests
Tests SHALL verify `MonthEvaluator` penalizes events not in their target month. `get_month_from_day_of_year` uses 0-indexed days (day 0–30 = month 1, day 31–58 = month 2, etc.).

#### Scenario: Perfect score — event in correct month
- **WHEN** an event has `MONTH=1` and `DATE` is in month 1 (day 0–30)
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Events with MONTH=-1 are ignored
- **WHEN** an event has `MONTH=-1` (no constraint)
- **THEN** it does not affect the score

#### Scenario: Exact formula — event one month off
- **WHEN** an event has `MONTH=1` but `DATE` is in month 2 (day 31–58), a difference of 1
- **THEN** `evaluate()` returns `pytest.approx(0.85 ** 1)`

#### Scenario: Comparison — closer-to-target scores higher
- **WHEN** dataset A has an event 1 month off and dataset B has an event 2 months off
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — event on last day of January (day 30)
- **WHEN** an event has `MONTH=1` and `DATE=30`
- **THEN** `get_month_from_day_of_year(30)` returns `1` and the event contributes 0 violations

#### Scenario: Edge case — event on first day of February (day 31)
- **WHEN** an event has `MONTH=1` but `DATE=31`
- **THEN** `get_month_from_day_of_year(31)` returns `2` and the event contributes 1 violation

---

### Requirement: SameDayEvaluator tests
Tests SHALL verify `SameDayEvaluator` penalizes non-INFO events sharing a date. Setup via `SamplingDataHolder` using type `'INFO'`.

#### Scenario: Perfect score — all non-INFO events on unique dates
- **WHEN** no two non-INFO events share the same DATE value
- **THEN** `evaluate()` returns `1.0`

#### Scenario: INFO events sharing a date are not penalized
- **WHEN** two INFO events share the same DATE but no non-INFO events do
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one date clash
- **WHEN** exactly two non-INFO events share one date
- **THEN** `evaluate()` returns `pytest.approx(0.3 ** 1)`

#### Scenario: Exact formula — two date clashes on different days
- **WHEN** two separate dates each have two non-INFO events
- **THEN** `evaluate()` returns `pytest.approx(0.3 ** 2)`

#### Scenario: Comparison — fewer clashes scores higher
- **WHEN** dataset A has 0 clashes and dataset B has 1 clash
- **THEN** `evaluate(A) > evaluate(B)`

---

### Requirement: TypeSpreadEvaluator tests
Tests SHALL verify `TypeSpreadEvaluator` rewards even temporal spacing of event types within each group. Setup via `SamplingDataHolder`; type must not be in `excluded_types`.

#### Scenario: Perfect score — single event per type-group combination
- **WHEN** a type appears only once in a group (fewer than 2 events → early return of 1)
- **THEN** `evaluate()` returns `1.0` for that type-group pair

#### Scenario: Comparison — evenly spaced scores higher than clustered
- **WHEN** dataset A has events of a type spread evenly across the year and dataset B has events of the same type clustered within 30 days
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Comparison — more events evenly spaced still beats clustering
- **WHEN** dataset A has 4 events of a type at roughly equal intervals and dataset B has 4 events of the same type bunched in adjacent days
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — excluded types do not affect score
- **WHEN** events of type `'ST'` (in `excluded_types`) are present
- **THEN** they are not factored into the spread score

---

### Requirement: WeekClumpingEvaluator tests
Tests SHALL verify `WeekClumpingEvaluator(2025)` penalizes weeks with many events. Week boundaries are Monday-aligned with offset 2 for 2025 (Jan 1 = Wednesday).

#### Scenario: Perfect score — at most 2 events per week
- **WHEN** every week contains at most 2 events
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one week with exactly 3 events
- **WHEN** exactly one calendar week contains 3 events and all others have ≤2
- **THEN** `evaluate()` returns `pytest.approx(0.99 ** 1)`

#### Scenario: Exact formula — one week with exactly 4 events
- **WHEN** exactly one calendar week contains 4 events and all others have ≤2
- **THEN** `evaluate()` returns `pytest.approx(0.99 ** 1 * 0.9 ** 1)`

#### Scenario: Comparison — spread across weeks beats clustering
- **WHEN** dataset A has 6 events spread one-per-week and dataset B has all 6 events in the same week
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — events in the last week of 2025 (days 360–364)
- **WHEN** 3 events are placed in the last week (days 360, 362, 364)
- **THEN** `evaluate()` returns a value < 1.0 without error

---

### Requirement: WeekDayEvaluator tests
Tests SHALL verify `WeekDayEvaluator(2025)` rewards even weekday distribution (Mon–Thu) for a type's group assignments. Setup via `SamplingDataHolder` using `add_type`.

#### Scenario: Perfect score — events evenly distributed Mon–Thu for one group
- **WHEN** a type's RB events fall exactly one each on Mon, Tue, Wed, Thu
- **THEN** `evaluate()` returns `pytest.approx(1.0)` (variance = 0)

#### Scenario: Comparison — balanced distribution beats all-on-one-day
- **WHEN** dataset A has 4 RB events spread Mon/Tue/Wed/Thu and dataset B has all 4 RB events on Monday
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — events only on weekends (Sat/Sun) are filtered out
- **WHEN** all events of a type fall on Saturday or Sunday (weekday ≥ 5)
- **THEN** those events are excluded from the Mon–Thu count and `evaluate()` returns `1.0`

#### Scenario: Edge case — year-boundary days have correct weekday mapping
- **WHEN** an event is placed at day 0 (Jan 1, 2025 = Wednesday, weekday 2) and day 364 (Dec 31, 2025 = Wednesday, weekday 2)
- **THEN** both are mapped to weekday 2 (Wednesday) without error

---

### Requirement: WeekendEvaluator tests
Tests SHALL verify `WeekendEvaluator(2025)` penalizes SAT events not on Saturdays and non-SAT events on weekends. Uses 0-indexed days: first Saturday = day 3, first Friday = day 2.

#### Scenario: Perfect score — SAT events on Saturdays, others on weekdays
- **WHEN** all SAT=1 events fall on a Saturday and all SAT=0 non-fixed events fall on Mon–Thu
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Exact formula — one non-SAT event on a Friday
- **WHEN** one non-fixed SAT=0 event falls on day 2 (Jan 3, 2025 = Friday)
- **THEN** `evaluate()` returns `pytest.approx(0.6 ** 1)`

#### Scenario: Exact formula — one SAT event not on a Saturday
- **WHEN** one non-fixed SAT=1 event falls on a weekday (not a Saturday)
- **THEN** `evaluate()` returns `pytest.approx(0.6 ** 1)`

#### Scenario: Fixed events are not penalized
- **WHEN** a fixed non-SAT event falls on a Friday
- **THEN** `evaluate()` returns `1.0`

#### Scenario: Comparison — compliant schedule beats violating schedule
- **WHEN** dataset A has all events on correct day types and dataset B has 3 violations
- **THEN** `evaluate(A) > evaluate(B)`

#### Scenario: Edge case — last Saturday of 2025 (day 361, Dec 27)
- **WHEN** a SAT=1 event is placed at day 361
- **THEN** it is recognized as a Saturday and incurs no penalty
