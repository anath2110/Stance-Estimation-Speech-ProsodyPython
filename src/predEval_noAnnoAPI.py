# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:03:00 2017

@author: Anindita Nath
University of Texas at ElPaso
"""

from prosprop_noAnnoAPI import prosprop


def predict(aufileloc,ppmfile,lang,**kwargs):

# converted from original by Nigel Ward, UTEP, June 2017
# see ../doc/UTEP-prosody-overview.docx
# called from the top level, to predict the predictions


    predictions= prosprop(aufileloc,ppmfile, 100, 'l',lang,**kwargs)

   
    return predictions


# ------------------------------------------------------------------
# test with
# cd testeng
# predEval('audio', 'annotations', 'smalltest-ppm.mat');
# Note that for this the training data is in the test data,
# so can obtain 100% if omit the leave-one-out flat, 'l' when calling prosprop

# larger test
# cd english
# predEval('audio', /annotation', 'ppmfiles/English-ppm.mat'); % takes 2 hours

# Turkish test
# cd turkish


