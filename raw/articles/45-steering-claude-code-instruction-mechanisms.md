> Source: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
> 拉取日期：2026-09-02（原文发布日期 2026-06-18）
> 作者：Anthropic（Claude Code 官方博客）
> 归档说明：AnySearch extract 提取的全文 markdown；表格等结构保留原文。

# Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents

[

](https://claude.com)

Explore here

# SteeringClaudeCode:whentouseCLAUDE.md,skills,hooks,andsubagents

[](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

[](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

- 

Category

[Claude Code](https://claude.com/blog/category/claude-code)
- 

Product

[Claude Code](https://claude.com/product/claude-code)
- 

Date

June 18, 2026
- 

Reading time

12

min
- 

Share[Copy link](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more

Claude is built to work the way you work, and in Claude Code you can customize it.

There are seven methods for instructing Claude's behavior: CLAUDE.md files, rules,[**skills**](https://code.claude.com/docs/en/skills),[**subagents**](https://code.claude.com/docs/en/sub-agents),[**hooks**](https://code.claude.com/docs/en/hooks-guide), output styles, and appending the system prompt.

Each method controls:
- When an instruction loads into context;
- Whether it persists through long sessions (compaction behavior); and
- How much authority it carries.

The table below provides a quick summary of key differences across each method while the post provides additional detail and decision framework for determining where each of your Claude instructions belongs.

MethodWhen it's loadedCompaction behaviorContext costWhen to useCLAUDE.md (root)Session start; stays in context for the entire sessionMemoized. Read once and cached for the session; cache cleared and re-read after compactionHigh. Every line costs tokens whether relevant or notBuild commands, directory layout, monorepo structure, coding conventions, team normsCLAUDE.md (subdirectory)On-demand, when Claude reads a file under that subdirectoryLost until that subdirectory is touched againLow. Only consumes context when the relevant subdirectory is being worked onConventions specific to a subdirectoryRulesSession start (user-level rules) or only when matching files are touched (path-scoped)Re-injected on compactionMedium. Always-on unless path-scopedSpecific constraints or conventions (e.g., all API handlers must validate input with Zod)SkillsName and description at session start; full body loads when the skill is invokedInvoked skills re-injected up to a shared budget; oldest dropped firstLow. Full body loads only when invoked; subject to a shared token budget across invoked skillsProcedural workflows (deploy or release checklists)SubagentsName, description, and tool list at session start; body loads only when called via the Agent toolOnly the final message (summary plus metadata) returns to the main sessionLow. Zero cost in main context until called; runs in its own isolated context windowRunning work in parallel or side tasks that should run in isolation and return only a summary (deep search, log analysis, dependency audit)HooksFire on lifecycle eventsBypass compaction entirelyLow. Configuration lives outside main context; some output may return (e.g., blocking errors)Deterministic automation: run linters, post to Slack on completion, block commands, back up chat history on PreCompactOutput stylesSession start; injected into the system promptNever compactedHigh. Occupies context window, but overwrites default system promptSignificant role changes (code assistant to general assistant)Appending the system promptSession start; passed as a CLI flagNever compacted; applies only to that invocationModerate. Cached after first request in a sessionTone, response length, formatting preferences

## The seven methods for delivering instructions

There are seven ways to customize Claude Code's behavior: CLAUDE.md files for always-on project context, rules for hard constraints, skills for reusable procedures, subagents for delegated work, hooks for deterministic automation, and output styles or system-prompt appends for global changes.

Each method trades context cost against authority. These methods influence Claude's behavior while two separate dials,[which model and effort level you choose](https://claude.com/blog/claude-model-and-effort-level-in-claude-code), control how capable it is and how hard it works.

### CLAUDE.md files

CLAUDE.md is a markdown file at the root of your project. It loads into context at session start and stays there for the entire session.

Build commands, directory layout, monorepo structure, coding conventions, and team norms all fit naturally here.

There are two types, and they load differently:
- **Always loaded**: The first type is a root CLAUDE.md file, either in a shared repository and/or saved locally for your personal preferences specific to a project. All these files load at session start, and won’t get lost or degraded across long sessions. When Claude Code compacts the conversation, it re-reads these files.
- **On-demand:**CLAUDE.md files in subdirectories below the folder where you initialized the session. For example,`app/api/CLAUDE.md`loads when Claude reads a file under`app/api`, not at session start. It shares the compaction behavior of path-scoped rules: gone until that subdirectory is touched again.

All subdirectory CLAUDE.md files below the cwd load when Claude reads a file within that directory.

In a shared repository, CLAUDE.md grows the way any unowned config file does: every team appends its own instructions and nothing gets deleted. The cost compounds at scale.

Every line loads into every session for every engineer working in the repo, whether it's relevant to their task or not. This consumes tokens and dilutes adherence to the instructions that actually matter. As the file grows, push team-specific conventions into path-scoped rules and procedures into skills, where they load only when relevant.

**Tip:**Keep CLAUDE.md under 200 lines, give it an owner, and review changes to it like code. The content itself should follow the same rules as any prompt:[writing effective prompts](https://claude.com/blog/best-practices-for-prompt-engineering)means being explicit, explaining the why behind constraints, and showing examples.

Think of this file as giving Claude an overview of your codebase, or as an index pointing to other files where Claude can find more information as needed.

In monorepos, give each team's directory its own subdirectory CLAUDE.md so teams only load their own conventions, and developers can use the claudeMdExcludes setting to skip files from teams whose code they never touch.

For standards that must apply to every repository in the organization — security policies, compliance requirements — a centrally managed CLAUDE.md can be deployed to developer machines via MDM or config management, and it can't be excluded by individual settings.

More on setting up CLAUDE.md in our blog post,[CLAUDE.md files: Customizing Claude Code for your codebase](https://claude.com/blog/using-claude-md-files).

No items found.

[Prev](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

0/5

[Next](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

Get Claude Code

Or read the[documentation](https://code.claude.com/docs/en/overview)

Try Claude Code

[Try Claude Code](https://claude.ai/redirect/claude_com.v1.3600cbe3-ee40-42e6-b946-0f5c2e0fb9fa/code)

Developer docs

[Developer docs](https://code.claude.com/docs/en/overview)

eBook

## 

[](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

### Rules

[**Rules**](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)are markdown files in`.claude/rules/`that give Claude specific constraints or conventions.

Unscoped rules behave like CLAUDE.md in that they are always loaded at session start and get re-injected on compaction. This can waste tokens by loading context even when it's not relevant for the task at hand.

Path-scoped rules allow you to load rule instructions only when they are relevant by adding a`paths`field that controls when they load.

For example: a rule scoped to`src/api/**`stays out of context during a docs-only session. It would only be loaded whenever Claude reads files within that`src/api/`directory.

Here’s what that looks like:`---paths:-"src/api/**"-"**/*.handler.ts"---AllAPIhandlersmustvalidateinputwithZodbeforeprocessing.`

**Tip**: A file-specific constraint, like "migrations are append-only," fits best as a**rule**placed in your paths: frontmatter. Reach for a path scoped rule over a nested CLAUDE.md file when the instruction regards a cross-cutting concern or file that appears in multiple (but not all) corners of the codebase.

### Skills

[**Skills**](https://code.claude.com/docs/en/skills)live in`.claude/skills/`as folders of instructions, scripts, and resources that Claude loads dynamically. Each skill has a`SKILL.md`file with a name, description, and body.

Only the name and description load at session start; the full body loads when Claude invokes the skill, either through a slash command (/code-review) or by auto-matching the task.

Skills are triggered via your system prompt.

For example,`/code-review`is a built-in skill that reviews your current diff and reports its findings without editing files. The skill defines the playbook so Claude follows the same structured approach every time you invoke it.

On compaction, Claude Code re-injects invoked skills up to a total budget across all invoked skills. If you’ve invoked many skills during a session, the oldest ones drop first.

**Tip:**Instructions that are procedural, like deploy workflows, release checklists, or review processes, belong in a skill rather than in CLAUDE.md.

Claude Code ships with skills, but you can also write your own custom skills. Our[complete guide to building skills for Claude](https://claude.com/blog/complete-guide-to-building-skills-for-claude)shows you how.

### Subagents

[**Subagents**](https://code.claude.com/docs/en/sub-agents)are markdown files in`.claude/agents/`that define isolated assistants for specific side tasks. Each file uses YAML frontmatter (name, description, plus optional fields for model and tool access) followed by a body that becomes that subagent's system prompt.

Subagents are similar to skills in that the name, description, and tool list load at session start, but the larger context within the body of the agent doesn’t auto-invoke. Claude calls them via the Agent tool, passing in a prompt string.

Claude Code’s context window holds everything Claude knows about your session. The[interactive timeline here](https://code.claude.com/docs/en/context-window)walks through what loads and when.

Not only does the larger instructional context within the body of the subagent not auto-invoke, it never enters the parent conversation at all.

The subagent then runs in its own fresh context window, and the only thing that returns to your main session is the subagent’s final message (often the aggregated result of many subtasks) plus metadata.

This pattern scales: subagents can nest up to five levels deep, and[dynamic workflows](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)orchestrate tens to hundreds of background agents without requiring you to specify each detail of the subagent architecture. The orchestration plan and intermediate results live in script variables rather than in Claude’s context window, which enables scale without losing instructional fidelity.

**Tip:**That isolation is one of the main reasons to reach for a subagent instead of a skill. Use a subagent when a side task like deep search, a log analysis pass, or a dependency audit would clutter your main conversation with intermediate results you won't reference again. Use a skill when you want the procedure to play out inside the main thread so you can see and steer each step.

### Hooks

[**Hooks**](https://code.claude.com/docs/en/hooks-guide)are user-defined commands, HTTP endpoints, or LLM prompts that provide more deterministic control over Claude’s behavior by firing on[specific events in Claude’s lifecycle](https://code.claude.com/docs/en/hooks#hook-lifecycle)like file edits, tool calls, or session start.

A map of events in a Claude Code session when a hook can fire.

You register hooks in`settings.json`, managed policy settings, or skill/agent frontmatter.

There are several types of hooks: command, HTTP, mcp_tool, prompt, and agent. All hooks are deterministically triggered. The first three execute deterministically while the latter two, prompt and agent, use Claude’s judgment rather than a set of rules to determine the output.

Hooks have low context costs because the configuration or instruction lives outside the main context window. The harness runs the handler (command, http, mcp_tool) or makes model calls with separate windows (prompt, agent) depending on the hook type.

Some hooks may have the output saved to the main context window. For example, a blocking hook's standard error is saved within context so Claude knows why the call was denied.

But most hooks won’t have the output saved to the main window unless the configuration explicitly returns it. If you backed up your chat history into another file for later reference before compaction using the`PreCompact`event, Claude wouldn’t know which file had the chat history saved.

This makes these hook types fundamentally different from CLAUDE.md, rules, and skills. You can learn more in our post****[**how to configure hooks**](https://claude.com/blog/how-to-configure-hooks).

**Tip:**Use hooks for anything that should happen deterministically: running linters after edits, posting to Slack on completion, or blocking specific commands before they execute. A`PreToolUse`hook can inspect any tool call and exit code 2 to deny it.

They have low context cost because they are code that the harness runs rather than instructions to Claude that get loaded into context. Skills and hooks are also the building blocks of[designing agent loops](https://claude.com/blog/getting-started-with-loops)—repeating workflows that run until a stop condition is met.

### Output styles

[**Output styles**](https://code.claude.com/docs/en/output-styles)are files in`.claude/output-styles/`that inject instructions into the system prompt. They never get compacted, load at the start of every session, and are cached after the first request within a session, meaning they have a moderate context cost.

Because they sit in the system prompt, output styles carry the highest instruction-following weight of any method that we've covered so far and should be used judiciously.

**Changes to the output style will replace the default output style**(unless you set keep-coding-instructions: true in the style's frontmatter).

In Claude Code, this would remove instructions that tell Claude it is helping users with software engineering tasks and contains other critical default instructions such as:
- How to scope changes;
- When to add or omit code comments;
- What to do about security concerns; and
- Verification habits like running tests before declaring work complete.

By default, a custom output style drops all of this and Claude Code becomes more of a general assistant than a software engineer assistant.

**Tip**: Before writing a custom output style, check the built-in styles.**Proactive**,**Explanatory**, and**Learning**cover the most common needs (autonomy, teaching mode, collaborative coding) without you having to maintain a style file.

### Appending the system prompt

An alternative to modifying output styles is the`append-system-prompt`flag. Whereas modifying output style files can have large, unintended changes to Claude’s behavior, the append flag is only additive to the original system prompt. It doesn’t modify Claude’s role; it just adds instructions to its default role.

It is also passed at invocation time, and only applies to that invocation, rather than persisted as a file across sessions.

Appending the system prompt can have a higher context cost compared to other methods of passing instructions. It increases input tokens, though prompt caching reduces this cost after the first request in a session. Instructing Claude to use a more verbose or longer style also increases output tokens.

**Tip:**Appending the system prompt is best for adding specific coding standards, output formatting, or domain-specific knowledge. Keep in mind that appending the system prompt has diminishing returns for adherence. Generally, the more instructions you provide using this method, the less strictly Claude will follow them, particularly if any contradict.

## When to use each method

If you find yourself doing one of the following, you may want to consider an alternative location for your instructions:

**"Every time X, always do Y" in CLAUDE.md.**If the behavior should happen reliably, like running prettier after every edit or posting to Slack on completion, use a hook in`settings.json`instead. The model choosing to run a formatter is different from the formatter running automatically.

**“Never do this” in CLAUDE.md**. When there's something that absolutely must not happen, an instruction is the wrong tool. Claude will follow the instruction most of the time, but when under pressure, in a long session or an ambiguous situation, or due to a prompt injection in a file accessed as part of the task, the model can fail to follow a prompted rule. A real guardrail needs to be deterministic, and the enforcement methods are[hooks](https://code.claude.com/docs/en/hooks)and[permissions](https://code.claude.com/docs/en/permissions). A`PreToolUse`hook can inspect a call and exit with code 2 to block it.[**Managed settings**](https://code.claude.com/docs/en/settings#managed-settings)****go further: they are admin-deployed, cannot be overridden by a user's local config, and are the only way to enforce a deterministic, organization-wide guardrail.

**A 30-line procedure in CLAUDE.md.**Procedures belong in skills. CLAUDE.md is for facts Claude should hold all the time: build commands, monorepo layout, team conventions. A deployment runbook or a security review checklist should live in`.claude/skills/`, where the body loads only when invoked.

**An API-specific rule without paths.**If a rule only applies to`src/api/**`, scoping it with`paths:`keeps it out of context during unrelated work. An unscoped rule is mechanically identical to putting the content in CLAUDE.md: always loaded, always costing tokens.

**Writing personal preferences to a project-level CLAUDE.md file.**All file-based methods have a user-level counterpart loaded for every Claude Code session regardless of which repo you’re in. Use local files for personal preferences (always use semantic commit messages). Keep project-level files for preferences that are team-wide but specific to a given codebase.

## Getting started with Claude Code customization

You can find more tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions, in our[best practices for Claude Code](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md)documentation.

Once you have a few of these working, you can bundle many of them (skills, subagents, hooks, output styles) as a[plugin](https://code.claude.com/docs/en/plugins)to share a coherent setup across teammates or projects.

*This article was written by Michael Segner member of Anthropic staff.*

FAQ

No items found.

[](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

## Related posts

Explore more product news and best practices for teams building with Claude.

Aug 20, 2026

### The Claude Code guide for startups

Claude Code

[The Claude Code guide for startups](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

[The Claude Code guide for startups](https://claude.com/blog/claude-code-guide-for-startups)

Aug 21, 2026

### The AI-Native SDLC playbook

Enterprise AI

[The AI-Native SDLC playbook](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

[The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)

Aug 24, 2026

### How an Anthropic field marketer uses Claude Code to send weekly personalized updates to every sales rep

Claude Code

[How an Anthropic field marketer uses Claude Code to send weekly personalized updates to every sales rep](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

[How an Anthropic field marketer uses Claude Code to send weekly personalized updates to every sales rep](https://claude.com/blog/how-an-anthropic-field-marketer-uses-claude-code-to-send-weekly-personalized-updates-to-every-sales-rep)

Aug 13, 2026

### Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions

Agents

[Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

[Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions](https://claude.com/blog/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions)

## Transform how your organization operates with Claude

See pricing

[See pricing](https://claude.com/pricing#api)

Contact sales

[Contact sales](https://claude.com/contact-sales)

Get the developer newsletter

Product updates, how-tos, community spotlights, and more. Delivered monthly to your inbox.

Thank you! You’re subscribed.

Sorry, there was a problem with your submission, please try again later.

[](https://claude.com/blog-product/claude-code)

Claude Code

[](https://claude.com/blog-usecases/coding)

Coding