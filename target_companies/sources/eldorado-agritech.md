# Eldorado Agritech Pvt. Ltd. — sources for verification

No fresh research was done for this company. Its HVT sheet row (segment_ref
`crop-seeds`) matches an already-existing, previously-approved contract-v3
profile: `../../context/hc-profiling/example-eldorado-agritech.json`
("Tarun-approved," hand-converted from `outputs/eldorado-agritech.html`,
2026-06-30). That file's content was copied into
`../companies/eldorado-agritech.json` and `.html` unchanged, except:
- `meta.segmentRef` relabeled `india-seeds` → `crop-seeds` to match this
  company's HVT sheet segment_ref.
- `meta.verified` reset to `false` — a human has not re-checked this content
  specifically inside `target_companies/` yet, even though it was verified
  in its prior context.

All financial figures (revenue, PAT, EBITDA margin, ROE, IPO size), market
data, and workflow steps trace to the original file's own sources: DRHP,
Kaveri Seed filings, IMARC, Mordor Intelligence, CIMMYT, agri-extension
research, farmer purchase-decision research, CARE Ratings, company-reported.
See that file's `colophon.sources` for the full list.

## Unresolved
The HVT sheet row flags `unresolved_pillars: product_improvement` and
`triage_status: needs-review` for this company. The reused profile's P1
block *does* state R&D/patent/certification facts (66 of 1,371 employees in
research, 9 patents, DSIR/NABL/ISO/IEC 17025 labs) that read as
product-improvement evidence — but those came from the DRHP/company-reported
sources in the original fixture, not from re-checking whatever gap the HVT
tool's own Serper+Gemini run flagged. **Recommend the user specifically
compare the HVT sheet's `product_improvement`/`product_improvement_source`
cell for this row against the P1 block above before flipping
`meta.verified`** — they may already agree, but this file did not verify
that itself.
Row identity (for cross-check): CIN `U01400TG2009PLC063998`, ownership_type
`listed` (per the sheet — note the reused profile's own colophon still
narrates it as pre-IPO/DRHP-filed, i.e. not yet listed at the time that
content was written; confirm which is current).
