# 5. Agent Version Log

## 1. Purpose

This log records the practical differences between notebook submissions, the
leaderboard or replay signal that motivated each change, and the lesson carried
forward into the next candidate.

## 2. Versions

| Version | Notebook | Public score | Main change | Outcome |
| --- | --- | ---: | --- | --- |
| Starter V5 | `1_maze_crawler_starter.ipynb` | 217.0 | starter-compatible factory/scout baseline | valid but weak survival |
| Jump-BFS V2 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1062.4 | wall memory, mirrored walls, jump-preferred factory BFS, active scout replacement | best leaderboard signal so far |
| Jump-BFS V4 | `2_maze_crawler_jump_bfs_agent.ipynb` | 895.3 | one lifetime scout, low return threshold, immediate positive-energy transfer | local seed improved, leaderboard regressed |
| Jump-BFS V5 candidate | `2_maze_crawler_jump_bfs_agent.ipynb` | pending | one active scout, replacement allowed, return threshold restored to 75, per-episode wall-memory reset | intended to recover V2 behavior with safer state handling |
| Jump-BFS V6 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1228.8 | active scout replacement plus per-episode wall-memory reset | best leaderboard signal so far |
| Jump-BFS V8 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1087.3 | V6 plus factory danger gate for scout builds and batch evaluation cell | danger gate underperformed V6 |
| Worker wall V2 | `3_maze_crawler_worker_wall_agent.ipynb` | peak around 1348 | V6 core plus one conservative wall-removal worker | strongest new strategy family so far |
| Worker wall V4 | `3_maze_crawler_worker_wall_agent.ipynb` | 1035.8 | moved worker target from two rows ahead to three rows ahead | underperformed Worker V2 |
| Worker wall V6 | `3_maze_crawler_worker_wall_agent.ipynb` | 1105.0 | restores two-row target and raises worker energy gate to 750 | recovered from V4 but stayed below Worker V2 |
| Worker wall V7 candidate | `3_maze_crawler_worker_wall_agent.ipynb` | pending | keeps worker priority and adds a high-reserve second-scout gate | tests whether extra crystal vision fixes energy/tiebreak losses |

## 3. Lessons

The starter notebook proved that valid submission plumbing and basic survival
worked, but public score stayed low.

Jump-BFS V2 was the first strong result. The likely winning ingredients were
factory survival pathing and enough scout activity to expand vision.

Jump-BFS V4 looked strong on the notebook seed because `agent_v2` reached
`960`, nearly matching factory-only `961`. The public score dropped, however,
which suggests the one-lifetime-scout rule and immediate transfer behavior
overfit that seed and reduced useful vision on broader matchups.

V6 confirmed that active scout replacement plus per-episode reset was the best
combination so far. V8 tested a small danger gate: factories do not build scouts
when they are within `FACTORY_DANGER_GAP` rows of `southBound`. That scored
lower, suggesting the scout's broader vision value is more important than the
small amount of factory tempo saved by skipping danger-zone builds.

Worker wall removal is a different strategy family. It should be tested in a
separate notebook once the jump-BFS line plateaus, because workers add new
costs, action conflicts, and wall-editing decisions.

The worker notebook keeps jump-BFS V6 as the base and adds only one worker. The
first worker test produced the strongest score signal in the project, while
the three-row target underperformed. Restoring the two-row target and higher
worker energy gate recovered some score, but a replay loss showed both
factories alive with our side trailing in total energy and scout count. The
next candidate keeps worker priority intact, then allows a second scout only
when the factory has a large scroll gap and at least `900` energy.

## 4. Next Evaluation

For the next agent family, compare:

- public score against V6;
- public score against Worker V2, because that is the current worker benchmark;
- whether replay losses are caused by low factory position or low energy;
- counts for `BUILD_SCOUT`, `TRANSFER_*`, `JUMP_*`, and `IDLE`;
- counts for `BUILD_WORKER` and `REMOVE_*`;
- whether the second scout appears only in safe, high-energy states;
- factory gap to `southBound` in late-game snapshots.
