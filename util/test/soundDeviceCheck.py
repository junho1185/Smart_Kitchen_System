import pyaudio

index = pyaudio.PyAudio().get_device_count()
print(index)