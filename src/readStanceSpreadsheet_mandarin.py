# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 18:27:40 2017

@author: Anindita Nath
         University of Texas at El Paso
"""
import csv
import numpy as np
def readStanceSpreadsheet(csvfilename):
  
  
#  file format expected: CSV
#  
#  The annotators give us excel files, which we convert to CSV as follows:
#  1. open the excel file
#  2. go to the Developer tab (if necessary, first do: file->options->customize ribbon)
#  3. click "view code" in the middle of the ribbon
#  4. Copy in the"lightweight VBA macro from http://superuser.com/questions/841398/how-to-convert-excel-file-with-multiple-sheets-to-a-set-of-csv-files
#  saved locally as excel-to-csv-macro
#  5. Click Run 
#
#
#  English and Mandarin (from Speed of Sound)
#  row 1: "Stance Annotation"
#  row 2: informal description of audio file 
#  row 3: URL, whose last segment determines the audio file name
#  row 4: "segment start time", then a list of mm:ss format times
#  row 5: informal names for the segments 
#  rows 6-21:  stance-num-and-name, then a list of stance values 
# if the first column is empty, then skip the row
#  
#  Turkish and Uzbek (from Appen)
#  row 1: date of annotation
#  row 2: "lorelei file ID", then the audio file name 
#  row 3: "segment" id, can ignore
#  row 4: "topic": informal description for each segment
#  row 5: "segment start time": mm:ss.dd, mm:ss.dd ... 
#  rows 6-21: same as above 
#
#  thus, what we what to pull out is
#  NSvals: rows 6-21
#  NStags: SOS: row 5, Appen: row 4 
#  starts: SOS: row 4, Appen: row 5 
#  audio filename: for SOS row 3 tail of the URL; for Appen row 2, second column
#  stancenames: all non-blank fields in first column of rows 6-21

  #print(csvfilename)
  with open(csvfilename) as csvDataFile:
        csvReader = csv.reader(csvDataFile,delimiter=',')
        rows=[]
        count=0
        while True:            
            rows.append(next(csvReader))
            count=count +1
            if(count>=21): #since there are 21 rows in stance files, hard-coded as was in original
                break;
  appenformat=isAppenFormat(rows[0])
  #print(appenformat)
 
  if appenformat:
    lineOfStarts = rows[4]
    lineOfTags = rows[3]
    line2fields = ''.join(rows[1])
    aufilebase = line2fields
  else:
    lineOfStarts = rows[3]
    lineOfTags = rows[4]
    line3fields = rows[2]
    url = ''.join(line3fields)
    #aufilebase = url[28:]   # hardcoded 
    # mandarin
    aufile = url.split(sep='.')  
    aufilebase=aufile[0]
  #print(rows[20])
  #print('in readStanceSpreadsheet')
  #print(aufilebase)
  
  #starts=parseTags(lineOfStarts)
  parsestartsline,noofvalidtimes=parseTags(lineOfStarts)
  starts = minsecToSec(parsestartsline)
  #print(starts)
  allTags,noofvalidtags= parseTags(lineOfTags)  #informal name OR situation type / out-of-domain  #print(allTags)

  NStags = allTags 
  
  NSvals,stancenames= parseStanceVals(rows[5:21],noofvalidtags)
#  np.set_printoptions(threshold=np.inf)
#  print(NSvals)
#  print(NStags)
#  print(starts)
#  print(aufilebase)  
#  print(stancenames)
  return NSvals,NStags,starts,aufilebase,stancenames
 
def parseTags(tagthing):
  tagslist = []  

  for fields in range(1, len(tagthing)):      
          tagslist.append(tagthing[fields])
          tags=np.asarray(tagslist)
  tagsemptyindices=np.where(tags[:]=="")
  tagsOutOfDomain=np.where(tags[:]=="Out of Domain")
  tagsDomain=np.where(tags[:]=="Domain")
  tagsdomain=np.where(tags[:]=="domain")
  
  #print(tagsOutOfDomain)
  #print(tagsDomain)
  #print(tagsdomain)
  tagsnonempty=np.delete(tags,tagsemptyindices)
  tagsOutOfDomain=np.delete(tagsnonempty,tagsOutOfDomain)
  tagsDomain=np.delete(tagsnonempty,tagsDomain)
  tagsdomain=np.delete(tagsnonempty,tagsdomain)
  
  #print(tagsnonempty.shape)
  #print(len(tagsnonempty))   
  #print(tagsnonempty)
  return tagsnonempty,len(tagsnonempty)
'''------------------------------------------------------------------'''
#converts a sequence like 1:03, 1:25 to [63, 85]
# cannot yet handle mm:ss.dd and hh:mm:ss.dd
def minsecToSec(timetags):
  timesInSeconds = []
  #print(len(timetags))
  for nsi in range(len(timetags)):
    #print(nsi)
    #str1 = ''.join(timetags[nsi]) #converted each tag  to string 
    #timespec = str1.find(':')    
    #print(timespec)
    #numberOfColons=str1.count(':') 
    #print(numberOfColons)
#    if numberOfColons == 2: # for the format hh:mm:ss
#      timespec = timetags[nsi][3:]
#    else:
    timespec = timetags[nsi] #mandarin
    #print(timespec)
    minsec = timespec.split(':')
    #print(minsec)
    #print((minsec[0]))
    #print(int(minsec[1]))
    timeInSeconds =60 * int(minsec[0]) + int(minsec[1])  #convert minutes and seconds to seconds
    timesInSeconds.append(timeInSeconds)
    timesinsecs=np.asarray(timesInSeconds)
  #print(timesInSeconds)
  return timesinsecs
def parseStanceVals(stancerows,noofannotatedcolums):
    #print(len(stancerows))
    stancenames=[]
    stancevalues=[]
    for sr in range(len(stancerows)):
        # get stancenames from the stance-name(1st) column , store it separately 
        #print('sr')
        #print(sr)  
        stancenamecolumn=''.join(stancerows[sr][0]) #convert stancename column of each row to string       
        if(stancenamecolumn!=""):    # skip those rows which are blank,no stance names
          stancenames.append(stancenamecolumn) 
          for sv in  range(1,(noofannotatedcolums + 1)):
            #print('sv')
            #print(sv)
            #print(stancerows[sr][sv])
            if (''.join(stancerows[sr][sv])=="" or ''.join(stancerows[sr][sv])==' '): # those columns having no stances, make them 0
                stancerows[sr][sv]=0
           
#            print('before')
            #print(stancerows[sr][sv])
            stancerows[sr][sv]=int(stancerows[sr][sv])
            #print('after')
            #print(stancerows[sr][sv])
          stancevalues.append(stancerows[sr][1:noofannotatedcolums + 1])
        
       
    stancenames=np.asarray(stancenames)# convert to numpy for easier access in other functions
    stancevals=np.asarray(stancevalues)# convert to numpy for easier access in other functions
#    print(stancevals)
#    print(stancevals.shape)
    #for mandarin
    #cols=stancevals.shape[1]
   # print('stancevalsrows')
    #print(stancevals.shape[0])
    #print('stancevalscols')
    #print(cols)
    #stanceval = np.ndarray(shape=(14,cols),dtype='float32', buffer=stancevals)
#    print(stanceval.shape)
#    print(stanceval)
    return stancevals,stancenames
    
        
     
     
    
'''------------------------------------------------------------------'''
def isAppenFormat(row1):
  str1 = ''.join(row1)
  if (str1.find('Stance')>=0):
    appenish = False
  else:
    appenish = True
  return appenish

      
  

'''------------------------------------------------------------------'''

#to test:
#readSpreadsheet('stance-master/testeng/annotations/stance_ChevLocalNewsJuly3_L.csv');

#[vals, tags, starts, aufile, stNames] = readStanceSpreadsheet('../../Mandarin stance data/mandarin/trainAnnotationsCSV/reportstance_Mandarin mk97001~10 Nicolas(2)_mk97001.csv')
#np.set_printoptions(threshold=np.inf)
#print(vals)
#print(vals.shape)
#for i in range(0,len(tags)):
#    print(vals[i])