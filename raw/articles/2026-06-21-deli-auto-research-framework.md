> 原文：https://victorchen96.github.io/auto_research/framework.html
> 抓取方式：webReader（2026-06-21）
> 作者 / 项目：Victor Chen — Deli_AutoResearch（个人 GitHub Pages 上的协议框架）
> 性质说明：本文是一个**自包含的 SKILL.md 协议框架**（ship no code，纯约定），用于长时间自主任务（days–weeks）。下文为网页正文导读（01–09 节）+ 末尾完整 SKILL.md（第 10 节，权威来源）。validation 为作者**框架内自评**（见第 09 节 limits），非同行评议或大公司验证。

---

# Deli_AutoResearch — Autonomous Research Framework

The skill itself is one self-contained Markdown document.

It depends on no external resource or private infrastructure — a single SKILL.md fully defines the whole protocol: motivation, behavioral constraints, architecture, state files, stall detection, heartbeat watchdog, scheduling patterns, and engineering constraints. Below is a structured reading guide; the complete SKILL.md is appended at the bottom, copyable in one click.

## 01 Motivation: Three Failure Modes

Long-running code agents exhibit three recurring failure modes whose common cause is missing engineering scaffolding, not model capability. Every mechanism in the framework targets them.

#### 1. Cognitive Loop

Successive iterations try similar directions with diminishing returns, unable to escape a local optimum on their own.

#### 2. Stalling

The agent finishes a chunk, summarizes, and waits for feedback. Externally the session looks alive and polling runs, but work has stopped — more common than crashes.

#### 3. Runtime Fragility

Context compaction silently breaks the loop; closing a session takes down the timers parasitic on it. Failures go unnoticed by default.

## 02 Behavioral Constraints

Hard rules of the framework, each induced from a real failure.

#### i. Zero interaction

No prompting the user during a run: no Plan Mode, no question tool, no ending on a question. Continue until stopped. Resolve ambiguity yourself and log the reasoning (level=decision).

#### ii. Ready means execute

The most common hidden violation: finishing all prep then asking "should I submit?". Prep exists to be executed; submitting, resubmitting, fixing, and starting monitors are routine — no confirmation needed.

#### iii. Callback means report-alive

After context compaction the loop silently dies. The first action of every callback updates its own last_seen, then checks liveness; on failure it restarts immediately and logs it.

#### iv. Persist state to files

All progress is written to state/ files, not conversation memory. Each iteration starts a fresh session, injecting only curated state; never resume.

#### v. Guardian / worker separation

A heartbeat patrol may only do three things to tasks that aren't its own: liveness-check, restart, nudge. It does not read their data, modify their state, or report for them. Basis: a patrol once overstepped into another task's business, causing context pollution, reporting drift, and concurrent-write risk.

## 03 Architecture

The orchestrator monitors state, detects stalls, and injects new directions; each task runs in its own fresh session. Three core decisions: separate execution from evaluation, prefer fresh sessions over resume, and enforce direction diversity.

```
┌── Orchestrator (current session / durable cron) ─────────┐
│ monitor state files → detect stalls → inject new direction │
└──────┬──────────────────┬──────────────────┬────────────┘
       ▼                  ▼                  ▼
   [Task A]           [Task B]           [Task C]   ← each its own fresh session
```

## 04 State File System

Each task keeps its own state and log directories. Three process types write separate log streams, so debugging never needs cross-file correlation.

```
{task}/state/
├── task_spec.md           # goal / milestones / success criteria
├── progress.json          # {iteration, status, stale_count, ...}
├── findings.jsonl         # accumulated findings (append-only)
├── directions_tried.json  # directions tried (basis for diversity)
└── iteration_log.jsonl    # per-iteration summary

{task}/logs/
├── work.jsonl             # work agent; decisions tagged level=decision
├── orchestrator.jsonl     # orchestrator
└── heartbeat.jsonl        # heartbeat watchdog
```

## 05 Stall Detection & Pivoting

