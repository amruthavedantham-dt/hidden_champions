# Hidden Champions Data Infra — the Engine-Characterization Model

### Program: dt-ICP-publicprofile | 2026-06-30 (v2.0)
### Purpose: characterize the wealth-creation engine (or its potential) for a PRE-QUALIFIED population. It does not gatekeep, grade, or eliminate.

---

## What this is, and what it is NOT

- **The population is pre-qualified.** An upstream project already filtered ~1,100 companies *with potential* out of ~12,000. The data infra never sees the other ~10,900, so it is **not a gatekeeper** — no screen-out, no pass/fail, no financial gate. Financial weakness, distress, small size, private/unlisted status, missing filings, a down year — none of these are eliminators (they were removed).
- **Its job is to characterize the wealth-creation engine** so we know what to do with each company: how much of the engine is present and verified, and how big the execution gap is.
- **It is NOT profiling.** Generating the P1–P5 article (voice, narrative, wealth read, FE contract, the rendered page) is a separate project (`generation-spec.md`, `profile-spec.md`, `profile-fe-contract.md`) that consumes this infra's output.

---

## The wealth-creation engine model

**The engine is a causal chain (Damodaran), not a checklist.** Capture the chain and the gap, or you describe the company, not its engine:

```
DIFFERENTIATION → protected by a MOAT → kept current by PRODUCT-IMPROVEMENT CAPABILITY → ALIGNED to a market need → wealth
                                                                                                  ↑
                                         the wealth lives in the ALIGNMENT, and the upside lives in the EXECUTION GAP
```

The four pillars + the value field, each a first-class object carrying verification provenance (registry | primary | operator | web):

