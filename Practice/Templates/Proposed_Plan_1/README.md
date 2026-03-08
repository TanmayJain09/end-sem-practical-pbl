## Proposed Attendance Data Format

To ensure scalability, analytical consistency, and machine-readability, the attendance system follows a normalized row-wise structure.

Each row represents **one student’s attendance for one lecture**.

### Schema

| Column      | Description |
|------------|------------|
| Date        | Lecture date (YYYY-MM-DD recommended) |
| Time        | Lecture start time (24-hour format) |
| Batch       | `D1`, `D2`, or `Both` |
| PRN         | Unique student identifier |
| Name        | Full name of student |
| Attendance  | `1 = Present`, `0 = Absent` |

### Example

| Date       | Time  | Batch | PRN        | Name                    | Attendance |
|------------|-------|-------|------------|--------------------------|------------|
| 25-02-2026 | 13:30 | Both  | 2501132001 | Patil Yoksh Laxman      | 1 |
| 25-02-2026 | 13:30 | Both  | 2501132002 | Uttekar Paarth Hanumant | 1 |
| 25-02-2026 | 13:30 | Both  | 2501132003 | Gupta Aastha Vijay      | 0 |
| 25-02-2026 | 14:30 | D1    | 2501132001 | Patil Yoksh Laxman      | 1 |
| 25-02-2026 | 14:30 | D1    | 2501132002 | Uttekar Paarth Hanumant | 0 |
| 26-02-2026 | 09:30 | D2    | 2501132004 | Satvik Anand            | 1 |

### Rationale

- No merged cells  
- No multi-row headers  
- No structurally empty columns  
- Fully compatible with Pandas and database systems  
- Suitable for analytics and ML pipelines  