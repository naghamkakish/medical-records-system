import sqlite3
import os

DB_FILE = "medical_system.db"

def initialize_database():
    """Initializes the SQLite database and executes schema.sql."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    if os.path.exists("schema.sql"):
        with open("schema.sql", "r") as f:
            cursor.executescript(f.read())
        print("[INFO] Database schema successfully loaded from schema.sql!")
    else:
        print("[ERROR] schema.sql file not found.")

    conn.commit()
    conn.close()

def add_patient(full_name, dob, gender, phone, blood_type):
    """Inserts a new patient into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (full_name, date_of_birth, gender, phone_number, blood_type)
        VALUES (?, ?, ?, ?, ?)
    """, (full_name, dob, gender, phone, blood_type))
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    print(f"[SUCCESS] Added patient '{full_name}' with ID: {patient_id}")
    return patient_id

def add_doctor(full_name, specialty, phone, email):
    """Inserts a new doctor into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctors (full_name, specialty, phone_number, email)
        VALUES (?, ?, ?, ?)
    """, (full_name, specialty, phone, email))
    conn.commit()
    doctor_id = cursor.lastrowid
    conn.close()
    print(f"[SUCCESS] Added doctor 'Dr. {full_name}' ({specialty}) with ID: {doctor_id}")
    return doctor_id

def record_encounter(patient_id, doctor_id, diagnosis, notes, medications=None, referral_spec=None):
    """Records a patient visit along with optional prescriptions and cross-specialty referrals securely."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        cursor.execute("""
            INSERT INTO encounters (patient_id, doctor_id, diagnosis, clinical_notes)
            VALUES (?, ?, ?, ?)
        """, (patient_id, doctor_id, diagnosis, notes))
        encounter_id = cursor.lastrowid

        if medications:
            for med, dosage, instructions in medications:
                cursor.execute("""
                    INSERT INTO prescriptions (encounter_id, medication_name, dosage, instructions)
                    VALUES (?, ?, ?, ?)
                """, (encounter_id, med, dosage, instructions))

        if referral_spec:
            cursor.execute("""
                INSERT INTO referrals (encounter_id, referred_to_specialty, reason, status)
                VALUES (?, ?, ?, 'Pending')
            """, (encounter_id, referral_spec, f"Referred from encounter #{encounter_id} for specialist review."))

        conn.commit()
        print(f"[SUCCESS] Recorded encounter ID {encounter_id} successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[ERROR] Transaction failed: {e}")
    finally:
        conn.close()

def view_patient_summary(patient_id):
    """Queries the custom SQL view to display a patient's complete history."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT visit_date, attending_doctor, doctor_specialty, diagnosis, medication_name, dosage
        FROM patient_medical_summary
        WHERE patient_id = ?
    """, (patient_id,))

    records = cursor.fetchall()
    conn.close()
    return records

if __name__ == "__main__":
    initialize_database()

    p_id = add_patient("Sara Zaid", "1994-06-15", "Female", "+962798887766", "A+")
    d_id = add_doctor("Rami Haddad", "Cardiology", "+962781112233", "rami.haddad@clinic.jo")

    meds = [("Lisinopril", "10mg", "Take once daily in the morning")]
    record_encounter(
        patient_id=p_id,
        doctor_id=d_id,
        diagnosis="Stage 1 Hypertension",
        notes="Patient reports occasional dizziness.",
        medications=meds,
        referral_spec="Endocrinology"
    )

    print("\n--- Patient Medical Summary Report ---")
    summary = view_patient_summary(p_id)
    for row in summary:
        print(f"Date: {row[0]} | Doctor: {row[1]} ({row[2]})")
        print(f"Diagnosis: {row[3]}")
        print(f"Prescription: {row[4]} - {row[5]}")
        print("-" * 40)
