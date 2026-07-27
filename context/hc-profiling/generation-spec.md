# Profile Generation Spec — Data-In, Profile-Out

### Program: dt-ICP-publicprofile | 2026-06-30
### Freeze this dataset, fetch it for 1000 companies (factory), generate each profile from the data alone (individual)

---

> **SCOPE: this is the PROFILING project, not the data infra.** The data infra (`data-infra-spec.md`) is a separate, inclusion-only step: it decides *who* is a Hidden Champion or potential one by detecting **capability + market**, and it NEVER eliminates. Profiling assumes a company is already qualified, and only decides *how to tell its story*. Nothing in this spec screens a company out. The `healthClass` labels below (engine / forward-bet / capability-led / turnaround) are **narrative frames** for the P1 story, not gates — there is no `screen-out`.

---

## The two functions, and the build order

- **P1, P2 = attention mechanics** (the hook): the wealth engine and the market. Numbers-light; they earn a read, not trust.
- **P3, P4, P5 = the credibility engine**, built **bottom-up** (opposite of display order):
  **P5** (their *actual* workflow, specific intel) → **P4** (HVT experiments that fit it) → **P3** (the opportunities those chase).
- A **generic P5 collapses the stack.** If P5 is generic industry steps, P4 and P3 are generic too, and nothing earns "they studied us." P5 must be specific to the company.

**Two research depths (by intent):**
- **Directory pass (the 1,000):** lean (~3 calls), attention layer + generic-scaffold execution.
- **Pursuit pass (companies you chase):** deep qualitative dig for the bottom half, worth the premium. Mine the DRHP "Our Business" + MD&A + Risk Factors, management interviews, news, the company's own content for *operational intel*. The highest-value data here is **qualitative, not numeric.**

## The principle

**Research is a factory process; generation is individual.** The factory fills a frozen dataset (segment data once per segment, company data per company). Generation then templates Parts 1-5 from those fields only, no live research. This is token-efficient (research done once, in batch) and accurate (generation uses sourced fields only, so it cannot hallucinate).

```
SEGMENT dataset (once per segment)  ─┐
COMPANY dataset (scraped per co.)   ─┼─►  DERIVED (computed)  ─►  OPPORTUNITIES (rules)  ─►  TEMPLATE P1-P5
```

---

## A. company  (scraped per company)

| Field | Type | Used in |
|------|------|---------|
| name, brands[], foundedYear, hqCity, hqState, sector, subSector | str | P1 |
| **whatTheyDo, statedPositioning, operationsModel** (grounded prose, ideally their words) | str | P1/P5 — *prevents invented descriptions* |
| **leadership**: { promoters[], rd } (founder / maverick signal) | obj | P1 |
| products: { varietiesCount, cropsCount, **crops[]**, **flagship**, categories[] } | obj | P1, P5 |
| **financials**: { revenueCr{FY}, patCr{FY}, ebitdaCr{FY}, ebitdaMarginPct{FY}, roePct, rocePct, borrowingsCr{FY}, revenueMixPct{} } | obj | P1, P2, derived |
| **revenueTrend / profitTrend / marginTrend**: up\|up-slow\|flat\|down (THREE separate trends; they diverge, e.g. Pioneer revenue up + profit down) | enum×3 | P1 |
| **wealthEvidenceType[]**: financial \| tech-leadership \| global-position \| customer-ROI \| forward-bet \| stored-assets \| brand (an ARRAY; the nucleus may lean on several; Pioneer leans on tech-leadership + forward-bet + stored-assets) | enum[] | P1 |
| **healthClass**: engine \| forward-bet \| turnaround \| screen-out (the wealth-engine screen, see below) | enum | P1, gate |
| **archetype**: e.g. The Patent House, The Quiet Exporter, The Heritage Maker in Recovery | str | P1 |
| **brand**: { name, heritageYear, channels[], recognition } (a consumer brand is a wealth asset + a velocity lever; seed/process models had none, Pioneer has Hakoba) | obj | P1, P3(velocity), P5(H2) |
| **exportFootprint**: { countries, sharePctIfKnown } | obj | P1, P2 |
| **ipo**: { sizeCr, freshCr, ofsCr, drhpFiled, promoters[] } | obj | P1 |
| employees, rdHeadcount | int | P1, derived |
| patents | int | P1, opp |
| certifications[] | str[] | P1 |
| products: { varietiesCount, cropsCount, categories[] } | obj | P1, P5, opp |
| rd: { farmsAcres, leadership } | obj | P1, P5 |
| distribution: { dealersTotal, dealersActive, statesCount, countryStatesTotal, geographyScope } | obj | P1, P2, P5, opp |
| recentMoves[] | str[] | P1, P5, opp |
| segmentRef | str | links to B |
| sourcesByField | map | every part (provenance) |

