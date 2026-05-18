---
source: "pdf"
source_file: "D:\\AI-resource\\The-Complete-Guide-to-Building-Skill-for-Claude.pdf"
created: "2026-05-18T01:13:07Z"
pages: 33
---


The Complete Guide to Building Skills for Claude <!-- page break -->
| Contents |  |
| --- | --- |
| Introduction | 3 |
| Fundamentals 4 |  |
| Planning and design | 7 |
| Testing and iteration | 14 |
| Distribution and sharing | 18 |
| Patterns and troubleshooting | 21 |
| Resources and references | 28 |
<!-- page break -->
| Introduction |  |
| --- | --- |
| A skill is a set of instructions - packaged as a simple folder - that teaches Claude | Two Paths Through This Guide |
| how to handle specific tasks or workflows. Skills are one of the most powerful | Building standalone skills? Focus on Fundamentals, Planning and Design, and |
| ways to customize Claude for your specific needs. Instead of reexplaining your | category 1-2. Enhancing an MCP integration? The "Skills + MCP" section and |
| preferences, processes, and domain expertise in every conversation, skill s let you | category 3 are for you. Both paths share the same technical requirements, but |
| teach Claude once and benefit every time. | you choose what's relevant to your use case. |
| Skills are powerful when you have repeatable workflows: generating frontend | What you'll get out of this guide: By the end, you'll be able to build a functional |
| designs from specs, conducting research with consistent methodology, creating | skill in a single sitting. Expect about 15-30 minutes to build and test your first |
| documents that follow your team's style guide, or orchestrating multistep | working skill using the skillcreator. |
| processes. They work well with Claude's builtin capabilities like code execution |  |
|  | Let's get started. |
| and document creation. For those building MCP integrations, skills add another |  |
| powerful layer helping turn raw tool access into reliable, optimized workflows. |  |
| This guide covers everything you need to know to build effective skills - from |  |
| planning and structure to testing and distribution. Whether you're building a |  |
| skill for yourself, your team, or for the community, you'll find practical patterns |  |
| and realworld examples throughout. |  |
| What you'll learn: |  |
• Technical requirements and best practices for skill structure  • Patterns for standalone skills and MCPenhanced workflows • Patterns we've seen work well across different use cases  • How to test, iterate, and distribute your skills  Who this is for:  • Developers who want Claude to follow specific workflows consistently • Power users who want Claude to follow specific workflows  • Teams looking to standardize how Claude works across their organization <!-- page break -->
Chapter 1

# Fundamentals

<!-- page break -->

### Chapter 1


# Fundamentals


### What is a skill? Composability

A skill is a folder containing: Claude can load multiple skills simultaneously. Your skill should work well
|  |  |  | alongside others, not assume it's the only capability available. |
| --- | --- | --- | --- |
| • SKILL. md |  | (required): Instructions in Markdown with YAML frontmatter |  |
| • scripts/ | (optional): Executable code (Python, Bash, etc.) |  | Portability |
| • references/ |  | (optional): Documentation loaded as needed |  |
|  |  |  | Skills work identically across Claude. ai, Claude Code, and API. Create a skill once |
| • assets/ | (optional): Templates, fonts, icons used in output |  | and it works across all surfaces without modification, provided the environment |
|  |  |  | supports any dependencies the skill requires. |
| Core design principles |  |  |  |
|  |  |  | For MCP Builders: Skills + Connectors |
| Progressive Disclosure |  |  |  |
|  |  |  | 💡 Building standalone skills without MCP? Skip to Planning and Design - you can |
| Skills use a threelevel system: |  |  | always return here later. |
| • First level (YAML frontmatter): |  | Always loaded in Claude's system prompt. |  |
|  |  |  | If you already have a working MCP server , you've done the hard part. Skills are |
Provides just enough information for Claude to know when each skill should the knowledge layer on top - capturing the workflows and best practices you be used without loading all of it into context. already know, so Claude can apply them consistently. • Second level (SKILL. md body): Loaded when Claude thinks the skill is  relevant to the current task. Contains the full instructions and guidance.

## The kitchen analogy

• Third level (Linked files): Additional files bundled within the skill directory  that Claude can choose to navigate and discover only as needed. MCP provides the professional kitchen: access to tools, ingredients, and equipment. This progressive disclosure minimizes token usage while maintaining  specialized expertise. Skills provide the recipes: stepbystep instructions on how to create something valuable. <!-- page break -->
| Together, they enable users to accomplish complex tasks without needing to |  |
| --- | --- |
| figure out every step themselves. |  |
| How they work together: |  |
| MCP (Connectivity) | Skills (Knowledge) |
| Connects Claude to your service | Teaches Claude how to use your service |
| (Notion, Asana, Linear, etc.) | effectively |
| Provides realtime data access and tool | Captures workflows and best practices |
invocation What Claude can do How Claude should do it

