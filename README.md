# Kaggle Maze Crawler

![Maze Crawler competition banner](https://kaggle.com/competitions/140389/images/header)

<p>
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-Maze%20Crawler-20BEFF?logo=kaggle&logoColor=white&style=flat-square">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=flat-square">
  <img alt="Notebook first" src="https://img.shields.io/badge/workflow-notebook--first-4B8BBE?style=flat-square">
  <img alt="Generated submission" src="https://img.shields.io/badge/submission-main.py%20%2B%20submission.py-2E7D32?style=flat-square">
</p>

Notebook-first workspace for the
[Kaggle Maze Crawler](https://www.kaggle.com/competitions/maze-crawler)
competition. The project starts from Kaggle's
[official starter notebook](https://www.kaggle.com/code/bovard/getting-started-with-maze-crawler),
adds replay-driven documentation, and separates the compact starter agent from
the stronger jump-preferred BFS experiment.

## Notebooks

| Notebook | Purpose |
| --- | --- |
| [`notebooks/1_maze_crawler_starter.ipynb`](notebooks/1_maze_crawler_starter.ipynb) | Starter-compatible notebook with setup, simulations, and generated submission files. |
| [`notebooks/2_maze_crawler_jump_bfs_agent.ipynb`](notebooks/2_maze_crawler_jump_bfs_agent.ipynb) | Experimental agent with wall memory, mirrored walls, jump-preferred factory BFS, and BFS scout routing. |

Both notebooks generate `main.py` and `submission.py` inside the Kaggle runtime.
Those files are generated artifacts and are intentionally ignored in git.

## Kaggle Workflow

1. Open the competition page and accept the rules.
2. Create or import a Kaggle notebook.
3. Upload one notebook from `notebooks/`.
4. Run all cells. The notebook writes and verifies `main.py` and
   `submission.py`.
5. Inspect the simulation replay.
6. Submit from the Kaggle notebook UI.

Use notebook 1 for a clean starter baseline. Use notebook 2 when testing the
jump-BFS agent.

## Project Notes

| Document | Contents |
| --- | --- |
| [`docs/0_coding_standards.md`](docs/0_coding_standards.md) | Notebook, documentation, and git conventions. |
| [`docs/1_instructions.md`](docs/1_instructions.md) | Competition objective, submission contract, and solution approach. |
| [`docs/2_eda_insights.md`](docs/2_eda_insights.md) | Observation schema, replay insights, and Pilkwang visual references. |
| [`docs/3_notebook_maze_crawler_kaggle_starter.md`](docs/3_notebook_maze_crawler_kaggle_starter.md) | Detailed notes for the starter notebook. |
| [`docs/4_notebook_maze_crawler_jump_bfs_agent.md`](docs/4_notebook_maze_crawler_jump_bfs_agent.md) | Algorithm notes for the jump-preferred BFS notebook. |

## Current Insight

The last Kaggle starter run showed the factory-only baseline surviving well
against random, while the first scout version lost on the same seed. That points
to a simple lesson: factory tempo matters more than early economy. The jump-BFS
notebook responds by planning factory movement first, then using the scout as a
secondary vision and crystal unit.
