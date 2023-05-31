
import pyaudio
import wave
from pydub import AudioSegment

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
OUTPUT_FILENAME = "enregistrement.mp3"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Enregistrement en cours...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Enregistrement terminé.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("enregistrement.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

audio = AudioSegment.from_wav("enregistrement.wav")
audio.export(OUTPUT_FILENAME, format="mp3")



from ShazamAPI import Shazam

mp3_file_content_to_recognize = open('enregistrement.mp3', 'rb').read()

shazam = Shazam(mp3_file_content_to_recognize)
recognize_generator = shazam.recognizeSong()
print(next(recognize_generator))