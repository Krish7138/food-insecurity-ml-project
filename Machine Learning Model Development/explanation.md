# Machine Learning Model Development

## Introduction

In the cleaned and feature-engineered dataset from previous stages was used to build machine learning models. The goal was to predict three important social hardship outcomes:

- Food insecurity
- Fuel poverty
- Child hardship

Different machine learning models were trained and compared to find which model performs best for each domain.

---

# Main Objectives of
The main goals of this stage were:

1. Prepare data for modelling  
2. Split data into training and testing sets  
3. Balance the dataset  
4. Train multiple machine learning models  
5. Tune model parameters  
6. Compare model performance  
7. Save trained models for later use  

---

# Why We Use Machine Learning

Machine learning allows systems to learn patterns from past data and make predictions on new data.

In this project, machine learning was used to identify households that may be at risk based on survey responses.

This can help:

- Government departments  
- Local councils  
- Charities  
- Support organisations  

to provide support earlier and more efficiently.

---

# Why We Used Multiple Models

Different algorithms learn patterns in different ways. One model may work better than another depending on the dataset.

Therefore, multiple models were tested and compared.

The models used were:

- Support Vector Machine (SVM)
- Random Forest
- Decision Tree
- XGBoost

---

# 1. Support Vector Machine (SVM)

## Why We Use This Model

SVM works well when data has complex boundaries between classes.

It is useful when categories are difficult to separate.

## Strengths

- Good for medium-sized datasets  
- Strong generalisation ability  
- Works well with many features  

## Why It Was Useful Here

Survey data contains many variables and hidden patterns. SVM can detect complex relationships.

---

# 2. Random Forest

## Why We Use This Model

Random Forest uses many decision trees together and combines their predictions.

## Strengths

- Handles nonlinear patterns  
- Works well with mixed data types  
- Reduces overfitting compared to single trees  

## Why It Was Useful Here

Social hardship is affected by many interacting factors such as income, health and housing.

---

# 3. Decision Tree

## Why We Use This Model

Decision Tree makes predictions using simple rule-based splits.

Example:

- If unemployed and low income = higher risk

## Strengths

- Easy to understand  
- Easy to explain  
- Good baseline model  

## Why It Was Useful Here

Useful for interpretable policy rules.

---

# 4. XGBoost

## Why We Use This Model

XGBoost is an advanced boosting algorithm that builds many small trees step-by-step.

## Strengths

- Often high predictive performance  
- Handles complex patterns  
- Strong on structured tabular data  

## Why It Was Useful Here

Survey datasets are structured tabular data, where XGBoost often performs strongly.

---

# Why We Split Data into Train and Test Sets

The dataset was divided into:

- 75% Training data  
- 25% Testing data  

## Why We Do This

Training data is used to teach the model.

Testing data is used to evaluate how well the model performs on unseen data.

## What We Achieve

This helps measure real-world prediction ability.

---

# Why We Balanced the Dataset

Some target classes had more records than others.

Example:

- Many secure households  
- Fewer severe hardship households  

This is called class imbalance.

## Why This Is a Problem

Without balancing:

- Model may favour majority class  
- Minority vulnerable groups may be ignored  

## Why We Used SMOTE

SMOTE creates synthetic examples for smaller classes.

## What We Achieve

- Better fairness  
- Better minority class prediction  
- Improved model learning  

---

# Why We Used GridSearchCV

Machine learning models have settings called hyperparameters.

Examples:

- SVM C value  
- Tree depth  
- Number of trees  
- Learning rate  

## Why We Use GridSearchCV

GridSearchCV tests many combinations automatically and selects the best one.

## What We Achieve

- Better model accuracy  
- Better tuned models  
- More reliable results  

---

# Why We Used Cross Validation

GridSearchCV uses cross validation.

This means training data is split into several parts and tested multiple times.

## Why This Helps

- Reduces chance of lucky results  
- More stable evaluation  
- Better model selection  

---

# Why We Used Preprocessing

Before training, data was prepared using:

- Missing value imputation  
- Standard scaling for numeric columns  
- One-hot encoding for categorical columns  

## Why This Is Needed

Machine learning models need numeric and clean input data.

## What We Achieve

- Better learning quality  
- Cleaner pipeline  
- Consistent training process  

---

# Why We Used One-Hot Encoding

Many survey columns were text categories such as:

- Gender  
- Age group  
- Household type  

Machine learning models need numbers.

## What We Did

Converted categories into binary columns.

## Example

Gender:

- Male = 1/0  
- Female = 0/1  

## What We Achieve

Allows models to use categorical information correctly.

---

# Why We Saved Models

After training, all models were saved into folders:

- models/food/
- models/fuel/
- models/child/

## Why We Do This

Saved models can be reused later without retraining.

## Benefits

- Faster evaluation  
- Used in Role 4  
- Easier deployment  

---

# Evaluation Metrics Used

The following metrics were recorded:

- Train Accuracy  
- Test Accuracy  
- Train Error  
- Test Error  
- Weighted F1 Score  
- Best Cross Validation Score  

---

# Why Accuracy Alone Is Not Enough

Accuracy shows total correct predictions.

But with imbalanced data, it can be misleading.

Therefore F1-score was also used.

---

# Why We Used Weighted F1 Score

Weighted F1 considers:

- Precision  
- Recall  
- Class imbalance  

This gives better performance measurement for real-world social data.

---

# What We Achieved in
1. Built models for three hardship domains  
2. Compared four machine learning algorithms  
3. Tuned models using GridSearchCV  
4. Balanced minority classes  
5. Saved all trained models  
6. Identified best model per domain  

---

# Practical Value

This modelling stage shows that survey data can be used to predict hardship risk early.

Possible use cases:

- Early warning systems  
- Council intervention planning  
- Charity targeting  
- Social support resource allocation  

---

# Conclusion
successfully developed machine learning models to predict food insecurity, fuel poverty and child hardship.

Using multiple algorithms, balanced data and parameter tuning helped improve prediction quality.

The results showed that no single model was best for every domain. Different social problems required different modelling approaches.

This stage created the foundation for Role 4, where models are evaluated, explained and interpreted in detail.