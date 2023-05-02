import torch
import threading 
from MS import MS_simulator_uncontiguos_index



def MS_distributed_CTA_scheduler(sub_CTA_list, number_of_CTA_to_exe, number_of_CTAs_per_MS,result,MS_init_inedes,faulty_MS = -1, block_executed_by_fauly_MS = None):
    executed_CTA = 0
   
    while(executed_CTA < number_of_CTA_to_exe):
        if((number_of_CTA_to_exe-executed_CTA) < number_of_CTAs_per_MS):
            MS_simulator_uncontiguos_index(sub_CTA_list[executed_CTA : number_of_CTA_to_exe],(number_of_CTA_to_exe-executed_CTA),result,MS_init_inedes[executed_CTA : number_of_CTA_to_exe],faulty_MS,block_executed_by_fauly_MS)
            executed_CTA = number_of_CTA_to_exe
        else:
            MS_simulator_uncontiguos_index(sub_CTA_list[executed_CTA : executed_CTA+number_of_CTAs_per_MS],number_of_CTAs_per_MS,result, MS_init_inedes[executed_CTA : executed_CTA+number_of_CTAs_per_MS],faulty_MS,block_executed_by_fauly_MS)
            executed_CTA += number_of_CTAs_per_MS
            


def Distributed_CTA_scheduler(CTA_list,to_schedule_CTAs_per_MS,number_of_MS_per_cluster,number_of_CTAs_per_MS, result_list, init_index,faulty_MS = -1, block_executed_by_fauly_MS = None, Scheduler_result = None, cluster_index = -1):
    
    

    n_touples = len(to_schedule_CTAs_per_MS)

    MS_init_indexes = []
    sub_CTA_list = []

    for m in range(number_of_MS_per_cluster):
        MS_init_indexes.append([])
        sub_CTA_list.append([])
        
    #now i have to regroup all the touples for each MS
    for touple in range(n_touples):
        ms_index,internal_init_index,i = to_schedule_CTAs_per_MS[touple]
        MS_init_indexes[ms_index].append(internal_init_index+init_index)
        sub_CTA_list[ms_index].append(CTA_list[internal_init_index])

    
    threads = []
    for ms in range(number_of_MS_per_cluster):
        
        Scheduler_result[ms+ cluster_index*number_of_MS_per_cluster] = MS_init_indexes[ms][:]
        if( ms != faulty_MS):
            threads.append(threading.Thread(target=MS_distributed_CTA_scheduler, args=(sub_CTA_list[ms][:],len(sub_CTA_list[ms]),
                                                                                        number_of_CTAs_per_MS,result_list,MS_init_indexes[ms][:],-1,None)    ))
        else:
            threads.append(threading.Thread(target=MS_distributed_CTA_scheduler, args=(sub_CTA_list[ms][:],len(sub_CTA_list[ms]),
                                                                                        number_of_CTAs_per_MS,result_list,MS_init_indexes[ms][:],faulty_MS,block_executed_by_fauly_MS)    ))

    for ms in range(number_of_MS_per_cluster):
        threads[ms].start()
    for ms in range(number_of_MS_per_cluster):
        threads[ms].join()


    



 