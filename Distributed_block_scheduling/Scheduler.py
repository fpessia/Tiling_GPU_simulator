import torch
import threading
from Distributed_block_scheduler import Distributed_block_scheduler
#from Distributed_CTA_scheduler import Distributed_CTA_scheduler

def Scheduler(CTA_list,number_of_cluster, number_of_MS_per_cluster, number_of_CTAs_per_MS, scheduling_protocol):
    
    n_CTA = len(CTA_list)
    result_list = []

    A, B = CTA_list[0]
    xr,y1 = A.size()
    x1, yr = B.size()

    for n in range(n_CTA):
        result_list.append(torch.zeros(xr,yr))


    if(scheduling_protocol == "Distributed_block"):

        to_schedule_CTAs_per_cluster = []
        for c in range(number_of_cluster):
            to_schedule_CTAs_per_cluster.append(int(n_CTA/number_of_cluster))
        if((n_CTA % number_of_cluster) != 0):
            left_to_schedule = n_CTA % number_of_cluster
            for i in range(left_to_schedule):
                to_schedule_CTAs_per_cluster[i] += 1

        cluster_thread = []
        for c in range(number_of_cluster):
            to_schedule_CTAs_per_MS = []
            ms_index = 0
            scheduled_CTA = 0

            while(scheduled_CTA < to_schedule_CTAs_per_cluster[c]):
                n_CTA_for_current_MS = number_of_CTAs_per_MS
                if((to_schedule_CTAs_per_cluster[c]- scheduled_CTA) < number_of_CTAs_per_MS):
                    n_CTA_for_current_MS = to_schedule_CTAs_per_cluster[c]- scheduled_CTA
                to_schedule_CTAs_per_MS.append((ms_index,scheduled_CTA,n_CTA_for_current_MS)) 
                ms_index += 1
                if(ms_index == number_of_MS_per_cluster):
                    ms_index = 0
                scheduled_CTA += number_of_CTAs_per_MS
            
            init_index = 0
            for k in range(c):
                init_index += to_schedule_CTAs_per_cluster[k]

            
            
            l = len(to_schedule_CTAs_per_MS) #cannot pass the list by reference
            cluster_thread.append(threading.Thread(target=Distributed_block_scheduler, args=(CTA_list[init_index: init_index+to_schedule_CTAs_per_cluster[c]],
                                                                                            to_schedule_CTAs_per_MS[0 : l],number_of_MS_per_cluster,
                                                                                             number_of_CTAs_per_MS,result_list, init_index)  ))
        
        for c in range(number_of_cluster):
            cluster_thread[c].start()
        for c in range(number_of_cluster):
            cluster_thread[c].join()

        return result_list     
     
   
    else: 
        print("Not implemented protocol")

        


    
