# Setup Guide

## Quick Start (5 minutes)

### Step 1: Verify `.claude/rules/` works

Create a test file to confirm auto-loading:

```bash
mkdir -p .claude/rules
echo '# Test\nIf you see this, say "AUTOLOAD WORKS".' > .claude/rules/test.md
```

Start a new Claude Code session and send any message. If Claude mentions the test, it works. Delete the test file:

```bash
rm .claude/rules/test.md
```

> **If it doesn't work:** Skip `.claude/rules/` and add the discovery protocol directly as a section in your `CLAUDE.md`. You lose the compaction-survival benefit but the system still works.

### Step 2: Create the discovery protocol

Copy `templates/discovery-protocol.md` to `.claude/rules/discovery-protocol.md`:

```bash
cp templates/discovery-protocol.md .claude/rules/discovery-protocol.md
```

Edit the file to match your projects. Replace the example entries with your actual projects, folders, statuses, and connections.

**Keep it under 80 lines** — this file is injected into every prompt.

### Step 3: Create STATE.md for each active project

Copy the template into each active project folder:

```bash
cp templates/STATE.md my-project/STATE.md
```

Fill in the current state. Light projects might be 15 lines; complex ones 40-50. Only "Status" and "What's Next" are required sections.

### Step 4: Add to CLAUDE.md

Add this to your root `CLAUDE.md`:

```markdown
## Session Startup
Session orientation is handled by `.claude/rules/discovery-protocol.md` (auto-loaded).
It contains the project registry, orientation protocol, and update protocol.
```

### Step 5: (Optional) Trim CLAUDE.md / MEMORY.md

If your `CLAUDE.md` or `MEMORY.md` contain project status information (workspace tables, project summaries, etc.), move that content into the discovery system:

- Workspace/project tables → registry in `discovery-protocol.md`
- Per-project summaries → `STATE.md` files
- Keep behavioral rules, preferences, and conventions where they are

---

## Automated Setup (paste to Claude)

If you'd rather have Claude set it up for you, paste this prompt into a Claude Code session:

````
I want to set up a project discovery system for this workspace. Here's the architecture:

1. Create `.claude/rules/discovery-protocol.md` with:
   - An orientation protocol (read STATE.md when entering a project, read CLAUDE.md for rules)
   - An update protocol (update STATE.md after work, sync the registry)
   - A project registry table with columns: Project, Folder, Purpose, Status, Last Touched, Next Action, Connections
   - A non-project folders table for utility directories
   - A cross-project links section

2. Create a `STATE.md` in each active project folder with:
   - Status (one line)
   - What Changed Last Session (bullet list, overwritten each session)
   - What's Next (priority order)
   - File Map (table: "what you need" → "read this file")
   - Open Questions / Blockers
   - Footer comment: <!-- After updating this file, sync status to discovery-protocol.md registry -->

3. Add to CLAUDE.md: "Session orientation is handled by `.claude/rules/discovery-protocol.md` (auto-loaded)."

4. If CLAUDE.md or MEMORY.md have project status tables or summaries, move that content into the discovery system files and remove it from the originals. Keep behavioral rules and preferences in place.

First, explore my workspace to understand what projects exist, then create all the files. Keep the registry under 80 lines.
````

---

## Maintenance

Claude handles all maintenance automatically — you never need to touch these files. The update protocol in `discovery-protocol.md` tells Claude when and how to update.

**If things go stale:** This happens when sessions end abruptly (crashes, usage limits). Next session, Claude should notice stale dates in the registry and reconcile. If it doesn't, just say: "Check the discovery protocol — some projects look stale."

**To add a new project:** Just tell Claude about it. The protocol says to create a registry row + STATE.md immediately.

**To iterate on the format:** Edit `discovery-protocol.md` directly. Bump the version line. No ceremony needed.

---

## Adapting for Other AI Tools

The discovery system works with any AI tool that reads markdown files:

| Tool | Auto-loading | Setup |
|------|-------------|-------|
| **Claude Code** | `.claude/rules/` auto-loads | Full support — follow steps above |
| **Gemini CLI** | `GEMINI.md` auto-loads | Add the protocol content to `GEMINI.md` or reference it |
| **Codex CLI** | `AGENTS.md` auto-loads | Add the protocol content to `AGENTS.md` or reference it |
| **Other** | Varies | Include "read `.claude/rules/discovery-protocol.md` first" in your system prompt |

For tools without auto-loading, the system still works — just tell the AI to read `discovery-protocol.md` at the start of each session.
