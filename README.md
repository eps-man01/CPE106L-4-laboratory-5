# Lab Activity 5: Data Modeling and Introduction to SQL
**Course:** CPE106L-4 Software Design Laboratory  

## Description
This activity implements a relational database for a university course enrollment system using SQLite and Python.

## Database Schema
- **students**: Stores basic student information (student_id, name, email, year_level).
- **courses**: Stores available courses (course_id, course_code, course_name, units).
- **enrollments**: Junction table managing course enrollments and grades (enrollment_id, student_id, course_id, grade).

## How to Run
1. Ensure Python 3 is installed.
2. Execute the Python script:
   ```bash
   python3 src/main.py