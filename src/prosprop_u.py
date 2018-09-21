# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 13:59:00 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""
import warnings
from prosodizeCorpus import prosodizeCorpus
from normalizeCorpus import normalizeCorpus
from prepForKnn import prepForKnn
from patchWiseknn import patchwiseKNN
import numpy as np
import scipy
import os
import datetime
import time
#import pickle
import _pickle as pickle
from makePPM import makePPM
warnings.filterwarnings("ignore")
now = datetime.datetime.now()

def prosprop(audioDir, segInfoDir, ppmfile, stride, flags,lang):

    # converted from original by Nigel Ward and Ivan Gris, UTEP, June 2017
    # see ../doc/UTEP-prosody-overview.docx

    # audioDir is the name of a directory containing au files
    # segInfoDir is the directory containing info on the segments of the au files
    # ppmfile is a prosody-property-mapping file
    # stride is when chosing patches, how many milliseconds between them
    # flags is a string of single-character codes

    [writeJson, leaveOneOut, ufStances] = parseTheFlags(flags)

    print('loading ppm file: %s\n' %ppmfile)
    # load from .mat file
    
    ppmfilepy=scipy.io.loadmat(ppmfile,struct_as_record=False, squeeze_me=True)
    provenancepy =ppmfilepy['provenancepy']
    propertyNamespy =ppmfilepy['propertyNamespy']
    featurespecpy =ppmfilepy['featurespecpy']    
    meanspy =ppmfilepy['meanspy']
    stddevspy =ppmfilepy['stddevspy']
    modelpy =ppmfilepy['modelpy']
    algorithmpy =ppmfilepy['algorithmpy'] 
    featurefilename=ppmfilepy['featurefilename']
    
    # load from .pkl file
#    with open(ppmfile, 'rb') as f:
#            ppmfilepy = pickle.load(f)
#            
#    provenancepy = ppmfilepy[0]
#    propertyNamespy=ppmfilepy[1]
#    featurespecpy = ppmfilepy[2]     
#    meanspy = ppmfilepy[3]
#    stddevspy = ppmfilepy[4]      
#    modelpy = ppmfilepy[5]
    print("processing '%s' with respect to %s (%s)\n" % (audioDir,ppmfile,provenancepy))

    testProsodized = prosodizeCorpus(audioDir, segInfoDir, featurespecpy, 100,lang,featurefilename)
    
    testNormalized = normalizeCorpus(testProsodized, meanspy, stddevspy)

    [patchFeatures, patchProperties] = prepForKnn(modelpy, -1, True)
    #print(patchProperties.shape)
    baseline = np.mean(patchProperties,axis=0) # means over training data
    #print(baseline.shape)                 
    nproperties = len(propertyNamespy)
    nsegments = len(testNormalized)
    propvals = np.zeros((nsegments, nproperties))

    print(' patchwiseKnn on segment: \n')
    for i in range(nsegments):
        progressBar(i)
        
        segmentData = testNormalized[i].features;
        if leaveOneOut:            
            indicesToExclude = i
            print('leaveoneout from modelpy' + str(indicesToExclude))
            patchFeatures, patchProperties = prepForKnn(modelpy, indicesToExclude, False)
        if segmentData.size !=0:
            print('testsegment' + str(i))
            propvals[i,:], votePerPatch, patchNeighbors=patchwiseKNN(segmentData, patchFeatures, patchProperties, 3)
       
        #print(propvals)
    # [propvals(i,:), votes] = patchwiseKnn(segmentData, patchFeatures, patchProperties, 3);
    # debug output
    # if i == 1
    # [largest, index] = max(votes(:,1))
    # end
    print('\n')
    #saveResults(propvals, propertyNamespy, writeJson)
    saveResults(propvals, propertyNamespy, writeJson,baseline,lang)
    return propvals, baseline

# ----------------------------------------------------------------------------
# show status to show that the computation is still progressing
def progressBar(i):
    print(' %3d' %i)
    if (i % 20 == 0):
        print('\n')


# ----------------------------------------------------------------------------
#def saveResults(propvals, propertyNames, jsonFlag):
def saveResults(propvals, propertyNames, jsonFlag,baseline,lang):

 # !!! important for NIST competition!!!  normalizedEstimates = newNormalize(allEstimates);

    #filePrefix = 'props'
    outdir = 'output_python' + lang
    if not os.path.exists(outdir):
        os.makedirs(outdir)    
   

    outfilebase = outdir + '/propspy' + str(now.year) + '-' + str(now.month) + \
    '-' + str(now.day) +'-' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)
   
    scipy.io.savemat(outfilebase, {'propvalspy': propvals, 'baselinepy':baseline}) 
    predtextfile='pypredictions' + lang +'.txt'
    np.savetxt(predtextfile,propvals,fmt='%.1f',delimiter=', ')
      
   
    if jsonFlag:
        print('not implemented\n')  #use writeResultsAsJason in december.m


# ----------------------------------------------------------------------------
def parseTheFlags(flags):
    writeJson = False
    leaveOneOut = False
    ufStances = False
    if flags=='j':
        writeJson = True

    if flags == 'l':
        leaveOneOut = True

    if flags =='u':
        ufStances = True
    return writeJson, leaveOneOut, ufStances

# ---------------------------------------------------------------------------
# testing
#startc=time.time()
#print('creating the model')
#model= makePPM('stance-master/testeng/audio/', 'stance-master/testeng/annotations/', 'stance-master/src/mono4.fss', 'ppmtestpy')
#endc=time.time()
#durcreation=endc-startc
#print('Time taken to create the model :' + str(durcreation) + '  secs')
#starte=time.time()
#print('evaluating the model')
#propvals, baseline=prosprop('stance-master/testeng/audio/', 'stance-master/testeng/annotations/', 'ppmtestpy.mat', 100, 'l');
#ende=time.time()
#durevaluation=ende-starte
#print('Time taken to evaluate the model :' + str(durevaluation) + '  secs')
# or use regressionTest();
