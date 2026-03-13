# Claude Code Discovery System

A standardized hub-and-spoke architecture for orienting AI assistants (Claude, Gemini, Codex, etc.) across multi-project workspaces. Solves three problems:

1. **Cold start** — new sessions waste tokens re-discovering project state
2. **Staleness** — AI acts on outdated info and makes wrong moves
3. **Inconsistency** — some projects are well-documented, others are black boxes

## How It Works

```
Session Start (automatic):
  ┌─────────────┐     ┌──────────────┐     ┌──────────────────────┐
  │  CLAUDE.md   │     │  MEMORY.md   │     │ discovery-protocol.md│
  │  (rules)     │     │  (memories)  │     │ (registry + protocol)│
  └─────────────┘     └──────────────┘     └──────────────────────┘
        │                     │                        │
        └─────────────────────┴────────────────────────┘
                              │
                     AI is now oriented
                              │
Entering a project (on-demand):
                              │
                    ┌─────────▼─────────┐
                    │  project/STATE.md  │
                    │  (detailed state)  │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ project/CLAUDE.md  │
                    │ (project rules)    │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Deeper docs      │
                    │ (only if needed)   │
                    └───────────────────┘
```

## File Tiers

| Tier | File | Location | Auto-loaded? | Purpose |
|------|------|----------|-------------|---------|
| 0 | `CLAUDE.md` | project root | Yes (always) | Rules, conventions — **how** to work |
| 0 | `MEMORY.md` | memory dir | Yes (first 200 lines) | Behavioral memories — **who** the user is |
| 1 | `discovery-protocol.md` | `.claude/rules/` | Yes (always, survives compaction) | Dashboard — **what** exists + orient/update protocol |
| 2 | `STATE.md` | per-project folder | On-demand | **Where** a specific project stands |

### Why `.claude/rules/`?

Files in `.claude/rules/` auto-load every session **and** reload after context compaction. This is the key enforcement mechanism — even after the AI's context is compressed multiple times, it still sees the orientation and update instructions.

## Setup

### 1. Create the discovery protocol

Copy [`templates/discovery-protocol.md`](templates/discovery-protocol.md) to `.claude/rules/discovery-protocol.md` in your workspace root. Edit the project registry to match your projects.

### 2. Create STATE.md for each active project

Copy [`templates/STATE.md`](templates/STATE.md) into each active project folder. Fill in the current state.

### 3. Add a reference in CLAUDE.md

Add to your root `CLAUDE.md`:

```markdown
## Session Startup
Session orientation is handled by `.claude/rules/discovery-protocol.md` (auto-loaded).
It contains the project registry, orientation protocol, and update protocol.
```

### 4. (Optional) Trim CLAUDE.md and MEMORY.md

Move project state out of CLAUDE.md and MEMORY.md into the discovery system:
- Workspace/project tables → registry in `discovery-protocol.md`
- Project summaries → per-project `STATE.md` files
- Keep behavioral rules, feedback, and conventions in CLAUDE.md/MEMORY.md

## Protocols

### Orientation Protocol (session start)

1. `discovery-protocol.md` loads automatically — AI sees the project dashboard.
2. When the user asks to work on a project → AI reads that project's `STATE.md`.
3. If the project has a `CLAUDE.md` → AI reads that for rules/conventions.
4. Deeper docs only if `STATE.md`'s file map says they're needed.
5. "Entering a project" = substantive work. Quick factual lookups use the registry alone.

### Update Protocol (during/after work)

| Trigger | Action |
|---------|--------|
| After finishing work on a project | Update its `STATE.md` (what was done, what's next) |
| After updating any `STATE.md` | Sync that project's row in the registry (status, last-touched, next) |
| Before session ends | Ensure `STATE.md` and registry reflect current state |
| Stale last-touched date detected | Reconcile by reading the project folder |

### Enforcement Layers

1. **Primary:** `discovery-protocol.md` in `.claude/rules/` — always loaded, survives compaction
2. **Secondary:** CLAUDE.md reference — backup pointer to the protocol
3. **Tertiary:** `STATE.md` footer comment — reminder visible when editing

### Graceful Degradation

If a session ends abruptly (crash, usage limit), updates may not happen. Next session, the AI notices stale dates in the registry, reconciles by reading the project folder, then updates before proceeding.

## Token Efficiency

The system is designed to be token-efficient:

- **Registry:** ~40-50 lines auto-loaded per session (~300 tokens). Negligible overhead.
- **STATE.md:** Only loaded on-demand when entering a project. Not auto-loaded.
- **Net effect:** If you move project state *out* of CLAUDE.md/MEMORY.md and *into* the discovery system, the auto-loaded context may actually shrink.
- **Real savings:** Eliminates wasteful scanning, wrong-file reads, and corrections from stale info.

### Budget Constraints

- Keep `discovery-protocol.md` under **80 lines** (it's injected into every prompt)
- Keep `MEMORY.md` under **200 lines** (only first 200 auto-load)
- `STATE.md` files can be any length (loaded on-demand), but 15-50 lines is typical

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| New project mid-session | AI creates both a registry row and a minimal `STATE.md` |
| Project moves folders | AI searches for it, updates the registry path |
| Multiple projects in one session | Update each `STATE.md` after finishing, sync registry after each |
| Registry grows large (>20 rows) | Split into active vs. archived sections |

## Iteration

- Version line in the registry (`v1 — YYYY-MM-DD`) — bump on format changes
- Review every ~2 weeks for deficiencies
- Watch for: STATE.md bloat, registry staleness, unnecessary reads, unused sections

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with `.claude/rules/` support
- Works with any AI tool that reads markdown files for orientation (Gemini, Codex, etc.) — they just won't get the auto-loading benefit without `.claude/rules/`

## License

MIT
