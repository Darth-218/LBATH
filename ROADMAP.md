# LBATH implementation roadmap

This roadmap turns the curated gaps in [`research/GAPS.md`](research/GAPS.md)
into an ordered implementation backlog. The GitHub issues are the detailed
source of truth for acceptance criteria; this file is the stable map of
phases, dependencies, and gap coverage.

## Principles

1. Fix evaluation and boundary contracts before building interfaces.
2. Build the telemetry and evidence foundation before agent capability work.
3. Keep the hunter read-only until evaluation and security probes justify more authority.
4. Validate on realistic telemetry before claiming production readiness or specializing models.
5. Do not edit `research/GAPS.md` by hand; update `research/curated_gaps.yaml` and regenerate.

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

When an issue changes phase, dependencies, or gap coverage, update its GitHub
body first and then the matching row here. When a new research gap is added to
`research/curated_gaps.yaml`, add an issue and link it from the gap coverage
table rather than editing generated gap output.
