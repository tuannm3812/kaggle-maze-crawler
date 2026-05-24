# 5. Agent Version Log

## 1. Purpose

This log records the practical differences between notebook submissions and
the replay or leaderboard signal that motivated each change.

## 2. Versions

| Version | Notebook | Public score | Main change | Outcome |
| --- | --- | ---: | --- | --- |
| Starter V5 | `1_maze_crawler_starter.ipynb` | 217.0 | starter-compatible factory/scout baseline | valid but weak survival |
| Jump-BFS V2 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1062.4 | wall memory, mirrored walls, jump-preferred factory BFS, active scout replacement | best leaderboard signal so far |
| Jump-BFS V4 | `2_maze_crawler_jump_bfs_agent.ipynb` | 895.3 | one lifetime scout, low return threshold, immediate positive-energy transfer | local seed improved, leaderboard regressed |
| Jump-BFS V5 candidate | `2_maze_crawler_jump_bfs_agent.ipynb` | pending | one active scout, replacement allowed, return threshold restored to 75, per-episode wall-memory reset | intended to recover V2 behavior with safer state handling |

## 3. Lessons

The starter notebook proved that valid submission plumbing and basic survival
worked, but public score stayed low.

Jump-BFS V2 was the first strong result. The likely winning ingredients were
factory survival pathing and enough scout activity to expand vision.

Jump-BFS V4 looked strong on the notebook seed because `agent_v2` reached
`960`, nearly matching factory-only `961`. The public score dropped, however,
which suggests the one-lifetime-scout rule and immediate transfer behavior
overfit that seed and reduced useful vision on broader matchups.

The current candidate keeps V2's active-scout replacement behavior while
retaining the safer episode reset guard. It deliberately avoids transferring
spawn energy at step 2; scouts only return once they carry at least
`SCOUT_RETURN_ENERGY`.

## 4. Next Evaluation

After running the current notebook on Kaggle, compare:

- public score against V2 and V4;
- whether replay losses are caused by low factory position or low energy;
- counts for `BUILD_SCOUT`, `TRANSFER_*`, `JUMP_*`, and `IDLE`;
- factory gap to `southBound` in late-game snapshots.
