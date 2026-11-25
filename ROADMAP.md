# LBATH implementation roadmap

This roadmap turns the curated gaps in [`research/GAPS.md`](research/GAPS.md)
into an ordered backlog for a graduation project that produces a conference
paper, a thesis, and an applied system. GitHub issues are the detailed source
of truth for acceptance criteria; this file is the stable map of phases,
dependencies, evidence gates, and gap coverage.

## Deliverable tracks

- **System track** — phases 0–6 below. Builds the evaluator, hunter, controls,
  and realism evidence.
- **Paper track** — interleaved research-publication work from R-20 through
  R-27. Converts system evidence into claims, tables, figures, and manuscripts.
- **Applied delivery track** — R-28. Packages the accepted system into a
  runnable prototype with a pilot-ready boundary.

Every accepted experiment must have a stable ID in `experiments/`, immutable
run files in `artifacts/`, and paper-ready output in `results/`.

## Principles

1. Fix evaluation and boundary contracts before building interfaces.
2. Build the telemetry and evidence foundation before agent capability work.
3. Keep the hunter read-only until evaluation and security probes justify more authority.
4. Validate on realistic telemetry before claiming production readiness or specializing models.
5. Keep core paper claims independent of unavailable real telemetry.
6. Make component choices configurable so they can be ablated, not merely described.
7. Generate paper tables and figures from result files; never hand-copy measured numbers.
8. End with a reproducible applied system, not only a benchmark harness.
9. Do not edit `research/GAPS.md` by hand; update `research/curated_gaps.yaml` and regenerate.

## Evidence gates

| Gate | Trigger | Evidence required | Decision |
| --- | --- | --- | --- |
| A — Protocol locked | Phase 0–1 plus R-20, R-21 | Research questions, metric contract, authority policy, evidence contract, related-work matrix | Freeze the method; no silent metric changes |
| B — Baseline usable | Phase 2–3 plus R-22, R-23 | Evaluator, TTP corpus, reproducibility, manifests, splits, seeds | Freeze splits and baseline before capability claims |
| C — Results frozen | Phase 4–5 plus R-24 | Single-hunter baseline, ablations, robustness, authority enforcement | Draft conference paper from accepted experiment IDs |
| D — Graduation artifact | Phase 6 plus R-25, R-27, R-28 | Realism fallback, thesis, applied-system package | Submit thesis and release the applied system |

## Research questions

