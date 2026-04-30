# Machine Learning Model Development Pipeline

This project now includes a script-based pipeline in `src\pipeline.py` that reproduces the model training workflow from `main.ipynb` for:

- food insecurity
- fuel poverty
- child hardship

All generated outputs are written to `src\results\`.

## Project Structure

```text
dataset/
main.ipynb
src/
  pipeline.py
  results/
```

## Required Folders and Files to Run Pipeline

Run from the project root (`Machine Learning Model Development`) and make sure these paths exist:

```text
requirements.txt
dataset/
  feature_engineered_data.csv
  food_features.json
  fuel_features.json
  child_features.json
src/
  pipeline.py
```

## Setup (venv)

Set up manually from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python .\src\pipeline.py
```

## What the Pipeline Does

1. Loads feature-engineered data and domain feature JSON files from `dataset\`.
2. Builds preprocessing with imputation, scaling, and one-hot encoding.
3. Applies SMOTE on training data.
4. Trains and tunes SVM, RandomForest, DecisionTree, and XGBoost using GridSearchCV.
5. Saves trained models and evaluation outputs.
6. Generates result graphs.

## Outputs

Everything is saved in `src\results\`:

- `model_results.csv`
- `best_models_summary.csv`
- `test_accuracy_by_domain_model.png`
- `best_model_per_domain.png`
- `test_accuracy_heatmap.png`
- `models\food\*.pkl`
- `models\fuel\*.pkl`
- `models\child\*.pkl`
