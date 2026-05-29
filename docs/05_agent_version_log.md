# 5. Agent Version Log

## 1. Purpose

This log records the practical differences between notebook submissions, the
leaderboard or replay signal that motivated each change, and the lesson carried
forward into the next candidate.

## 2. Configuration Comparison

### 2.1 Baseline And Jump-BFS Agents

| Version | Notebook | Public score | Factory pathing | Wall memory | Scout policy | Scout return | Danger gate | State reset | Outcome |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Starter V5 | `1_maze_crawler_starter.ipynb` | 217.0 | greedy north/fallback movement | none | starter-style scout support | basic | off | not needed | valid but weak survival |
| Jump-BFS V2 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1062.4 | jump-preferred BFS | visible + mirrored walls | one active scout with replacement | `75` | off | partial | first strong leaderboard lift |
| Jump-BFS V4 | `2_maze_crawler_jump_bfs_agent.ipynb` | 895.3 | jump-preferred BFS | visible + mirrored walls | one lifetime scout | low threshold; immediate positive transfer | off | partial | local seed improved, leaderboard regressed |
| Jump-BFS V5 candidate | `2_maze_crawler_jump_bfs_agent.ipynb` | pending | jump-preferred BFS | visible + mirrored walls | one active scout with replacement | `75` | off | on | recovery candidate after V4 |
| Jump-BFS V6 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1228.8 | jump-preferred BFS | visible + mirrored walls | one active scout with replacement | `75` | off | on | best jump-BFS control |
| Jump-BFS V8 | `2_maze_crawler_jump_bfs_agent.ipynb` | 1087.3 | jump-preferred BFS | visible + mirrored walls | one active scout with replacement | `75` | on at gap `<= 4` | on | danger gate reduced scout value |

### 2.2 Worker Wall-Removal Agents

All worker versions inherit the Jump-BFS V6 factory/scout core unless noted.

| Version | Notebook | Public score | Max scouts | Worker count | Worker target | Worker build gap | Worker energy gate | Second scout gate | Outcome |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- | --- |
| Worker wall V2 | `3_maze_crawler_worker_wall_agent.ipynb` | peak around 1348 | 1 | 1 | factory row `+2` | `8` | `650` | off | strongest observed strategy family |
| Worker wall V4 | `3_maze_crawler_worker_wall_agent.ipynb` | 1035.8 | 1 | 1 | factory row `+3` | `8` | `650` | off | overextended worker route |
| Worker wall V6 | `3_maze_crawler_worker_wall_agent.ipynb` | 1105.0 | 1 | 1 | factory row `+2` | `8` | `750` | off | recovered over V4 but below V2 |
| Worker wall V7 candidate | `3_maze_crawler_worker_wall_agent.ipynb` | pending | 2 | 1 | factory row `+2` | `8` | `750` | gap `> 12`, energy `>= 900` | tests energy/tiebreak losses |

### 2.3 Miner Hybrid Agents

Miner-hybrid agents are a separate family motivated by replay analysis of
opponents that transform miners into high-yield mines.

| Version | Notebook | Public score | Max scouts | Max workers | Max miners | Miner build gap | Miner energy gate | Node distance | Outcome |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Miner hybrid V1 | `4_maze_crawler_miner_hybrid_agent.ipynb` | `1029.6` | 1 | 1 | 1 | `12` | `850` | `6` | inherited worker survival worked, but miner gate never fired in reviewed replays |
| Miner hybrid V2 candidate | `4_maze_crawler_miner_hybrid_agent.ipynb` | pending | 1 | 1 | 1 | `12` | `850` | `12` | remembers mining nodes so miner builds are no longer tied to currently visible close nodes |

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

Replay comparison later showed that the biggest strategic gap is mine economy,
not extra scouting. Strong opponents build a miner, transform it, and harvest
roughly `+49` net factory energy per turn. The first miner-hybrid submission
used one strictly gated miner and disabled V8's second-scout branch, but the
downloaded public replays showed `0` `BUILD_MINER` and `0` `TRANSFORM` actions.
Its current score is therefore a survival-base signal, not evidence that the
mine policy is working yet.

Miner hybrid V2 keeps the same survival base and cost gates, but adds a
remembered mining-node cache. Visible nodes are stored until they fall behind
`southBound`, and miner spawning/routing can target remembered nodes within a
wider route window. The first evaluation criterion is not Elo; it is whether
the replay trace finally shows nonzero `BUILD_MINER`, `TRANSFORM`, and owned
mine steps.

## 4. Next Evaluation

For the next agent family, compare:

- public score against V6;
- public score against Worker V2, because that is the current worker benchmark;
- whether replay losses are caused by low factory position or low energy;
- counts for `BUILD_SCOUT`, `TRANSFER_*`, `JUMP_*`, and `IDLE`;
- counts for `BUILD_WORKER` and `REMOVE_*`;
- counts for `BUILD_MINER` and `TRANSFORM`;
- whether the second scout appears only in safe, high-energy states;
- factory gap to `southBound` in late-game snapshots.