| Question | Evidence issues |
| --- | --- |
| RQ1: Does evidence-scoped memory with provenance improve finding quality and trust? | [#7](https://github.com/Darth-218/LBATH/issues/7), [#10](https://github.com/Darth-218/LBATH/issues/10), [#17](https://github.com/Darth-218/LBATH/issues/17) |
| RQ2: Does ATT&CK-guided hypothesis generation beat unguided ReAct on tactic coverage? | [#13](https://github.com/Darth-218/LBATH/issues/13), [#16](https://github.com/Darth-218/LBATH/issues/16) |
| RQ3: Does role-separated orchestration beat a single hunter, and at what cost? | [#18](https://github.com/Darth-218/LBATH/issues/18), [#20](https://github.com/Darth-218/LBATH/issues/20), [#24](https://github.com/Darth-218/LBATH/issues/24) |
| RQ4: Do sanitized boundaries and authority tiers resist injection without blocking hunts? | [#19](https://github.com/Darth-218/LBATH/issues/19), [#21](https://github.com/Darth-218/LBATH/issues/21), [#22](https://github.com/Darth-218/LBATH/issues/22) |
| RQ5: How far do benchmark results transfer to realistic noisy telemetry? | [#23](https://github.com/Darth-218/LBATH/issues/23), [#31](https://github.com/Darth-218/LBATH/issues/31) |

## Phase 0 — Decisions and contracts

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#5](https://github.com/Darth-218/LBATH/issues/5) | R-00 Define evaluation contract and scorecard | tactic, hypothesis | — |
| [#6](https://github.com/Darth-218/LBATH/issues/6) | R-01 Define action authority and autonomy policy | adversarial | — |
| [#7](https://github.com/Darth-218/LBATH/issues/7) | R-02 Define evidence, memory, and security-context contract | adversarial, tactic | — |

## Phase 1 — Telemetry and evidence foundation

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#8](https://github.com/Darth-218/LBATH/issues/8) | R-03 Normalize cross-platform telemetry schema | cross-platform | #7 |
| [#9](https://github.com/Darth-218/LBATH/issues/9) | R-04 Build typed read-only security tool interface | cross-platform, error | #8 |
| [#10](https://github.com/Darth-218/LBATH/issues/10) | R-05 Build incident-scoped evidence store with provenance | tactic, adversarial | #7, #8 |
| [#11](https://github.com/Darth-218/LBATH/issues/11) | R-06 Put retrieval behind a testable interface | adversarial | #9, #10 |

## Phase 2 — Measurement

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#12](https://github.com/Darth-218/LBATH/issues/12) | R-07 Implement multi-rollout evaluator with hidden ground truth | tactic, hypothesis | #5, #10, #11 |
| [#13](https://github.com/Darth-218/LBATH/issues/13) | R-08 Select or build TTP-sequence regression corpus | tactic, hypothesis | #8, #12 |
| [#14](https://github.com/Darth-218/LBATH/issues/14) | R-09 Make hunts reproducible from published artifacts | — | #12 |

## Phase 3 — Reliable core loop and knowledge

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#15](https://github.com/Darth-218/LBATH/issues/15) | R-10 Add bounded retry, fallback, and audit trail | error | #9, #12 |
| [#16](https://github.com/Darth-218/LBATH/issues/16) | R-11 Add ATT&CK-anchored hypothesis generation | hypothesis, tactic | #13, #15 |
| [#17](https://github.com/Darth-218/LBATH/issues/17) | R-12 Enforce evidence citations and calibrate L3 gate | adversarial, tactic | #7, #10, #12, #15 |

## Phase 4 — Orchestration

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#18](https://github.com/Darth-218/LBATH/issues/18) | R-13 Freeze single-hunter baseline | multi-agent | #12, #15, #16, #17 |
| [#19](https://github.com/Darth-218/LBATH/issues/19) | R-14 Add sanitized message bus and poisoning defenses | adversarial, multi-agent | #7, #10, #15 |
| [#20](https://github.com/Darth-218/LBATH/issues/20) | R-15 Add coordinator and role-separated specialists | multi-agent | #18, #19 |

## Phase 5 — Trust and control

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#21](https://github.com/Darth-218/LBATH/issues/21) | R-16 Run injection and poisoning probe suite | adversarial | #11, #12, #17, #20 |
| [#22](https://github.com/Darth-218/LBATH/issues/22) | R-17 Enforce action authority tiers and human approval | adversarial | #6, #9, #20, #21 |

## Phase 6 — Realism and specialization

| Issue | Title | Gaps | Depends on |
| --- | --- | --- | --- |
| [#23](https://github.com/Darth-218/LBATH/issues/23) | R-18 Run production-realism pilot | cross-platform, tactic | #8, #12, #22 |
| [#24](https://github.com/Darth-218/LBATH/issues/24) | R-19 Define cost/latency model strategy and specialization gate | — | #12, #16, #23 |

## Research publication track

| Issue | Title | Depends on |
| --- | --- | --- |
| [#26](https://github.com/Darth-218/LBATH/issues/26) | R-20 Define thesis and conference paper scope | — |
| [#27](https://github.com/Darth-218/LBATH/issues/27) | R-21 Build BibTeX and related-work matrix | R-20 |
| [#28](https://github.com/Darth-218/LBATH/issues/28) | R-22 Create experiment registry and paper-ready outputs | #5, #12, R-20 |
| [#29](https://github.com/Darth-218/LBATH/issues/29) | R-23 Freeze dataset manifests, splits, and seeds | #13, #14, R-22 |
| [#30](https://github.com/Darth-218/LBATH/issues/30) | R-24 Add ablation/configuration harness | #11, #16, #18, #20, R-22 |
| [#31](https://github.com/Darth-218/LBATH/issues/31) | R-25 Define data-access, ethics, and realistic-pilot fallback | #23, R-20 |
| [#32](https://github.com/Darth-218/LBATH/issues/32) | R-26 Draft conference paper | R-20, R-21, R-22, R-23, R-24, #21, #23 |
| [#33](https://github.com/Darth-218/LBATH/issues/33) | R-27 Draft thesis chapters | R-26, #23, R-25 |

## Applied system delivery

| Issue | Title | Depends on |
| --- | --- | --- |
| [#34](https://github.com/Darth-218/LBATH/issues/34) | R-28 Build applied-system release package | #20, #22, #23, R-24, R-26 |

## Gap coverage

| Curated gap | Issues |
| --- | --- |
| `gap-cross-platform-telemetry` | [#8](https://github.com/Darth-218/LBATH/issues/8), [#9](https://github.com/Darth-218/LBATH/issues/9), [#23](https://github.com/Darth-218/LBATH/issues/23) |
| `gap-error-recovery` | [#15](https://github.com/Darth-218/LBATH/issues/15), [#17](https://github.com/Darth-218/LBATH/issues/17), [#19](https://github.com/Darth-218/LBATH/issues/19) |
| `gap-hypothesis-generation` | [#13](https://github.com/Darth-218/LBATH/issues/13), [#16](https://github.com/Darth-218/LBATH/issues/16) |
| `gap-multi-agent-orchestration` | [#18](https://github.com/Darth-218/LBATH/issues/18), [#19](https://github.com/Darth-218/LBATH/issues/19), [#20](https://github.com/Darth-218/LBATH/issues/20) |
| `gap-tactic-specific-knowledge` | [#12](https://github.com/Darth-218/LBATH/issues/12), [#13](https://github.com/Darth-218/LBATH/issues/13), [#16](https://github.com/Darth-218/LBATH/issues/16), [#17](https://github.com/Darth-218/LBATH/issues/17) |
| `gap-adversarial-robustness` | [#7](https://github.com/Darth-218/LBATH/issues/7), [#10](https://github.com/Darth-218/LBATH/issues/10), [#11](https://github.com/Darth-218/LBATH/issues/11), [#17](https://github.com/Darth-218/LBATH/issues/17), [#19](https://github.com/Darth-218/LBATH/issues/19), [#21](https://github.com/Darth-218/LBATH/issues/21), [#22](https://github.com/Darth-218/LBATH/issues/22) |

## Maintenance

When an issue changes phase, dependencies, gap coverage, or paper deliverable,
update its GitHub body first and then the matching row here. When a new research
gap is added to `research/curated_gaps.yaml`, add an issue and link it from the
gap coverage table rather than editing generated gap output. Paper claims must
reference experiment IDs from `experiments/`; measured numbers must come from
`results/`.
