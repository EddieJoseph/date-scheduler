## Context

The project has 10 MCMC evaluators under `src/ej/scheduler/generation/evaluation/`. None have tests. The existing test infrastructure (`make_events`, `make_scheduler_data`, `SamplingDataHolder`) already covers the data layer — evaluator tests can build directly on top of it.

Evaluators fall into three tiers by constructor complexity:
- **Tier 1**: constructor takes only primitives (year or nothing); `evaluate()` callable immediately
- **Tier 2**: constructor is trivial but requires a setup method (`set_info_type`, `set_assi_types`, etc.) called with a `SamplingDataHolder` before `evaluate()` works
- **Tier 3**: constructor calls `pd.read_excel`, which fails without a real file

## Goals / Non-Goals

**Goals:**
- Test all 10 evaluators with absolute scores, formula verification, comparison ordering, and date-boundary edge cases
- Wire Tier 2 setup methods through a real `SamplingDataHolder` (not bypassed via attribute injection)
- No production code changes

**Non-Goals:**
- Testing interaction between evaluators (composition is tested by the optimizer)
- Performance or timeout testing
- Integration tests against real holiday Excel files

## Decisions

### 1. Tier 2: Wire through SamplingDataHolder, not attribute injection

Setting `evaluator.info_type = 0` bypasses the `map_types` call entirely and tests nothing about the wiring. Using a real `SamplingDataHolder` (via the new `make_sdh` fixture) tests that the setup methods correctly translate string type names to integer IDs, which is the actual failure mode if types are renamed or reordered.

**Alternative**: direct attribute injection is simpler but tests less and can silently diverge from production wiring.

### 2. Tier 3: Mock `pd.read_excel`, set `blocked_dates` directly

`HolidayEvaluator` and `JfHolidayEvaluator` read Excel files in their constructors. The constructor logic (filtering by year, flattening date ranges) is a separate concern from `evaluate()`. Tests focus on `evaluate()` behavior given a known `blocked_dates` list — achieved by patching `pd.read_excel` to return an empty DataFrame, then setting `self.blocked_dates` manually.

**Alternative A**: Create a real temp Excel file via openpyxl — adds a dependency on the file format and tests the constructor path, but that path is simpler and already covered by the existing holiday file fixture in production.

**Alternative B**: Refactor constructor to accept pre-built `blocked_dates` — cleaner long-term but is a production code change, out of scope.

### 3. One test file per evaluator

10 test files under `tests/generation/evaluation/`. Keeps each file focused, makes failures easy to locate, and mirrors the source layout under `src/ej/scheduler/generation/evaluation/`.

### 4. Use year 2025 throughout

All year-dependent evaluators (`AsCleanEvaluator`, `WeekClumpingEvaluator`, `WeekendEvaluator`, `WeekDayEvaluator`) use year 2025. This fixes the weekday offset (Jan 1, 2025 = Wednesday, offset = 2) and makes date calculations reproducible across the suite.

Key 2025 reference dates:
- Day 1 = Jan 1 (Wednesday)
- Day 3 = Jan 3 (Friday) — first Friday
- Day 4 = Jan 4 (Saturday) — first Saturday
- Day 31 = Jan 31 — last day of January
- Day 32 = Feb 1 — first day of February
- Day 365 = Dec 31 (Wednesday) — last day of year

### 5. `make_sdh` fixture in conftest.py

A small factory fixture `make_sdh` wraps `make_scheduler_data → SamplingDataHolder`. Tier 2 tests need this to call setup methods. Placed in the root `tests/conftest.py` so all test subdirectories can use it.

## Risks / Trade-offs

- [Year-hardcoded tests] → Tests break if ported to a leap year or the year constant changes. Mitigation: all year-sensitive tests document which 2025 day-of-year values they use and why.
- [TYPE integer IDs are order-dependent] → `SamplingDataHolder.map_types` assigns IDs in the order types are first encountered. Tests that set up `make_scheduler_data` with specific type strings must ensure the setup call matches what `evaluate()` sees. Mitigation: always call the evaluator's setup method after constructing `SamplingDataHolder`, never pre-compute IDs manually.
- [Mock bypasses constructor parse logic] → Holiday constructor filtering (year range, multi-day spans) is untested. Acceptable: that logic is straightforward date arithmetic and would be tested separately if a holiday-constructor spec is added later.
