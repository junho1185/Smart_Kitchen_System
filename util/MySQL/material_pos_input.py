import mysql.connector as conn
import os

mydb = conn.connect(
    host="localhost",
    user="root",
    password=os.environ.get("MYSQL_PASSWORD"),
    database="Smart_Kitchen_System"
)

cursor = mydb.cursor()

query = 'DELETE FROM Materials'
cursor.execute(query)
mydb.commit()

materials = ["간장", "참기름", "설탕", "소금", "후추", "식용유", "맛술", "꿀", "식초", "고춧가루"]

for i in range(len(materials)):
    query = "INSERT INTO Materials (name, location) VALUES (%s, %s)"
    cursor.execute(query, [materials[i], i])
    mydb.commit()