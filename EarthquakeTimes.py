from obspy.taup import TauPyModel
model = TauPyModel(model="iasp91")
import numpy as np
from geopy.distance import great_circle

#there will be just 1 file, so no need to do a function
EarthQ=np.genfromtxt('/Users/Noon/Documents/Studia/Magisterka/Earthquakes/export_EMSC_201_2014.txt', dtype='str', delimiter=';')
#in this moment can not extract colums 1-5. Usecols does not work


    #this block is about real parameters of the earthquakes

Days_month=[31,59,90,120,151,181,212,243,273,304,334,365] #do not consider leap year
EarthQ_year=[]
EarthQ_day=[] #number of the day of the year
EarthQ_time=[] #time of the earthQ in [s]
EarthQ_lat=[] #latitude of the epicentrum
EarthQ_long=[] #longtitude of the epicentrum
EarthQ_depth=[] #depth of the earthQ in km??

for i in range(len(EarthQ)):
    EarthQ_year.append(EarthQ[i][0][0:4])

for i in range(len(EarthQ)):
    EarthQ_month=int(EarthQ[i][0][5:7])
    EarthQ_day.append(int(EarthQ[i][0][8:10])+Days_month[EarthQ_month-2])
    
for i in range(len(EarthQ)):
    EarthQ_hour=int(EarthQ[i][1][0:2])
    EarthQ_min=int(EarthQ[i][1][3:5])
    EarthQ_sec=int(EarthQ[i][1][6:9])
    EarthQ_time.append(EarthQ_hour*3600+EarthQ_min*60+EarthQ_sec)
 
for i in range(len(EarthQ)):
    EarthQ_lat.append(float(EarthQ[i][2]))

for i in range(len(EarthQ)):
    EarthQ_long.append(float(EarthQ[i][3]))
    
for i in range(len(EarthQ)):
    EarthQ_depth.append(float(EarthQ[i][4]))    
    


                        
                    #counting time and distance from earthQ to Poland

def Distance(point1, point2): #in km
    return (great_circle(point1, point2).km)/111.133 #bardzo gruba konwertacja do deg.
                                                    #nie wiem, czy taka wystarczy
def TrTime(dist, depth):
    time=[]
    arrival= model.get_travel_times(depth,dist,phase_list=["P","S","pP","sP",
                        "PcP","PP","PKiKP","pPKiKP","sPKiKP","sPKiKP","S"]) 
    
    for i in range(len(arrival)): #wyłuskiwanie liczb
        str1=str(arrival[i])
        temp=''
        for c in str1:
            if c in '1234567890.':
                temp=temp+c  
        time.append(float(temp))
    return time #lista czasów dla jednego zdarzenia, wychodzą różne dla każdego trzęsienia???


                

 
        
                    


