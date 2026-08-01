# Profiler anatomy — what to keep, what to fork

The reference implementation is the Google Apps Script profiler in `profiler/` (bound to the HVT spreadsheet). It splits cleanly into a **reusable harness** (topic-blind plumbing) and a **topic brain** (research ontology — fork per topic). A new profiler = copy the sheet + script project, carry the harness, replace the brain, keep the export speaking the import contract.

The harness is not sacred code. A fork may restyle its look and feel (menus, dialogs, sheet formatting, naming) and optimize its internals freely. What a fork may **never drop** are the guarantees below — every one exists because a 500-company batch on paid APIs punishes its absence.

## Harness guarantees (non-negotiable in any rewrite)

1. **Every external call is rate limited.** Spacing before each Serper/Gemini fetch, multiplicative backoff on 429/503 (current code: ×1.5 up to a per-API ceiling), slow decay on success (×0.95 down to a floor). If a rewrite introduces anything that could synchronize calls (parallel fetches, fixed retry sleeps), add jitter — the current limiter is a deliberately deterministic adaptive sleep, which is fine while calls are strictly sequential. The limiter state must be **persisted** (Script Properties), not module memory — each trigger fire is a fresh execution, and an in-memory sleep value would reset every tick so backoff never accumulates.
2. **Circuit breaker.** Consecutive-failure halt with timed auto-resume, plus a dead-key/out-of-credits detector that hard-pauses the batch (manual resume only) so a bad key cannot loop-burn credits.
3. **Checkpoint/resume.** State checkpointed to Script Properties around the 6-minute Apps Script execution limit; self-rescheduling one-shot triggers; a run resumes from its checkpoint. (Known edge in the current code: if BOTH APIs' breakers halt in the same tick, the batch parks with no continuation trigger and waits for a manual Resume after cooldown — position is preserved, resumption is not automatic.)
4. **Per-unit failure containment.** One (company, step) failure is recorded and skipped, with a retry-failed flow; a bad row never sinks the batch.
5. **Durable search cache.** `SEARCH_CACHE` with no TTL. It deduplicates API spend *and* is the corpus the export's `evidence` is drawn from — dropping it starves the CRM's generated profiles.
6. **Cost ledger.** Per-call token/cost logging with projections; a long batch must never run blind.
7. **The CRM contract.** Restyle anything, but the input to and output from the CRM keep the exact [crm-import-contract.md](crm-import-contract.md) shape — the envelope is the wall between the two worlds.

## The harness (current implementation)

| File | What it does |
|---|---|
| `Batch.gs` / `BatchFailers.gs` | Menu-driven batch runs over the sheet; (company, step) units consumed one at a time inside a ~5-minute budget per trigger fire, checkpointed after every unit; self-rescheduling triggers between fires; per-unit failure containment; retry-failed flow (its failure buffer is fed from `EventLog.error` — see the caution below). |
| `RateLimiter.gs` | Adaptive per-API sleep (×1.5 backoff / ×0.95 decay), persisted across trigger fires. |
| `CircuitBreaker.gs` | Consecutive-failure halts with timed auto-resume, plus a dead-key/out-of-credits detector that hard-pauses the batch (manual resume only). |
| `TokenLog.gs` / `CostSummary.gs` / `PipelineSummary.gs` / `EventLog.gs` | Per-call cost ledger, cost projections, run summaries, event trail. |
| `SheetIO.gs` / `SheetSetup.gs` | Row find-or-create by company name, column-name-based reads/writes (schema migrations by column name), review-status dropdowns. |
| `Serper.gs` (mechanics) | The fetch pipeline: cache-check → breaker-check → rate-limit → call → log → scrape #1 result → cache-write. The durable `SEARCH_CACHE` sheet (no TTL) is what later feeds the export's `evidence`. The *loop* is generic; only the query tables are topic data. |
| `Export.gs` (mechanics) | Row → import-envelope serialization, evidence attachment from the cache (25 × ~400 chars, deduped, URL-filtered), Drive/download dialogs, 200-per-file split, run-id minting. **No network to the CRM, no config**: the operator downloads the file and uploads it in the CRM screen. |

> **Repo snapshot caution:** `EventLog.gs` in this repo copy is **empty**, yet most harness files call `EventLog.*` (Batch, BatchFailers, Serper, Gemini, Identity, CircuitBreaker, Vocabularies). The working definition lives in the bound Apps Script project. Fork from the live project, or restore `EventLog.gs` first — without it the batch throws at its first `EventLog` call, and the retry-failed buffer (populated from `EventLog.error`) never fills.

## The brain (fork per topic)

| File | What changes |
|---|---|
| `Config.gs` | **The topic ontology.** `HVT_HEADERS` (the sheet's ~50 columns: identity block + per-pillar claim/source/credibility/needsVerify/review columns + any structured extras) and `SERPER_QUERIES_BY_PILLAR` (the search battery: a map of pillar → quoted-name query templates, plus site-restricted and sector variants). Rename the pillars to the new topic's taxonomy; the pillar names flow into the export as free strings. |
| `Gemini.gs` | The extraction prompt (temperature 0, JSON response, closed vocabularies) and the deterministic sanitization passes (enum enforcement, self-published-domain downgrades, trigger-keyword `needsVerify` backstops, source-upgrade word-overlap gates, fabrication clearing). All of it is written against the topic's pillars and vocabularies — rewrite against the new ontology, keep the *pattern* (extract-only, validate in code, never trust the model). Keep `thinkingBudget: 0` in the generation config. |
| `Vocabularies.gs` | The quality lists: official-registry domain allowlist, self-published denylist, trigger keywords that force `needsVerify`. Re-derive for the topic (a compliance topic cares about cert registries; a talent topic about job boards). |
| `Identity.gs` | Statutory identity resolution (CIN regex, ownership enums). Mostly reusable for Indian companies; adjust per market. |
| `Calibration.gs` | The regression harness: a frozen evidence snapshot for a handful of known companies with expected outputs. Rebuild the set for the new topic — this is what keeps a fork honest over time. |
| `Export.gs` (mapping) | `serializeCompanyRow_` maps HVT columns → the contract's company object. Update the column names and the `CRM_EXPORT_PILLARS` list; keep everything else (URL filtering, conservative credibility defaults, review-value mapping, omission of empty fields — the CRM's strict validation depends on these). |

## Settings inventory

**Script Properties (research side):**
- `SERPER_API_KEY`, `GEMINI_API_KEY`, `GEMINI_MODEL` — the research engines.
- `CRM_EXPORT_SEQ` — auto-managed export run counter. Nothing else: the export needs **no CRM URL, no token, no offering** (offering is chosen in the CRM upload screen).

**Constants worth knowing (in `Export.gs`):** 200 companies/file, 25 evidence/company at ~400 chars each, review-enum mapping (`Needs registry check` → `Pending`), claim/evidence `source` emitted only when it matches `^https?://\S+$`.

**CRM side settings (once per org, not per profiler):** Spotlights AI Config holds the generation provider/model/key (encrypted) and the Serper key for the CRM's own intel refreshes. The generation model is chosen there — thinking-class models are handled (thinking budget pinned to zero on writing calls), and per-version token usage is stamped for the cost popup.

## The five-step recipe for a new topic

1. Copy the spreadsheet + Apps Script project.
2. In `Config.gs`: write the new pillar taxonomy, HVT columns, and query battery.
3. Rewrite `Gemini.gs`'s prompt + sanitization and `Vocabularies.gs`'s lists against that taxonomy; rebuild `Calibration.gs`'s expected set.
4. Update `Export.gs`'s column mapping and pillar list. Do not touch its envelope shape.
5. Run the batch, review the sheet, export, upload in the CRM, import — then build the topic's lens (see [crm-generation-pipeline.md](crm-generation-pipeline.md)).
