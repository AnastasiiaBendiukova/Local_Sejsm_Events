

import numpy as np
import matplotlib.pyplot as plt 
from obspy.core import *
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
import sys
import os 
import scipy.io as sio
from datetime import datetime


#from EarthquakeTimes import * 
from datetime import date, datetime, timedelta


coordinates={'B941':[54.0751, 17.6372],
'B914':[54.3719, 17.5664],
'B904':[54.2062, 18.1451],
'B955':[53.9641, 18.0097],
'B952':[53.9062, 17.5355],
'B953':[53.9370, 17.1490],
'B954':[54.1963, 17.1310],
'B940':[54.5347, 18.0428],
'B93E':[54.1295, 18.6132],
'B93F':[53.6429, 18.0682],
'B93D':[53.5992, 17.1992], 
'B956':[53.5992, 17.1992],
'B906':[54.5400, 17.1334]}


day = sys.argv[1]
station_name = sys.argv[2]


# obsługa błędu niepodania dwóch parametrów 
while True:
    try:
        if len(sys.argv[1]) and len(sys.argv[2]):
            print("Udane wczytanie dwóch parametrów")
            break
    except:
        print("Blad podania dwoch argumentow")
        
    
station_coord=coordinates[station_name]

            
            
ST = UTCDateTime(day, iso8601=True) 
ET = ST + 86400 

S = Stream()
for a in range(0,1):
	date = datetime.strftime(ST.datetime+timedelta(days=a),"%Y%j")
	file = "/Users/noon/Documents/Studia/Magisterka/Dane/"+station_name+"_"+day+".mseed"
	if os.path.isfile(file):
		if os.stat(file).st_size > 0:
			S = S + read(file)
            
            



    
              
            
    
S._cleanup(); #ZNALAZLAM TO W METODZIE MERGE, ALE NIE ROZUMIEM PO CO TU TO JEST


#Tego na razie nie robimy - to zrobimy potem
#S.trim(ST-3600,ET+3600) 

print(S)
print()
Z = S.select(component="Z")
print(Z)
df = Z[0].stats.sampling_rate
print("df=",df)
Z.filter('lowpass', freq=1.0, corners=2, zerophase=True)
cft={}
for i in range(len(Z)):
    cft[i]=classic_sta_lta(Z[i].data, int(60 * df), int(180 * df))
#    plot_trigger(Z[i],cft[i], 1.5, 0.5)



#Lista triggerow w zapisie True/False dla każdego z odcinków, czestosc zapisu - 100 Hz
trig3={}
#num=[]
for k in range(len(cft)):
    trig3[k]=[]
    for i in range(len(cft[k])):
        if cft[k][i]>1.5:
            trig3[k].append(True)
#           num.append(i)
        else:
            trig3[k].append(False)



#zmniejszenie czestosci zapisu 

trig2={}
for k in range(len(cft)):
    trig2[k]=[]
    for i in range(int(len(trig3[k])/100)):
        if trig3[k][3*i]==True or trig3[k][(3*i)+1]==True or trig3[k][(3*i)+2]==True:
            trig2[k].append(True)
        else:
            trig2[k].append(False)
        
#wyciąganie dłigosci przerw w zapisach 
gap={}
for i in range(len(cft)-1): #przerw jest o 1 mniej niz odcinkow  
    start=str(Z[i].stats.endtime)
    start_sec=int(start[11:13])*3600+int(start[14:16])*60+round(float(start[17:22]))
    end=str(Z[i+1].stats.starttime)
    end_sec=int(start[11:13])*3600+int(end[14:16])*60+round(float(end[17:22]))
    gap[i]=end_sec-start_sec
      
#sklejanie
if len(cft)!=1:
    trig=[] 
    file = open('List_gaps.txt', 'w')
    file.write(day+ ", "+ station_name)
    file.close()
    for k in range(len(cft)-1):
        for i in range(len(trig2[k])):
            trig.append(trig2[k][i])
        for s in range(gap[k]):
            trig.append(0)

    for i in range(len(trig2[len(cft)-1])):
        trig.append(trig2[len(cft)-1][i])        
    
else:
    trig=trig2[0]
    
        
    
      



#FileName=day+'_'+station_name 
#sio.savemat(FileName, {'trig':trig})

#