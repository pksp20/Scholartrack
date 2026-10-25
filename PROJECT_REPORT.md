# ScholarTrack Student Management System

**Mini Project Report**

**Project name:** ScholarTrack  
**Student name:** ____________________  
**Roll number:** ____________________  
**Class:** ____________________  
**Institution:** ____________________  
**Submission date:** ____________________

## 1. Introduction

ScholarTrack is a web application for storing and maintaining student records. It provides a simple interface for staff to add, find, update, and remove student information.

## 2. Aim

To design and develop a web-based Student Management System using HTML, CSS, Python Flask, and SQLite, demonstrating full-stack development and CRUD operations.

## 3. Objectives

- Build a user-friendly interface for student records.
- Add, list, search, update, and delete student details.
- Connect the browser interface to a Flask server and SQLite database.
- Validate required fields, marks, contact numbers, and unique roll numbers.
- Display records and search results dynamically through web requests.

## 4. Tools and technologies

| Layer | Technology | Use |
|---|---|---|
| Front end | HTML, CSS | Forms, tables, layout, responsive styling |
| Back end | Python, Flask | Routes, validation, application logic |
| Database | SQLite | Persistent student record storage |

## 5. Database design

The `students` table contains:

| Field | Type | Rule |
|---|---|---|
| `id` | Integer | Primary key, auto-increment |
| `name` | Text | Required |
| `roll_no` | Text | Required and unique |
| `class_name` | Text | Required |
| `marks` | Real | Required, from 0 to 100 |
| `contact` | Text | Required |
| `created_at` | Timestamp | Set automatically |

## 6. Main functions

1. **Create:** Enter a student's name, roll number, class, marks, and contact number.
2. **Read:** View the student list and dashboard summary.
3. **Search:** Find records by name, roll number, or class.
4. **Update:** Edit a student's saved details.
5. **Delete:** Remove a record after a confirmation prompt.

The system rejects duplicate roll numbers, marks outside the 0–100 range, missing required fields, and invalid contact formats.

## 7. Application flow

The user submits a form in the browser. Flask validates the submitted values, performs the requested operation in SQLite, and returns the updated page. Search terms are sent to the server as query parameters.

## 8. Verification

The application was smoke-checked for its health route, record listing, creation, search, duplicate-roll validation, marks validation, editing, and deletion. All checks passed.

## 9. How to run

Install Python 3.9 or newer, install the dependency with `python -m pip install -r requirements.txt`, then run `python app.py`. Open `http://127.0.0.1:5000` in a browser. See `README.md` for Windows setup steps.

## 10. Conclusion

The project demonstrates how a browser interface, a Flask server, and an SQLite database work together. It supports the basic lifecycle of student records and applies validation to help maintain consistent data.

## 11. Possible future improvements

- Add user login and role-based access.
- Add attendance and subject-wise marks.
- Export records to CSV or PDF.
- Add pagination for larger student lists.
