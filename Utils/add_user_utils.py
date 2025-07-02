import re
from models.db_connection import DBConnection

def validate_and_add_user(data):
    """
    Validates input data and adds a user to the database if valid.
    Returns a tuple: (success: bool, message: str, code: int)
    """
    required_fields = ['UserName', 'CreatedDate', 'FirstName', 'LastName', 'PhoneNumber', 'ID', 'Email']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing or empty required field: {field}", 20001

    # Validate UserName, FirstName, LastName
    name_pattern = re.compile(r"^[A-Za-z]+$")
    if not name_pattern.match(data['UserName']):
        return False, "UserName must contain only letters.", 20002
    if not name_pattern.match(data['FirstName']):
        return False, "FirstName must contain only letters.", 20002
    if not name_pattern.match(data['LastName']):
        return False, "LastName must contain only letters.", 20002

    # Validate CreatedDate
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not date_pattern.match(data['CreatedDate']):
        return False, "CreatedDate must be in ISO format YYYY-MM-DD.", 20003

    # Validate PhoneNumber
    if not re.match(r"^\d{10}$", data['PhoneNumber']):
        return False, "PhoneNumber must be a valid 10-digit number.", 20004

    # Validate ID
    if not re.match(r"^\d{9}$", data['ID']):
        return False, "ID must be a valid 9-digit identifier.", 20005

    # Validate Email
    email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    if not email_pattern.match(data['Email']):
        return False, "Email must be a valid email address.", 20006

    # Optional field
    home_address = data.get('HomeAddress', '')

    # Insert into database using DBConnection (moved from DAL)
    db = DBConnection()
    db.execute(
        """
        INSERT INTO Users (UserName, CreatedDate, FirstName, LastName, PhoneNumber, HomeAddress, ID, Email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data['UserName'],
            data['CreatedDate'],
            data['FirstName'],
            data['LastName'],
            data['PhoneNumber'],
            home_address,
            data['ID'],
            data['Email']
        ),
        commit=True
    )
    return True, f"User: {data['ID']} added successfully", 20000
