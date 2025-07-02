import pandas as pd
from models.db_connection import DBConnection

def generate_report():
    """
    Fetches all sessions and returns a summary table grouped by PatientID.
    Returns a list of dicts with PatientID, number_of_session, and total_duration.
    Raises exceptions on error.
    """
    db = DBConnection()
    sessions = db.execute("SELECT PatientID, StartDate, EndDate FROM Sessions", fetchall=True)
    if not sessions:
        return []
    df = pd.DataFrame([dict(row) for row in sessions])
    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df['duration'] = (df['EndDate'] - df['StartDate']).dt.days
    summary = df.groupby('PatientID').agg(
        number_of_session=('PatientID', 'count'),
        total_duration=('duration', 'sum')
    ).reset_index()
    return summary.to_dict(orient='records')
