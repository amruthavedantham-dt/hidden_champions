# Plan B — FDE Data-Fetch for 1,100 Companies (Serper + Gemini → CSV)

### Program: dt-ICP-publicprofile | 2026-06-30 (rev. 2) | dev-ready (FDE runbook)
### SSOT: `data-infra-spec.md` (the engine model + verification discipline). FDE delivers a CSV; engineering ingests CSV → `pdgms_hc_company.engine` (JSON) downstream.

---

## Objective
For each of the ~1,100 pre-qualified companies, deliver **one CSV row** capturing the wealth-creation-engine fields (below). The population is pre-qualified (1,100 of 12,000) — this is **characterization, not screening**. The FDE produces a **CSV** (company name + the data-field columns). Converting the CSV to the engine JSON and loading it into the database is a downstream engineering step (Plan A), **not** the FDE's job.

## The tool split (this is the anti-hallucination guarantee)
- **Serper = grounding.** Search (`/search`) for discovery + snippets; page fetch for the few decisive pages. Serper is the ONLY source of facts.
- **Gemini = structuring, NON-grounding.** It receives the Serper text and fills the CSV fields. It may use **only** the supplied text, must put a **source** in the source column for each claim, and must **flag (not invent)** anything unsupported. Gemini never "knows" a fact on its own.

## The CSV (one row per company)
Headers, in order. A starter file with two worked rows (Pioneer, O/E/N) is provided: `data/hidden-champions-fde-template.csv`.

