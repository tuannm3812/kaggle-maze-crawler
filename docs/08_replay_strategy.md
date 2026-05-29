# 8. Replay Strategy

## 1. Replay Scope

Using Kaggle replay downloads, we compared five important submission families:

| Agent Line | Submission Ref | Replays Reviewed | Public Score Signal |
| --- | ---: | ---: | ---: |
| Worker wall Version 2 | `53049656` | `72` | `1289.6`, peak around `1348` |
| Worker wall Version 6 | `53086334` | `48` | `1141.5` |
| Worker wall Version 8 | `53106716` | `55` | `1096.6` |
| Jump-BFS Version 6 | `52989413` | `49` | `1222.1` |
| Miner hybrid Version 1 | `53131425` | `7` | `1029.6` |

The local replay files are ignored by git and organized as:

- `replays/submissions/<agent_version>/episodes.json`;
- `replays/submissions/<agent_version>/<episode_id>.json`;
- `replays/analysis/*.json` for derived comparison summaries.

## 2. Aggregate Replay Findings

| Agent Line | Results In Sample | Main Loss Modes | Notes |
| --- | --- | --- | --- |
| Worker V2 | `42W / 28L / 2D` | scroll/factory loss, then energy tiebreak | Best worker line; lower worker energy gate appears better than later variants. |
| Worker V6 | `28W / 19L / 1D` | scroll/factory loss, then simultaneous-factory tiebreak | Higher worker energy gate recovered from V4 but did not beat V2. |
| Worker V8 | `32W / 18L / 5D` | simultaneous-factory tiebreak, then scroll/factory loss | Second-scout gate did not clearly improve the worker family. |
| Jump-BFS V6 | `31W / 14L / 4D` | scroll/factory loss and energy tiebreak | Strong non-worker control; no worker cost, but no wall-removal upside. |
| Miner V1 | `5W / 2L / 0D` | early sample only | Did not build or transform a miner in reviewed games, so this is mostly the inherited worker/scout base. |

Against opponents that established mines, every line became more fragile:

| Agent Line | Opponent Mine Games | Results | Signal |
| --- | ---: | --- | --- |
| Worker V2 | `18` | `9W / 9L` | Strongest worker line still splits mine matchups. |
| Worker V6 | `16` | `10W / 6L` | Survives some mine games but loses hard when mine economy stabilizes. |
| Worker V8 | `15` | `8W / 7L` | Extra scout does not solve mine-economy losses. |
| Jump-BFS V6 | `9` | `3W / 6L` | No-worker line is especially vulnerable to established mines. |

## 3. Key Opponent Advantage

The harmo-miu losses revealed the clearest strategic gap. Harmo-miu built a
miner, transformed it on a mining node, and positioned the factory to harvest
mine energy. Once the mine was active, its factory gained roughly `+49` net
energy per turn.

Observed examples:

| Episode | Seed | Opponent | Opponent Transform Step | Final Energy Gap |
| --- | ---: | --- | ---: | --- |
| `77988433` | `746634771` | harmo-miu | around `163` | opponent `4251`, us `47` |
| `77986565` | `290904391` | harmo-miu | around `188` | opponent `4304`, us `439` |

This is not just better crystal collection. It is a different economy plan.
Our scout/worker spending cannot match a stable mine once the opponent safely
parks near it.

## 4. Our Current Weaknesses

1. We do not create mines, so late-game tiebreaks against mine agents are
   structurally difficult.
2. Worker spending often produces only one or two `REMOVE_*` actions before the
   worker runs out of energy.
3. V8 adds scout capacity, but the replay sample does not show enough energy
   conversion to justify the added complexity.
4. Several losses still end with factory gap near `0`, so any economy upgrade
   must stay gated by scroll safety.

## 5. Next-Agent Strategy

The next serious agent should be a separate miner-hybrid experiment, not
another broad scout variant.

Implemented notebook:

- [`../notebooks/4_maze_crawler_miner_hybrid_agent.ipynb`](../notebooks/4_maze_crawler_miner_hybrid_agent.ipynb)

Core strategy:

1. Keep Jump-BFS V6 factory movement as the survival base.
2. Keep worker logic conservative; start from Worker V2-style timing rather
   than V8 second-scout behavior.
3. Add a single miner only when a visible mining node is close and factory gap
   is safe.
4. Transform immediately when the miner reaches a node.
5. Let the factory collect mine energy only when doing so does not put the
   factory near scroll danger.
