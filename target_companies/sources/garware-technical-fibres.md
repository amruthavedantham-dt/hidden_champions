# Garware Technical Fibres Ltd — sources for verification

## Differentiation / moat / product improvement
From HVT sheet row (Serper+Gemini-researched, reviewed `Verified`, but
`unresolved_pillars: differentiation, moat` — the HVT tool itself flagged
these two as needing another look despite the review status; recommend
re-checking before flipping `meta.verified`).
- Differentiation: "India's leading player in technical textiles..." —
  self-claimed, `needs_verify: yes` per sheet. Source: garwarefibres.com.
- Moat: Four Star Export House (DGFT) — self-claimed, `needs_verify: yes`
  per sheet. Source: garwarefibres.com.
- Product improvement: DSIR-registered R&D unit, patented V2/anti-fouling
  nets — `registry-confirmed`, `needs_verify: no` per sheet. Source:
  indiascienceandtechnology.gov.in (DSIR's own listing).

## Financial snapshot (fresh research, this session)
- Revenue FY24-25 ₹1,540 Cr / FY25-26 ₹1,529 Cr, PAT ₹232 Cr → ₹199 Cr,
  EBITDA margin ~21% → ~19%: screener.in/company/GARFIBRES/consolidated/
- ROE 18.07% (Q4 FY26): marketsmojo.com result analysis
- Founded 1976: indiantextilemagazine.in company history piece
- Employee count: genuinely conflicting across sources (1,000-5,000 band
  per PitchBook vs. an apparent "22 employees" filing anomaly on another
  aggregator) — excluded from the profile rather than guessed
- Export share 57%→61%, 75+ countries, regional cage-net dominance
  (90% Canada, 80% Scotland, 30-35% Chile/Norway):
  indiantextilemagazine.in; blog.leveragedgrowth.in
- Patents ~90-101 filed (figure varies by source, both cited):
  indiantextilemagazine.in; scanx.trade
- July 2025 Norway acquisitions (OTS, AMS) + UK subsidiary:
  blog.leveragedgrowth.in; aquafeed.co.uk

## Segment: nets-ropes-geosynthetics
Built fresh this session — see `../segments/nets-ropes-geosynthetics.json`
for full sourcing (Grand View Research, Future Market Insights, Research
and Markets, Indian Infrastructure magazine, ScienceDirect). No clean
public peer set was found for direct netting/geosynthetics comparables —
the only "peer group" tool result (Trendlyne) returned generic textile
companies (Raymond, Ginni Filaments) that are not functional comparables,
so `peers[]` was left empty rather than populated with a bad match.

## needsInput / gaps
- R&D headcount: not found.
- Clean segment-specific peer financials: not found (flagged above).
- `marketSharePct` was deliberately not computed — Garware's real position
  is a set of regional dominance figures (90% Canada, etc.), not a share
  of a single well-defined global addressable market; `p2_market` states
  this explicitly rather than forcing a misleading percentage.
