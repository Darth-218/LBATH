# Conventions

Field definitions, enum tie-breaks, and the rules that keep the corpus
comparable. Read this before your first entry.

## Contents

- [Why these rules exist](#why-these-rules-exist)
- [IDs](#ids)
- [paradigm](#paradigm)
- [memory.type](#memorytype)
- [architecture.components](#architecturecomponents)
- [problem](#problem)
- [extraction_basis](#extraction_basis)
- [unknown is a legal value](#unknown-is-a-legal-value)
- [Relations](#relations)
- [Adding a field is a schema change](#adding-a-field-is-a-schema-change)

## Why these rules exist

The schema enforces structure. It cannot enforce consistency. Two contributors
can both produce valid entries that describe the same paper differently, and
the corpus stays green while quietly becoming incomparable — which is the
exact problem this directory exists to solve.

Everything below is a tie-break for a case the schema cannot decide. If you
hit an ambiguity these rules don't cover, that's a signal to add one here in
the same PR, not to guess.

## IDs

IDs are stable keys, not display names. Every `related` reference points at
one, and it should not change.

Use `arxiv-2401.12345` when the paper has an arXiv id. Fall back to
`doi-10.xxxx/yyyy` only when it does not. **Prefer arXiv over DOI when both
exist.**

Slugs (`rag-cti-hunting-2024`) are not allowed. They drift when a title
changes or when naming taste differs, and the drift is invisible — nothing
fails, references just quietly stop resolving.

The readable name goes in `short_name`. That is what `COMPARISON.md` displays.

### This rule also prevents duplicates

Nothing in the schema stops one person adding `arxiv-2401.12345` and another
adding the DOI for the same paper. The ids differ, the titles match, and
validation passes. Preferring arXiv collapses that case.

Before adding an entry, search for it:

```sh
grep -ril "some distinctive title phrase" research/papers/
```

## paradigm

What the paper's contribution actually is. Not what it mentions in related
work.

- `prompting` — a single model call. No retrieval, no tools, no loop.
- `rag` — retrieval augments a generation step, with a **fixed** retrieval
  stage. The retriever feeds the model; the model does not decide to retrieve
  again.
- `agentic` — a loop where the model chooses the next action, including
  whether to call a tool or retrieve. Iteration is model-driven.
- `fine-tuned` — the contribution is weight updates; inference is a single
  pass.
- `hybrid` — genuinely combines two of the above as co-equal contributions.

### Tie-breaks

**If the model decides when to stop, it is `agentic`,** even if retrieval is
present. `rag` means the retrieval step is fixed.

Reserve `hybrid` for when the paper's own ablation shows neither mechanism
dominates. If one is doing the work, label it that one. `hybrid` is not a way
to avoid choosing.

If a paper uses retrieval but the ablation shows the retriever contributes
nothing, that is `prompting` with a caveat in `limitations`, not `rag`.

## memory.type

What persists across steps. `none` is a real answer and the common one.

- `none` — no state persists across steps.
- `vector` — embedding store.
- `graph` — knowledge graph or entity-relation store.
- `episodic` — transcript or history of prior interactions.
- `hybrid` — genuinely combines two of the above.
- `unknown` — the paper does not say. See below.

### Tie-breaks

Conversation history passed in the context window is `episodic`. A vector
store used *as* conversation history is `vector` — classify by the mechanism,
not the purpose.

If the paper describes memory but never says how it is implemented, that is
`unknown`, not a guess.

## architecture.components

One row per distinct stage.

**If it has a distinct input/output contract and you would draw it as a
separate box on a diagram, it is a component.**

Do not enumerate submodules, helper functions, or the internals of a
retriever. A paper with an ingestion stage, a retriever, a reasoner, and an
action executor has four components, not twelve.

### Tie-breaks

A retriever and a reranker are one component unless the paper treats them
separately in its own ablation or evaluation. If the paper merges them in its
architecture figure, you merge them here.

Each component's `inputs` and `outputs` describe the interface, not the data
flow of a specific run. `[query] → [CTI passages]`, not `[the January incident
query]`.

Leave `implementation` prose short and factual. If the paper names a specific
library or model, name it. If not, describe the mechanism.

## problem

What the paper's evaluation measures.

- `threat-hunting` — proactive search for adversaries in telemetry.
- `cti-triage` — assessing, enriching, or prioritizing threat intel.
- `attack-mapping` — mapping observations to ATT&CK or an equivalent framework.
- `incident-response` — reactive handling of a confirmed incident.
- `detection-engineering` — authoring or tuning detection rules.

### Tie-breaks

Most papers span several. **Pick the one the evaluation measures,** not the
one the abstract leads with. Abstracts overclaim scope; evaluations don't.

If the evaluation measures two genuinely, pick the one that consumes more of
the results section and note the other in `limitations`.

## extraction_basis

How you came to know what you wrote down. Be honest — this is the one field
that gates how much the corpus trusts the entry.

- `full-text` — you read the whole paper.
- `abstract-only` — you read the abstract and nothing else.
- `cited-by` — you know of it only through another paper's description.
- `third-party-summary` — a blog post, talk, or someone else's notes.

**Only `full-text` entries appear in the main comparison table.** Everything
else renders in an appendix, so secondhand summaries never acquire the same
visual weight as verified extraction.

If you upgrade an entry to `full-text` later, re-check the fields you wrote
from the summary. They are frequently wrong in the details that matter —
orchestration, memory, evaluation.

## unknown is a legal value

Many fields accept the literal string `unknown`. Use it deliberately.

Omitting a field is ambiguous — did the author forget, decide it was N/A, or
look and fail to find it? Explicit `unknown` distinguishes "not checked" from
"checked, absent," which is exactly what a reader needs.

Fields where `unknown` is legal include:

- `architecture.memory.type`
- `architecture.tools` (as a whole value, not per-item)
- `architecture.models[].access`
- `evaluation.datasets`, `metrics`, `baselines` (as a whole value)
- `evaluation.reproducible`

For `limitations`, use `[]` to mean the paper states none. Never omit the
field — an empty list and a missing field are different claims.

Do not use `unknown` to avoid reading the paper. It means you looked and the
information is not there.

## Relations

Author **one direction only.** Declare `extends`, not `extends-by`. The
renderer derives the inverse.

`validate.py` rejects self-references, duplicate edges, unresolved ids, and
contradictory back-edges, and warns on redundant ones.

- `supersedes` — this paper replaces the other. Later work that makes the
  earlier one obsolete.
- `extends` — builds directly on the other's method. Uses its architecture or
  evaluation as a starting point.
- `contradicts` — findings or claims are in tension. Results disagree, or the
  two papers make incompatible architectural claims.
- `same-authors` — overlapping author list. Useful for spotting a line of
  work; implies nothing about the content.

### Tie-breaks

`extends` and `supersedes` are the pair most often confused. `extends` means
the later paper *uses* the earlier one; `supersedes` means it *replaces* it.
A paper can extend without superseding — that is the common case.

`contradicts` requires the contradiction to be legible from the papers
themselves, not from your judgment about which is correct. If the papers
merely differ in setup, that is not a contradiction.

Relations are optional. Do not manufacture them to fill the field.

## Adding a field is a schema change

`additionalProperties: false` is set throughout, so a typo'd key fails
validation rather than being silently ignored. That is intentional.

If a real paper does not fit the shape, **change the schema in the same PR**
rather than bending the paper to fit. The first three entries are expected to
force adjustments — that is the schema being tested, not the paper being
wrong.

When you change the schema:

1. Bump `schema_version` if the change is not backward compatible.
2. Update this file in the same PR.
3. Update `templates/paper.yaml` and `templates/note.yaml` if the change
   affects them.
4. Re-run `render.py` — the generated files will reflect the new field.

