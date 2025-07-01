import requests
import sys
import os
import json

# the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_add_user_invalid_email():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-user",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "UserName": "bademailuser",
            "CreatedDate": "2023-01-01",
            "FirstName": "Bad",
            "LastName": "Email",
            "PhoneNumber": "1234567890",
            "HomeAddress": "Nowhere",
            "ID": "123456789",
            "Email": "not-an-email"  # Invalid email format
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 400