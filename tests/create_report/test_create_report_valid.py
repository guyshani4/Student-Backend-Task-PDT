import requests
import sys
import os
import json

# the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

BASE_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"

def test_create_report_valid():
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

    # Check that the body is a dict with a 'data' key containing a list
    body = json.loads(result.get("body", "{}"))
    assert isinstance(body, dict)
    assert "data" in body
    assert isinstance(body["data"], list)
