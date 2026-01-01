# CLAUDE.md

**This file has been reorganized for better multi-AI collaboration.**

## 📁 New Structure

AI development instructions are now located in the `.ai/` directory:

### For All AI Assistants
**📄 [`.ai/agents.md`](.ai/agents.md)** - Universal instructions for working with this codebase
- Repository architecture and patterns
- Technology stack and versions
- Development commands
- Common workflows
- Live internet research protocol (mandatory for all AIs)

### For Claude Code Specifically
**📄 [`.ai/claude.md`](.ai/claude.md)** - Claude-specific tool usage and autonomous workflows
- WebSearch, Read, Edit, Write, Bash tool patterns
- Multi-file change workflows
- Schema synchronization procedures
- TodoWrite progress tracking
- VSCode integration patterns

---

## Quick Links

- **Architecture Overview**: [`.ai/agents.md#repository-overview`](.ai/agents.md#repository-overview)
- **Development Commands**: [`.ai/agents.md#development-commands`](.ai/agents.md#development-commands)
- **Schema Sync Workflow**: [`.ai/agents.md#critical-cross-repo-workflow-schema-synchronization`](.ai/agents.md#critical-cross-repo-workflow-schema-synchronization)
- **Claude Tool Usage**: [`.ai/claude.md#claude-code-tool-usage`](.ai/claude.md#claude-code-tool-usage)

---

**Why the change?**
- **Better organization**: Separates universal knowledge from tool-specific workflows
- **Multi-AI friendly**: Other AI providers (GPT-4, Gemini) can use `agents.md`
- **Maintainability**: Framework updates go in one place, tool patterns in another
- **Discoverability**: Industry-standard `.ai/` directory convention
