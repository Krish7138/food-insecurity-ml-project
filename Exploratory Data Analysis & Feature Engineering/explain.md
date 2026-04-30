# Exploratory Data Analysis & Feature Selection (Updated Version)

## Introduction

In this updated stage, the focus was placed on improving the quality of features before model training.

Instead of using all available variables directly, a feature selection process was introduced using **XGBoost Feature Importance**.

This helped identify the most useful variables for predicting:

- Food insecurity
- Fuel poverty
- Child hardship

By selecting stronger variables and removing weak ones, the later machine learning models became cleaner, faster and less likely to overfit.

---

# Main Objectives

1. Explore dataset structure  
2. Understand target distributions  
3. Create engineered features  
4. Train XGBoost model for each domain  
5. Measure feature importance  
6. Remove weak / zero-importance features  
7. Save final selected feature lists for the next stage  

---

# Why This Stage Is Important

Good models depend on good features.

If weak or irrelevant variables are included:

- noise increases
- overfitting increases
- training becomes slower
- accuracy may fall

Therefore, this stage was used to improve feature quality before modelling.

---

# Why We Used XGBoost for Feature Selection

XGBoost is a powerful tree-based algorithm that automatically learns which variables are most useful during training.

It provides a **feature importance score** for every input variable.

This makes it highly suitable for feature selection.

---

# Why XGBoost Was Chosen

## 1. Handles Nonlinear Relationships

Social hardship data is complex.

Examples:

- low income + unemployment
- health issue + fuel costs
- family type + child hardship

XGBoost captures these patterns better than simple linear methods.

---

## 2. Works Well with Mixed Data

The survey dataset contains:

- numerical features
- categorical variables
- engineered risk scores

XGBoost performs strongly on structured tabular data.

---

## 3. Gives Feature Importance Scores

After training, XGBoost shows how much each variable helped prediction.

Example:

- income may score high
- weak categories may score zero

This helps remove useless variables.

---

## 4. Fast and Reliable

XGBoost trains efficiently and often gives stable results.

This makes it practical for repeated domain-wise feature selection.

---

# What Is Feature Importance

Feature importance measures how useful a variable was during prediction.

Higher score = more useful feature.

Lower score = weak or unnecessary feature.

Example:

| Feature | Importance |
|--------|------------|
| Income | High |
| Household Type | Medium |
| Rare Category | Low |

---

# Domain Wise Feature Selection Process

Feature selection was done separately for:

- Food domain
- Fuel domain
- Child domain

This is important because different problems need different variables.

Example:

- Fuel poverty needs heating / housing variables
- Food insecurity needs income / support variables
- Child hardship needs household structure variables

---

# Steps Performed

## Step 1: Load Feature Engineered Dataset

The cleaned dataset from Role 1 was used.

---

## Step 2: Build Domain Feature Sets

Separate feature lists were created for:

- food_features
- fuel_features
- child_features

---

## Step 3: Train XGBoost

For each domain:

- X values = selected features
- y values = target label

XGBoost model was trained.

---

## Step 4: Extract Feature Importance

After training, importance scores were collected.

Bar charts were created to visualize top variables.

---

## Step 5: Remove Weak Features

Features with very low or zero importance were removed.

Examples:

- duplicate engineered features
- weak employment categories
- irrelevant domain features

---

## Step 6: Save Final JSON Files

Final selected features were saved as:

- food_features.json
- fuel_features.json
- child_features.json

These were then used in the next stage.

---

# Why We Removed Weak Features

Weak features may cause:

- overfitting
- slower training
- unstable results
- noisy predictions

Removing them improves generalization.

---

# What We Achieved

## 1. Cleaner Dataset

Only useful variables were kept.

## 2. Faster Training

Fewer columns reduce training time.

## 3. Lower Overfitting

Noise was reduced.

## 4. Better Accuracy Potential

Models focus on stronger signals.

## 5. Easier Interpretation

Important variables are easier to explain.

---

# Example Important Variables Found

Depending on domain, strong variables included:

- annual household income
- social support score
- household type
- age group
- health condition
- prepayment meter risk
- isolation score

---

# Why Not Use Correlation Only

Correlation only measures simple linear relationships.

But social hardship data often contains complex interactions.

XGBoost captures:

- nonlinear effects
- combined effects
- threshold effects

Therefore it was better than basic correlation filtering.

---

# Why This Helps the Next Stage

The next stage uses these final selected variables for model training.

Because weak features were removed earlier:

- models train better
- models overfit less
- evaluation becomes stronger

---

# Practical Importance

This approach helps build realistic early-warning systems where only meaningful information is used.

Possible uses:

- councils identifying hardship risk
- charities prioritising support
- fuel assistance targeting
- child welfare monitoring

---

# Final Conclusion

This updated stage used XGBoost feature importance to select the most useful variables for each hardship domain.

This method improved data quality by removing weak and noisy features before modelling.

Using XGBoost was effective because it handles complex survey data, captures nonlinear patterns and provides reliable feature rankings.

Overall, this stage created a stronger foundation for the next-stage machine learning model development.