# 6. Notebook: Maze Crawler Worker Wall-Removal Agent

## 1. File

Notebook: [`../notebooks/3_maze_crawler_worker_wall_agent.ipynb`](../notebooks/3_maze_crawler_worker_wall_agent.ipynb)

## 2. Purpose

This notebook is the strongest active experiment family after the jump-BFS and
miner lines plateaued below the Worker Version 2 benchmark. It keeps the
Version 6 factory/scout reference behavior and adds one conservative worker to
test whether wall removal can improve factory survival in blocked routes.

## 3. Algorithm Summary

The worker agent keeps the proven jump-BFS core:

1. remembered wall cache;
2. mirrored wall inference;
3. jump-preferred factory BFS;
4. one active replacement scout.

It adds one worker experiment:

1. Build the first scout before worker logic.
2. Build at most one worker.
3. Build the worker only when an active scout exists.
4. Build the worker only when the factory gap to `southBound` is safely above
   `WORKER_BUILD_GAP`.
5. Require Worker Version 2-style factory energy before spending on the
   worker.
6. Route the worker toward cells two rows ahead of the factory.
7. Use `REMOVE_NORTH` only when a known north wall blocks the worker and it has
   enough energy.

## 4. Why Separate

Workers change the action economy: they cost more than scouts, move more
slowly, can block factory routes, and spend energy on wall edits. Keeping this
as a separate notebook makes the experiment easier to evaluate against the
Version 6 reference.

## 5. Evaluation Plan

Compare the worker notebook against Version 6 on:

- public score;
- factory survival step;
- `BUILD_WORKER` count;
- `REMOVE_*` count;
- whether worker placement blocks factory movement;
- factory gap to `southBound` near losses.

The first worker submission produced the strongest project signal so far,
peaking around `1348` before settling lower. The three-row-ahead worker target
underperformed at `1035.8`, and the two-row/high-reserve recovery reached
`1105.0`. The miner line later created mines reliably but did not beat the
worker or jump-BFS baselines. The current Worker V9 candidate therefore returns
to Worker Version 2-style controls and changes only scout return timing.

## 6. Worker V9 Candidate

Worker V9 is a one-variable energy-conversion test:

| Setting | Worker V2 | Worker V9 |
| --- | ---: | ---: |
| `MAX_ACTIVE_SCOUTS` | `1` | `1` |
| `MAX_ACTIVE_WORKERS` | `1` | `1` |
| `WORKER_BUILD_GAP` | `8` | `8` |
| `WORKER_FRONT_OFFSET` | `2` | `2` |
| `WORKER_MIN_FACTORY_ENERGY` | `650` | `650` |
| `SCOUT_RETURN_ENERGY` | `75` | `60` |

Run this on the second account first. The target is higher `TRANSFER_*` count
and final factory energy without reducing worker utility or scout exploration
too much.

Promote the worker line only if it beats both the jump-BFS Version 6 control
and the Worker Version 2 benchmark on leaderboard episodes, or if replays show
a clear blocked-route survival advantage that has not yet converged in Elo.
