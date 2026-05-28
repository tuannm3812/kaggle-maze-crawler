# 6. Notebook: Maze Crawler Worker Wall-Removal Agent

## 1. File

Notebook: [`../notebooks/3_maze_crawler_worker_wall_agent.ipynb`](../notebooks/3_maze_crawler_worker_wall_agent.ipynb)

## 2. Purpose

This notebook is the strongest active experiment family after the jump-BFS
line plateaued. It keeps the Version 6 factory/scout reference behavior and
adds one conservative worker to test whether wall removal can improve factory
survival in blocked routes.

## 3. Algorithm Summary

The worker agent keeps the proven jump-BFS core:

1. remembered wall cache;
2. mirrored wall inference;
3. jump-preferred factory BFS;
4. one active replacement scout, plus one optional high-reserve second scout.

It adds one worker experiment:

1. Build the first scout before worker logic.
2. Build at most one worker.
3. Build the worker only when an active scout exists.
4. Build the worker only when the factory gap to `southBound` is safely above
   `WORKER_BUILD_GAP`.
5. Require strong factory energy before spending on the worker.
6. Route the worker toward cells two rows ahead of the factory.
7. Add a second scout only after worker priority, with `factory_gap > 12` and
   factory energy at least `900`.
8. Use `REMOVE_NORTH` only when a known north wall blocks the worker and it has
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
`1105.0`. A later loss showed both factories alive but our side behind on total
energy and scout count, so the current candidate adds one high-reserve second
scout to improve crystal vision without delaying the worker.

Promote the worker line only if it beats both the jump-BFS Version 6 control
and the Worker Version 2 benchmark on leaderboard episodes, or if replays show
a clear blocked-route survival advantage that has not yet converged in Elo.
