import openai
import os


class ChatGPT:
    def __init__(self, speechTxt):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.userSpeechText = "\"" + speechTxt + "\"\n"
        self.instruction = 'Summarize what they need, put it into json format. Fields must be Action and Item. In ' \
                           'Action fields it must be one of the followings: Request, Quit. Item field must be what ' \
                           'they want in Korean.'
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
