# Data Preprocessing & Data Understanding

This project now includes a reproducible Python pipeline in `src\pipeline.py` that implements the preprocessing logic from `main.ipynb`.

## Required folder and files to run the pipeline

Run the commands from the project root folder:

- `src\pipeline.py` (pipeline script)
- `requirements.txt` (Python dependencies)
- `Food_insecurity_Raw_Survey_Responses.xlsx` (input dataset file)

All generated outputs (cleaned dataset, graphs, and summary files) are saved inside:

- `src\result\`

## Run with venv

Manually create a virtual environment, install dependencies, and run the pipeline:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python .\src\pipeline.py
```

After execution, check `src\result\` for:

- `cleaned_dataset_role01.csv`
- label distribution plots
- score distribution plots
- `summary.json`

## Instructions

### 1. Manual setup (venv)

Run these commands from the project root:

1. `python -m venv .venv`
2. `.\.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python .\src\pipeline.py`

### 2. Output location

Every generated graph and output artifact is saved in:

- `src\result\`

This includes the cleaned dataset CSV and summary/plot files.
