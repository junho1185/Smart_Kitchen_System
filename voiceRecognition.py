import speech_recognition as sr

# 음성 인식 객체 생성
r = sr.Recognizer()

# 마이크를 사용해 음성 입력 받기
with sr.Microphone() as source:
    print("말씀하세요...")
    audio = r.listen(source)

# 인식된 음성 출력
try:
    print("음성인식 결과:", r.recognize_google(audio, language='ko-KR'))
except sr.UnknownValueError:
    print("음성을 인식할 수 없습니다.")
except sr.RequestError as e:
    print("Google Speech Recognition 서비스에 접근할 수 없습니다: {0}".format(e))