# CRM generation pipeline — from imported intel to a published profile

What happens after a profiler's file is imported, and exactly what a new topic must supply on the CRM side (short answer: one lens document, no code).

## 1. Company intel — where imported data lives

Each import writes one insert-only intel row per company (provider `profiler`). Its generation-facing `canonical` holds these **data classes** — the complete vocabulary a lens may request:

| Class | Content | Fed by |
|---|---|---|
| `identity` | name, sector, registration basics | import + CRM company row |
| `firmographics` | size, industry, geography, figures | import (`identity.sector/segmentRef`) + Serper refresh |
| `people` | known people/roles | CRM contacts + Serper |
| `momentum` | recent moves, news | Serper refresh + manual notes |
| `presence` | footprint, address, web presence | Serper + company row |
| `context` | verbatim lines from call notes | the record's notes box |
| `scores` | human nodal scores | the record's Scoring tab |
| `claims` | graded statements `{text, tier, source?, pillar?}` | **import claims** + website-read claims |
| `evidence` | research excerpts `{text, source?, pillar?}` | **import evidence** (the richness source) |
| `gap` / `alignment` / `proof` | structured extras (first profiler's ontology) | import, optional |

The four intel doors stack per company: profiler import, Serper refresh, website read, call notes. A human note beats profiler data; profiler beats Serper.

## 2. The lens — the only thing a new topic must create

A lens is pure data (imported or composed in the studio, never code): the topic's questions and editorial stance.

```json
{
  "schemaVersion": 1,
  "name": "…", "slug": "kebab-case", "description": "…",
  "thesis": {
    "claim": "What this kind of profile argues, in one paragraph.",
    "tone": "The writing voice.",
    "reader": "Who reads the page.",
    "stance": "suppress"
  },
  "blocks": [
    {
      "blockKey": "kebab-key",
      "question": "What must this section answer?",
      "approach": "HOW to answer it: ordering, honesty rules, card tags, what to omit.",
      "dataRequirements": ["claims", "evidence"],
      "required": false,
      "renderHint": "para"
    }
  ],
  "ask": { "cta": "The closing invitation.", "framing": "…" }
}
```

Rules that matter for a new topic:

- `dataRequirements` entries must come from the class table above. **The prompt only ever carries classes some block requested** — a lens that skips `gap/alignment/proof` never sees them, so topics without structured extras just don't ask.
- Every block MUST carry `required` (a boolean literal — omitting it rejects the lens). `renderHint` (`para | list | table | accordion | stats`) steers block→slot mapping. `required: true` makes that block's classes hard requirements (generation refuses without them) — use sparingly.
- **Card tags are lens vocabulary:** if a block's approach says "render each item as a card `### TAG — Title`", the engine renders tagged cards with whatever TAG set the approach names (the first topic uses MARGIN/VELOCITY; the worked example's software-fit topic uses SIGNAL/FIT). The mechanism is engine; the words are yours.
- `thesis.stance` is reserved (`suppress | permit | verdict`); today all generation follows the no-verdict doctrine.
- One lens serves every company on that topic. Compose (two-step preview, data-class chips) or import JSON; update supersedes into a new version; generation always follows the chain's active tip.

## 3. Layouts

Layouts are a server-side catalog (data). The default **Editorial** is the deep 7-slot page (Snapshot stats, three prose parts, Workflows table, Experiments list, a pinned two-reveal accordion titled Proof / Activation Path) with **authored titles** — the model writes each part's narrative title; the catalog titles are theme hints. Nine generic archetypes (essay, brief, snapshot, evidence, comparison, objections, meeting-pack, data-room, story-proof) have no fixed titles at all and fit any topic. A topic wanting its own fixed frames adds one entry to the catalog literal (small code, the only layout-related code there is).

## 4. Generation — what the engine guarantees for any topic

- **Per-part writing:** one full-attention model call per slot, in order, each seeing prior parts' titles/openers; the hero (a thesis headline serving the lens's own thesis) and conclusion are written last with the whole page in view. Rich dossiers (≥10 entries) unlock 3–5 developed paragraphs per prose part.
- **Grounding fence:** the model may only use the dossier (numbered claims + evidence with tier and source) and the fenced manifest. Citations are tracked per section via `[C#]` markers that are **stripped from the visible page** — sources stay internal (studio toggle only).
- **Writing doctrine (topic-neutral):** attribute a self-claim once then write freely; name the tension between what the subject claims and what the record shows; no verdicts, no advice; grading vocabulary (tiers, "unverified") never appears in reader-visible text; superlatives are leads, not proof; em-dashes stripped.
- **Cost stamp:** every version records its API calls (tokens in/out/thinking per call); the studio shows a per-version popup with an INR estimate at a live, server-cached USD→INR rate.
- Publish flow (consent gate, passcode page at `/p/s/…`, sends, engagement, Heat Index) is identical for every topic.

## 5. The full new-topic checklist (CRM side)

1. Import the profiler's file (offering from the dropdown).
2. Import or compose the topic's lens; it is active immediately.
3. Create a spotlight (company × lens), pick a layout, Generate.
4. Review, per-slot regenerate or edit, publish, send.

No CRM code in any step. The three bounded exceptions (topic-specific structured sections, verdict stance wiring, a custom fixed-frame layout) are listed in the [README](README.md).
