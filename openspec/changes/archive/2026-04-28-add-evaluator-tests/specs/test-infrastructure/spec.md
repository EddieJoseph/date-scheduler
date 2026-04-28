## ADDED Requirements

### Requirement: conftest.py with make_sdh fixture
`tests/conftest.py` SHALL define a `make_sdh` pytest fixture that returns a callable. Calling it with optional keyword arguments SHALL produce a `SamplingDataHolder` instance backed by an in-memory `SchedulerData` — no file I/O.

#### Scenario: Default SamplingDataHolder construction
- **WHEN** `make_sdh()` is called with no arguments
- **THEN** the result is a `SamplingDataHolder` whose internal numpy array has shape `(N, 16)` and all type mappings are initialized

#### Scenario: Column overrides propagate through SamplingDataHolder
- **WHEN** `make_sdh(n=3, type=["ASI", "ASI", "INFO"])` is called
- **THEN** the resulting `SamplingDataHolder` can resolve those type names via `map_types(["ASI"])` without error

#### Scenario: No external files required
- **WHEN** any test using `make_sdh` is run
- **THEN** no file-system reads occur
