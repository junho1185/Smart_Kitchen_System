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
        print(fetchResult)
        if(len(fetchResult)):
            return fetchResult[0][0]
        else:
            return None

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

    def getPosition(self, material):
        query = "SELECT location FROM Materials WHERE name = %s"
        self.cursor.execute(query, [material])
        fetchResult = self.cursor.fetchall()

        if len(fetchResult[0]) > 0:
            return int(fetchResult[0][0])
        else:
            return 11

    def getMaterials(self):
        query = "SELECT name FROM Materials"
        self.cursor.execute(query)
        fetchResult = self.cursor.fetchall()

        material_list = []
        for i in range(len(fetchResult)):
            material_list.append(fetchResult[i][0])

        return material_list

    def putRecipe(self, name, region, recipe):
        query = "INSERT INTO RecipeIndex (foodName, region) VALUES (%s, %s)"
        self.cursor.execute(query, (name, region))
        self.mydb.commit()

        recipe = recipe.strip()
        recipes = recipe.split('/')
        stepNum = 1
        foodID = self.getID(name)

        # Showing result of the generated recipe
        print("Generated Recipe")
        for r in recipes:
            print("#", r)

        for r in recipes:
            if len(r) > 1:
                query = "INSERT INTO RecipeSteps (foodID, stepNum, recipe) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (foodID, stepNum, r))
                self.mydb.commit()
                stepNum += 1

    def close(self):
        self.mydb.close()