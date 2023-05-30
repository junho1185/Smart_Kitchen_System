import speech_recognition as sr
import sounddevice

class voiceRecognition:
    def __init__(self):
        # 음성 인식 객체 생성
        self.r = sr.Recognizer()
        self.text = ""

    def speechToText(self):

        # 마이크를 사용해 음성 입력 받기
        with sr.Microphone(device_index=0) as source:
            print("말씀하세요...")
            audio = self.r.listen(source)

        # 인식된 음성 출력
        try:
            self.text = self.r.recognize_google(audio, language='ko-KR')
            print("음성인식 결과:", self.text)

        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            print("Google Speech Recognition 서비스에 접근할 수 없습니다: {0}".format(e))