| Mechanism | Rule |
| --- | --- |
| Stall detection | An iteration with 0 new findings or a metric drop → stale_count + 1 |
| Forced pivot | stale_count ≥ 2 → change a structural constraint, not tactical parameters; ≥ 4 → flag for human attention |
| Direction diversity | A new direction must differ from every tried one; after a stall, inject perturbation (start from the opposite hypothesis, find structurally similar cross-domain cases, etc.) |
| Round cap | A single work session caps at 15 rounds or 30 minutes |

**Why pivot structure, not tactics**

This comes from practice: when a task stalls repeatedly within a frame, the decisive gain usually comes from correcting the environment/structural constraint itself, not from tuning strategy parameters harder inside the existing frame. Two stalls should prompt questioning the environment, not deeper digging in one direction.

## 06 Heartbeat Watchdog (3-Layer)

The business loop is itself unreliable and needs an independent guardian layer. Three mutually-checking layers: any one dying can be detected and recovered by another.

| Layer | Form | Role |
| --- | --- | --- |
| L0 | A resident shell guard depending on no session | Heartbeat timestamp stale > 2h → spin up an emergency patrol via a headless agent |
| L1 | A durable scheduled job, hourly | Check each loop's last_seen, restart timed-out loops, detect stalling and nudge |
| L2 | Business loops, each in its own session | First line of each callback updates its own last_seen |

**Stall detection threshold**

