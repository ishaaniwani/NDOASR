from microphone import Microphone
from microphonepair import MicrophonePair
import speech_recognition as sr

soundFile1 = 'WavFileDatabase/WAV/mic1.wav'
soundFile2 = 'WavFileDatabase/WAV/mic2.wav'

mic1 = Microphone(0, 0, soundFile1)
mic2 = Microphone(0, 0.15, soundFile2)

micPair = MicrophonePair(mic1, mic2)
doa = micPair.getDOA()
speech = micPair.getRecognizedSpeech()
print(doa)
print(speech)