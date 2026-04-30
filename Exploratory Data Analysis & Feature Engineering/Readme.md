# Exploratory Data Analysis & Feature Engineering Pipeline

This repository now includes a reproducible pipeline in `src\pipeline.py` based on `main.ipynb`.

## Required files and folders

To run the pipeline, keep this structure:

- `src\pipeline.py` (pipeline script)
- `requirements.txt` (Python dependencies)
- `cleaned_dataset_role01.csv` (default input dataset)

## Setup (venv)

Manual setup:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python.exe .\src\pipeline.py
```

Optional arguments:

```powershell
.\.venv\Scripts\python.exe .\src\pipeline.py --input .\cleaned_dataset_role01.csv --result-dir .\src\result
```

## Output location

All outputs are written inside `src\result\`:

- `plots\` (EDA and feature-importance charts)
- `data\` (feature-engineered CSV, selected feature JSON files, importance CSV files)
- `pipeline_summary.json`
