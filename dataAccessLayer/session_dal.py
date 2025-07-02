from models.db_connection import DBConnection

def insert_session(patient_id, start_date, end_date, summary, therapist_id):
    db = DBConnection()
    db.execute(
        """
        INSERT INTO Sessions (PatientID, StartDate, EndDate, Summary, TherapistID)
        VALUES (?, ?, ?, ?, ?)
        """,
        (patient_id, start_date, end_date, summary, therapist_id),
        commit=True
    ) 