# Why this matters for your MCP users


## Without skills:

• Users connect your MCP but don't know what to do next  • Support tickets asking "how do I do X with your integration"  • Each conversation starts from scratch • Inconsistent results because users prompt differently each time • Users blame your connector when the real issue is workflow guidance

## With skills:

• Prebuilt workflows activate automatically when needed • Consistent, reliable tool usage • Best practices embedded in every interaction • Lower learning curve for your integration <!-- page break -->
Chapter 2 Planning and design <!-- page break -->

# Chapter 2

| Planning and design |  |  |
| --- | --- | --- |
| Start with use cases |  | Common skill use case categories |
| Before writing any code, identify 2-3 concrete use cases your skill should enable. |  | At Anthropic, we’ve observed three common use cases: |
| Good use case definition: |  | Category 1: Document & Asset Creation |
|  |  | Used for: Creating consistent, highquality output including documents, |
|  | Use Case: Project Sprint Planning | presentations, apps, designs, code, etc. |
|  | Trigger: User says "help me plan this sprint" or "create |  |
|  | sprint tasks" | Real example: frontenddesign skill (also see skills for docx, pptx, xlsx, and |
|  | Steps: | ppt ) |
|  | 1. Fetch current project status from Linear (via MCP) |  |
|  | 2. Analyze team velocity and capacity | "Create distinctive, productiongrade frontend interfaces with high design |
|  | 3. Suggest task prioritization | quality. Use when building web components, pages, artifacts, posters, or |
|  | 4. Create tasks in Linear with proper labels and estimates | applications." |
|  | Result: Fully planned sprint with tasks created |  |
|  |  | Key techniques: |
|  |  | • Embedded style guides and brand standards |
| Ask yourself: |  |  |
|  |  | • Template structures for consistent output |
| • | What does a user want to accomplish? |  |
|  |  | • Quality checklists before finalizing |
| • | What multistep workflows does this require? |  |
|  |  | • No external tools required - uses Claude's builtin capabilities |
| • | Which tools are needed (builtin or MCP?) |  |
| • | What domain knowledge or best practices should be embedded? |  |
<!-- page break -->
| Category 2: Workflow Automation | Define success criteria |  |
| --- | --- | --- |
| Used for: Multistep processes that benefit from consistent methodology, |  |  |
|  | How will you know your skill is working? |  |
| including coordination across multiple MCP servers. |  |  |
|  | These are aspirational targets - rough benchmarks rather than precise |  |
| Real example: skillcreator skill |  |  |
|  | thresholds. Aim for rigor but accept that there will be an element of vibesbased |  |
|  | assessment. We are actively developing more robust measurement guidance and |  |
| "Interactive guide for creating new skills. Walks the user through use case |  |  |
|  | tooling. |  |
| definition, frontmatter generation, instruction writing, and validation." |  |  |
|  | Quantitative metrics: |  |
| Key techniques: |  |  |
|  | • | Skill triggers on 90% of relevant queries |
| • Stepbystep workflow with validation gates |  |  |
|  |  | – How to measure: Run 10-20 test queries that should trigger your skill. Track |
| • Templates for common structures |  |  |
|  |  | how many times it loads automatically vs. requires explicit invocation. |
| • Builtin review and improvement suggestions |  |  |
|  | • | Completes workflow in X tool calls |
| • Iterative refinement loops |  | – How to measure: Compare the same task with and without the skill enabled. |
|  |  | Count tool calls and total tokens consumed. |
| Category 3: MCP Enhancement |  |  |
|  | • | 0 failed API calls per workflow |
|  |  | – How to measure: Monitor MCP server logs during test runs. Track retry rates |
| Used for: Workflow guidance to enhance the tool access an MCP server provides. |  |  |
|  |  | and error codes. |
| Real example: sentrycodereview skill (from Sentry) |  |  |
|  | Qualitative metrics: |  |
| "Automatically analyzes and fixes detected bugs in GitHub Pull Requests using |  |  |
|  | • | Users don't need to prompt Claude about next steps |
| Sentry's error monitoring data via their MCP server." |  |  |
|  |  | – How to assess: During testing, note how often you need to redirect or clarify. |
|  |  | Ask beta users for feedback. |
| Key techniques: |  |  |
| • Coordinates multiple MCP calls in sequence |  |  |
|  | • | Workflows complete without user correction |
| • Embeds domain expertise |  | – How to assess: Run the same request 3-5 times. Compare outputs for |
|  |  | structural consistency and quality. |
| • Provides context users would otherwise need to specify |  |  |
|  | • | Consistent results across sessions |
| • Error handling for common MCP issues |  |  |
|  |  | – How to assess: Can a new user accomplish the task on first try with minimal |
|  |  | guidance? |
<!-- page break -->

