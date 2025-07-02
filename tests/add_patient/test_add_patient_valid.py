import requests
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"


def test_add_patient_valid():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-patient",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "FirstName": "Alice",
            "LastName": "Wonder",
            "ID": "111222333",
            "DateOfBirth": "1985-05-15",
            "Gender": "female",
            "MedicalHistory": "Asthma",
            "HomeAddress": "789 Main St",
            "InterfaceLanguage": "EN"
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 200