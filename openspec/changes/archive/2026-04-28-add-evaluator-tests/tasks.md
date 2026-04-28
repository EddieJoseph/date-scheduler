## 1. Test Infrastructure

- [x] 1.1 Add `make_sdh` fixture to `tests/conftest.py` — wraps `make_scheduler_data` → `SamplingDataHolder`
- [x] 1.2 Create `tests/generation/evaluation/__init__.py`

## 2. Tier 1 Evaluator Tests (pure, no setup, no files)

- [x] 2.1 Create `tests/generation/evaluation/test_as_clean_evaluator.py` — perfect score, one violation (formula), comparison, year-end edge case
- [x] 2.2 Create `tests/generation/evaluation/test_month_evaluator.py` — perfect score, one violation, comparison, Jan 31 / Feb 1 boundary
- [x] 2.3 Create `tests/generation/evaluation/test_week_clumping_evaluator.py` — perfect score, 3-per-week, 4-per-week, comparison, last-week-of-2025 edge case
- [x] 2.4 Create `tests/generation/evaluation/test_weekend_evaluator.py` — perfect score, non-SAT on Friday, SAT not on Saturday, fixed-event exemption, comparison, day 361 edge case

## 3. Tier 2 Evaluator Tests (setup via SamplingDataHolder)

- [x] 3.1 Create `tests/generation/evaluation/test_assi_evaluator.py` — `set_assi_types` via `make_sdh`, perfect order, one violation, two violations, ORDER=-1 exclusion, comparison
- [x] 3.2 Create `tests/generation/evaluation/test_same_day_evaluator.py` — `set_info_type` via `make_sdh`, perfect score, INFO events exempt, one clash, two clashes, comparison
- [x] 3.3 Create `tests/generation/evaluation/test_type_spread_evaluator.py` — `set_types` via `make_sdh`, single event (returns 1.0), evenly-spaced vs clustered comparison, excluded-type check
- [x] 3.4 Create `tests/generation/evaluation/test_week_day_evaluator.py` — `add_type` via `make_sdh`, even distribution (score 1.0), balanced vs all-on-Monday comparison, weekend-day filtering, year-boundary weekday mapping

## 4. Tier 3 Evaluator Tests (mock pd.read_excel)

- [x] 4.1 Create `tests/generation/evaluation/test_holiday_evaluator.py` — patch `pd.read_excel`, set `blocked_dates` directly; perfect score, one hit, fixed exemption, comparison, day 0 / day 364 edge cases
- [x] 4.2 Create `tests/generation/evaluation/test_jf_holiday_evaluator.py` — same mock approach plus set `jf_type`; non-JF events exempt, one JF hit, comparison

## 5. Verification

- [x] 5.1 Run `python -m pytest tests/generation/evaluation/` — all tests pass with no errors
