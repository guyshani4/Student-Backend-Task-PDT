from flask import Blueprint, request, jsonify
import re, logging
from models.db_connection import DBConnection
import json
# This route is intended to add a new user to the database.
# It expects the following parameters (with validation):
# - UserName (str, required validation - no digits, no special characters)
# - CreatedDate (str, required validation - must be in ISO format, e.g., YYYY-MM-DD)
# - FirstName (str, required validation - no digits, no special characters)
# - LastName (str, required validation - no digits, no special characters)
# - PhoneNumber (str, required validation - must be a valid phone number format - e.g., 10 digits)
# - HomeAddress (str, no validation)
# - ID (str, required validation - must be a valid identifier, e.g., 9 digits)
# - Email (str, required validation - must be a valid email format)
# # The Parameters will be formatted as JSON in the request body.
# The route must return an appropriate message for each specific failure or success.
# If validation fails, return 400 status. If successful, return 200 status.



add_user_bp = Blueprint('add_user', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@add_user_bp.route('/api/add-user', methods=['POST'])
def add_user():
    try:
        #data = request.get_json()

        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                event = request.get_json(force=True)
                if isinstance(event, dict) and "body" in event:
                    data = json.loads(event["body"])
            except Exception:
                data = {}
        print("DEBUG DATA:", data)
        # Required fields
        required_fields = ['UserName', 'CreatedDate', 'FirstName', 'LastName', 'PhoneNumber', 'ID', 'Email']
        for field in required_fields:
            if field not in data or not data[field]:
                logger.error("Missing or empty required field in add_user: %s", field)
                return jsonify({"message": f"Missing or empty required field: {field}"}), 400

        # Validate UserName, FirstName, LastName
        name_pattern = re.compile(r"^[A-Za-z]+$")
        if not name_pattern.match(data['UserName']):
            return jsonify({"message": "UserName must contain only letters."}), 400
        if not name_pattern.match(data['FirstName']):
            return jsonify({"message": "FirstName must contain only letters."}), 400
        if not name_pattern.match(data['LastName']):
            return jsonify({"message": "LastName must contain only letters."}), 400

        # Validate CreatedDate 
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(data['CreatedDate']):
            return jsonify({"message": "CreatedDate must be in ISO format YYYY-MM-DD."}), 400

        # Validate PhoneNumber 
        if not re.match(r"^\d{10}$", data['PhoneNumber']):
            return jsonify({"message": "PhoneNumber must be a valid 10-digit number."}), 400

        # Validate ID 
        if not re.match(r"^\d{9}$", data['ID']):
            return jsonify({"message": "ID must be a valid 9-digit identifier."}), 400
        
        # Validate Email 
        email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        if not email_pattern.match(data['Email']):
            return jsonify({"message": "Email must be a valid email address."}), 400

        # Optional field
        home_address = data.get('HomeAddress', '')

        # Insert into database using DBConnection
        db = DBConnection()
        db.execute("""
            INSERT INTO Users (UserName, CreatedDate, FirstName, LastName, PhoneNumber, HomeAddress, ID, Email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['UserName'],
            data['CreatedDate'],
            data['FirstName'],
            data['LastName'],
            data['PhoneNumber'],
            home_address,
            data['ID'],
            data['Email']
        ), commit=True)
        logger.info("User: %s added successfully", data['ID'])
        return jsonify({"message": "User added successfully."}), 200

    except Exception as e:
        # Try to log the user ID if available
        user_id = data.get('ID', 'unknown') if 'data' in locals() and isinstance(data, dict) else 'unknown'
        logger.error("Error in add_user %s: %s", user_id, str(e))
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500