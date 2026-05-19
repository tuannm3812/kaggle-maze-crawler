# Kaggle Maze Crawler Starter

Starter workspace for the Kaggle competition:

https://www.kaggle.com/competitions/maze-crawler

The local notebook follows Kaggle's starter notebook:

https://www.kaggle.com/code/bovard/getting-started-with-maze-crawler

The main artifacts are:

- `maze_crawler_kaggle_starter.ipynb`: Kaggle notebook version with setup, smoke tests, and a `main.py` write cell.
- `main.py`: the same starter-style submission agent for local inspection/version control.

## Kaggle Setup

1. Open the competition page and accept the rules.
2. Create a Kaggle notebook.
3. Add the competition data from **Add Input** if Kaggle does not attach it automatically.
4. Upload or import `maze_crawler_kaggle_starter.ipynb`.
5. Run all cells.
6. Save the notebook, then use **Submit to Competition** from the Kaggle notebook UI.

This competition uses Kaggle Environments' `crawl` environment. Kaggle expects an `agent(obs, config)` function in `main.py`, and that function returns a dictionary mapping each of your robot ids to an action.

## Local Notes

The starter installs `kaggle-environments>=1.29.0` and creates the environment with:

```python
make("crawl", configuration={"randomSeed": 42}, debug=True)
```

If `crawl` is not available locally, run the notebook on Kaggle after accepting the competition rules.
