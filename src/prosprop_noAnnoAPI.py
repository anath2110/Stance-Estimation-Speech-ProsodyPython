# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:03:00 2017

@author: Anindita Nath
University of Texas at ElPaso
"""


from prosodizeCorpus_noAnnoAPI import prosodizeCorpus
from normalizeCorpus import normalizeCorpus
from prepForKnn import prepForKnn
from patchWiseknn import patchwiseKNN
import numpy as np
import scipy
import os
import datetime


now = datetime.datetime.now()

def prosprop(audioDir,ppmfile, stride, flags,lang,**kwargs):

    # converted from original by Nigel Ward and Ivan Gris, UTEP, June 2017
    # see ../doc/UTEP-prosody-overview.docx

    # audioDir is the name of a directory containing au files
    # segInfoDir is the directory containing info on the segments of the au files
    # ppmfile is a prosody-property-mapping file
    # stride is when chosing patches, how many milliseconds between them
    # flags is a string of single-character codes

    [writeJson, leaveOneOut, ufStances] = parseTheFlags(flags)

    print('loading ppm file: %s\n' %ppmfile)
   
    ppmfilepy=scipy.io.loadmat(ppmfile,struct_as_record=False, squeeze_me=True)
    provenancepy =ppmfilepy['provenancepy']
    propertyNamespy =ppmfilepy['propertyNamespy']
    featurespecpy =ppmfilepy['featurespecpy']    
    meanspy =ppmfilepy['meanspy']
    stddevspy =ppmfilepy['stddevspy']
    modelpy =ppmfilepy['modelpy']
    #algorithmpy =ppmfilepy['algorithmpy']    
    
    print("processing '%s' with respect to %s (%s)\n" % (audioDir,ppmfile,provenancepy))
    testProsodized = prosodizeCorpus(audioDir,featurespecpy, 100,lang,**kwargs)
    testNormalized = normalizeCorpus(testProsodized, meanspy, stddevspy)

    #[patchFeatures, patchProperties] = prepForKnn(modelpy, -1, True)
    #baseline = np.mean(patchProperties) # means over annotations data

    nproperties = len(propertyNamespy)
    nsegments = len(testNormalized)
    propvals = np.zeros((nsegments, nproperties))

    print(' patchwiseKnn on segment: \n')
    for i in range(nsegments):
        progressBar(i)

        segmentData = testNormalized[i].features;
        if leaveOneOut:
            #print('leaveoneout')
            indicesToExclude = i
            patchFeatures, patchProperties = prepForKnn(modelpy, indicesToExclude, False)
        
        if segmentData.size !=0:
            propvals[i,:], votePerPatch, patchNeighbors=patchwiseKNN(segmentData, patchFeatures, patchProperties, 3)
#           
    print('\n')
    
    saveResults(propvals, propertyNamespy, writeJson,lang) 
    
    return propvals

# ----------------------------------------------------------------------------
# show status to show that the computation is still progressing
def progressBar(i):
    print(' %3d' %i)
    if (i % 20 == 0):
        print('\n')


# ----------------------------------------------------------------------------
def saveResults(propvals, propertyNames, jsonFlag,lang):

 # !!! important for NIST competition!!!  normalizedEstimates = newNormalize(allEstimates);

    #filePrefix = 'props'
    outdir = 'output_python' + lang
    if not os.path.exists(outdir):
        os.makedirs(outdir)    
   

    outfilebase = outdir + '/propspy' + str(now.year) + '-' + str(now.month) + \
    '-' + str(now.day) +'-' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)
   
    scipy.io.savemat(outfilebase, {'propvalspy': propvals}) 
   
    #np.savetxt(pypredictions_opfile,propvals,fmt='%.1f',delimiter=', ')
      
   
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
