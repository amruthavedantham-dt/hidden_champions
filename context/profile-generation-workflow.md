# HC Profile Workflow — raw data → contract JSON → live passcode-protected profile

### 2026-07-10 | operational (every step below verified live on dev) | companions live in THIS folder
### SSOTs here: `generation-spec.md` (generation rules) · `profile-fe-contract.md` v3 (output schema) · `example-eldorado-agritech.json` (a complete, valid reference profile)
### Chain: Plan B CSV (FDE) → THIS WORKFLOW → profile live at `/p/hiddenchampions/{slug}` + CRM company + notification email

---

## The one identity rule

**Domain is the SSOT for company identity.** A company is recognized by its website domain, nothing else. The platform normalizes whatever it is given (`https://www.AcmeCorp.in/about-us` → `acmecorp.in`), matches the CRM by the `domain` field with a website-host fallback, and backfills `domain` onto records that matched by website. If no company matches, the platform creates one (`source: hc-profiling`). Never create a company by hand first; never match by name.

## What the platform does on upload (no workflow steps needed)

`POST /api/v3/pdgms/hc/profiles` with `{ domain, slug, company?, contactId?, profile }`:

1. Validates the profile JSON against contract v3 — rejects with **every failing path** (fix in one round trip). `meta.verified: true` is mandatory (the human no-fabrication gate).
2. Resolves the company by domain (creates it from the `company` block if new).
3. Rejects a second profile for the same company (one per company).
4. Creates the SharedPage (readable slug, system passcode) + the `hc_profile` row.
5. **Email decision, automatic:**
   - consent on record (rep captured it with screenshot) → **"created"** email: *thank you for agreeing*, link + passcode + corrections request, CC the mapped rep;
   - no consent but a `contactId` given → **"created-unsolicited"**: *we came across you, found it interesting*, public-sources disclosure, take-it-down offer;
   - no contact on the CRM at all → **no email**, response says `no-contact-on-crm`; the profile is live and waits.
6. Returns `{ slug, password, email }` — the passcode's only plaintext moment. If the email failed or was skipped, the analyst holds the passcode.

**Contact added later?** `POST /profiles/:id/rotate-passcode` with `{ contactId }` — if no email was ever sent, it sends the correct **create-variant** (not "passcode changed") with a fresh passcode.

---

## The workflow (per company, run in Claude Code)

**Inputs:** one Plan B CSV row (38 columns, source-tagged) · the segment CSV row · pursuit-pass qualitative intel (A2) if this is a company we chase.

1. **Normalize the domain** from the CSV's website column. This is the identity; everything else keys off it. Slug = readable kebab of the company name (e.g. `eldorado-agritech`).
2. **Map the CSV row → engine/company JSON** (Plan B §ingestion mapping: `align1/2/3` → `alignment[]`, `moat{type,durability}`, `sourcesByField` from source columns).
3. **Generate the contract-v3 profile JSON**, per `generation-spec.md`, bottom-up:
   - **P5 first** (workflow steps; A2 intel where grounded, else the segment's generic scaffold with `stepsTier: "segment"` + `flags.generic: true` — the validator enforces the marking);
   - **P4** experiments referencing P5 steps (`opportunityRef`);
   - **P3** opportunities those chase;
   - **P1/P2** attention layer from company + segment fields (P2 reuses the segment's locked insight set).
   - Every Node carries `tier / epistemic / source / fields`. Missing data → `flags.needsInput: true` (the renderer omits it) — **never invented**. `**…**` marks emphasis. Register: veteran business journalist — report, attribute, juxtapose; no adjectives, no verdicts.
   - Save as `{slug}.json` in your working folder, one file per company; it is also the upload body's `profile` value.
4. **Human verify** (Tarun or analyst): check each fact Node against its source column; only then set `meta.verified: true`. Interpretive tiers to double-check: `spotted` nodes are `derived` (DT's reading), not A2.
5. **Upload:**
   ```
   POST {backend}/api/v3/pdgms/hc/profiles     (authed, org context)
   { "domain": "<from CSV>", "slug": "<slug>",
     "company": { "name": "...", "industry": "..." },   ← used only if the domain is new to the CRM
     "contactId": <id>,                                  ← only if emailing a known contact without consent
     "profile": { ...contract v3 JSON... } }
   ```
6. **Post-checks (30 seconds):**
   - open `/p/hiddenchampions/{slug}`, enter the returned passcode, eyeball the 5 parts;
   - response `email.sent` true → confirm the log row on the company record; false with `no-contact-on-crm` → expected for a new company, add the contact when known and rotate;
   - the company shows on `/crm/hidden-champions` (profiles tab) and is off the pending list.

## Failure modes the platform catches for you
- Schema-invalid JSON → 400 with every failing path.
- `meta.verified` missing → rejected (no unverified content can go live).
- Generic P5 not marked → rejected.
- Duplicate company (by domain) → matched, not duplicated; duplicate profile → rejected.
- Slug taken → rejected (`slug-taken`); pick another.

## Ship-time status (2026-07-10 EOD)
- ✅ HC migrations applied to prod Supabase and verified (tables + enum + FKs).
- ✅ `app_url` set in prod config.
- ✅ Code pushed: backend `dev`, frontend `main`.
- Open: deploy + FDE account/token + joint dry run (see `fde-rollout-plan.md`).
