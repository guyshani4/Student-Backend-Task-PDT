from flask import Blueprint, jsonify, request
import logging
import json
from Utils.setup_session_utils import validate_and_add_session

# Custom Status Codes:
# 30000 - Success: Session added
# 30001 - Missing or empty required field
# 30002 - Invalid StartDate/EndDate
# 30003 - PatientID does not exist
# 30004 - TherapistID does not exist
# 30999 - Internal server error

# This route is intended to add a new session to the database.
# It expects the following parameters (with validation):
# - PatientID (int, required validation - must be a valid integer and exist in the Patients table)
# - StartDate (str, required validation - must be in ISO format, e.g., YYYY-MM-DD)
# - EndDate (str, required validation - must be in ISO format, e.g., YYYY-MM-DD)
# - Summary (str, no validation)
# - TherapistID (int, required validation - must be a valid integer and exist in the Users table)
# # The Parameters will be formatted as JSON in the request body.
# The route must return an appropriate message for each specific failure or success.
# If validation fails, return 400 status. If successful, return 200 status.


setup_session_bp = Blueprint('setup_session', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@setup_session_bp.route('/api/setup-session', methods=['POST'])
def setup_session():
    try:
        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                event = request.get_json(force=True)
                if isinstance(event, dict) and "body" in event:
                    data = json.loads(event["body"])
            except Exception:
                data = {}

        success, message, code = validate_and_add_session(data)
        if not success:
            logger.error("setup_session failed: %s", message)
            return jsonify({"message": message, "customCode": code}), 400
        logger.info(message)
        return jsonify({"message": "Session added successfully.", "customCode": code}), 200

    except Exception as e:
        patient_id = data.get('PatientID', 'unknown') if 'data' in locals() and isinstance(data, dict) else 'unknown'
        logger.error("Error in setup_session for PatientID %s: %s", patient_id, str(e))
        return jsonify({"message": f"An error occurred: {str(e)}", "customCode": 30999}), 500