import numpy as np
import matplotlib.pyplot as plt 
from obspy.core import read
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
 
from EarthquakeTimes import *

#20.07
#QUESTIONS
#1. Jak lepiej, miec listę wszystkich st i tr 
#2. dla pięciu dni nie udało się wczytać, za słaby laptop

NumberOfDays=1 #liczba dni
NumOfDay=[] #the day of a stream
st=[]
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
             
    
 
    
    
    

    






