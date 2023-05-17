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
        query = "SELECT foodName FROM RecipeIndex WHERE region=%s"
        self.cursor.execute(query, [region])
        fetchResult = self.cursor.fetchall()
        foodNames = []

        for i in range(len(fetchResult)):
            foodNames.append(fetchResult[i][0])
        return foodNames

    def getFoodName(self, foodID):
        query = "SELECT foodName FROM RecipeIndex WHERE id = %s"
        self.cursor.execute(query, [foodID])
        fetchResult = self.cursor.fetchall()
        foodName = fetchResult[0][0]

        return foodName

    def getRecipe(self, foodID):
        query = "SELECT recipe FROM RecipeSteps WHERE foodID = %s"
        self.cursor.execute(query, [foodID])
        fetchResult = self.cursor.fetchall()
        recipe = []

        for i in range(len(fetchResult)):
            recipe.append(fetchResult[i][0])

        return recipe

    def close(self):
        self.mydb.close()