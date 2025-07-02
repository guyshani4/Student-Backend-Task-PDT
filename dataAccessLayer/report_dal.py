from models.db_connection import DBConnection

def fetch_all_sessions():
    db = DBConnection()
    return db.execute("SELECT PatientID, StartDate, EndDate FROM Sessions", fetchall=True) 