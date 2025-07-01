from flask import Blueprint, jsonify
import re
from models.db_connection import DBConnection
import pandas as pd

# This route should return a summary table for all patients using the pandas library.
# It should query the database for all sessions and group them by PatientID.
# The result should be a table with the following columns: PatientID | number_of_session | total_duration
# If the query is successful, return the summary table with a 200 status code.
# If any error occurs during processing, return a 500 error with the error message.


create_report_bp = Blueprint('create_report', __name__)

@create_report_bp.route('/api/create-report', methods=['GET'])
def create_report():
    print("DEBUG: create_report route called")
    try:
        db = DBConnection()
        # Fetch all sessions from the database
        sessions = db.execute("SELECT PatientID, StartDate, EndDate FROM Sessions", fetchall=True)
        if not sessions:
            return jsonify([]), 200  # Return empty list if no sessions

        # Convert to DataFrame
        df = pd.DataFrame([dict(row) for row in sessions])

        # Calculate session duration (assuming StartDate and EndDate are in 'YYYY-MM-DD' format)
        df['StartDate'] = pd.to_datetime(df['StartDate'])
        df['EndDate'] = pd.to_datetime(df['EndDate'])
        df['duration'] = (df['EndDate'] - df['StartDate']).dt.days

        # Group by PatientID
        summary = df.groupby('PatientID').agg(
            number_of_session=('PatientID', 'count'),
            total_duration=('duration', 'sum')
        ).reset_index()

        # Convert to list of dicts for JSON response
        result = summary.to_dict(orient='records')
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500