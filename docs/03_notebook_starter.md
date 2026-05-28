# 3. Notebook: Maze Crawler Kaggle Starter

## 1. File

Notebook: [`../notebooks/1_maze_crawler_starter.ipynb`](../notebooks/1_maze_crawler_starter.ipynb)

## 2. Purpose

This notebook is the source of truth for the starter agent. It runs simple
simulations, renders Kaggle replays, and generates the submission artifacts.

## 3. Sections

| Section | Role |
| --- | --- |
| 1. Crawl Getting Started | explains the two baseline policies |
| 2. Setup | installs/imports Kaggle Environments |
| 3. Agent Helpers | defines wall, robot, and coordinate helpers |
| 4. Factory Bug Move | implements `agent_v1` |
| 5. Agent V1 Simulation | runs factory-only replay |
| 6. Scout Snail Move | implements scout policy and `agent_v2` |
| 7. Agent V2 Simulation | runs factory-plus-scout replay |
| 8. Generate Submission Files | writes `main.py` |
| 9. Verify Generated Files | mirrors and checks `submission.py` |
| 10. Submit To The Leaderboard | describes Kaggle submission |
| 11. Next Improvements | lists next policy upgrades |

Visual context and Pilkwang's diagrams are kept in
[`02_eda_insights.md`](02_eda_insights.md), not in the submission notebook.

## 4. Generated Outputs

The notebook writes:

- `main.py`
- `submission.py`

These files are generated outputs and are ignored by git.

## 5. Validation

The notebook verification cell:

1. copies `main.py` to `submission.py`;
2. compiles both files with `py_compile`;
3. asserts both files are identical.

For local review, we also extract the `%%writefile main.py` cell and compile it
without creating tracked source files.

## 6. Current Limitations

The baseline does not yet:

- remember walls across fog;
- run BFS/A* pathing;
- build workers;
- use miners;
- evaluate paired seeds automatically.

These are intentional next steps rather than missing notebook plumbing.
