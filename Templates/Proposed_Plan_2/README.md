## Automated Attendance Generation System (Excel Macro Based)

### Overview

This project implements an automated attendance generation workflow using a macro-enabled Excel workbook (`.xlsm`).

Instead of manually entering attendance rows for each student and lecture, the system separates:

- Lecture metadata entry  
- Student master records  
- Attendance database generation  

The goal is to ensure structured, scalable, and analysis-ready attendance data.

---

## Workbook Structure

### 1️⃣ Students_Master

Stores all registered students.

| PRN | Name | Batch |
|-----|------|-------|
| 2501132001 | Patil Yoksh Laxman | D1 |
| 2501132004 | Satvik Anand | D2 |

---

### 2️⃣ Lecture_List

Teacher adds new lectures here.

| Date | Time | Batch |
|------|------|-------|
| 25-02-2026 | 09:30 | Both |
| 25-02-2026 | 11:45 | D1 |
| 25-02-2026 | 14:30 | D2 |

After adding a lecture, the teacher clicks **“Generate Attendance”**.

---

### 3️⃣ Attendance_Database (Auto-Generated)

This sheet is automatically populated by the macro.

| Date | Time | Batch | PRN | Name | Present |
|------|------|-------|------|------|---------|
| 25-02-2026 | 09:30 | Both | 2501132001 | Patil Yoksh Laxman | 0 |
| 25-02-2026 | 09:30 | Both | 2501132002 | Uttekar Paarth Hanumant | 0 |

- Default value: `0` (Absent)  
- Teacher updates `1` for present students  

Each row represents **one student per lecture**.

---

## Automation Logic

When the button is clicked:

1. New lectures from `Lecture_List` are read.
2. Matching students are fetched from `Students_Master`.
3. Attendance rows are generated in `Attendance_Database`.
4. Duplicate entries are prevented using a unique key:
    Date + Time + Batch + PRN

---

## Design Advantages

- No merged cells  
- No multi-row headers  
- Fully normalized row-wise format  
- Compatible with Pandas and ML workflows  
- Easily scalable for large datasets  
- Separation of metadata and transactional data  

---

## Intended Workflow

1. Add lecture details in `Lecture_List`
2. Click **Generate Attendance**
3. Mark present students in `Attendance_Database`
4. Export for analytics or model training

---

## Future Scope

- Attendance percentage computation  
- Absenteeism trend analysis  
- Predictive modeling  
- Database integration  