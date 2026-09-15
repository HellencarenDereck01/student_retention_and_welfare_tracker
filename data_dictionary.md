# Data Dictionary

This document describes the cleaned datasets used in the Student Retention &
Welfare Tracker project.

It explains the columns in each dataset and the columns created during the
data cleaning and analysis process.

The final section describes the school_dashboard.csv file, which combines
the main school-level information used for the dashboard.

### 1. Student Attendance
### 2. School Infrastructure
### 3. Mid-Day Meal Procurement
### 4. School Master
### 5. Test Scores
### 6. Final School Dashboard Dataset

## 1. Student Attendance
| Column | Description | Data Type |
|---|---|---|
| record_id | ID of the attendance record | String |
| grade | Grade/class of the students | Integer |
| total_students| Total number of students recorded | Integer |
| present_students | Number of students marked present | Integer |
| marked_by | Person who recorded the attendance | String |
| attendance_count_anomaly` | Shows if the number of present students is greater than the total number of students | Boolean |
| attendance_rate | Percentage of students marked present | Float |
| date | Date of the attendance record | Date |
| day_of_week | Day of the week calculated from the date | String |
| is_sunday | Shows whether the attendance record is on a Sunday | Boolean |
| proxy_attendance_flag | Flags possible proxy attendance records | Boolean |
| school_id | Unique ID of the school | String |
| teacher_present | Shows whether the teacher was present | Boolean |

## 2. School Infrastructure
| Column | Description | Data Type |
|---|---|---|
| inspection_id | ID of the infrastructure inspection | String |
| has_electricity | Shows whether electricity is available or functional | Boolean |
| has_drinking_water | Shows whether drinking water is available or functional | Boolean |
| has_functional_toilet | Shows whether the school has a functional toilet | Boolean |
| has_boundary_wall | Shows whether the school has a boundary wall | Boolean |
| has_playground | Shows whether the school has a playground | Boolean |
| inspector_name | Name of the person who carried out the inspection | String |
| remarks | Additional comments from the inspection | String |
| date | Date of the infrastructure inspection | Date |
| school_id | Unique ID of the school | String |

## 3. Mid-Day Meal Procurement
| Column | Description | Data Type |
|---|---|---|
| procurement_id | ID of the procurement record | String |
| date | Date of the procurement | Date |
| school_id | Unique ID of the school | String |
| vendor_name | Name of the supplier/vendor | String |
| grain_type | Type of food or grain purchased | String |
| quantity | Quantity purchased after converting the units to kilograms | Float |
| unit | Unit of measurement for the quantity | String |
| total_cost | Total cost of the procurement | Float |
| payment_status | Payment status of the procurement | String |

## 4. School Master
| Column | Description | Data Type |
|---|---|---|
| school_id | Unique ID of the school | String |
| school_name | Name of the school | String |
| district | District where the school is located | String |
| block | Block where the school is located | String |
| total_enrolled_students | Total number of students enrolled in the school | Integer |
| school_type | Type of school | String |
| medium | Medium of instruction used in the school | String |

## 5. Test Scores
| Column | Description | Data Type |
|---|---|---|
| assessment_id | ID of the assessment record | String |
| grade | Grade/class of the students | Integer |
| grading_scale | Grading system used in the original record | String |
| avg_score | Average score recorded for the assessment | Float |
| max_marks | Maximum marks for the assessment, where available | Float |
| total_students_assessed | Number of students included in the assessment | Integer |
| score_percentage | Student score converted to a percentage | Float |
| date | Date of the assessment | Date |
| school_id | Unique ID of the school | String |
| subject | Subject of the assessment | String |

## 6. Final School Dashboard Dataset
| Column | Description | Data Type |
|---|---|---|
| school_id | Unique ID of the school | String |
| school_name | Name of the school | String |
| district | District where the school is located | String |
| block | Block where the school is located | String |
| total_enrolled_students | Total number of students enrolled in the school | Integer |
| school_type | Type of school | String |
| medium | Medium of instruction used in the school | String |
| avg_attendance_rate | Average attendance rate of the school | Float |
| total_attendance_records | Total number of attendance records | Integer |
| proxy_attendance_records | Number of records flagged as possible proxy attendance | Integer |
| proxy_attendance_rate | Percentage of attendance records flagged as possible proxy attendance | Float |
| count_anomaly_records | Number of records where present students were greater than total students | Integer |
| count_anomaly_rate | Percentage of attendance records with count anomalies | Float |
| total_mdm_quantity_kg | Total MDM quantity purchased in kilograms | Float |
| total_mdm_records | Total number of MDM procurement records | Integer |
| total_mdm_cost | Total cost of MDM procurement | Float |
| avg_mdm_cost | Average cost per MDM procurement record | Float |
| mdm_regularity_rate | Relative measure of how regular MDM procurement records are across schools | Float |
| unique_vendors | Number of different vendors supplying the school | Integer |
| unique_grain_types | Number of different grain or food types purchased | Integer |
| assessed_facilities | Number of infrastructure facilities with available information | Integer |
| functional_facilities | Number of assessed facilities that were functional | Integer |
| infrastructure_deficit_index | Percentage of assessed facilities that were not functional | Float |
| average_test_score | Average student test score as a percentage | Float |
| total_assessments | Total number of test assessments | Integer |
| subjects_assessed | Number of different subjects assessed | Integer |
| student_welfare_risk_score | Total number of warning signs identified for the school | Integer |
| risk_level | Risk category based on the welfare risk score | String |

