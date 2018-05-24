import numpy as np
import matplotlib.pyplot as plt 
from obspy.core import *
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
import sys
import os 
from datetime import datetime

from EarthquakeTimes import * 
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
for a in range(-1,2):
	date = datetime.strftime(ST.datetime+timedelta(days=a),"%Y%j")
	file = "/Users/noon/Documents/Studia/Magisterka/Dane/13BB_"+day+"/"+station_name+"_"+day+".mseed"
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
cft = classic_sta_lta(Z[0].data, int(60 * df), int(180 * df))
print(cft)
#plot_trigger(Z[0],cft, 1.5, 0.5) #nie rozumiem skad 1.5


#Lista triggerow w zapisie 0/1
trig=[]
num=[]
for i in range(len(cft)):
    if cft[i]>1.5:
        trig.append(1)
        num.append(i)
    else:
        trig.append(0)


        

 
#znalezienie czasow fal po dotarciu do Polski
#tworzę jedną listę czasów dotarcia fal do Polski (będzie 1 fail. Funkcja nie jest potrzebna)                  
PolishTimes2=[] #2D array
PolishTimes=[]
for i in range(len(EarthQ)):
    dist_temp=Distance([EarthQ_lat[i], EarthQ_long[i]], station_coord)
    time_temp=TrTime(dist_temp,EarthQ_depth[i])
    time_temp_pol=time_temp+np.repeat(EarthQ_time[i],len(time_temp))
    PolishTimes2.append(time_temp_pol)
    

for i in range(len(PolishTimes2)):
    for k in range(len(PolishTimes2[i])):
        PolishTimes.append(PolishTimes2[i][k])

for i in range(len(PolishTimes)):
    if PolishTimes[i]-int(PolishTimes[i])<0.5:
        PolishTimes[i]=int(PolishTimes[i])
    else:
        PolishTimes[i]=int(PolishTimes[i])+1


for i in range(len(PolishTimes)):
    if trig[PolishTimes[i]]==1:
        trig[i]=0
 
FileName=day+'_'+station_name+'.txt' 
#start_time = datetime.now()  

f=open(FileName,'w')
for i in range(len(trig)):
    f.write(str(trig[i])+'\n')
f.close()    
 
#end_time = datetime.now()
#print('Duration: {}'.format(end_time - start_time))
      