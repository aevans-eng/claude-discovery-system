# Discovery Protocol & Project Registry (v1 — YYYY-MM-DD)

## How to Orient
1. This file loads automatically every session. You now have the project dashboard below.
2. When the user asks to work on a project → read its STATE.md first.
3. If the project has a CLAUDE.md → read that for rules/conventions.
4. Only read deeper docs if STATE.md's file map says they're needed for the task.
5. "Entering a project" = substantive work. Quick factual lookups can use the registry alone.

## How to Update
- After finishing work on a project → update its STATE.md (what was done, what's next).
- After updating any STATE.md → sync that project's row below (status, last-touched, next).
- Before session ends → ensure STATE.md and registry reflect current state.
- If a project's last-touched date looks stale → reconcile by reading the project folder.

## Project Registry

| Project | Folder | Purpose | Status | Last Touched | Next Action | Connections |
|---------|--------|---------|--------|-------------|-------------|-------------|
| Example App | app/ | Main product | Active | 2026-01-15 | Add auth flow | → api (backend) |
| API Server | api/ | REST backend | Active | 2026-01-14 | Deploy v2 | ← app (frontend) |
| Docs Site | docs-site/ | Public documentation | Needs update | 2026-01-10 | Sync with v2 API | ← api |
| Old Dashboard | legacy/ | Deprecated UI | Dormant | — | — | — |

## Non-Project Folders
These folders are part of the workspace but don't get STATE.md files.

| Folder | Purpose |
|--------|---------|
| scripts/ | Build scripts, CI helpers, dev utilities |
| shared/ | Shared libraries and types |
| .config/ | Project-wide configuration |

## Cross-Project Links
- App depends on API → API changes may break app
- Docs must stay in sync with API (update after every API release)
- Shared types used by both app and API → changes affect both
