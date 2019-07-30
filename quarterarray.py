from microphonepair import MicrophonePair
import math

class MicrophoneQuarter(object):
    # given an angle in standard position, find the reference angle
    # PRECONDITIONS: 0 <= angle <= 360
    # this is used for the DOAs for the microphones, so the standard angle should never be over 180
    def findReferenceAngle(self, angle):
        if angle >= 0 and angle <= 90:
            return angle
        elif angle >= 90 and angle <= 180:
            return angle - 90
        elif angle >= 180 and angle <= 270:
            return angle - 180
        else:
            return angle - 270

    # Use the trinagulation formula to get the source position of the angles
    # The function requires the y axis angles because those are the ones that work with the formula
    def triangulate(self, distance, angle1, angle2):
        yEst = distance/(abs(math.degrees(math.atan(angle1))) + abs(math.degrees(math.atan(angle2))))
        xEst = yEst * abs(math.degrees(math.atan(angle1)))
        return xEst, yEst

    # Calculates the source position
    def __init__(self, micPair1:MicrophonePair, micPair2:MicrophonePair):
        # distance between microphone should be the same.
        self.distance = micPair1.distance(micPair1.getMic1(), micPair2.getMic2())
        self.DOA1 = micPair1.getDOA()
        self.DOA2 = micPair2.getDOA()

        referenceAngle1 = self.findReferenceAngle(self.DOA1)
        referenceAngle2 = self.findReferenceAngle(self.DOA2)

        yAxisAngle1 = 90 - referenceAngle1
        yAxisAngle2 = 90 - referenceAngle2

        self.x, self.y = self.triangulate(self.distance, yAxisAngle1, yAxisAngle2)
        self.recognizedSpeech = micPair1.getRecognizedSpeech()


    # Return the x coordinate of the estimated source positon
    def getX(self):
        return self.x

    # Return the y coordinate of the estimated source position
    def getY(self):
        return self.y

    # Return the recognized speech of that area
    # the possibility that there is no speech has been dealt with
    def getRecognizedSpeech(self):
        return self.recognizedSpeech

    # Return the distance between the microphones
    def getDistance(self):
        return self.distance