## A2. company execution intel  (qualitative; pursuit pass; feeds P5 → P4 → P3)

The bottom-half credibility data, and the highest-value grounding for a company you chase. Sourced from the DRHP "Our Business" / MD&A / Risk Factors, management interviews, news, and the company's own content. Specific to the company; this is what makes P5 *theirs*, not generic.

- **goToMarketIntel** — real channel / demand / pricing practices → P5 H1/H2
- **rdToMarketIntel** — breeding, trial, launch process → P5 H4/H5
- **operationsIntel** — own vs contract production, processing, capacity → P5 H3
- **statedPriorities / risks** — what management says it chases or fears → P4
- **signals** — hiring, capex, launches, partnerships → momentum
- **strategicNarrative** — origin → current bet → trajectory (the *story*, not just facts; Damodaran). e.g. SED: sugar-process tech → biofuel/SAF platform → P1/P2 forward layer
- **customerEvidence** — case studies, named deployments, outcomes, testimonials (company-specific PMF proof; Ellis) → P1/P3
- **outsideInQualitative** — what press, analysts, customers, reviews, awards say (counters self-serving self-description; Drucker) → P1/P2
- **theoryOfBusiness / jobToBeDone** — who the customer is, the job they hire the company for, what it is abandoning (Drucker) → P3/P5

Sources for the qualitative tier: DRHP business/MD&A/risk, management interviews, **case studies, press, analyst notes, reviews, awards, client lists.**

**Rule:** where this intel is grounded, P5 uses it. Where it isn't, P5 falls back to the segment's generic value-chain steps, **marked as generic**, never presented as theirs.

## B. segment  (fetched once per segment, shared)

| Field | Type | Used in |
|------|------|---------|
| segmentName | str | P2 |
| **segments[]** (a company can sell into MORE THAN ONE; Pioneer = commodity yarn + embroidery/lace + brand) — each: { key, **nature: commodity\|differentiated**, market{...}, **shareIsMeaningful: bool** } | obj[] | P2 |
| **market (GLOBAL by default)**: { worldSizeUSD_B range, cagr range, **exportGeographies[]**, **globalCompetitors[]**, domesticSlice } | obj | P2, derived |
| *Note: most Hidden Champions are exporters; the market tier is the WORLD market with a domestic slice, never India-only.* | | |
| *Note: in a COMMODITY market a tiny maker's share% is the wrong metric (Pioneer ~0.06% of $67B PFY). Set `shareIsMeaningful:false` and pivot P2 to the differentiated sub-niche / second segment where it actually competes.* | | |
| subSegments[]: { name, sizeUSD_M_from, yearFrom, sizeUSD_M_to, yearTo, hybridSharePct } | obj[] | P2, P3 |
| adjacentMarkets[]: { name, sizeUSD_B, lossSplit } | obj[] | P2, P3 |
| structureFacts[] | str[] | P2 |
| adoptionStructure: { srrNationalPct, farmSavedPct, hybridRepurchase } | obj | P2 (headroom + recurring demand) |
| **peers[]**: { name, revenueCr, ebitdaMarginPct, patMarginPct, roePct, growthPct } — collected (e.g. Kaveri Seed); benchmarks the company numbers (Damodaran) | obj[] | P1 |
| **customerValue**: { drivers[], strongestPredictor } — collected (farmer purchase-decision research, Drucker) | obj | P2 |
| valueChain[]: { hId, hName, steps[] } (H5..H1) | obj[] | P5 |
| benchmarks[]: { name, value, source } | obj[] | P5/opp |
| sources[] | str[] | all |

