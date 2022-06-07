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
import csv

testFileName = sys.argv[1]
ofilename = sys.argv[2]

fsize = os.stat(testFileName).st_size
remaining = fsize 
binaryFile = open(testFileName, mode='rb')

ts1 = struct.unpack('<Q', binaryFile.read(8))
ts2 = struct.unpack('<Q', binaryFile.read(8))

vals = {}
firstTs = None
while remaining >= 104:
  ts3 = struct.unpack('<Q', binaryFile.read(8))
  secs = ts3[0] / 1e9
  if secs == 0:
        #print("Timestamp is 0! Continue.")
        break
  dt = datetime.datetime.fromtimestamp(secs)
  if firstTs is None:
    firstTs = secs
  numRecs = struct.unpack('<I', binaryFile.read(4))
  rec = []
  for x in range(numRecs[0]):
    value = struct.unpack('<f', binaryFile.read(4))
    rec.append(value[0])
  
  vals[secs] = rec

  try:
    for x in range(5):
      value = struct.unpack('<I', binaryFile.read(4))
  except Exception as e:
    #print("Probably no trailing bytes.. " + str(e))
    pass

  processed = 20+(numRecs[0]*4)+4+8
  remaining = remaining - processed 

#save the converted csv file
with open(ofilename, "w") as ofile:
    writer = csv.writer(ofile, dialect='excel') # for 'normal' OSs: delimiter=' '
    for key in vals:
        writer.writerow([key] + vals[key])
        
    

