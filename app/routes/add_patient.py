from flask import Blueprint, request, jsonify
import logging
import json
from Utils.add_patient_utils import validate_and_add_patient
# This route is intended to add a new patient to the database.
# It expects the following parameters (with validation):
# - FirstName (str, required validation - no digits, no special characters)
# - LastName (str, required validation - no digits, no special characters)
# - ID (int, required validation - must be a valid integer with 9 digits)
# - DateOfBirth (str, required validation - must be in ISO format, e.g., YYYY-MM-DD)
# - Gender (str, required validation - must be in one of ['male', female', 'other'])
# - MedicalHistory (str, no validation)
# - HomeAddress (str,  no validation)
# - InterfaceLanguage (str, required validation - 2 letters max)
# The Parameters will be formatted as JSON in the request body.
# The route must return an appropriate message for each specific failure or success.
# If validation fails, return 400 status. If successful, return 200 status.

# Custom Status Codes:
# 10000 - Success: Patient added
# 10001 - Missing or empty required field
# 10002 - Invalid FirstName/LastName
# 10003 - Invalid ID
# 10004 - Invalid DateOfBirth
# 10005 - Invalid Gender
# 10006 - Invalid InterfaceLanguage
# 10999 - Internal server error

add_patient_bp = Blueprint('add_patient', __name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@add_patient_bp.route('/api/add-patient', methods=['POST'])
def add_patient():
    try:
        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                event = request.get_json(force=True)
                if isinstance(event, dict) and "body" in event:
                    data = json.loads(event["body"])
            except Exception:
                data = {}

        success, message, code = validate_and_add_patient(data)
        if not success:
            logger.error("add_patient failed: %s", message)
            return jsonify({"message": message, "customCode": code}), 400
        logger.info(message)
        return jsonify({"message": "User added successfully.", "customCode": code}), 200

    except Exception as e:
        patient_id = data.get('ID', 'unknown') if 'data' in locals() and isinstance(data, dict) else 'unknown'
        logger.error("Error in add_patient %s: %s", patient_id, str(e))
        return jsonify({"message": f"An error occurred: {str(e)}", "customCode": 10999}), 500