6. Disable second-scout experiments in the miner notebook until miner ROI is
   measured.

Initial gates to test:

| Gate | Starting Value | Reason |
| --- | ---: | --- |
| `MAX_ACTIVE_MINERS` | `1` | Isolate miner value. |
| `MINER_BUILD_GAP` | `12` | Avoid miner spend during scroll danger. |
| `MINER_MIN_FACTORY_ENERGY` | `850` | Preserve factory survival budget. |
| `MINER_MAX_NODE_DISTANCE` | `6` | Build only when transform target is realistic. |
| `MINE_COLLECT_MIN_GAP` | `8` | Do not camp a mine if scroll pressure is high. |

## 6. Evaluation Plan

Compare the miner-hybrid notebook against:

1. Worker V2, because it is the best observed worker benchmark.
2. Jump-BFS V6, because it is the stable non-worker control.
3. Worker V8, because it tested extra scout economy and underperformed.

Track these metrics:

- `BUILD_MINER` count;
- `TRANSFORM` count;
- first transform step;
- mine-owned steps;
- factory energy after transform;
- final factory gap;
- final total energy;
- whether mining caused new scroll deaths.

Promote the miner line only if it either beats Worker V2 in public score or
clearly wins mine-economy matchups without increasing scroll/pathing losses.

## 7. Miner V1 Replay Check

Miner Version 1 has too few public episodes for a stable rating conclusion, but
the action trace already found a clear implementation lesson.

| Signal | Value |
| --- | ---: |
| Public score at check time | `1029.6` |
| Downloaded public replays | `7` |
| Replay results | `5W / 2L / 0D` |
| Average game length | `337.7` steps |
| Average final own energy | `239.3` |
| `BUILD_MINER` actions | `0` |
| `TRANSFORM` actions | `0` |
| Own mine games | `0` |

The miner gate is currently too strict or too dependent on visible nearby
nodes. It requires a visible mining node reachable from the factory spawn cell
within `MINER_MAX_NODE_DISTANCE = 6` at a moment when build cooldown, spawn
cell, energy, and scroll-gap checks are all valid. In the reviewed public
episodes that conjunction never happened.

Miner Version 2 implements the next miner experiment:

1. Keep the worker/scout survival base unchanged.
2. Loosen miner discovery from "visible close node before build" to "build a
   miner after scout coverage has exposed any promising node in the same lane."
3. Add a remembered mining-node cache, because mining nodes are only visible
   while in range.
4. Route the miner to the remembered node with a larger but scroll-aware BFS
   depth.
5. Track `BUILD_MINER`, `TRANSFORM`, and first transform step before judging
   leaderboard score.

Notebook change:

- `MINER_MAX_NODE_DISTANCE` increased from `6` to `12`;
- `_mining_node_memory` stores visible mining nodes until they scroll away;
- miner build and route selection use remembered nodes, not only the current
  observation.

Miner Version 2 still failed the behavior test in the reviewed replays:
`BUILD_MINER = 0`, `TRANSFORM = 0`, and `owned mine steps = 0`. A replay-gate
counterfactual showed the missing overlap was timing, not node discovery:

| Candidate Gate | Possible Base Build Windows In 5 V2 Replays |
| --- | ---: |
| `gap > 8`, `energy >= 750` | `13` |
| `gap > 6`, `energy >= 750` | `37` |
| `gap > 8`, `energy >= 700` | `61` |

Miner Version 3 uses the conservative first option: `MINER_BUILD_GAP = 8` and
`MINER_MIN_FACTORY_ENERGY = 750`. It should be run on the second account first,
because the goal is to verify miner behavior without replacing the main
account's known stronger submissions.

Miner Version 3 did verify miner behavior on the second account:

| Signal | Value |
| --- | ---: |
| Replays reviewed | `36` |
| Result sample | `19W / 13L / 4D` |
| `BUILD_MINER` actions | `28` |
| `TRANSFORM` actions | `22` |
| Owned mine games | `21` |
| Average first mine step | `52.5` |

That shifted the bottleneck from "can we create mines?" to "can we harvest
them?" Miner Version 4 keeps the V3 miner gates and adds a safe factory
collection rule:

- target only owned mines;
- require factory scroll gap above `MINE_COLLECT_MIN_GAP = 10`;
- target mines within `MINE_TARGET_MAX_DISTANCE = 6`;
- route only to mines with at least `100` stored energy unless already on the
  mine.
