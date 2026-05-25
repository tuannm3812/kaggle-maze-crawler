# Kaggle Maze Crawler

![Maze Crawler competition banner](docs/assets/maze_crawler_header.png)

<p>
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-Maze%20Crawler-20BEFF?logo=kaggle&logoColor=white&style=flat-square">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=flat-square">
  <img alt="Notebook first" src="https://img.shields.io/badge/workflow-notebook--first-4B8BBE?style=flat-square">
  <img alt="Best public score" src="https://img.shields.io/badge/best%20public-1171.5-2E7D32?style=flat-square">
</p>

Notebook-first workspace for the
[Kaggle Maze Crawler](https://www.kaggle.com/competitions/maze-crawler)
competition. The project keeps the official starter baseline separate from the
current jump-preferred BFS agent line, so each submission version has a clear
algorithm story and replay trail.

## 1. Project Overview

Maze Crawler is a two-player Kaggle Environments game where each agent controls
a factory and optional robots inside a scrolling maze. The practical goal is to
keep the factory alive while using scouts, crystals, and map knowledge to
outlast the opponent.

This repository is built around a notebook-first competition workflow:

- reproduce the official starter submission;
- inspect rendered Kaggle simulations;
- iterate on compact, submission-safe agents;
- document every meaningful policy change and leaderboard result;
- generate `main.py` and `submission.py` directly inside Kaggle notebooks.

## 2. Key Highlights

| Highlight | Current Status |
| --- | --- |
| Best public score | `1171.5` with the jump-preferred BFS line |
| Starter score | `217.0` from the starter-compatible notebook |
| Main agent | wall memory, mirrored walls, jump-preferred factory BFS |
| Scout policy | one active replacement scout for vision and crystals |
| Current candidate | factory danger gate to skip scout builds near `southBound` |
| Submission outputs | each notebook writes and verifies `main.py` and `submission.py` |

## 3. What We Built

| Area | Work Completed |
| --- | --- |
| Starter baseline | reproduced Kaggle starter flow with setup, simulation, generated files, and verification |
| Replay analysis | extracted rewards, steps, action counts, scout builds, transfers, jumps, idles, and factory gap |
| Pathfinding | added BFS over known passable edges and jump-preferred factory search |
| Map memory | cached visible walls across turns and mirrored symmetric wall information |
| Survival logic | added emergency factory fallbacks and danger gating near `southBound` |
| Scout economy | tested greedy scout, BFS scout, one-lifetime scout, and one-active replacement scout |
| Submission hygiene | notebooks write `main.py` and `submission.py`, then compile and compare them |
| Documentation | added coding standards, EDA notes, notebook notes, and an agent version log |

## 4. Algorithms And Skills

Core algorithms and techniques:

- **Jump-preferred BFS:** searches factory jumps before normal moves when jump
  cooldown is ready.
- **Known-wall BFS:** routes scouts and factories through remembered open
  edges.
- **Optimistic fog handling:** treats unknown cells as passable while caching
  confirmed wall bitfields.
- **Mirror inference:** mirrors observed wall bits across the symmetric board
  to increase map coverage.
- **Danger gating:** blocks scout builds when factory survival is at risk near
  the scrolling boundary.
- **Replay-driven evaluation:** compares notebook replays, action counts, and
  leaderboard outcomes instead of trusting a single local seed.

Skillsets demonstrated:

- Kaggle notebook engineering and submission packaging;
- Python agent design under turn-based game constraints;
- graph search/pathfinding;
- simulation debugging and replay interpretation;
- experiment tracking and version documentation;
- lightweight technical writing for reproducible competition work.

## 5. Current Insight

The latest notebook run shows why we evaluate with both replays and public
episodes. On the main seed, `agent_v2` beat factory-only (`1029` vs `961`) and
successfully transferred scout energy. In the 5-seed batch, `agent_v2` still
had one poor seed, so the leaderboard episodes are the better signal before we
lock in another policy change.

## 6. Notebooks

| Notebook | Purpose |
| --- | --- |
| [`notebooks/1_maze_crawler_starter.ipynb`](notebooks/1_maze_crawler_starter.ipynb) | Starter-compatible notebook with setup, simulations, and generated submission files. |
| [`notebooks/2_maze_crawler_jump_bfs_agent.ipynb`](notebooks/2_maze_crawler_jump_bfs_agent.ipynb) | Main experimental agent with jump-preferred BFS, active scout replacement, danger gating, and batch evaluation. |

Generated `main.py` and `submission.py` are Kaggle runtime artifacts and are
intentionally ignored in git.

## 7. Kaggle Workflow

1. Open the competition page and accept the rules.
2. Create or import a Kaggle notebook.
3. Upload or sync one notebook from `notebooks/`.
4. Run all cells.
5. Inspect the rendered replay and optional batch evaluation.
6. Save a Kaggle version and submit from the Kaggle notebook UI.

Use notebook 1 for the control baseline. Use notebook 2 for the current
submission candidate.

## 8. Project Notes

| Document | Contents |
| --- | --- |
| [`docs/0_coding_standards.md`](docs/0_coding_standards.md) | Notebook, documentation, and git conventions. |
| [`docs/1_instructions.md`](docs/1_instructions.md) | Competition objective, submission contract, and solution approach. |
| [`docs/2_eda_insights.md`](docs/2_eda_insights.md) | Observation schema, replay insights, and visual references. |
| [`docs/3_notebook_maze_crawler_kaggle_starter.md`](docs/3_notebook_maze_crawler_kaggle_starter.md) | Detailed notes for the starter notebook. |
| [`docs/4_notebook_maze_crawler_jump_bfs_agent.md`](docs/4_notebook_maze_crawler_jump_bfs_agent.md) | Algorithm notes for the jump-preferred BFS notebook. |
| [`docs/5_agent_version_log.md`](docs/5_agent_version_log.md) | Submission version history, scores, and lessons. |

## 9. Next Experiments

Wait for enough leaderboard episodes on the current danger-gated candidate
before changing the core policy again. If it underperforms Version 6, roll back
the danger gate and keep active scout replacement. If it improves, the next
separate strategy family to test is worker wall removal for blocked factory
routes.
