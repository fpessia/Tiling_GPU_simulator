import torch
import threading
from MS import MS_simulator_contiguos_index


def MS_distributed_block_scheduler(sub_CTA_list, number_of_CTA_to_exe, number_of_CTAs_per_MS,result,initial_index,faulty_MS = -1,block_executed_by_fauly_MS= None):
    executed_CTA = 0
    while(executed_CTA < number_of_CTA_to_exe):
        if ((number_of_CTA_to_exe- executed_CTA) < number_of_CTAs_per_MS):
            MS_simulator_contiguos_index(sub_CTA_list[executed_CTA : number_of_CTA_to_exe],(number_of_CTA_to_exe- executed_CTA),result, initial_index+executed_CTA,faulty_MS,block_executed_by_fauly_MS )
            executed_CTA = number_of_CTA_to_exe
        else:
            MS_simulator_contiguos_index(sub_CTA_list[executed_CTA : executed_CTA+number_of_CTAs_per_MS],number_of_CTAs_per_MS,result,initial_index+executed_CTA,faulty_MS,block_executed_by_fauly_MS )
            executed_CTA += number_of_CTAs_per_MS
        



def Distributed_block_scheduler(CTA_list,to_schedule_CTAs_per_MS,number_of_MS_per_cluster,number_of_CTAs_per_MS, result_list, init_index,faulty_MS = -1, block_executed_by_fauly_MS= None):
    
    MS_thread_list = []
    n_touples = len(to_schedule_CTAs_per_MS)
    #print("n_couples : " +str(n_touples) + "\n")

    if(n_touples <= number_of_MS_per_cluster):
        for n in range(n_touples):
            ms_index,internal_init_index,n_CTA_per_current_MS = to_schedule_CTAs_per_MS[n]
            if(ms_index != faulty_MS):
                    MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler, args=(CTA_list[internal_init_index : internal_init_index+n_CTA_per_current_MS],
                                                                                                        n_CTA_per_current_MS,number_of_CTAs_per_MS,result_list,
                                                                                                        init_index+internal_init_index, -1, None)   ))
            else: 
                    MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler, args=(CTA_list[internal_init_index : internal_init_index+n_CTA_per_current_MS],
                                                                                                        n_CTA_per_current_MS,number_of_CTAs_per_MS,result_list,
                                                                                                        init_index+internal_init_index, faulty_MS, block_executed_by_fauly_MS)   ))                    

        for n in range(n_touples):
            MS_thread_list[n].start()
        for n in range(n_touples):
            MS_thread_list[n].join()
    else:
        n_cycles = int(n_touples/number_of_MS_per_cluster)
        uncompleted_cycle = n_touples %  number_of_MS_per_cluster
        for n_cycle in range(n_cycles):
            MS_thread_list = []
            for n in range(number_of_MS_per_cluster):
                ms_index,internal_init_index,n_CTA_per_current_MS = to_schedule_CTAs_per_MS[n+n_cycle*number_of_MS_per_cluster]
                if(ms_index != faulty_MS):
                    MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler, args=(CTA_list[internal_init_index : internal_init_index+n_CTA_per_current_MS],
                                                                                                        n_CTA_per_current_MS,number_of_CTAs_per_MS,result_list,
                                                                                                        init_index+internal_init_index, -1, None)   ))
                else: 
                    MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler, args=(CTA_list[internal_init_index : internal_init_index+n_CTA_per_current_MS],
                                                                                                        n_CTA_per_current_MS,number_of_CTAs_per_MS,result_list,
                                                                                                        init_index+internal_init_index, faulty_MS, block_executed_by_fauly_MS)   ))                    

            for n in range(number_of_MS_per_cluster):
                MS_thread_list[n].start()
            for n in range(number_of_MS_per_cluster):
                MS_thread_list[n].join()

        MS_thread_list = []
        for n_cycle in range(uncompleted_cycle):
            ms_index,internal_init_index,n_CTA_per_current_MS = to_schedule_CTAs_per_MS[n_cycle+n_cycles*number_of_MS_per_cluster]
            if(ms_index != faulty_MS):
                    MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler, args=(CTA_list[internal_init_index : internal_init_index+n_CTA_per_current_MS],
                                                                                                        n_CTA_per_current_MS,number_of_CTAs_per_MS,result_list,
                                                                                                        init_index+internal_init_index, -1, None)   ))
            else: 
                    MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler, args=(CTA_list[internal_init_index : internal_init_index+n_CTA_per_current_MS],
                                                                                                        n_CTA_per_current_MS,number_of_CTAs_per_MS,result_list,
                                                                                                        init_index+internal_init_index, faulty_MS, block_executed_by_fauly_MS)   ))                    
    
        for n in range(uncompleted_cycle):
            MS_thread_list[n].start()
        for n in range(uncompleted_cycle):
            MS_thread_list[n].join()
         





