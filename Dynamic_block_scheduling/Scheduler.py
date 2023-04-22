import torch
import threading
from Distributed_block_scheduler import Distributed_block_scheduler
from Distributed_CTA_scheduler import Distributed_CTA_scheduler
from Greedy_clustering_scheduler import Greedy_clustering_scheduler
from Global_Round_Robin_scheduler import Global_Round_Robin_scheduler
from Two_level_Round_Robin_scheduler import Two_level_Round_Robin_scheduler
from Delay_generator import random_delay_generator_simulator

def Scheduler(CTA_list,number_of_cluster, number_of_MS_per_cluster, number_of_CTAs_per_MS, scheduling_protocol):
    
    n_CTA = len(CTA_list)
    result_list = []
    cluster_thread = []

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



    elif(scheduling_protocol == "Distributed_CTA"):
        to_schedule_CTAs_per_cluster = []
        for c in range(number_of_cluster):
            to_schedule_CTAs_per_cluster.append(int(n_CTA/number_of_cluster))
        if((n_CTA % number_of_cluster) != 0):
            left_to_schedule = n_CTA % number_of_cluster
            for i in range(left_to_schedule):
                to_schedule_CTAs_per_cluster[i] += 1

        for c in range(number_of_cluster):
            to_schedule_CTAs_per_MS = []
            ms_index = 0
            scheduled_CTA = 0

            while(scheduled_CTA < to_schedule_CTAs_per_cluster[c]):
                to_schedule_CTAs_per_MS.append((ms_index,scheduled_CTA, 1))
                scheduled_CTA += 1
                ms_index += 1
                if ms_index == number_of_MS_per_cluster:
                    ms_index = 0
            
            init_index = 0
            for k in range(c):
                init_index += to_schedule_CTAs_per_cluster[k]
            
            l = len(to_schedule_CTAs_per_MS)
            cluster_thread.append(threading.Thread(target=Distributed_CTA_scheduler, args=(CTA_list[init_index : init_index+to_schedule_CTAs_per_cluster[c]],
                                                                                           to_schedule_CTAs_per_MS[0 : l],number_of_MS_per_cluster,
                                                                                           number_of_CTAs_per_MS,result_list, init_index)  ))
        for c in range(number_of_cluster):
            cluster_thread[c].start()
        for c in range(number_of_cluster):
            cluster_thread[c].join()
        
        return result_list 

    elif(scheduling_protocol == "Greedy-Clustering"):
        num_of_CTA_in_cluster = number_of_CTAs_per_MS*number_of_MS_per_cluster
        total_num_of_CTA = num_of_CTA_in_cluster * number_of_cluster
        to_schedule_CTAs_per_cluster = []
        scheduled_CTA = 0
        cluster = 0

        for c in range(number_of_cluster):
            to_schedule_CTAs_per_cluster.append([])

        while(scheduled_CTA < n_CTA):
            if(scheduled_CTA < total_num_of_CTA):
                if(scheduled_CTA < (cluster +1)*num_of_CTA_in_cluster):
                    to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                    scheduled_CTA +=1
                else:
                    cluster +=1
                    to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                    scheduled_CTA += 1
            else : 
                if(scheduled_CTA == total_num_of_CTA):
                    cluster = 0
                    to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                    cluster += 1
                    scheduled_CTA += 1
                else:
                    to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                    scheduled_CTA += 1
                    cluster += 1
                    if(cluster == number_of_cluster):
                        cluster = 0
    
        
        for c in range(number_of_cluster):
            cluster_thread.append(threading.Thread(target=Greedy_clustering_scheduler, args=(CTA_list,to_schedule_CTAs_per_cluster[c],
                                                                                             number_of_MS_per_cluster,number_of_CTAs_per_MS,
                                                                                             result_list)     ))
        for c in range(number_of_cluster):
            cluster_thread[c].start()
        for c in range(number_of_cluster):
            cluster_thread[c].join()
        
        return result_list

    elif(scheduling_protocol == "Global-round-robin"):
        to_schedule_CTAs_per_cluster = []
        for c in range(number_of_cluster):
            to_schedule_CTAs_per_cluster.append([])

        scheduled_CTA = 0
        cluster = 0
        sm_counter = 0

        while(scheduled_CTA < n_CTA):
            if (scheduled_CTA < (number_of_cluster*number_of_MS_per_cluster*number_of_MS_per_cluster)):
                if(sm_counter < number_of_MS_per_cluster):
                    to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                    sm_counter += 1
                    scheduled_CTA += 1
                else :
                    cluster += 1
                    if(cluster == number_of_cluster):
                        cluster = 0
                    sm_counter = 0
                    to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                    scheduled_CTA += 1
            else:
                if(scheduled_CTA == (number_of_cluster*number_of_MS_per_cluster*number_of_MS_per_cluster)):
                    cluster = 0
                to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                cluster += 1
                scheduled_CTA += 1
                if(cluster == number_of_cluster):
                    cluster = 0
        
        for c in range(number_of_cluster):
            cluster_thread.append(threading.Thread(target=Global_Round_Robin_scheduler, args=(CTA_list,to_schedule_CTAs_per_cluster[c],
                                                                                              number_of_MS_per_cluster,number_of_CTAs_per_MS,
                                                                                              result_list)     ))
        for c in range(number_of_cluster):
            cluster_thread[c].start()
        for c in range(number_of_cluster):
            cluster_thread[c].join()


        return result_list

    elif(scheduling_protocol == "Two-level-round-robin"):
        to_schedule_CTAs_per_cluster = []
        number_of_static_CTAs = number_of_cluster*number_of_MS_per_cluster*number_of_CTAs_per_MS
        
        for c in range(number_of_cluster):
            to_schedule_CTAs_per_cluster.append([])
        
        scheduled_CTA = 0
        cluster = 0
        dynamic_scheduled_row = 0
        stocastic_ordering = []
        stocastic_counter = 0

        while(scheduled_CTA < n_CTA):
            if(scheduled_CTA < number_of_static_CTAs):
                to_schedule_CTAs_per_cluster[cluster].append(scheduled_CTA)
                cluster += 1
                scheduled_CTA += 1
                if(cluster == number_of_cluster):
                    cluster = 0
            else : #dynamic scheduling
                if(scheduled_CTA == dynamic_scheduled_row*number_of_MS_per_cluster*number_of_cluster+ number_of_static_CTAs):
                    stocastic_counter = 0
                    dynamic_scheduled_row += 1
                    stocastic_ordering = []
                    random_delay_generator_simulator(stocastic_ordering,number_of_cluster)
                    to_schedule_CTAs_per_cluster[stocastic_ordering[stocastic_counter]].append(scheduled_CTA)
                    scheduled_CTA +=1
                    stocastic_counter += 1
                else : 
                    to_schedule_CTAs_per_cluster[stocastic_ordering[stocastic_counter]].append(scheduled_CTA)
                    scheduled_CTA += 1
                    stocastic_counter += 1
                    if(stocastic_counter == number_of_cluster):
                        stocastic_counter = 0

                    


        for c in range(number_of_cluster):
            cluster_thread.append(threading.Thread(target=Two_level_Round_Robin_scheduler, args=(CTA_list,to_schedule_CTAs_per_cluster[c],
                                                                                                 number_of_CTAs_per_MS,number_of_MS_per_cluster,
                                                                                                 result_list)     ))
        for c in range(number_of_cluster):
            cluster_thread[c].start()
        for c in range(number_of_cluster):
            cluster_thread[c].join()


        return result_list
 
    else: 
        print("Not implemented protocol")
        return []

        


    
