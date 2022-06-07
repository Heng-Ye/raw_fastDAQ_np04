import os
import struct
import datetime

cwd = os.getcwd()
print(cwd)

#testFileName = '/eos/user/h/heliao/fastacq/ 2018_09_10_07H55mn36.328873s_NP04_DSS_FASTACQ.facq'
testFileName = '2018_09_12_01H49mn06.496500s_NP04_DSS_FASTACQ.facq'
binaryFile = open(testFileName, mode='rb')
print(binaryFile)

#data = object()
#(data.offset,)
print("LabView TS:")
ts1 = struct.unpack('<Q', binaryFile.read(8))
ts2 = struct.unpack('<Q', binaryFile.read(8))
print(ts1)
print(ts2)

print("\n Normal TS:")
ts3 = struct.unpack('<Q', binaryFile.read(8))
print(ts3)
secs = ts3[0] / 1e9
dt = datetime.datetime.fromtimestamp(secs)
dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
print('\n',dt)
numRecs = struct.unpack('<I', binaryFile.read(4))
print("Num records" + str(numRecs))

for x in range(numRecs[0]):
  value = struct.unpack('<f', binaryFile.read(4))
  print(value)

print("\n Additional 5 x 4 Bytes:")
for x in range(5):
  value = struct.unpack('<I', binaryFile.read(4))
  print(value)
print('\n')