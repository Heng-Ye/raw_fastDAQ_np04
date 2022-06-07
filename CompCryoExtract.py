
import numpy
import struct
import datetime
from os import listdir
from os.path import isfile, join
import os
import time
import platform
import glob

import sys

#testFileName = '2018_09_11_23H50mn43.748014s_NP04_DSS_FASTACQ.facq'
#destPath = './'
#ofilename = destPath+'test.csv'

testFileName = sys.argv[1]
ofilename = sys.argv[2]

'''
This section is dedicated to access the DFS place for the files.
Then read in the filenames sorted by creation time -newest on front-.
'''        
#for testing:
#acqPath = r'\\CRIOSPARELAB9039@SSL\DavWWWRoot\files\C\FASTACQ'
#acqPath = r'G:\Users\r\rsipos\Public\fastacq'
#acqPath = r'\\NP04-CRIO-DSS-01@SSL\DavWWWRoot\files\C\FASTACQ'
#acqPath = r'Z:\C\FASTACQ'
#acqPath = r'Y:\C\FASTACQ'
#files = [f for f in listdir(acqPath) if isfile(join(acqPath,f))]
#files.sort(key=lambda x: os.path.getmtime(acqPath+'\\'+x), reverse=True)

#print(acqPath)
#print(files)
#print("last modified: %s" % time.ctime(os.path.getmtime(acqPath+'\\'+files[0])))

#testFileName = acqPath+'\\'+files[0]
fsize = os.stat(testFileName).st_size
remaining = fsize 
#print(fsize)
binaryFile = open(testFileName, mode='rb')
#print(binaryFile)

#data = object()
#(data.offset,)
#print("LabView TS:")
ts1 = struct.unpack('<Q', binaryFile.read(8))
ts2 = struct.unpack('<Q', binaryFile.read(8))
#print(ts1)
#print(ts2)

vals = {}
firstTs = None
while remaining >= 104:
  #print("Normal TS:")
  ts3 = struct.unpack('<Q', binaryFile.read(8))
  #print(ts3)
  secs = ts3[0] / 1e9
  #print('ts3[0]:',ts3[0])
  #print('secs:',secs)
  if secs == 0:
        print("Timestamp is 0! Continue.")
        break
  dt = datetime.datetime.fromtimestamp(secs)
  #dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
  #print('dt:',dt)
  if firstTs is None:
    firstTs = secs
  #print(dt)
  numRecs = struct.unpack('<I', binaryFile.read(4))
  #print("Num records" + str(numRecs))
  rec = []
  for x in range(numRecs[0]):
    value = struct.unpack('<f', binaryFile.read(4))
    #print(value)
    #print("idx:" + str(x))
    rec.append(value[0])
  
  #print(rec)
  vals[secs] = rec

  #print("Additional 5 x 4 Bytes:")
  try:
    for x in range(5):
      value = struct.unpack('<I', binaryFile.read(4))
  except Exception as e:
    print("Probably no trailing bytes.. " + str(e))
    pass
    #print(value)
    #print('\n')

  processed = 20+(numRecs[0]*4)+4+8
  #print("Processed bytes: " + str(processed))
  remaining = remaining - processed 
  #print("Remaining: " + str(remaining))

print("Remaining bytes unprocessed:" + str(remaining))
print(vals[firstTs])

#################################################################

import csv

'''
This is the section for uploading the data to CERNBox
'''
##destPath = r'C:\Users\Public\sync'
#destPath = './'
#print("Destination for csv files:"+destPath)
#outFile = destPath+'test.txt'
#f= open(outFile,"w+")
#for i in range(10):
#     f.write("This is line %d\r\n" % (i+1))
#f.close()

#ofilename = destPath+'\\test.csv'
with open(ofilename, "w") as ofile:
    writer = csv.writer(ofile, dialect='excel') # for 'normal' OSs: delimiter=' '
    for key in vals:
        writer.writerow([key] + vals[key])
        
    

