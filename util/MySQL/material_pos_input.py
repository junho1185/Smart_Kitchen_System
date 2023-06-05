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

materials = ["후추", "고춧가루", "설탕", "소금", "참기름", "식초", "맛술", "식용유", "꿀", "간장"]

for i in range(len(materials)):
    query = "INSERT INTO Materials (name, location) VALUES (%s, %s)"
    cursor.execute(query, [materials[i], i])
    mydb.commit()