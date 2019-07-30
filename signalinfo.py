# class to handle the signal and the information that we need about it so that we can use in the GUI

class SignalInfo(object):

    WORD_THRESHOLD = 4

    # Constructs new objects with default parameters
    def __init__(self, x=0, y=0, recognizedSpeech=None):
        self.mx = x
        self.my = y
        self.mrecognizedSpeech = recognizedSpeech
        self.speechSlider:list = []
        if recognizedSpeech is not None:
            self.speechSlider = recognizedSpeech.split()

    # Returns x value of the speech signal
    def getX(self):
        return self.mx

    # Returns y value of the speech signal
    def getY(self):
        return self.my

    # Returns the recognizedSpeech of the speech signal
    def getRecognizedSpeech(self):
        return self.mrecognizedSpeech

    def getSpeechSlider(self):
        return self.speechSlider

    def setSpeechSlider(self, narray:list):
        self.speechSlider = narray

    def add(self, words:str):
        words = words.split()
        for word in words:
            self.speechSlider.append(word)
            if len(self.speechSlider) > self.WORD_THRESHOLD:
                self.speechSlider.pop(0)

    # Sets a new x value for the speech signal
    def setX(self, nx):
        self.mx = nx

    # Sets a new y value for the speech signal
    def setY(self, ny):
        self.my = ny

    # Sets a new text for the recognizedSpeech
    def setRecognizedSpeech(self, nrecognizedSpeech):
        self.mrecognizedSpeech = nrecognizedSpeech

    # Checks if the signal is speech or not
    def signalIsSpeech(self):
        return not self.mrecognizedSpeech == None