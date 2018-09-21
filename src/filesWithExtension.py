# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:17:55 2017

@author: ANINDITA Nath
University of Texas at El Paso
"""
import numpy as np

import os

def filesWithExtension(dirname, extension): 

  filenames = []
  for file in os.listdir(dirname):
    if file.endswith(extension):
        fname=file
    filenames.append(fname)
  filenames=np.asarray(filenames)
    
  return filenames
#filenames=filesWithExtension("stance-master/testeng/annotations", ".csv")
#print (filenames)