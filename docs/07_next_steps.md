# 7. Next Steps

## 1. Current Recommendation

Do not rush another speculative scout/worker submission while Worker Version 8
is below the known worker controls. The latest visible scores show:

| Agent | Score Signal | Interpretation |
| --- | ---: | --- |
| Worker wall Version 2 | around `1289.6`, peak around `1348` | strongest worker benchmark |
| Jump-BFS Version 6 | around `1222.1` to `1228.8` | stable non-worker control |
| Worker wall Version 6 | around `1141.5` | better than V4/V8, below V2 |
| Worker wall Version 8 | around `1104.8` | second-scout gate has not beaten controls |
| Miner hybrid Version 1 | around `1029.6` | score came without any miner build in reviewed replays |
| Miner hybrid Version 2 candidate | pending | remembers visible mining nodes and widens miner routing |

Version 8 can keep running for a few more episodes if replay count is small,
but it should not be treated as the next champion unless it climbs above
Worker Version 6 and begins approaching Worker Version 2.

Replay comparison still points to mine economy as the strategic gap, but Miner
Version 1 did not actually exercise that plan. See
[`08_replay_strategy.md`](08_replay_strategy.md) for the detailed replay
summary and next-agent design.

## 2. Immediate Analysis Tasks

1. Download or inspect at least two Worker Version 8 losses.
2. Classify each loss as one of:
   - scroll/pathing failure;
   - energy/tiebreak failure;
   - worker blocking or wasted wall removal;
   - scout overinvestment or collision.
3. Record final factory gap, total energy, unit count, `BUILD_SCOUT`,
   `BUILD_WORKER`, `REMOVE_*`, `TRANSFER_*`, `JUMP_*`, and `IDLE` counts.
4. Compare the same signals against Worker Version 6 and Worker Version 2
   replays when available.

## 3. Candidate Agent Ideas

Prefer one-variable changes so leaderboard movement is interpretable.

| Candidate | Change | Why It Might Help | Risk |
| --- | --- | --- | --- |
| Miner hybrid V1 | Add one gated miner/mine path on top of the V6/Worker V2 survival base. | Mine opponents are creating 4,000+ energy late games that scout/worker policies cannot match. | Miner spend can create new scroll deaths if gated poorly. |
| Miner hybrid V2 | Remember mining nodes and loosen the pre-build reachability gate. | V1 never issued `BUILD_MINER`; node visibility is too narrow for the current gate. | A miner built too early may starve the factory. |
| Worker timing V9 | Keep one scout; tune `WORKER_MIN_FACTORY_ENERGY` between `650` and `750`. | Version 2 beat later variants, so timing may matter more than extra units. | Too low can starve factory energy. |
| Transfer V9 | Improve scout return/transfer targeting without adding more scouts. | Converts existing scout value into tiebreak energy. | Return behavior may reduce exploration. |
| Worker action V9 | Remove north walls only when the target row is near factory path. | Reduces wasted `REMOVE_*` cost. | More logic may miss useful openings. |

## 4. Submit/Wait Rule

Submit a new version only when at least one of these is true:

- Version 8 has enough episodes and remains clearly below Worker Version 6;
- replay analysis identifies a specific failure that a one-variable change can
  target;
- the new candidate preserves the best known latest submission coverage on
  Kaggle.

If the latest tracked submissions would both become speculative variants, wait.
Keep a strong known worker submission active while testing new ideas.

Miner V2 should be judged first on behavior, then on Elo:

1. `BUILD_MINER > 0`;
2. `TRANSFORM > 0`;
3. at least one owned-mine step;
4. no obvious rise in scroll/factory deaths;
5. only then compare public score against Worker V2 and Jump-BFS V6.

## 5. Documentation Updates After Each Run

After every Kaggle submission:

1. Update [`05_agent_version_log.md`](05_agent_version_log.md) with score,
   configuration, and outcome.
2. Update [`06_notebook_worker_wall_agent.md`](06_notebook_worker_wall_agent.md)
   if the worker policy changes.
3. Update [`09_notebook_miner_hybrid_agent.md`](09_notebook_miner_hybrid_agent.md)
   if the miner policy changes.
4. Add replay observations to [`02_eda_insights.md`](02_eda_insights.md) when
   a new failure mode appears.
5. Keep notebook outputs cleared before committing code changes.
