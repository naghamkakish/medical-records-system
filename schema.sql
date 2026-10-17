-- Medical Records & Cross-Specialty System Schema

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Patients Table
CREATE TABLE IF NOT EXISTS "patients" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "full_name" TEXT NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "gender" TEXT NOT NULL,
    "phone_number" TEXT NOT NULL,
    "blood_type" TEXT
);

-- Doctors Table
CREATE TABLE IF NOT EXISTS "doctors" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "full_name" TEXT NOT NULL,
    "specialty" TEXT NOT NULL,
    "phone_number" TEXT NOT NULL,
    "email" TEXT NOT NULL
);

-- Encounters (Visits) Table - Junction between Patients and Doctors
CREATE TABLE IF NOT EXISTS "encounters" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "patient_id" INTEGER NOT NULL,
    "doctor_id" INTEGER NOT NULL,
    "visit_date" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "diagnosis" TEXT NOT NULL,
    "clinical_notes" TEXT,
    FOREIGN KEY ("patient_id") REFERENCES "patients"("id") ON DELETE CASCADE,
    FOREIGN KEY ("doctor_id") REFERENCES "doctors"("id") ON DELETE CASCADE
);

-- Prescriptions Table - One-to-Many with Encounters
CREATE TABLE IF NOT EXISTS "prescriptions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "encounter_id" INTEGER NOT NULL,
    "medication_name" TEXT NOT NULL,
    "dosage" TEXT NOT NULL,
    "instructions" TEXT NOT NULL,
    FOREIGN KEY ("encounter_id") REFERENCES "encounters"("id") ON DELETE CASCADE
);

-- Cross-Specialty Referrals Table
CREATE TABLE IF NOT EXISTS "referrals" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "encounter_id" INTEGER NOT NULL,
    "referred_to_specialty" TEXT NOT NULL,
    "reason" TEXT NOT NULL,
    "status" TEXT DEFAULT 'Pending',
    FOREIGN KEY ("encounter_id") REFERENCES "encounters"("id") ON DELETE CASCADE
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS "idx_encounters_patient" ON "encounters"("patient_id");
CREATE INDEX IF NOT EXISTS "idx_encounters_doctor" ON "encounters"("doctor_id");
CREATE INDEX IF NOT EXISTS "idx_prescriptions_encounter" ON "prescriptions"("encounter_id");

-- Custom SQL View: Complete Patient Medical History Summary
CREATE VIEW IF NOT EXISTS "patient_medical_summary" AS
SELECT
    p.id AS patient_id,
    p.full_name AS patient_name,
    d.full_name AS attending_doctor,
    d.specialty AS doctor_specialty,
    e.visit_date,
    e.diagnosis,
    pr.medication_name,
    pr.dosage
FROM patients p
JOIN encounters e ON p.id = e.patient_id
JOIN doctors d ON e.doctor_id = d.id
LEFT JOIN prescriptions pr ON e.id = pr.encounter_id;
