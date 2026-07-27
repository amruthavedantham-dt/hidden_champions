# Hidden Champions Profiling — team folder

Everything Amrutha (FDE) and the dev side need, self-contained:

| File | What it is |
|---|---|
| `fde-rollout-plan.md` | START HERE — both cases, one-time setup, API documentation, errors, go-live checklist |
| `profile-generation-workflow.md` | The per-company runbook: raw data → profile JSON → upload |
| `fde-datafetch-plan.md` | Plan B: fetching the 38-column CSV per company (Serper + Gemini) |
| `data-infra-spec.md` | Field definitions + verification discipline for the data fetch |
| `generation-spec.md` | How a profile is written (P5→P4→P3 then P1/P2, sourced fields only) |
| `profile-fe-contract.md` | The JSON schema a profile must satisfy (the platform validates against this) |
| `example-eldorado-agritech.json` | A complete, valid profile — the reference for what "done" looks like |
| `hidden-champions-fde-template.csv` | The 38-column CSV template with worked rows |

Code: backend module `src/pdgms/hc/` (API at `/api/v3/pdgms/hc`), frontend
`/p/hiddenchampions/[slug]` + `/crm/hidden-champions`.