## C. derived  (computed at generation, no research)

- revenueGrowthPct = revenueCr / revenuePrevCr − 1
- marketSharePct = (revenueCr → USD) / segment.market.size
- growthVsMarketX = revenueGrowthPct / segment.market.cagr
- rdRatio = rdHeadcount / employees
- dealerActivePct = dealersActive / dealersTotal

## D. opportunities[]  (rule-derived from A+B+C; one rule → one card)

Each: `{ lever: margin|velocity, hId, statement, evidenceFields[] }`. Rules:

| Rule (trigger) | → Opportunity | lever | hId |
|---|---|---|---|
| patents > 0 AND segment hybrids carry a yield premium | Pricing the patents | margin | H5 |
| dealerActivePct < 60% | Reactivate dormant dealers | velocity | H2 |
| recentMoves names a new high-value subSegment | The growing [subSegment] | velocity | H3 |
| products.categories includes seed AND crop-protection | The input basket | margin | H5 |
| geographyScope == domestic AND segment has export tailwind | More states & export | velocity | H1 |

## E. engagementOnly  (NOT publicly scrapeable; the A→B layer)

The panel (Ellis, Drucker, Damodaran) flagged these as the data that actually proves wealth creation but cannot be scraped. They are never asserted in the public profile; the colophon names them as what an engagement establishes.
- **retention**: reorder / repeat-purchase rate, dealer retention across seasons (Ellis)
- **customerValue**: who the customer is and what they value, yield / cost / reliability / region-fit (Drucker)
- **trueUnitEconomics**: margin by variety or crop, cost-to-serve per dealer (Damodaran)

The schema is therefore **two-tier**: A-D are scrapeable and drive the public profile; E is the engagement tier and is the case for the conversation, not a public claim.

---

## The Hx grid IS the organizing spine (v6.0 — the holistic-view insight)

The data infra is **not** a flat company/segment table that P5 happens to read at the end. The value chain (**H5 Offers → H4 Capability → H3 Capacity → H2 Customer experience → H1 Orders**) is the spine, and **every Hx carries its own elements.** Read all five rungs + the market + the financial outcome and you have the holistic company. **Every profile Part is a projection of this grid.**

**Per-Hx cell** (attempted for every horizontal; a blank cell is a *visible* data gap, never a silent omission):

| element | tier | feeds |
|---|---|---|
| `companyPractice` | A2 (grounded / operator) | P5 steps (theirs) |
| `industryNorm` | segment | P5 steps (generic scaffold, marked) |
| `marketContext` | segment / market | P2 (the market force acting on THIS rung) |
| `strength` (cornered resource, if located here) | A2 / operator | P1, P3 |
| `opportunity` { lever, statement } | derived | P3, P4 |
| `benchmark` { value, source } | segment | P1 / P3 |
| `source` | — | provenance |

**Projection map — each Part is a slice of the grid:**
- **P1 engine** = H4 ⊗ H5 (capability fused with offers = the R&D→PMF axis) + financial outcome
- **P2 market** = aggregate market sizing + the `marketContext` column read across H5..H1
- **P3 opportunities** = the `opportunity` column across H5..H1 (each already carries `hId` — the grid was leaking through all along)
- **P4 experiments** = one per `opportunity` cell
- **P5 workflows** = the full grid (companyPractice + industryNorm + spotted opportunity), H5→H1

**Consequences:**
- **Coverage is guaranteed.** The factory must attempt all five rungs; a missing rung shows as `needsInput`, not silence.
- **The strength pass lands somewhere specific.** The cornered resource sits ON an Hx (Pioneer: HMLV flexibility at H3+H4, design library at H5), so "where is the edge" has a typed answer.
- **The market is not a separate silo.** Market forces attach to the rung they act on (HMLV→H5/H1, sustainability premium→H5, China+1→H1, power cost→H3).
- This is the **PDGMS grid ontology (the horizontals) applied to the profile** — the simulation eating its own dogfood. The flat A/A2/B tables remain the raw *sources*; the Hx grid is the derived *structure* every Part renders from.

Worked grid: `data/pioneer.json` → `hxGrid`.

## The ownership × operating-status expansion (v7.0 — the 8-company hard-tail batch)

