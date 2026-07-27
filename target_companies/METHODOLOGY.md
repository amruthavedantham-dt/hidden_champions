# Methodology — HVT sheet → contract-v3 profile, at scale

Runbook for turning `hcp_hv_100_companies_export.csv` rows into
`companies/<slug>.json` + `.html` profiles. Written from how the first two
batches (30 companies) were actually done, so a future session — or a
script — can repeat it without re-deriving the process. Full schema rules
live in `../context/hc-profiling/generation-spec.md` and
`profile-fe-contract.md`; `../profile_generation/RECIPE.md` is the
condensed per-company version. This file is the **batch-scale operational
layer** on top of those — grouping, agent prompts, classification rules,
tracking.

## 0. Track progress in `progress.csv`

One row per CSV company: `row, company_name, segment_ref, status, slug,
note`. `status` is `pending | done | deferred`. **Always check this file
first** before starting a new batch — it's the single source of truth for
what's left, what's done, and why anything was skipped. Update it as each
company completes (or gets deferred) in the current batch, not just at the
end.

## 1. Pick the next batch (~15 rows) and pre-screen for usability

Read the next N `pending` rows from the CSV. Before committing to the
batch, check each row for two failure modes seen already:
- **Missing identity** (blank `sector`/`segment_ref`/`cin`) — the Identity
  step never ran on this row. Pillar data may still be rich (Litmus
  Organics was) — don't discard, just defer with a note, since inventing
  a `segment_ref` isn't allowed (it's the user's own taxonomy).
- **Empty pillar data** (`differentiation`/`moat`/`product_improvement`/
  `align*`/`gap*` all blank, only identity present) — Mitra Industries was
  this case. There's nothing to build `corneredResource` from; defer it.

Mark both `deferred` in `progress.csv` with a one-line reason, and pull in
the next `pending` row to keep the batch at the target size. Never
silently drop a row — every row ends up `done` or `deferred`, never just
missing.

## 2. Group the batch by segment_ref for parallel research

Companies sharing a `segment_ref` (e.g. multiple companies tagged
`pharmaceutical-formulations`) only need that segment researched **once**
— check `segments/<segment_ref>.json` for an existing file before
assigning it to a new research group. Split the batch into ~5 groups of
~3 companies each, grouped to keep same-segment companies together when
possible (reduces duplicate research, though it's not always avoidable
since sector diversity across a random batch is normal).

## 3. Dispatch parallel research agents (one per group)

Use the `Agent` tool, `subagent_type: general-purpose`,
`run_in_background: true`, one call per group, all in a single message so
they run concurrently. Each agent gets a **self-contained prompt** with:
- The group's companies: name, CIN (if known), website, sector,
  `segment_ref`.
- **Part 1 — company financials** (per company, ~3 searches): revenue
  (1-2 FY), PAT/EBITDA margin, ROE, founded year, employee count,
  ownership/CIN confirmation, patents/certifications/R&D headcount,
  export footprint, recent moves (last ~2 years). Source hierarchy: DRHP
  > Screener.in > Tofler/Tracxn > MCA/ROC > press > company site
  (self-claimed, mark it). Explicit `NOT FOUND` for anything missing —
  never estimate.
- **Part 2 — segment research** (once per unique `segment_ref` in the
  group, skip if the file already exists): world market size + CAGR
  (global by default), export geographies, global competitors, India
  domestic slice, 2-4 named peers with revenue/margin/ROE/growth,
  structural demand facts, customer buying drivers, generic H5→H1 value
  chain steps for the segment.
- Explicit instruction: **research only, no file writes**, return a
  structured markdown report (one `# Company:` block per company, one
  `# Segment:` block per unique segment), cite every fact inline.

Agents run in the background — do not poll; each returns a
`task-notification` when done. Process results as they land rather than
waiting for all five (this session assembled Group D's profiles while
Groups A/B/C/E were still running).

## 4. Build segment files first (`segments/<segment_ref>.json`)

Shape per `generation-spec.md` §B — `segmentName`, `market` (world range +
CAGR + export geographies + competitors + domestic slice as a sub-note),
`subSegments[]`, `adjacentMarkets[]`, `structureFacts[]`,
`adoptionStructure`, `peers[]`, `customerValue`, `valueChain[]` (the H5→H1
generic scaffold, reused by every company sharing the segment),
`sources[]`. Write `"peers": []` or an explanatory `note` field rather
than forcing a bad-fit peer match when no clean comparable exists (seen
repeatedly — niche segments like blasting-peening-systems or
transmission-synchro-rings have no clean public peer set).

## 5. Assemble each company profile

`researchDepth: "directory"` for every company in this pipeline (no A2/
pursuit intel is being collected) — this has one big scope-reducing
consequence: **`p5_workflows` is always the segment's generic scaffold**
(`stepsTier: "segment"`, `flags.generic: true` on every horizontal).
Don't invent company-specific steps. Instead, overlay real HVT-row/
research facts onto the generic steps via the `spotted` node on whichever
horizontal they land on — this is what makes a "generic" workflow still
feel company-specific without fabricating process detail.

