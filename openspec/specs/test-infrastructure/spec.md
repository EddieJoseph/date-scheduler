## ADDED Requirements

### Requirement: pytest.ini at project root
A `pytest.ini` file SHALL exist at the project root with `testpaths = tests` and `pythonpath = src` so that `python -m pytest` discovers tests without path manipulation.

#### Scenario: Tests discovered with default invocation
- **WHEN** the user runs `python -m pytest` from the project root
- **THEN** pytest finds and runs all tests under `tests/` without import errors

### Requirement: conftest.py with make_events fixture
`tests/conftest.py` SHALL define a `make_events(n, **kwargs)` pytest fixture that returns an `(N, 16)` int16 numpy array where column semantics match `SamplingRows`. Any column can be overridden by passing the lowercase enum name as a keyword argument.

#### Scenario: Default array construction
- **WHEN** `make_events(3)` is called
- **THEN** the result is shape `(3, 16)`, dtype `int16`, with `id` auto-incremented (0, 1, 2), `include=1`, `fixed=0`, `date=0`, `month=-1`, `type=0`, `order=-1`, and all flag columns `0`

#### Scenario: Column override
- **WHEN** `make_events(3, date=[10, 100, 200], fixed=[0, 0, 1])` is called
- **THEN** column `DATE` contains `[10, 100, 200]` and column `FIXED` contains `[0, 0, 1]`

### Requirement: conftest.py with make_scheduler_data fixture
`tests/conftest.py` SHALL define a `make_scheduler_data` pytest fixture that returns a callable. Calling it with optional row-count and column overrides SHALL produce a valid `SchedulerData` instance backed by an in-memory DataFrame — no file I/O.

#### Scenario: Default SchedulerData construction
- **WHEN** `make_scheduler_data(2)` is called
- **THEN** the result is a `SchedulerData` whose `dates` DataFrame has 2 rows and all 22 columns required by `SamplingDataHolder`

#### Scenario: No external files required
- **WHEN** any test using `make_scheduler_data` is run
- **THEN** no file-system reads occur (no Excel, no CSV)
