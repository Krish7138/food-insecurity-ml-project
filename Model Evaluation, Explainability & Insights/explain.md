# Model Evaluation, Visual Analysis & Final Insights

## Introduction

In this stage, the machine learning models developed in the previous stage were evaluated using unseen test data.

The purpose of this stage was to determine:

- Which model performed best
- How reliable each model was
- Whether overfitting existed
- How models compared across domains
- Which visualisations best explained model behaviour

The three domains evaluated were:

- **Food insecurity**
- **Fuel poverty**
- **Child hardship**

---

## Main Objectives

1. Evaluate trained models using test data  
2. Compare all models across domains  
3. Detect overfitting using train–test gap  
4. Visualise prediction performance  
5. Use ROC curves for classification quality  
6. Use confusion matrices for error analysis  
7. Draw final conclusions  
8. Suggest future improvements  

---

## Why This Stage Is Important

A trained model is only useful if it performs well on new, unseen data.

Role 4 verifies:

- Accuracy on unseen data
- Prediction mistakes
- Model stability
- Model suitability for selection

This stage converts technical model results into practical business insight.

---

## Models Evaluated

The following algorithms were trained and compared:

- SVM
- Random Forest
- Decision Tree
- XGBoost

Each model was tested in:

- Food domain
- Fuel domain
- Child domain

---

## Evaluation Methods Used

### 1. Confusion Matrix

#### What It Is

A confusion matrix compares:

- Actual class labels
- Predicted class labels

It highlights both correct predictions and errors.

#### Why It Was Used

Accuracy alone does not show which classes were misclassified.  
A confusion matrix gives class-level error detail.

Examples:

- Severe hardship predicted as moderate hardship
- Low food security predicted as marginal

#### What Was Achieved

- Identified weak classes
- Found overlapping labels
- Improved understanding of model mistakes

---

### 2. ROC Curve

#### What It Is

ROC = **Receiver Operating Characteristic** curve.

It plots:

- True Positive Rate (TPR)
- False Positive Rate (FPR)

across different thresholds.

#### Why It Was Used

Two models may have similar accuracy but different class-separation ability.  
ROC helps evaluate discrimination quality beyond accuracy.

#### What Was Achieved

- Measured class-separation strength
- Compared models beyond raw accuracy
- Assessed prediction reliability

---

### 3. Train vs Test Error Plot (Domain-Wise)

#### What It Is

Error was defined as:

```text
Error = 1 - Accuracy
```

Plots were created for:

- Food domain
- Fuel domain
- Child domain

for all models.

#### Why It Was Used

To detect overfitting.  
If train error is very low but test error is high, the model may have memorised training data.

#### What Was Achieved

- Detected unstable models
- Compared generalisation performance
- Selected more balanced models

---

### 4. Train vs Test Accuracy Plot (All Models)

#### What It Is

Bar charts comparing:

- Train Accuracy
- Test Accuracy

For:

- SVM
- Random Forest
- Decision Tree
- XGBoost

across all domains.

#### Why It Was Used

This allows quick visual comparison of strongest-performing models.

#### What Was Achieved

- Identified the best model by domain
- Compared all algorithms clearly
- Explained performance differences

---

## Domain-Wise Findings

### Food Domain

#### Observation

Food insecurity was the hardest domain.

#### Reasons

- Four overlapping labels
- Similar patterns between classes
- Complex social behaviour factors

#### Result

Accuracy was lower than in other domains.

---

### Fuel Domain

#### Observation

Fuel poverty showed stronger model performance.

#### Reasons

- Housing type
- EPC rating
- Prepayment meter usage
- Heating affordability

These were clearer indicators.

---

### Child Domain

#### Observation

Child hardship predictions were often stable.

#### Reasons

- Income level
- Household type
- Employment status

These strongly influenced child hardship outcomes.

---

## Model Behaviour Summary

### XGBoost

**Strengths:**

- Strong overall performance
- Handles non-linear relationships
- Often the best model

### Random Forest

**Strengths:**

- Stable performance
- Lower variance than a single tree

### Decision Tree

**Weakness:**

- Higher overfitting risk
- Lower test accuracy

### SVM

**Strengths:**

- Good performance on structured data
- Competitive in some domains

---

## What Was Achieved

1. **Real performance measurement**  
    Used unseen test data.

2. **Overfitting detection**  
    Used train–test accuracy/error gap.

3. **Error understanding**  
    Used confusion matrices.

4. **Better comparison**  
    Used domain-wise visualisations.

5. **Practical insights**  
    Identified suitable models for deployment.

---

## Practical Value of Results

These models can support:

- Early hardship detection
- Council support planning
- Food bank demand forecasting
- Fuel support targeting
- Child welfare risk screening

---

## Limitations

- Survey responses are self-reported
- Some labels overlap strongly
- Class imbalance exists
- Limited external socio-economic data
- Snapshot-only (non-longitudinal) data

---

## Future Enhancements

### 1. Add More External Data

Examples:

- Postcode deprivation score
- Local inflation
- Regional unemployment

### 2. Improve Imbalance Handling

Use:

- SMOTEENN
- Class-weighted learning

### 3. Try Advanced Models

- CatBoost
- LightGBM
- Ensemble stacking

### 4. Probability Calibration

Improve confidence score quality.

### 5. Time-Series Prediction

Track hardship changes over time.

### 6. Explainable AI

Add:

- SHAP
- LIME
- Local explanations

---

## Final Conclusion

This stage successfully evaluated all trained machine learning models using confusion matrices, ROC curves, train–test error plots, and train–test accuracy comparisons.

Performance varied by domain. Food insecurity was the most difficult problem, while fuel and child domains often showed stronger predictive patterns.

Overall, **XGBoost** and **Random Forest** performed best, while **Decision Tree** showed higher overfitting risk.

The evaluation confirms that machine learning can effectively support identification of vulnerable households and enable early intervention in real-world social policy settings.