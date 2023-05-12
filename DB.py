import mysql.connector as conn
import os

class mysqlDB:
    def __init__(self):
        self.mydb = conn.connect(
            host="localhost",
            user="root",
            password=os.environ.get("MYSQL_PASSWORD"),
            database="Smart_Kitchen_System"
        )
        self.cursor = self.mydb.cursor()

    def getID(self, foodName):
        query = "SELECT ID FROM RecipeIndex WHERE foodName=%s"
        self.cursor.execute(query, [foodName])
        fetchResult = self.cursor.fetchall()
        return fetchResult[0][0]

    def getFoodNames(self, region):
        query = "SELECT foodName FROM RecipeIndex WHERE region=%d"
        self.cursor.execute(query, [region])
        fetchResult = self.cursor.fetchall()
        foodNames = list(fetchResult[0])
        return foodNames