# Kaggle Maze Crawler

![Maze Crawler competition banner](docs/assets/maze_crawler_header.png)

[![Kaggle](https://img.shields.io/badge/Kaggle-Maze%20Crawler-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/maze-crawler)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Workflow](https://img.shields.io/badge/Workflow-Notebook--first-455A64)
![Agent](https://img.shields.io/badge/Agent-Rule--based%20BFS-6A1B9A)
![Best Public Score](https://img.shields.io/badge/Best%20public%20score-~1348-2E7D32)
![Status](https://img.shields.io/badge/Status-Active%20experimentation-F9A825)

Notebook-first workspace for
[Kaggle Maze Crawler](https://www.kaggle.com/competitions/maze-crawler), a
two-player strategy game where agents must keep a factory alive in a scrolling,
fog-of-war maze while managing scouts, workers, walls, and energy.

## 1. Project Overview

The project develops rule-based Kaggle agents that survive the southern scroll,
learn useful wall structure under fog of war, and improve late-game energy
tiebreaks. The work starts from the official starter-style notebook and builds
toward stronger jump-BFS and worker wall-removal agents.

The repository is intentionally notebook-first: Kaggle notebooks generate
`main.py` and `submission.py` during execution, while docs capture the agent
logic, leaderboard observations, and experiment decisions.

## 2. Task And Goal

| Area | Summary |
| --- | --- |
| Competition task | Submit an agent that plays Maze Crawler against other bots. |
| Win condition | Keep the factory alive longer than the opponent, or win the final tiebreak on total energy and unit count. |
| Core challenge | Balance northward survival, fog exploration, route opening, and energy collection under a shrinking board. |
| Project goal | Improve from the starter baseline using transparent, reproducible algorithms rather than opaque model training. |

## 3. Key Metrics

| Submission Line | Public Score | Key Lesson |
| --- | ---: | --- |
| Starter-compatible baseline | `217.0` | Valid submission flow, weak survival. |
| Jump-BFS Version 2 | `1062.4` | Wall memory and jump-aware BFS created the first major lift. |
| Jump-BFS Version 6 | `1228.8` | Active scout replacement plus per-episode reset became the jump-BFS control. |
| Jump-BFS Version 8 | `1087.3` | Danger-gated scout builds reduced broader scout value. |
| Worker wall-removal Version 2 | peak around `1348` | Best observed strategy family: V6 core plus one conservative worker. |
| Worker wall-removal Version 4 | `1035.8` | Moving the worker target too far ahead overextended the policy. |
| Worker wall-removal Version 6 | `1105.0` | Two-row worker recovery helped but did not regain the V2 peak. |
| Miner hybrid Version 1 | `1029.6` | Gated miner idea submitted, but reviewed replays showed no miner builds yet. |
| Miner hybrid Version 2 candidate | pending | Adds remembered mining nodes to make miner builds observable. |
| Miner hybrid Version 3 candidate | pending | Second-account timing test with lower miner build gates. |
| Miner hybrid Version 4 candidate | pending | Tests safe factory collection from owned mines. |
| Miner hybrid Version 5 candidate | pending | Tests scout-assisted collection from owned mines. |
| Miner hybrid Version 6 candidate | pending | Tests faster scout return after mine collection. |
| Miner hybrid Version 7 candidate | pending | Tests broader scout mine targeting. |

Current candidate direction: keep the survival core, then make the miner policy
less dependent on a currently visible nearby node so the agent can actually
test transformed mine economy.

## 4. What We Built

| Capability | Implementation |
| --- | --- |
| Factory routing | Jump-preferred breadth-first search toward safer northern rows. |
| Map memory | Persistent wall cache with optimistic handling for undiscovered cells. |
| Symmetry use | Mirrored wall inference across the east-west symmetric board. |
| Survival fallback | Emergency jump, sidestep, and last-resort escape behavior near the scroll. |
| Scout policy | Active scout replacement for vision and crystal collection. |
| Worker policy | One conservative worker removes known north walls ahead of the factory. |
| Economy experiment | One miner only when a visible mining node is close and the factory is safe. |
| Submission safety | Notebook-generated `main.py`/`submission.py`, compile checks, and per-episode memory reset. |

## 5. Progress And Lessons

- The largest gain came from replacing greedy movement with remembered-map
  pathfinding and jump-aware survival.
- Scout value is matchup-dependent: too little scouting loses vision and
  crystals, but careless scout gating can hurt factory tempo.
- Worker wall removal is the strongest direction so far, but small routing
  changes can swing results sharply.
- Some losses are not scroll deaths; they are mine-economy losses. Strong
  opponents can transform a miner and generate thousands of factory energy.
- Replay inspection and leaderboard feedback both matter because single-seed
  notebook simulations can overfit.

## 6. Key Artifacts

| Path | Purpose |
| --- | --- |
| [`notebooks/1_maze_crawler_starter.ipynb`](notebooks/1_maze_crawler_starter.ipynb) | Starter-compatible baseline and submission plumbing. |
| [`notebooks/2_maze_crawler_jump_bfs_agent.ipynb`](notebooks/2_maze_crawler_jump_bfs_agent.ipynb) | Jump-preferred BFS reference agent. |
| [`notebooks/3_maze_crawler_worker_wall_agent.ipynb`](notebooks/3_maze_crawler_worker_wall_agent.ipynb) | Current worker wall-removal experiment. |
| [`notebooks/4_maze_crawler_miner_hybrid_agent.ipynb`](notebooks/4_maze_crawler_miner_hybrid_agent.ipynb) | Miner-hybrid experiment for mine-economy matchups. |
| [`docs/README.md`](docs/README.md) | Documentation index. |
| [`docs/01_competition_instructions.md`](docs/01_competition_instructions.md) | Competition objective, rules, and solution framing. |
| [`docs/02_eda_insights.md`](docs/02_eda_insights.md) | Visual/replay insights and environment observations. |
| [`docs/05_agent_version_log.md`](docs/05_agent_version_log.md) | Version history, scores, and experiment lessons. |
| [`docs/06_notebook_worker_wall_agent.md`](docs/06_notebook_worker_wall_agent.md) | Worker-agent algorithm notes. |
| [`docs/07_next_steps.md`](docs/07_next_steps.md) | Current action plan and submit/wait rule. |
| [`docs/08_replay_strategy.md`](docs/08_replay_strategy.md) | Replay comparison and next-agent strategy. |
| [`docs/09_notebook_miner_hybrid_agent.md`](docs/09_notebook_miner_hybrid_agent.md) | Miner-hybrid notebook notes. |

To run a submission, open the target notebook on Kaggle, run all cells, confirm
the generated-file verification passes, save a Kaggle version, and submit from
the notebook UI.
