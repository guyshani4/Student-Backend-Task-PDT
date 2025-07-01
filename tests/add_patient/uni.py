import requests
import sys
import os
# from models import db_connection as DBConnection
# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from models.db_connection import DBConnection
import json

# This file contains example tests for the API endpoints and DB queries for the PDT project.
# In order to run this test, you need the local server running
# You can run it with the command: pytest <filename>.py.

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

# Check if return status code is 200
def test_add_patient():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-patient",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "FirstName": "Tester",
            "LastName": "External",
            "HomeAddress": "100 Test Ave",
            "ID": "203846573",
            "InterfaceLanguage": "en",
            "DateOfBirth": "1990-01-01",
            "Gender": "Male",
            "MedicalHistory": "No known allergies"
        })
    }

    res = requests.post(BASE_URL, json=lambda_event)
    # assert res.status_code == 200 #should be allways 200
    result = res.json()
    statusCode = result.get("statusCode", 0) # your code status code
    assert statusCode == 200 #should be allways 200

