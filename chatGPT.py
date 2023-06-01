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
        filename = "data/chatGPTHistory.txt"

        with open(filename, "a", encoding="utf-8") as file:
            file.write(str(response) + '\n')

    def get_recipe(self, name):
        instruction = "Give me a recipe of " + name + ". All recipe text must be in Korean. You need to answer only the recipe text." \
                                                      "Separate each step by character \'/\' so I can parse it easily." \
                                                      "Remove the numbers of each steps of the recipe." \
                                                      "The string length of each recipe step should not exceed 50. " \
                                                      "So rather divide it into several steps than putting it all together." \
                                                      "Now put it into a json format. Field name for the recipe text must be \'Recipe\'" \
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