# Context: Hidden Champions HVT — Apps Script + Gemini build

Paste this whole file into Claude Code as the starting context. Build only what's asked for in §4 — do not build the full production pipeline (see §9).

---

## 1. What this project is

We're characterizing pre-qualified Indian manufacturers (already passed a separate revenue/manufacturer/PE-acquisition screen) against a four-pillar "wealth-creation engine" model: **differentiation → moat → product-improvement capability → alignment**, plus **execution gap** as the upside signal. This isn't a pass/fail score — every company here already qualified. The job is to characterize *how much of the engine is present and verified*.

The discipline that matters most: **an operator or website claim is a lead to verify, not a fact to record.** Nothing gets marked verified just because it's repeated across multiple websites — it needs an independent, registry-level source (DSIR, patent office, MCA, sector certification bodies) before it counts as confirmed.

This phase is a 5-company High-Velocity Test (HVT) of the method itself, not a production run.

---

## 2. What to build right now — scope boundary

**Build:**
- Two Apps Script functions, callable one at a time from the Script Editor or a custom Sheet menu
- Bound to a Google Sheet using the column schema in §3
- API keys read from `PropertiesService.getScriptProperties()` — never hard-coded

**Do NOT build:**
- Any orchestrator that loops across companies automatically
- Checkpointing / 6-minute-limit handling
- Circuit breaker / batch failure handling
- Caching layer

Those all exist in the production C1–C6 pipeline for a reason — unattended runs at ~1,100-company scale. At 5 companies, run manually, none of that applies. Building it now would be solving a problem this phase doesn't have.

---

## 3. Sheet column schema (one row per company)

```
company_name, cin, ownership_type, sector, segment_ref,
differentiation, differentiation_source, differentiation_credibility, differentiation_needs_verify,
moat_type, moat_durability, moat, moat_source, moat_credibility, moat_needs_verify,
product_improvement, product_improvement_source, product_improvement_credibility, product_improvement_needs_verify,
align1_capability, align1_need, align1_pull,
align2_capability, align2_need, align2_pull,
align3_capability, align3_need, align3_pull,
alignment_source,
gap_latent, gap_currently_monetized, gap_summary, gap_activation_path,
proof_type, proof_status, proof_source,
unresolved_pillars, notes
```

`credibility` values: `self-claimed | third-party | qualification-gated | registry-confirmed`
`needs_verify`: `yes | no`
`proof_status`: `not-found | claimed-verify | confirmed | registry-access-blocked`

---

## 4. The two functions to build

### `runSerperGrounding(companyName)`
- Fires Serper search+fetch queries, grouped by pillar:
  - **Differentiation**: `"<company>" patents`, `"<company>" DSIR`, `"<company>" "first in India" OR "only" OR "pioneer"`, `"<company>" proprietary technology`
  - **Moat**: `"<company>" certification OR approval OR AS9100 OR IATF OR GOTS`, `"<company>" sole supplier OR qualified vendor`
  - **Product improvement**: `"<company>" R&D center`, `"<company>" DSIR recognized`, `"<company>" new product launch`
  - **Alignment / gap**: `"<company>" export`, `"<company>" expansion OR hiring OR new facility`
- Writes each result's snippet + source URL into a staging area (a `RAW_EVIDENCE` sheet is fine — don't write directly into final columns yet)
- Does not judge anything — just grounds and stores

