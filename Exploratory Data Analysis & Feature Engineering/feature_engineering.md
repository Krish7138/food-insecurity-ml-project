# Feature Engineering Explanation

## Introduction

Feature engineering was used to transform raw survey responses into meaningful indicators that improve machine learning model performance. These engineered variables help capture economic hardship, social vulnerability, health risk, and combined deprivation factors more effectively than raw columns alone.

---

# 1. income_risk_group

## What is this?

This feature classifies households into low-income risk groups.

Example:

- 1 = Low income household  
- 0 = Higher income household

## Why we take this?

Income is one of the strongest predictors of:

- Food insecurity
- Fuel poverty
- Child hardship

Using one grouped variable is easier than many income categories.

## Impact

- Reduces category complexity
- Highlights poverty risk
- Improves model learning

## What we achieved

- Better prediction accuracy
- Easier interpretation
- Stronger financial hardship signal

---

# 2. employment_risk

## What is this?

A score created from employment status.

Example:

- Unemployed = High risk
- Part-time = Medium risk
- Full-time = Low risk

## Why we take this?

Employment affects:

- Household income
- Bill payment ability
- Financial stability

## Impact

Combines multiple employment columns into one useful feature.

## What we achieved

- Stronger economic predictor
- Simpler data structure
- Better model performance

---

# 3. social_support_score

## What is this?

Counts available support sources such as:

- Foodbank
- Family
- Community group
- Neighbours

## Why we take this?

Support networks help households survive hardship.

## Impact

Higher support can reduce vulnerability.

## What we achieved

- Added social resilience information
- Better real-world prediction
- Stronger welfare insights

---

# 4. isolation_score

## What is this?

Converts loneliness or isolation responses into numeric score.

Example:

- Never = 0
- Rarely = 1
- Sometimes = 2
- Often = 3
- Always = 4

## Why we take this?

Isolation is linked to:

- Mental stress
- Reduced support access
- Higher hardship risk

## Impact

Makes wellbeing measurable for models.

## What we achieved

- Better emotional risk signal
- Improved prediction quality
- Stronger behavioural insight

---

# 5. health_risk

## What is this?

Binary feature:

- 1 = Has limiting health condition
- 0 = No limiting condition

## Why we take this?

Poor health may reduce:

- Ability to work
- Income security
- Heating tolerance
- Household resilience

## Impact

Strong vulnerability indicator.

## What we achieved

- Better hardship prediction
- Improved fairness
- Better health-economic link analysis

---

# 6. prepay_meter_risk

## What is this?

Binary feature:

- 1 = Uses prepayment meter
- 0 = Does not use prepayment meter

## Why we take this?

Prepayment users often face:

- Higher costs
- Running out of credit
- Self-disconnection
- Fuel poverty

## Impact

Strong predictor for energy hardship.

## What we achieved

- Better fuel poverty modelling
- Improved energy-risk detection

---

# 7. fuel_vulnerability_score

## What is this?

Combined score using:

- Low income
- Health risk
- Prepayment meter risk

## Why we take this?

Fuel poverty is usually caused by multiple risks together.

## Impact

Captures compound hardship more accurately.

## What we achieved

- Better than single features alone
- Higher fuel model accuracy
- More realistic household vulnerability score

---

# 8. income_unemployed_interaction

## What is this?

Interaction feature:

Low income × Unemployed

## Why we take this?

Low income alone is risk.  
Unemployment alone is risk.  
Together creates much higher hardship pressure.

## Impact

Captures severe economic distress.

## What we achieved

- Better food insecurity prediction
- Better child hardship prediction
- Improved extreme-case detection

---

# 9. medical_heat_risk

## What is this?

Interaction feature:

Health risk × Prepayment meter risk

## Why we take this?

Households with health issues and heating difficulty are highly vulnerable.

## Impact

Strong predictor for cold-home hardship.

## What we achieved

- Better fuel poverty prediction
- Better vulnerable household identification
- Better welfare targeting potential

---

# Overall Importance of Feature Engineering

## Why we used it

Raw survey data can be noisy and fragmented. Feature engineering transforms raw answers into stronger predictive indicators.

## Overall Impact

- Reduced noise
- Better patterns for machine learning
- Stronger domain insights

## Final Achievement

1. Improved model accuracy  
2. Easier interpretation  
3. Better social risk prediction  
4. Stronger dissertation quality  
5. More useful policy recommendations