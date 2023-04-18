import torch
import threading
from Distributed_block_scheduler import Distributed_block_scheduler

def MS_executor(A,B,result,CTA_number):
    result[CTA_number] = torch.matmul(A,B)


def MS_simulator(input, number_of_CTAs_per_MS,result): #result is a list for by reference
    #divide the touples
    thread_list =[]
    for n in range(number_of_CTAs_per_MS):
        A,B = input[n]
        thread_list.append(threading.Thread(target=MS_executor, args=(A,B,n,result)))

    for n in range(number_of_CTAs_per_MS):
        thread_list[n].start()
    for n in range(number_of_CTAs_per_MS):
        thread_list[n].join()
    



def Scheduler(CTA_list, number_of_MS, number_of_CTAs_per_MS, scheduling_protocol):
    n_CTA = len(CTA_list)


    if(scheduling_protocol == "Distributed_block"):
        to_schedule_CTAs_per_MS = []
        #Divide the list of CTA acorss available MS
        for ms in range(number_of_MS):
            to_schedule_CTAs_per_MS.append(int(n_CTA/number_of_MS))
        if((n_CTA %  number_of_MS) != 0):
            left_to_schedule = n_CTA - int(n_CTA/number_of_MS)
            for i in range(left_to_schedule):
                to_schedule_CTAs_per_MS[i] = to_schedule_CTAs_per_MS[i] + 1
        # Now I call the  distributed-block scheduler
        return  Distributed_block_scheduler(CTA_list,to_schedule_CTAs_per_MS,number_of_CTAs_per_MS)


    
    else: 
        print("Not implemented protocol")

        


    
