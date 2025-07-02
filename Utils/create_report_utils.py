import pandas as pd
from models.db_connection import DBConnection

def generate_report():
    """
    Fetches all sessions and returns a summary table grouped by PatientID.
    Returns a tuple: (success: bool, result: list, code: int)
    """
    db = DBConnection()
    sessions = db.execute("SELECT PatientID, StartDate, EndDate FROM Sessions", fetchall=True)
    if not sessions:
        return True, [], 40001
    df = pd.DataFrame([dict(row) for row in sessions])
    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df['duration'] = (df['EndDate'] - df['StartDate']).dt.days
    summary = df.groupby('PatientID').agg(
        number_of_session=('PatientID', 'count'),
        total_duration=('duration', 'sum')
    ).reset_index()
    return True, summary.to_dict(orient='records'), 40000
