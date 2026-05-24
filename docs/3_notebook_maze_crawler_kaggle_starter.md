# 3. Notebook: Maze Crawler Kaggle Starter

## 1. File

Notebook: [`../maze_crawler_kaggle_starter.ipynb`](../maze_crawler_kaggle_starter.ipynb)

## 2. Purpose

This notebook is the source of truth for the starter agent. It runs simple
simulations, renders Kaggle replays, and generates the submission artifacts.

## 3. Sections

| Section | Role |
| --- | --- |
| 1. Crawl Getting Started | explains the two baseline policies |
| 2. Optional Visual Context | displays attached Maze Crawler diagrams |
| 3. Setup | installs/imports Kaggle Environments |
| 4. Agent Helpers | defines wall, robot, and coordinate helpers |
| 5. Factory Bug Move | implements `agent_v1` |
| 6. Agent V1 Simulation | runs factory-only replay |
| 7. Scout Snail Move | implements scout policy and `agent_v2` |
| 8. Agent V2 Simulation | runs factory-plus-scout replay |
| 9. Generate Submission Files | writes `main.py` |
| 10. Verify Generated Files | mirrors and checks `submission.py` |
| 11. Submit To The Leaderboard | describes Kaggle submission |
| 12. Next Improvements | lists next policy upgrades |

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
