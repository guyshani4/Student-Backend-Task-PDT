from flask import Blueprint, request, jsonify
import re, logging
from models.db_connection import DBConnection
import json
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


add_patient_bp = Blueprint('add_patient', __name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@add_patient_bp.route('/api/add-patient', methods=['POST'])
def add_patient():
    try:
        #data = request.get_json()

        # Try to get data as usual
        data = request.get_json(silent=True)
        # If data is None, try to parse Lambda event format
        if data is None and request.data:
            try:
                event = request.get_json(force=True)
                if isinstance(event, dict) and "body" in event:
                    data = json.loads(event["body"])
            except Exception:
                data = {}


        # Required fields
        required_fields = ['FirstName', 'LastName', 'ID', 'DateOfBirth', 'Gender', 'InterfaceLanguage']
        for field in required_fields:
            if field not in data or not data[field]:
                logger.error("Missing or empty required field in add_patient: %s", field)
                return jsonify({"message": f"Missing or empty required field: {field}"}), 400

        # Validate FirstName and LastName 
        name_pattern = re.compile(r"^[A-Za-z]+$")
        if not name_pattern.match(data['FirstName']):
            return jsonify({"message": "FirstName must contain only letters."}), 400
        if not name_pattern.match(data['LastName']):
            return jsonify({"message": "LastName must contain only letters."}), 400

        # Validate ID 
        try:
            patient_id = int(data['ID'])
            if len(str(patient_id)) != 9:
                return jsonify({"message": "ID must be a 9-digit integer."}), 400
        except Exception:
            return jsonify({"message": "ID must be a 9-digit integer."}), 400

         # Validate DateOfBirth 
        dob_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not dob_pattern.match(data['DateOfBirth']):
            return jsonify({"message": "DateOfBirth must be in ISO format YYYY-MM-DD."}), 400
        
        # Validate Gender
        if data['Gender'] not in ['male', 'female', 'other']:
            return jsonify({"message": "Gender must be one of ['male', 'female', 'other']."}), 400

        # Validate InterfaceLanguage 
        if not re.match(r"^[A-Za-z]{1,2}$", data['InterfaceLanguage']):
            return jsonify({"message": "InterfaceLanguage must be 1 or 2 letters."}), 400

        # Optional fields
        medical_history = data.get('MedicalHistory', '')
        home_address = data.get('HomeAddress', '')

        # Insert into database using DBConnection
        db = DBConnection()
        db.execute("""
            INSERT INTO Patients (FirstName, LastName, ID, DateOfBirth, Gender, MedicalHistory, HomeAddress, InterfaceLanguage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['FirstName'],
            data['LastName'],
            patient_id,
            data['DateOfBirth'],
            data['Gender'],
            medical_history,
            home_address,
            data['InterfaceLanguage']
        ), commit=True)
        logger.info("Patient: %s added successfully", patient_id)
        return jsonify({"message": "User added successfully."}), 200

    except Exception as e:
        # Try to log the patient ID if available
        patient_id = data.get('ID', 'unknown') if 'data' in locals() and isinstance(data, dict) else 'unknown'
        logger.error("Error in add_patient %s: %s", patient_id, str(e))
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500