### `runGeminiStructure(companyName)`
- Reads the staged snippets for that company
- Sends them to Gemini with a system prompt that enforces:
  1. Only use facts present in the provided snippets — never add one
  2. Every claim proposed must carry which snippet supports it
  3. Default `credibility: self-claimed` unless the source is explicitly a third party independently reporting it (not just repeating the company's own words)
  4. Flag (don't resolve) anything that would need a registry check — DSIR, patents, MCA, sector certs — set `needs_verify: yes` and leave `proof_status: not-found`
  5. Never output `commodity` for differentiation unless the snippets show an explicit absence-of-differentiation finding, not just silence
- Writes its output as a **draft** into the final columns — you review and overwrite before it counts as final

**Non-negotiable output requirement:** every claim the function writes must carry its exact source URL in the adjacent `*_source` column — not just the claim text. Without the URL, there's nothing to verify against; you'd just be trusting Gemini's word for it, which is the exact failure mode this method exists to prevent. **Check this on the very first run, before looking at anything else** — open the URL next to the first claim and confirm the page actually says what the claim says.

**What "verify" means in practice for you, once this works:** you are not sourcing claims from scratch. The script finds candidate evidence and drafts the claim + source; your job is to open that source and confirm it says what's claimed, then decide if that source is good enough on its own or needs a registry check. The one exception — where you *do* go find something new yourself — is chasing the actual registry (DSIR list, IP India, MCA) for anything flagged `needs_verify: yes`, since Serper/Gemini can't reach those directly.

---

## 5. What stays manual — never automate these

- Registry checks themselves (DSIR recognized-units list, IP India patent search by assignee, MCA master data) — Gemini can only flag that one is needed
- Assigning the final `credibility` tier and `needs_verify` value after your own check
- The reasoning log (§7) — this is the actual deliverable, and automating it defeats the point

---

## 6. Company 1 — Spray Engineering Devices Limited (start here)

Seed data already gathered, so you're not starting from zero:

| Field | Value | Status |
|---|---|---|
| CIN | U00000CH2004PLC027625 | Resolved |
| Ownership type | Conflict: Private Ltd (IndiaFilings) vs Public Ltd/unlisted (Zauba, EMIS) | **Unresolved — check MCA master data directly** |
| Revenue | ₹460 Cr (Director's Report FY24-25) vs ₹462 Cr (Tracxn) vs >₹500 Cr (Tofler) | Near the 500 Cr ceiling — pin down before trusting the band |
| Differentiation | "100+ patented technologies," MVR-based Low Temperature Evaporation (LTE®) system, boiler-less sugar processing | `source: company site` · `credibility: self-claimed` · `needs_verify: yes` |
| Product improvement | "In-house R&D unit recognized by DSIR" | `source: company site, repeated by 2 aggregators, none independent` · `credibility: self-claimed` · `needs_verify: yes` · `proof_status: not-found` |
| Moat | Not yet gathered | Check ATUFS / Ministry of Textiles registration and any sole-supplier lock-in with sugar mills |

**First run checklist:**
1. `runSerperGrounding("Spray Engineering Devices Limited")`
2. `runGeminiStructure("Spray Engineering Devices Limited")` — compare its draft against the seed data above; it should independently reach roughly the same self-claimed/needs_verify calls
3. Manually check: DSIR recognized-units list, IP India patent search (assignee = Spray Engineering Devices), MCA master data for ownership type
4. Fill the reasoning log (§7) for each pillar
5. **Only once this run looks right** (Gemini's drafts are sane, prompts don't need major fixes) → move to company 2

---

## 7. Reasoning log template — fill per pillar, per company

```
Pillar: [differentiation / moat / product_improvement]
Claim: [one line]
Evidence checked: [every source touched, INCLUDING negative results —
                    e.g. "DSIR list checked, not found"]
Credibility tier assigned: [self-claimed / third-party / qualification-gated / registry-confirmed]
   → Why: [one sentence]
needs_verify: [yes/no]
   → Why: [one sentence]
Confidence: [High / Med / Low]
   → Why: [one sentence]
Conflicts found: [e.g. two sources disagree on ownership type]
   → Tie-break applied: [which source won, and why]
```

---

## 8. The other 4 companies — queue after SprayEDL passes

Don't touch these until SprayEDL's run is clean. Same two functions, same schema — no new code needed, just new company names:

| # | Company | What it's testing |
|---|---|---|
| 2 | Tatva Chintan Pharma Chem Ltd | Registry-backed positive control (listed, SEBI-disclosed) — does the method reach `confirmed` fast without over-verifying? |
| 3 | Sandstorm Equipment Co. | Private/unlisted, thin financials — unconfirmed via search, may turn out `financialsAvailability` isn't really "none" in practice |
| 4 | Jaishil Sulphur & Chemical Industries | Quiet/thin web presence but one real registry hit (OMRI organic listing) — does the method correctly credit it instead of defaulting to commodity? |
| 5 | Natesan Synchrocones Pvt. Ltd. | Different sector from SprayEDL (auto/aerospace precision components) — real Govt of India Technology Development Award to check |

---

## 9. Explicit non-goals (repeat, because it's tempting to over-build)

No `main.js`-style orchestrator. No automatic looping across the 5 companies. No checkpointing. No production error handling. This is you, running two functions by hand, reading the output, and doing the verification and reasoning yourself. The code's only job is to save you the copy-paste between a search tab and the sheet — not to make decisions.
