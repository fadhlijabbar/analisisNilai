import mysql.connector
import bcrypt

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi"
)
cursor = db.cursor()

def loginAkun(username: str, password: str) -> bool:

    db.connect()
    
    query = "SELECT username, password FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user:
        stored_password = user[1].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True

    return False

db.commit()
db.close()

