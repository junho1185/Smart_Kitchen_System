import mysql.connector as conn
import os
from recipe_parser import RecipeParser

mydb = conn.connect(
    host="localhost",
    user="root",
    password=os.environ.get("MYSQL_PASSWORD"),
    database="Smart_Kitchen_System"
)

cursor = mydb.cursor()

rp = RecipeParser()

rp.doParse()

Korean = rp.Korean
Japanese = rp.Japanese
Chinese = rp.Chinese
Western = rp.Western

query = "truncate table RecipeIndex;"
cursor.execute(query)
mydb.commit()

# Putting foods into RecipeIndex Table
for recipe in Korean.keys():
    query = f"INSERT INTO RecipeIndex (foodName, region) VALUES (\"{recipe}\", 1)"
    cursor.execute(query)
    mydb.commit()

for recipe in Japanese.keys():
    query = f"INSERT INTO RecipeIndex (foodName, region) VALUES (\"{recipe}\", 2)"
    cursor.execute(query)
    mydb.commit()

for recipe in Chinese.keys():
    query = f"INSERT INTO RecipeIndex (foodName, region) VALUES (\"{recipe}\", 3)"
    cursor.execute(query)
    mydb.commit()

for recipe in Western.keys():
    query = f"INSERT INTO RecipeIndex (foodName, region) VALUES (\"{recipe}\", 4)"
    cursor.execute(query)
    mydb.commit()

# Putting recipe steps in the RecipeSteps Table
for food in Korean.keys():
    recipes = Korean[food].strip().split(' / ')
    query = "SELECT ID FROM RecipeIndex WHERE foodName=%s"
    cursor.execute(query, [food])
    fetchResult = cursor.fetchall()
    foodID = fetchResult[0][0]

    stepNum = 1
    for recipe in recipes:
        query = "INSERT INTO RecipeSteps (foodID, stepNum, recipe) VALUES (%s, %s, %s)"
        cursor.execute(query, (foodID, stepNum, recipe))
        mydb.commit()
        stepNum += 1

for food in Japanese.keys():
    recipes = Japanese[food].strip().split(' / ')
    query = "SELECT ID FROM RecipeIndex WHERE foodName=%s"
    cursor.execute(query, [food])
    fetchResult = cursor.fetchall()
    foodID = fetchResult[0][0]

    stepNum = 1
    for recipe in recipes:
        query = "INSERT INTO RecipeSteps (foodID, stepNum, recipe) VALUES (%s, %s, %s)"
        cursor.execute(query, (foodID, stepNum, recipe))
        mydb.commit()
        stepNum += 1

for food in Western.keys():
    recipes = Western[food].strip().split(' / ')
    query = "SELECT ID FROM RecipeIndex WHERE foodName=%s"
    cursor.execute(query, [food])
    fetchResult = cursor.fetchall()
    foodID = fetchResult[0][0]

    stepNum = 1
    for recipe in recipes:
        query = "INSERT INTO RecipeSteps (foodID, stepNum, recipe) VALUES (%s, %s, %s)"
        cursor.execute(query, (foodID, stepNum, recipe))
        mydb.commit()
        stepNum += 1

for food in Chinese.keys():
    recipes = Chinese[food].strip().split(' / ')
    query = "SELECT ID FROM RecipeIndex WHERE foodName=%s"
    cursor.execute(query, [food])
    fetchResult = cursor.fetchall()
    foodID = fetchResult[0][0]

    stepNum = 1
    for recipe in recipes:
        query = "INSERT INTO RecipeSteps (foodID, stepNum, recipe) VALUES (%s, %s, %s)"
        cursor.execute(query, (foodID, stepNum, recipe))
        mydb.commit()
        stepNum += 1


mydb.close()