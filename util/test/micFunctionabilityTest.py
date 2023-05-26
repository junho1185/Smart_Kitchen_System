import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording audio...")

# Read audio data from the stream for 5 seconds
frames = []
for _ in range(int(RATE / CHUNK * 5)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording complete.")

# Stop the stream and close PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Convert the recorded audio frames to a numpy array
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

# Play back the recorded audio
print("Playing recorded audio...")
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

stream.write(audio_data.tobytes())

stream.stop_stream()
stream.close()
p.terminate()

print("Playback complete.")
