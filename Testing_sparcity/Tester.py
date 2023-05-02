import torch
import random
import time 
import numpy
from Tiling2D import Tiling2D
from Tiling2D import schedule_protocols
import matplotlib.pyplot as plt

num_of_cluster = 3
num_of_MS_per_cluster = 4
num_of_CTA_per_MS = 3

faulty_BLOCK = []

A = torch.randn(1280,1280)
B = torch.randn(1280,1280)

schedule_policy = []
MS_executing = []

for scheduler in range(len(schedule_protocols)-1):
    curr_schedule = scheduler + 1
    scheduler_result = []
    MS_executing.append([])
    C = Tiling2D(A,B,num_of_cluster,num_of_MS_per_cluster,num_of_CTA_per_MS,schedule_protocols[curr_schedule],0, -1, faulty_BLOCK, scheduler_result)
 
    n_CTA = 0
    
    for ms in range(num_of_cluster*num_of_MS_per_cluster):
        n_CTA += len(scheduler_result[ms])
        #print(scheduler_result[ms])
        #print("\n \n")
    print("n of cta : "+ str(n_CTA))
    n_CTA = 16000
    for cta in range(n_CTA):
        ms_index = 0
        i = 0
        while(scheduler_result[ms_index][i] != cta):
            i += 1
            if i == len(scheduler_result[ms_index]):
                ms_index += 1
                i = 0
                if (ms_index == num_of_cluster*num_of_MS_per_cluster):
                    print("what the fuck")
                    print(cta)
                
        MS_executing[scheduler].append(ms_index)
x = []
number_of_MS_executing_same_CTA = []
for n in range(n_CTA):
    x.append(n)
    number_of_MS_executing_same_CTA.append(0)
for n in range(n_CTA):
    max = 0
    for i in range(4):
        nequal_CTA = 0
        if(MS_executing[i][n] == MS_executing[1][n]):
            nequal_CTA += 1
        if(MS_executing[i][n] == MS_executing[2][n]):
            nequal_CTA += 1
        if(MS_executing[i][n] == MS_executing[3][n]):
            nequal_CTA += 1
        if(MS_executing[i][n] == MS_executing[0][n]):
            nequal_CTA += 1
        
        if nequal_CTA > max :
            max = nequal_CTA
    number_of_MS_executing_same_CTA[n] = max


  #      number_of_MS_executing_same_CTA[n] += 1
   # if(MS_executing[1][n] == MS_executing[2][n]):
   #     number_of_MS_executing_same_CTA[n] += 1
  #  if(MS_executing[1][n] == MS_executing[3][n]):
   #     number_of_MS_executing_same_CTA[n] += 1
   # if(MS_executing[2][n] == MS_executing[3][n]):
     #   number_of_MS_executing_same_CTA[n] += 1
avg = 0
for n in range(n_CTA):
    avg += number_of_MS_executing_same_CTA[n]

print( avg/n_CTA)
 

plt.plot(x,number_of_MS_executing_same_CTA,'ro')
plt.ylabel("number of multiprocessor executing  same CTA")
plt.xlabel("CTA")
plt.show()
#plt.plot(x, MS_executing[0],'r--', x,MS_executing[1],'bs',x,MS_executing[2],'g^') #, x,MS_executing[3])

