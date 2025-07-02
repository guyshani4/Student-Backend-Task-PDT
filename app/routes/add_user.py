from flask import Blueprint, request, jsonify
import logging
import json
from Utils.add_user_utils import validate_and_add_user
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

# Custom Status Codes:
# 20000 - Success: User added
# 20001 - Missing or empty required field
# 20002 - Invalid UserName/FirstName/LastName
# 20003 - Invalid CreatedDate
# 20004 - Invalid PhoneNumber
# 20005 - Invalid ID
# 20006 - Invalid Email
# 20999 - Internal server error

add_user_bp = Blueprint('add_user', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@add_user_bp.route('/api/add-user', methods=['POST'])
def add_user():
    try:
        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                event = request.get_json(force=True)
                if isinstance(event, dict) and "body" in event:
                    data = json.loads(event["body"])
            except Exception:
                data = {}
        print("DEBUG DATA:", data)
        success, message, code = validate_and_add_user(data)
        if not success:
            logger.error("add_user failed: %s", message)
            return jsonify({"message": message, "customCode": code}), 400
        logger.info(message)
        return jsonify({"message": "User added successfully.", "customCode": code}), 200

    except Exception as e:
        user_id = data.get('ID', 'unknown') if 'data' in locals() and isinstance(data, dict) else 'unknown'
        logger.error("Error in add_user %s: %s", user_id, str(e))
        return jsonify({"message": f"An error occurred: {str(e)}", "customCode": 20999}), 500