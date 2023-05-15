class RecipeParser:
    def __init__(self, *args):
        self.Korean = {}
        self.Japanese = {}
        self.Western = {}
        self.Chinese = {}
    
    def doParse(self):

        with open("recipe.txt", 'r', encoding="UTF-8") as f:
            for line in f:
                tokens = line.split()
                if len(tokens) == 0:
                    continue 
                name = tokens[1]
                recipe = f.readline()
                if(tokens[0] == 'Korean'):
                    self.Korean[name] = recipe
                elif(tokens[0] == 'Japanese'):
                    self.Japanese[name] = recipe
                elif(tokens[0] == 'Chinese'):
                    self.Chinese[name] = recipe
                elif(tokens[0] == 'Western'):
                    self.Western[name] = recipe
                else:
                    print("Format Error")
        
    def parseList(self):

        for recipe in self.Korean.keys():
            print(recipe + '의 레시피는 다음과 같다.')
            print(self.Korean[recipe])

        for recipe in self.Japanese.keys():
            print(recipe + '의 레시피는 다음과 같다.')
            print(self.Japanese[recipe])

        for recipe in self.Western.keys():
            print(recipe + '의 레시피는 다음과 같다.')
            print(self.Western[recipe])

        for recipe in self.Chinese.keys():
            print(recipe + '의 레시피는 다음과 같다.')
            print(self.Chinese[recipe])

