from datetime import datetime

new=[]
for i in range(3,14,2):
    new.append(i)
    


start_time = datetime.now()

f=open('new.txt','w')
for i in range(len(new)):
    f.write(str(new[i])+'\n')   
f.close()    


end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