Map HVT columns → contract-v3 fields:
- `differentiation`/`moat*`/`product_improvement*` → `p1_engine` blocks,
  carrying the sheet's own `*_credibility`/`*_needs_verify` through
  untouched (never re-judge them).
- `align1-3_*` → context for `p2_market` insights (the market pull each
  capability points at).
- `gap_*` → almost always becomes `p3_opportunities` item 1 (the rule
  table in generation-spec.md §D rarely fires cleanly on non-seed
  companies — the HVT row's own gap research is usually the more reliable
  opportunity source at directory depth; tag `source: "HVT gap research"`).
- `proof_*` → certifications/qualifications context in `p1_engine`.
- `unresolved_pillars`/`triage_status` → **always check these against
  what you're about to write**, and note in `sources.md` if the sheet
  flagged a pillar the HVT tool itself wasn't confident in, even if
  `_review` says `Verified`. This has been the single most common
  cross-check catch across both batches so far.

### healthClass — pick one honestly, don't force "engine"

| Signal pattern seen in this project so far | healthClass |
|---|---|
| Revenue + PAT + ROE all healthy and rising together | `engine` (Fredun, Supriya, Unisem) |
| Financials soft/volatile but a real, funded platform/tech bet in motion | `forward-bet` (Spray Engineering Devices — literally generation-spec.md's own reference case; Tatva Chintan; Mantra Softech) |
| Financials thin/unclear/unavailable, but a real certified or differentiated capability + a market moving toward it | `capability-led` (Garware, Infinita Biotech, Natesan, Sandstorm, Gracure, Jaishil, Spaco, Metlok) |
| Real stored assets/brand, financials lagging | `turnaround` (none yet in this project — watch for it) |

No `screen-out` — every row already passed the data-infra qualification
gate upstream. A thin or unreliable financial figure is narrative context,
never a reason to downgrade or skip a company.

### Data-quality patterns to actively watch for (confirmed recurring)

- **Aggregator extraction artifacts**: Tracxn/Tofler free-tier pulls have
  produced obviously-wrong figures more than once (a "₹9,112 Cr PAT" on a
  ₹364 Cr-revenue company). Sanity-check any aggregator figure against the
  company's own revenue scale before using it; disregard and note if
  implausible rather than silently using it.
- **Self-claimed scale vs. independently-checkable trade data**: two
  companies so far (Sandstorm, Infinita Biotech) claimed export reach that
  didn't match Volza/ExportGenius shipment records. Flag the gap
  explicitly in the profile — don't average or silently pick one number.
- **Corporate-identity collisions**: similarly-named entities (Metlok
  Bengaluru vs. Nagpur) can get conflated by a single source describing
  facts that may belong to a different legal entity. If the CIN and the
  described facility/city don't obviously match, flag it as unresolved
  rather than picking one.

## 6. Generate the HTML preview

`gen_html.py` (in this folder) renders `companies/<slug>.json` into
`companies/<slug>.html` using the exact CSS/layout established in
`eldorado.html`/`pioneer.html`. Run: `python3 gen_html.py
companies/<slug>.json companies/<slug>.html`. Stdlib-only, no
dependencies. If the JSON schema ever changes shape, update this script's
`render()` function to match — it's a straight structural mapping, not a
templating engine, so it will silently produce a broken section if a
JSON field it expects is renamed or restructured.

## 7. Write `sources/<slug>.md`

Not a restatement of the JSON — a provenance log. Cover: which pillar
claims came from the HVT sheet (with its own credibility/needs_verify
tags) vs. what was freshly researched this session; every financial
figure's source; anything flagged as a data-quality issue (per §5 above);
what's genuinely `needsInput`/not found. This is what the user actually
checks before flipping `meta.verified`.

## 8. Batch-level wrap-up

Update `progress.csv` for every row touched (done or deferred). Report to
the user: what's done, what was substituted/deferred and why, and any
cross-company issues worth their attention before the next batch (e.g. an
identity collision, a systematically unreliable data source).

## Toward automation

Everything in §3-§7 is mechanical enough to script once the research step
is either (a) accepted as an LLM-agent call rather than a deterministic
API call, or (b) replaced with a real API-backed research pipeline (DRHP/
Screener/Tofler APIs instead of ad hoc web search). The parts that
currently need a human-in-the-loop judgment call, not just automation:
- Pre-screening a row as usable vs. deferred (§1) — a simple emptiness
  check would work; the "is this pillar data too thin to build from"
  judgment currently isn't fully mechanical.
- `healthClass` classification (§5) — the trigger table above is a
  reasonable first-pass rule set, but "financials lagging vs. genuinely
  volatile vs. genuinely unavailable" still took real judgment on messy
  aggregator data in both batches so far.
- Flagging data-quality issues (§5) — currently relies on noticing an
  implausible number or a claim/trade-data mismatch; a script would need
  explicit sanity-check rules (e.g. PAT > revenue → flag) to catch even
  the confirmed patterns above, and would still miss novel ones.
