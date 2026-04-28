## 1. State Persistence in schedule.py

- [x] 1.1 Add `save_state(prefix, last_stage, last_phase)` helper that writes `{prefix}_state.json`
- [x] 1.2 Add `load_state(prefix)` helper that reads the state file and returns `(last_stage, last_phase)` or `None` if absent or unreadable
- [x] 1.3 Call `save_state()` immediately after each `save_to()` call in `optimize()`, passing the correct phase number (1–5)
- [x] 1.4 Add `resume: bool = False` parameter to `optimize()`
- [x] 1.5 Implement resume entry-point in `optimize()`: call `load_state()`, verify the referenced xlsx exists, load it via `SchedulerData.create_from()`, set `i` and skip the appropriate phases; fall back to normal flow if state is absent or xlsx is missing

## 2. CLI Changes in cli_interface.py

- [x] 2.1 Add `--resume` flag (store_true) to the `optimize` subparser with help text noting that `-i` is ignored when a checkpoint is found
- [x] 2.2 Pass `resume=args.resume` to the `optimize()` call
- [x] 2.3 Add `clear` subparser with `-o/--output` argument (same semantics as optimize)
- [x] 2.4 Implement `clear` dispatch: glob `{prefix}*.xlsx`, delete matches, delete `{prefix}_state.json` if present

## 3. Verification

- [ ] 3.1 Manual test: run optimize, interrupt after stage 2, re-run with `--resume`, confirm it resumes from stage 2 data
- [x] 3.2 Manual test: run `--resume` on an empty output folder, confirm it behaves like a fresh run
- [x] 3.3 Manual test: run `clear -o <prefix>`, confirm all xlsx and state files are removed
- [x] 3.4 Manual test: run `clear -o <prefix>` on an empty folder, confirm no error
