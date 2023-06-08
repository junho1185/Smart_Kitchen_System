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
        instruction = name + "의 레시피를 한국어로 알려줘. 레시피의 각 단계는 / 로 나눠서 줄 바꿈 없이 한 줄로 표현해줘." \
                             "각 레시피 단계의 문자 길이는 15자를 넘지 않도록 제한해줘. 그 텍스트를 json 형태에서 Recipe 필드에 넣어줘." \
                             "다른 필드는 Region이야. 이 필드에는 1, 2, 3, 4 숫자만 들어가. 한식이면 1, 일식이면 2, 중식이면 3, 양식이면 4를 넣어줘. json 형식의 텍스트만 줘"
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": instruction}
                ]
            )
            self.write_history(response)
            print("ChatGPT Response:")
            print(response)
            return response.choices[0].message['content']

        except Exception as e:
            print(f'Error occurred during ChatGPT request. Error Message: {e}')
            return None