import requests
import sys
import os
import json

# the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"
def test_add_patient_invalid_date_format():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-patient",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "FirstName": "John",
            "LastName": "Doe",
            "ID": "123456789",
            "DateOfBirth": "01-01-1990",  # Invalid format
            "Gender": "male",
            "MedicalHistory": "None",
            "HomeAddress": "123 Main St",
            "InterfaceLanguage": "EN"
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 400