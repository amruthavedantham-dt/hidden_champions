# Temp Profile Creator — Serper-down fallback

**Why this exists, separate from `../profile_generation/`:** that folder
assumes you already have an HVT sheet row (built via Serper grounding +
Gemini). Serper credits are exhausted right now, so there's no way to get a
fresh HVT row for a new company today. This folder does the whole thing —
research AND profile generation — using Claude's own web search instead of
Serper. Once credits are back, go back to the normal HVT sheet → `profile_generation`
flow for volume; use this only to keep moving today.

## The two-phase process, per company

**Phase 1 — research + sources (Claude does this)**
You give me: company name, website if known, and anything you have (this is
usually just consent, from the blind-call note — that's fine, see below).
I research the company myself (web search, no Serper) against the same
4-pillar model and verification discipline the HVT tool uses, and write
`sources/<slug>.md` — every claim I found, tagged with its credibility tier,
and the exact source URL. **I do not finalize anything at this stage.**

**Phase 2 — you verify, then I finalize**
You open `sources/<slug>.md`, check each claim against its source, tell me
what to fix/drop/keep. Once you say it's good, I generate:
- `companies/<slug>.json` — the full contract-v3 profile, `meta.verified: true`
  (only set after your go-ahead, never before)
- `companies/<slug>.html` — a readable preview

Then you upload `companies/<slug>.json` straight into the CRM's **New
profile** form (domain + slug + paste/attach the JSON) — no Postman, no API
token.

## What to give me to start a company

- Company name (exact legal name if you have it — spelling matters, a wrong
  name returns nothing)
- Website, if known
- Anything from the call beyond consent (skip if there's genuinely nothing —
  see below)
- Any financial figures you already have, with source

## If the call gave you nothing but permission

That's fine and expected for a blind call — same as we discussed for the CRM
route. I'll research the company from scratch (public web only) and the
profile's P5 workflow section will honestly fall back to the segment's
generic scaffold (`stepsTier: "segment"`, `flags.generic: true`) rather than
claiming company-specific process detail I don't actually have. Everything
else (financials, market, opportunities) comes from public research.

## Files here

| Path | Purpose |
|---|---|
| `RECIPE.md` | Full operating instructions I follow for both phases |
| `segments/<segment_ref>.json` | Segment-tier research, fetched once, reused across companies in the same segment |
| `sources/<slug>.md` | Phase 1 output — draft claims + sources, for you to verify |
| `companies/<slug>.json` / `.html` | Phase 2 output — final profile, only after you've verified |

## SSOT this still follows

`../context/hc-profiling/data-infra-spec.md` (the 4-pillar verification
discipline), `generation-spec.md` + `profile-fe-contract.md` (the profile
schema), `example-eldorado-agritech.json` (reference output).
