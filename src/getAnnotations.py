# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 18:13:44 2017


@author: ANINDITA Nath
university of Texas at El Paso
"""
import numpy as np
import scipy
import os
import warnings
from readStanceAnnotations import readStanceAnnotations 

def  getAnnotations(annotationDir):

  #converted from original by Nigel Ward, UTEP, June 2017
  #propertyValues is a cell array, one cell per news segment
  #where each cell is a struct, including: propvec, start, broadcast
  #this function essentiall just reformats flat arrays into an array of structs

  if isUtepAnnotationDir(annotationDir)==True:
      vals, tags,segStarts, segEnds, segUrls, propertyNames = readStanceAnnotations(annotationDir)
      
      nsegments = len(segStarts)
      segStructs = np.empty(nsegments, dtype=[('properties','f4',(14,)),('starts','i4'),('broadcast', 'S100')])

      for i in range (nsegments):
          segStructs['properties'][i] = vals[i]
          segStructs['starts'][i] = segStarts[i]
          segStructs['broadcast'][i] = segUrls[i]
    
      propertyValues = segStructs
  else:
    warnings.error('get annotations: found no csv files, so assuming it is an LDC corpus, but that is not  yet implemented\n');

  return propertyValues, propertyNames


'''------------------------------------------------------------------'''
def isUtepAnnotationDir(audioDir):
  result = len(csvfilesInToplevelDirectory(audioDir)) > 0
  return result

'''------------------------------------------------------------------'''
def  csvfilesInToplevelDirectory(dirname):
  filenames = []
  for file in os.listdir(dirname):
    if file.endswith(".csv"):
        fname=file
    filenames.append(fname)
  filenames=np.asarray(filenames)
  return filenames

#filenames=csvfilesInToplevelDirectory('stance-master/testeng/annotations/')
#print(filenames.shape)
#result=isUtepAnnotationDir('stance-master/testeng/annotations/')
#propertyValues, propertyNames=getAnnotations('stance-master/testeng/annotations/')
##np.set_printoptions(threshold=np.inf)
#print(propertyNames)
##print(propertyValues)
#for i in range(19):
#     print(propertyValues['properties'][i])
#scipy.io.savemat('getanno', {'propvalspy': propertyValues,'propertyNamespy':propertyNames})  
     