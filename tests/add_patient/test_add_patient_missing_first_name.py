import requests
import sys
import os
import json

# the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_add_patient_missing_first_name():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-patient",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            # "FirstName" is missing
            "LastName": "External",
            "ID": "203846573",
            "DateOfBirth": "1990-01-01",
            "Gender": "male",
            "MedicalHistory": "None",
            "HomeAddress": "100 Test Ave",
            "InterfaceLanguage": "EN"
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)  # Optional: helps with debugging
    assert statusCode == 400