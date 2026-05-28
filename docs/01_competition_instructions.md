# 1. Competition Instructions And Approach

## 1. Objective

Maze Crawler is a two-player Kaggle Environments competition using the `crawl`
environment. Each submission exposes `agent(obs, config)` from `main.py` and
returns a dictionary mapping controlled robot ids to action strings.

The practical objective is survival first, economy second:

- keep the factory ahead of the southern scroll boundary;
- avoid local wall traps and factory collisions;
- collect enough energy to win tiebreaks when both factories survive;
- use support robots only when they improve factory survival or net energy.

References:

- Kaggle competition: https://www.kaggle.com/competitions/maze-crawler
- Official starter: https://www.kaggle.com/code/bovard/getting-started-with-maze-crawler
- Structure baseline inspiration: https://www.kaggle.com/code/pilkwang/maze-crawler-structure-baseline

## 2. Submission And Evaluation

Each notebook must generate:

- `main.py`: Kaggle-facing agent source.
- `submission.py`: mirrored source for helper tooling.

Both files are generated outputs and are intentionally ignored in git. The
notebook must verify that both files compile and are byte-for-byte identical.

Kaggle evaluates submitted agents through ladder episodes against similarly
rated bots. The public score is an estimated skill rating, not a direct sum of
match rewards. A single win or loss can move the score depending on opponent
rating and uncertainty.

**Key submission caution:** the competition tracks only the latest submissions
for ongoing/final consideration. Do not rapidly submit speculative agents if it
would push a stronger known agent out of the latest tracked set. Use Kaggle
episodes and local notebook diagnostics before replacing a strong version.

## 3. Game Rules We Must Respect

### 3.1 Board And Scrolling

- The maze is 20 columns wide with east-west symmetry.
- The southern boundary advances over time and destroys robots, mines,
  crystals, and factories below it.
- Scroll pressure accelerates during the match, so a safe early factory can
  still lose if it stalls later.
- The factory should usually prioritize northward progress over side quests.

**Focus:** factory row gap to `southBound` is one of the most important replay
signals. Low gap losses mean movement/pathing failed; high gap losses usually
mean energy or tiebreak economy failed.

### 3.2 Win Conditions And Tiebreaks

The match ends when one factory is destroyed, both factories collide, both are
eliminated, or the episode reaches the time limit.

If both factories survive to a tiebreak:

1. Higher total robot energy wins.
2. If energy is tied, higher unit count wins.
3. If both are tied, the result is a draw.

**Focus:** once factory survival is reliable, extra crystals and safe support
robots matter because they decide tiebreaks.

### 3.3 Robot Roles

| Robot | Role | Project priority |
| --- | --- | --- |
| Factory | Main unit; builds robots and can jump every 20 turns. | Highest priority: keep moving north and avoid traps. |
| Scout | Low-cost, fast vision/crystal collector. | Useful, but overbuilding can hurt factory tempo. |
| Worker | Removes or builds walls for 100 energy. | Strong when one worker opens blocked routes ahead of factory. |
| Miner | Can transform on mining nodes to create mines. | Deferred until scout/worker economy is stable. |

**Focus:** support robots are not automatically good. They cost factory energy,
can block spawn/movement cells, and can cause friendly collisions.

## 4. Observation And Action Contract

Important observation fields:

| Field | Meaning | Agent use |
| --- | --- | --- |
| `obs.player` | Our player id. | Filter owned robots. |
| `obs.robots` | Robot data keyed by uid. | Read type, position, energy, owner, cooldowns. |
| `obs.walls` | Flat wall bitfield array; `-1` means unknown. | Cache visible walls for pathfinding. |
| `obs.crystals` | Visible crystals only. | Scout targets and energy opportunity. |
| `obs.mines` | Remembered mines. | Future miner/economy extension. |
| `obs.miningNodes` | Visible mining nodes only. | Future miner transform targets. |
| `obs.southBound` | Current southern scroll boundary. | Factory danger and worker/scout build gates. |
| `obs.northBound` | Current northern row bound. | Pathfinding target limit. |