## Technical requirements YAML frontmatter: The most important part

The YAML frontmatter is how Claude decides whether to load your skill. Get this

## File structure

right. yourskillname/ Minimal required format ├── SKILL. md  # Required - main skill file ├── scripts/  # Optional - executable code --- │  ├── process\_data. py # Example name: yourskillname │  └── validate. sh # Example description: What it does. Use when user asks to \[specific ├── references/  # Optional - documentation phrases\]. │  ├── apiguide. md # Example --- │  └── examples/ # Example └── assets/  # Optional - templates, etc.  └── reporttemplate. md # Example That's all you need to start.

## Field requirements


## Critical rules

name (required): SKILL. md naming: • kebabcase only • Must be exactly SKILL. md (casesensitive) • No spaces or capitals • No variations accepted (SKILL. MD, skill. md, etc.) • Should match folder name Skill folder naming: description (required): • Use kebabcase: notionprojectsetup ✅ • MUST include BOTH: • No spaces: Notion Project Setup ❌ – What the skill does – When to use it (trigger conditions) • No underscores: notion\_project\_setup ❌ • Under 1024 characters • No capitals: NotionProjectSetup ❌ • No XML tags ( < or > ) No README. md: • Include specific tasks users might say • Don't include README. md inside your skill folder • Mention file types if relevant • All documentation goes in SKILL. md or references/ • Note: when distributing via GitHub, you'll still want a repolevel README for  human users —see Distribution and Sharing. <!-- page break -->
license (optional):

# Writing effective skills

• Use if making skill open source

## The description field

• Common: MIT, Apache-2.0 According to Anthropic's engineering blog: "This metadata…… provides just compatibility (optional) enough information for Claude to know when each skill should be used without • 1-500 characters loading all of it into context." This is the first level of progressive disclosure. • Indicates environment requirements: e. g. intended product, required system  packages, network access needs, etc. Structure: metadata (optional): \[What it does\] + \[When to use it\] + \[Key capabilities\] • Any custom keyvalue pairs  • Suggested: author, version, mcpserver  • Example: Examples of good descriptions: \`\`\`yaml  metadata: author: ProjectHub

# Good - specific and actionable

