# Profile FE Contract (v3.0)

### The JSON the frontend renders, and the data-infra stress test

The frontend renders this object. Every text element is a **Node** carrying its data lineage, so the contract doubles as the spec the data infra must satisfy: **if a Node cannot be filled from its declared tier, that is the gap.**

## The Node convention

```jsonc
Node = {
  "text": "string",                 // what renders
  "tier": "company|A2|segment|universal|derived|engagement",
  "epistemic": "fact|interpretation|opportunity|question",
  "source": "string",               // citation shown/footnoted
  "fields": ["dataset.path", ...],  // exact fields it traces to (no field → no Node)
  "flags": { "needsInput": false, "generic": false, "gated": false }
}
```
- `tier` = which data layer must supply it (drives the stress test).
- `generic:true` = a P5 scaffold step, not company-specific (must be visibly marked).
- `needsInput:true` = data missing → FE omits or shows a placeholder, never invents.
- `gated:true` = lives behind a reveal button.

## The contract (shape, with one representative Node per section)

```jsonc
{
  "meta": {
    "schemaVersion": "3.0",
    "profileId": "eldorado-agritech",
    "series": "Hidden Champions of India",
    "segmentRef": "india-seeds",
    "researchDepth": "directory|pursuit",
    "verified": true,               // human no-fabrication gate
    "generatedAt": "<stamped post-gen>"
  },

  "masthead": {
    "kicker": "Hidden Champions of India / a DeepThought series",   // universal
    "headline": { "text": "...", "tier": "universal", "epistemic": "interpretation", "source": "DT framing" },
    "subhead":  { "text": "...", "tier": "company",   "epistemic": "fact", "source": "DRHP", "fields": ["whatTheyDo","ipo.sizeCr"] }
  },

  "snapshot": [                      // wealth-forward cells
    { "label": "Revenue", "value": "₹441 Cr · FY25", "tier": "company", "source": "DRHP", "fields": ["financials.revenueCr.FY25"] },
    { "label": "ROE",     "value": "34.6%",          "tier": "company", "source": "DRHP", "fields": ["financials.roePct_FY25"] }
    // PAT, EBITDA margin, IPO, Founded ...
  ],

  "p1_engine": {                     // ATTENTION
    "eyebrow": "A wealth-creation engine",
    "blocks": [
      { "text": "Revenue grew from ₹270cr (FY23) to ₹441cr (FY25)... PAT grew faster...",
        "tier": "company", "epistemic": "fact", "source": "DRHP",
        "fields": ["financials.revenueCr","financials.patCr","derived.revenueCAGRpct"] },
      { "text": "For scale, Kaveri Seed earned 27.6% EBITDA, 16.9% ROE...",
        "tier": "segment", "epistemic": "fact", "source": "Kaveri filings", "fields": ["peers[0]"] }
      // R&D + products + IPO blocks ...
    ]
  },

  "p2_market": {                     // ATTENTION
    "eyebrow": "The market it sells into",
    "insights": [
      { "point": "...", "evidence": "...", "tier": "segment", "epistemic": "fact",
        "source": "IMARC, Mordor", "fields": ["market","derived.marketSharePct"] },
      { "point": "Buy on yield and price, repeat on trust", "evidence": "...",
        "tier": "segment", "epistemic": "fact", "source": "farmer research", "fields": ["customerValue"] }
    ],
    "reflect": { "text": "...", "tier": "derived", "epistemic": "interpretation" }
  },

  "p3_opportunities": {              // CREDIBILITY (built last, from P4/P5)
    "eyebrow": "Constraints, read as opportunities",
    "items": [
      { "lever": "margin|velocity", "title": "...", "body": "...",
        "glaser": "<oxytocin possibility line>",
        "tier": "derived", "epistemic": "opportunity", "source": "...",
        "fields": ["opportunities[0]"], "opportunityRef": "opp-1" }
    ]
  },

  "p4_experiments": {                // CREDIBILITY, gated
    "eyebrow": "Experiments worth testing",
    "guesslabel": { "text": "Possibilities, not prescriptions...", "tier": "universal" },
    "items": [
      { "lever": "...", "title": "...", "body": "...",
        "tier": "derived", "epistemic": "interpretation", "opportunityRef": "opp-1",
        "flags": { "gated": true } }
    ]
  },

  "p5_workflows": {                  // CREDIBILITY, gated, build-root (P5→P4→P3)
    "eyebrow": "The workflows we mapped (H5 → H1)",
    "intro": { "text": "...", "tier": "universal" },
    "horizontals": [
      { "hId": "H4", "hName": "Capability",
        "steps": ["develop parent lines","breed hybrids & OPVs","field-trial","certify & patent"],
        "stepsTier": "A2|segment",            // A2 = company-specific (pursuit), segment = generic scaffold
        "spottedAt": "field-trial",
        "spotted": { "text": "...", "tier": "A2|derived", "epistemic": "opportunity", "opportunityRef": "opp-1" },
        "source": "DRHP business / CIMMYT",
        "flags": { "gated": true, "generic": false } }   // generic:true if stepsTier==segment
    ]
  },

  "takeaway": { "text": "...", "tier": "universal", "epistemic": "interpretation" },

  "cta": { "label": "Spot an opportunity", "note": "...", "tier": "universal" },

  "colophon": {
    "text": "...", "tier": "universal",
    "sources": ["DRHP","Kaveri filings","IMARC","Mordor","CIMMYT","Simon-Kucher","agri-extension","farmer research"]
  },

  "engagementTier": {               // NEVER rendered as fact; the A→B note
    "note": "What an outside profile cannot see... is what a closer engagement establishes.",
    "items": ["retention","customerValue(company-specific)","trueUnitEconomics"]
  }
}
```

## Stress test — every Node maps to a tier the infra must supply

| Section | Tier(s) the FE demands | Grounded by | Stress point |
|---|---|---|---|
| masthead, takeaway, cta, eyebrows, guesslabel | universal | DT framing (one-time) | free; never a gap |
| snapshot, p1_engine | company (financials, IPO, R&D, products) | DRHP + website (~2-3 calls) | gap if not IPO/disclosed → some cells `needsInput` |
| p1 peer line, p2_market | segment (market, peers, SRR, customerValue) | fetched once per segment | gap = whole segment missing, not per company |
| p3 / p4 | derived (rules over company+segment) | computed at gen | no fetch; gap only if upstream fact missing |
| **p5 horizontals (steps + spotted)** | **A2 (specific) → segment (generic scaffold)** | DRHP business/MD&A, interviews (pursuit) | **the real stress point**: directory pass renders `generic:true`; pursuit pass fills A2. Generic must be marked. |
| engagementTier | engagement (not collected) | n/a | never rendered as fact |

**What the contract proves about the infra:**
1. Universal + derived nodes are free (no fetch) — most of P3/P4 and all framing.
2. Company + segment nodes are the ~3 + ~7-once calls already specced.
3. **The one node type that can silently degrade is `p5.horizontals.steps` when `stepsTier == segment` (generic).** The FE must render `generic:true` distinctly, and pursuit mode must upgrade it to `A2`. This is exactly where credibility lives, so the contract forces the infra to declare per-step whether it's company-specific or generic.
4. Any `needsInput:true` node = a real, visible data gap, never filled by invention.
