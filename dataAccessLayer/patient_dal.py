from models.db_connection import DBConnection

def insert_patient(first_name, last_name, patient_id, dob, gender, medical_history, home_address, interface_language):
    db = DBConnection()
    db.execute(
        """
        INSERT INTO Patients (FirstName, LastName, ID, DateOfBirth, Gender, MedicalHistory, HomeAddress, InterfaceLanguage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (first_name, last_name, patient_id, dob, gender, medical_history, home_address, interface_language),
        commit=True
    ) 