Eight companies (Western India Plywoods, Dey's Medical, Natural Dehydrated Vegetables, Hindustan Antibiotics, United Telecoms, Jyoti, O/E/N India, DMCC) were run clean-room. Result: 1 screen-out, 0 thriving engines, 7 borderline — and the borderline cases cluster in **unlisted / niche-component / distressed**, exactly where the listed-company assumptions fail. The single proof case is **HAL vs Jyoti**: identical balance-sheet distress (negative net worth, defaults), opposite verdicts (defunct screen-out vs live turnaround with a Navy sole-supplier moat). Distress decides nothing; operating momentum + retained capability decides. That forces TWO axes the schema lacked, and several evidence-model fixes.

**1. `ownershipType` (new axis — drives the financial SOURCE, not just availability):**

| ownershipType | financial source class | example |
|---|---|---|
| listed | Screener / BSE-NSE (clean) | DMCC, Jyoti, WIPL |
| unlisted-public | ROC / Tofler (partial) | Dey's, O/E/N, UTL |
| private | directory / press estimate or none | Natural Dehydrated Veg |
| government-PSU | Parliament answers, Dept disclosures | Hindustan Antibiotics |
| group-holding | multi-entity, no clean consolidated | UTL, NDV (Meghani group) |

**2. `operatingStatus` is descriptive context, not an eliminator.** operatingStatus (going-concern | sick/distressed | under-disinvestment | defunct/exited | asset-holding) tells the profiler the going-concern state so the story is honest; it never drops a company. Inclusion was already decided by the data infra on capability + market.

**The HAL/Jyoti read (capability, not distress, is decisive):**
- distress + declining-debt + **rising ops** + retained capability → tell it as a **turnaround** (Jyoti)
- distress + flat ops + asset-only → a **stored-shell** (watch; revisit when ops or capability return)
- capability dormant (production ceased) → the data infra simply hasn't surfaced it yet — **not eliminated, revisit if revived** (HAL)

**3. Financials are nullable/soft and NEVER gate classification.** 6 of 8 had absent/partial/unreliable financials. Add `financialsAvailability`: full | partial | estimate-only | none. The strength pass runs regardless. (Empirically forces the never-write-off rule: NDV, O/E/N, UTL would all wrongly screen-out on a financials gate.)

**4. The cornered resource is rarely scrapeable — model it as evidence + provenance + a proxy layer:**
- `corneredResource` { claim, type, source, claimCredibility: self-claimed | third-party | customer-attested | **qualification-gated**, confidence, needsOperatorVerify }.
- `qualifications[]` as a **proxy signal** for design-in / qualification lock-in (the moat invisible in filings): JSS/AS9100D/IATF (O/E/N), sole-Navy-approval (Jyoti), BRC/FSSC/Kosher/Star-Export-House (NDV), DST-recognized R&D, GOTS (Pioneer).
- **Heritage ≠ moat guard** (DMCC 1919, Dey's, HAL): founding year is a fact, not an edge, unless tied to retained share / relationships / IP.

**5. Relationship/contract is a first-class evidence type with DUAL polarity** (UTL: the BBNL contract is both the marquee win and a Supreme Court dispute): `contracts[]` { counterparty, type, polarity: win | dispute | both, source }.

**6. Niche/relative leadership, not absolute global share** (O/E/N <0.3% global but India #1): `nicheLeadership` { scope: india | regional | global, rank, basis }, separate from `marketSharePct`. Extend `shareIsMeaningful` to a **per-line `shareApplicable`** (DMCC/WIPL: commodity line share-irrelevant, specialty line relevant; the moat-bearing specialty revenue split is usually undisclosed → flag qualitatively).

**7. Cyclicality** (DMCC: sales +24% CAGR while PAT fell ₹33→7→27 on the chemical cycle): `cyclical: true` + peak-to-trough margin band + `cyclePhase`: trough | recovering | peak. A point-estimate `profitTrend` mis-reads a trough as decline.

**8. Entity resolution keyed on CIN, not name/ticker** (pipeline-integrity requirement). Name collisions seen: O/E/N vs FCI OEN Connectors (OENCONNECT), Jyoti Ltd vs Jyoti Structures, Dey's multiple CINs, UTL vs its listed sub Trigyn. Naive name/ticker scraping pulls the WRONG company's financials. Canonical `cin` + a dedup step.

**9. `upstreamDependency`** { input, controlled: bool, riskNote } (DMCC's boron "moat" is undercut by imported minerals — a strength on a fragile supply chain is not a clean moat).

**10. `revenueNature`: recurring | project-orderbook** + an `orderBook` field where lumpy (Jyoti, UTL: project revenue + ~220 debtor-days makes a P&L snapshot misleading).

**Net:** the schema goes from "a listed company in one clean segment with scrapeable financials and a scrapeable moat" to **a company of any ownership type, in any operating state, whose moat is usually a qualification/relationship/claim carried with provenance and confidence, whose financials may be null, and whose identity is a CIN.** The strength pass + never-write-off rule is what keeps the hard tail (where most real Hidden Champions live) from being wrongly screened out.

## Part → field map (a projection of the Hx grid, above)

- **P1 (engine):** revenueCr/revenuePrevCr (+growthPct), rdHeadcount/employees (+rdRatio), patents, certifications, products.varieties/crops, rd.*, distribution.states/dealers, recentMoves.
- **P2 (market):** segment.market (range), derived.marketSharePct, structureFacts, subSegments, adjacentMarkets (+lossSplit).
- **P3 (opportunities):** opportunities[] (rule output), each with evidence + source.
- **P4 (experiments):** opportunities[] → one experiment per opportunity, from an experiment-template library keyed by (lever, hId).
- **P5 (workflows):** company **execution intel (A2)** for the specific steps wherever grounded; segment.valueChain[] only as generic scaffold (marked) where A2 is missing; company facts woven at the matching step; opportunities mapped by hId. *Build order is P5 → P4 → P3; specificity here is what makes the whole bottom half credible.*

---

## The P1 narrative frame (capability-first; v5.0 — the Pioneer "don't write them off" sample)

**For PROFILING only — this picks how to tell the story, it never eliminates** (inclusion is the data infra's job). The first cut at Pioneer framed it `turnaround` off the P&L (profit ₹19cr→₹4.6cr, ROE 0.87%, 0.45x book). That is the **McKinsey-writes-them-off** failure: judging a company by its lagging financial readout and missing the capability that makes it valuable. The operator named the real story the scrape had missed: **Pioneer is a high-mix, low-volume (HMLV) manufacturer at scale** (300,000+ designs vs ~20,000 at a notable peer; 1.2B stitches; low-MOQ flexibility), and the market (fast fashion, SKU proliferation, China+1) is moving toward exactly that and *pays a premium for it* (low-MOQ → 30-50% better sell-through). The financials lag the capability; they do not define it.

**So generation runs a CAPABILITY/STRENGTH pass BEFORE the financial classification, and financials alone can never screen a company out.**

1. **Strength pass (first).** Find the cornered resource: the hard-to-replicate operational edge (HMLV-at-scale, design-library size, switching cost, a brand, a tech/process lead, a global niche position). This is mostly **A2 qualitative + operator input** — the highest-value strength is often NOT in filings (Pioneer's HMLV edge required the operator to name it). Capture in `corneredResource` + `capabilities[]`, and link to the **`demandTailwind`** (the market trend moving toward it, sized + buyer-value proof).
2. **Financial read (second).** Report the trends honestly (see below), but as *context for the capability*, never as the verdict.
3. **Classify.**

| `healthClass` | Trigger | P1 frame | Nucleus leans on |
|---|---|---|---|
| **engine** | profit up + healthy ROE (Eldorado) | "a wealth-creation engine" | financials |
| **forward-bet** | financials soft/down + credible tech/platform bet (SED) | "a deep-tech bet on the next curve" | tech-leadership, forward-bet |
| **capability-led** | financials lag, but a valuable, in-demand capability the market is moving toward (Pioneer) | "a [capability] maker, in a market turning its way; the margin hasn't caught the value yet" | capability-leadership, demand tailwind |
| **turnaround** | real stored assets/brand, financials lagging | "an asset base ahead of its margin" | stored-assets, brand |

**No `screen-out` here.** Inclusion is decided upstream by the data infra (`data-infra-spec.md`) on capability + market, and it never eliminates. By the time profiling runs, the company already qualifies; these labels only pick the P1 narrative frame. If the financials are weak, that is context for the story (capability-led / turnaround), never a reason to drop the company.

Disciplines that fall out of this sample:
- **Cornered resource + demand tailwind = the P1 spine for capability-led.** Lead with what they're built to do and the market moving toward it; report the weak numbers plainly *after*, framed as "the margin hasn't caught the value of the capability yet."
- **The flagship opportunity is "price the capability you're giving away"** (margin, `isCorneredResourceMove:true`) — the 7 Powers Cornered-Resource → Process-Power move. It leads P3 for capability-led companies.
- **Three trends, not one.** revenueTrend, profitTrend, marginTrend diverge; state the divergence honestly, never average into a growth story.
- **Commodity-share is the wrong metric.** When `shareIsMeaningful:false`, P2 says so and pivots to the niche where the capability pays.
- **Brand is a wealth asset** (`brand` object): a P1 line + a D2C velocity opportunity.
- **Highest cortisol risk lives here.** A financially weak company is exactly where a cocky verdict destroys trust. Strength first, numbers honest, verdict never.

**New data this archetype needs** (folds into the tiers above): `corneredResource` + `capabilities[]` (company A2, often operator-supplied); `demandTailwind` { trend, buyerValueProof, switchingCost, geographyWedge } (segment, amortizes); a `flexibility/specialty price premium` where obtainable. The factory therefore needs a **human/operator strength-pass hook** — the scrape alone will miss the cornered resource.

## Grounding economics & variable discipline (panel-reviewed v3.0)

**Cost is per-source, not per-field.** Collect only variables that change a sentence, but ground high-value ones deeply, these are companies we chase and will spend premium research on.

- **Segment tier amortizes.** peers, SRR/adoptionStructure, customerValue, valueChain, market, structureFacts are fetched ONCE per segment and reused across every company in it. Spend the premium research budget here; it pays back across hundreds of profiles.
- **Company tier stays lean.** Pull from one or two cheap sources (DRHP / filings + website). One DRHP fetch yields financials + IPO + mix together.

**Dropped (cost > value):**
- `ipo.leadManagers` — deal plumbing, changes no sentence.
- `financials.patMarginPct` — redundant with EBITDA margin + ROE + PAT growth.
- `countryStatesTotal` — a constant (28), not a scrape.
- `ipo.promoters` — keep only if the founder is a real signal (scientist / maverick), else drop.
- `financials.patCAGRpct`, `revenueCAGRpct` — derive at generation, do not scrape.

**Keep even when costly:** peers, customerValue, adoptionStructure (SRR), valueChain, full financials, IPO size, R&D depth (headcount/patents/certifications), dealers total+active, product breadth + mix.

---

## Discipline (carried from profile-spec.md)
- Every rendered fact traces to a field; no field, no sentence.
- **Descriptive prose (what they do, products, operations) renders ONLY from grounded descriptive fields.** An empty descriptive field is omitted or marked needs-input, never invented. Numbers alone let the model fabricate the narrative, so ground the description, not just the digits.
- **The nucleus reports the financial trend honestly (up / flat / down) and never assumes growth.** For down or cyclical companies (e.g. SED, FY25 down), it leans on the non-financial `wealthEvidenceType` (tech leadership, global niche position, customer-ROI, forward-bet), not on a growth story that isn't there.
- **Market is global by default.** Most targets are exporters; lead with world market + export footprint, treat domestic as a slice.
- **Every qualitative insight carries a `claimCredibility` tag (self-claimed | third-party | customer-attested) and a source.** Qualitative hallucinates easiest, so no unsourced qualitative, ever; self-claimed items are rendered as the company's claim, not as fact.
- Ranges shown where the segment has multiple sources.
- Voice is set at template time (Feynman-plain, Glaser on opportunities, journo-reported), not re-derived per company.
- Human-verify the dataset before publish (the no-fabrication gate is at the data layer, once, not per profile).

Company record: `data/eldorado.json`. Segment record: `data/segment-india-seeds.json`.
