Zach Lloyd
@zachlloydtweets
How to build a self-improvement loop for your Skills
如何为你的技能打造一个自我提升的闭环
22
114
901
73K
7.3 万
There’s been a lot of chatter about using “loops” lately to drive agents, and I think this has been accompanied by a bit of “what actually is a loop”?
最近关于用“循环”来驱动智能体的讨论很多，而随之而来的一个问题就是：“到底什么是循环呢？”
I can’t speak for everyone else using the term, but I wanted to show a practical approach using Skills and cloud agents for a particularly powerful kind of loop: a self-improvement loop.
我无法代表所有使用这一术语的人，但我想通过技能与云端智能体的结合，展示一种实用的方法，实现一种特别强大的循环——自我提升循环。
This is the idea that an agent can improve the quality of its own Skills over time from external feedback. My example is a loop that involves a human feedback step, but if you have a clear goal that doesn’t require a human, you can use the same method with an automated grader.
其核心思想是：智能体能够借助外部反馈，随着时间推移不断提升自身技能的质量。我的示例中包含了一个需要人类参与的反馈环节，但如果你的目标明确且无需人工介入，也可以采用同样的方法，配合自动化评分机制来完成。
To make matters concrete, say this Skill does issue triage, separating incoming issues into a few buckets: ready-to-implement, duplicate, needs-info. This would also work for a code review Skill, a bug fixing Skill, an incident response Skill, and so on.
为了更具体地说明，假设某项技能负责对收到的问题进行分类处理，将其划分为几个类别：可立即实施、重复问题、需补充信息等。这种方法同样适用于代码评审技能、缺陷修复技能、事件响应技能等等。
Here’s what a first draft of the Skill might look like:
Full triage-issue Skill
What you need to do is set up the following loops:
An inner agent loop: this is where you actually apply the Skill. For issue triage, you could be running it manually, or, more likely, you have an integration with your task tracker that runs the Skill whenever a new issue is filed. Interactions with the Skill are recorded somewhere: in a file, an agent trace, or an interaction in an external system like Slack or Github.
An outer agent loop: this is an agent that runs on a schedule and observes the inner loop use of the Skill. For the issue triager, this will likely be a cloud agent that pulls records of every time the Triage agent ran. Its job is to look at all the runs of the inner agent and adjust its Skill based on the performance of those runs. Since Skills are just files, this means it should make a diff to improve Skill based on user feedback from past runs.
I’ll show you how to do this in practice using Warp and Oz, our cloud agent platform, but there are lots of ways you can accomplish it. We will use Github Issues as the issue tracker.
Here is a sample repo with the Skills and GitHub workflows to follow along.
Step 1: set up the inner agent loop
The inner agent loop uses a Github action that runs on every new issue created.
Full GitHub Action
The Github action invokes a cloud agent through Oz, Warp’s cloud agent platform. This cloud agent syncs the repo, pulls in the issue contents from github, and tries to classify it. The code on how to set this up is in the repo linked below.
Now when a new issue comes in, a cloud agent runs the inner loop triaging skill, and applies a label indicating that a new feature request is ready to implement.
Step 2: set up the outer loop for self-improvement
Let’s say though that a human reviewer doesn’t agree with the agent assignment. As a person looking at the agent’s assigned labels, I switch the issue from “ready to implement” to “needs info” and add a comment on the thread as to why it was mis-categorized, e.g. because there is ambiguity on whether we should add a setting for the new feature.
Here’s where the outer loop becomes interesting. The outer loop agent runs once a day and looks at all issues that have been triaged, and when it runs, it will find that I manually adjusted the label and gave a reason why.
Full improve-triage-issue Skill
Since the outer loop agent Skill is run through a coding agent, it will take the feedback I provided and make a diff to update the triage Skill.
Once that diff merges, it feeds back into Skill that drives the inner loop agent, and the next time the agent runs the Skill should work better.
Would love to know if this is useful for folks. We use self improvement loops to manage the Warp open-source repository, and we extracted the framework behind it for others to adopt. Early version here.
Want to publish your own Article?
Upgrade to Premium
11:39 PM · Jun 16, 2026
·
73.8K
 Views
22
114
901
2.2K
Relevant
View quotes
