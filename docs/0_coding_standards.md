# Coding Standards

## 1. Repository Scope

This repository is notebook-first. The Kaggle notebook is the executable
source of truth; generated `main.py` and `submission.py` files are notebook
outputs and should not be committed.

Keep the root small:

- `notebooks/` for runnable Kaggle workflows.
- `docs/` for coding standards, competition instructions, insights, and
  notebook notes.
- `README.md` for the high-level project overview.

Avoid adding local-only folders such as `data/`, `models/`, `outputs/`,
`configs/`, or `scripts/` unless the project moves away from Kaggle execution.

## 2. Notebook Naming

Use numbered, stable notebook names:

1. `1_maze_crawler_starter.ipynb`
2. `2_maze_crawler_jump_bfs_agent.ipynb`
3. `3_maze_crawler_worker_wall_agent.ipynb`
4. `4_maze_crawler_self_play_eval.ipynb`

Each runnable notebook should generate its own `main.py` and `submission.py`.
Do not split submission generation into a separate notebook unless Kaggle
submission flow changes.

## 3. Code Style

Follow PEP 8 for Python code:

- Use 4 spaces for indentation.
- Keep lines to 79 characters or fewer where practical.
- Prefer readable list/dict comprehensions, f-strings, and small helper
  functions when they clarify intent.
- Add type hints for reusable functions when the type is clear.
- Group imports in this order:
  1. Standard library
  2. Third-party libraries
  3. Local modules
- Separate import groups with a blank line.

Use Google-style docstrings for reusable functions:

```python
def wall_at(obs: Any, config: Any, col: int, row: int) -> int:
    """Return the known wall bitfield at a cell.

    Args:
        obs: Current Maze Crawler observation.
        config: Environment configuration.
        col: Cell column.
        row: Cell row.

    Returns:
        Wall bitfield for the requested cell.
    """
```

Add short inline comments only when they explain why a decision was made.
Avoid comments that restate what the code already says.

## 4. Notebook Style

Each notebook should include:

- a clear title cell;
- numbered Markdown sections using `1.`, `2.`, `3.`, etc.;
- a short purpose statement near the top;
- a setup section for Kaggle package/runtime requirements;
- a small configuration block near the top for tunable values such as seed and
  render size;
- Kaggle path auto-detection for optional datasets and figures;
- simulation cells that render replays when `crawl` is available;
- artifact-writing cells for generated `main.py` and `submission.py`;
- verification cells that compile generated files and assert they match.

Prefer readable, self-contained notebook code over imports from local modules.
Kaggle should be able to run the notebook after attaching only the competition
data and optional figure inputs.

When notebook code changes, clear outputs before committing unless the outputs
are intentionally part of the review. Kaggle is the trusted execution record.

Competition notebook code should be able to run inside Kaggle's runtime. If an
installation is needed for simulation, keep it explicit in the setup section.
Generated submission code should not depend on notebook-only variables.

## 5. Visualization Style

Maze Crawler visuals should help explain agent behavior:

- Use Kaggle environment replays for primary simulation evidence.
- Use optional diagram images only when the figure dataset is attached.
- Prefer compact tables for action policies, risks, and planned improvements.
- Keep chart titles short and analytical.
- Do not add decorative plots that do not support a decision.

## 6. Documentation Style

Documentation should be written for a teammate reviewing the competition plan:

- Use numbered sections.
- Lead with objectives, constraints, and implications.
- Include exact commands, notebook cells, and file paths where useful.
- Link notebooks and docs with relative paths.
- Keep broad narrative in `README.md`.
- Keep detailed evidence in focused docs.

Required docs:

- `docs/1_instructions.md`: competition objective, constraints, and our
  approach.
- `docs/2_eda_insights.md`: observation schema, replay insights, and planned
  analysis.
- one notebook note per runnable notebook.

## 7. Git Hygiene

Do not commit:

- raw Kaggle competition data;
- generated `main.py` or `submission.py`;
- Kaggle working directories;
- local replay dumps unless they are curated docs evidence;
- Python caches or notebook checkpoints;
- ad hoc experiment outputs.

Commit lightweight artifacts only when they directly support written analysis,
such as curated docs, small diagrams, or notebook summaries.
