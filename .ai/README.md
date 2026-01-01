# .ai/ Directory

This directory contains instructions for AI assistants working with the Edinburgh Finds codebase.

## Files

### [`agents.md`](agents.md)
**Universal AI Instructions** - For ALL AI assistants (Claude, GPT-4, Gemini, etc.)

Contains:
- Repository architecture and design patterns
- Technology stack with current versions
- Development commands (npm, pip, bash)
- Common workflows (adding venues, extending schema, debugging)
- **Mandatory live internet research protocol**
- Security checklist
- Framework-specific best practices

**Use this when:**
- Learning the codebase architecture
- Checking current package versions
- Understanding data flow patterns
- Following development workflows

### [`claude.md`](claude.md)
**Claude Code-Specific Instructions** - For Claude Code only

Contains:
- Tool usage patterns (WebSearch, Read, Edit, Write, Bash)
- Multi-file change workflows
- Autonomous task planning with TodoWrite
- Schema synchronization procedures
- Error handling patterns
- VSCode integration

**Use this when:**
- Making code changes with Claude Code
- Running autonomous workflows
- Coordinating multi-repo changes
- Debugging with Claude's tools

## Directory Structure

```
.ai/
├── README.md                      # This file
├── agents.md                      # Universal AI instructions
├── claude.md                      # Claude Code-specific workflows
└── context/                       # Deep-dive documentation
    └── architecture-review.md     # Scalability concerns & planned improvements
```

## Quick Reference

| Task | File to Read |
|------|-------------|
| Understanding the monorepo architecture | `agents.md#repository-overview` |
| **Understanding planned improvements & what to avoid** | `agents.md#architecture-review--future-direction` |
| **Reading detailed architecture analysis** | `context/architecture-review.md` |
| Checking current package versions | `agents.md#technology-stack` |
| Running development commands | `agents.md#development-commands` |
| Learning the confidence tracking system | `agents.md#confidence-tracking-system` |
| Syncing database schema (critical!) | `agents.md#critical-cross-repo-workflow-schema-synchronization` |
| Using Claude's WebSearch tool | `claude.md#live-internet-research-websearch` |
| Making multi-file changes | `claude.md#multi-file-code-changes` |
| Autonomous task planning | `claude.md#autonomous-task-planning` |

## For New AI Instances

**Start here:**
1. Read [`agents.md`](agents.md) first - understand the architecture **and future direction**
2. Skim [`context/architecture-review.md`](context/architecture-review.md) - understand what NOT to perpetuate
3. Check package versions in `edinburgh_finds_web/package.json` and `edinburgh_finds_backend/requirements.txt`
4. If using Claude Code, also read [`claude.md`](claude.md) for tool-specific workflows
5. **Always search the internet for version-specific documentation** before coding (see agents.md research protocol)

## For Humans

This directory helps AI assistants work more effectively with your codebase by:
- Providing current architecture documentation
- Enforcing version-aware development (live internet research)
- Separating universal patterns from tool-specific workflows
- Maintaining consistency across different AI providers

You can edit these files to update AI behavior without changing code.