version: 1.0.0 mcpserver: projecthub
|  | description: Analyzes Figma design files and generates |
| --- | --- |
| ``` | developer handoff documentation. Use when user uploads . fig |
|  | files, asks for "design specs", "component documentation", or |
| Security restrictions | "designtocode handoff". |
| Forbidden in frontmatter: | # Good - includes trigger phrases |
|  | description: Manages Linear project workflows including sprint |
• XML angle brackets (< > )
|  | planning, task creation, and status tracking. Use when user |
| --- | --- |
| • Skills with "claude" or "anthropic" in name (reserved) | mentions "sprint", "Linear tasks", "project planning", or asks |
|  | to "create tickets". |
| Why: Frontmatter appears in Claude's system prompt. Malicious content could |  |
| inject instructions. | # Good - clear value proposition |
|  | description: Endtoend customer onboarding workflow for |
|  | PayFlow. Handles account creation, payment setup, and |
|  | subscription management. Use when user says "onboard new |
|  | customer", "set up subscription", or "create PayFlow account". |
<!-- page break -->
Examples of bad descriptions: Example: \`\`\`bash

# Too vague

python scripts/fetch\_data. py --projectid PROJECT\_ID description: Helps with projects. Expected output: \[describe what success looks like\]
|  | # Missing triggers |  |
| --- | --- | --- |
|  | description: Creates sophisticated multipage documentation |  |
|  | systems. | (Add more steps as needed) |
|  | # Too technical, no user triggers |  |
|  |  | Examples |
|  | description: Implements the Project entity model with |  |
|  | hierarchical relationships. |  |
|  |  | Example 1: [common scenario] |
|  |  | User says: "Set up a new marketing campaign" |
| Writing the main instructions |  | Actions: |
| After the frontmatter, write the actual instructions in Markdown. |  | 1. Fetch existing campaigns via MCP |
|  |  | 2. Create new campaign with provided parameters |
| Recommended structure: |  |  |
|  |  | Result: Campaign created with confirmation link |
| Adapt this template for your skill. Replace bracketed sections with your specific |  |  |
| content. |  | (Add more examples as needed) |
|  | --- |  |
|  |  | Troubleshooting |
|  | name: yourskill |  |
|  | description: [ -- .] |  |
|  |  | Error: [Common error message] |
|  | --- |  |
|  |  | Cause: [Why it happens] |
|  | # Your Skill Name |  |
|  |  | Solution: [How to fix] |
|  | - # Instructions |  |
|  |  | (Add more error cases as needed) |
|  | -- # Step 1: [First Major Step] |  |
|  | Clear explanation of what happens. |  |
<!-- page break -->
Reference bundled resources clearly

# Best Practices for Instructions

Be Specific and Actionable Before writing queries, consult \`references/apipatterns.md\`  for: ✅ Good:
- Rate limiting guidance - Pagination patterns
| Run `python scripts/validate.py --input {filename}` to check | - Error codes and handling |
| --- | --- |
| data format. |  |
| If validation fails, common issues include: |  |
| - Missing required fields (add them to the CSV) |  |
|  | Use progressive disclosure |
| - Invalid date formats (use YY-MM-DD) |  |
|  | Keep SKILL. md focused on core instructions. Move detailed documentation to |
\`references/\` and link to it. (See Core Design Principles for how the three- ❌  Bad: level system works.) Validate the data before proceeding. Include error handling -# Common Issues --# MCP Connection Failed If you see "Connection refused": 1. Verify MCP server is running: Check Settings > Extensions 2. Confirm API key is valid 3. Try reconnecting: Settings > Extensions > \[Your Service\] >  Reconnect <!-- page break -->

## Chapter 3


# Testing and iteration

<!-- page break -->

### Chapter 3


# Testing and iteration

Skills can be tested at varying levels of rigor depending on your needs: Recommended Testing Approach • Manual testing in Claude. ai - Run queries directly and observe behavior. Fast Based on early experience, effective skills testing typically covers three areas: iteration, no setup required. • Scripted testing in Claude Code - Automate test cases for repeatable 1. Triggering tests validation across changes.
|  | Goal: | Ensure your skill loads at the right times. |
| --- | --- | --- |
| • Programmatic testing via skills API - Build evaluation suites that run |  |  |
| systematically against defined test sets. | Test cases: |  |
| Choose the approach that matches your quality requirements and the visibility | • ✅ | Triggers on obvious tasks |
| of your skill. A skill used internally by a small team has different testing needs | • ✅ | Triggers on paraphrased requests |
| than one deployed to thousands of enterprise users. |  |  |
|  | • ❌ | Doesn't trigger on unrelated topics |
|  | Example test suite: |  |
Pro Tip: Iterate on a single task before expanding Should trigger:
| We’ve found that the most effective skill creators iterate on a single challenging | - "Help me set up a new ProjectHub workspace" |
| --- | --- |
| task until Claude suceds, then extract the winning approach into a skill. This | - "I need to create a project in ProjectHub" |
| leverages Claude’s incontext learning and provides faster signal than broad | - "Initialize a ProjectHub project for Q4 planning" |
| testing. Once you have a working foundation, expand to multiple test cases for |  |
Should NOT trigger: coverage.
- "What's the weather in San Francisco?" - "Help me write Python code" - "Create a spreadsheet" (unless ProjectHub skill handles  sheets)
<!-- page break -->

# 2. Functional tests

With skill : Goal: Verify the skill produces correct outputs.
- Automatic workflow execution - 2 clarifying questions only
| Test cases: | - 0 failed API calls |
| --- | --- |
| • Valid outputs generated | - 6,000 tokens consumed |
| • API calls suced |  |
| • Error handling works |  |
|  | Using the skillcreator skill |
| • Edge cases covered |  |
|  | The skillcreator skill - available in Claude. ai via plugin directory or |
| Example: |  |
|  | download for Claude Code - can help you build and iterate on skills. If you |
|  | have an MCP server and know your top 2–3 workflows, you can build and test a |
| Test: Create project with 5 tasks | functional skill in a single sitting - often in 15–30 minutes. |
Given: Project name "Q4 Planning", 5 task descriptions When: Skill executes workflow Creating skills: Then: • Generate skills from natural language descriptions
  - Project created in ProjectHub  - 5 tasks created with correct properties
• Produce properly formatted SKILL. md with frontmatter
  - All tasks linked to project
• Suggest trigger phrases and structure
  - No API errors
|  | Reviewing skills: |
| --- | --- |
|  | • Flag common issues (vague descriptions, missing triggers, structural |
| 3. Performance comparison | problems) |
|  | • Identify potential over/undertriggering risks |
| Goal: Prove the skill improves results vs. baseline. |  |
|  | • Suggest test cases based on the skill's stated purpose |
| Use the metrics from Define Success Criteria . Here's what a comparison might |  |
| look like. | Iterative improvement: |
|  | • After using your skill and encountering edge cases or failures, bring those |
| Baseline comparison: |  |
examples back to skillcreator  • Example: "Use the issues & solution identified in this chat to improve how the Without skill : skill handles \[specific edge case\]"
- User provides instructions each time - 15 backandforth messages - 3 failed API calls requiring retry - 12,000 tokens consumed
<!-- page break -->
To use: Execution issues: • Inconsistent results "Use the skillcreator skill to help me build a skill for • API call failures \[your use case\]" • User corrections needed Note: skillcreator helps you design and refine skills but does not execute Solution: Improve instructions, add error handling automated test suites or produce quantitative evaluation results.

# Iteration based on feedback

Skills are living documents. Plan to iterate based on: Undertriggering signals: • Skill doesn't load when it should • Users manually enabling it • Support questions about when to use it Solution: Add more detail and nuance to the description - this may include  keywords particularly for technical terms Overtriggering signals: • Skill loads for irrelevant queries • Users disabling it • Confusion about purpose Solution: Add negative triggers, be more specific <!-- page break -->
Chapter 4 Distribution and  sharing <!-- page break -->

# Chapter 4

| Distribution and sharing |  |
| --- | --- |
| Skills make your MCP integration more complete. As users compare connectors, | Using skills via API |
| those with skills offer a faster path to value, giving you an edge over MCPonly |  |
| alternatives. | For programmatic use cases - such as building applications, agents, or automated |
|  | workflows that leverage skills - the API provides direct control over skill |
|  | management and execution. |
| Current distribution model (January 2026) |  |
|  | Key capabilities: |
| How individual users get skills: |  |
|  | • `/v1/skills` endpoint for listing and managing skills |
| 1. Download the skill folder |  |
• Add skills to Messages API requests via the \`container.skills\` parameter
2. Zip the folder (if needed) • Version control and management through the Claude Console
3. Upload to Claude. ai via Settings > Capabilities > Skills • Works with the Claude Agent SDK for building custom agents
4. Or place in Claude Code skills directory

# When to use skills via the API vs. Claude. ai:


# Organizationlevel skills:

• Admins can deploy skills workspacewide (shipped December 18, 2025) Use Case Best Surface • Automatic updates End users interacting with skills directly Claude. ai / Claude Code
| • Centralized management |  |  |
| --- | --- | --- |
|  | Manual testing and iteration during development | Claude. ai / Claude Code |
| An open standard |  |  |
|  | Individual, adhoc workflows | Claude. ai / Claude Code |
| We've published Agent Skills as an open standard. Like MCP, we believe skills |  |  |
| should be portable across tools and platforms - the same skill should work | Applications using skill s programmatically | API |
| whether you're using Claude or other AI platforms. That said, some skills are |  |  |
| designed to take full advantage of a specific platform's capabilities; authors can | Production deployments at scale | API |
| note this in the skill's compatibility field. We've been collaborating with |  |  |
| members of the ecosystem on the standard, and we're excited by early adoption. | Automated pipelines and agent systems | API |
<!-- page break -->
| Note: Skills in the API require the Code Execution Tool beta, which provides the |  |
| --- | --- |
| secure environment skills need to run. | - Select the skill folder (zipped) |
|  | 3. Enable the skill : |
| For implementation details, see: |  |
|  | - Toggle on the [Your Service] skill |
| • Skills API Quickstart |  |
|  | - Ensure your MCP server is connected |
• Create Custom skills
|  |  | 4. Test: |
| --- | --- | --- |
| • | Skills in the Agent SDK | - Ask Claude: "Set up a new project in [Your Service]" |
| Recommended approach today |  | Positioning your skill |
| Start by hosting your skill on GitHub with a public repo, clear README (for |  | How you describe your skill determines whether users understand its value and |
| human visitors —this is separate from your skill folder, which should not contain |  | actually try it. When writing about your skill—in your README, documentation, |
| a README. md), and example usage with screenshots. Then add a section |  | or marketing - keep these principles in mind. |
| to your MCP documentation that links to the skill, explains why using both |  |  |
| together is valuable, and provides a quickstart guide. |  | Focus on outcomes, not features: |
| 1. Host on GitHub |  | ✅ Good: |
|  | – Public repo for opensource skills |  |
|  | – Clear README with installation instructions | "The ProjectHub skill enables teams to set up complete project |
|  | – Example usage and screenshots | workspaces in seconds —including pages, databases, and |
|  |  | templates —instead of spending 30 minutes on manual setup." |
| 2. Document in Your MCP Repo |  |  |
|  | – Link to skills from MCP documentation |  |
|  | – Explain the value of using both together |  |
|  |  | ❌ Bad: |
|  | – Provide quickstart guide |  |
| 3. Create an Installation Guide |  | "The ProjectHub skill is a folder containing YAML frontmatter |
|  |  | and Markdown instructions that calls our MCP server tools." |
|  | - # Installing the [Your Service] skill |  |
|  | 1. Download the skill : |  |
Highlight the MCP + skills story:
| - Clone repo: `git clone https: - /github. com/yourcompany/ |  |
| --- | --- |
| skills` |  |
| - Or download ZIP from Releases | "Our MCP server gives Claude access to your Linear projects. |
|  | Our skill s teach Claude your team's sprint planning workflow. |
| 2. Install in Claude: | Together, they enable AIpowered project management." |
| - Open Claude. ai > Settings > skill s |  |
| - Click "Upload skill " |  |
<!-- page break -->
Chapter 5 Patterns and  troubleshooting <!-- page break -->

# Chapter 5

| Patterns and troubleshooting |  |
| --- | --- |
| These patterns emerged from skills created by early adopters and internal teams. | Pattern 1: Sequential workflow orchestration |
| They represent common approaches we've seen work well, not prescriptive |  |
| templates. | Use when: Your users need multistep processes in a specific order. |
|  | Example structure: |
| Choosing your approach: Problemfirst vs. toolfirst |  |
| Think of it like Home Depot. You might walk in with a problem - "I need to fix a | - # Workflow: Onboard New Customer |
| kitchen cabinet" - and an employee points you to the right tools. Or you might |  |
| pick out a new drill and ask how to use it for your specific job. | -- # Step 1: Create Account |
Call MCP tool: \`create\_customer\` Skills work the same way: Parameters: name, email, company • Problemfirst: "I need to set up a project workspace" → Your skill orchestrates --# Step 2: Setup Payment the right MCP calls in the right sequence. Users describe outcomes; the skill Call MCP tool: \`setup\_payment\_method\` handles the tools. Wait for: payment method verification • Toolfirst: "I have Notion MCP connected" → Your skill teaches Claude the  optimal workflows and best practices. Users have access; the skill provides --# Step 3: Create Subscription expertise. Call MCP tool: \`create\_subscription\` Parameters: plan\_id, customer\_id (from Step 1)
| Most skills lean one direction. Knowing which framing fits your use case helps |  |
| --- | --- |
| you choose the right pattern below. | -- # Step 4: Send Welcome Email |
Call MCP tool: \`send\_email\` Template: welcome\_email\_template Key techniques: • Explicit step ordering • Dependencies between steps • Validation at each stage • Rollback instructions for failures <!-- page break -->
| Pattern 2: Multi-MCP coordination |  | Pattern 3: Iterative refinement |
| --- | --- | --- |
| Use when: | Workflows span multiple services. | Use when: Output quality improves with iteration. |
| Example: Designtodevelopment handoff |  | Example: Report generation |
|  | -- # Phase 1: Design Export (Figma MCP) | - # Iterative Report Creation |
|  | 1. Export design assets from Figma |  |
|  | 2. Generate design specifications | -- # Initial Draft |
|  | 3. Create asset manifest | 1. Fetch data via MCP |
2. Generate first draft report
| -- # Phase 2: Asset Storage (Drive MCP) | 3. Save to temporary file |
| --- | --- |
| 1. Create project folder in Drive |  |
| 2. Upload all assets | -- # Quality Check |
| 3. Generate shareable links | 1. Run validation script: `scripts/check_report.py` |
2. Identify issues:
| -- # Phase 3: Task Creation (Linear MCP) | - Missing sections |
| --- | --- |
| 1. Create development tasks | - Inconsistent formatting |
| 2. Attach asset links to tasks | - Data validation errors |
| 3. Assign to engineering team |  |
--# Refinement Loop
| -- # Phase 4: Notification (Slack MCP) | 1. Address each identified issue |
| --- | --- |
| 1. Post handoff summary to #engineering | 2. Regenerate affected sections |
| 2. Include asset links and task references | 3. Revalidate |
4. Repeat until quality threshold met --# Finalization Key techniques:
1. Apply final formatting • Clear phase separation
2. Generate summary 3. Save final version • Data passing between MCPs • Validation before moving to next phase • Centralized error handling Key techniques: • Explicit quality criteria • Iterative improvement • Validation scripts • Know when to stop iterating <!-- page break -->

# Pattern 4: Contextaware tool selection


# Pattern 5: Domainspecific intelligence

Use when: Same outcome, different tools depending on context. Use when: Your skill adds specialized knowledge beyond tool access. Example: File storage Example: Financial compliance
| - # Smart File Storage | - # Payment Processing with Compliance |
| --- | --- |
| -- # Decision Tree | -- # Before Processing (Compliance Check) |
| 1. Check file type and size | 1. Fetch transaction details via MCP |
| 2. Determine best storage location: | 2. Apply compliance rules: |
| - Large files (>10MB): Use cloud storage MCP | - Check sanctions lists |
| - Collaborative docs: Use Notion/Docs MCP | - Verify jurisdiction allowances |
| - Code files: Use GitHub MCP | - Assess risk level |
| - Temporary files: Use local storage | 3. Document compliance decision |
| -- # Execute Storage | -- # Processing |
| Based on decision: | IF compliance passed: |
| - Call appropriate MCP tool | - Call payment processing MCP tool |
| - Apply servicespecific metadata | - Apply appropriate fraud checks |
| - Generate access link | - Process transaction |
|  | ELSE: |
| -- # Provide Context to User | - Flag for review |
| Explain why that storage was chosen | - Create compliance case |
|  | -- # Audit Trail |
| Key techniques: | - Log all compliance checks |
|  | - Record processing decisions |
• Clear decision criteria
- Generate audit report
• Fallback options • Transparency about choices Key techniques: • Domain expertise embedded in logic • Compliance before action • Comprehensive documentation • Clear governance <!-- page break -->

# Troubleshooting


# Wrong name: My Cool Skill


## Skill won't upload


# Correct

Error: "Could not find SKILL. md in uploaded folder" name: mycoolskill
| Cause: File not named exactly SKILL. md |  |
| --- | --- |
| Solution : |  |
|  | Skill doesn't trigger |
| • Rename to SKILL. md (casesensitive) |  |
| • Verify with: ls -la should show SKILL. md | Symptom: Skill never loads automatically |
| Error: "Invalid frontmatter" | Fix: |
| Cause: YAML formatting issue | Revise your description field. See The Description Field for good/bad examples. |
| Common mistakes: | Quick checklist: |
|  | • Is it too generic? ("Helps with projects" won't work) |
| # Wrong - missing delimiters | • Does it include trigger phrases users would actually say? |
name: myskill • Does it mention relevant file types if applicable? description: Does things Debugging approach:

# Wrong - unclosed quotes name: myskill

Ask Claude: "When would you use the \[skill name\] skill?" Claude will quote the description: "Does things description back. Adjust based on what's missing.

# Correct


## Skill triggers too often

--- name: myskill Symptom: Skill loads for unrelated queries description: Does things --- Solutions: 1. Add negative triggers Error: "Invalid skill name" description: Advanced data analysis for CSV files. Use for Cause: Name has spaces or capitals statistical modeling, regression, clustering. Do NOT use for  simple data exploration (use dataviz skill instead). <!-- page break -->
| 2. Be more specific | Instructions not followed |
| --- | --- |
|  | Symptom: Skill loads but Claude doesn't follow instructions |
| # Too broad |  |
| description: Processes documents |  |
|  | Common causes: |
| # More specific | 1. Instructions too verbose |
| description: Processes PDF legal documents for contract review | – Keep instructions concise |
– Use bullet points and numbered lists – Move detailed reference to separate files
3. Clarify scope
2. Instructions buried – Put critical instructions at the top description: PayFlow payment processing for ecommerce. Use – Use ## Important or ## Critical headers specifically for online payment workflows, not for general – Repeat key points if needed financial queries.
3. Ambiguous language

# Bad


# MCP connection issues

Make sure to validate things properly Symptom: Skill loads but MCP calls fail

# Good CRITICAL: Before calling create\_project, verify:

Checklist:
- Project name is nonempty
1. Verify MCP server is connected
- At least one team member assigned
– Claude. ai: Settings > Extensions > \[Your Service\]
- Start date is not in the past
– Should show "Connected" status  Advanced technique: For critical validations, consider bundling a script
2. Check authentication that performs the checks programmatically rather than relying on language – API keys valid and not expired instructions. Code is deterministic; language interpretation isn't. See the Office – Proper permissions/scopes granted skills for examples of this pattern. – OAuth tokens refreshed
4. Model "laziness" Add explicit encouragement:
3. Test MCP independently – Ask Claude to call MCP directly (without skill) – "Use \[Service\] MCP to fetch my projects" -# Performance Notes – If this fails, issue is MCP not skill
- Take your time to do this thoroughly - Quality is more important than speed
4. Verify tool names
- Do not skip validation steps
– Skill references correct MCP tool names – Check MCP server documentation Note: Adding this to user prompts is more effective than in SKILL. md – Tool names are casesensitive <!-- page break -->

# Large context issues

Symptom: Skill seems slow or responses degraded Causes: • Skill content too large • Too many skills enabled simultaneously • All content loaded instead of progressive disclosure Solutions: 1. Optimize SKILL. md size – Move detailed docs to references/ – Link to references instead of inline – Keep SKILL. md under 5,000 words 2. Reduce enabled skills – Evaluate if you have more than 20 - 50 skills enabled simultaneously – Recommend selective enablement – Consider skill "packs" for related capabilities <!-- page break -->
Chapter 6 Resources and  references <!-- page break -->

### Chapter 6


# Resources and references

If you're building your first skill, start with the Best Practices Guide, then Tools and Utilities reference the API docs as needed.

### skillcreator skill:

Official Documentation • Built into Claude. ai and available for Claude Code • Can generate skills from descriptions

### Anthropic Resources:

• Reviews and provides recommendations • Best Practices Guide • Use: "Help me build a skill using skillcreator" • Skills Documentation • API Reference Validation: • MCP Documentation • skillcreator can assess your skills • Ask: "Review this skill and suggest improvements"

### Blog Posts:

• Introducing Agent Skills

## Getting Support

• Engineering Blog: Equipping Agents for the Real World

### For Technical Questions:

• Skills Explained • General questions: Community forums at the Claude Developers Discord • How to Create Skills for Claude • Building Skills for Claude Code

### For Bug Reports:

• Improving Frontend Design through Skills • GitHub Issues: anthropics/skills/issues • Include: Skill name, error message, steps to reproduce

## Example skills


### Public skills repository:

• GitHub: anthropics/skills • Contains Anthropiccreated skills you can customize <!-- page break -->

# Before upload

| Reference A: Quick |  |
| --- | --- |
|  | Tested triggering on obvious tasks |
| checklist | Tested triggering on paraphrased requests |
|  | Verified doesn't trigger on unrelated topics |
| Use this checklist to validate your skill before and after upload. If you want |  |
|  | Functional tests pass |
| a faster start, use the skillcreator skill to generate your first draft, then run |  |
| through this list to make sure you haven't missed anything. | Tool integration works (if applicable) |
|  | Compressed as . zip file |
| Before you start |  |

# After upload

  Identified 2-3 concrete use cases
| Tools identified (builtin or MCP) | Test in real conversations |
| --- | --- |
| Reviewed this guide and example skills | Monitor for under/overtriggering |
| Planned folder structure | Collect user feedback |
|  | Iterate on description and instructions |
| During development | Update version in metadata |
  Folder named in kebabcase  SKILL. md file exists (exact spelling)  YAML frontmatter has --- delimiters  name field: kebabcase, no spaces, no capitals  description includes WHAT and WHEN  No XML tags (< >) anywhere  Instructions are clear and actionable  Error handling included  Examples provided  References clearly linked <!-- page break -->

## Security notes


# Reference B: YAML


### Allowed:


# frontmatter

• Any standard YAML types (strings, numbers, booleans, lists, objects) • Custom metadata fields

## Required fields

• Long descriptions (up to 1024 characters) --- ### Forbidden: name: skillnameinkebabcase • XML angle brackets (< >) - security restriction description: What it does and when to use it. Include specific  trigger phrases. • Code execution in YAML (uses safe YAML parsing) --- • Skills named with "claude" or "anthropic" prefix (reserved)

## All optional fields

name: skillname description: \[required description\] license: MIT # Optional: License for opensource allowedtools: "Bash(python:\*) Bash(npm:\*) WebFetch" # Optional:  Restrict tool access metadata: # Optional: Custom fields  author: Company Name  version: 1.0.0  mcpserver: servername  category: productivity  tags: \[projectmanagement, automation\]  documentation: https:-/example. com/docs  support: support@example. com <!-- page break -->

# Reference C: Complete skill


# examples

For full, productionready skills demonstrating the patterns in this guide:  • Document Skills - PDF , DOCX , PPTX , XLSX creation • Example Skills - Various workflow patterns • Partner Skills Directory - View skills from various partners such as Asana,  Atlassian, Canva, Figma, Sentry, Zapier, and more These repositories stay uptodate and include additional examples beyond  what's covered here. Clone them, modify them for your use case, and use them as  templates. <!-- page break -->
claude. ai
