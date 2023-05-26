import openai
import os


class ChatGPT:
    def __init__(self, speechTxt):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.userSpeechText = "\"" + speechTxt + "\"\n"
        self.instruction = 'You are a natural language processor, the text above is what was recognized by mic input.' \
                           'Summarize what they want and put it into a json format. There are two fields.' \
                           'Type and Name. Type must be either Dish or Ingredient. Name must be represented in Korean.' \
                           'Just give me a json format text.'
        self.command = (self.userSpeechText + self.instruction)

    def get_response(self):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.command}
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
