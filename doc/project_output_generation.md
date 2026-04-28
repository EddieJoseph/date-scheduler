# Project Output Generation

## Entry Point

`generate_output.generate_reports(version, old_versions, input_file_prefix, holiday_file_path, additional_days_file_path, year, output_path)`

Generates outputs for the complete schedule + 4 group-specific variants (JF, RB, KB, GB).

## Output Files Per Run

| File | Format | Description |
|---|---|---|
| `Jahresprogramm_komplett_v.xlsx` | Excel | All events, styled table |
| `Jahreskalender_komplett_v.pdf` | PDF | Visual week-grid calendar |
| `Jahresprogramm_komplett_v.ics` | ICS | All events as calendar entries |
| `Jahresprogramm_{GROUP}_v.pdf` | PDF | Per-group program (longtable) |
| `Jahreskalender_{GROUP}_v.pdf` | PDF | Per-group visual calendar |
| `Jahresprogramm_{GROUP}_v.ics` | ICS | Per-group calendar entries |
| `Änderungen_Jahresprogramm_v.pdf` | PDF | Color-coded diff vs all old versions |

## Group Filtering (`util/file_generation_utils.py`)

- `filter_jf(dates)` → TYPE == 'J'
- `filter_rb/kb/gb(dates)` → rb/kb/gb == True **OR** type in {ST, MS, ASIKVK, ASSITST, ASIKONT, KS, B, IFA}
- Shared types appear in all three of RB/KB/GB regardless of group flags

## PDF Generation (LaTeX)

All PDFs use **string-replacement templates** in `src/ej/scheduler/reporting/pdf/templates/` (or `pdf/templates/`), compiled with `lualatex.exe`.

**Program PDF** (`programm_pdf_generation.py`):
- Template `Jahresprogramm_tmpl.tex` + `row_tmpl.tex`
- 8-column longtable: Nr, Datum, Zeit, Tag, Kurs, Aufgebot, Art/Thema, Verantwortlich
- Appends change table (`addition_tmpl.tex`) at end

**Calendar PDF** (`calendar_pdf_generation.py`):
- Template `cal_tmpl.tex` + `cal_row.tex` + `cal_subhead.tex`
- 7-column week grid (Mon–Sun), up to 3 events per day cell
- Highlights holidays and additional days (gray italic)

**Change PDF** (`change_table_generation.py`):
- Template `Anpassungen_Jahresprogramm_tmpl.tex`
- Compares current version against all old versions
- Color coding: `\color{OliveGreen}` new events, `\color{BrickRed}\sout{...}` deleted, mixed for changed fields
- Detects changes in: NAME, DATE, TIME, CALLED_UP, THEME, RESPONSIBLE

**LaTeX escaping:** `file_generation_utils.translate_umlauts()` escapes German umlauts and special chars (ä→`\"a`, &→`\&`, etc.)

## ICS Generation (`reporting/ics/ics_generation.py`)

- Uses `ics` library; timezone: Europe/Zurich
- All-day event if no TIME set
- Event name includes group tags: `"Übung [GB, KB]"`
- Description: Aufgebot, Responsible, Theme, Details, Version

## Event Enumeration (`reporting/new_enumerator.py`)

- `NewEnumerator` assigns numeric suffixes to duplicate event names
- Cross-group events (or SAN type) get `X_ALL` numbering
- Single-group events numbered per group: "Übung 1", "Übung 2"
