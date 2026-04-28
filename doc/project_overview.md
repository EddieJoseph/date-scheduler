# Project Overview

This is a two-phase CLI tool that optimizes annual event schedules for **Milizfeuerwehr Basel-Stadt** (Swiss militia fire department).

**Domain:** ~80 firestation training/exercise events per year must be distributed across the calendar subject to many constraints (holidays, weekends, group balance, type spread, etc.).

**Workflow:**
1. **Phase 1 — Optimize** (`python -m ej.scheduler.cli_interface optimize`): Takes an Excel file of events with metadata and runs MCMC to find an optimal date assignment. Outputs an optimized Excel file.
2. **Phase 2 — Generate** (`python -m ej.scheduler.cli_interface generate`): Takes the optimized Excel and produces per-group reports in three formats: PDF programs, PDF calendars, and ICS calendar files. Also produces a versioned change-tracking PDF.

**Four organizational groups** (events are tagged for one or more):
- **JF** — Jugendfeuerwehr (Youth Fire Department), TYPE == 'J'
- **RB** — Riehen-Bettingen
- **KB** — Kleinbasel
- **GB** — Grossbasel

Shared event types (ST, MS, ASIKVK, ASSITST, ASIKONT, KS, B, IFA) appear in all group reports regardless of group flags.
