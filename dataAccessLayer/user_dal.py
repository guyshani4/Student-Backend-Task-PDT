from models.db_connection import DBConnection

def insert_user(user_name, created_date, first_name, last_name, phone_number, home_address, user_id, email):
    db = DBConnection()
    db.execute(
        """
        INSERT INTO Users (UserName, CreatedDate, FirstName, LastName, PhoneNumber, HomeAddress, ID, Email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user_name, created_date, first_name, last_name, phone_number, home_address, user_id, email),
        commit=True
    ) 