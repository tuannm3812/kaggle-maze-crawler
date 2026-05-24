# Kaggle Maze Crawler Starter

Starter workspace for the Kaggle competition:

https://www.kaggle.com/competitions/maze-crawler

The local notebook follows Kaggle's starter notebook:

https://www.kaggle.com/code/bovard/getting-started-with-maze-crawler

The source artifact is:

- `maze_crawler_kaggle_starter.ipynb`: Kaggle notebook version with setup, optional visuals, simulations, and generated submission files.

Supporting docs:

- `CODING_STANDARDS.md`: project conventions for notebooks, generated artifacts, docs, and git hygiene.
- `docs/1_instructions.md`: competition objective, constraints, and current solution approach.
- `docs/2_eda_insights.md`: observation schema and replay-analysis notes.
- `docs/3_notebook_maze_crawler_kaggle_starter.md`: detailed notes for the current notebook.

## Kaggle Setup

1. Open the competition page and accept the rules.
2. Create a Kaggle notebook.
3. Add the competition data from **Add Input** if Kaggle does not attach it automatically.
4. Upload or import `maze_crawler_kaggle_starter.ipynb`.
5. Run all cells. The notebook writes both `main.py` and `submission.py`, then verifies they match.
6. Save the notebook, then use **Submit to Competition** from the Kaggle notebook UI.

This competition uses Kaggle Environments' `crawl` environment. Kaggle expects an `agent(obs, config)` function in `main.py`, and that function returns a dictionary mapping each of your robot ids to an action.

## Local Notes

The setup cell installs `kaggle-environments>=1.29.0` and imports `make`. The simulation cells create the environment with:

```python
make("crawl", configuration={"randomSeed": 42}, debug=True)
```

Run the full notebook on Kaggle after accepting the competition rules so the `crawl` environment and renderer are available.

The optional visual-context cell displays diagrams from Pilkwang's public notebook figure dataset when that dataset is attached to the Kaggle notebook. The agent and checks do not depend on those images.

`main.py` and `submission.py` are generated notebook outputs and are intentionally ignored in git.
