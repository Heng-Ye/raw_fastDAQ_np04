import csv
#import pandas as pd
#import xlrd as xl 
#from pandas import ExcelWriter
#from pandas import ExcelFile
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from dateutil.parser import parse
import operator
import sys

filename = sys.argv[1]
figName = sys.argv[2]

#pars initialization
lineNum = 0
#chofchs = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
chofchs = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ] 
time_msec = []
time = []
time_ref = []
n_ch = 16
n_tot = 17
#color_ch = ['black', 'red', 'orange', 'seagreen', 'blue', 'blueviolet', 'gray', 'deepskyblue', 'fuchsia', 'turquoise', 'sienna', 'greenyellow', 'black', 'lightcoral', 'yellow', 'black']
#color_ch = ['black', 'red', 'orange', 'seagreen', 'blue', 'blueviolet', 'gray', 'deepskyblue', 'fuchsia', 'turquoise', 'sienna', 'greenyellow', 'black', 'dodgerblue', 'lightcoral']
color_ch = ['black', 'red', 'orange', 'seagreen', 'blue', 'blueviolet', 'gray', 'deepskyblue', 'fuchsia', 'turquoise', 'sienna', 'green', 'black', 'dodgerblue', 'lightcoral']
t0 = 0
tt0 = 0
#leg_title = ["UP_DS_BR", "UP_DS_BL", "UP_MS_BR", "UP_MS_BL", "UP_US_BR", "UP_US_BL", "DN_DS_BR", "DN_DS_BL", "DN_MS_BR", "DN_MS_BL", "DN_US_BR", "DN_US_BL", "Heinzinger", "Beam Plug", "N/A", "LEVEL_METER"]
leg_title = ["UP_DS_BR", "UP_DS_BL", "UP_MS_BR", "UP_MS_BL", "UP_US_BR", "UP_US_BL", "DN_DS_BR", "DN_DS_BL", "DN_MS_BR", "DN_MS_BL", "DN_US_BR", "DN_US_BL", "Heinzinger", "Beam Plug", "LEVEL_METER"]

majorLocator   = MultipleLocator(20)
xFormatter = FormatStrFormatter('%.2f')
yFormatter = FormatStrFormatter('%.2f')
minorLocator   = MultipleLocator(5)

#set plot range
xmin = [ .94, .94, .94, .94, .94, .94, .94, .94, .94, .94, .94, .94, .94, .94, .94, .94]
xmax = [ .97, .97, .97, .97, .97, .97, .97, .97, .97, .97, .97, .97, .97, 1., .97, .97] 

#read csv file & save to list
with open(filename, 'r') as f:
  reader = csv.reader(f, delimiter=',')
  for row in reader:
    lineNum += 1
    t_in_line = float(row[0])+25200 #+2500: 7 hrs after Fermilab Time , i.e. CERN Time (add time offset if running the code in the U.S.)
    time_msec.append(t_in_line)
    if (lineNum==1):
      t0=t_in_line

    #time since start of this event [sec]
    t_ref = t_in_line - t0
    time_ref.append(t_ref)

    #Time conversion
    dt = datetime.datetime.fromtimestamp(t_in_line)
    dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    time.append(dt)
    if (lineNum==1):
      tt0=dt

    #for j in range(n_ch):
    for j in range(n_tot):
      if (j!=12 and j!=14 and j<n_ch-1):
        chofchs[j].append(1000.*float(row[j+1]))
      if (j==12): #replace ch13 with Heinzinger
        chofchs[j].append(50.*float(row[n_ch+1]))
      if (j==15): #level meter
        chofchs[j-1].append(7075.+60.*float(row[j+1]))

#calculation
#software threshold [unit: mV]
amp_th = [ -10, -10, -10, -10, 
           -10, -10, -10, -10, 
           -10, -10, -10, -10, 
           -10, -3000, -10000000 ] 

amin = [None] * (n_ch - 1)
tmin = [None] * (n_ch - 1)
amax = [None] * (n_ch - 1)
tmax = [None] * (n_ch - 1)
trig = [0] * (n_ch - 1)

#get maximum & minimum and their keys
count_trig=0
trig_index=99
for i in range(n_ch-1):
    tmax[i], amax[i] = max(enumerate(chofchs[i]), key=operator.itemgetter(1))
    tmin[i], amin[i] = min(enumerate(chofchs[i]), key=operator.itemgetter(1))
    #print('amax[', i, ']:', amax[i], '; tmax[', i, ']:', tmax[i])
    #print('amin[', i, ']:', amin[i], '; tmin[', i, ']:', tmin[i])
    if (amin[i]<=amp_th[i]) :
      trig[i]=1
      count_trig+=1
      trig_index=i

#title strings
if (count_trig==0):
  str_trig='No current draw on specfic GP(s)'
  str_gp_amin=''
if (count_trig==1):
  for i in range(n_ch-1):
    if (trig[i]==1):
      str_trig='Trigger: {}'.format(leg_title[i])
      str_gp_amin='GP({}):{:.2f} mV'.format(leg_title[i],amin[i])
if (count_trig>1):
  tmp_ct=0
  for i in range(n_ch-1):
    if (trig[i]==1):
      tmp_ct+=1
      if (tmp_ct==1): 
        str_trig='Trigger:{}'.format(leg_title[i])
        str_gp_amin='GP({}):{:.2f} mV '.format(leg_title[i],amin[i])
      if (tmp_ct>1): 
        str_trig+=' + {}'.format(leg_title[i])
        str_gp_amin+='+ GP({}):{:.2f} mV'.format(leg_title[i],amin[i])

plt.figure(figsize=(20,10))
for k in range(n_ch-1):
    plt.rcParams['axes.grid'] = True
    ax = plt.subplot(4,4,k+1)
    plt.plot(time_ref[:], chofchs[k][:], label='{}'.format(leg_title[k]), color=color_ch[k], linewidth=0.8)
    #plt.plot(time[:], chofchs[k][:], label='{}'.format(leg_title[k]), color=color_ch[k], linewidth=0.6)
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    #plt.xlim([xmin[k],xmax[k]])
    #plt.xlim(0.95, 1.05)
    #plt.xlim(0.95, 1.1)
    plt.xlim(0.97, 1.5)
    plt.legend(loc="upper right")

    if k==0 :
      plt.ylabel("Voltage [mV]")

    if k==13 :
      plt.ylabel("Voltage [mV]")

    if k==12 :
      plt.ylabel("Current [uA]")

    if k==14 :
      plt.ylabel("Level [mm]")

    if k==n_ch-1 :
      plt.xlabel("Time since start of this event [sec]")
plt.suptitle('CERN Time: {}\n {}\n HZ:{:.2f} uA / BP:{:.2f} mV / {}'.format(tt0,str_trig,amax[12],amax[13],str_gp_amin))

#plt.show()

plt.savefig(figName)
