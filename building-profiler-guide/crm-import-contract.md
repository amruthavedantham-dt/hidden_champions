# CRM import contract — what a profiler must emit

The CRM ingests profiler output through one endpoint. The file is uploaded by a logged-in manager in the UI (`/crm/companies` → "Import from profiler", paste or `.json` file); the profiler itself never calls the CRM — no URL, no token, no network config on the research side.

- **Endpoint:** `POST /api/v3/pdgms/crm/profiler-import` (admin/manager; the FE screen injects `offeringId` from a dropdown at upload time)
- **Validation:** Zod, `strict` at every level — **unknown keys reject the whole file**. Empty optional fields must be omitted, never sent as `""` or `null`.
- **Caps:** ≤200 companies per file · ≤30 claims, ≤20 contacts, ≤25 evidence, ≤3 alignment rows per company.

## The envelope (v1)

```json
{
  "schemaVersion": 1,
  "source": "hcp-profiler",
  "runId": "export-7-1785319086617",
  "exportedAt": "2026-08-01T10:00:00Z",
  "companies": [ { ...company objects... } ]
}
```

| Field | Rule | Notes |
|---|---|---|
| `schemaVersion` | literal `1` | |
| `source` | literal `"hcp-profiler"` | Historical protocol id — **every profiler sends exactly this string**, regardless of topic. Treat it as the wire-format name, not a topic label. |
| `runId` | string ≤200 | Shown on the intel card; make it unique per export run. |
| `exportedAt` | ISO datetime **with offset** (`Z` ok) | |
| `offeringName` | optional, **ignored** | Legacy; the offering comes from the upload screen's dropdown. Omit it. |
| `companies` | 1–200 items | One bad company is skipped with a reason; it never sinks the batch. |

## One company object

```json
{
  "identity": {
    "name": "Acme Industries Pvt Ltd",
    "website": "https://www.acme.in",
    "cin": "U12345MH2012PTC123456",
    "ownershipType": "private-limited",
    "sector": "industrial fasteners",
    "segmentRef": "india-specialty-fasteners"
  },
  "summary": "One-paragraph research summary of the company.",
  "triage": { "status": "auto-confirmed", "unresolvedPillars": [] },
  "claims": [
    {
      "pillar": "compliance",
      "claim": "Holds ISO 9001:2015 certification renewed in 2025.",
      "source": "https://registry.example/cert/123",
      "credibility": "registry-confirmed",
      "needsVerify": "no",
      "review": "Verified"
    }
  ],
  "evidence": [
    { "text": "Title: snippet or excerpt of a research source, up to 600 chars (the reference exporter ships ~400).", "source": "https://example.com/article", "pillar": "compliance" }
  ],
  "alignment": [ { "capability": "…", "need": "…", "pull": "strong", "source": "https://…" } ],
  "gap": { "latent": "…", "currentlyMonetized": "…", "summary": "…", "activationPath": "…", "source": "https://…" },
  "proof": { "type": "certification", "status": "claimed-verify", "source": "https://…", "pillar": "compliance" },
  "contacts": [ { "name": "R. Mehta", "designation": "Managing Director", "email": "r@acme.in", "phone": "+91 98xxxxxxx" } ]
}
```

### Field rules that reject files when broken

- `identity.name` — the only required field inside `identity` (≤300 chars). At company level, exactly two keys are required: `identity` and `claims`.
- `claims[]` — **required array** (may be empty). Each claim: `pillar` **free string** 1–120 (any topic's taxonomy works), `claim` ≤2000, `credibility` ∈ `registry-confirmed | qualification-gated | third-party | self-claimed`, `needsVerify` ∈ `yes | no`, optional `review` ∈ `Pending | Verified | Rejected`, optional `source` — **must be a real URL** (a hand-typed "company brochure" rejects the whole file; omit non-URLs), optional `moatType`/`moatDurability` strings.
- `evidence[]` — optional, ≤25 × `{text 1–600, source? URL, pillar? ≤120}`. This is the research corpus behind the claims; it is what makes generated profiles rich. Ship it.
- `gap` / `alignment` / `proof` — optional structured extras (field names above are fixed). Omit entirely when the topic has no use for them.
- `contacts[]` — optional; each needs `name`; `email`/`phone`/`designation` optional.
- `triage` — optional, but when present BOTH keys are required: `status` ∈ `auto-confirmed | needs-review` AND `unresolvedPillars` (array, may be empty, ≤20 items × ≤200 chars — omitting it rejects the file). Rides the stored raw only.

## What the CRM does on import

- **Offering** resolves from the dropdown's id first; failure aborts the batch before any write.
- **Company matching:** by normalized bare-host domain (from `identity.website`) first, then case-insensitive exact name. Existing company → fields update, except any field a human edited in the CRM (human edits always win). New → created with source `hcp-profiler`. Re-importing the same file creates no duplicate companies or contacts, but each import appends one more intel row per company (insert-only history), and matched companies count as `updated` even when nothing actually changed.
- **Contacts:** deduped within the company by email, else phone, else exact name; created under the upload's offering (contacts require an offering).
- **Intel:** ONE new intel row per company, provider `profiler`, insert-only history. `raw` = the untouched company object (+ runId/exportedAt); `canonical` = the generation-facing shape.
- **Held-claims policy:** `review: "Rejected"` → kept in raw only, never generation-visible. `needsVerify: "yes"` without `review: "Verified"` → stored as *held* (visible on the record, dimmed, excluded from generation). Everything else → live claims the generator may cite.
- **Response:** `{ created, updated, contactsCreated, intelRows, skipped: [{name, reason}], offeringId, fieldSkips }`.

## Minimal viable company

For a topic with no structured extras, this is a fully valid, generation-ready company:

```json
{
  "identity": { "name": "Acme Industries", "website": "https://acme.in", "sector": "fasteners" },
  "summary": "…",
  "claims": [ { "pillar": "anything-you-like", "claim": "…", "credibility": "third-party", "needsVerify": "no" } ],
  "evidence": [ { "text": "…", "source": "https://…" } ]
}
```

Claims + evidence are the universal backbone. Everything else is optional garnish.
