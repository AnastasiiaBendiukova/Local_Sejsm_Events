import numpy as np
import matplotlib.pyplot as plt 
from obspy.core import *
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
import sys
import os

#from EarthquakeTimes import *
from datetime import date, datetime, timedelta

#20.07
#QUESTIONS
#1. Jak lepiej, miec listę wszystkich st i tr 
#2. dla pięciu dni nie udało się wczytać, za słaby laptop

NumberOfDays=1 #liczba dni
NumOfDay=[] #the day of a stream
st=[]

day = sys.argv[1]
station = sys.argv[2]
# Tu można dodać obsługę błędu niepodania dwóch parametrów

ST = UTCDateTime(day, iso8601=True)
ET = ST + 86400

S = Stream()
for a in range(-1,2):
	date = datetime.strftime(ST.datetime+timedelta(days=a),"%Y%j")
	file = "/media/goto/DATA/13BB/DATA_Pomerania/MSEED_DAILY/"+date+"/"+station+"_"+date+".mseed"
	if os.path.isfile(file):
		if os.stat(file).st_size > 0:
			S = S + read(file)
S._cleanup();
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
plot_trigger(Z[0], cft, 1.5, 0.5)
exit()


#create an array of streams
for i in range(NumberOfDays):
    st_temp=read('/Users/Noon/Documents/Studia/Magisterka/Dane/13BB_201420'+str(i+1)+'/*.mseed')
    st.append(st_temp)
    NumOfDay.append(int(20+i))
    
    
#In future these may be local variables inside the function
tr1=st[0][0]
tr2=st[0][1]
tr3=st[0][2]


def filt(x):
    return x.filter('lowpass', freq=1.0, corners=2, zerophase=True)
#To zwraca kopię?Czy kazda metoda zwraca kopię (np jak w string)?

def plots(x):
    t = np.arange(0, x.stats.npts / x.stats.sampling_rate, x.stats.delta)
    plt.subplot(211)
    plt.plot(t, x.data, 'k')
    plt.ylabel('Raw Data')
    plt.subplot(212)
    plt.plot(t, filt(x).data, 'k')
    plt.ylabel('Lowpassed Data')
    plt.xlabel('Time [s]')
    plt.suptitle(x.stats.starttime)
    plt.show()

plots(tr1)    

                    #Triggers 
                   
def Triggers(x):
    df = x.stats.sampling_rate #nie do konca rozumiem co to jest
    trig = classic_sta_lta(x.data, int(10 * df), int(20 * df)) #czemu jak zwiekszam, to liczy sie dluzej
    plot_trigger(x, trig, 1.5, 0.5)
    return trig
    
Triggers(filt(tr1))
trig=Triggers(filt(tr1)) 


#to juz nie jest zrobione ogolnie
TrEarthQ=[]
for i in range(len(PolishTimes)):
    for j in range(len(PolishTimes[i])):
        for k in range(len(tr1)):
            if PolishTimes[i][j]==tr1[k]:
                TrEarthQ.append(tr1[k])
             
    
 
    
    
    

    






