import mysql.connector
import bcrypt

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi"
)
cursor = db.cursor()

def daftarAkun(username: str, password: str):
    db.connect()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    check_query = "SELECT COUNT(*) FROM user WHERE username = %s"
    cursor.execute(check_query, (username,))
    result = cursor.fetchone()

    if result[0] > 0:
        return "Username sudah terdaftar"

    register_query = "INSERT INTO user (username, password) VALUES (%s, %s)"
    cursor.execute(register_query, (username, hashed_password.decode('utf-8')))
    db.commit()

    db.close()
