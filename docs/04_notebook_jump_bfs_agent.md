# 4. Notebook: Maze Crawler Jump-Preferred BFS Agent

## 1. File

Notebook: [`../notebooks/2_maze_crawler_jump_bfs_agent.ipynb`](../notebooks/2_maze_crawler_jump_bfs_agent.ipynb)

## 2. Purpose

This notebook is the first stronger agent experiment after the starter. It
keeps the same Kaggle submission contract, but changes the movement logic to
address local dead ends near the south scroll boundary.

## 3. Algorithm Summary

The agent borrows conservative ideas from a stronger public notebook without
copying the full competition solution:

1. Cache visible wall bitfields across turns.
2. Mirror observed walls across the symmetric board.
3. Use BFS to route the factory toward higher rows.
4. Explore factory jumps before normal moves when jump cooldown is ready.
5. Use emergency escape fallbacks when the factory is close to the south
   boundary.
6. Keep at most one active scout, but allow a replacement when no scout is
   alive.
7. Keep the Version 8 danger gate available as an optional experiment, but
   default it off because Version 6 scored better.
8. Return and transfer scout energy only after the scout reaches the return
   threshold.
9. Reset persistent wall memory when a new episode starts.

## 4. Kaggle Output Insight

The previous starter run on Kaggle showed:

| Agent | Opponent | Reward | Opponent Reward | Insight |
| --- | --- | ---: | ---: | --- |
| `agent_v1` | random | 928 | -393 | factory-only north tempo survived well |
| `agent_v2` | random | -410 | 107 | scout addition hurt survival on that seed |

This suggests the first refinement should protect factory tempo before adding
more economy. The jump-BFS notebook therefore treats the factory route as the
primary policy and keeps the scout as a secondary vision/crystal unit.

The latest jump-BFS run improved survival:

| Agent | Opponent | Reward | Opponent Reward | Insight |
| --- | --- | ---: | ---: | --- |
| `agent_v1` | random | 961 | -393 | factory jump-BFS survived strongly |
| `agent_v2` | random | 785 | -393 | scout survived but did not repay cost |

Replay extraction showed three scout builds and zero transfers in that run.
The one-lifetime-scout experiment then improved the local notebook seed:
`agent_v1` scored `961`, while `agent_v2` scored `960`. The public score
regressed, though, because Version 4 scored `895.3` while Version 2 scored
`1062.4`.

Version 6 became the best jump-BFS public score so far at `1228.8`. Version 8
tested the factory danger gate and dropped to `1087.3`, so the active-scout V6
behavior remains the jump-BFS reference. The separate worker wall-removal line
later produced the best overall signal, which is why worker experiments now
live in their own notebook. Detailed version history is tracked in
[`05_agent_version_log.md`](05_agent_version_log.md).

## 5. Sections

| Section | Role |
| --- | --- |
| 1. Algorithm Summary | explains the upgraded strategy |
| 2. Setup | installs/imports Kaggle Environments |
| 3. Agent Helpers | defines wall memory, robot, and coordinate helpers |
| 4. Factory Jump-Preferred BFS | implements `agent_v1` |
| 5. Agent V1 Simulation | runs factory-only replay |
| 6. Scout BFS Move | implements scout policy and `agent_v2` |
| 7. Agent V2 Simulation | runs factory-plus-BFS-scout replay |
| 8. Generate Submission Files | writes `main.py` |
| 9. Verify Generated Files | mirrors and checks `submission.py` |
| 10. Batch Evaluation | optional paired-seed local evaluation |
| 11. Submit To The Leaderboard | describes Kaggle submission |
| 12. Next Improvements | lists next policy upgrades |

## 6. Current Limitations

The notebook still does not:

- build workers to remove route-blocking walls;
- use miners or transform mines;
- analyze downloaded Kaggle episode replays automatically;
- reserve all future destinations across larger robot groups.
