# Worked example — a solution-led "Software Fit" profiler

The most common reason to build a second profiler: **you built a software, it solves problem XYZ for a definable kind of company, and you want to reach those companies with a page that proves you understand them.** The profiler researches each target company; the lens writes a spotlight in three movements: what the company is doing, where its record suggests the problem shows up, and which capability of your software answers each observed strain. The page is sent to the company itself, so "what they lack" must read as recognition, never as diagnosis.

The fictional software here: **FlowStock**, an inventory and demand planning SaaS. Problem XYZ: spreadsheet planning breaking at multi-plant, multi-channel scale (stockouts, overstock, planner burnout). ABC profile: operations heads at mid-size consumer-goods manufacturers. Swap in your own software and the whole file still works; nothing below needs CRM code.

## 1. The topic ontology (the fork of `Config.gs`)

Three pillars replace differentiation/moat/product_improvement:

| Pillar | What it captures |
|---|---|
| `operations-footprint` | What the company runs today: plants, SKUs, channels, capacity |
| `planning-pain` | Signals of the problem the software solves: stockouts, reposted planner roles, manual tooling |
| `buying-readiness` | Timing signals: expansion, new channels, systems moves, funding |

HVT columns (per company row): the identity block unchanged (`company_name, website, cin, ownership_type, sector, segment_ref`), then per pillar: `<pillar>`, `<pillar>_source`, `<pillar>_credibility`, `<pillar>_needs_verify`, `<pillar>_review`, plus `company_summary`, `triage_status`, `unresolved_pillars`. Of the structured extras, this topic **keeps the alignment columns** (they map software capability to observed need, see below) and **drops gap/proof** — those belong to the first profiler's ontology.

One topic-specific constant joins `Config.gs`: the software's capability list, the fixed side of every alignment row.

```
const SOLUTION_CAPABILITIES = [
  'Multi-plant demand forecasting that replaces spreadsheet planning',
  'Channel-level inventory sync across D2C, marketplaces and distributors',
  'Stockout and overstock alerts with reorder suggestions',
  'Planner workflow: one queue instead of mailed spreadsheets'
];
```

Query battery (`SERPER_QUERIES_BY_PILLAR`), examples:

```
operations-footprint: '"{company}" plant OR facility OR capacity', '"{company}" SKUs OR product range', '"{company}" distributors OR marketplace OR D2C'
planning-pain:        '"{company}" out of stock OR unavailable', '"{company}" "demand planner" OR "supply planner" job', '"{company}" ERP OR "excel planning"'
buying-readiness:     '"{company}" expansion OR "new plant" OR funding', '"{company}" D2C launch OR "online store"', '"{company}" digital OR automation initiative'
```

`Vocabularies.gs` re-derived: the high-signal sources for this topic are job boards, marketplace seller pages and retailer reviews (strain shows up there before it shows up in press releases); trigger keywords forcing `needsVerify` become "zero stockouts", "98%", "fully automated", "doubles".

`Gemini.gs` keeps the extract-only pattern (temperature 0, JSON out, code-side sanitization, `thinkingBudget: 0`) and gains one mapping step: from `SOLUTION_CAPABILITIES`, emit at most 3 capability-need pairs where the **need quotes something observed** in the staged evidence. A capability with no observed need is omitted; the sanitization pass clears any pair whose need has no word overlap with the evidence. Never invent a need to fit a feature.

## 2. What the export emits (unchanged mechanics, new words)

```json
{
  "schemaVersion": 1,
  "source": "hcp-profiler",
  "runId": "export-3-1785500000000",
  "exportedAt": "2026-08-06T11:00:00Z",
  "companies": [
    {
      "identity": { "name": "Meridian Kitchenware Pvt Ltd", "website": "https://meridiankitchen.example", "sector": "consumer goods, cookware" },
      "summary": "Mid-size cookware and kitchen-storage maker, three plants near Coimbatore, selling through distributors and marketplaces, now opening a D2C channel.",
      "triage": { "status": "auto-confirmed", "unresolvedPillars": [] },
      "claims": [
        { "pillar": "operations-footprint", "claim": "Runs three plants around Coimbatore and lists about 1,200 active SKUs across cookware and kitchen storage.", "source": "https://tradedaily.example/meridian-third-plant", "credibility": "third-party", "needsVerify": "no", "review": "Verified" },
        { "pillar": "planning-pain", "claim": "A demand planner opening asking for advanced Excel has been reposted for four months.", "source": "https://jobs.example/meridian-demand-planner", "credibility": "third-party", "needsVerify": "no" },
        { "pillar": "buying-readiness", "claim": "The company says its new D2C store will double online volume by FY28.", "source": "https://meridiankitchen.example/press/d2c-launch", "credibility": "self-claimed", "needsVerify": "yes", "review": "Pending" }
      ],
      "evidence": [
        { "text": "Marketplace seller page: 14 of Meridian's 60 bestselling listings showed 'currently unavailable' during Diwali week, back in stock by December.", "source": "https://marketplace.example/meridian-seller", "pillar": "planning-pain" },
        { "text": "Trade daily: the third Coimbatore plant commissioned in 2025 adds roughly 40% capacity, aimed at the kitchen-storage lines.", "source": "https://tradedaily.example/meridian-third-plant", "pillar": "operations-footprint" },
        { "text": "Retail news: Meridian's D2C store launches with 300 SKUs; the company plans marketplace exclusives for the rest of the range.", "source": "https://retailnews.example/meridian-d2c", "pillar": "buying-readiness" }
      ],
      "alignment": [
        { "capability": "Multi-plant demand forecasting that replaces spreadsheet planning", "need": "A demand planner posting built around Excel, live for four months, at three-plant and 1,200-SKU scale", "pull": "strong", "source": "https://jobs.example/meridian-demand-planner" },
        { "capability": "Channel-level inventory sync across D2C, marketplaces and distributors", "need": "A new D2C store adds a third channel to reconcile against marketplace and distributor stock", "pull": "moderate", "source": "https://retailnews.example/meridian-d2c" }
      ],
      "contacts": [ { "name": "S. Meenakshi", "designation": "Head of Operations" } ]
    }
  ]
}
```

