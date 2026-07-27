# Profile Generation — temporary working folder

**Status: temporary, ~1 week.** This exists so Amrutha can turn an already-run
HVT sheet row into a newsletter-ready company profile. No Apps Script, no
clasp, no menu items. It's this folder plus Claude Code doing the work
interactively, per `RECIPE.md`.

## How to use it

Paste into chat, for one company at a time:
1. Its HVT sheet row (all 38ish Plan B columns — differentiation, moat,
   product_improvement, alignment, gap, proof, sources, `segment_ref`, etc.)
2. Any financial figures you have (revenue, PAT, EBITDA margin, ROE, founded
   year, employee count — with where each came from: DRHP, Tofler, Tracxn...)
3. Optional: any qualitative intel from a BD call or DRHP read (go-to-market
   practices, R&D-to-launch process, named customers, management interviews) —
   only if this is a company you're actively pursuing (a "pursuit pass").
   Skip this for a directory-pass company; the generic segment scaffold is a
   legitimate fallback, per `generation-spec.md`, as long as it's marked
   `generic: true`.

Say "generate the profile" (or similar). Claude will:
- Reuse `segments/<segment_ref>.json` if it already exists, or research and
  build it once (market size/CAGR, peers, customer-value drivers, generic
  value-chain steps) — see `RECIPE.md` §1.
- Build the company + derived fields, classify `healthClass`, generate
  `opportunities[]`, and assemble the full contract-v3 profile JSON bottom-up
  (P5 → P4 → P3 → P1/P2), per `RECIPE.md` §2–§5.
- Save `companies/<slug>.json` (the contract-v3 profile — the eventual
  upload body) and `companies/<slug>.html` (a readable rendered preview, same
  visual template as `../context/hc-profiling`'s worked examples) so you have
  something to actually read without needing the live platform.

## What this folder does NOT do

- **Does not upload anything.** Once a profile is verified, upload it
  yourself: CRM → Hidden Champions → **New profile** → paste in the
  company domain (+ slug, optional) → paste or attach `companies/<slug>.json`
  → **Publish profile**. (The Postman/API-token route in `fde-rollout-plan.md`
  is now superseded by this CRM form — that doc predates the UI shipping.)
- **Does not set `meta.verified: true`.** That's the human no-fabrication
  gate — every generated JSON ships with `verified: false` and a checklist of
  which fact-Nodes to check against their source. Only flip it yourself,
  after checking — the CRM form (like the API) rejects unverified JSON.
- **Is not a replacement for the HVT Apps Script tool.** That tool still owns
  data-infra characterization (the 4 pillars + gap) at scale. This folder only
  turns an already-characterized row into a profile.

## Files here

| File | Purpose |
|---|---|
| `RECIPE.md` | The operating instructions Claude follows every time it generates a profile |
| `segments/<segment_ref>.json` | Segment-tier dataset, fetched once, reused across every company in that segment |
| `companies/<slug>.json` | Generated contract-v3 profile JSON, one per company |
| `companies/<slug>.html` | Readable rendered preview of the same profile |

## SSOT (don't duplicate, read these when in doubt)

`../context/hc-profiling/` — `generation-spec.md` (the real generation rules),
`profile-fe-contract.md` (the JSON schema), `example-eldorado-agritech.json`
(a complete valid reference), `fde-datafetch-plan.md` (the 38-col CSV = your
HVT sheet), `profile-generation-workflow.md` (the full runbook, including the
parts this folder deliberately skips), `fde-rollout-plan.md` (the upload API,
once you have a token).
