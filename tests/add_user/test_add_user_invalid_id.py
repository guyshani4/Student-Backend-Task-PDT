import requests
import sys
import os
import json

# the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_add_user_invalid_id():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-user",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "UserName": "badiduser",
            "CreatedDate": "2023-01-01",
            "FirstName": "Bad",
            "LastName": "ID",
            "PhoneNumber": "1234567890",
            "HomeAddress": "Nowhere",
            "ID": "123",  # Invalid: not 9 digits
            "Email": "badiduser@example.com"
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 400