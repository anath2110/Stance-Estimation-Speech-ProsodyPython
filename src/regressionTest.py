# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 13:59:00 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""

import warnings
from predEval import predEval
import numpy as np
import scipy
import time
from makePPM import makePPM
warnings.filterwarnings("ignore")

def regressionTest(pathtoaudiodir,pathtoannodir,ppmfile):   

    results, MSE = predEval(pathtoaudiodir, pathtoannodir, ppmfile)
    predictionsfile=scipy.io.loadmat('testregression',struct_as_record=False)
    predictions =predictionsfile['predictionspy']   

    permissibleError = 0.1 # on a scale from 0 to 2
    largestError = abs((np.max(results - predictions)))

    if largestError > permissibleError:
        print('regression test succeeded: values matched')
    else:
        print("regression test failed; something changed %d" %largestError)
    return results

#testing
startc=time.time()
print('creating the model')
model= makePPM('../testeng/audio/', '../testeng/annotations/', '../testeng/featurefile/mono4.fss', 'ppmtestpy')
endc=time.time()
durcreation=endc-startc
print('Time taken to create the model :' + str(durcreation) + '  secs')
starte=time.time()
print('evaluating the model')
predictionsfinal = regressionTest('../testeng/audio/', '../testeng/annotations/', 'ppmtestpy.mat')
ende=time.time()
durevaluation=ende-starte
print('Time taken to evaluate the model :' + str(durevaluation) + '  secs')

