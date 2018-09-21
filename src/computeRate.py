from findClusterMeans import  findClusterMeans
import numpy as np
import math
import readtracks
import computeLogenergy
#Translated on Python by Alonso Granados 10/29/2017
# Nigel Ward and Paola Gallardo 12/04/2014
def computeRate(logEnergy, windowSizeMs):
    logEnergy = np.array(logEnergy)
    frames = int(windowSizeMs/10)
    #Computes a speaking-rate proxy using proxy for special flux
    deltas = abs(logEnergy[1:] - logEnergy[:(len(logEnergy)-1)])
    cumSumDeltas = np.append(np.zeros(1),np.cumsum(deltas))
    WindowLiveliness = cumSumDeltas[frames-1:] - cumSumDeltas[:(len(cumSumDeltas)-frames+1)]
    #Normalize rate for robustness against recording volume
    silence_mean, speech_mean = findClusterMeans(logEnergy)
    scaledLiveliness = (WindowLiveliness - silence_mean)/(speech_mean-silence_mean)
    headFramesToPad = int(math.floor(frames/2) - 1)
    tailFramesToPad = int(math.ceil(frames/2) - 1)
    scaledLiveliness = np.append(np.zeros(headFramesToPad), scaledLiveliness)
    scaledLiveliness = np.append(scaledLiveliness, np.zeros(tailFramesToPad))
    return scaledLiveliness

 # We tested this by applying it to 21d.au and listening to places
 #  where the high rate values were.
 # These were in fact places where the speaker was talking quickly.
 # "Ums" were detected as slow, nicely.
 # Regions of silence were low on this measure, as expected.
 #
 # Jan 2017,
 # Further testing showed that this was not consistently indicating rate.
 # It also responds to creaky voice, and to articulatory precision;
 # it may also respond to consonants vs vowels.
 # So it's now less important, now that I have lengthening and articulatory
 #  precision features.
 # But it correlates quite weakly with all of these, so keep it for now.

# filenames = [4,3,4.3,2,1]
# print(computeRate(filenames,30))
