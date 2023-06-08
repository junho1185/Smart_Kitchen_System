import openai
import os


class ChatGPT:
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"

    def get_response(self, speechTxt):
        userSpeechText = "\"" + speechTxt + "\"\n"
        instruction = 'You are a natural language processor, the text above is what was recognized by mic input.' \
                           'Summarize what they want and put it into a json format. There are two fields.' \
                           'Type and Name. Type must be either Dish or Ingredient. Name must be ' \
                      'the corresponding food name or ingredient name represented in Korean.' \
                      'If the recognized text does not contain either Dish nor Ingredient, put \'None\' to both fields.' \
                           'Just give me a json format text.'
        command = userSpeechText + instruction
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": command}
                ]
            )
            self.write_history(response)
            return response.choices[0].message['content']

        except Exception as e:
            print(f'Error occurred during ChatGPT request. Error Message: {e}')
            return None

    def write_history(self, response):
        filename = "code/data/chatGPTHistory.txt"

        with open(filename, "a", encoding="utf-8") as file:
            file.write(str(response) + '\n')

    def get_recipe(self, name):
        # In case the recipe used requested does not exist in database.
        instruction = "Give me a recipe of " + name + "in Korean." \
                                                      "Separate the sequence of the recipe by  \'/\' so I can parse it easily." \
                                                      "The string length of each recipe sequence should not exceed 20. " \
                                                      "So rather divide it into several steps than putting it all together." \
                                                      "Now put it into a json format. Field name for the recipe text must be \'Recipe\'." \
                                                      "In the Recipe field, there should be only text in the form of what I mentioned earlier." \
                                                      "Another field would be \'Region\' which indicates where the food comes from." \
                                                      "Value for the field would be an integer from 1 to 4. Korean(1), Japanese(2), " \
                                                      "Chinese(3), Western(4). Just give me the json format text."
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": instruction}
                ]
            )
            self.write_history(response)
            return response.choices[0].message['content']

        except Exception as e:
            print(f'Error occurred during ChatGPT request. Error Message: {e}')
            return None