import openai

class chatGPT:
    def __init__(self, speechTxt):
        openai.api_key = "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"
        self.model = "gpt-3.5-turbo"
        self.userSpeechText = "\"" + speechTxt + "\""
        self.instruction = 'Summarize what they need, put it into json format. Fields must be Action and Item. In Action fields ' \
                           'it must be one of the followings: Request, Quit. Item field must be what they want in Korean.'

    def getResponse(self):
        # function to request ChatGPT API and get a response
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.userSpeechText + self.instruction}
                ]
            )

            self.writeHistory(response)
            return response.choices[0].message['content']

        except Exception as e:
            print(f'Error occurred during ChatGPT request. Error Message: {e}')
            return None

    def writeHistory(self, response):
        # function to write history of responses
        filename = "data/chatGPTHistory.txt"

        # Open the file in append mode and write the text to it
        with open(filename, "a") as file:
            file.write(str(response))