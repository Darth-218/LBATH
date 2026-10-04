# Architecture Extraction Report: Three Agentic Threat Hunting Papers

This report extracts and analyzes the architectural components from the three core papers identified in the literature review.

## 1. Paper 1: Mohsin et al. (2026) - "A Unified Framework for Human–AI Collaboration in Security Operations Centers with Trusted Autonomy"

**Source:** `A Unified Framework for Human–AI Collaboration in SecurityOperations Centers with Trusted Autonomy.pdf`  
**Type:** Conceptual framework + empirical validation  
**DOI:** 10.1145/3837073

### 1.1 High-Level Architecture

The paper proposes a **triadic Human-AI Collaboration Framework** (Figure 3) organized in two layers:

- **Top Layer (Functional Tiers):** System Security, Alerts Management, Threat Management, and Response & Recovery
- **Bottom Layer (Autonomy Control):** 5-level autonomy scale (Level 0-4) aligned with HITL/HOtL/HOoTL
- **Core:** Symbiotic human-AI interaction with feedback loops and transparency mechanisms

### 1.2 Core Architectural Components

#### 1.2.1 Autonomy Controller (Core Decision Logic)
The framework formalizes autonomy calibration through mathematical models:

| Component | Formula | Purpose |
|---|---|---|
| Task Complexity (C), Risk (R), Trust (T) | Normalized to [0,1] | Inputs driving autonomy decisions |
| Autonomy Level (A*) | $A^* = A(C,R,T) = 1 - (w_1 C + w_2 R)(1-T)$ | Calculates appropriate autonomy level |
| HITL Involvement (H) | $H = 1 - A$ | Inverse relationship with autonomy |
| Trust (T) | $T = w_1 E + w_2 P + w_3 (1-U)$ | Computed from Explainability (E), Performance (P), Uncertainty (U) |
| Dynamic Update | $A_{t+1} = A_t + k(\Delta T - \Delta R)$, $T_t = T_{t-1} + \Delta T(E,P,U)$ | Adaptive autonomy switching |

**Autonomy Levels (0-4):**
- **Level 0 (Manual):** Human-only control (HITL)
- **Level 1 (Assisted):** AI suggests, human decides (HITL)
- **Level 2 (Semi-Autonomous):** AI acts, human approves major actions (HITL→HOtL)
- **Level 3 (High Autonomy):** AI acts autonomously for low-risk, human supervises (HOtL)
- **Level 4 (Fully Autonomous):** AI self-directed with oversight (HOoTL)

#### 1.2.2 CyberAlly System Architecture (Implementation)

Figure 5 shows the concrete implementation deployed in ACDC Cyber Range:

```text
Endpoints + IDS/IPS Agents
  → Wazuh SIEM/EDR (Aggregation)
    → Slack Hub (Visibility)
      → CyberAlly (RAG-augmented GPT LLM + Knowledge Graphs)
        → Triage & Prioritization
          → [Benign → Archived] / [Critical → Collaborative Review]
            → Cydarm Ticketing (Automated)
              → Mitigation Actions + Feedback Logging
```

**Key Components:**
- **Data Ingestion:** Wazuh SIEM/EDR aggregating telemetry from endpoints, IDS/IPS
- **Communication Layer:** Slack hub for team visibility
- **Reasoning Engine:** RAG-augmented GPT LLM with Chain-of-Thought (CoT) reasoning
- **Knowledge Layer:** Knowledge graphs (entity grounding) + RAG over security DB (MITRE ATT&CK, threat feeds, network topology)
- **Workflow Orchestration:** SOAR playbooks + Cydarm ticketing
- **Trust Controller:** Dynamic autonomy switching with uncertainty/explainability scoring
- **Feedback Loop:** All actions logged for continuous learning and trust calibration

#### 1.2.3 Operational Workflows

Three functional domains (Figure 4):
1. **Alerts Management (L1-L3):** AI correlates/severity-scores → Tier-1 validates → AI auto-dismisses FPs via NLP → Tier-2 review
2. **Threat Management (L2-L3):** AI classifies incidents, reconstructs attack paths → root-cause analysis → Tier-2/3 verification → detection model updates
3. **Response & Recovery (L1-L4):** AI suggests actions → approval gates → SOAR execution (post-confirmation) → escalation based on risk

