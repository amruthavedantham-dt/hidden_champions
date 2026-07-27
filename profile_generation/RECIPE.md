# Recipe — HVT row → contract-v3 profile JSON + HTML preview

Follow this in order, for one company per request. Full rules live in
`../context/hc-profiling/generation-spec.md` and `profile-fe-contract.md` —
this is the condensed, operational version; fall back to those two files for
anything not covered here.

## 0. Inputs for this run

- The company's HVT row (Plan B's 38 columns — `differentiation`, `moat_*`,
  `product_improvement*`, `align1-3_*`, `gap_*`, `proof_*`, `unresolved_pillars`,
  `segment_ref`, `notes`, sources for each).
- Financial snapshot facts, each with where it came from (DRHP / Screener /
  Tofler / Tracxn / press). Need at least: revenue, one of PAT or EBITDA
  margin, ROE, founded year. Missing ones become `needsInput: true`, never
  guessed.
- Optional A2 intel (pursuit pass only) — see generation-spec.md §A2.
- `researchDepth`: `"directory"` if no A2 was given, `"pursuit"` if it was.

## 1. Segment tier — build once, reuse always

Check `segments/<segment_ref>.json` first. If it exists, reuse it as-is — do
not re-research. If it doesn't:

Research and write it, shaped per generation-spec.md §B:
`segmentName`, `market` (GLOBAL by default — world size range + CAGR +
export geographies + global competitors + domestic slice), `subSegments[]`,
`adjacentMarkets[]`, `structureFacts[]`, `adoptionStructure` (seed-replacement-
rate-style recurring-demand structure, if applicable to the segment),
`peers[]` (2-4 named comparable companies with revenue/margin/ROE/growth —
this benchmarks the company numbers in P1), `customerValue` (drivers +
strongest predictor, from buyer research if findable), `valueChain[]` (the
generic H5→H1 steps for how companies in this segment operate — this is the
`stepsTier: "segment"` fallback every company in the segment shares),
`sources[]`.

This is the expensive, deep-research step — spend real effort here, because
it amortizes across every company sharing this `segment_ref`.

## 2. Company tier (A) — map the HVT row + financials

Map the HVT columns to generation-spec.md §A fields:
- `differentiation` + `moat*` + `product_improvement*` → `corneredResource`
  `{ claim, type, source, claimCredibility, confidence, needsOperatorVerify }`
  + `capabilities[]`. Carry the HVT row's `*_credibility` and `*_needs_verify`
  through untouched — do not re-judge them here.
- `align1-3_*` → `demandTailwind` candidates (the market trend the capability
  points at) — cross-reference against the segment's `market`/`customerValue`.
- `gap_*` → seeds for `opportunities[]` (step 4), not rendered directly.
- `proof_type`/`proof_status`/`proof_source` → `certifications[]` /
  `qualifications[]` entries if `proof_status` is `confirmed` or `claimed-verify`.
- Financial snapshot facts → `financials{ revenueCr, patCr, ebitdaMarginPct,
  roePct, ... }`, `foundedYear`, `employees`. Each keeps its own source.
- `notes` column — scan for anything not already captured (name collisions,
  informal financial mentions) and fold in or discard.

If A2 was given, map it to §A2 fields (`goToMarketIntel`, `rdToMarketIntel`,
`operationsIntel`, `statedPriorities`, `signals`, `strategicNarrative`,
`customerEvidence`, `outsideInQualitative`, `theoryOfBusiness`) — this is what
lets P5 be company-specific instead of the segment's generic scaffold.

## 3. Derived (compute, never scrape)

`revenueGrowthPct`, `marketSharePct` (company revenue in USD ÷ segment market
size), `growthVsMarketX`, `rdRatio` (rdHeadcount ÷ employees, if known),
`dealerActivePct` if distribution data exists. Skip any derived field whose
inputs are missing — don't estimate.

## 4. Opportunities[] (rule-derived, one rule → one card)

Apply generation-spec.md §D's rule table against what's now known (patents,
`dealerActivePct`, `recentMoves`, product categories, `geographyScope`).
Every hit becomes `{ lever: margin|velocity, hId, statement, evidenceFields[] }`
with an `opp-N` id — these seed both `p3_opportunities` and `p4_experiments`
later. If the HVT row's `gap_activation_path` already names an opportunity the
rule table misses, add it too (tag `source: "gap_activation_path"`).

