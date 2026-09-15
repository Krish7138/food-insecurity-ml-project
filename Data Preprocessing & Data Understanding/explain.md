# Data Preprocessing & Data Understanding

## Introduction

This stage prepares raw survey responses for machine learning by converting noisy, mixed-format inputs into a consistent and model-ready dataset.

The notebook in this folder performs the full preprocessing pipeline:

 Loads multiple survey sheets from one Excel workbook
 Merges them into a single dataframe
 Filters responses based on explicit consent
- Standardizes long question text into stable column names
- Converts text responses to numeric values
- Builds domain scores and target labels
- Normalizes support-source fields into binary indicators
- Exports the final cleaned dataset

---

## Main Objectives

1. Understand the raw data structure and available sheets
2. Combine data from multiple collection sources
3. Remove non-consent records
4. Standardize critical column names
5. Transform survey text responses into numeric signals
6. Build food, child, and fuel hardship scores
7. Create final class labels for each domain
8. Export a clean dataset for downstream feature engineering and modeling

---

## Why This Stage Is Important

Machine learning models require clean and consistent input data. Raw survey files usually contain:

- Long free-text column headers
- Mixed categorical responses
- Missing values
- Domain-specific answer formats

Without preprocessing, model quality drops because of noise, inconsistent mapping, and unstable feature definitions.

This stage ensures later steps use reliable data.

---

## Data Sources and Merge Strategy

The workbook `Food_insecurity_Raw_Survey_Responses.xlsx` is loaded and the following sheets are merged:

- 2022-12-03_incentivised
- 2022-11-22_27_incentivised
- 2022-11-22_27_non_incentivised

After reading each sheet, they are concatenated into one dataframe for unified cleaning and scoring.

---

## Consent Filtering

A strict consent check is applied to keep only records where participants agreed to the survey terms.

This step:

- Removes ineligible responses
- Improves ethical data handling
- Keeps only valid rows for analysis

Duplicate count is also checked to understand data quality after filtering.

---

## Column Standardization

Several long survey questions are renamed to shorter, stable names (for example, `food_worry`, `food_not_last`, `no_balanced_meal`).

Why this is needed:

- Long question strings are error-prone in code
- Minor text or encoding differences can break transformations
- Stable names improve maintainability

A fallback alias rule is included for `food_not_last` so preprocessing remains robust even if punctuation/apostrophe variants appear in source columns.

---

## Domain Question Sets

The notebook defines three domain-specific feature groups:

- `food_cols`
- `child_cols`
- `fuel_cols`

These lists are used consistently for:

- Numeric mapping
- Score construction
- Label creation

This ensures each target label is computed from its intended question set.

---

## Response Mapping and Numeric Conversion

A mapping dictionary converts text responses into binary values (mostly 1 for risk/affirmative and 0 for non-risk/negative).

Processing logic per column:

1. Strip whitespace and normalize values
2. Replace text responses using the mapping dictionary
3. Convert to numeric type
4. Fill non-convertible/missing values with 0

This produces clean numeric features suitable for model training.

---

## Fuel Heating-Days Threshold Rule

For the question about number of days without heat, a threshold transformation is applied:

- 1 if days >= 36
- 0 otherwise

This converts a long-tail numeric input into a consistent binary hardship risk signal.

---

## Score and Label Construction

Three hardship scores are created by summing mapped domain columns:

- `food_security_score`
- `child_security_score`
- `fuel_security_score`

Class labels are then generated from score thresholds:

- Food: High, Marginal, Low, Very Low
- Child: High, Marginal, Low, Very Low
- Fuel: Secure, Moderate Risk, High Risk

These labels become the main supervised learning targets in later stages.

---

## Support Feature Normalization

Support-source columns are converted to binary indicators:

- Foodbank
- Community or faith group
- Close family or friends
- Neighbours

Each is mapped to 1 when present and 0 otherwise.

This creates compact and model-friendly representations of support access behavior.

---

## Output

The cleaned final dataset is saved as:

- `cleaned_dataset_role01.csv`

This file is the main output of the stage and is used by subsequent feature engineering and modeling workflows.

---

## Data Quality and Safety Notes

- Domain labels are derived from explicitly defined domain column sets.
- Missing or unexpected mapped values are coerced safely to numeric defaults.
- Duplicate and shape checks are included as quick integrity validations.

These controls reduce leakage risk and improve reproducibility.

---

## Limitations

- Survey data is self-reported and may contain response bias.
- Binary mapping simplifies nuanced response intensity.
- Threshold choices (for example, heating-days cutoff) are rule-based and may be refined later.

---

## Future Improvements

1. Add explicit schema validation before transformations
2. Track per-column missingness before and after mapping
3. Externalize mapping and thresholds into a config file
4. Add unit tests for scoring and label functions
5. Version output files with timestamp or run id

---

## Final Conclusion

This stage converts raw multi-sheet survey data into a structured, numerically encoded, and labeled dataset ready for machine learning.

By combining consent filtering, robust mapping, domain-wise scoring, and consistent output generation, the pipeline builds a dependable foundation for the next project stages.
