import wavfile as wf
import speech_recognition as sr
import math
import numpy as np
from vad import VoiceActivityDetector
from xcorr import xcorr
from microphone import Microphone
from pydub import AudioSegment

class MicrophonePair(object):

    # Get an array of amplitudes of the wav file
    def getAmplitudeList(self, fileName: str):
        sampleRate, amplitudes = wf.read(fileName)
        if type(amplitudes[0]) is not np.int16:
            newAmplitudes = []
            for array in amplitudes:
                num = sum(array) / len(array)
            return newAmplitudes
        return amplitudes

    # Returns the start of speech, in ms, of a wav file. If no speech is detected, then returns -1
    def getSpeechStartTime(self, fileName):
        v = VoiceActivityDetector(fileName)
        windows = v.detect_speech()
        for i in range(0, len(windows)):
            arr = windows[i]
            if arr[len(arr) - 1] == 1:
                # VAD breaks wav file into 20 ms windowed chunks, with a 10 ms overlay
                return i * 10 
        return -1

        # Returns the coefficents and delays of the cross correlation function of two arrays

    # a and b should be the same length
    def crossCorrelate(self, a: list, b: list, maxDelay: int):
        # maxDelay cannot be greater the length of the arrays, that will cause errors
        assert maxDelay < len(a)

        lags, coeffs = xcorr(a, b, maxlags=maxDelay)
        return lags, coeffs

    # Applies distance formula to get distance between microphones
    def distance(self, mic1:Microphone, mic2:Microphone):
        x1 = mic1.getX()
        y1 = mic1.getY()
        x2 = mic2.getY()
        y2 = mic2.getY()

        dist = math.sqrt( (y2 - y1)**2 + (x2 - x1)**2)
        return dist

    # Calculates DOA and recognized Speech all in one go
    def __init__(self, mic1, mic2):
        self.microphone1 = mic1
        self.microphone2 = mic2
        # Check if there is speech, if not, then there is no point in doing 
        # further calculations. 
        speechStartTime = self.getSpeechStartTime(mic1.getFileName())
        if speechStartTime == -1:
            self.speechExists = False
            return 
        else: 
            self.speechExists = True

        if self.speechExists:

            # Get speech portion from both wav files
            speech1 = mic1.getSound()[speechStartTime - 300:speechStartTime + 400]
            speech2 = mic2.getSound()[speechStartTime - 300:speechStartTime + 400]

            speech1Holder = 'holder/speech1.wav'
            speech2Holder = 'holder/speech2.wav'

            speech1.export(speech1Holder,format='wav')
            speech2.export(speech2Holder,format='wav')

            # Prepare an amplitudes list for the speech portions
            # Needs to be normalized and values need to be lessened
            # so that cross correlation does not deal with the square root
            # of negative numbers and there is not an overflow error
            data1 = self.getAmplitudeList(speech1Holder)
            data2 = self.getAmplitudeList(speech2Holder)

            a = []
            b = []

            for num in data1:
                a.append(abs(int(num / 100)))

            for num in data2:
                b.append(abs(int(num / 100)))

            a = np.asarray(a)
            b = np.asarray(b)

            # if the the cross correlation result is negative, then that means that mic1 recieved the signal # of frames before mic 2

            lags, coeff = xcorr(b, a, maxlags=len(a) - 1)
            frameDelay = lags[np.argmax(coeff)]
            numFrames = len(data1)
            durationSeconds = AudioSegment.from_wav(speech1Holder).duration_seconds

            timeDelay = (frameDelay * durationSeconds) / numFrames
            distance = 0.20
            c = 340

            try:
                self.theta = math.degrees(math.acos((timeDelay * c) / distance))
            except:
                if timeDelay < 0:
                    self.theta = 150
                elif timeDelay > 0:
                    self.theta = 30

            if self.theta < 90:
                r = sr.Recognizer()
                with sr.WavFile(mic1.getFileName()) as source:
                    audio = r.record(source)
                    text = r.recognize_google(audio)
                self.recognizedSpeech = text
            else:
                r = sr.Recognizer()
                with sr.WavFile(mic2.getFileName()) as source:
                    audio = r.record(source)
                text = r.recognize_google(audio)
                self.recognizedSpeech = text
        else:
            self.DOA = None
            self.recognizedSpeech = None

    # Getter functions for microphone array class

    # Get the estimated direction of arrival of the sound source 
    def getDOA(self):
        return self.theta

    # Get the recognized speech signal of the sound source
    def getRecognizedSpeech(self):
        return self.recognizedSpeech

    # Get the normalized and lessened amplitude values of the speech portion of the first wav file
    def getSpeech1(self):
        return self.speech1

    # Get the normalized and lessened amplitude values of the speech portion of the second wav file
    def getSpeech2(self):
        return self.speech2

    # Return whether or not speech actually exists inside of the wav file 
    # This will be used for the microphone array class. 
    def getSpeechExists(self):
        return self.speechExists

    # Returns microphone 1
    def getMic1(self):
        return self.microphone1

    # Return microphone 2
    def getMic2(self):
        return self.microphone2