# 1. Competition Instructions And Approach

## 1. Objective

Maze Crawler is a Kaggle Environments competition using the `crawl`
environment. A submission exposes `agent(obs, config)` from `main.py`; the
agent returns a dictionary mapping each controlled robot id to an action.

The practical objective is to keep the factory alive while building enough
economy to outscore the opponent. The factory must continue moving north as the
maze scrolls upward from the south. Energy, crystals, workers, miners, and
transfers matter only if the factory survives long enough to use them.

References:

- Kaggle competition: https://www.kaggle.com/competitions/maze-crawler
- Official starter: https://www.kaggle.com/code/bovard/getting-started-with-maze-crawler
- Structure baseline inspiration: https://www.kaggle.com/code/pilkwang/maze-crawler-structure-baseline

## 2. Submission Contract

The notebook must generate:

- `main.py`: Kaggle-facing agent source.
- `submission.py`: mirrored source for tooling that expects that filename.

Both files are generated outputs and are intentionally ignored in git. The
notebook verifies that both files compile and are byte-for-byte identical.

## 3. Game Constraints We Handle First

Factory survival comes before economy:

1. Move north when the path is open.
2. Use `JUMP_NORTH` when north is blocked and the jump cooldown is ready.
3. Sidestep east or west only when north is blocked and jump is unavailable.
4. Return `IDLE` rather than emitting an invalid action when trapped.

Scout economy is deliberately conservative:

1. Build at most one scout.
2. Send the scout toward visible crystals.
3. Return to the factory once carried energy is high enough.
4. Transfer energy only when adjacent and the edge is open.

## 4. Current Solution

The current notebook implements two policies:

- `agent_v1`: factory-only bug move for survival sanity checks.
- `agent_v2`: factory bug move plus one scout with short tabu memory.

The final generated `agent` delegates to `agent_v2`.

## 5. Why This Baseline

This baseline is intentionally small because it is the control surface for
later work. It gives us:

- valid Kaggle submission artifacts;
- replayable simulations against a random opponent;
- helper functions for wall bitfields and robot filtering;
- a simple scout policy that can be replaced with stronger pathing later.

## 6. Planned Improvements

The next meaningful upgrades are:

1. Add a worker that removes route-blocking walls ahead of the factory.
2. Cache remembered walls from fogged observations.
3. Replace greedy scout movement with BFS over known passable edges.
4. Add miner logic only after carrier return paths are reliable.
5. Evaluate policy changes on paired random seeds and inspect replays.
