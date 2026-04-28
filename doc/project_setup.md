# Project Setup and Dependencies

## Runtime

- **Python 3.11** (venv in `venv/` at project root)
- **No `setup.py` / `pyproject.toml`** — modules run directly via `-m` flag
- Package namespace: `src/ej/scheduler/`

## Dependencies (`requirements.txt`)

```
numpy==1.26.4        # Numerical MCMC loop (int16 array operations)
pandas==2.2.2        # DataFrame I/O and intermediate representation
openpyxl==3.1.2      # Excel read/write
ics==0.7.3           # ICS calendar file generation
matplotlib==3.9.0    # Optimization score convergence plot
```

Install: `pip install -r requirements.txt`

## System Dependency

**`lualatex.exe` must be on PATH** for Phase 2 PDF generation. Without it, PDF reports fail silently or with a subprocess error.

## CLI Invocation

```bash
# Phase 1 — Optimize
python -m ej.scheduler.cli_interface optimize \
  -i <input_file> -y <year> -o <output_prefix> \
  -H <holidays_file> [--random-seed <seed>]

# Phase 2 — Generate reports
python -m ej.scheduler.cli_interface generate \
  -i <input_prefix> -H <holidays_file> \
  -a <additional_dates_file> -y <year> \
  -v <version> [-o <old_versions_csv>] -p <output_path>
```

## OpenSpec Integration

`.claude/` directory contains OpenSpec skill definitions and `opsx` command shortcuts, but `openspec/config.yaml` contains only `schema: spec-driven` — no custom domain context defined yet.
