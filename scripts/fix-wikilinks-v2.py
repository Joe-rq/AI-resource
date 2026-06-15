#!/usr/bin/env python3
"""Fix 22 orphan wikilinks: convert old link text to correct page title."""
import re, os, sys

wiki = sys.argv[1] if len(sys.argv) > 1 else '/Users/qrq/AI/AI-resource/wiki'

fixes = {
    'Agent-Runtime': 'Agent Runtime',
    'Agent-Secure-Runtime': 'Agent Secure Runtime',
    'Agent-Harness-治理协议': 'Agent Harness 治理协议',
    'Agent-Macro-Evaluation': 'Agent Macro Evaluation',
    'Multi-Agent-协作模式': 'Multi-Agent 协作模式',
    'Meta-Reflection-Techniques': 'Meta Reflection Techniques',
    'Thin-Harness-Fat-Skills': 'Thin Harness, Fat Skills',
    'Worker-Verifier 对抗循环': 'Worker Verifier 对抗循环',
    'Thin Harness Fat Skills': 'Thin Harness, Fat Skills',
    '08-agent-runtime-battlefield': '08 - Agent Runtime 主战场',
    '10-singapore-fm-nanoclaws-second-brain': '新加坡外长的 AI 第二大脑',
    '11-hermes-agent-nous-research': 'Hermes Agent：Nous Research 的开源 Agent 框架',
    '19-addyosmani-loop-engineering': 'Loop Engineering：从 Prompt 到系统设计',
    'A harness for every task': 'A harness for every task: Anthropic 官方 Dynamic Workflows 深度解读',
    'Agent Memory/index': 'Agent Memory',
    'Claude-Code-Skills/index': 'Claude Code Skills',
    'Claude-Code-Subagent/index': 'Claude Code Subagent',
    'Agent-Memory/architecture': 'Agent Memory Architecture',
    'Agent-Memory/forgetting-and-compaction': 'Forgetting & Compaction',
    'Agent-Memory/self-evolving-memory': 'Self-Evolving Memory',
    'Claude Code Dynamic Workflows': 'Claude Code Dynamic Workflows 实践指南',
}

files_changed = set()

for root, dirs, files in os.walk(wiki):
    for f in files:
        if not f.endswith('.md'):
            continue
        path = os.path.join(root, f)
        with open(path) as fh:
            content = fh.read()

        new_content = content
        for old, new in fixes.items():
            escaped = re.escape(old)
            # Plain link: [[old]] → [[new]]
            new_content = re.sub(
                r'\[\[' + escaped + r'\]\]',
                '[[' + re.escape(new) + ']]',
                new_content
            )
            # Link with display: [[old|display]] → [[new|display]]
            new_content = re.sub(
                r'\[\[' + escaped + r'\|([^\]]+)\]\]',
                lambda m, n=new: '[[' + n + '|' + m.group(1) + ']]',
                new_content
            )

        if new_content != content:
            with open(path, 'w') as fh:
                fh.write(new_content)
            files_changed.add(os.path.relpath(path, wiki))

print(f"Files changed: {len(files_changed)}")
for fc in sorted(files_changed):
    print(f"  {fc}")