If progress has no update for over 2h and the last output is a question → judged stalled, launch a nudge subagent (inject the task's task_spec and progress, instruct it to continue and update state). Three consecutive nudges with no progress → judged structurally stuck; stop nudging and reopen with a new direction. The 2h threshold is deliberately shorter than the 4h stuck-task threshold: stalling is a voluntary stop, cheap to fix, worth catching earlier.

## 07 Subagent Scheduling Patterns

| Pattern | Use | Key Idea |
| --- | --- | --- |
| A  Goal-driven | Research iteration | Inject tried directions, require verifiable findings, write back to findings.jsonl |
| B  Parallel exploration | Complex sub-problems | Fire multiple agents in one message: investigation, refutation, cross-domain analogy |
| C  Experiment run | Long compute jobs | Start minute-level polling right after submit: auto-diagnose errors, fix, resubmit |
| D  Verification | Post-iteration QA | An independent subagent audits the evidence chain of findings |

A subagent prompt should include: background, a verifiable deliverable, working directory, file/line caps, and completion criteria.

## 08 Engineering Constraints

Induced by the meta-learning loop from real failures; violating them empirically caused stalls or regressions.

1. At most 5 large files per iteration; no single file over 300 lines.
2. State is injected via files, not conversation history.
3. Validation (test / compile / check) must run between iterations.
4. Citation-like content is verified every 20 entries, never batched up.
5. With multiple candidate directions, prefer adding diversity over digging one deeper.
6. Unresolvable external-dependency failures escalate: full report + notify the owner + poll for a reply; never abandon silently.

## 09 Validation & Limits

The framework has carried several heterogeneous long-horizon tasks. Output of the paper-writing track (pages / citations / in-framework self-rating):

| Paper | Pages | Citations | Self-rated |
| --- | --- | --- | --- |
| Autonomous Research Agents | 59 | 228 | 8.0 |
| Continual Learning | 65 | 326 | 8.0 |
| Long-Horizon Decision-Making | 55 | 384 | 8.0 |
| Self-Play (285B RL experiment + theory hardening) | 75 | 217 | 8.6 |

**Limits (honest disclosure)**

1. Scores come from in-framework multi-persona simulated review; comparable only longitudinally within the same protocol, not an external quality claim.
2. Longest continuous run was 72 hours with 6 directional human inputs — zero operational intervention, directional intervention retained.
3. Fabricated citations and data artifacts originate from the LLM itself; the framework makes external checking a mechanical step in the process, it does not remove the error source.
4. Separation of duties relies on protocol constraints, not model discipline; removing the constraints brings overstepping back.

## 10 Full SKILL.md

The authoritative source for the guide above — one self-contained Markdown document depending on no external resource.

```markdown
---
name: Deli_AutoResearch
description: A protocol framework for long-horizon autonomous tasks. Targets three empirically-observed failure modes — cognitive loops, stalling, runtime fragility — by prescribing state management, stall detection, and watchdog mechanisms. Validated on multiple task types including paper writing (4 ICLR-format surveys, in-framework self-rating 8.0-8.6/10).
type: Agent Framework
tags: autonomous, long-horizon, zero-interaction, anti-loop, heartbeat-watchdog, loop, multi-agent, unattended, orchestration
---

# Deli_AutoResearch

This skill is a protocol framework for long-horizon autonomous tasks (days to weeks). It ships no executable code; instead it prescribes a set of battle-tested conventions: how state is persisted, how stalls are detected, how guardians are layered, and what constraints bind agent behavior. Implementation details are left to the adopter's environment.

## 1. Motivation

Long-running code agents exhibit three recurring failure modes:

1. Cognitive loop — successive iterations try similar directions with diminishing returns, unable to escape a local optimum on their own.
2. Stalling — the agent finishes a chunk of work, outputs a summary, and waits for user feedback. Externally the session looks alive and polling runs, but work has effectively stopped. Run logs show this is more common than crashes.
3. Runtime fragility — context compaction silently breaks the loop; closing a session takes down the timers parasitic on it. Failures go unnoticed by default.

The common cause of all three is missing engineering scaffolding, not insufficient model capability. Every mechanism in this framework targets the failure modes above.

## 2. Behavioral Constraints

1. Zero interaction — no prompting the user during a run: no Plan Mode, no question tool, no ending on a question. Continue working until the user stops you. Resolve ambiguity yourself and write the reasoning to the log (level=decision).
2. Ready means execute — the most common hidden violation: finishing all preparation and then asking "should I submit?". The purpose of preparation is execution; submitting, resubmitting, fixing, and starting monitors are all routine operations needing no confirmation.
3. Callback means report-alive — after context compaction the loop dies silently. The first action of every callback is to update its own last_seen, then check liveness; on detecting failure it restarts immediately and logs it.
4. Persist state to files — all progress is written to state/ files, not conversation memory. Each iteration starts a fresh session, injecting only curated state; never use resume.
5. Guardian / worker separation — a heartbeat patrol may take only three actions on tasks that are not its own: liveness-check, restart, nudge. It does not read their data, modify their state files, or report to the user on their behalf.

## 3. Architecture

    ┌── Orchestrator (current session / durable cron) ──┐
    │ monitor state files → detect stalls → inject direction │
    └────┬─────────────┬─────────────┬────────────┘
      [Task A]      [Task B]      [Task C]   ← each its own fresh session

Core design decisions:
- Separate execution from evaluation — the agent doing the work does not judge its own progress; stall determination is made by the orchestration layer based on quantitative metrics.
- Fresh session over resume — context accumulation is the primary cause of cognitive loops. Each iteration starts with fresh context; state is injected via files.
- Enforced direction diversity — before each iteration, read the list of tried directions; a new direction must differ from all history.

## 4. State Files

    {task}/state/
    ├── task_spec.md           # goal / milestones / success criteria
    ├── progress.json          # {iteration, total_findings, status, stale_count}
    ├── findings.jsonl         # accumulated findings (append-only)
    ├── directions_tried.json  # directions already tried
    └── iteration_log.jsonl    # per-iteration summary

    {task}/logs/
    ├── work.jsonl             # written by work agent; decisions tagged level=decision
    ├── orchestrator.jsonl     # written by orchestrator
    └── heartbeat.jsonl        # written by heartbeat watchdog

Log line format: {"ts":"...", "source":"...", "level":"info|warn|error|decision", "event":"...", "detail":"..."}

## 5. Usage

    # 1. Initialize the task directory, write state/task_spec.md and an initial progress.json

    # 2. Start the orchestrator loop:
    /loop 2h check all tasks under : (1) read progress.json;
    (2) if stale_count>=3 generate a fresh direction; (3) launch a work agent
    via the Agent tool (with explicit goal and completion criteria);
    (4) write results back to state files. Zero interaction.

    # 3. Register a durable heartbeat watchdog (survives across sessions):
    hourly patrol: write a timestamp; check each loop's last_seen against interval×3,
    restart if exceeded; check each task's progress for stalls over 2h, nudge if stalled.
    Zero interaction.

## 6. Stall Detection & Pivoting

| Mechanism | Rule |
|-----------|------|
| Stall detection | an iteration with 0 new findings or a metric drop → stale_count + 1 |
| Forced pivot | stale_count >= 2 → change a structural constraint, not tactical parameters; >= 4 → flag for human attention |
| Direction diversity | a new direction must differ from every tried one; after a stall, inject a perturbation strategy |
| Round cap | a single work session caps at 15 rounds or 30 minutes |

"Pivot structure, not tactics" comes from practice: when a task stalls repeatedly within a frame, the decisive gain usually comes from correcting the environment/structural constraint itself, not from tuning strategy parameters harder inside the existing frame.

## 7. Heartbeat Watchdog

The business loop is itself unreliable and needs an independent guardian layer. Three mutually-checking layers (V3):

| Layer | Form | Depends on | Role |
|-------|------|------------|------|
| L0 | resident shell guard | no session | heartbeat stale > 2h → spin up an emergency patrol via a headless agent |
| L1 | durable cron, hourly | a living interactive session | check each loop's last_seen, restart timed-out loops, detect stalling and nudge |
| L2 | business loop | each its own session | first line of each callback updates its own last_seen |

Any one layer dying can be detected and recovered by another.

Stall detection: if progress has no update for over 2 hours and the last output is a question → judged stalled, launch a nudge subagent. Three consecutive nudges with no progress → judged structurally stuck; stop nudging and reopen with a new direction. The 2h threshold is deliberately shorter than the 4h stuck-task threshold.

## 8. Subagent Scheduling Patterns

| Pattern | Use | Key idea |
|---------|-----|----------|
| A Goal-driven | research iteration | inject tried directions, require verifiable findings, write back to findings.jsonl |
| B Parallel exploration | complex sub-problems | fire multiple agents in one message: investigation, refutation, cross-domain analogy |
| C Experiment run | long compute jobs | start minute-level polling right after submit: auto-diagnose errors, fix, resubmit |
| D Verification | post-iteration QA | an independent subagent audits the evidence chain of findings |

A subagent prompt should include: background, a verifiable deliverable, working directory, file/line caps, and completion criteria.

## 9. Engineering Constraints

1. At most 5 large files per iteration; no single file over 300 lines.
2. State is injected via files, not conversation history.
3. Validation (test / compile / check) must run between iterations.
4. Citation-like content is verified every 20 entries, never batched up.
5. With multiple candidate directions, prefer adding diversity over digging one deeper.
6. Unresolvable external-dependency failures escalate (full report + notify the owner + poll for a reply); never abandon silently.

## 10. Validation & Limits

The framework has carried several heterogeneous tasks: academic paper writing, long-horizon research, etc. Paper-track output:

| Paper | Pages | Citations | Self-rated |
|-------|-------|-----------|------------|
| Autonomous Research Agents | 59 | 228 | 8.0/10 |
| Continual Learning | 65 | 326 | 8.0/10 |
| Long-Horizon Decision-Making | 55 | 384 | 8.0/10 |
| Self-Play (285B RL experiment + theory hardening) | 75 | 217 | 8.6/10 |

Limits:
1. Scores come from in-framework multi-persona simulated review; comparable only longitudinally within the same protocol, not an external quality claim.
2. The longest continuous run on record was 72 hours, with 6 directional human inputs during it — zero operational intervention, directional intervention retained.
3. Fabricated citations and data artifacts originate from the LLM itself; the framework makes external checking a mechanical step in the process, it does not remove the error source.
4. Separation of duties relies on protocol constraints, not model self-discipline; removing the constraints brings overstepping behavior back.
```
