# Hidden Champions Profiling — FDE Rollout Plan

### 2026-07-10 | for the FDE running profiling | everything you need is in THIS folder (`PDGMSDocs/hc-profiling/`)
### Companions here: `profile-generation-workflow.md` (the per-company runbook) · `fde-datafetch-plan.md` (Plan B, the data fetch) · `generation-spec.md` (how a profile is written) · `profile-fe-contract.md` (the JSON schema) · `example-eldorado-agritech.json` (a complete, valid example)
### Code: PDGMS-Backend `dev` (`feat(hc)`) · PDGMS-Frontend `main` (`feat(hc)`)

---

## What you are producing

A private, passcode-protected profile page for each company, live at
`{app}/p/hiddenchampions/{slug}`, plus the notification email the platform sends
for you. You never write the email and never handle the passcode: the platform
generates the passcode, picks the right email wording, sends it to the contact
with a copy to the BD rep, and logs everything.

**One identity rule: the website domain is how a company is recognized.**
Always supply the domain; never create companies by hand; never match by name.
The platform normalizes messy input (`https://www.AcmeCorp.in/about` →
`acmecorp.in`), finds the CRM record, or creates one if the domain is new.

---

## One-time setup (ask Tarun/dev once)

| Item | What you need |
|---|---|
| PDGMS account | Your login, with **org-manager** role (profile creation is a privileged action) |
| API token | Issued by the admin (NodeBB ACP → API Access), bound to your user. Keep it private; it acts as you. |
| Base URL | The backend URL, called `{api}` below. Dev: `http://localhost:4567`. Production: provided at go-live. |
| Org ID | Your organization id for the `X-Organization-Id` header. |

Every API call carries two headers:
```
Authorization: Bearer <your-token>
X-Organization-Id: <org-id>
```

---

## Case 1 — Target companies (you run the entire flow)

1. **Fetch the data** — Plan B, as you already do: one 38-column CSV row per company, every claim with its source.
2. **Generate the profile JSON** — run the workflow in Claude Code per `profile-generation-workflow.md` (this folder). Output: one contract-v3 JSON file per company. Do not set `meta.verified` until step 3.
3. **Verify** — check each fact against its source column. Then set `meta.verified: true`. Unverified JSON is rejected by the platform, by design.
4. **Upload:**
```
POST {api}/api/v3/pdgms/hc/profiles
Content-Type: application/json

{
  "domain": "companywebsite.in",
  "slug": "company-name",                     ← the readable URL slug, lowercase-hyphen
  "company": { "name": "Company Pvt Ltd", "industry": "…" },   ← used only if the domain is new to the CRM
  "contactId": 123,                            ← optional; see "who gets emailed"
  "profile": { …the JSON from step 2… }
}
```
5. **Read the response:**
```
{ "profile": {…}, "slug": "company-name", "password": "9f2c…", "email": { "sent": true|false, "ccTo": …, "error": … } }
```
   - `email.sent: true` → done; the contact has the link + passcode.
   - `email.sent: false, error: "no-contact-on-crm"` → normal for a company with no contact yet. The profile is live and waiting. When a contact is added to the company, send the first notification with:
```
POST {api}/api/v3/pdgms/hc/profiles/{profileId}/rotate-passcode
{ "contactId": <the new contact's id> }
```
     (The platform knows no email was ever sent and sends the proper introduction, not a "passcode changed" note.)
6. **30-second check:** open `{app}/p/hiddenchampions/{slug}`, enter the returned passcode, eyeball the five parts. The company should now be on the **Profiles** tab of `{app}/crm/hidden-champions` and off **Pending**.

**Who gets emailed, automatically:** if the company has profiling consent on record, the consented contact gets the *"thank you for agreeing"* email. If not, and you passed a `contactId`, that person gets the *"we came across your company"* email (it includes a take-it-down offer). If neither, nobody is emailed until you rotate with a contact.

## Case 2 — Blind-call companies (BD team gets consent first)

1. The BD rep, after the call, opens the company record in the CRM and records **profiling consent**: picks the contact who agreed and uploads the consent email screenshot. That is the rep's job, not yours.
2. The company appears on **your queue**: `{app}/crm/hidden-champions` → **Pending** tab (consented, no profile yet), with the contact, the consent date, and the screenshot link.
3. You run the same steps as Case 1 (fetch → generate → verify → upload). Use the domain; do not pass `contactId` — the consent decides everything, and the *consented* email goes out with a copy to the rep automatically.

---

## Errors you will see, and what they mean

| Response | Meaning | What you do |
|---|---|---|
| `invalid-profile-json …` (lists paths) | The JSON fails the contract; every failing path is listed | Fix those paths, re-upload. Common: missing `source` on a company/segment node, `meta.verified` not true, unmarked generic P5. |
| `profile-already-exists` | This company already has a profile | Don't re-upload; corrections go through the edit flow on the company record. |
| `slug-taken` | Another page uses that slug | Pick a different slug. |
| `company-block-required-for-new-domain` | New domain and you didn't send the `company` block | Add `"company": { "name": … }`. |
| `contact-not-of-company` | The contactId belongs to another company | Use a contact from this company. |
| `invalid-slug-format` | Slug must be lowercase letters/digits/hyphens, 3–80 chars | Fix the slug. |

## The other endpoints you may need

- `GET {api}/api/v3/pdgms/hc/dashboard` — your queue as data: `{ pending: […], profiles: […] }`.
- `GET {api}/api/v3/pdgms/hc/profiles/company/{companyId}` — one company's profile, page state, and edit history.
- `POST {api}/api/v3/pdgms/hc/profiles/{profileId}/rotate-passcode` — new passcode, re-sends the email (body `{ "contactId": … }` optional).

Corrections after the company replies are the **rep's** job (the edit panel on the company record; every edit is recorded with before/after). You only re-verify sources if the analyst view flags an edited node.

## Boundaries (the platform enforces these; don't work around them)

- No profile without `meta.verified: true` — the no-fabrication gate is the product.
- One profile per company. Corrections edit the live profile; they never re-upload.
- The passcode appears once, in the API response and the email. If it's lost, rotate; never store it anywhere.
- Consent screenshots and contact emails are personal data; they live only in the CRM.

## Go-live checklist (before the first real company)
- [x] HC migrations applied to production Supabase and DB-verified (2026-07-10).
- [x] `app_url` set to the production frontend domain.
- [ ] Deploy backend `dev` + frontend `main` (Swapnanil).
- [ ] FDE account: org-manager role + API token issued (Swapnanil → Amrutha).
- [ ] Dry run: one company end-to-end with the contact email pointed at DT, both cases (Amrutha + Swapnanil).
