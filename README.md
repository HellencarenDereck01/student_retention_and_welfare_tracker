
# Student Retention & Welfare Tracker

## Education & EdTech 

The **Student Retention & Welfare Tracker** is a data analysis project that looks at different factors that may affect students' attendance, welfare, and performance in school.

The project uses school attendance, Mid-Day Meal (MDM), infrastructure, school information, and test score data.

We cleaned the data, checked for errors, found useful patterns, and combined the data to create a school-level dataset that can be used for a dashboard.

## Project Goal

The main goal of this project is to help the Education Department understand the condition of schools and identify schools that may need more attention.

We look at:

- Student attendance
- Attendance reporting problems
- Mid-Day Meal procurement
- School infrastructure
- Student test scores
- Differences between districts
- Schools with several warning signs


# Project Structure

```text
student_retention_and_welfare_tracker/
│
├── data/
│   ├── raw/
│   │   ├── track4_mid_day_meal_procurement.xlsx
│   │   ├── track4_school_infrastructure.csv
│   │   ├── track4_school_master.csv
│   │   ├── track4_student_attendance.csv
│   │   └── track4_test_scores.json
│   │
│   └── processed/
│       ├── attendance_clean.csv
│       ├── infrastructure_clean.csv
│       ├── mid_day_meal_procurement_cleaned.csv
│       ├── school_master_cleaned.csv
│       ├── test_scores_clean.csv
│       └── school_dashboard.csv
│
├── notebooks/
│   ├── attendance_cleaning.ipynb
│   ├── infrastructure_cleaning.ipynb
│   ├── mid_day_meal_procurement_cleaning.ipynb
│   ├── school_master_cleaning.ipynb
│   ├── test_score_cleaning.ipynb
│   └── exploratory_analysis.ipynb
│
├── sql/
│   ├── source_views.sql
│   ├── school_kpis.sql
│   ├── welfare_risk.sql
│   └── school_dashboard.sql
│
├── src/
│   └── build_analytics.py
│
├── dashboard/
│   └── __init__.py
│
├── agent.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
````

---

# Data Used

We used five datasets in this project:

| Dataset               | What it contains                                |
| --------------------- | ----------------------------------------------- |
| Student Attendance    | Daily student attendance records                |
| MDM Procurement       | Mid-Day Meal food procurement records           |
| School Infrastructure | Information about school facilities             |
| School Master         | School names, districts, blocks, and enrollment |
| Test Scores           | Student assessment and test score records       |

The main column used to connect the datasets is school_id.
For attendance and MDM records, school_id and date can also be used together.

# Data Cleaning

The raw data had different types of problems. We cleaned each dataset before using it for analysis.

## 1. Student Attendance

The attendance data originally had **20,800 rows**.

We:

* Removed exact duplicate rows.
* Standardized school IDs.
* Standardized teacher presence values.
* Standardized grade values.
* Changed dates into one format.
* Calculated attendance rate.
* Found cases where the number of present students was higher than the total number of students.
* Found possible proxy attendance records, such as 100% attendance reported on Sundays.
* Kept these unusual records and marked them instead of deleting them.

### Result

|                                   | Number |
| --------------------------------- | -----: |
| Raw rows                          | 20,800 |
| Cleaned rows                      | 20,000 |
| Rows removed                      |    800 |
| Count problems found              |    806 |
| Possible proxy attendance records |    979 |
| Invalid dates                     |      0 |
| Missing school IDs                |      0 |



## 2. School Infrastructure

The infrastructure data originally had **3,150 rows**.

We:

* Removed duplicate rows.
* Standardized Yes/No values.
* Standardized school IDs.
* Standardized dates.
* Kept missing information where it was not possible to safely fill it.
* Created an Infrastructure Deficit Index to show how many of the checked facilities were not functional.

Different values such as:
Yes, Y, 1, Haan, Hai, Working, Functional were treated as positive/functional.

Values such as No, N, 0, Nahi, Kharab, Broken, Under Repair were treated as negative/not functional.

### Result

|                        | Number |
| ---------------------- | -----: |
| Raw rows               |  3,150 |
| Cleaned rows           |  3,000 |
| Duplicate rows removed |    150 |
| Schools covered        |    598 |
| Invalid dates          |      0 |



## 3. Mid-Day Meal Procurement

The MDM data had different units and different ways of writing vendor and food names.

We:

* Standardized vendor names.
* Standardized grain names.
* Changed all quantities to kilograms.
* Handled values with units written inside the quantity.
* Converted bags/sacks to kilograms using the project rule of **1 bag/sack = 50 kg**.
* Cleaned the cost values.
* Standardized payment status.

The cleaned MDM dataset contains **12,000 records**.


## 4. Test Scores

The test score data contains **8,000 records**.

The scores were recorded in different formats, so we changed them into one percentage format.

For example:

* Percentage scores were kept as percentages.
* Scores such as `45/50` were changed to percentages.
* Letter grades were changed to percentage values.
* CGPA values were converted to percentages.

The final score column is called score_percentage

### Result

|               |  Value |
| ------------- | -----: |
| Assessments   |  8,000 |
| Schools       |    600 |
| Average score | 66.06% |
| Median score  | 65.00% |
| Lowest score  |    38% |
| Highest score |    95% |



## 5. School Master

The School Master data is used as the main school reference table.

The cleaned data contains:

* 600 schools
* School ID
* School name
* District
* Block
* Total enrollment
* School type
* Medium

Each school has one record in this table.
# Data Analysis

After cleaning the data, we looked at the main patterns in the datasets.

The analysis includes:

* Average attendance
* Attendance problems
* MDM regularity
* MDM cost and quantity
* School infrastructure
* Test scores
* District comparisons
* Schools with several warning signs

We first summarized each dataset by school before joining them. This prevents the same school from being counted many times when different datasets are combined.
# Main Measures

The project looks at several important measures.

### Attendance

* Average Attendance Rate
* Potential Proxy Attendance Rate
* Attendance Count Anomaly Rate

### Mid-Day Meal

* MDM Regularity Rate
* Total MDM Quantity
* Total MDM Cost
* MDM Cost per KG
* Vendor information

### Infrastructure

* Number of Functional Facilities
* Number of Assessed Facilities
* Infrastructure Deficit Index

### Test Scores

* Average Test Score
* Number of Assessments
* Subjects Assessed
* Average Test Score by District

### School Risk

We created a simple **Student Welfare Risk Score** using six warning signs:

1. Low attendance
2. High potential proxy attendance
3. High attendance count problems
4. Low MDM regularity
5. High infrastructure deficit
6. Low test scores

Schools are grouped into:

* Low Risk
* Moderate Risk
* High Risk

The risk score is only used to help identify schools that may need further attention. It does not prove that a school has a problem.
# Main Findings
## Attendance

The overall average attendance rate is about **81.66%**.

The differences between districts are small. However, some districts have more attendance reporting problems than others.

## Potential Proxy Attendance

About **4.94%** of attendance records were marked as potential proxy attendance.
These records are treated as **possible unusual reporting**, not confirmed fraud.

## MDM Regularity
The average MDM regularity rate is about **60.61%**.
In our data, there was almost no relationship between MDM regularity and average attendance.
Therefore, we do not claim that MDM regularity directly causes higher or lower attendance.

## School Infrastructure
The average Infrastructure Deficit Index is about **28.90%**.
Most schools fall within the moderate deficit range.
The analysis also showed very little relationship between the overall infrastructure deficit and attendance in this dataset.

## Test Scores
The average test score is about **66.06%**.
The average scores between districts are fairly close.

## Schools with Higher Risk
The risk analysis identified **10 schools** as high risk.
Moga had the highest number of high-risk schools in our analysis.
One important finding was that some schools with high attendance still had a high risk score because of problems in other areas.
This shows why looking at only attendance is not enough.

# Final School Dataset
The final file is:
```text
data/processed/school_dashboard.csv
```

It contains **600 schools**, with one row for each school.
It includes information about:

* School details
* Attendance
* MDM
* Infrastructure
* Test scores
* Welfare risk score
* Risk level

# SQL

We use **DuckDB** and SQL to create the final school-level results.
The process is:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Cleaned Data
   ↓
SQL Analysis
   ↓
School KPIs
   ↓
Welfare Risk Score
   ↓
Final School Dataset
   ↓
Dashboard
```

