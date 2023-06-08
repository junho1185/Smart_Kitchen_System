import mysql.connector as conn
import os

mydb = conn.connect(
    host="localhost",
    user="root",
    password=os.environ.get("MYSQL_PASSWORD"),
    database="Smart_Kitchen_System"
)

cursor = mydb.cursor()

query = "DELETE FROM RecipeSteps"
cursor.execute(query)
mydb.commit()

query = "DELETE FROM RecipeIndex"
cursor.execute(query)
mydb.commit()

