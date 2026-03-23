# 🏢 Employee Management System

A desktop-based Employee Management System built with **Python (Tkinter)** and **MySQL**.

---

## 📋 Features

- 🔐 **Login** — Secure employee login with username & password
- 📝 **Register** — Add new employees with full details
- 👥 **View All Employees** — Browse all employee records in a table
- 🔍 **Search Employee** — Search by Employee ID or Name
- ✏️ **Update Employee** — Edit employee details by ID
- 🗑️ **Delete Employee** — Remove an employee with confirmation prompt

---

## 🛠️ Requirements

- Python 3.x
- MySQL Server
- Required Python packages:
  ```
  pip install mysql-connector-python
  ```

---

## 🗄️ Database Setup

1. Open MySQL and create the database:
   ```sql
   CREATE DATABASE employee_db;
   USE employee_db;
   ```

2. Create the `employees` table:
   ```sql
   CREATE TABLE employees (
       Employee_ID     VARCHAR(20) PRIMARY KEY,
       usrename        VARCHAR(50),
       Emp_Name        VARCHAR(100),
       Emp_Age         INT,
       Emp_Gender      VARCHAR(10),
       Emp_DOB         DATE,
       Emp_Address     VARCHAR(200),
       Emp_Blood       VARCHAR(5),
       Emp_PhoneNo     VARCHAR(15),
       Emp_Salary      DECIMAL(10,2),
       Emp_EMGNo       VARCHAR(15),
       Emp_Account     VARCHAR(20),
       Emp_AadharCard  VARCHAR(12),
       Emp_PanCard     VARCHAR(10),
       password        VARCHAR(100),
       EMP_DOJ         DATE
   );
   ```

---

## ▶️ How to Run

1. Make sure MySQL server is running.
2. Update the database credentials in the script if needed:
   ```python
   conn = mysql.connect(
       host="localhost",
       user="root",
       password="",       # your MySQL password
       database="employee_db",
       port=3306
   )
   ```
3. Run the application:
   ```
   python employee_management.py
   ```

---

## 📁 Project Structure

```
employee_management.py   # Main application file
README.md                # Project documentation
```

---

## 📌 Notes

- The `usrename` column name is kept as-is to match the existing database schema.
- Passwords are stored as plain text. For production use, consider hashing passwords with `bcrypt`.
- Date fields should be entered in `YYYY-MM-DD` format.

---

## 👨‍💻 Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3   | Core language |
| Tkinter    | GUI framework |
| MySQL      | Database |
| mysql-connector-python | DB connection |
