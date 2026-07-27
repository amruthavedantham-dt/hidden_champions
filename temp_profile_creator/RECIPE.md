# Recipe — Serper-free research → sources → verified profile

Two phases per company. Do not skip from Phase 1 straight to a finalized
profile — Phase 2 only happens after the user has verified.

## Phase 1 — Research (no Serper; WebSearch/WebFetch only)

Same 4-pillar model and verification discipline as the HVT tool
(`../context/hc-profiling/data-infra-spec.md`), just executed by hand instead
of via Serper+Gemini:

**Queries to run per pillar** (same intent as `Config.js`'s
`SERPER_QUERIES_BY_PILLAR`, adapted to web search):
- Differentiation: `"<company>" patents`, `"<company>" DSIR`, `"<company>"
  "first in India" OR "only" OR "pioneer"`, `"<company>" proprietary technology`
- Moat: `"<company>" certification OR approval OR AS9100 OR IATF OR GOTS`,
  `"<company>" sole supplier OR qualified vendor`
- Product improvement: `"<company>" R&D center`, `"<company>" DSIR
  recognized`, `"<company>" new product launch`
- Alignment/gap: `"<company>" export`, `"<company>" expansion OR hiring OR
  new facility`
- Identity: `"<company>" CIN`, `"<company>" Zauba OR Tofler OR MCA`,
  `"<company>" GST OR GSTIN OR Udyam`
- If a website is known: fetch it directly (WebFetch) and read About/
  Products/R&D/Certifications pages — this is usually higher-signal than
  search snippets.

**Verification discipline — non-negotiable, carried from data-infra-spec.md:**
1. **A company/operator claim is a LEAD, not a fact.** Tag `self-claimed` +
   `needs_verify: yes` by default. It only upgrades if an *independent*
   source (not the company's own site, not a directory that just repeats the
   company's words) confirms it.
2. **Registry proof (DSIR, patents, MCA, sector certs) usually isn't on the
   open web.** If Serper/web search can't reach it, mark `proof_status:
   not-found` + `needs_verify: yes` — never invent a registry check you
   didn't actually do, and never silently drop it either.
3. **Web-silence is not commodity.** If you find nothing on differentiation,
   the field is `unresolved`, not "commodity" — commodity requires a
   *positive* finding (a fungible product AND an active sweep that
   confirmed no patent/registry/proprietary process exists).
4. **Positioning ≠ capability.** "Competitive pricing," "lowest bid," "quality
   products" are marketing copy, not evidence for any pillar.
5. Superlative/exclusivity claims (`"largest"`, `"leading"`, `"sole
   supplier"`, `"India's first"`) are unverified leads needing `needs_verify:
   yes` just like registry-checkable claims — don't let them slip through as
   confirmed just because they don't mention a specific registry.

**Financial snapshot:** search for revenue, PAT/margin, ROE, founded year,
employee count — from DRHP/filings/Tofler/Tracxn/press if the company is
big enough to have any, or its own website/LinkedIn otherwise. Cite each
figure's source individually; don't let one aggregator's number silently
stand in for all of them.

**Segment tier** (`segments/<segment_ref>.json`) — build once, reuse across
every company sharing that segment. Same shape as `../profile_generation/RECIPE.md`
§1: market size/CAGR (global by default), 2-4 named peers with
revenue/margin/ROE, customer buying drivers, the segment's generic H5→H1
value-chain steps, sources. Check this file exists before re-researching a
segment you've already done.

### Phase 1 output: `sources/<slug>.md`

One file per company, this shape:

```
# <Company Name> — sources for verification

## Differentiation
Claim: ...
Source: <url>
Credibility: self-claimed | third-party | qualification-gated | registry-confirmed
needs_verify: yes/no — why

## Moat
(same shape)

## Product improvement
(same shape)

## Alignment
Claim: <capability> → <market need>, pull: must-have|strong|nice-to-have
Source: <url>

## Execution gap
Latent capability / currently monetized / the gap / activation path
Source(s): ...

## Financial snapshot
Revenue: ... (source)
PAT / EBITDA margin: ... (source)
ROE: ... (source)
Founded: ... Employees: ... (source)

## Unresolved
[pillars/facts with no usable evidence — list plainly, don't fill with a guess]
```

**Stop here.** Tell the user the file is ready and wait for their
verification pass before touching Phase 2.

## Phase 2 — Finalize (only after user says the sources check out)

Incorporate whatever corrections the user gave (drop/fix/confirm claims).
Then, same steps as `../profile_generation/RECIPE.md` §3–§7:
1. Derived fields (growth%, market share%, etc — computed, never scraped).
2. `opportunities[]` via the rule table in `generation-spec.md` §D.
3. Classify `healthClass` — strength/cornered-resource pass FIRST, financial
   trend second, never classify off the P&L alone (`engine` / `forward-bet`
   / `capability-led` / `turnaround`).
4. Assemble the contract-v3 JSON bottom-up: P5 workflows (generic scaffold
   + `flags.generic: true` unless the user gave company-specific process
   detail) → P4 experiments → P3 opportunities → P1 engine / P2 market →
   masthead/snapshot/takeaway/cta/colophon/engagementTier. Every Node:
   `{ text, tier, epistemic, source, fields, flags }` — copy the shape from
   `example-eldorado-agritech.json`, don't reinvent it. Anything not
   groundable gets `flags.needsInput: true`, never invented.
5. `meta.verified: true` — only now, because the user has actually checked
   the sources. `meta.schemaVersion: "3.0"`, `researchDepth: "directory"`
   (this whole folder is directory-depth research; call it `"pursuit"` only
   if the user gave real call/DRHP intel beyond consent).

### Phase 2 output

`companies/<slug>.json` (upload-ready for the CRM's New Profile form) and
`companies/<slug>.html` (readable preview, same visual pattern as
`../context/hc-profiling`'s worked HTML examples).
