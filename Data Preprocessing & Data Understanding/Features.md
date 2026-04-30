# Features

### Column: `#`

* Type: Integer
* Description: Record identifier or row index.

### Column: `I agree to take part in this survey`

* Type: Binary
* Values:

   1 = Agreed
   0 = Did not agree
Range: {0, 1}

---

### Column: `Gender`

* Type: Nominal categorical
* Values:

  * Male
  * Female
  * Prefer not to say
  * Non binary/ other


### Column: `Age group`

* Type: Ordinal categorical
* Categories:

  Range {16to19 - 75to79}

---

### Column: `Health condition limiting daily activities`

* Type: Categorical
* Values:

  * Yes
  * No
  * Prefer not to say


### Column: `Household type`

* Type: Nominal categorical
* Categories include:

  * Living alone (no children)
  * Living with partner (no children)
  * Living with partner (with children under 18)
  * Living with other non-family adults
  * Living with adult family members
  * Living alone with children



### Column: `Life satisfaction`

* Type: Numerical (discrete)
* Range: 1 to 10
* null values 


### Column: `Life compared to neighbourhood`

* Type: Ordinal categorical
* Values:

  * Much worse
  * Worse
  * The same
  * Better
  * Much better
  * Null values


### Column: `Lack companionship`

* Type: Ordinal categorical
* Values:

  * Hardly ever or never
  * Some of the time
  * Often
  * null values



### Column: `Feel isolated`

* Type: Ordinal categorical
* Values:

  * Hardly ever or never
  * Some of the time
  * Often
  * Null value 


### Column: `Turn to friends and family for help`

* Type: Ordinal categorical
* Values:

  * Not at all
  * To some extent
  * To a large extent 
  * Null value 


### Column: `Borrow or exchange favours with neighbours`

* Type: Ordinal categorical
* Values:

  * Definitely disagree
  * Tend to disagree
  * Tend to agree
  * Definitely agree
  * Null value

# Food Support Sources (Multi-label Variables)

### Columns:

* Foodbank
* Neighbours
* Close family or friends
* Community or faith group
* None of the above
* Other

Type: Binary presence indicator

* If text is present, the source was used.
* If NaN, the source was not used.

The `Other` column contains free-text responses describing additional support sources.



# Adult Food Insecurity 

## Core Food Insecurity Questions

### Columns:

* Worried food would run out before getting money to buy more
* Food bought did not last and no money to get more
* Could not afford balanced meals

Type: Ordinal categorical
# Values:

* Never true
* Sometimes true
* Often true
* Null value
### Columns:
* Cut meal size or skipped meals
* Ate less than felt necessary
* Hungry but did not eat
* Lost weight due to lack of food
* Did not eat for a whole day
* These represent increasing severity of food insecurity.

Type: Binary
Values:

* Yes
* No
* Null value
## Frequency Questions

### How often did this happen?
 * Null value
# Child Food Insecurity
### Columns: 
* Relied on low-cost food for children
* Could not afford balanced meals for children
* Children were not eating enough
# Values:
* Never true
* Sometimes true
* Often true
* Null value

# Child Severe Food Insecurity Indicators

## Columns:
* Cut size of children's meals
* Children skipped meals
* Children hungry but could not afford food
* Children did not eat for a whole day

Type: Binary categorical
Values:
* Yes
* No
* Null value
## Frequency of Child Food Insecurity

## Column:

How often did this happen? (child section)
Type: Ordinal categorical
Values:
* Only 1 or 2 months
* Some months but not every month
* Almost every month
* Null value
Missing values in these columns generally indicate that the household does not have children.


# Housing Characteristics

### Column: `Housing type`

* Type: Nominal categorical
* Includes:

  * Renting from private landlord
  * Housing association
  * Buying with mortgage
  * Owning outright
  * Temporary accommodation
  * Student accommodation
  * Shelter or hostel

---

### Column: `EPC rating`

* Type: Ordinal categorical
* Values: A, B, C, D, E, F, G
* A represents highest energy efficiency and G the lowest.
* Includes "Don't know".

---

### Column: `Prepayment meter`

* Type: Categorical
* Values:

  * Yes
  * No
  * Don't know

---

# Energy Poverty Indicators

## Frequency-Based Energy Hardship

Type: Ordinal categorical
Values:

* Never
* 1 or 2 months
* Some months but not every month
* Almost every month

Columns include:

* Reduced expenses to pay energy bill
* Kept home cold
* Behind on energy payments
* Worried about energy payments
* Worried about rent or mortgage payments
* Avoided cooking to reduce energy use

---

## Binary Energy Hardship

Type: Binary
Values:

* 1 = Yes
* 0 = No

Columns:

* Unable to use heating due to affordability
* Heating equipment broken and unaffordable to repair
* Medical attention required due to cold home

---

## Numerical Feature

### Column: `Days without heat`

* Type: Continuous numerical
* Observed range: 0 to 365 days
* Higher values indicate severe energy deprivation.
* Contains extreme values that may require outlier analysis.

---

# Employment Status (Multi-label)

Separate binary columns:

* Working full-time
* Working part-time
* Unemployed
* Retired
* Not working – looking after house/children
* Not working – long term sick or disabled
* Student
* Other

Each column:

* Non-null value indicates presence (1)
* Null indicates absence (0)

The `Other` column contains free-text employment descriptions.

---

# Income

### Column: `Annual household income`

* Type: Ordinal categorical
* Categories:

  * Less than £14,900
  * £14,901–£24,300
  * £24,301–£37,900
  * £37,901–£58,900
  * More than £58,900
  * Prefer not to say

### Column: `incentivised`
# Values:{0,1}