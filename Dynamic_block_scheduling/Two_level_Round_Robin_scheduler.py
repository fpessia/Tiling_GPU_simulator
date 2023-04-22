import torch
import math
import threading 
from Greedy_clustering_scheduler import MS_Greedy_clustering_scheduler





def Two_level_Round_Robin_scheduler(CTA_list, to_schedule_CTA_for_this_cluster,number_of_CTA_per_MS, number_of_MS_per_cluster, result_list):
    to_schedule_CTAs_per_MS = []
    index_list = []
    matrix_block_list = []
    CTAs_of_cluster = len(to_schedule_CTA_for_this_cluster)

    for ms in range(number_of_MS_per_cluster):
        to_schedule_CTAs_per_MS.append([])
        index_list.append([])
        matrix_block_list.append([])
    
    scheduled_CTA = 0
    ms = 0

    while(scheduled_CTA < CTAs_of_cluster):
        to_schedule_CTAs_per_MS[ms].append(to_schedule_CTA_for_this_cluster[scheduled_CTA])
        ms += 1
        if (ms == number_of_MS_per_cluster):
            ms = 0
        scheduled_CTA += 1
    MS_threads = []
  

    for ms in range(number_of_MS_per_cluster):
        
        CTAs_of_this_MS = len(to_schedule_CTAs_per_MS[ms])
        
        
        if CTAs_of_this_MS != 0 : 
            n_sub_group = int(math.ceil(CTAs_of_this_MS/number_of_CTA_per_MS))
        else : 
            n_sub_group = 0

        n_completed_sub_group = int(CTAs_of_this_MS/number_of_CTA_per_MS)

        for s in range(n_sub_group):
            index_list[ms].append([])
            matrix_block_list[ms].append([])

        for n_completed in range(n_completed_sub_group):
            for cta_ms in range(number_of_CTA_per_MS):
                index_list[ms][n_completed].append(to_schedule_CTAs_per_MS[ms][cta_ms+n_completed*number_of_CTA_per_MS])
                matrix_block_list[ms][n_completed].append(CTA_list[to_schedule_CTAs_per_MS[ms][cta_ms+n_completed*number_of_CTA_per_MS]])
        
        if(n_sub_group != n_completed_sub_group):
            left_to_schedule = CTAs_of_this_MS - n_completed_sub_group*number_of_CTA_per_MS
            for left in range(left_to_schedule):
                index_list[ms][n_completed_sub_group].append(to_schedule_CTAs_per_MS[ms][n_completed_sub_group*number_of_CTA_per_MS + left])
                matrix_block_list[ms][n_completed_sub_group].append(CTA_list[to_schedule_CTAs_per_MS[ms][n_completed_sub_group*number_of_CTA_per_MS + left]])
        
   
        MS_threads.append(threading.Thread(target=MS_Greedy_clustering_scheduler, args=(matrix_block_list[ms],
                                                                                        result_list, index_list[ms])     ))

        
    for ms in range(number_of_MS_per_cluster):
        MS_threads[ms].start()
    for ms in range(number_of_MS_per_cluster):
        MS_threads[ms].join()

        
             
                 



       

    


