import pandas as pd
from dataAccessLayer.report_dal import fetch_all_sessions

def generate_report():
    """
    Fetches all sessions and returns a summary table grouped by PatientID.
    Returns a list of dicts with PatientID, number_of_session, and total_duration.
    Raises exceptions on error.
    """
    sessions = fetch_all_sessions()
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
