# Food Insecurity ML Pipeline - Instructions

This repository contains a 4-stage workflow to preprocess survey data, engineer features, train models, and evaluate results for:

- Food insecurity
- Fuel poverty
- Child hardship

## Project Structure

| Folder | Purpose |
| --- | --- |
| `Data Preprocessing & Data Understanding` | Clean and transform raw survey data into model-ready format |
| `Exploratory Data Analysis & Feature Engineering` | Analyze data and perform feature engineering/selection |
| `Machine Learning Model Development` | Train and compare ML models; save trained models |
| `Model Evaluation, Explainability & Insights` | Evaluate model performance and generate final insights |

## Requirements

- Python 3.10+ recommended
- Jupyter Notebook

Install dependencies from the project root:

```powershell
python -m pip install -r requirements.txt
```

## How to Run (Recommended Order)

Run the notebooks in this exact order:

1. `Data Preprocessing & Data Understanding\main.ipynb`
2. `Exploratory Data Analysis & Feature Engineering\main.ipynb`
3. `Machine Learning Model Development\main.ipynb`
4. `Model Evaluation, Explainability & Insights\main.ipynb`

Start Jupyter from the project root:

```powershell
jupyter notebook
```

Then open each notebook and run all cells from top to bottom.

## Main Outputs

- Cleaned dataset: `cleaned_dataset_role01.csv`
- Model results summary: `role3_model_results.csv`
- Trained models: `models\` folders inside stage directories

## Notes

- Keep folder names unchanged; notebooks reference local files using current structure.
- If a notebook fails due to missing input files, verify that required datasets are present in that stage's `dataset\` folder.