### 1.3 Architectural Strengths
- **Explicit trust/risk gating:** Mathematical formulation of when to escalate/de-escalate autonomy
- **Human-in-the-loop by design:** Approval gates for major actions (especially L2)
- **Grounded reasoning:** RAG + knowledge graphs reduce hallucinations
- **Feedback-driven adaptation:** Trust updates based on performance, explainability, uncertainty

---

## 2. Paper 2: Mahboubi et al. (2024) - "Evolving techniques in cyber threat hunting: A systematic review"

**Source:** JNCA 232 (2024) 104004  
**Type:** Systematic Literature Review (117 papers)  
**Focus:** Threat hunting methodology, process, taxonomy

### 2.1 Core Architecture (Process Model)

The paper's most important architectural contribution is the **10-Step Systematic Process of Adaptive Threat Hunting** (Figure 2), derived from SANS maturity model:

```text
1. Ingestion of heterogeneous data sources (data lakes, logs)
  → 2. Formulation of threat definitions & hypotheses
    → 3. Proactive threat hunting (hypothesis-aligned search)
      → 4. Employment of threat observation techniques (analysis/anomaly detection)
        → 5. Classification of identified threats (clustering/characteristics)
          → 6. Human validation of threats (MANDATORY GATE)
            → 7. Assessment against prevention/detection (IDS/IPS/firewalls)
              → 8. Extraction of threat signatures & patterns
                → 9. Enhancement of detection & mitigation frameworks (ATT&CK/STIX)
                  → 10. Iterative enhancement (feedback → back to step 2)
```

**Key Characteristic:** This is a **hypothesis-driven iterative loop** with mandatory human validation at step 6.

### 2.2 Taxonomy of Architectural Approaches (Classification)

The paper classifies threat hunting architectures into 6 categories (Figure 4):

| Category | Architectural Style | Representative Systems | Key Components |
|---|---|---|---|
| **Supervised ML** | Pipeline (train → infer) | LSTM/CNN, ensemble, transformer/BiLSTM (DeepAG) | Feature extraction, classifiers, labeled datasets |
| **Unsupervised ML** | Anomaly detection pipeline | LogAnomaly, LogUAD, autoencoders, UHAC, UN-AVOIDS | Embedding, reconstruction/error scoring, clustering |
| **Reasoning** | Knowledge-driven | CCS (KG deduction), logic programming, game theory | Knowledge bases, inference engines, causal models |
| **Graph-based** | Graph analytics | Poirot, DeepHunter (GNN), ANUBIS, Euler, AttackDB/AHG, THREATRACE, T-trace, Hopper | Provenance graphs, query graphs, knowledge graphs (KG), GNNs, path alignment |
| **Rule-based** | Deterministic matching | SteinerLog, C-BEDIM/S-BEDIM, ProvTalk, HERCULE | Rule engines, signature DBs, pattern matchers |
| **Other** | Hybrid/statistical | UEBA (SVD+Mahalanobis), MABAT (MAB), ELK+honeypots | Statistical models, bandit algorithms, behavioral analytics |

### 2.3 Formal Hypothesis-Driven Architecture

The paper proposes a mathematical foundation for hypothesis-driven hunting:

- **HMM-based Attacker Model:** Hidden states = attack stages, observations = network effects (A, B, π matrices; forward/Viterbi)
- **Anomaly Scoring:** $a(x_i)$ via Mahalanobis distance
- **Threat Indicator Fusion:** $t(x_i)=1$ if $c(x_i)\cdot a(x_i) > \tau$ with $\tau^* = \arg\min_\tau\{\mu\cdot FPR(\tau) + (1-\mu)\cdot[1-TPR(\tau)]\}$
- **Iterative Refinement:** $(M', c') = f(M,c,I)$ from investigation findings

### 2.4 Key Architectural Insight
**Hypothesis generation is the central, under-served component.** Most surveyed systems focus on detection/analysis but deprioritize automated hypothesis formulation (step 2). The loop is explicitly iterative with mandatory human validation.

---

## 3. Paper 3: Chona et al. (2026) - "Cyber Defense Benchmark: Agentic Threat Hunting Evaluation for LLMs in SecOps"

**Source:** Simbian AI Technical Report v1.0, April 2026  
**Type:** Benchmark + Agent Architecture  
**Repo:** github.com/simbianai/cyber_defense_benchmark

### 3.1 Agent Architecture

The benchmark defines a **single-agent architecture**: `UniversalHunter` with a minimal, testable interface.

