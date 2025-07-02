import re
from dataAccessLayer.session_dal import insert_session
from models.db_connection import DBConnection

def validate_and_add_session(data):
    """
    Validates input data and adds a session to the database if valid.
    Returns a tuple: (success: bool, message: str)
    """
    required_fields = ['PatientID', 'StartDate', 'EndDate', 'TherapistID']
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            return False, f"Missing or empty required field: {field}"

    patient_id = data['PatientID']
    therapist_id = data['TherapistID']

    # Validate StartDate and EndDate (ISO format)
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not date_pattern.match(data['StartDate']):
        return False, "StartDate must be in ISO format YYYY-MM-DD."
    if not date_pattern.match(data['EndDate']):
        return False, "EndDate must be in ISO format YYYY-MM-DD."

    # Check PatientID exists
    db = DBConnection()
    patient = db.execute("SELECT 1 FROM Patients WHERE ID = ?", (patient_id,), fetchone=True)
    if not patient:
        return False, "PatientID does not exist."

    # Check TherapistID exists
    therapist = db.execute("SELECT 1 FROM Users WHERE ID = ?", (therapist_id,), fetchone=True)
    if not therapist:
        return False, "TherapistID does not exist."

    # Optional field
    summary = data.get('Summary', '')

    # Insert into Sessions table using DAL
    insert_session(
        patient_id,
        data['StartDate'],
        data['EndDate'],
        summary,
        therapist_id
    )
    return True, f"Session added successfully: PatientID={patient_id}, TherapistID={therapist_id}, StartDate={data['StartDate']}, EndDate={data['EndDate']}"
