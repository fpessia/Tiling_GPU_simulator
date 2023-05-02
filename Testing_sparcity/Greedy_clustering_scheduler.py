import torch
import math
import threading 
from MS import MS_simulator_uncontiguos_index
from Delay_generator import random_delay_generator_simulator


def MS_Greedy_clustering_scheduler(matrix_block_list,result_list, index_list, faulty_MS = -1, block_executed_by_fauly_MS = None):

    n_groups = len(index_list)
    for CTA_group in range(n_groups):
        MS_simulator_uncontiguos_index(matrix_block_list[CTA_group],len(matrix_block_list[CTA_group]),result_list,index_list[CTA_group],faulty_MS,block_executed_by_fauly_MS)



def Greedy_clustering_scheduler(CTA_list,to_schedule_CTA_for_this_cluster,number_of_MS_per_cluster,number_of_CTA_per_MS,result_list,faulty_MS = -1,block_executed_by_fauly_MS = None,Scheduler_result =None, cluster_index = -1):
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
    num_of_static_scheduled = number_of_MS_per_cluster*number_of_CTA_per_MS

    stocastic_order = []
    dynamic_block = 0
    dynamic_block_counter = 0

    while(scheduled_CTA < CTAs_of_cluster):
        if(scheduled_CTA < num_of_static_scheduled):
            to_schedule_CTAs_per_MS[ms].append(to_schedule_CTA_for_this_cluster[scheduled_CTA])
            ms += 1
            if (ms == number_of_MS_per_cluster):
                ms = 0
            scheduled_CTA += 1
        else : #dynamic scheduling
            if(scheduled_CTA == num_of_static_scheduled+dynamic_block*num_of_static_scheduled):
                ms = 0
                dynamic_block_counter = 0
                stocastic_order = []
                diff = CTAs_of_cluster - scheduled_CTA
                if (diff < num_of_static_scheduled):
                    stocastic_order = random_delay_generator_simulator(stocastic_order, diff)
                else:
                    stocastic_order = random_delay_generator_simulator(stocastic_order, num_of_static_scheduled)
            
            to_schedule_CTAs_per_MS[ms].append(to_schedule_CTA_for_this_cluster[num_of_static_scheduled+dynamic_block*num_of_static_scheduled+
                                                                                stocastic_order[dynamic_block_counter]])
            ms += 1
            if ms == number_of_MS_per_cluster:
                ms = 0
            dynamic_block_counter += 1
            scheduled_CTA += 1
            if(dynamic_block_counter == num_of_static_scheduled):
                dynamic_block_counter = 0
                dynamic_block += 1
            

    MS_threads = []
  

    for ms in range(number_of_MS_per_cluster):
        
        CTAs_of_this_MS = len(to_schedule_CTAs_per_MS[ms])
        Scheduler_result[ms + cluster_index*number_of_MS_per_cluster] = to_schedule_CTAs_per_MS[ms]
        
        
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
        
        if( ms != faulty_MS):
            MS_threads.append(threading.Thread(target=MS_Greedy_clustering_scheduler, args=(matrix_block_list[ms],
                                                                                            result_list, index_list[ms], -1, None)     ))
        else:
            MS_threads.append(threading.Thread(target=MS_Greedy_clustering_scheduler, args=(matrix_block_list[ms],
                                                                                            result_list, index_list[ms], faulty_MS, block_executed_by_fauly_MS)     ))            


        
    for ms in range(number_of_MS_per_cluster):
        MS_threads[ms].start()
    for ms in range(number_of_MS_per_cluster):
        MS_threads[ms].join()

        
             
                 



       

    