```text
Agent (UniversalHunter)
  → HunterAction {reasoning, tool, sql_query, submitted_timestamps}
    → HolodeckHuntEnv (Gymnasium)
      → In-memory SQLite `logs` table (505 columns + raw_json, 4 indexes)
        → Observation (briefing + last query + result OR error)
          → Agent Loop (max 50 queries / 75 turns)
```

**Core Design Principle:** Deliberately minimal - SQL is the **only** tool interface (no RAG, no vector store, no external APIs). This isolates agent reasoning capability.

### 3.2 Action Space

The agent has exactly **3 actions**:

| Action | Parameters | Purpose |
|---|---|---|
| `run_sql` | `sql_query` (string) | Execute SQL against logs table; returns ≤10 rows + full row count + error if any |
| `submit_flags` | `submitted_timestamps` (array) | Submit candidate malicious event timestamps as evidence |
| `give_up` | - | Explicit early termination |

### 3.3 Reasoning Architecture

- **Paradigm:** ReAct-style (Reasoning → Act → Observe)
- **Structured Output:** JSON-schema constrained decoding for `HunterAction`
- **Mandatory Reasoning:** `reasoning` field is required before every tool call (internal monologue)
- **System Prompt:** Mission + full 505-column schema + pagination instructions + 3 available actions
- **Context:** Conversation history is the **belief state** (short-term memory only)

### 3.4 Key Architectural Constraints

- **Read-only:** `run_sql` only; no write/execute capabilities (sandboxed by design)
- **Budget-constrained:** 50-query budget, 1.5× safety cap (75 turns) - forces efficiency
- **Error-resilient:** SQL errors surfaced in observation space (agent must self-correct within budget)
- **Unprimed:** No guided questions, no alert seeding, no RAG - pure discovery from telemetry

---

## 4. Cross-Paper Architecture Synthesis

### 4.1 Common Architectural Patterns

| Aspect | Mohsin (2026) | Mahboubi (2024) | Chona (2026) |
|---|---|---|---|
| **Control Flow** | Feedback-driven adaptive loop with trust gates | Iterative 10-step hypothesis loop (mandatory human validation at step 6) | Turn-based ReAct loop with budget constraints |
| **Reasoning** | CoT + RAG + Knowledge Graphs | Inductive/deductive + graph reasoning (survey) | ReAct with mandatory `reasoning` field (structured JSON) |
| **Human-in-the-Loop** | Explicit tiers (HITL/HOtL/HOoTL), approval gates for major actions | Mandatory validation at step 6 of hunt process | Not present (benchmark only; read-only, no destructive actions) |
| **Memory** | Short-term (current incident) + Long-term (ATT&CK/KG/threat feeds/history) | CTI knowledge bases, provenance graphs (long-term) | Short-term only (conversation history as belief state) |
| **Grounding** | RAG + Knowledge Graphs (explicit) | KG/provenance graphs (recommended) | None (deliberately ungrounded - tests discovery) |
| **Tool Interface** | SIEM (Wazuh), SOAR, Ticketing (Cydarm), Slack | Heterogeneous tools (SIEM/SOAR/EDR/CTI) | SQL-only (minimal interface) |

### 4.2 Critical Architectural Gaps Identified

From cross-paper analysis:
1. **Hypothesis Generation (Step 2)** - Most under-served component (Mahboubi); Chona shows agents fail at spontaneous hypothesis generation (Credential Access/Initial Access blind spots)
2. **Multi-Agent Orchestration** - All three primarily single-agent; Mohsin notes future work on agent teams
3. **Error Recovery** - Chona surfaces errors but has no explicit retry/fallback policies; others don't specify
4. **Tactic-Specific Knowledge** - Chona empirically shows domain-specific query knowledge missing (ATT&CK mapping failures)
5. **Cross-Platform Telemetry** - All focus on Windows/event logs; limited coverage of Linux/cloud/network flows
6. **Adversarial Robustness** - Named as risk (Mohsin) but never empirically tested

---

## 5. Conclusion

The three papers present complementary architectural views:
- **Mohsin** provides the **production-ready socio-technical architecture** with explicit trust/autonomy control and human oversight
- **Mahboubi** provides the **canonical process architecture** (hypothesis-driven loop) and taxonomy of technical approaches
- **Chona** provides the **minimal, testable agent architecture** with rigorous evaluation constraints

Together, they define the architectural blueprint for building, evaluating, and deploying agentic threat hunting systems in SOC environments.