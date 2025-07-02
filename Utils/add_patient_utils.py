import re
from models.db_connection import DBConnection

def validate_and_add_patient(data):
    """
    Validates input data and adds a patient to the database if valid.
    Returns a tuple: (success: bool, message: str, code: int)
    """
    required_fields = ['FirstName', 'LastName', 'ID', 'DateOfBirth', 'Gender', 'InterfaceLanguage']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing or empty required field: {field}", 10001

    # Validate FirstName and LastName
    name_pattern = re.compile(r"^[A-Za-z]+$")
    if not name_pattern.match(data['FirstName']):
        return False, "FirstName must contain only letters.", 10002
    if not name_pattern.match(data['LastName']):
        return False, "LastName must contain only letters.", 10002

    # Validate ID
    try:
        patient_id = int(data['ID'])
        if len(str(patient_id)) != 9:
            return False, "ID must be a 9-digit integer.", 10003
    except Exception:
        return False, "ID must be a 9-digit integer.", 10003

    # Validate DateOfBirth
    dob_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not dob_pattern.match(data['DateOfBirth']):
        return False, "DateOfBirth must be in ISO format YYYY-MM-DD.", 10004

    # Validate Gender
    if data['Gender'] not in ['male', 'female', 'other']:
        return False, "Gender must be one of ['male', 'female', 'other'].", 10005

    # Validate InterfaceLanguage
    if not re.match(r"^[A-Za-z]{1,2}$", data['InterfaceLanguage']):
        return False, "InterfaceLanguage must be 1 or 2 letters.", 10006

    # Optional fields
    medical_history = data.get('MedicalHistory', '')
    home_address = data.get('HomeAddress', '')

    # Insert into database using DBConnection (moved from DAL)
    db = DBConnection()
    db.execute(
        """
        INSERT INTO Patients (FirstName, LastName, ID, DateOfBirth, Gender, MedicalHistory, HomeAddress, InterfaceLanguage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data['FirstName'],
            data['LastName'],
            patient_id,
            data['DateOfBirth'],
            data['Gender'],
            medical_history,
            home_address,
            data['InterfaceLanguage']
        ),
        commit=True
    )
    return True, f"Patient: {patient_id} added successfully", 10000
