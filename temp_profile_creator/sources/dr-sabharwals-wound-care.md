# Dr. Sabharwal's Wound Care — sources for verification

**✅ Identity RESOLVED (2026-07-18, analyst-confirmed).** The entity behind
drsabharwal.co is **Dr Sabharwal's Wound Care Private Limited**, CIN
`U21002HP2024PTC010734`, incorporated 13 March 2024, registered address in
Baddi, Himachal Pradesh — matching the factory address on the website. Per
[Falcon Ebiz](https://www.falconebiz.com/company/DR-SABHARWALS-WOUND-CARE-PRIVATE-LIMITED-U21002HP2024PTC010734)
(citing MCA records), this is a **recent conversion from proprietorship to
Pvt Ltd** — explains why the site's GST is still tied to an individual PAN
(Mr. Manish): the new company PAN/GST likely hasn't propagated to public
aggregators yet, being under 2 years old. **Consequence: neither of the two
older entities below (Medicals Pvt Ltd, Manufacturing Labs Ltd) is this
company** — they're other units of the same family group, not this one.
Their financials, CINs, and history do NOT apply here.

**Original (now superseded) identity confusion, kept for the record:**
"Dr. Sabharwal's" is a family-run group brand with **multiple domains**
(drsabharwal.co, .com, .net, .co.in) and **multiple distinct legal entities**
turning up under near-identical names:

1. **Dr. Sabharwal's Medicals Private Limited** — CIN `U74899DL1986PTC137445`,
   incorporated 17 Dec 1986, Delhi, Private company.
   Source: [ZaubaCorp](https://www.zaubacorp.com/DR-SABHARWAL-S-MEDICALS-PRIVATE-LIMITED-U74899DL1986PTC137445)
2. **Dr. Sabharwal's Manufacturing Labs Limited** — a Public company,
   incorporated 24 Dec 1984. **Two different CINs appear for this same name
   across sources**: `U74899DL1984PLC137444` (one ZaubaCorp page, Delhi) vs.
   `U74899CH1984PLC044526` (Tofler + a second ZaubaCorp page, registered
   address Chandigarh). A third variant, `L74899DL1984PLC137444` (note the
   "L" prefix — normally denotes a *listed* company, unlike the "U" on the
   others), showed up on a third aggregator. This is either an aggregator
   data error somewhere, or genuinely two different registered entities —
   **not resolved.** Directors: Ajit Rai Sabharwal, Anjana Sabharwal (both
   42-year tenure — likely the founders), Dhruv Sabharwal, Prem Nath, Archita
   Sabharwal — a family-run structure.
   Source: [ZaubaCorp #1](https://www.zaubacorp.com/company/DR-SABHARWAL-S-MANUFACTURING-LABS-LIMITED/U74899DL1984PLC137444), [ZaubaCorp #2](https://www.zaubacorp.com/DR-SABHARWAL-S-MANUFACTURING-LABS-LIMITED-U74899CH1984PLC044526), [Tofler](https://www.tofler.in/dr-sabharwal-s-manufacturing-labs-limited/company/U74899CH1984PLC044526), [Falcon Ebiz](https://www.falconebiz.com/company/DR-SABHARWAL-S-MANUFACTURING-LABS-LIMITED-L74899DL1984PLC137444)
3. **The website you gave me (drsabharwal.co)** — WebFetch of this exact
   domain returned GST `02AFRPS9185G1ZU` and lists **"Mr. Manish (Proprietor)"**
   as the contact, at the Baddi, Himachal Pradesh factory. The GST number
   embeds a PAN (`AFRPS9185G`) whose 4th character is **"P" — Individual/Person**,
   not a company PAN. This suggests the operating unit behind *this specific
   website* may be a proprietorship (or a factory-level GST registration),
   **not** the same legal entity as either Ltd/Pvt Ltd company above — though
   very plausibly still part of the same family group/brand.
   Source: WebFetch of https://www.drsabharwal.co/

**This needs a human check, not another search** — ideally: ask the company
directly (on a follow-up call) which legal entity actually invoices/contracts
under drsabharwal.co, or check MCA's own master data (not aggregators) for
the real, current CIN. Don't let the profile assert financials or a CIN for
this company until this is sorted — same failure mode as O/E/N vs OENCONNECT
in the main HVT tool.

## What's true regardless of which entity — company/product facts
(from the drsabharwal.co WebFetch + the group's own drsabharwal.com About page)
- Group established 1984 ("Dr. Sabharwal's Group"), ~1986 for at least one
  of the registered entities above.
- Products: surgical dressings, speciality bandages, adhesive/transdermal
  pain patches, surgical tape, hand sanitizers, liquid antiseptics, eye pads,
  knee caps, canula fixing strips. Named products: "Chloro Tulle Dressing
  BP," "Elastic Adhesive Bandage," "Nuvlon-D" antiseptic wipe, "Excel Pore
  Plus" surgical tape.
- Manufacturing: "two full-fledged production facilities" (per drsabharwal.co)
  vs. "3 Factories" (per a separate search summary) — another minor
  inconsistency, not resolved.
- Export: claimed presence in 40-50 countries (varies by source), including
  USA, GCC countries, Turkey, Malaysia, Ethiopia; US FDA registered.
Credibility: self-claimed (company's own site + directory listings).
needs_verify: yes.

## Differentiation
**Claim:** "State of the art R&D has developed innovative Transdermal drug
delivery patches, Bandages, Plasters & Surgical dressings in various sizes &
shapes." More specific than a generic R&D claim — names an actual product
category (transdermal patches) as an R&D output.
Credibility: self-claimed. needs_verify: yes. No patent or DSIR registration
found in search — same as any other unconfirmed claim, this is `unresolved`,
not `commodity` (no positive sweep confirming absence).
**Claim (superlative, needs the same scrutiny as any "first/only" claim):**
"First to achieve ISO 9002 in 1997, then ISO 9001:2000" — an exclusivity-type
claim (being first), self-claimed, needs_verify: yes.

## Moat
**Claim:** ISO 9001, **ISO 13485** (medical-device-specific QMS — a real,
industry-meaningful certification, more relevant here than for a generic
manufacturer), GMP, GLP, WHO GMP, COPP (Certificate of Pharmaceutical
Product), SA8000 (social accountability), **US FDA audited**.
Credibility: self-claimed (company site + directories); **not yet checked
against a primary registry** the way Slidewell's ISO status was checked on
IAF CertSearch — same verification path is available here (search
"Sabharwal" on iafcertsearch.org) and should be run before trusting any of
these as current.
**Claim:** "Awarded five times for excellence in Exports by Government of
India" via Chemexcil (Chemical & Allied Products Export Promotion Council —
a real Indian government-affiliated export promotion body). Checkable if
Chemexcil publishes award records; not yet checked.
No CDSCO (India's medical-device regulator) registration was found in
search — worth checking directly on CDSCO's MD Online portal
(cdscomdonline.gov.in), since a wound-care/medical-device manufacturer
selling in India would need a CDSCO license.
Credibility: self-claimed. needs_verify: yes. proof_status: not-found.

## Product improvement
Same transdermal-patch R&D claim as above — no separate independent evidence
found. Credibility: self-claimed. needs_verify: yes.

## Alignment
- Capability: ISO 13485/US-FDA-audited medical-device manufacturing at
  export scale → Need: global wound-care/medical-device buyers requiring
  certified suppliers. Pull: strong (inferred; not yet grounded against a
  market report).
- Capability: transdermal patch R&D → Need: growing transdermal drug-delivery
  demand generally. Pull: not yet sized — segment research (next step) should
  ground this.

## Execution gap
Not enough to state responsibly yet — blocked on the identity question above.
Once the right entity is confirmed, the financial trend (see below) suggests
a real story: profit growing far faster than revenue (or even as revenue
falls), which usually means a cost/mix story, not a demand story. Needs the
right entity's real numbers before drafting `gap_summary`.

## Financial snapshot (tentative — tagged to Dr. Sabharwal's Manufacturing
Labs Limited, CIN U74899CH1984PLC044526, Chandigarh — NOT confirmed as the
entity behind drsabharwal.co; treat as provisional until identity is resolved)
- Net profit: **+190.59% YoY**
- Total revenue: **−6.49% YoY** (declining, not growing)
- Net profit margin: 7.03%
- ROE: 7.53%
- Authorized capital ₹1.5 Cr, paid-up ₹80 lakh
- Exact revenue/profit amounts paywalled on Tofler (only % changes visible)
Source: [Tofler](https://www.tofler.in/dr-sabharwal-s-manufacturing-labs-limited/company/U74899CH1984PLC044526)

## Segment
Medical devices / wound care & first-aid consumables (surgical dressings,
transdermal patches, bandages) — India export-manufacturing. Segment-tier
research not yet built.

## Unresolved
- **Which legal entity actually operates drsabharwal.co** — the single
  biggest open item, affects every other field including financials and CIN.
- ISO/GMP/FDA/Chemexcil claims — not yet checked against a primary registry
  (IAF CertSearch, US FDA database, Chemexcil) the way Slidewell's ISO status
  was.
- No CDSCO registration found — worth a direct check.
- No patent/DSIR evidence found — differentiation/product-improvement
  `unresolved`, not commodity.
- Minor factual inconsistencies across sources (2 vs 3 factories; 40 vs 50
  countries) — low-stakes, not worth resolving unless it becomes relevant.
