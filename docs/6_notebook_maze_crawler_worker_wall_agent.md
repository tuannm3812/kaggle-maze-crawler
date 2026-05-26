# 6. Notebook: Maze Crawler Worker Wall-Removal Agent

## 1. File

Notebook: [`../notebooks/3_maze_crawler_worker_wall_agent.ipynb`](../notebooks/3_maze_crawler_worker_wall_agent.ipynb)

## 2. Purpose

This notebook starts a new agent family after the jump-BFS line plateaued. It
keeps the Version 6 factory/scout reference behavior and adds one conservative
worker to test whether wall removal can improve factory survival in blocked
routes.

## 3. Algorithm Summary

The worker agent keeps the proven jump-BFS core:

1. remembered wall cache;
2. mirrored wall inference;
3. jump-preferred factory BFS;
4. one active replacement scout.

It adds one worker experiment:

1. Build at most one worker.
2. Build the worker only when an active scout exists.
3. Build the worker only when the factory gap to `southBound` is safely above
   `WORKER_BUILD_GAP`.
4. Require strong factory energy before spending on the worker.
5. Route the worker toward cells ahead of the factory.
6. Use `REMOVE_NORTH` only when a known north wall blocks the worker and it has
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

Promote the worker line only if it beats Version 6 on leaderboard episodes or
shows a clear replay advantage on blocked-route losses.
