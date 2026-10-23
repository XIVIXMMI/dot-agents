# agents

A template repo of Claude Code rules, skills and agents, split into reusable parts. Use it as a starting point, then edit.

| Folder | What | Changes when |
|---|---|---|
| `core/` | Rules, skills, docs templates for any project | rarely |
| `stacks/<name>/` | Language / platform specifics (`swift`) | the tech stack changes |
| `workflows/<name>/` | How the agents build (`tdd-pipeline`) | the way of building changes |
| `presets/` | Sample recipe (`example/`): components list, `CLAUDE.md` skeleton, `settings.json` | per project |

Each component mirrors a project's `.claude/` (`agents/ rules/ skills/ specs/ reports/ docs/`). Component `README.md` files are not installed.

Note: skills and agents still mention "Micro-journal" and its decision IDs (D-NNN) from the project they came from. Replace them when you adapt the template.

## Use

```bash
./install.sh example /path/to/project          # skips files that already exist
./install.sh example /path/to/project --force  # overwrite
```

## Add a new way of working

1. Create `workflows/<name>/` with the folders it needs.
2. Copy `presets/example/` to `presets/<project>/` and list `core`, a stack and the new workflow in `components`.
3. Fill in `CLAUDE.md` and `settings.json`.

Vendored third-party skills: see `THIRD-PARTY-NOTICES.md`.