1. **differentiation** — what makes the offering non-commodity. A *positive* finding only; never inferred from price-led behaviour, never from web-silence.
2. **moat** `{ type: switching-cost | qualification-lock-in | IP | brand | integration | scale | network, durability: compounding | stable | eroding }` — typed and durability-rated, not an untyped "cornered resource." (An eroding brand-moat ≠ a compounding qualification-lock-in.)
3. **productImprovementCapability** — THE discriminator (Dey's failed here; O/E/N won here). Evidence: R&D-engine recognition (DSIR/registry), patents, NPD pipeline, the company's *history of product evolution*. "The ability to keep answering what the customer will value next" (Drucker). A heritage asset with no engine is NOT this.
4. **alignment[]** — an explicit RELATION, not a flag: each (capability/moat) → a specific market need/trend, with **pullStrength** (must-have | strong | nice-to-have, + direction). Alignment is PMF at the capability level (Ellis); store the vector, not just the endpoints.
5. **executionGap / leverageability** `{ latentCapability, currentlyMonetized, gap, activationPath }` — what the capability *could* do minus what it captures today. The wealth-*potential* signal AND the DT wedge; it operationalizes "even if not executing today, the capability can be leveraged" (Jyoti: distressed but capable; Pioneer: capable but under-priced).

---

## Evidence that fills each pillar

Capability is rarely in the financials; it must be sourced as evidence and mapped to the pillar it supports. Each piece:
`{ claim, fillsPillar: differentiation|moat|productImprovement, source, claimCredibility: self-claimed | third-party | customer-attested | qualification-gated | registry-confirmed, confidence, needsOperatorVerify }`.

- **differentiation / moat** — cornered resource, niche/scale leadership, manufacturing flexibility (HMLV-at-scale), design library (switching cost), integration, installed base, brand (Keo Karpin, Hakoba).
- **moat (qualification-lock-in)** — approvals as proxy for design-in lock-in: JSS / AS9100D / IATF (O/E/N), sole-supplier approval (Jyoti–Navy), GOTS (Pioneer). Note: generic export certs (BRC/FSSC/Kosher) are table-stakes, NOT a moat by themselves.
- **productImprovement** — DSIR/registry R&D recognition, patents, NPD pipeline, history of product evolution.

The highest-value evidence often must be named by an operator, not scraped — that is expected, not a disqualifier, but it is a *lead to verify* (see discipline).

## Market & alignment signals

- **Market sized GLOBAL by default** (most are exporters): the world market with a domestic slice, never India-only.
- **demandTailwind** — the trend moving TOWARD the capability (HMLV/low-MOQ demand; China+1; certified-sustainable demand), with the buyer-value proof. This is what `alignment[]` points the pillars at.
- **niche/relative leadership counts** even when absolute global share is tiny — a component maker at <0.3% global can still be the India #1 in its sub-category. Score relative leadership, not absolute share.

## Verification discipline (battle-tested — the NDV/UTL stress tests)

The differentiation/engine call is corruptible from four directions; guard all:

1. **An operator/self claim is a LEAD to verify, not a fact to record.** Identical skepticism to the operator, the website, and your own prior read. (Tested: an asserted "NDV has a DSIR R&D center" was deliberately false — it must not enter the analysis until a primary source confirms it. The same skepticism *upgraded* UTL only on independently-verifiable evidence: TEC approval, Ghosh's confirmed role.) The source never decides the call; the evidence does.
2. **Pillar proof usually lives in government registries / primary docs the public web does not surface** — DSIR Recognised In-house R&D Units, TEC GR/IR certificates, patent grants. Company sites and aggregators cannot settle it. Route to a registry / operator-verify step; carry a `differentiationProof` keyed to the registry source, with an explicit "registry-access-blocked → unresolved" state.
3. **Web-silence is not evidence of commodity** (a poorly-marketed differentiated company won't showcase its R&D) **— but neither is it evidence of differentiation.** Default to `unresolved`; never down-label to commodity on silence, never up-label on an unverified claim. A `commodity` label requires a *positive* finding: a genuinely fungible product AND a rigorous sweep (full-site + registry + search) that turned up no registry recognition, patent, proprietary process, or spec-lock (e.g. NDV).
4. **Surface positioning signals are inadmissible as capability evidence.** Price-led behaviour, lowest-bid tender wins, "competitive pricing" copy describe go-to-market, not the underlying capability.

## Identity & sourcing (find the right company and its data; never decides anything)

- **Entity resolution on CIN**, not name/ticker — avoid collisions (O/E/N vs the listed OENCONNECT, Jyoti Ltd vs Jyoti Structures, a holding co vs its listed sub).
- **ownershipType** (listed | unlisted-public | private | government-PSU | group-holding) — drives WHERE to look (Screener vs ROC/Tofler vs directory vs Parliament answers vs multi-entity group).
- **financialsAvailability** (full | partial | estimate-only | none) — a sourcing property, never a gate.

## Characterization output (not a verdict)

Per company, report how much of the engine is present-and-verified, and the size of the gap:
- **confirmed engine** — all four pillars present AND verified (registry/primary/customer-attested).
- **potential** — pillars present but ≥1 unverified → route to the verify step (the default state for most of the 1,100).
- **executionGap** — sized where possible; this is the opportunity, and the bridge to the profiling project and the engagement.

(No "rejected" bucket — the population is pre-qualified. A company where a pillar can't be found stays `unresolved`, pending registry/operator input.)

## Grounding cost (deeper per company; segment amortizes)

The population is pre-qualified, so spend on engine-anatomy depth, not a broad "does a market exist" screen:
- **Company tier:** capability/moat/product-improvement evidence + identity — a website/profile pass, plus the registry/operator step for the pillars that need verification. The pillar proof, not the financials, is the cost centre.
- **Segment tier:** market + demandTailwind + alignment context, fetched once per segment, amortized across every company in it.
- Financials are NOT required (this is a profiling cost, not a data-infra cost).

## The 8-company batch under the engine model

Scored on all four pillars + alignment (see `batch-8-classification.md` and `data/data-infra-batch8.json`):
- **Confirmed engine (2):** O/E/N (DST R&D lab + qualification lock-in, EV/defence aligned), Jyoti (engineering depth + sole-Navy approval, infra/defence aligned). [Pioneer, from the prior batch, sits here too.]
- **Potential, verify the third pillar (3):** United Telecoms (DWDM R&D currency), DMCC (specialty-chem R&D engine), Western India Plywoods (specialty-as-core).
- **Not an engine (3):** Dey's (brand asset, no product-improvement engine, faded alignment), Natural Dehydrated Vegetables (commodity — verified, incl. the false-DSIR stress test), Hindustan Antibiotics (capability dormant — revisit if revived).

## What lives in the (separate) profiling project, not here

`healthClass`/narrative frames, the wealth read prose, revenue/profit/margin trends, cyclicality, operating-status-as-story, P1–P5 mapping, the Hx-grid-as-article-spine, voice, the FE contract. The data infra carries the **four pillars + alignment + execution gap + identity** — and hands those to profiling.
