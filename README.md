# Kaggle Maze Crawler Starter

Starter workspace for the Kaggle competition:

https://www.kaggle.com/competitions/maze-crawler

The main artifact is `maze_crawler_kaggle_starter.ipynb`. Upload it to Kaggle or create a new Kaggle notebook and import it.

## Kaggle Setup

1. Open the competition page and accept the rules.
2. Create a Kaggle notebook.
3. Add the competition data from **Add Input** if Kaggle does not attach it automatically.
4. Upload or import `maze_crawler_kaggle_starter.ipynb`.
5. Run all cells.
6. Submit the generated `/kaggle/working/submission.py` or `/kaggle/working/submission.tar.gz`, depending on the competition submit dialog.

This competition is a 1v1 simulation/RL-style competition, so the notebook creates an agent file rather than a normal prediction CSV.

## Local Notes

The competition files require Kaggle authentication and rules acceptance, so this repo intentionally keeps the notebook self-inspecting. When it runs on Kaggle, it prints the mounted input files and tries to detect the environment name.
