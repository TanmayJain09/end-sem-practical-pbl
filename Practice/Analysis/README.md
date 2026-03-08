# Attendance Data Analysis (EDA & Student Analytics)

## Project Overview

This notebook performs **data cleaning, transformation, exploratory data analysis (EDA), and student-level analytics** on attendance data.

The objective is to convert raw attendance records into **structured insights** that help understand:

- Lecture attendance patterns
- Batch-wise attendance behavior
- Student attendance performance
- Students at risk due to low attendance

The analysis prepares the dataset for **future dashboard visualization and automated analytics systems**.

---

# Dataset Description

The dataset contains **lecture-level attendance records**.

Each row represents the attendance status of a student for a specific lecture.

| Column | Description |
|------|------|
| Batch | Student batch (D1 / D2 / BOTH) |
| PRN | Unique student ID |
| Name | Student name |
| Present | Attendance indicator (1 = Present, 0 = Absent) |
| DateTime | Date and time of lecture |

Example:

| Batch | PRN | Name | Present | DateTime |
|------|------|------|------|------|
| D2 | 2501132081 | Deshpande Aditya Milind | 1 | 2026-02-23 09:30:00 |

---

# Data Processing Pipeline

The notebook follows a structured **data analytics workflow**.

---

## 1. Data Import

Attendance data is loaded into a **Pandas DataFrame** for processing.

Main operations:
- Import CSV file
- Initial inspection (`head`, `info`, `shape`)

Purpose:
To understand the structure of the dataset before cleaning.

---

## 2. Data Cleaning

Cleaning steps include:

- Standardizing column types
- Ensuring `PRN` is treated as a string
- Converting date and time into proper datetime format
- Removing redundant columns

This ensures the dataset is **consistent and analysis-ready**.

---

## 3. Feature Engineering

A new column `DateTime` is created by combining **Date and Time**.

This enables analysis across:

- Individual lectures
- Daily attendance patterns
- Time-based lecture analysis

Example transformation: Date + Time --> DateTime


---

# Exploratory Data Analysis (EDA)

EDA is used to understand the **structure, trends, and distribution** of attendance data.

---

## 4. Dataset Overview

Basic dataset statistics are calculated:

- Total records
- Total students
- Number of lectures conducted

This gives a **high-level overview of the dataset scale**.

---

## 5. Overall Attendance Metrics

The notebook calculates:

- Total present entries
- Total absent entries
- Overall attendance percentage

This provides a **general attendance health indicator**.

---

## 6. Lecture-Level Analysis

Attendance is analyzed across different lectures.

Key insights include:

- Attendance percentage per lecture
- Participation trends across lecture times

This helps identify **which lectures had higher or lower participation**.

---

## 7. Batch-Level Analysis

Attendance behavior is analyzed by **student batch**.

Metrics include:

- Average attendance per batch
- Comparison between batches

This helps detect **systematic differences between batches**.

---

# Student-Level Analytics

A **student analytics table** is created to summarize attendance performance.

Each student’s attendance is calculated relative to **total lectures conducted for their batch**.

Columns generated:

| Column | Description |
|------|------|
| PRN | Student identifier |
| Name | Student name |
| Lectures_Attended | Total lectures attended |
| Total_Lectures_Batch | Total lectures for student's batch |
| Net_Attendance_Percentage | Final attendance percentage |

This table becomes the **core dataset for further analysis**.

---

# Risk Classification

Students are categorized based on their attendance percentage.

| Attendance Percentage | Category |
|------|------|
| ≥ 75% | Safe |
| 50% – 74% | Warning |
| < 50% | Critical |

Purpose:

- Identify students needing academic attention
- Provide actionable insights for instructors

---

# Performance Score

A normalized **performance score** is calculated using attendance percentage.

performance_score = Net_Attendance_Percentage/100


This allows:

- Easy comparison between students
- Scoring-based analytics

---

# Analytical Insights Generated

The notebook produces several useful insights:

### Student Attendance Ranking
Identifies students with highest and lowest attendance.

### Attendance Distribution
Shows how attendance percentages are distributed among students.

### Risk Identification
Detects students in the **Critical attendance category**.

### Batch-wise Performance
Compares attendance behavior between batches.

---

# Output Tables Generated

The final important datasets created are:

### Student Analytics Table

Contains full student performance metrics.

### Critical Students Table

List of students with **very low attendance** requiring attention.

---

# Purpose of this Analysis

This analysis serves as the **foundation for advanced applications**, including:

- Attendance dashboards
- Automated attendance analytics
- Student early-warning systems
- Academic monitoring tools

Future systems can directly use the generated **student analytics tables** for visualization and reporting.