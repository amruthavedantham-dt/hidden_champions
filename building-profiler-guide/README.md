# Profiler Guide — building a research profiler for any topic

This guide is for building a **new profiler** (a research pipeline that studies companies for some reason) and plugging it into the CRM's Companies/Spotlights system. The Hidden Champions profiler was the first; the CRM side is deliberately topic-agnostic, so a second profiler for any other reason (selling a software you built, vendor reliability, talent brand, acquisition fit, anything) reuses everything behind the upload button with **zero CRM code changes** for the standard path.

## The one-sentence architecture

> A profiler researches companies and exports a JSON file in the **import envelope** format; the CRM ingests that file into graded company intel; a **lens** (pure data, per topic) tells the generation engine what questions to answer from that intel; the engine writes, cites, and publishes the profile page.

The wall between the two worlds is the JSON contract. Everything on the CRM side of the wall is shared machinery. Everything on the profiler side is per-topic and expected to be forked — including its look and feel and internals, which may be restyled or optimized freely. Two things are non-negotiable in any fork: the harness guarantees (rate limiting with backoff and jitter, circuit breaker, checkpoint/resume, failure containment, search cache, cost ledger — see [profiler-anatomy.md](profiler-anatomy.md)) and the import contract itself.

## Reading order

| File | What it covers |
|---|---|
| [crm-import-contract.md](crm-import-contract.md) | The exact JSON a profiler must emit, field by field, with caps and validation rules, and what the CRM does with each field on import. |
| [profiler-anatomy.md](profiler-anatomy.md) | The App Script profiler's architecture: which parts are a reusable harness (keep), which parts are topic brains (fork), and every setting involved. |
| [crm-generation-pipeline.md](crm-generation-pipeline.md) | What happens after import: intel classes, lenses, layouts, per-part generation, writing rules, citations, cost stamps. What a new topic's lens must contain. |
| [worked-example-software-fit.md](worked-example-software-fit.md) | A complete solution-led example: you built a software that solves a problem for a definable kind of company; pillars, queries, export JSON, and the lens that writes "what they run, where it strains, how the software helps", end to end. |

## What "zero code" covers, and the three known exceptions

A new topic needs, at minimum: a forked profiler script (research side) and one new lens document (CRM side, imported through the studio, no code). That is the whole standard path.

Three cases need bounded CRM work, all scoped in advance:

1. **Topic-specific structured sections.** The envelope's structured extras (`gap`, `alignment`, `proof`) carry field names from the first profiler's ontology. Flat `claims` + `evidence` cover any topic; a topic wanting its *own* structured shapes (say `riskRegister`) is a ~5-file additive extension (both validators, canonical build, merge passthrough, class list), no migration.
2. **Verdict-shaped topics.** The writing doctrine forbids verdicts (correct for outreach pages). A topic whose purpose *is* judgment on the page itself (grading a lead's fit to their face, scoring a vendor) needs the reserved `thesis.stance` lens field wired into the generation preamble — small, deliberately deferred until a real case exists.
3. **Layout fit.** The default Editorial layout's pinned reveal headings (Proof / Activation Path) fit capability-story topics. Other topics pick one of the nine generic archetypes (no code), or add one entry to the layout catalog (a data literal in one file).
