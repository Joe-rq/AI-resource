---
title: "ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering"
source: "url"
source_file: "https://arxiv.org/html/2602.23193"
created: "2026-05-22T01:41:14Z"
source_url: "https://arxiv.org/html/2602.23193"
extract_method: "arxiv"
---

## 1Introduction

LLM-based software engineering is shifting from conversational interactions to agentic workflows that require _long-horizon consistency_—that is, maintaining coherence between goals, contracts, and effects over dozens of cycles and artifacts *[[17](#bib.bib17)]*. In brownfield scenarios, where the agent needs to navigate large repositories and modify multiple files with cross-dependencies, the risk of _state drift_ increases: the agent may believe it has fixed a bug while the actual system remains unchanged, or it may rewrite specifications to bypass local compilation failures.

A recurring empirical source for these difficulties is software engineering benchmarks on real GitHub issues, such as SWE-bench, which aims to measure the ability of agents to produce coherent and verifiable patches in real-world codebases, moving beyond synthetic and isolated problems *[[8](#bib.bib8)]*. Even when there is progress in configurations with human validation or restricted suites, the operational challenge of governance remains: auditing what the agent did, why it did it, and how to revert with forensic precision *[[12](#bib.bib12)]*.

Contemporary multi-agent frameworks like AutoGen *[[15](#bib.bib15)]*, MetaGPT *[[7](#bib.bib7)]*, and LangGraph *[[9](#bib.bib9)]* have made significant progress in agent coordination, role assignment, and workflow orchestration. However, these systems typically manage state through in-memory data structures or database snapshots, lacking the _immutable audit trail_ and _deterministic replay_ guarantees that are essential for production software engineering workflows where accountability and reversibility are non-negotiable.

This work proposes that the core problem is not just "improving the prompt"; it is restructuring the system around verifiable invariants. ESAA applies the Event Sourcing pattern to the agent’s lifecycle: the source of truth is not the current snapshot of the repository, but an immutable log of intentions, decisions, and effects, from which the current state is deterministically projected *[[4](#bib.bib4)]*. In parallel, ESAA adopts Command Query Responsibility Segregation principles, aligned with the CQRS tradition, to reduce coupling between writing (changes) and reading (derived state) *[[5](#bib.bib5)]*. The architecture is validated through two case studies of increasing complexity: a landing page project orchestrated with single-agent composition (9 tasks, 49 events) and a clinical dashboard system (clinic-asr) orchestrated with four heterogeneous LLM agents operating concurrently (50 tasks, 86 events, 8 completed phases). Both cases demonstrate state reproducibility via replay and hash verification.

---

## 2Related Work

### 2.1Tool-Using Agents and Interleaved Reasoning

The ReAct pattern describes a cycle where the model alternates between reasoning and acting via tools, incorporating environment observations into the next step *[[17](#bib.bib17)]*. While this interaction increases capability in tool-oriented tasks, it also amplifies vulnerabilities: noisy observations and tool outputs consume the context window, and errors can propagate through multiple turns.

Benchmarks like SWE-bench formalize part of this problem by requiring patches that pass tests in real repositories, capturing a relevant fraction of real-world requirements *[[8](#bib.bib8)]*. "Verified" sets and more rigorous evaluation protocols are also emerging, aimed at reducing false positives from solutions that do not address the root of the defect *[[12](#bib.bib12)]*. Nevertheless, these benchmarks do not resolve the need for a governance kernel to control effects and maintain an audit trail.

### 2.2Multi-Agent Frameworks

Recent multi-agent systems have explored various coordination strategies. AutoGen *[[15](#bib.bib15)]* enables conversational patterns between agents with role-based specialization. MetaGPT *[[7](#bib.bib7)]* assigns software engineering roles (architect, developer, tester) to different agents with structured output protocols. LangGraph *[[9](#bib.bib9)]* provides a graph-based state machine to define agent workflows with conditional edges and cycles.

Although these frameworks advance agent coordination, they share common limitations from an auditability perspective: (i) state is typically mutable and stored as snapshots rather than a change log; (ii) there is no native mechanism for deterministic replay of the complete decision trail; (iii) the blast radius of a compromised agent is not formally bounded by contracts. ESAA addresses these gaps by applying event sourcing as the fundamental state management paradigm. [Table˜1](#S2.T1 "In 2.2 Multi-Agent Frameworks ‣ 2 Related Work ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") presents a structured comparison.

_Table 1: Comparison of ESAA with contemporary multi-agent frameworks._

| Capability | AutoGen | MetaGPT | LangGraph | CrewAI | ESAA |
| --- | --- | --- | --- | --- | --- |
| Immutable event log | – | – | – | – | ✓ |
| Deterministic replay | – | – | – | – | ✓ |
| Boundary contracts | – | Partial | – | – | ✓ |
| Constrained JSON output | – | ✓ | – | – | ✓ |
| Multi-agent concurrency | ✓ | ✓ | ✓ | ✓ | ✓ |
| Hash-verified projection | – | – | – | – | ✓ |
| Role-based specialization | ✓ | ✓ | ✓ | ✓ | ✓ |
| "Done" immutability rule | – | – | – | – | ✓ |
| Blast radius containment | – | Partial | – | – | ✓ |

### 2.3Context Limits and Long-Horizon Degradation

Recent works point to systematic degradation in long context windows, with a drop in recall in the middle of the context (_lost-in-the-middle_), affecting tasks that depend on facts buried in logs, docs, or extensive histories *[[10](#bib.bib10)]*. This limitation creates recency bias and can induce the agent to ignore initial contracts, especially in environments requiring consistency with specifications and security policies.

### 2.4Event Sourcing and CQRS

Event Sourcing records every state change as an immutable event in an append-only log; the current state is a projection of these events *[[4](#bib.bib4)]*. Alongside this, CQRS separates write and read models to optimize consistency and queries, reducing complexity in systems with strong audit and traceability requirements *[[5](#bib.bib5)]*. ESAA transposes these principles to LLM-assisted software engineering: the agent does not "write state"; it emits intentions and proposed diffs that are validated and applied by a deterministic orchestrator.

### 2.5Constrained Output and Syntactic Structure

A practical bottleneck in agents is the _structure gap_: models generate probabilistic text, but systems require payloads compliant with schemas (JSON, API calls, patches). Constrained decoding and structured generation approaches guide sampling using grammars and schemas, reducing parsing failures and rejections *[[3](#bib.bib3), [16](#bib.bib16)]*. Inference and serving frameworks like SGLang also highlight the relevance of this layer by integrating mechanisms for structured outputs and high-throughput execution pipelines *[[14](#bib.bib14)]*.

---

### 2.1Tool-Using Agents and Interleaved Reasoning

The ReAct pattern describes a cycle where the model alternates between reasoning and acting via tools, incorporating environment observations into the next step *[[17](#bib.bib17)]*. While this interaction increases capability in tool-oriented tasks, it also amplifies vulnerabilities: noisy observations and tool outputs consume the context window, and errors can propagate through multiple turns.

Benchmarks like SWE-bench formalize part of this problem by requiring patches that pass tests in real repositories, capturing a relevant fraction of real-world requirements *[[8](#bib.bib8)]*. "Verified" sets and more rigorous evaluation protocols are also emerging, aimed at reducing false positives from solutions that do not address the root of the defect *[[12](#bib.bib12)]*. Nevertheless, these benchmarks do not resolve the need for a governance kernel to control effects and maintain an audit trail.

---

### 2.2Multi-Agent Frameworks

Recent multi-agent systems have explored various coordination strategies. AutoGen *[[15](#bib.bib15)]* enables conversational patterns between agents with role-based specialization. MetaGPT *[[7](#bib.bib7)]* assigns software engineering roles (architect, developer, tester) to different agents with structured output protocols. LangGraph *[[9](#bib.bib9)]* provides a graph-based state machine to define agent workflows with conditional edges and cycles.

Although these frameworks advance agent coordination, they share common limitations from an auditability perspective: (i) state is typically mutable and stored as snapshots rather than a change log; (ii) there is no native mechanism for deterministic replay of the complete decision trail; (iii) the blast radius of a compromised agent is not formally bounded by contracts. ESAA addresses these gaps by applying event sourcing as the fundamental state management paradigm. [Table˜1](#S2.T1 "In 2.2 Multi-Agent Frameworks ‣ 2 Related Work ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") presents a structured comparison.

_Table 1: Comparison of ESAA with contemporary multi-agent frameworks._

| Capability | AutoGen | MetaGPT | LangGraph | CrewAI | ESAA |
| --- | --- | --- | --- | --- | --- |
| Immutable event log | – | – | – | – | ✓ |
| Deterministic replay | – | – | – | – | ✓ |
| Boundary contracts | – | Partial | – | – | ✓ |
| Constrained JSON output | – | ✓ | – | – | ✓ |
| Multi-agent concurrency | ✓ | ✓ | ✓ | ✓ | ✓ |
| Hash-verified projection | – | – | – | – | ✓ |
| Role-based specialization | ✓ | ✓ | ✓ | ✓ | ✓ |
| "Done" immutability rule | – | – | – | – | ✓ |
| Blast radius containment | – | Partial | – | – | ✓ |

---

### 2.3Context Limits and Long-Horizon Degradation

Recent works point to systematic degradation in long context windows, with a drop in recall in the middle of the context (_lost-in-the-middle_), affecting tasks that depend on facts buried in logs, docs, or extensive histories *[[10](#bib.bib10)]*. This limitation creates recency bias and can induce the agent to ignore initial contracts, especially in environments requiring consistency with specifications and security policies.

---

### 2.4Event Sourcing and CQRS

Event Sourcing records every state change as an immutable event in an append-only log; the current state is a projection of these events *[[4](#bib.bib4)]*. Alongside this, CQRS separates write and read models to optimize consistency and queries, reducing complexity in systems with strong audit and traceability requirements *[[5](#bib.bib5)]*. ESAA transposes these principles to LLM-assisted software engineering: the agent does not "write state"; it emits intentions and proposed diffs that are validated and applied by a deterministic orchestrator.

---

### 2.5Constrained Output and Syntactic Structure

A practical bottleneck in agents is the _structure gap_: models generate probabilistic text, but systems require payloads compliant with schemas (JSON, API calls, patches). Constrained decoding and structured generation approaches guide sampling using grammars and schemas, reducing parsing failures and rejections *[[3](#bib.bib3), [16](#bib.bib16)]*. Inference and serving frameworks like SGLang also highlight the relevance of this layer by integrating mechanisms for structured outputs and high-throughput execution pipelines *[[14](#bib.bib14)]*.

---

## 3ESAA Architecture

ESAA establishes a strict separation between (i) the LLM’s heuristic cognition and (ii) the system’s deterministic execution. The agent does not have direct write permission to the project or the event store. Its role is to emit structured intentions and change proposals, always compliant with an output contract validatable by JSON Schema *[[1](#bib.bib1)]*.

[Figure˜1](#S3.F1 "In 3 ESAA Architecture ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") illustrates the complete orchestration cycle.

LLM Agent (intention) Orchestrator (deterministic) Event Store(. jsonl) Boundary Contract JSON Schema Validation Read-Model(. json)agent. resultappend eventprojectpurified viewoutput. rejected_Figure 1: ESAA Orchestration Cycle: the agent emits structured intentions validated by boundary contracts and JSON Schema; the orchestrator persists events in the append-only store and projects the read-model. The agent receives only a purified view, never the raw state._

### 3.1Canonical Artifacts

The ESAA implementation operates with a set of canonical artifacts (stored in . roadmap/):

1. (1)Event store (activity. jsonl): an append-only log of ordered events (event_seq), containing intentions, dispatches, effects, and run closures.
2. (2)Materialized view (roadmap. json): a read-model derived by pure projection; includes tasks, dependencies, indexes, and verification metadata (e. g., projection_hash_sha256).
3. (3)Boundary contracts (AGENT_CONTRACT. yaml, ORCHESTRATOR_CONTRACT. yaml): define permitted actions per task type (spec/impl/qa), output patterns, and hard prohibitions (e. g., denying direct file. write by the agent).
4. (4)PARCER profiles (PARCER_PROFILE.*. yaml): metaprompting profiles that suppress free-form output and force a strict JSON envelope. PARCER (Persona, Audience, Rules, Context, Execution, Response) defines six dimensions that constrain the agent’s output behavior, ensuring each agent receives instructions appropriate to its role with mandatory output schemas and specific prohibited actions per task type.

### 3.2Trace-First Model and Immutability

ESAA adopts a "trace-first" model: the event is recorded as a fact before any irreversible effect, allowing for audit and containment controls. The _immutability of done rule_ defines that completed tasks cannot regress. In case of a defect, an issue. report event creates a new correction path (hotfix) without reopening the history, preserving the decision trail.

### 3.3Determinism through Canonicalization and Hashing

To ensure reproducibility via replay, ESAA specifies deterministic canonicalization of the projected state and hash calculation. The idea follows the principle of invariant representation for cryptographic operations, as per JSON canonicalization schemes *[[13](#bib.bib13)]*. The SHA-256 hash of the canonicalized read-model (projection_hash_sha256) allows for the detection of divergence between projection and materialization *[[2](#bib.bib2)]*.

### 3.4Multi-Agent Dispatch and Concurrency

ESAA supports heterogeneous multi-agent orchestration through the append-only semantics of the event store. The orchestrator assigns tasks to agents based on role-based specialization (e. g., specification agents, implementation agents, QA agents) and tracks claims and completions per agent via correlation identifiers. Concurrent execution is naturally serialized at the event level: multiple agents can work in parallel, but their results are validated and appended sequentially, preserving total ordering in the log. This design allows the orchestrator to detect conflicts (e. g., overlapping file modifications) before applying effects.

---

### 3.1Canonical Artifacts

The ESAA implementation operates with a set of canonical artifacts (stored in . roadmap/):

1. (1)Event store (activity. jsonl): an append-only log of ordered events (event_seq), containing intentions, dispatches, effects, and run closures.
2. (2)Materialized view (roadmap. json): a read-model derived by pure projection; includes tasks, dependencies, indexes, and verification metadata (e. g., projection_hash_sha256).
3. (3)Boundary contracts (AGENT_CONTRACT. yaml, ORCHESTRATOR_CONTRACT. yaml): define permitted actions per task type (spec/impl/qa), output patterns, and hard prohibitions (e. g., denying direct file. write by the agent).
4. (4)PARCER profiles (PARCER_PROFILE.*. yaml): metaprompting profiles that suppress free-form output and force a strict JSON envelope. PARCER (Persona, Audience, Rules, Context, Execution, Response) defines six dimensions that constrain the agent’s output behavior, ensuring each agent receives instructions appropriate to its role with mandatory output schemas and specific prohibited actions per task type.

---

### 3.2Trace-First Model and Immutability

ESAA adopts a "trace-first" model: the event is recorded as a fact before any irreversible effect, allowing for audit and containment controls. The _immutability of done rule_ defines that completed tasks cannot regress. In case of a defect, an issue. report event creates a new correction path (hotfix) without reopening the history, preserving the decision trail.

---

### 3.3Determinism through Canonicalization and Hashing

To ensure reproducibility via replay, ESAA specifies deterministic canonicalization of the projected state and hash calculation. The idea follows the principle of invariant representation for cryptographic operations, as per JSON canonicalization schemes *[[13](#bib.bib13)]*. The SHA-256 hash of the canonicalized read-model (projection_hash_sha256) allows for the detection of divergence between projection and materialization *[[2](#bib.bib2)]*.

---

### 3.4Multi-Agent Dispatch and Concurrency

ESAA supports heterogeneous multi-agent orchestration through the append-only semantics of the event store. The orchestrator assigns tasks to agents based on role-based specialization (e. g., specification agents, implementation agents, QA agents) and tracks claims and completions per agent via correlation identifiers. Concurrent execution is naturally serialized at the event level: multiple agents can work in parallel, but their results are validated and appended sequentially, preserving total ordering in the log. This design allows the orchestrator to detect conflicts (e. g., overlapping file modifications) before applying effects.

---

## 4Methodology

### 4.1Architectural Intervention Design

The research follows an artifact-oriented technical validation design: an architecture is proposed (ESAA), formal contracts are defined (schemas, boundaries, event vocabulary), and reproducible execution is demonstrated in two case studies of increasing complexity. The unit of analysis is the orchestrator run, composed of a sequence of events in activity. jsonl and a derivable read-model in roadmap. json.

### 4.2Orchestrator Implementation and Validation Pipeline

The orchestrator executes a transactional pipeline: (i) validates agent output via JSON Schema and boundary rules; (ii) emits output. rejected for violations; (iii) applies effects via orchestrator. file. write; (iv) appends events to the event store; (v) reprojects roadmap. json; (vi) executes esaa verify via replay and hash comparison. The choice of JSON Schema as a formal contract aims to reduce ambiguity and create observable, treatable failures *[[1](#bib.bib1)]*.

### 4.3Experimental Setup and Reproducibility

For open reproducibility purposes, the project’s public repository provides the architecture in its initial state (_clean state_), containing only the initialization event (run. init) in the event store. This allows other researchers to execute the pipeline from scratch and observe the deterministic state derivation documented in this study.

---

### 4.1Architectural Intervention Design

The research follows an artifact-oriented technical validation design: an architecture is proposed (ESAA), formal contracts are defined (schemas, boundaries, event vocabulary), and reproducible execution is demonstrated in two case studies of increasing complexity. The unit of analysis is the orchestrator run, composed of a sequence of events in activity. jsonl and a derivable read-model in roadmap. json.

---

### 4.2Orchestrator Implementation and Validation Pipeline

The orchestrator executes a transactional pipeline: (i) validates agent output via JSON Schema and boundary rules; (ii) emits output. rejected for violations; (iii) applies effects via orchestrator. file. write; (iv) appends events to the event store; (v) reprojects roadmap. json; (vi) executes esaa verify via replay and hash comparison. The choice of JSON Schema as a formal contract aims to reduce ambiguity and create observable, treatable failures *[[1](#bib.bib1)]*.

---

### 4.3Experimental Setup and Reproducibility

For open reproducibility purposes, the project’s public repository provides the architecture in its initial state (_clean state_), containing only the initialization event (run. init) in the event store. This allows other researchers to execute the pipeline from scratch and observe the deterministic state derivation documented in this study.

---

## 5Case Studies

Two case studies validate the ESAA architecture across different complexity scales and agent compositions.

### 5.1Case Study 1: Landing Page (Single-Agent Composition)

The example-landingpage project was structured as a pipeline with 9 sequential tasks (T-1000 to T-1210), covering specification, implementation, and QA. To simulate orchestrator behavior and validate the agents’ability to adhere to constrained output contracts, the execution and artifact generation were conducted using a composition of advanced tools: GPT-5.3-Codex, Claude Code opus 4.6 (integrated with VSCode), and Antigravity (operating with the Gemini 3 Pro model).

The consolidation of this workflow generated a local event store with 49 events, concluding with run. status=success and verify_status=ok. The produced artifact set included four specifications in . roadmap/specs/, code files in src/ (vanilla HTML/CSS/JS), and QA reports in . roadmap/qa/.

The execution followed the cycle: attempt. create

→

\to

orchestrator. dispatch

→

\to

agent. result

→

\to

orchestrator. file. write

→

\to

task. update

→

\to

 (repeat)

→

\to

verify. ok

→

\to

run. end. This trail materializes the idea that the project state is derived from facts, not direct edits *[[4](#bib.bib4)]*.

### 5.2Case Study 2: Clinical Dashboard (Multi-Agent Concurrency)

The clinic-asr project represents a substantially more complex validation scenario: a clinical dashboard system (POC) with real-time audio transcription capabilities, covering database schema design, REST API contracts, SSE event vocabulary, SPA architecture, configuration management, security policies, and end-to-end testing.

#### 5.2.1Project Structure

The roadmap comprised 15 phases (PH-19 to PH-33) and 50 tasks distributed across 7 components: web UI (16 tasks), API (11), database (7), testing (7), configuration (4), observability (3), and documentation/release (2). Tasks were organized into a dependency graph with a defined critical path of 9 tasks, from data persistence to final release.

#### 5.2.2Multi-Agent Orchestration

Four heterogeneous LLM agents were assigned to tasks based on specialization:

- •Claude Sonnet 4.6 —10 tasks: database schema specification, API contract definition, configuration system design;
- •Codex GPT-5 —10 tasks: UI architecture specification, configuration audit, API implementation, testing;
- •Antigravity (Gemini 3 Pro) —5 tasks: persistence implementation, repository layer, service integration;
- •Claude Opus 4.6 —5 tasks: security and privacy documentation, observability strategy, deployment guides.

#### 5.2.3Event Store Analysis

The execution generated 86 events over approximately 15 hours (2026-02-19 09:00 to 2026-02-20 00:14, America/Sao_Paulo), with the following distribution: 30 claims, 30 completions, 17 promotions (backlog

→

\to

 ready), 8 phase completions, and 1 version initialization. All 30 task completions had acceptance_results with positive validation.

A key observation is the evidence of _concurrent multi-agent execution_: at timestamp 2026-02-19T21:55, six claims were recorded within the same minute—Antigravity completing task T-2601 while Claude Opus 4.6 simultaneously claimed five tasks (T-2301, T-2302, T-2303, T-2401, T-2403). This demonstrates that the event store’s append-only semantics naturally serializes concurrent agent activities while preserving the temporal ordering necessary for replay.

#### 5.2.4Progression and Current State

At the time of analysis, 31 of 50 tasks (62%) were completed (done), 2 were in the ready state, and 17 remained in the backlog. Eight out of fifteen phases were completed. The remaining phases cover UI implementation (PH-27 to PH-32) and final hardening/release (PH-33), demonstrating that ESAA can manage an ongoing project with partial completion while maintaining full traceability of concluded work.

### 5.3Comparative Summary

[Table˜2](#S5.T2 "In 5.3 Comparative Summary ‣ 5 Case Studies ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") presents a quantitative comparison of the two case studies.

_Table 2: Quantitative comparison of the two case studies._

| Metric | CS1: Landing Page | CS2: Clinic ASR |
| --- | --- | --- |
| Total tasks | 9 | 50 |
| Total events | 49 | 86 |
| Distinct agents | 3 (composition) | 4 (concurrent) |
| Phases | 1 pipeline | 15 (8 completed) |
| Components | 3 (spec/impl/QA) | 7 (DB, API, UI, tests, config, obs, docs) |
| Duration | Single session | ∼ \sim15 hours |
| output. rejected | 0 | 0 |
| verify_status | ok | ok (partial—31/50) |
| Concurrent claims | No | Yes (6 in 1 min) |
| Dependency graph | Linear | DAG with critical path |
| Event vocabulary | 15 types | 5 types (simplified) |
| Acceptance criteria | Implicit | Explicit per task |

The evolution from CS1 to CS2 reveals a natural maturation of the protocol: the event vocabulary was simplified from 15 to 5 action types, suggesting that the core lifecycle (claim

→

\to

complete with promote for backlog management) captures essential state transitions. Internal orchestrator events (e. g., orchestrator. dispatch, orchestrator. file. write) can be inferred from the sequence rather than explicitly logged, reducing log verbosity while preserving traceability.

---

### 5.1Case Study 1: Landing Page (Single-Agent Composition)

The example-landingpage project was structured as a pipeline with 9 sequential tasks (T-1000 to T-1210), covering specification, implementation, and QA. To simulate orchestrator behavior and validate the agents’ability to adhere to constrained output contracts, the execution and artifact generation were conducted using a composition of advanced tools: GPT-5.3-Codex, Claude Code opus 4.6 (integrated with VSCode), and Antigravity (operating with the Gemini 3 Pro model).

The consolidation of this workflow generated a local event store with 49 events, concluding with run. status=success and verify_status=ok. The produced artifact set included four specifications in . roadmap/specs/, code files in src/ (vanilla HTML/CSS/JS), and QA reports in . roadmap/qa/.

The execution followed the cycle: attempt. create

→

\to

orchestrator. dispatch

→

\to

agent. result

→

\to

orchestrator. file. write

→

\to

task. update

→

\to

 (repeat)

→

\to

verify. ok

→

\to

run. end. This trail materializes the idea that the project state is derived from facts, not direct edits *[[4](#bib.bib4)]*.

---

### 5.2Case Study 2: Clinical Dashboard (Multi-Agent Concurrency)

The clinic-asr project represents a substantially more complex validation scenario: a clinical dashboard system (POC) with real-time audio transcription capabilities, covering database schema design, REST API contracts, SSE event vocabulary, SPA architecture, configuration management, security policies, and end-to-end testing.

#### 5.2.1Project Structure

The roadmap comprised 15 phases (PH-19 to PH-33) and 50 tasks distributed across 7 components: web UI (16 tasks), API (11), database (7), testing (7), configuration (4), observability (3), and documentation/release (2). Tasks were organized into a dependency graph with a defined critical path of 9 tasks, from data persistence to final release.

#### 5.2.2Multi-Agent Orchestration

Four heterogeneous LLM agents were assigned to tasks based on specialization:

- •Claude Sonnet 4.6 —10 tasks: database schema specification, API contract definition, configuration system design;
- •Codex GPT-5 —10 tasks: UI architecture specification, configuration audit, API implementation, testing;
- •Antigravity (Gemini 3 Pro) —5 tasks: persistence implementation, repository layer, service integration;
- •Claude Opus 4.6 —5 tasks: security and privacy documentation, observability strategy, deployment guides.

#### 5.2.3Event Store Analysis

The execution generated 86 events over approximately 15 hours (2026-02-19 09:00 to 2026-02-20 00:14, America/Sao_Paulo), with the following distribution: 30 claims, 30 completions, 17 promotions (backlog

→

\to

 ready), 8 phase completions, and 1 version initialization. All 30 task completions had acceptance_results with positive validation.

A key observation is the evidence of _concurrent multi-agent execution_: at timestamp 2026-02-19T21:55, six claims were recorded within the same minute—Antigravity completing task T-2601 while Claude Opus 4.6 simultaneously claimed five tasks (T-2301, T-2302, T-2303, T-2401, T-2403). This demonstrates that the event store’s append-only semantics naturally serializes concurrent agent activities while preserving the temporal ordering necessary for replay.

#### 5.2.4Progression and Current State

At the time of analysis, 31 of 50 tasks (62%) were completed (done), 2 were in the ready state, and 17 remained in the backlog. Eight out of fifteen phases were completed. The remaining phases cover UI implementation (PH-27 to PH-32) and final hardening/release (PH-33), demonstrating that ESAA can manage an ongoing project with partial completion while maintaining full traceability of concluded work.

---

#### 5.2.1Project Structure

The roadmap comprised 15 phases (PH-19 to PH-33) and 50 tasks distributed across 7 components: web UI (16 tasks), API (11), database (7), testing (7), configuration (4), observability (3), and documentation/release (2). Tasks were organized into a dependency graph with a defined critical path of 9 tasks, from data persistence to final release.

---

#### 5.2.2Multi-Agent Orchestration

Four heterogeneous LLM agents were assigned to tasks based on specialization:

- •Claude Sonnet 4.6 —10 tasks: database schema specification, API contract definition, configuration system design;
- •Codex GPT-5 —10 tasks: UI architecture specification, configuration audit, API implementation, testing;
- •Antigravity (Gemini 3 Pro) —5 tasks: persistence implementation, repository layer, service integration;
- •Claude Opus 4.6 —5 tasks: security and privacy documentation, observability strategy, deployment guides.

---

#### 5.2.3Event Store Analysis

The execution generated 86 events over approximately 15 hours (2026-02-19 09:00 to 2026-02-20 00:14, America/Sao_Paulo), with the following distribution: 30 claims, 30 completions, 17 promotions (backlog

→

\to

 ready), 8 phase completions, and 1 version initialization. All 30 task completions had acceptance_results with positive validation.

A key observation is the evidence of _concurrent multi-agent execution_: at timestamp 2026-02-19T21:55, six claims were recorded within the same minute—Antigravity completing task T-2601 while Claude Opus 4.6 simultaneously claimed five tasks (T-2301, T-2302, T-2303, T-2401, T-2403). This demonstrates that the event store’s append-only semantics naturally serializes concurrent agent activities while preserving the temporal ordering necessary for replay.

---

#### 5.2.4Progression and Current State

At the time of analysis, 31 of 50 tasks (62%) were completed (done), 2 were in the ready state, and 17 remained in the backlog. Eight out of fifteen phases were completed. The remaining phases cover UI implementation (PH-27 to PH-32) and final hardening/release (PH-33), demonstrating that ESAA can manage an ongoing project with partial completion while maintaining full traceability of concluded work.

---

### 5.3Comparative Summary

[Table˜2](#S5.T2 "In 5.3 Comparative Summary ‣ 5 Case Studies ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") presents a quantitative comparison of the two case studies.

_Table 2: Quantitative comparison of the two case studies._

| Metric | CS1: Landing Page | CS2: Clinic ASR |
| --- | --- | --- |
| Total tasks | 9 | 50 |
| Total events | 49 | 86 |
| Distinct agents | 3 (composition) | 4 (concurrent) |
| Phases | 1 pipeline | 15 (8 completed) |
| Components | 3 (spec/impl/QA) | 7 (DB, API, UI, tests, config, obs, docs) |
| Duration | Single session | ∼ \sim15 hours |
| output. rejected | 0 | 0 |
| verify_status | ok | ok (partial—31/50) |
| Concurrent claims | No | Yes (6 in 1 min) |
| Dependency graph | Linear | DAG with critical path |
| Event vocabulary | 15 types | 5 types (simplified) |
| Acceptance criteria | Implicit | Explicit per task |

The evolution from CS1 to CS2 reveals a natural maturation of the protocol: the event vocabulary was simplified from 15 to 5 action types, suggesting that the core lifecycle (claim

→

\to

complete with promote for backlog management) captures essential state transitions. Internal orchestrator events (e. g., orchestrator. dispatch, orchestrator. file. write) can be inferred from the sequence rather than explicitly logged, reducing log verbosity while preserving traceability.

---

## 6Results and Discussion

### 6.1Structural Compliance and Reduction of Parsing Failures

By restricting agent output to a validatable JSON envelope and a small vocabulary of actions, ESAA reduces the probability of parsing failures and "out-of-contract outputs." In both case studies, the output. rejected count was zero, suggesting that the constrained output regime was sufficient to keep the agents (operated by four distinct LLM providers) within the protocol. This strategy is consistent with the goals of structured generation libraries, which prioritize syntactic compliance to enable deterministic execution *[[3](#bib.bib3), [16](#bib.bib16)]*.

### 6.2Auditability and Debugging through Replay

The primary output of ESAA is not just the generated code, but the complete trail of events and their effects. This allows for "time-travel debugging" via replay: reprocessing the event store from event zero to reconstruct the read-model exactly and verify divergences. Using SHA-256 hashing as a state projection commitment follows best practices for change detection and message integrity *[[2](#bib.bib2)]*. To reduce serialization ambiguities, canonicalization through key sorting and string normalization aligns with the JSON Canonicalization Scheme *[[13](#bib.bib13)]*.

### 6.3Multi-Agent Coordination via Event Store

The clinic-asr case study demonstrates that the event store serves as a natural coordination mechanism for heterogeneous agents. Three properties emerge from the data:

1. 1. Serialized accountability: despite concurrent execution, the append-only log preserves total ordering, allowing precise attribution of each state change to a specific agent and task.
2. 2. Specialization tracking: the log reveals agent specialization patterns—Claude Sonnet handled specification tasks, Codex GPT-5 handled UI and testing, Antigravity handled implementation, and Claude Opus handled cross-cutting concerns. This information is forensically recoverable solely from the event store.
3. 3. Phase-gated progression: the promote → \to claim → \to complete → \to phase. complete sequence enforces dependency ordering without requiring agents to be aware of each other, reducing coordination overhead.

### 6.4Context Efficiency and Degradation Mitigation

ESAA proposes that the agent should not carry long-term memory in the raw prompt; it should receive a purified view (roadmap + relevant facts) derived from the log. This approach addresses limitations like _lost-in-the-middle_, as the orchestrator selectively injects information needed for the current step, rather than relying on the model to maintain all details across long windows *[[10](#bib.bib10)]*. In the clinic-asr case, with 50 tasks and complex interdependencies, the purified view mechanism was essential for maintaining agent coherence over the 15 hours of execution.

### 6.5Security and Blast Radius

By denying direct writing and imposing boundaries per task type, ESAA reduces the blast radius of a compromised agent (e. g., via prompt injection). The strategy aligns with broad recommendations of least privilege and prevention of integrity and logging failures in applications, as synthesized in critical risk guides *[[11](#bib.bib11)]*. It is also worth noting that parsing/grammar layers can have availability vulnerabilities when used in high-throughput pipelines; therefore, the implementation must treat grammar engines as components to be monitored and versioned *[[6](#bib.bib6)]*.

### 6.6Overhead Considerations

The ESAA architecture introduces overhead in three dimensions: (i) _token overhead_ from the JSON envelope and validation preamble in each agent invocation (estimated at 200–500 tokens per invocation); (ii) _latency overhead_ from schema validation and event persistence (sub-second per event in both case studies); and (iii) _storage overhead_ of the append-only log (the 86-event log of clinic-asr occupies approximately 15 KB). These costs are negligible compared to LLM inference costs and provide substantial returns in auditability and reproducibility.

---

### 6.1Structural Compliance and Reduction of Parsing Failures

By restricting agent output to a validatable JSON envelope and a small vocabulary of actions, ESAA reduces the probability of parsing failures and "out-of-contract outputs." In both case studies, the output. rejected count was zero, suggesting that the constrained output regime was sufficient to keep the agents (operated by four distinct LLM providers) within the protocol. This strategy is consistent with the goals of structured generation libraries, which prioritize syntactic compliance to enable deterministic execution *[[3](#bib.bib3), [16](#bib.bib16)]*.

---

### 6.2Auditability and Debugging through Replay

The primary output of ESAA is not just the generated code, but the complete trail of events and their effects. This allows for "time-travel debugging" via replay: reprocessing the event store from event zero to reconstruct the read-model exactly and verify divergences. Using SHA-256 hashing as a state projection commitment follows best practices for change detection and message integrity *[[2](#bib.bib2)]*. To reduce serialization ambiguities, canonicalization through key sorting and string normalization aligns with the JSON Canonicalization Scheme *[[13](#bib.bib13)]*.

---

### 6.3Multi-Agent Coordination via Event Store

The clinic-asr case study demonstrates that the event store serves as a natural coordination mechanism for heterogeneous agents. Three properties emerge from the data:

1. 1. Serialized accountability: despite concurrent execution, the append-only log preserves total ordering, allowing precise attribution of each state change to a specific agent and task.
2. 2. Specialization tracking: the log reveals agent specialization patterns—Claude Sonnet handled specification tasks, Codex GPT-5 handled UI and testing, Antigravity handled implementation, and Claude Opus handled cross-cutting concerns. This information is forensically recoverable solely from the event store.
3. 3. Phase-gated progression: the promote → \to claim → \to complete → \to phase. complete sequence enforces dependency ordering without requiring agents to be aware of each other, reducing coordination overhead.

---

### 6.4Context Efficiency and Degradation Mitigation

ESAA proposes that the agent should not carry long-term memory in the raw prompt; it should receive a purified view (roadmap + relevant facts) derived from the log. This approach addresses limitations like _lost-in-the-middle_, as the orchestrator selectively injects information needed for the current step, rather than relying on the model to maintain all details across long windows *[[10](#bib.bib10)]*. In the clinic-asr case, with 50 tasks and complex interdependencies, the purified view mechanism was essential for maintaining agent coherence over the 15 hours of execution.

---

### 6.5Security and Blast Radius

By denying direct writing and imposing boundaries per task type, ESAA reduces the blast radius of a compromised agent (e. g., via prompt injection). The strategy aligns with broad recommendations of least privilege and prevention of integrity and logging failures in applications, as synthesized in critical risk guides *[[11](#bib.bib11)]*. It is also worth noting that parsing/grammar layers can have availability vulnerabilities when used in high-throughput pipelines; therefore, the implementation must treat grammar engines as components to be monitored and versioned *[[6](#bib.bib6)]*.

---

### 6.6Overhead Considerations

The ESAA architecture introduces overhead in three dimensions: (i) _token overhead_ from the JSON envelope and validation preamble in each agent invocation (estimated at 200–500 tokens per invocation); (ii) _latency overhead_ from schema validation and event persistence (sub-second per event in both case studies); and (iii) _storage overhead_ of the append-only log (the 86-event log of clinic-asr occupies approximately 15 KB). These costs are negligible compared to LLM inference costs and provide substantial returns in auditability and reproducibility.

---

## 7Threats to Validity

Internal validity. Both case studies were executed in controlled environments with defined project scopes. Although the clinic-asr pipeline demonstrates significantly higher complexity than the landing page (50 vs. 9 tasks, 4 agents, 7 components), strong causality regarding performance in enterprise repositories cannot be concluded without a larger sample. Furthermore, the use of temperature 0.0 reduces variability but may not reflect setups that explore sampling diversity *[[17](#bib.bib17)]*.

External validity. Results from a landing page and a clinical POC do not necessarily generalize to domains with continuous integration pipelines, database migrations, or monorepos at scale. Benchmarks on real issues suggest that repository complexity directly influences agent success, and ESAA must be tested on workloads aligned with SWE-bench and harder variants *[[8](#bib.bib8), [12](#bib.bib12)]*.

Construct validity. Measures such as output. rejected and verify_status capture compliance and state reproducibility but do not directly measure "design quality" or "business value" of the software. To broaden constructs, it is recommended to include human evaluations and quality metrics (e. g., test coverage, accessibility, maintainability).

Conclusion validity. Two case studies (n=2) improve upon the initial single-case design but still limit statistical inferences. The appropriate conclusion is that ESAA demonstrates technical feasibility and produces verifiable invariants in scenarios of different complexities, not that it maximizes performance on any benchmark.

---

## 8Conclusion and Future Work

ESAA proposes a paradigm shift: treating LLMs as intention emitters under contract, rather than "developers" with unrestricted permissions. By adopting Event Sourcing as the source of truth and applying verifiable projections through replay, the architecture offers native auditability, operational immutability, and state reproducibility *[[4](#bib.bib4)]*. In parallel, the use of formal contracts and constrained output reduces the structure gap and enables a deterministic execution pipeline *[[1](#bib.bib1), [3](#bib.bib3)]*. The two case studies provide complementary evidence: the landing page demonstrates the architecture’s core mechanics in a controlled single-pipeline scenario, while clinic-asr validates multi-agent concurrent orchestration with heterogeneous LLMs, complex dependency graphs, and phase-gated progression in a real-world application domain.

Future work includes: (i) an official CLI (esaa init/run/verify) with integration to remote repositories; (ii) conflict detection and resolution strategies for concurrent file modifications; (iii) automated time-travel debugging with visual diff comparison of projections at arbitrary event points; (iv) systematic evaluation on real-world issue benchmarks (SWE-bench) and enterprise-scale projects *[[8](#bib.bib8), [12](#bib.bib12)]*; and (v) formal verification of orchestrator invariants using model checking techniques.

---

## References

- [1] JSON Schema. (2020). JSON Schema specification (Draft 2020-12). [https://json-schema. org/draft/2020-12/json-schema-core. html](https://json-schema.org/draft/2020-12/json-schema-core.html)
- [2] Dang, Q. H. (2013). Changes in Federal Information Processing Standard (FIPS) 180-4, Secure Hash Standard. National Institute of Standards and Technology. [https://www. nist. gov/publications/changes-federal-information-processing-standard-fips-180-4-secure-hash-standard](https://www.nist.gov/publications/changes-federal-information-processing-standard-fips-180-4-secure-hash-standard)
- [3] Outlines. (n. d.). Outlines: Structured generation for LLMs (software). GitHub. [https://github. com/dottxt-ai/outlines](https://github.com/dottxt-ai/outlines)
- [4] Fowler, M. (2005). Event sourcing. MartinFowler. com. [https://martinfowler. com/eaaDev/EventSourcing. html](https://martinfowler.com/eaaDev/EventSourcing.html)
- [5] Fowler, M. (2011). CQRS. MartinFowler. com. [https://martinfowler. com/bliki/CQRS. html](https://martinfowler.com/bliki/CQRS.html)
- [6] GitLab. (2025). Advisory: DoS vulnerability in XGrammar used in vLLM (GHSA report mirror). [https://gitlab. com/gitlab-org/advisories/GHSA-x73x-g4m2-94q2](https://gitlab.com/gitlab-org/advisories/GHSA-x73x-g4m2-94q2)
- [7] Hong, S., et al. (2023). MetaGPT: Meta programming for multi-agent collaborative framework. arXiv. [https://arxiv. org/abs/2308.00352](https://arxiv.org/abs/2308.00352)
- [8] Jimenez, C. E., Yang, J., Narasimhan, K., & Press, O. (2024). SWE-bench: Can language models resolve real-world GitHub issues? In _Proceedings of the 12th International Conference on Learning Representations (ICLR)_. [https://openreview. net/forum? id=VTF8yN1YNt](https://openreview.net/forum?id=VTF8yN1YNt)
- [9] LangChain. (2024). LangGraph: Build resilient language agents as graphs. [https://github. com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- [10] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., & Liang, P. (2024). Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics_. [https://aclanthology. org/2024. tacl-1.9/](https://aclanthology.org/2024.tacl-1.9/)
- [11] OWASP. (2021). OWASP Top 10:2021. [https://owasp. org/Top10/2021/](https://owasp.org/Top10/2021/)
- [12] OpenAI. (2024). Introducing SWE-bench Verified. [https://openai. com/index/introducing-swe-bench-verified/](https://openai.com/index/introducing-swe-bench-verified/)
- [13] Rundgren, A., Jordan, B., & Erdtman, S. (2020). RFC 8785: JSON Canonicalization Scheme (JCS). IETF. [https://datatracker. ietf. org/doc/html/rfc8785](https://datatracker.ietf.org/doc/html/rfc8785)
- [14] sgl-project. (n. d.). SGLang: Fast serving framework for LLMs (software). GitHub. [https://github. com/sgl-project/sglang](https://github.com/sgl-project/sglang)
- [15] Wu, Q., et al. (2023). AutoGen: Enabling next-gen LLM applications via multi-agent conversation. arXiv. [https://arxiv. org/abs/2308.08155](https://arxiv.org/abs/2308.08155)
- [16] mlc-ai. (n. d.). XGrammar: Efficient, flexible, and portable structured generation engine (software). GitHub. [https://github. com/mlc-ai/xgrammar](https://github.com/mlc-ai/xgrammar)
- [17] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing reasoning and acting in language models. arXiv. [https://arxiv. org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

---

## Appendix AAgent Output Contract JSON Schema

[⬇](https://arxiv.org/data:text/plain;base64,ewogICIkc2NoZW1hIjogImh0dHBzOi8vanNvbi1zY2hlbWEub3JnL2RyYWZ0LzIwMjAtMTIvc2NoZW1hIiwKICAiJGlkIjogImh0dHBzOi8vZXNhYS5kZXYvc2NoZW1hcy9hZ2VudC1vdXRwdXQtdjAuMy4wLmpzb24iLAogICJ0aXRsZSI6ICJFU0FBIC0gQWdlbnQgT3V0cHV0IENvbnRyYWN0IiwKICAidHlwZSI6ICJvYmplY3QiLAogICJhZGRpdGlvbmFsUHJvcGVydGllcyI6IGZhbHNlLAogICJyZXF1aXJlZCI6IFsic2NoZW1hX3ZlcnNpb24iLCJjb3JyZWxhdGlvbl9pZCIsInRhc2tfaWQiLAogICAgImF0dGVtcHRfaWQiLCJhY3RvciIsImFjdGlvbiIsImlkZW1wb3RlbmN5X2tleSIsInBheWxvYWQiXSwKICAicHJvcGVydGllcyI6IHsKICAgICJzY2hlbWFfdmVyc2lvbiI6IHsgImNvbnN0IjogIjAuMy4wIiB9LAogICAgImNvcnJlbGF0aW9uX2lkIjogeyAidHlwZSI6ICJzdHJpbmciLCAibWluTGVuZ3RoIjogOCB9LAogICAgInRhc2tfaWQiOiAgICAgICAgeyAidHlwZSI6ICJzdHJpbmciLCAibWluTGVuZ3RoIjogMyB9LAogICAgImF0dGVtcHRfaWQiOiAgICAgeyAidHlwZSI6ICJzdHJpbmciLCAibWluTGVuZ3RoIjogOCB9LAogICAgImFjdG9yIjogICAgICAgICAgeyAidHlwZSI6ICJzdHJpbmciLCAicGF0dGVybiI6ICJeYWdlbnQtLioiIH0sCiAgICAiYWN0aW9uIjogICAgICAgICB7ICJlbnVtIjogWyJhZ2VudC5yZXN1bHQiLCAiaXNzdWUucmVwb3J0Il0gfSwKICAgICJpZGVtcG90ZW5jeV9rZXkiOnsgInR5cGUiOiAic3RyaW5nIiB9LAogICAgInBheWxvYWQiOiB7CiAgICAgICJ0eXBlIjogIm9iamVjdCIsCiAgICAgICJhZGRpdGlvbmFsUHJvcGVydGllcyI6IGZhbHNlLAogICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAic3VtbWFyeSI6ICAgeyAidHlwZSI6ICJzdHJpbmciLCAibWF4TGVuZ3RoIjogMjAwMCB9LAogICAgICAgICJwcm9wb3NhbHMiOiB7CiAgICAgICAgICAidHlwZSI6ICJhcnJheSIsCiAgICAgICAgICAiaXRlbXMiOiB7CiAgICAgICAgICAgICJ0eXBlIjogIm9iamVjdCIsCiAgICAgICAgICAgICJyZXF1aXJlZCI6IFsidHlwZSIsICJwYXRoIiwgInBhdGNoIl0sCiAgICAgICAgICAgICJwcm9wZXJ0aWVzIjogewogICAgICAgICAgICAgICJ0eXBlIjogIHsgImNvbnN0IjogImZpbGVfcGF0Y2giIH0sCiAgICAgICAgICAgICAgInBhdGgiOiAgeyAidHlwZSI6ICJzdHJpbmciLAogICAgICAgICAgICAgICAgICAgICAgICAgInBhdHRlcm4iOiAiXihcXC5yb2FkbWFwL3xzcmMvKSIgfSwKICAgICAgICAgICAgICAicGF0Y2giOiB7ICJ0eXBlIjogInN0cmluZyIsICJtaW5MZW5ndGgiOiAxIH0KICAgICAgICAgICAgfQogICAgICAgICAgfQogICAgICAgIH0sCiAgICAgICAgImlzc3VlIjogewogICAgICAgICAgInR5cGUiOiAib2JqZWN0IiwKICAgICAgICAgICJyZXF1aXJlZCI6IFsidGl0bGUiLCAiZGV0YWlscyIsICJzZXZlcml0eSJdLAogICAgICAgICAgInByb3BlcnRpZXMiOiB7CiAgICAgICAgICAgICJ0aXRsZSI6ICAgIHsgInR5cGUiOiAic3RyaW5nIiB9LAogICAgICAgICAgICAiZGV0YWlscyI6ICB7ICJ0eXBlIjogInN0cmluZyIgfSwKICAgICAgICAgICAgInNldmVyaXR5IjogeyAiZW51bSI6IFsibG93IiwibWVkaXVtIiwiaGlnaCIsImNyaXRpY2FsIl0gfQogICAgICAgICAgfQogICAgICAgIH0KICAgICAgfQogICAgfQogIH0KfQ==)

{

"$schema":"https://json-schema. org/draft/2020-12/schema",

"$id":"https://esaa. dev/schemas/agent-output-v0.3.0. json",

"title":"ESAA-AgentOutputContract",

"type":"object",

"additionalProperties": false,

"required":["schema_version","correlation_id","task_id",

"attempt_id","actor","action","idempotency_key","payload"],

"properties":{

"schema_version":{"const":"0.3.0"},

"correlation_id":{"type":"string","minLength":8},

"task_id":{"type":"string","minLength":3},

"attempt_id":{"type":"string","minLength":8},

"actor":{"type":"string","pattern":"^agent-.*"},

"action":{"enum":["agent. result","issue. report"]},

"idempotency_key":{"type":"string"},

"payload":{

"type":"object",

"additionalProperties": false,

"properties":{

"summary":{"type":"string","maxLength":2000},

"proposals":{

"type":"array",

"items":{

"type":"object",

"required":["type","path","patch"],

"properties":{

"type":{"const":"file_patch"},

"path":{"type":"string",

"pattern":"^(\\. roadmap/|src/)"},

"patch":{"type":"string","minLength":1}

}

}

},

"issue":{

"type":"object",

"required":["title","details","severity"],

"properties":{

"title":{"type":"string"},

"details":{"type":"string"},

"severity":{"enum":["low","medium","high","critical"]}

}

}

}

}

}

}

---

## Appendix BRoadmap Read-Model JSON Schema

[⬇](https://arxiv.org/data:text/plain;base64,ewogICIkc2NoZW1hIjogImh0dHBzOi8vanNvbi1zY2hlbWEub3JnL2RyYWZ0LzIwMjAtMTIvc2NoZW1hIiwKICAiJGlkIjogImh0dHBzOi8vZXNhYS5kZXYvc2NoZW1hcy9yb2FkbWFwLXYwLjMuMC5qc29uIiwKICAidGl0bGUiOiAiRVNBQSAtIFJvYWRtYXAgUmVhZC1Nb2RlbCIsCiAgInR5cGUiOiAib2JqZWN0IiwKICAicmVxdWlyZWQiOiBbInNjaGVtYV92ZXJzaW9uIiwicHJvamVjdCIsInJ1biIsInRhc2tzIiwiaW5kZXhlcyJdLAogICJwcm9wZXJ0aWVzIjogewogICAgInNjaGVtYV92ZXJzaW9uIjogeyAiY29uc3QiOiAiMC4zLjAiIH0sCiAgICAicHJvamVjdCI6IHsKICAgICAgInR5cGUiOiAib2JqZWN0IiwKICAgICAgInJlcXVpcmVkIjogWyJuYW1lIiwgImNyZWF0ZWRfYXQiLCAiYXVkaXRfc2NvcGUiXSwKICAgICAgInByb3BlcnRpZXMiOiB7CiAgICAgICAgIm5hbWUiOiAgICAgICAgeyAidHlwZSI6ICJzdHJpbmciIH0sCiAgICAgICAgImNyZWF0ZWRfYXQiOiAgeyAidHlwZSI6ICJzdHJpbmciIH0sCiAgICAgICAgImF1ZGl0X3Njb3BlIjogeyAidHlwZSI6ICJzdHJpbmciIH0KICAgICAgfQogICAgfSwKICAgICJydW4iOiB7CiAgICAgICJ0eXBlIjogIm9iamVjdCIsCiAgICAgICJyZXF1aXJlZCI6IFsicnVuX2lkIiwic3RhdHVzIiwibGFzdF9ldmVudF9zZXEiLAogICAgICAgICAgICAgICAgICAgICJsYXN0X2V2ZW50X3RzIiwidmVyaWZ5X3N0YXR1cyJdLAogICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAicnVuX2lkIjogICAgICAgeyAidHlwZSI6ICJzdHJpbmciIH0sCiAgICAgICAgInN0YXR1cyI6ICAgICAgIHsgImVudW0iOiBbImluaXRpYWxpemVkIiwicnVubmluZyIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJzdWNjZXNzIiwiZmFpbGVkIl0gfSwKICAgICAgICAibGFzdF9ldmVudF9zZXEiOiAgICAgICAgICAgeyAidHlwZSI6ICJpbnRlZ2VyIiwgIm1pbmltdW0iOiAwIH0sCiAgICAgICAgImxhc3RfZXZlbnRfdHMiOiAgICAgICAgICAgIHsgInR5cGUiOiAic3RyaW5nIiB9LAogICAgICAgICJwcm9qZWN0aW9uX2hhc2hfc2hhMjU2IjogICB7ICJ0eXBlIjogInN0cmluZyIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInBhdHRlcm4iOiAiXlthLWYwLTldezY0fSQiIH0sCiAgICAgICAgInZlcmlmeV9zdGF0dXMiOiAgICAgICAgICAgIHsgImVudW0iOiBbIm9rIiwibWlzbWF0Y2giLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiY29ycnVwdGVkIl0gfQogICAgICB9CiAgICB9LAogICAgInRhc2tzIjogewogICAgICAidHlwZSI6ICJhcnJheSIsCiAgICAgICJpdGVtcyI6IHsKICAgICAgICAidHlwZSI6ICJvYmplY3QiLAogICAgICAgICJyZXF1aXJlZCI6IFsidGFza19pZCIsImtpbmQiLCJ0aXRsZSIsInN0YXRlIiwKICAgICAgICAgICAgICAgICAgICAgImRlcGVuZHNfb24iLCJmaWxlcyJdLAogICAgICAgICJwcm9wZXJ0aWVzIjogewogICAgICAgICAgInRhc2tfaWQiOiAgICB7ICJ0eXBlIjogInN0cmluZyIgfSwKICAgICAgICAgICJraW5kIjogICAgICAgeyAiZW51bSI6IFsic3BlYyIsImltcGwiLCJxYSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJlbWVyZ2VuY3lfcGF0Y2giXSB9LAogICAgICAgICAgInRpdGxlIjogICAgICB7ICJ0eXBlIjogInN0cmluZyIgfSwKICAgICAgICAgICJzdGF0ZSI6ICAgICAgeyAiZW51bSI6IFsidG9kbyIsImluX3Byb2dyZXNzIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImJsb2NrZWQiLCJkb25lIl0gfSwKICAgICAgICAgICJkZXBlbmRzX29uIjogeyAidHlwZSI6ICJhcnJheSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIml0ZW1zIjogeyAidHlwZSI6ICJzdHJpbmciIH0gfSwKICAgICAgICAgICJmaWxlcyI6ICAgICAgeyAidHlwZSI6ICJhcnJheSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIml0ZW1zIjogeyAidHlwZSI6ICJzdHJpbmciIH0gfQogICAgICAgIH0KICAgICAgfQogICAgfSwKICAgICJpbmRleGVzIjogeyAidHlwZSI6ICJvYmplY3QiIH0KICB9Cn0=)

{

"$schema":"https://json-schema. org/draft/2020-12/schema",

"$id":"https://esaa. dev/schemas/roadmap-v0.3.0. json",

"title":"ESAA-RoadmapRead-Model",

"type":"object",

"required":["schema_version","project","run","tasks","indexes"],

"properties":{

"schema_version":{"const":"0.3.0"},

"project":{

"type":"object",

"required":["name","created_at","audit_scope"],

"properties":{

"name":{"type":"string"},

"created_at":{"type":"string"},

"audit_scope":{"type":"string"}

}

},

"run":{

"type":"object",

"required":["run_id","status","last_event_seq",

"last_event_ts","verify_status"],

"properties":{

"run_id":{"type":"string"},

"status":{"enum":["initialized","running",

"success","failed"]},

"last_event_seq":{"type":"integer","minimum":0},

"last_event_ts":{"type":"string"},

"projection_hash_sha256":{"type":"string",

"pattern":"^[a-f0-9]{64}$"},

"verify_status":{"enum":["ok","mismatch",

"corrupted"]}

}

},

"tasks":{

"type":"array",

"items":{

"type":"object",

"required":["task_id","kind","title","state",

"depends_on","files"],

"properties":{

"task_id":{"type":"string"},

"kind":{"enum":["spec","impl","qa",

"emergency_patch"]},

"title":{"type":"string"},

"state":{"enum":["todo","in_progress",

"blocked","done"]},

"depends_on":{"type":"array",

"items":{"type":"string"}},

"files":{"type":"array",

"items":{"type":"string"}}

}

}

},

"indexes":{"type":"object"}

}

}

---

## Appendix CCanonical Event Vocabulary

[Table˜3](#A3.T3 "In Appendix C Canonical Event Vocabulary ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") presents the complete event vocabulary (v0.3.0) as specified in the architecture, and [Table˜4](#A3.T4 "In Appendix C Canonical Event Vocabulary ‣ ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering") presents the simplified vocabulary observed in the clinic-asr case study.

_Table 3: Complete canonical event vocabulary (v0.3.0)._

| Event | Description |
| --- | --- |
| run. init | Initializes a run (metadata and scope). |
| attempt. create | Opens an attempt for a task and links an agent. |
| attempt. timeout | Expires an attempt (TTL) without completing the task. |
| orchestrator. dispatch | Triggers agent execution for an attempt. |
| agent. result | Agent intention (patch proposals), validated by schema/boundary. |
| issue. report | Record of defect/incident; may generate a hotfix task. |
| output. rejected | Rejected output (violated schema, boundary, authority, or idempotency). |
| orchestrator. file. write | Applied effect: writing to authorized files. |
| orchestrator. view. mutate | Applied effect: read-model update (derived). |
| task. create | Creates a new task (includes hotfix). |
| task. update | Updates task state (e. g., todo → \to in_progress → \to done). |
| verify. start | Starts audit via replay + deterministic hashing. |
| verify. ok | Audit passed; recordsprojection_hash_sha256. |
| verify. fail | Audit failed; records divergence (expected vs computed). |
| run. end | Finalizes run (success/failed) and closure criteria. |

_Table 4: Simplified event vocabulary observed in clinic-asr (CS2)._

| Event | Description | Count |
| --- | --- | --- |
| roadmap. version | Initializes the roadmap version. | 1 |
| promote | Moves a task from backlog to ready. | 17 |
| claim | Agent claims a task for execution. | 30 |
| complete | Agent completes a task with acceptance results. | 30 |
| phase. complete | All tasks in a phase are finished. | 8 |

The simplification from 15 to 5 event types reflects a design insight: internal orchestrator events (dispatch, file. write, view. mutate) can be inferred from the claim

→

\to

complete sequence, reducing log verbosity while maintaining essential traceability guarantees. The full vocabulary remains available for environments requiring maximum granularity.

---

## Appendix DCanonicalization and Verify Pseudocode

[⬇](https://arxiv.org/data:text/plain;base64,aW1wb3J0IGpzb24KaW1wb3J0IGhhc2hsaWIKCmRlZiBjYW5vbmljYWxfanNvbihvYmopOgogICAgIyBEZXRlcm1pbmlzdGljIEpTT046IHNvcnQga2V5cywgbm8gc3BhY2VzLCBVVEYtOCwgdHJhaWxpbmcgTEYKICAgIHJldHVybiAoCiAgICAgICAganNvbi5kdW1wcygKICAgICAgICAgICAgb2JqLAogICAgICAgICAgICBzb3J0X2tleXM9VHJ1ZSwKICAgICAgICAgICAgc2VwYXJhdG9ycz0oIiwiLCAiOiIpLAogICAgICAgICAgICBlbnN1cmVfYXNjaWk9RmFsc2UsCiAgICAgICAgKS5lbmNvZGUoInV0Zi04IikKICAgICAgICArIGIiXG4iCiAgICApCgpkZWYgaGFzaF9pbnB1dChwcm9qZWN0ZWRfc3RhdGUpOgogICAgIyBBdm9pZCBzZWxmLXJlZmVyZW5jZTogZXhjbHVkZSBydW4gbWV0YWRhdGEgYW5kIGhhc2ggZmllbGQKICAgIHJldHVybiB7CiAgICAgICAgInNjaGVtYV92ZXJzaW9uIjogcHJvamVjdGVkX3N0YXRlWyJzY2hlbWFfdmVyc2lvbiJdLAogICAgICAgICJwcm9qZWN0IjogcHJvamVjdGVkX3N0YXRlLmdldCgicHJvamVjdCIpLAogICAgICAgICJ0YXNrcyI6IHByb2plY3RlZF9zdGF0ZVsidGFza3MiXSwKICAgICAgICAiaW5kZXhlcyI6IHByb2plY3RlZF9zdGF0ZS5nZXQoImluZGV4ZXMiLCB7fSksCiAgICB9CgpkZWYgY29tcHV0ZV9wcm9qZWN0aW9uX2hhc2gocHJvamVjdGVkX3N0YXRlKToKICAgIHJldHVybiBoYXNobGliLnNoYTI1NigKICAgICAgICBjYW5vbmljYWxfanNvbihoYXNoX2lucHV0KHByb2plY3RlZF9zdGF0ZSkpCiAgICApLmhleGRpZ2VzdCgpCgpkZWYgZXNhYV92ZXJpZnkoZXZlbnRzLCByb2FkbWFwX2pzb24pOgogICAgcHJvamVjdGVkID0gcHJvamVjdF9ldmVudHMoZXZlbnRzKSAgIyBwdXJlIGZ1bmN0aW9uCiAgICBjb21wdXRlZCA9IGNvbXB1dGVfcHJvamVjdGlvbl9oYXNoKHByb2plY3RlZCkKICAgIHN0b3JlZCA9IHJvYWRtYXBfanNvblsicnVuIl1bInByb2plY3Rpb25faGFzaF9zaGEyNTYiXQogICAgcmV0dXJuICgKICAgICAgICB7InZlcmlmeV9zdGF0dXMiOiAib2sifQogICAgICAgIGlmIGNvbXB1dGVkID09IHN0b3JlZAogICAgICAgIGVsc2UgeyJ2ZXJpZnlfc3RhdHVzIjogIm1pc21hdGNoIn0KICAgICk=)

importjson

importhashlib

defcanonical_json(obj):

#DeterministicJSON: sortkeys, nospaces, UTF-8, trailingLF

return(

json. dumps(

obj,

sort_keys=True,

separators=(",",":"),

ensure_ascii=False,

). encode("utf-8")

+b"\n"

)

defhash_input(projected_state):

#Avoidself-reference: excluderunmetadataandhashfield

return{

"schema_version": projected_state["schema_version"],

"project": projected_state. get("project"),

"tasks": projected_state["tasks"],

"indexes": projected_state. get("indexes",{}),

}

defcompute_projection_hash(projected_state):

returnhashlib. sha256(

canonical_json(hash_input(projected_state))

). hexdigest()

defesaa_verify(events, roadmap_json):

projected=project_events(events)#purefunction

computed=compute_projection_hash(projected)

stored=roadmap_json["run"]["projection_hash_sha256"]

return(

{"verify_status":"ok"}

ifcomputed==stored

else{"verify_status":"mismatch"}

)

---

## Appendix ERepresentative Extract from activity. jsonl (CS2: clinic-asr)

The following extract illustrates concurrent multi-agent execution in the clinic-asr event store (lines 58–68), showing Claude Opus 4.6 claiming five tasks simultaneously:

[⬇](https://arxiv.org/data:text/plain;base64,eyJ0cyI6IjIwMjYtMDItMTlUMjE6NTU6NDQiLCJhY3Rpb24iOiJjbGFpbSIsInRhc2tfaWQiOiJULTIzMDEiLAogImFnZW50X2lkIjoiY2xhdWRlLW9wdXMtNC02IiwiYWNjZXB0YW5jZV9yZXN1bHRzIjpudWxsfQp7InRzIjoiMjAyNi0wMi0xOVQyMTo1NTo0NSIsImFjdGlvbiI6ImNsYWltIiwidGFza19pZCI6IlQtMjMwMiIsCiAiYWdlbnRfaWQiOiJjbGF1ZGUtb3B1cy00LTYiLCJhY2NlcHRhbmNlX3Jlc3VsdHMiOm51bGx9CnsidHMiOiIyMDI2LTAyLTE5VDIxOjU1OjQ2IiwiYWN0aW9uIjoiY2xhaW0iLCJ0YXNrX2lkIjoiVC0yMzAzIiwKICJhZ2VudF9pZCI6ImNsYXVkZS1vcHVzLTQtNiIsImFjY2VwdGFuY2VfcmVzdWx0cyI6bnVsbH0KeyJ0cyI6IjIwMjYtMDItMTlUMjE6NTU6NDciLCJhY3Rpb24iOiJjbGFpbSIsInRhc2tfaWQiOiJULTI0MDEiLAogImFnZW50X2lkIjoiY2xhdWRlLW9wdXMtNC02IiwiYWNjZXB0YW5jZV9yZXN1bHRzIjpudWxsfQp7InRzIjoiMjAyNi0wMi0xOVQyMTo1NTo0OCIsImFjdGlvbiI6ImNsYWltIiwidGFza19pZCI6IlQtMjQwMyIsCiAiYWdlbnRfaWQiOiJjbGF1ZGUtb3B1cy00LTYiLCJhY2NlcHRhbmNlX3Jlc3VsdHMiOm51bGx9CnsidHMiOiIyMDI2LTAyLTE5VDIxOjU2OjEwIiwiYWN0aW9uIjoiY29tcGxldGUiLCJ0YXNrX2lkIjoiVC0yMzAxIiwKICJhZ2VudF9pZCI6ImNsYXVkZS1vcHVzLTQtNiIsCiAiYWNjZXB0YW5jZV9yZXN1bHRzIjp7IlJ1bGVzIGRvY3VtZW50ZWQiOnRydWV9fQp7InRzIjoiMjAyNi0wMi0xOVQyMTo1NjoyMCIsImFjdGlvbiI6ImNvbXBsZXRlIiwidGFza19pZCI6IlQtMjMwMiIsCiAiYWdlbnRfaWQiOiJjbGF1ZGUtb3B1cy00LTYiLAogImFjY2VwdGFuY2VfcmVzdWx0cyI6eyJFdmVudHMgZG9jdW1lbnRlZCI6dHJ1ZX19)

{"ts":"2026-02-19T21:55:44","action":"claim","task_id":"T-2301",

"agent_id":"claude-opus-4-6","acceptance_results": null}

{"ts":"2026-02-19T21:55:45","action":"claim","task_id":"T-2302",

"agent_id":"claude-opus-4-6","acceptance_results": null}

{"ts":"2026-02-19T21:55:46","action":"claim","task_id":"T-2303",

"agent_id":"claude-opus-4-6","acceptance_results": null}

{"ts":"2026-02-19T21:55:47","action":"claim","task_id":"T-2401",

"agent_id":"claude-opus-4-6","acceptance_results": null}

{"ts":"2026-02-19T21:55:48","action":"claim","task_id":"T-2403",

"agent_id":"claude-opus-4-6","acceptance_results": null}

{"ts":"2026-02-19T21:56:10","action":"complete","task_id":"T-2301",

"agent_id":"claude-opus-4-6",

"acceptance_results":{"Rulesdocumented": true}}

{"ts":"2026-02-19T21:56:20","action":"complete","task_id":"T-2302",

"agent_id":"claude-opus-4-6",

"acceptance_results":{"Eventsdocumented": true}}