Wall bitfields use:

| Direction | Bit |
| --- | ---: |
| North | `1` |
| East | `2` |
| South | `4` |
| West | `8` |

Valid action families:

- movement: `NORTH`, `SOUTH`, `EAST`, `WEST`, `IDLE`;
- factory build: `BUILD_SCOUT`, `BUILD_WORKER`, `BUILD_MINER`;
- factory jump: `JUMP_NORTH`, `JUMP_SOUTH`, `JUMP_EAST`, `JUMP_WEST`;
- worker wall edit: `BUILD_*`, `REMOVE_*`;
- miner: `TRANSFORM`;
- energy transfer: `TRANSFER_*`.

**Focus:** invalid actions waste turns. The agent should prefer a conservative
valid action over speculative commands when trapped or uncertain.

## 5. Current Project Approach

The repository has four runnable notebooks:

| Notebook | Purpose |
| --- | --- |
| `1_maze_crawler_starter.ipynb` | Starter-compatible baseline and submission plumbing. |
| `2_maze_crawler_jump_bfs_agent.ipynb` | Jump-preferred BFS reference with wall memory and scout replacement. |
| `3_maze_crawler_worker_wall_agent.ipynb` | Worker wall-removal experiment built on the Jump-BFS reference. |
| `4_maze_crawler_miner_hybrid_agent.ipynb` | Miner-hybrid experiment for mine-economy matchups. |

Current algorithm priorities:

1. Keep persistent wall memory from visible cells.
2. Mirror observed walls across the symmetric board.
3. Route the factory with jump-preferred BFS toward safer northern rows.
4. Use emergency movement and jumps when the factory gap is low.
5. Maintain scout vision without starving factory tempo.
6. Add one conservative worker to remove north walls ahead of the factory.
7. Test one strictly gated miner when a visible mining node is close and safe.

## 6. Key Focus Areas

### 6.1 Factory Survival

Factory survival is the main constraint. Prioritize:

- factory gap to `southBound`;
- avoiding repeated `IDLE` near the scroll;
- avoiding jumps into dead cells or off-board positions;
- using wall memory to prevent local loops.

### 6.2 Energy Conversion

Energy matters most when both factories survive. Track:

- total energy at the final replay frame;
- scout count and scout carried energy;
- `TRANSFER_*` frequency;
- whether workers spend 100 energy on useful wall removals.

### 6.3 Worker Value

Worker wall removal is currently the strongest strategy family, but it is
sensitive. Track:

- `BUILD_WORKER` count;
- `REMOVE_*` count;
- whether the worker blocks the factory route;
- whether the worker survives long enough to justify its cost;
- whether changing target rows improves route opening or overextends.

### 6.4 Miner Value

Mining is the next major economy experiment. Track:

- `BUILD_MINER` count;
- `TRANSFORM` count;
- first transform step;
- whether the factory safely collects from the created mine;
- whether miner spending causes new scroll deaths.

### 6.5 Submission Discipline

Before submitting a new agent:

- compare against Jump-BFS Version 6 and Worker Version 2;
- inspect at least one win and one loss replay when available;
- check action counts for `BUILD_SCOUT`, `BUILD_WORKER`, `REMOVE_*`,
  `TRANSFER_*`, `JUMP_*`, and `IDLE`;
- avoid replacing a stronger latest submission with an unproven experiment.

## 7. Current Decision Note

The latest Worker Version 8 score is around `1106.0`, below Worker Version 6
at `1141.5` and below the earlier Worker Version 2 score around `1289.6`.
Because Worker Version 8 has played for several hours and is not trending above
the control, the second-scout gate does not look like the next champion yet.

Recommendation:

- wait for a few more Version 8 episodes only if Kaggle has very few replays;
- do not submit another speculative version immediately if doing so would push
  Worker Version 6 out of the latest tracked submissions;
- use the next work cycle to inspect Version 8 losses and design a smaller
  next candidate, likely around worker timing or energy transfer rather than
  adding more units.
