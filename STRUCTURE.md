# Master structure: rules and skills for any project

This repo is your **single place** for rules and skills you use across projects. Here’s what each part is and how to use it.

---

## The three main areas (no more “Skills” confusion)

| What you see in the tree | What it is | Use it for |
|--------------------------|------------|------------|
| **`skills/`** | **Skill modules** – each subfolder is one skill (e.g. `agentic-sdlc`, `docx`). Each has a `SKILL.md` that Cursor/Claude loads. | All the skills that show up in the Skills panel. Add new skills as new subfolders under `skills/`. |
| **`skill-template/`** | **Blank skeleton for creating a new skill.** One folder with a minimal `SKILL.md`. | When you want to add a new skill: copy this folder, rename it, and edit the `SKILL.md`. Not a skill itself – it’s a starter. |
| **`templates/`** | **Product document templates** – Brief, PRD, open-questions. These are **not** skills; they’re markdown structures you copy into projects or Notion. | Use when creating or updating a Product Brief, PRD, or open-questions list. Reference from PROJECT-CONTEXT. |

So: **skills** = the actual skills. **skill-template** = how you create a new skill. **templates** = product doc shapes (Brief/PRD/open-questions).

---

## Rest of the repo

| Folder / file | What it is | Use it for |
|---------------|------------|------------|
| **`.cursor/rules/`** | **Cursor rules** – applied when this workspace is open. | Product and project behavior: PROJECT-CONTEXT, meeting notes, open questions, Brief vs PRD, quality bar. See `docs/PRODUCT-MANAGEMENT-RULES.md`. |
| **`PROJECT-CONTEXT.md`** | **Current project context** – name, key docs, meeting notes path, open questions path, connections. | Fill this in (or copy per project) so the agent knows which project you’re in and where to find docs. |
| **`ASURION-CURSOR-SETUP.md`** | **Product setup overview** – what’s in the repo for Product (skills, rules, templates). | Quick reference for Product skills and rules. Cursor/MCP setup lives in Asurion’s docs. |
| **`docs/`** | **Docs** – Product management rules explained, and pointers to Asurion for setup. | `docs/PRODUCT-MANAGEMENT-RULES.md` for rules; `docs/README.md` for the rest. |
| **`spec/`** | Agent Skills specification (if present). | Reference only. |
| **`Cursor Projects/`** | Optional **nested clones** of other repos (e.g. APIM) for local work. | Tracked as **gitlinks** in this repo. If `git status` shows “modified content” under those paths, run `git reset --hard HEAD` **inside** each nested repo (or discard changes there) so the parent workspace stays clean — unless you intend to commit work in the child repo and update the parent’s pointer. |
| **`project/`** | **Product project artifacts** (e.g. `project/ssot-sur`) — discovery docs, PROJECT-CONTEXT, PRD/TRD markdown. | SSOT-SUR and similar programs; not Anthropic demo skills. |

---

## Using this as the master in any project

1. **Open this repo in Cursor** (or add it as a workspace folder) when you work on Product so the agent has access to `skills/` and `.cursor/rules/`.
2. **Per project:** Copy or point `PROJECT-CONTEXT.md` to the project (or use one at repo root and change it when you switch projects).
3. **Skills** = use the Skills panel; the agent will use the right one (e.g. discover-define for Briefs/PRDs).
4. **Rules** = always on when this repo is open; no need to “turn on” anything.
5. **Templates** = reference `templates/product-brief.md`, `templates/prd.md`, `templates/open-questions.md` when creating or updating those artifacts.

---

## Quick reference

- **“Where do I add a new skill?”** → Under `skills/`. Copy `skill-template/`, rename the folder, edit `SKILL.md`.
- **“Where do I change Product behavior?”** → `.cursor/rules/`. See `docs/PRODUCT-MANAGEMENT-RULES.md` for what each rule does.
- **“Where are the Brief/PRD templates?”** → `templates/`. They’re not skills; they’re doc structures.
- **“Why do I see Skills so many times?”** → Once as the **repo/workspace name** (e.g. “SKILLS”), once as the **folder** `skills/` (the modules), and once as **skill-template** (the starter for new skills). This file is the map.
