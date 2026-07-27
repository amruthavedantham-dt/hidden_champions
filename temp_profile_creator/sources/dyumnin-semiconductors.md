# Dyumnin Semiconductors (OPC) — sources for verification

## CEO-provided update (2026-07-24)
Source: a direct, on-record account from CEO **Vijayvithal Jahagirdar** —
[LinkedIn](https://www.linkedin.com/in/vijayvithal/) and a company YouTube
video he pointed to: [youtube.com/watch?v=XgEGejaDvfc](https://www.youtube.com/watch?v=XgEGejaDvfc)
(auto-generated transcript; several product names/terms are ASR-garbled —
flagged below as unconfirmed rather than guessed at). Per this project's
own RECIPE.md discipline, this is real founder-provided intel beyond
consent — `researchDepth` upgraded to `pursuit` in the company JSON. It is
still a company-side account (the founder describing his own company), so
credibility/needs_verify tags below follow the same rule as any other
operator claim — upgraded confidence over anonymous marketing copy, not
treated as independently audited.

## Identity
- Legal name: **Dyumnin Semiconductors (OPC) Private Limited** — "OPC" =
  One Person Company, a real, simplified Indian corporate structure for
  solo founders (explains the very small capital base below).
  CIN: `U72900KA2018OPC116057`, incorporated 5 Sept 2018, ROC Bangalore.
  Registered address: Vidyaranyapura, Bangalore — matches the company's
  Bengaluru location claim. Email on record: soumya@dyumnin.com.
  Source: [Tofler](https://www.tofler.in/dyumnin-semiconductors-opc-private-limited/company/U72900KA2018OPC116057), [ZaubaCorp](https://www.zaubacorp.com/company/DYUMNIN-SEMICONDUCTORS-OPC-PRIVATE-LIMITED/U72900KA2018OPC116057), [IndiaFilings](https://www.indiafilings.com/search/dyumnin-semiconductors-opc-private-limited-cin-U72900KA2018OPC116057) (analyst-confirmed)
- **Worth noting, from IndiaFilings**: the last balance sheet on record is
  dated **31 March 2019** — i.e., the most recent MCA filing indexed there
  is for the company's first year. This sits in some tension with the
  Tracxn revenue figure below (FY2021) — either a later filing exists that
  IndiaFilings hasn't indexed, or Tracxn sourced its figure differently.
  Not resolved; worth being aware of rather than asserting current
  compliance status confidently.
- Founded 2016 per Tracxn (by Vijayvithal Jahagirdar and "Dyumnin T" —
  likely a family name the company itself is named after, common
  practice), vs. legal incorporation in 2018 — same founding-vs-
  incorporation gap pattern seen elsewhere in this project.
- Director on record: Soumya Bharathi Vijayvithal Jahagirdar. Per the CEO's
  2026 video, her role is strategic planning and future products; described
  as an accomplished communicator with extensive networking in the
  **medical community** — confirmed directly by the CEO on 2026-07-24 as
  correct (not an ASR error, despite sitting oddly next to a semiconductor
  company).
- Capital: ₹1 lakh authorized/paid-up — very small, but normal and
  expected for an OPC structure, not itself a red flag.
- MCA classification: "Other Computer Related Activities" — a generic
  bucket; not unreasonable for a semiconductor IP/design services company
  even though it doesn't name the industry specifically (unlike Nav
  Bharati's genuinely wrong "ayurvedic" classification, this one is just
  imprecise, not incorrect).

## Differentiation — real technical service offering, some independently confirmed
- **Claim**: ASIC and FPGA design services — RISC-V processors, AI/ML
  hardware acceleration, networking, PCIe IP, System-on-Chip (SoC) design.
  Proprietary IP named: High-Frequency Trading (HFT) IP, a Register
  Abstraction Layer (RAL) tool, reference SoC designs, an "Interconnect
  Generator" (protocol-agnostic AXI/OCP support). This is a genuine,
  specific, technically plausible B2B services/IP-licensing offering — a
  different business model from any other company profiled in this batch
  (a design consultancy/IP boutique, not a manufacturer).
  Credibility: self-claimed (company site). needs_verify: yes for the
  specific IP claims, though the general service category is plausible
  given the confirmed open-source work below.
- **CONFIRMED, independently, via GitHub (analyst re-confirmed active)**:
  `github.com/dyumnin` and the `Dyumnin-Interns` organization have real,
  live, public repositories — notably **cocotb-ralgen** (a SystemRDL-to-
  raltest converter for cocotb, a genuine, well-known open-source
  hardware-verification framework used across the semiconductor industry).
  This is actual, checkable code, not a claim — a real, unusually strong
  technical credential for a company this small.
  Source: [github.com/dyumnin](https://github.com/dyumnin), [github.com/Dyumnin-Interns](https://github.com/Dyumnin-Interns), [cocotb-ralgen](https://github.com/dyumnin/cocotb-ralgen)
- **Founder credentials — independently confirmed, stronger than the
  claim originally checked.** A claim citing a specific quoted AMD/Xilinx
  community forum post from 2018 could **not** be independently found —
  that specific piece stays unconfirmed. But separate, real evidence
  turned up: founder **Vijayvithal Jahagirdar has his own personal GitHub**
  (`github.com/jahagirdar`); he was previously a **Design Lead at Texas
  Instruments**, focused on processor memory interface verification (a
  genuine, large-company technical background directly relevant to this
  company's specialization); and he gave a **public cocotb tutorial in
  October 2022**, published as videos. These are independently checkable
  facts that support the same conclusion (real, community-visible
  technical credibility in cocotb/verification) through better evidence
  than what was originally cited.
- **CEO's own account, on-record (2026 video + LinkedIn):** Jahagirdar
  describes his pre-Dyumnin career as spanning **Intel, LSI, and Texas
  Instruments** (not TI alone), "a veteran in the semiconductor domain with
  contributions to dozens of multi-million-gate ASICs" across process
  nodes from **180nm to 6nm**, plus unspecified papers and publications.
  First-person, on-record (his LinkedIn corroborates his identity), stronger
  than an anonymous claim — but the specific ASIC count and publication
  list were not independently checked, so this stays self-claimed +
  needs_verify: yes on the specifics.
- **Real, specific service pages confirmed on the company's own site**:
  dedicated pages for "Cocotb Verification Services" and "Custom FPGA
  design services," plus a claimed technology footprint across
  Xilinx/AMD FPGA families (Virtex, Kintex, Artix, Zynq, Ultrascale) —
  specific and plausible, self-claimed but consistent with the
  independently-confirmed GitHub/founder background above.
- **Superlative claim, needs the same scrutiny as any "pioneer" claim**:
  homepage describes the company as "Pioneering ASIC & FPGA Design
  Solutions" — self-claimed, needs_verify: yes.
- **Per the CEO's own account (2026 video), the service/product line is
  broader than the current site documents.** Full lifecycle: chip
  architecture, algorithm modeling, verification, RTL coding, synthesis,
  timing closure, pre-silicon validation, post-silicon validation, firmware
  development — for early-stage startup clients specifically. Named
  lines, checked against the current site (dyumnin.com/, /products) via
  WebFetch on 2026-07-24, none of which currently appear there. Product/
  partner names below were confirmed directly by the CEO on 2026-07-24
  after the auto-transcript initially garbled them (corrections in
  parentheses):
  - **Dikpalaka** — a perimeter security system, for industrial and
    defense applications (transcript originally rendered this "Dick
    Palaka... a 52 node perameter security system"; confirmed correct
    name is Dikpalaka: Perimeter Security System — no specific process
    node was actually stated, that was a mishearing of "perimeter").
  - A RISC-V server chip targeted at the data center market.
  - Various ARM-based SoCs for embedded-systems markets.
  - **HFT-NIC : FPGA Platform** — an FPGA-based high-frequency-trading
    platform (transcript originally rendered "hft Nick and fpga based...";
    confirmed correct name is HFT-NIC : FPGA Platform). The specific stock
    exchange it targets is still unconfirmed (transcript: "NSC" — possibly
    NSE — not corrected by the CEO, still needs_verify: yes).
  - EDA tools, reference designs, and a growing IP list — consistent with,
    and possibly restating, the already-confirmed reference-design/RAL
    work above.
  - A silicon-advisor role for **Simula.ai**, an AI company Dyumnin
    supports on graph AI and hyperdimensional-computing ("hypervector")
    methods (transcript originally rendered "simula do ai"; confirmed
    correct name is Simula.ai).
  - RISC-V ISA extensions with AI-specific instructions/accelerators for
    edge AI and TinyML applications.
  Credibility: self-claimed (CEO interview, names confirmed by CEO
  directly). needs_verify: yes for the substance/existence of each
  product and the Simula.ai advisory relationship — the general shape of
  the claim (a wider IP/services portfolio than the public site shows) is
  a first-person, on-record statement, not marketing copy, but still
  unaudited; only the exact names have been confirmed, not independently
  verified against a second source.
- Markets, per the CEO: Asia (especially India), US, and Europe. No named
  clients in any market independently confirmed.
- Design-Reuse.com supplier listing — the specific URL found in search
  returned a 404 (page not found). Could be a dead/outdated link rather
  than proof no listing ever existed; not confirmed either way.
- Silicon Hub vendor listing (siliconhub.ai) — a real semiconductor
  vendor-directory platform; the listing itself not independently opened/
  confirmed in this pass.

## Moat
No certifications (ISO or otherwise) found or claimed anywhere. This is
`unresolved`, not `commodity` — the real, GitHub-confirmed open-source
contribution work is arguably the closest thing to a moat signal here:
technical credibility earned in public, checkable by any potential client
directly, rather than a claimed certification.

## Product improvement
Same as differentiation — the cocotb/RAL tooling work is real, ongoing,
technical development, confirmed via GitHub commit history existing at
all (not fully audited for recency/activity level in this pass).

## Alignment
- Capability: ASIC/FPGA design + RISC-V/AI/networking IP → Need: fabless
  semiconductor companies and chip designers needing outsourced design/
  verification expertise. Pull: plausible; India's growing semiconductor
  design services sector is a real, named trend, not sized specifically
  for this company here.
- This is a B2B services relationship business (design-in/consulting wins
  with fabless chip companies), not a product-shipment business — alignment
  here is about winning named client engagements, not market share.

## Execution gap
Genuinely hard to assess — no financials are available at all (see below),
and the real story (if any) is in client wins and technical reputation,
neither of which is independently confirmable from public sources beyond
the GitHub work already noted.

## Financial snapshot — one real data point, one source rejected as hallucinated
- **Tofler explicitly states**: "Tofler currently has no financial reports
  for this company due to a lack of available information."
- **A separate part of the same fetch then presented specific percentage
  figures (revenue -6.49%, net profit +190.59%, margin 7.03%, debt/equity
  0.18) — these are REJECTED.** They are identical to figures the same
  fetch tool produced for a completely unrelated company (Konwert India
  Motors) earlier in this project — a clear case of the tool reusing/
  hallucinating cached data rather than reporting real numbers for this
  company. Do not use any of these figures.
- **One real, analyst-confirmed data point: Tracxn shows revenue of ₹15.5
  lakh for the year ending 31 March 2021.** This is plausible for a tiny
  OPC services shop, and internally consistent (not suspiciously round or
  repeated elsewhere in this project). Caveats: it's a single year with no
  trend, it's dated (FY2021, several years old), and it sits in tension
  with IndiaFilings showing no balance sheet filed after FY2019 (see
  Identity section) — not resolved which record is more current.
- **CEO Vijayvithal Jahagirdar states directly, on-record: annual company
  earnings of ₹1 crore+.** A materially higher, more current figure than
  the FY2021 Tracxn data point (several years apart, and possibly on a
  different basis — gross billings vs. net, self-reported vs. audited).
  This is the strongest financial signal on the company so far — a named
  founder's own on-record statement, not a marketing claim or third-party
  estimate — but it remains self-claimed and unaudited, so treat it as a
  lead (needs_verify: yes) rather than a confirmed figure.
- No employee count available from any source checked. Given the OPC
  structure and ₹1 lakh capital base, this is very likely a small,
  founder-plus-a-few-collaborators operation — consistent with the
  GitHub "Dyumnin-Interns" org naming.

## Segment
Semiconductor design services / IP licensing (fabless ASIC/FPGA design,
India). A different tier of the value chain from any other company in
this batch — a technical services boutique, not a manufacturer. Segment-
tier research not yet built.

## Resolved this session (2026-07-20)
- GitHub activity — analyst-confirmed active/real
- Financials — one real data point found (₹15.5L revenue, FY2021), one
  hallucinated source rejected
- Founder technical background — independently confirmed (ex-TI Design
  Lead, personal GitHub, a real 2022 cocotb tutorial), stronger evidence
  than the specific forum quote originally checked (which could not be found)

## Resolved this session (2026-07-24)
- Founder career background expanded: CEO's own on-record account adds
  Intel and LSI to Texas Instruments, plus a multi-million-gate-ASIC /
  180nm-6nm track record and unspecified papers/publications
- Director Soumya Bharathi's role clarified: strategic planning and future
  products, per the CEO
- A materially higher, self-reported revenue figure surfaced (₹1Cr+/yr,
  CEO on-record) — not a replacement for the FY2021 Tracxn figure, but a
  stronger, more current (if unaudited) data point
- Client geography clarified: Asia (India), US, Europe, per the CEO
- A much broader product/IP portfolio was described by the CEO than the
  public site currently documents (see Differentiation section) — several
  specific names ASR-garbled and flagged unconfirmed rather than guessed

## Still unresolved
- Design-Reuse.com listing — analyst found no solution/confirmation either way
- Silicon Hub listing — not independently opened/confirmed
- "Pioneering" claim — best read as fair for the verification-methodology
  angle specifically (Python/cocotb-based open-source verification), not
  for hardware design generally — a nuanced, not blanket, claim
- No patents, DSIR, or certifications found
- Employee count — unknown
- The specific tension between IndiaFilings' last-balance-sheet date
  (FY2019) and Tracxn's FY2021 revenue figure — not resolved
- Product/partner names confirmed by the CEO on 2026-07-24: Dikpalaka
  (perimeter security system), HFT-NIC : FPGA Platform, Simula.ai (AI
  advisory client), and that "medical community" was transcribed
  correctly. Still open: the exact stock exchange the HFT-NIC : FPGA
  Platform targets (transcript: "NSC," not corrected — possibly NSE)
- CEO-stated ₹1Cr+ revenue and product-portfolio claims — self-reported,
  not independently corroborated (names are now confirmed correct, but the
  underlying substance of each product/relationship is still unverified)
