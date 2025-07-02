from flask import Blueprint, jsonify
import re, logging
from models.db_connection import DBConnection
import pandas as pd
from Utils.create_report_utils import generate_report

# This route should return a summary table for all patients using the pandas library.
# It should query the database for all sessions and group them by PatientID.
# The result should be a table with the following columns: PatientID | number_of_session | total_duration
# If the query is successful, return the summary table with a 200 status code.
# If any error occurs during processing, return a 500 error with the error message.


create_report_bp = Blueprint('create_report', __name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@create_report_bp.route('/api/create-report', methods=['GET'])
def create_report():
    try:
        result = generate_report()
        return jsonify(result), 200
    except Exception as e:
        logger.error("Failed to create report: %s", str(e))
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500