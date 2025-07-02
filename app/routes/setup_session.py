from flask import Blueprint, jsonify, request
import re, logging
import json
from models.db_connection import DBConnection

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
        # Parse Lambda event or standard Flask request
        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                event = request.get_json(force=True)
                if isinstance(event, dict) and "body" in event:
                    data = json.loads(event["body"])
            except Exception:
                data = {}

        required_fields = ['PatientID', 'StartDate', 'EndDate', 'TherapistID']
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                logger.error("Missing or empty required field in setup_session: %s", field)
                return jsonify({"message": f"Missing or empty required field: {field}"}), 400

        # Extract IDs
        patient_id = data['PatientID']
        therapist_id = data['TherapistID']

        # Validate StartDate and EndDate (ISO format)
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(data['StartDate']):
            return jsonify({"message": "StartDate must be in ISO format YYYY-MM-DD."}), 400
        if not date_pattern.match(data['EndDate']):
            return jsonify({"message": "EndDate must be in ISO format YYYY-MM-DD."}), 400

        # Check PatientID exists
        db = DBConnection()
        patient = db.execute("SELECT 1 FROM Patients WHERE ID = ?", (patient_id,), fetchone=True)
        if not patient:
            return jsonify({"message": "PatientID does not exist."}), 400

        # Check TherapistID exists
        therapist = db.execute("SELECT 1 FROM Users WHERE ID = ?", (therapist_id,), fetchone=True)
        if not therapist:
            return jsonify({"message": "TherapistID does not exist."}), 400

        # Optional field
        summary = data.get('Summary', '')

        # Insert into Sessions table
        db.execute("""
            INSERT INTO Sessions (PatientID, StartDate, EndDate, Summary, TherapistID)
            VALUES (?, ?, ?, ?, ?)
        """, (
            patient_id,
            data['StartDate'],
            data['EndDate'],
            summary,
            therapist_id
        ), commit=True)
        logger.info("Session added successfully: PatientID=%s, TherapistID=%s, StartDate=%s, EndDate=%s", patient_id, therapist_id, data['StartDate'], data['EndDate'])
        return jsonify({"message": "Session added successfully."}), 200

    except Exception as e:
        patient_id = data.get('PatientID', 'unknown') if 'data' in locals() and isinstance(data, dict) else 'unknown'
        logger.error("Error in setup_session for PatientID %s: %s", patient_id, str(e))
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500