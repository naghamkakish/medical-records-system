# Medical Records & Cross-Specialty Management System

A robust, relational backend and Python application designed to manage patient health records, clinical encounters, prescriptions, and cross-specialty doctor referrals. Built with **Python 3** and **SQLite**, this project demonstrates advanced relational database design, data integrity enforcement, transaction safety, and programmatic interaction via Python.

---

## 🚀 Key Features

- **Normalized Relational Schema**: Enforces data integrity across multiple interconnected entities up to Third Normal Form (3NF).
- **Cross-Specialty Referrals & Prescriptions**: Tracks multi-departmental care workflows, linking primary visits to specialized consultations and medical prescriptions.
- **Transactional Safety**: Utilizes automated rollback mechanisms in Python to prevent partial or corrupted database writes.
- **Custom SQL Views**: Pre-aggregates complex multi-table joins (`patients`, `encounters`, `doctors`, `prescriptions`) into a unified reporting view (`patient_medical_summary`).
- **Performance Optimization**: Includes targeted indexes on foreign keys and frequently queried columns to optimize lookup speeds.
- **Parameterized Queries**: Built with strict input parameterization to protect against SQL injection vulnerabilities.

---

## 🛠️ Technology Stack

- **Language:** Python 3 (`sqlite3` standard library)
- **Database:** SQLite 3
- **Design Concepts:** Foreign Key Constraints, Cascading Deletes, Database Views, Indexing, ACID Transactions

---

## 📁 Project Architecture

```text
medical-records-system/
│
├── schema.sql         # Database definition, tables, indexes, and custom views
│
├── app.py             # Python script handling initialization, CRUD, and business logic
│
└── README.md          # Project documentation
