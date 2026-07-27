# target_companies

Verified profiles for companies sourced from the Hidden Champions HVT
Google Sheet (pillar research already run + reviewed via the Apps Script
tool — see `../apps_script/`) — distinct from `../temp_profile_creator/`,
which holds earlier hand-researched/test entries. Same contract-v3 JSON
shape and same verification discipline (`../temp_profile_creator/RECIPE.md`),
except Phase 1 pillar research (differentiation/moat/product_improvement/
alignment/gap) is taken from the sheet's already-reviewed columns instead of
being redone — only financials (revenue, PAT/margin, ROE, founded, employee
count) and any sheet gaps get fresh research per company.

- `companies/<slug>.json` + `.html` — finalized profile + preview
- `segments/<segment_ref>.json` — shared segment-tier market data, reused
  across companies sharing a `segment_ref`
- `sources/<slug>.md` — per-company source log, mainly for financial figures
  and anything not already covered by the sheet's own source columns
