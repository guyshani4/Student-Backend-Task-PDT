import requests
import sys
import os
import json
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.db_connection import DBConnection

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_create_report_total_duration():
    # Add patient and therapist
    db = DBConnection()
    patient_id = 555555555
    therapist_id = 999999999

    db.execute("INSERT OR IGNORE INTO Patients (FirstName, LastName, ID, DateOfBirth, Gender, MedicalHistory, HomeAddress, InterfaceLanguage) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               ("Report", "Patient", patient_id, "1980-01-01", "male", "None", "Report Address", "EN"), commit=True)
    db.execute("INSERT OR IGNORE INTO Users (UserName, CreatedDate, FirstName, LastName, PhoneNumber, HomeAddress, ID, Email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               ("reporttherapist", "2023-01-01", "Report", "Therapist", "1234567890", "Therapist Address", therapist_id, "reporttherapist@example.com"), commit=True)

    # Clean up any previous sessions for this patient
    db.execute("DELETE FROM Sessions WHERE PatientID = ?", (patient_id,), commit=True)

    # Add 3 sessions with different durations
    sessions = [
        ("2024-01-01", "2024-01-05"),  # 4 days
        ("2024-02-01", "2024-02-04"),  # 3 days
        ("2024-03-01", "2024-03-10"),  # 9 days
    ]
    for start, end in sessions:
        db.execute(
            "INSERT INTO Sessions (PatientID, StartDate, EndDate, Summary, TherapistID) VALUES (?, ?, ?, ?, ?)",
            (patient_id, start, end, "Session", therapist_id),
            commit=True
        )

    # Calculate expected total duration
    total_duration = sum(
        (datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days
        for start, end in sessions
    )

    # Call the create_report endpoint
    lambda_event = {
        "httpMethod": "GET",
        "path": "/api/create-report",
        "headers": {"Content-Type": "application/json"}
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 200

    body = json.loads(result.get("body", "{}"))
    assert isinstance(body, dict)
    assert "data" in body
    assert isinstance(body["data"], list)

    patient_report = next((row for row in body["data"] if row["PatientID"] == patient_id), None)
    assert patient_report is not None
    assert patient_report["total_duration"] == total_duration
    assert patient_report["number_of_session"] == 3
