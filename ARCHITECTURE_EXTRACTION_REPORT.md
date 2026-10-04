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

[...continued in full report...]