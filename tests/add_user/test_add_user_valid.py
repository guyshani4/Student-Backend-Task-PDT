import requests
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_add_user_valid():
    lambda_event = {
        "httpMethod": "POST",
        "path": "/api/add-user",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "UserName": "validuser",
            "CreatedDate": "2023-01-01",
            "FirstName": "Valid",
            "LastName": "User",
            "PhoneNumber": "1234567890",
            "HomeAddress": "123 Valid St",
            "ID": "987654321",
            "Email": "validuser@example.com"
        })
    }
    res = requests.post(BASE_URL, json=lambda_event)
    result = res.json()
    statusCode = result.get("statusCode", 0)
    print(result)
    assert statusCode == 200