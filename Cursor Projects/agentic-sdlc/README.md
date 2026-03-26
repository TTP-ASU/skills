# Agentic SDLC (all phases – PM use)

This folder contains **all SDLC phase skills** so they appear in the Cursor Skills panel. Use them for Product Briefs, PRDs, review, handoff, verification, and operations.

## Phases (Skills panel)

| Phase | Purpose |
|-------|---------|
| **00-orchestrator** | Route to the right phase; suggest project docs and MCPs |
| **01-discover-define** | Product Briefs, PRDs, scope |
| **02-review** | Review briefs, PRDs, designs |
| **03-handoff** | Epics, user stories, Jira/DevOps creation |
| **04-verify** | Acceptance criteria, sign-off |
| **05-operate** | Runbooks, launch, incidents |
| **domain** | Architecture and system context |
| **reference** | Templates and standards |

## Dashboard building blocks

- **Project-specific context:** Put key docs and connections in **PROJECT-CONTEXT.md** (repo root) or `docs/PROJECT-CONTEXT.md`. The agent uses it for the current project.
- **Cursor rules:** `.cursor/rules/project-building-blocks.mdc` is always applied so the agent uses these phases and your project docs/MCPs.

For the **full UBIF Stores agentic SDLC** (including virtual-sme-panel and extra assets), clone the repo that contains `Skills/agentic-sdlc` as described in Asurion’s **UBIF Stores Cursor Setup** (Notion or your team).

See **ASURION-CURSOR-SETUP.md** at the repo root for the full Product skills overview.
