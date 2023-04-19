import torch
import threading
from MS import MS_simulator


def MS_distributed_block_scheduler(sub_CTA_list, number_of_CTA_to_exe, number_of_CTAs_per_MS,result,initial_index):
    executed_CTA = 0
    while(executed_CTA < number_of_CTA_to_exe):
        if ((number_of_CTA_to_exe- executed_CTA) < number_of_CTAs_per_MS):
            MS_simulator(sub_CTA_list[executed_CTA : number_of_CTA_to_exe],(number_of_CTA_to_exe- executed_CTA),result, initial_index+executed_CTA )
            executed_CTA = number_of_CTA_to_exe
        else:
            MS_simulator(sub_CTA_list[executed_CTA : executed_CTA+number_of_CTAs_per_MS],number_of_CTAs_per_MS,result,initial_index+executed_CTA )
            executed_CTA += number_of_CTAs_per_MS
        



def Distributed_block_scheduler(CTA_list,to_schedule_CTAs_per_MS,number_of_CTAs_per_MS):

    A, B = CTA_list[0]
    xr,y1 = A.size()
    x1, yr = B.size()

    n_of_MS = len(to_schedule_CTAs_per_MS)
    MS_thread_list = []
    result = []
    for i in range(len(CTA_list)):
        result.append(torch.zeros(xr,yr))
        
    for t in range(n_of_MS):
        if t == 0:
            MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler,args=(CTA_list[0 : to_schedule_CTAs_per_MS[t]],
                                                                             to_schedule_CTAs_per_MS[t],number_of_CTAs_per_MS,result,0 )    ))           
        else :
            sum = 0
            for i in range(t):
                sum += to_schedule_CTAs_per_MS[i]
            MS_thread_list.append(threading.Thread(target=MS_distributed_block_scheduler,args=(CTA_list[sum : sum+to_schedule_CTAs_per_MS[t]],
                                                                             to_schedule_CTAs_per_MS[t],number_of_CTAs_per_MS, result,sum) ))
    for t in range(n_of_MS):
        MS_thread_list[t].start()
    for t in range(n_of_MS):
        MS_thread_list[t].join()

    return result


