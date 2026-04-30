# Model Evaluation, Explainability & Insights

This project evaluates trained models for **food**, **fuel**, and **child** domains using the logic from `main.ipynb`, packaged as a runnable pipeline script.

## Project pipeline (`src`)

- Main script: `src/pipeline.py`
- Output folder: `src/result`
- Inputs:
  - `dataset/feature_engineered_data.csv`
  - `role3_model_results.csv`
  - `models/*/*.pkl`

### Required folders and files to run the pipeline

Run from the project root folder:
`Model Evaluation, Explainability & Insights`

Required structure:
- `src/pipeline.py`
- `dataset/feature_engineered_data.csv`
- `role3_model_results.csv`
- `models\food\*.pkl`
- `models\fuel\*.pkl`
- `models\child\*.pkl`

The pipeline:
1. Loads data and model-result metadata.
2. Selects `XGBoost` rows per domain (same behavior as `main.ipynb`).
3. Evaluates each domain model.
4. Saves summary files and all generated graphs to `src/result`.

# Instructions (venv + pipeline setup)

## 1) Create and activate virtual environment (no `.ps1`)

Run in **Command Prompt (cmd)**:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

## 2) Install dependencies

```bat
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Run the pipeline

```bat
python src\pipeline.py
```

## 4) Output location

All generated artifacts are saved in:

```text
src\result
```

Generated outputs include:
- `best_model_summary.csv`
- `classification_reports.txt`
- Confusion matrix graphs
- ROC graphs
- Best-model comparison graphs
- Domain-wise all-model train/test accuracy graphs
- Domain-wise all-model train/test error graphs
