# Hidden Champions (HCP)

Tooling and research for the **Hidden Champions** program: identifying and
profiling India's "hidden champion" manufacturers — pre-qualified, often
under-the-radar companies with a real competitive moat — and turning that
research into structured, verifiable company profiles.

The work happens in two stages:

1. **Characterize** a company against a four-pillar "wealth-creation engine"
   model — differentiation, moat, product-improvement capability, and
   market alignment, plus any execution gap — using an automated Google
   Sheets + Apps Script pipeline (`apps_script/`).
2. **Profile** the characterized company into a polished, narrative
   JSON+HTML profile for publishing (`profile_generation/`,
   `target_companies/`, `temp_profile_creator/`), following a strict
   no-fabrication / human-verification discipline: every claim is tagged
   with its source and credibility tier, and nothing is marked "verified"
   until a human has actually checked it.

The underlying engine model and JSON schema are documented in
`context/data-infra-spec.md` and `context/hc-profiling/`.

## Folders

### `apps_script/`
The Google Apps Script project bound to the "Hidden Champions HVT" Google
Sheet. Given a company name + website, it:
- runs Serper-powered web searches and scrapes evidence for each pillar
  (`Serper.js`),
- resolves company identity — CIN, ownership type, sector (`Identity.js`),
- structures the evidence into the four pillars via Gemini, with closed
  vocabularies and source-fidelity checks enforced in code
  (`Gemini.js`, `Config.js`, `Vocabularies.js`),
- writes a short per-company narrative summary once characterization is
  done (`runCompanySummary`, menu item 5 — lives in `Gemini.js`),
- batches this across many companies with checkpointing, retries, and a
  circuit breaker for API failures (`Batch.js`, `BatchFailures.js`,
  `CircuitBreaker.js`, `RateLimiter.js`),
- tracks cost and progress (`TokenLog.js`, `CostSummary.js`,
  `PipelineSummary.js`, `EventLog.js`, `Triage.js`),
- regression-tests the pipeline's own output against a frozen, known-correct
  evidence snapshot for a fixed set of companies (`Calibration.js`),
- exports finished HVT rows as a JSON file (or Drive file) in the CRM's
  import format, for an operator to manually upload — this never talks to
  the CRM directly, no URL or token, and never writes back to the sheet
  (`Export.js`).

**How to use it:** open the bound Sheet, type a company's `company_name`
and `website` into a row, then run the menu items under **Hidden
Champions** in order (1. Run Serper Grounding → 2. Resolve Identity → 3.
Run Sector-Context Grounding → 4. Run Gemini Structure → 5. Run Company
Summary), or use the batch menu items to process many rows at once. Later
menu sections cover review/reporting (Build Review Queue, Pipeline/Cost
Summary, Batch Failures), calibration, cache maintenance, and the CRM
export tools described above. Local source is managed with
[`clasp`](https://github.com/google/clasp) — after editing a file here,
push it live with `clasp push` from this folder. Script Properties
`SERPER_API_KEY` and `GEMINI_API_KEY` must be set on the bound script
first (not stored in this repo).

A separate variant of this pipeline, adding an independent automated
validation pass on top of everything above, lives outside this repo — see
[Hidden Champions with Validation](https://github.com/amruthavedantham-dt/hcp-with-validation).

### `context/`
Reference material and specs that the rest of the project builds on —
not code, no need to run anything here:
- `data-infra-spec.md` — the four-pillar engine model itself.
- `HVT_Claude_Code_Context.md` — the original build spec for `apps_script/`.
- `hc-profiling/` — the company-profile JSON schema (`profile-fe-contract.md`),
  generation rules (`generation-spec.md`), a worked example
  (`example-eldorado-agritech.json`), and the upload/rollout plan.
- `eldorado.html`, `pioneer.html` — worked example profile pages used as the
  visual template for generated profiles.
- `profile-generation-workflow.md`, `fde-datafetch-plan.md` — supporting
  planning docs.

### `profile_generation/`
A temporary, interactive Claude Code workflow for turning an
**already-characterized HVT sheet row** into a full narrative company
profile. No scripts to run — paste a company's HVT row (plus any
financials you have) into a Claude Code session in this folder, ask it to
generate the profile per `RECIPE.md`, and it produces
`companies/<slug>.json` (the profile) and `companies/<slug>.html` (a
readable preview). See `profile_generation/README.md` for the full flow.

### `target_companies/`
Finalized profiles for companies sourced from the HVT Google Sheet
(pillar research already run and reviewed via `apps_script/`) — the
"production" profile set, kept separate from earlier hand-researched test
entries in `temp_profile_creator/`.
- `companies/<slug>.json` + `.html` — the finished profile and its preview.
- `segments/<segment_ref>.json` — shared market/segment data reused across
  companies in the same segment.
- `sources/<slug>.md` — per-company source notes, mainly for financial
  figures not already in the sheet.
- `progress.csv` — tracks which of the ~100 sheet rows have been turned
  into profiles (`pending` / `done` / `deferred`) — check this before
  resuming a batch.
- `METHODOLOGY.md` — the full runbook for processing companies at batch
  scale (pre-screening rules, field mapping, decision tables).
- `gen_html.py` — regenerates a company's `.html` preview from its `.json`:
  `python3 gen_html.py <company>.json <company>.html`.
- `hcp-import-ready/` — CRM-import-format JSON files produced by
  `apps_script/Export.js`'s CRM export tools, waiting to be manually
  uploaded through the CRM's own import screen.

### `temp_profile_creator/`
The same profile-generation process as above, but for companies **without**
an HVT sheet row yet (e.g. Serper credits exhausted, or a company found
outside the sheet pipeline) — Claude does the pillar research itself via
web search instead of reading it from the sheet. Two-phase process:
Phase 1 drafts claims + sources into `sources/<slug>.md` for you to verify;
Phase 2, only after your sign-off, finalizes `companies/<slug>.json` +
`.html` with `meta.verified: true`. See `temp_profile_creator/README.md`
and `RECIPE.md` for the full discipline.

## Typical flow for a new company

1. Add the company to the HVT Google Sheet and run it through
   `apps_script/` (or, if the sheet isn't an option yet, start directly in
   `temp_profile_creator/`).
2. Once pillar data is reviewed, generate its profile in
   `profile_generation/` or `target_companies/` (sheet-sourced) —
   or finish it in `temp_profile_creator/` (non-sheet-sourced).
3. Verify every claim against its cited source before setting
   `meta.verified: true`.
4. Upload the finished `companies/<slug>.json` via the CRM's **Hidden
   Champions → New profile** form.
