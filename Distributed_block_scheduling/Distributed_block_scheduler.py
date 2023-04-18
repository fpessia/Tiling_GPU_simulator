import torch
import threading
from Scheduler import MS_simulator,MS_executor


def MS_distributed_block_scheduler(sub_CTA_list, number_of_CTA_to_exe, number_of_CTAs_per_MS,result):
    executed_CTA = 0
    while(executed_CTA < number_of_CTA_to_exe):
        if ((number_of_CTA_to_exe- executed_CTA) < number_of_CTAs_per_MS):
            MS_simulator(sub_CTA_list[executed_CTA : number_of_CTA_to_exe],(number_of_CTA_to_exe- executed_CTA),result[executed_CTA : number_of_CTA_to_exe])
            executed_CTA = number_of_CTA_to_exe
        else:
            MS_simulator(sub_CTA_list[executed_CTA : executed_CTA+number_of_CTAs_per_MS],number_of_CTAs_per_MS,result[executed_CTA : executed_CTA+number_of_CTAs_per_MS])
            executed_CTA += number_of_CTAs_per_MS
        



def Distributed_block_scheduler(CTA_list,to_schedule_CTAs_per_MS,number_of_CTAs_per_MS):
    n_of_MS = len(to_schedule_CTAs_per_MS)
    MS_thread_list = []
    result = []
    for i in range(len(CTA_list)):
        result.append(0)
        
    for t in range(n_of_MS):
        if t == 0:
            MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler,args=(CTA_list[0 : to_schedule_CTAs_per_MS[t]],
                                                                             to_schedule_CTAs_per_MS[t],number_of_CTAs_per_MS,result[0 : to_schedule_CTAs_per_MS[t]])    ))           
        else :
            sum = 0
            for i in range(t):
                sum += to_schedule_CTAs_per_MS[t]
            MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler,args=(CTA_list[sum : sum+CTA_list[t]],
                                                                             to_schedule_CTAs_per_MS[t],number_of_CTAs_per_MS, result[sum : sum+CTA_list[t]]) ))
    for t in range(n_of_MS):
        MS_thread_list[t].start()
    for t in range(n_of_MS):
        MS_thread_list[t].join()

    return result