## 5. Classify `healthClass` (strength pass FIRST, financials second)

Do NOT classify off the P&L alone. Per generation-spec.md's P1 narrative
frame:
1. Find the cornered resource / strength first (from `corneredResource` +
   `capabilities[]` + the HVT pillars) and its `demandTailwind`.
2. Read the financial trend honestly (revenueTrend / profitTrend /
   marginTrend — three separate up/flat/down calls, don't average them).
3. Classify:

| healthClass | when |
|---|---|
| `engine` | profit up + healthy ROE |
| `forward-bet` | financials soft/down + a credible tech/platform bet |
| `capability-led` | financials lag, but a valuable capability the market is moving toward |
| `turnaround` | real stored assets/brand, financials lagging |

No `screen-out` — inclusion was already decided upstream. Weak financials are
narrative context (capability-led / turnaround), never a reason to drop or
downgrade the profile.

## 6. Assemble the contract-v3 JSON — build order P5 → P4 → P3 → P1/P2

Every text element is a Node: `{ text, tier, epistemic, source, fields,
flags }` (see profile-fe-contract.md for the exact shape and one worked
example per section — copy its structure, don't reinvent it).

1. **p5_workflows** first: one entry per Hx (H5 Offers → H4 Capability → H3
   Capacity → H2 Customer experience → H1 Orders). `stepsTier: "A2"` +
   `flags.generic: false` only where A2 intel actually grounds that
   horizontal's steps; otherwise `stepsTier: "segment"` + `flags.generic: true`
   using the segment's generic `valueChain[]` — **mark it, never present a
   generic step as company-specific.** Each horizontal's `spotted` node links
   to an `opportunityRef` from step 4.
2. **p4_experiments**: one experiment per opportunity from step 4, gated
   (`flags.gated: true`), referencing `opportunityRef`.
3. **p3_opportunities**: the same opportunities, rendered as reader-facing
   cards (`lever`, `title`, `body`, a Glaser-style possibility line), each
   with its `evidenceFields`.
4. **p1_engine**: financial narrative (revenue/PAT/margin/ROE trend, honestly
   stated per §Discipline — never assume growth), peer benchmark line from
   the segment's `peers[]`, R&D/patents/certifications, IPO if applicable.
   Lead with the cornered resource + demand tailwind if `healthClass` is
   `capability-led` or `forward-bet` (don't lead with weak numbers).
5. **p2_market**: segment market sizing + `marketSharePct` (or, if the
   segment's `nature` is commodity and share is sub-1%, say so plainly and
   pivot to the sub-niche where the capability actually competes — set
   `shareIsMeaningful: false` in that case), `customerValue`, structural
   trend facts.
6. `masthead`, `snapshot`, `takeaway`, `cta`, `colophon`, `engagementTier` —
   templated per `example-eldorado-agritech.json`, swap in this company's
   facts. `engagementTier` never asserts a fact — it only names what a real
   engagement would establish (retention, true unit economics, etc.).

**Every Node needs a `fields` array pointing at what it traces to.** If a
Part would need a fact that isn't in the HVT row, the financial snapshot, or
A2/segment data — set `flags.needsInput: true` on that Node (or drop it) and
list it in the run's verification checklist (step 7). Never invent a number
or a quote to fill a gap.

`meta`: `schemaVersion: "3.0"`, `profileId`/`slug` (readable kebab), `series:
"Hidden Champions of India"`, `segmentRef`, `researchDepth`, **`verified:
false`** (always — this is the human gate, not Claude's to flip), `generatedAt`
stamped now.

## 7. Output

Save two files under `companies/`:
- `<slug>.json` — the full contract-v3 profile from step 6.
- `<slug>.html` — a rendered preview. Reuse the exact CSS/layout pattern from
  `../context/hc-profiling`'s worked HTML examples (`eldorado.html`,
  `pioneer.html` — read whichever is closer in tone/length), swap in this
  company's content, keep Parts 4/5 behind the same reveal-button pattern.

Then give the user a short verification checklist: every `fact` Node's
source, every `needsInput: true` Node, and anything from `unresolved_pillars`
that made it into the profile — this is what they check before flipping
`meta.verified` themselves and (once they have the API token) uploading.