Note what carried over untouched: the envelope shape, `source: "hcp-profiler"` (protocol id), credibility grading, held-claims semantics (the self-claimed "double online volume" line stays out of generation until reviewed), evidence with URL-only sources. And note the reuse move: **`alignment` keeps its fixed field names** (`capability`, `need`, `pull`, `source`) **with this topic's own semantics** — capability is what the software does, need is what the company's record shows. Any offer-meets-need topic can ride these fields the same way.

## 3. The lens (the only CRM-side artifact)

```json
{
  "schemaVersion": 1,
  "name": "FlowStock Fit",
  "slug": "flowstock-fit",
  "description": "Reads a manufacturer through the problem FlowStock solves: what the company runs today, where the record says planning strains, and which FlowStock capability answers each strain.",
  "thesis": {
    "claim": "A company this deliberate about making and selling things eventually outgrows spreadsheet planning, and the strain shows up in public before it shows up in the P&L. This page holds what the company runs today against the strain its own record shows, then maps each strain to the one FlowStock capability that answers it. Nothing generic: every fit named here traces to something observed.",
    "tone": "A solutions engineer who did the homework, writing to an operations head: specific about their business, plain about ours, no feature hype. Their record leads; the software follows.",
    "reader": "The operations or supply-chain head at the profiled company. The page is sent to them, so it must read as recognition and help, never as surveillance or diagnosis."
  },
  "blocks": [
    { "blockKey": "company-snapshot", "renderHint": "stats", "required": true,
      "dataRequirements": ["identity", "firmographics"],
      "question": "What placement facts frame this company before reading?",
      "approach": "Label: value lines from grounded facts only: sector, plants, SKU count, channels, ownership. Omit what the data cannot ground." },
    { "blockKey": "operating-picture", "renderHint": "para", "required": false,
      "dataRequirements": ["claims", "evidence", "momentum"],
      "question": "What is this company doing and building right now?",
      "approach": "Write their operation the way they would be proud to read it: plants, range, channels, recent moves, drawn from third-party evidence first. Attribute self-claims once, then set them against the record. This section earns the right to discuss strain, so it must be the best-researched writing on the page. No software mentions here." },
    { "blockKey": "where-it-strains", "renderHint": "para", "required": false,
      "dataRequirements": ["claims", "evidence"],
      "question": "Where does the record suggest planning strains as they grow?",
      "approach": "Only strains the evidence shows, each as its own card: a '### ' heading of the form 'SIGNAL — <title>', a body developing what was observed and why it matters at their scale, and a closing line naming the evidence. Written as observations a good operator would recognize in their own week, never as diagnosis or blame. Still no software mentions." },
    { "blockKey": "how-flowstock-helps", "renderHint": "para", "required": false,
      "dataRequirements": ["alignment", "claims", "evidence"],
      "question": "Which FlowStock capability answers which observed strain?",
      "approach": "One card per alignment pair: a '### ' heading of the form 'FIT — <title>', the need first in their terms, then the capability that answers it, then a closing line naming the evidence behind the need. Skip any capability the record gives no need for; a short honest list beats a feature tour." }
  ],
  "ask": { "cta": "Thirty minutes, your SKU list, live on FlowStock. We set it up, you judge it.", "framing": "an offer of help with a strain the record suggests they already feel, not a pitch" }
}
```

The user's three questions map one-to-one onto the blocks: what their company is doing (`operating-picture`), what it is lacking (`where-it-strains`), how we can help with this software (`how-flowstock-helps`). The card vocabulary is this lens's own (SIGNAL/FIT); the `### TAG — Title` card mechanism is the engine's. And the honesty doctrine does the selling: the strain section carries no product mention at all, so by the time FlowStock appears, every fit already has an observed need under it.

## 4. Running it

1. Import the export file (`/crm/companies` → Import from profiler → pick the offering, e.g. "FlowStock").
2. Import the lens above (Spotlights → Lenses → Import JSON). Active immediately.
3. Create a spotlight for Meridian with the FlowStock Fit lens. Layout: the default **Editorial** suits this topic well (its pinned Proof / Activation Path reveals read naturally as "the evidence of strain" and "the path to adopting"); **meeting-pack**, **objections** or **evidence** archetypes also fit, with model-authored section titles.
4. Generate → review → publish → send to S. Meenakshi. Citations tracked internally, sources hidden from the reader, cost stamped per version — identical machinery.
5. Engagement capture and the Heat Index then tell your team who actually read their page and how warm they are — the lead-scoring half of this topic is already built into the CRM and stays private to your org.

## 5. Where this topic would hit the known exceptions

- Wanting a typed **capability-gap matrix** per company (rows: capability, their current tool, severity) → the ~5-file structured-sections extension. Flat claims + evidence + 3 alignment rows cover the standard case.
- Wanting the page itself to **grade the lead** ("strong fit / weak fit" verdicts on the page) → verdict territory: wire `thesis.stance` first. Today's doctrine deliberately never grades the reader's company to their face; the CRM's Heat Index does the scoring privately.
- Wanting a pinned fixed frame like "Your stack today / With FlowStock" → one entry in the layout catalog.
