# 9. Notebook: Maze Crawler Miner Hybrid Agent

## 1. File

Notebook: [`../notebooks/4_maze_crawler_miner_hybrid_agent.ipynb`](../notebooks/4_maze_crawler_miner_hybrid_agent.ipynb)

## 2. Purpose

This notebook starts a new agent family after replay analysis showed that
mine-economy opponents can reach `4000+` factory energy while our scout/worker
agents stay far lower. The goal is to test the smallest useful mining policy
without destabilizing factory survival.

## 3. Algorithm Summary

The miner-hybrid agent keeps the proven survival base:

1. remembered wall cache;
2. mirrored wall inference;
3. jump-preferred factory BFS;
4. one active replacement scout;
5. one conservative worker for route opening.

It adds a gated miner experiment:

1. Build at most one miner.
2. Build the miner only when the factory gap to `southBound` is above
   `MINER_BUILD_GAP`.
3. Require high factory energy before spending on the miner.
4. Require a visible mining node reachable within `MINER_MAX_NODE_DISTANCE`.
5. Transform immediately when the miner reaches a visible mining node.
6. Disable the V8 second-scout branch so miner ROI can be measured cleanly.

## 4. Initial Configuration

| Setting | Value | Reason |
| --- | ---: | --- |
| `MAX_ACTIVE_SCOUTS` | `1` | Avoid V8's over-broad second-scout branch. |
| `MAX_ACTIVE_WORKERS` | `1` | Preserve worker wall-removal utility. |
| `MAX_ACTIVE_MINERS` | `1` | Isolate miner value. |
| `WORKER_MIN_FACTORY_ENERGY` | `650` | Restore Worker V2-style timing. |
| `MINER_BUILD_GAP` | `12` | Avoid miner spend near scroll danger. |
| `MINER_MIN_FACTORY_ENERGY` | `850` | Preserve factory survival budget. |
| `MINER_MAX_NODE_DISTANCE` | `6` | Build only when transform target is realistic. |

## 5. Evaluation Plan

Compare against:

- Worker Version 2, the best observed worker benchmark;
- Worker Version 8, the second-scout experiment;
- Jump-BFS Version 6, the stable non-worker control.

Track:

- `BUILD_MINER`;
- `TRANSFORM`;
- first transform step;
- final factory gap;
- final total energy;
- whether miner spend causes new scroll deaths;
- whether mine-economy opponents become less lopsided.

Promote this notebook only if mining improves late energy matchups without
raising the scroll/pathing failure rate.

## 6. First Replay Result

Miner Version 1 reached a public score around `1029.6` in the first check and
showed `5W / 2L` across the seven downloaded public episodes. That early record
is not yet proof of the miner strategy because the trace contained:

- `0` `BUILD_MINER` actions;
- `0` `TRANSFORM` actions;
- `0` games with an owned mine.

The candidate behaved like a one-scout, one-worker survival agent. The miner
gate should be relaxed in the next version by remembering visible mining nodes
and allowing a miner to route toward a remembered target instead of requiring a
currently visible, close, reachable node from the spawn cell.

## 7. Version 2 Candidate

Version 2 keeps the same factory, scout, and worker logic, then changes the
miner trigger only:

| Setting | V1 | V2 |
| --- | ---: | ---: |
| `MINER_MAX_NODE_DISTANCE` | `6` | `12` |
| Mining-node memory | no | yes |
| Spawn target source | visible nodes only | visible or remembered nodes |
| Route target source | visible nodes only | visible or remembered nodes |

This is intentionally a behavior test. The first Kaggle run should confirm
that the agent actually builds miners and transforms at least once before the
leaderboard score is interpreted as evidence for or against mining.

## 8. Version 3 Candidate

Version 2 remembered nodes successfully, but replay checks still found no miner
builds. The blocker was timing: high energy and safe scroll gap rarely occurred
at the same build-ready moment.

Version 3 keeps the same remembered-node logic and changes only the miner
timing gates:

| Setting | V2 | V3 |
| --- | ---: | ---: |
| `MINER_BUILD_GAP` | `12` | `8` |
| `MINER_MIN_FACTORY_ENERGY` | `850` | `750` |
| `MINER_MAX_NODE_DISTANCE` | `12` | `12` |
| `MAX_ACTIVE_MINERS` | `1` | `1` |

Run this on the second Kaggle account first. The target is not immediate Elo;
the target is an observable replay trace with miner builds, transforms, and at
least one owned mine.

## 9. Version 4 Candidate

Version 3 proved the miner mechanics on the second account, but the agent still
often ended games with low final energy. Version 4 keeps V3 miner timing and
adds a conservative factory harvesting rule.

| Setting | V3 | V4 |
| --- | ---: | ---: |
| `MINER_BUILD_GAP` | `8` | `8` |
| `MINER_MIN_FACTORY_ENERGY` | `750` | `750` |
| `MINE_COLLECT_MIN_GAP` | unused | `10` |
| `MINE_TARGET_MAX_DISTANCE` | unused | `6` |
| `MINE_MIN_STORED_ENERGY` | unused | `100` |

Factory collection policy:

1. Keep normal build priority first.
2. If no build is selected and an owned mine is nearby, route to it only when
   the factory has a safe scroll gap.
3. If already on a safe owned mine, idle to collect.
4. Fall back to normal jump-BFS survival if no safe mine target exists.

This should be evaluated on the second account by comparing final energy,
owned-mine steps, and scroll-loss rate against Version 3.

## 10. Version 5 Candidate

Version 4 showed that factory-only mine collection is too weak. The factory
rarely reaches its own mines, so Version 5 adds scouts as mine couriers.

| Setting | V4 | V5 |
| --- | ---: | ---: |
| `MINE_COLLECT_MIN_GAP` | `10` | `8` |
| `MINE_TARGET_MAX_DISTANCE` | `6` | `8` |
| `MINE_MIN_STORED_ENERGY` | `100` | `50` |
| `SCOUT_MINE_TARGET_MAX_DISTANCE` | unused | `10` |
| `SCOUT_MINE_MIN_STORED_ENERGY` | unused | `50` |

Scout collection policy:

1. If the scout has at least `SCOUT_RETURN_ENERGY`, return to the factory as
   before.
2. Otherwise, route to a safe owned mine with stored energy before chasing
   crystals.
3. Fall back to the existing crystal and exploration policy when no safe mine
   target exists.

This candidate is intended to improve value capture on the main account's low
miner submissions while preserving the V3/V4 miner creation behavior.

## 11. Version 6 Candidate

Version 6 keeps Version 5's miner creation and scout-assisted mine targeting,
then changes only the scout return threshold.

| Setting | V5 | V6 |
| --- | ---: | ---: |
| `SCOUT_RETURN_ENERGY` | `75` | `60` |
| `SCOUT_MINE_TARGET_MAX_DISTANCE` | `10` | `10` |
| `SCOUT_MINE_MIN_STORED_ENERGY` | `50` | `50` |
| `MINER_BUILD_GAP` | `8` | `8` |
| `MINER_MIN_FACTORY_ENERGY` | `750` | `750` |

Run this on the second account first. The target is a higher `TRANSFER_*`
count and better final factory energy without lowering miner creation or
transform frequency.