| # | Column | Meaning |
|---|--------|---------|
| 1 | `company_name` | legal name |
| 2 | `cin` | Corporate Identity Number (resolve this first — kills name collisions) |
| 3 | `ownership_type` | listed / unlisted-public / private / government-PSU / group-holding |
| 4 | `sector` | broad sector |
| 5 | `segment_ref` | segment key (so the segment/market data is reused) |
| 6 | `differentiation` | what makes the offering non-commodity |
| 7 | `differentiation_source` | URL |
| 8 | `differentiation_credibility` | self-claimed / third-party / customer-attested / qualification-gated / registry-confirmed |
| 9 | `differentiation_needs_verify` | yes / no |
| 10 | `moat_type` | switching-cost / qualification-lock-in / IP / brand / integration / scale / network |
| 11 | `moat_durability` | compounding / stable / eroding |
| 12 | `moat` | the moat in a sentence |
| 13 | `moat_source` | URL |
| 14 | `moat_credibility` | (same scale as #8) |
| 15 | `moat_needs_verify` | yes / no |
| 16 | `product_improvement` | the R&D engine that keeps the product current (the key discriminator) |
| 17 | `product_improvement_source` | URL |
| 18 | `product_improvement_credibility` | (same scale) |
| 19 | `product_improvement_needs_verify` | yes / no |
| 20–22 | `align1_capability`, `align1_need`, `align1_pull` | capability → market need, pull = must-have/strong/nice-to-have |
| 23–25 | `align2_capability`, `align2_need`, `align2_pull` | second alignment (blank if none) |
| 26–28 | `align3_capability`, `align3_need`, `align3_pull` | third alignment (blank if none) |
| 29 | `alignment_source` | URL(s) for the market-need claims |
| 30 | `gap_latent` | what the capability could do |
| 31 | `gap_currently_monetized` | what it's capturing today |
| 32 | `gap_summary` | the execution gap in a sentence |
| 33 | `gap_activation_path` | how the gap could be closed |
| 34 | `proof_type` | DSIR / TEC / patent / none (the registry proof of the capability) |
| 35 | `proof_status` | confirmed / claimed-verify / blocked / not-found |
| 36 | `proof_source` | URL |
| 37 | `unresolved_pillars` | comma list of pillars with no usable evidence |
| 38 | `notes` | anything else (financial snapshot, collision warnings, etc.) |

Leave a cell **blank** rather than guess. `*_needs_verify = yes` for any self-claim. A `commodity`/no-moat finding goes in `notes` only after a positive sweep (see discipline).

## Methodology — factory (segment once, company per-company)
Group the 1,100 by segment first. Fetch each **segment tier once** (market size, demandTailwind), reuse it across every company in that segment (it informs the `align*` and `notes` columns); then run companies.

### Per-company workflow
1. **Identity / CIN** (Serper ~1–2): resolve canonical CIN (e.g. O/E/N vs the listed OENCONNECT). Fill cols 1–5.
2. **Pillar grounding** (Serper ~3–4): differentiation, moat, product-improvement.
3. **Registry / proof step** (Serper ~1–2): DSIR / TEC / patents → cols 34–36. If blocked/none → `proof_status` + `*_needs_verify=yes` / `unresolved_pillars` (NEVER down-label to commodity).
4. **Reuse segment tier** (0 calls if already fetched).
5. **Gemini fill** (1 call): all retrieved text → the CSV row values for one company.
6. **Append the row** to the working CSV for the QA gate.

### Segment tier (once per segment, ~5–6 Serper calls, reused)
`<segment> global market size CAGR`, `<segment> demand trend / China+1`, `<segment> India exporters`. Keep in a second small CSV/sheet keyed by `segment_ref`.

## Serper query-template library
- **Identity:** `"<co>" CIN zaubacorp OR tofler` · `"<co>" BSE NSE ticker`
- **Differentiation/moat:** `"<co>" only OR largest OR first manufacturer India` · `"<co>" proprietary OR technology OR custom`
- **Moat (qualification lock-in):** `"<co>" certification OR approval (defence OR aerospace OR automotive OR IATF OR AS9100 OR JSS)`
- **Product-improvement:** `"<co>" R&D OR "research and development" OR "new product" OR DSIR OR patent`
- **Registry proof:** `"<co>" DSIR recognised in-house R&D` · `"<co>" TEC approval` · `"<co>" patent`
- **Market/segment (once):** `<segment> global market size CAGR` · `<segment> demand trend China plus one` · `<segment> exporters India`

## Gemini fill prompt (rules)
- Use ONLY the provided Serper text; if a field isn't supported, leave it blank and set the matching `*_needs_verify=yes` — **never infer or invent**.
- Put a source URL in each `*_source` column.
- A `commodity`/no-moat note requires a **positive** basis (fungible product AND a sweep that found no registry recognition, patent, proprietary process, or spec-lock) — not web-silence.
- Surface positioning (price-led, lowest-bid, "competitive pricing") is **inadmissible** as capability evidence.
- An operator-supplied claim is a **lead**, tagged `self-claimed` + `needs_verify=yes`, never `registry-confirmed`.
- Output the CSV row values for the 38 columns, in order.

## Verification discipline (carried from `data-infra-spec.md`)
Operator/self claim = lead not fact · proof lives in registries the web may not surface (blocked → `needs_verify`) · web-silence ≠ commodity · positioning ≠ capability.

## Grounding budget
Company: ~6–9 Serper + 1 Gemini each. Segment: ~6 Serper once per segment. For 1,100 across ~70 segments ≈ **~8,000 Serper + ~1,100 Gemini**, + the human-verify gate.

## QA / human-verify gate (before handoff)
Spot-check `*_credibility` and sources; resolve `unresolved_pillars` / `claimed-verify` registry items via operator. No row is handed off without passing the no-fabrication check.

## Deliverables & DoD
- **One CSV** (the 38 columns) with a row per company, plus the small segment CSV.
- The 3 reference artifacts she works from: this runbook, `data-infra-spec.md` (field definitions), and `data/hidden-champions-fde-template.csv` (worked rows).
- **DoD:** N companies delivered as schema-valid, source-tagged CSV rows that the downstream ingestion converts to engine JSON and loads into Plan A — proving the CSV → engine contract end to end on real data.

## Downstream (NOT the FDE's job — engineering / Plan A)
A small ingestion step maps the CSV columns → the `engine` JSON object (`alignment[]` from the `align1/2/3` groups, nested `moat{type,durability}`, etc.) → loads into `pdgms_hc_company.engine` as `gated`.