The SQL files are used to:

* Load the cleaned data.
* Calculate school-level measures.
* Calculate the welfare risk score.
* Create the final school dashboard data.


# How to Run the Project

## 1. Clone the repository

```bash
git clone https://github.com/Sukanya022/student_retention_and_welfare_tracker.git
```

## 2. Open the project folder

```bash
cd student_retention_and_welfare_tracker
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the environment

For Windows:

```bash
venv\Scripts\activate
```

## 5. Install the required packages

```bash
pip install -r requirements.txt
```

## 6. Run the analytics pipeline

```bash
python src/build_analytics.py
```

The final school dataset will be created at:

```text
data/processed/school_dashboard.csv
```
# Dashboard

The cleaned and final school-level data is used to build an interactive dashboard.

The dashboard shows:

* Main school and district measures
* Attendance trends
* MDM information
* Infrastructure conditions
* Test scores
* High-risk schools
* School-level details
* District comparisons
# Limitations

There are some questions that cannot be answered directly because the required information is not available in the provided data.

### MDM Utilization and Wastage

The MDM dataset contains procurement information but does not contain reliable information about how much food was actually used or wasted.

Therefore, we do not calculate or make up a wastage value.

Instead, we use MDM quantity, cost, and regularity.

### Female Attendance

The attendance data does not contain student gender information.

Because of this, we cannot directly compare functional toilets with female attendance.

We instead compare infrastructure conditions with overall attendance.

### Risk Score

The risk score is a simple screening tool based on the available data.

It should not be treated as proof that a school is failing or that one factor causes another.


#  Tools Used

- Python
- VS Code
- Pandas
- NumPy
- DuckDB
- SQL
- Plotly
- Streamlit
- Git & GitHub


