import requests
import sys
import os
import json


# the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from models.db_connection import DBConnection
BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_setup_session_valid():

    db = DBConnection()
    db.execute("INSERT OR IGNORE INTO Patients (FirstName, LastName, ID, DateOfBirth, Gender, MedicalHistory, HomeAddress, InterfaceLanguage) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               ("Test", "Patient", 123456789, "1990-01-01", "male", "None", "123 Main St", "EN"), commit=True)
    db.execute("INSERT OR IGNORE INTO Users (UserName, CreatedDate, FirstName, LastName, PhoneNumber, HomeAddress, ID, Email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               ("therapistuser", "2023-01-01", "Therapist", "User", "1234567890", "Therapist Address", 987654321, "therapist@example.com"), commit=True)

    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/setup-session",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "PatientID": 123456789,
            "StartDate": "2024-01-01",
            "EndDate": "2024-01-10",
            "Summary": "First session",
            "TherapistID": 987654321
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 200