import torch
import threading
import numpy

lock = threading.Lock()

def MS_executor(A,B,result,CTA_number,faulty_MS, block_executed_by_fauly_MS):
    global lock
    result[CTA_number] = torch.from_numpy(numpy.matmul(A.numpy(),B.numpy()))
    #result[CTA_number] = torch.matmul(A,B)
    if(faulty_MS != -1):
        lock.acquire()
        block_executed_by_fauly_MS.append(result[CTA_number])
        lock.release()


def MS_simulator_contiguos_index(input, number_of_CTAs_per_MS,result,initial_index,faulty_MS = -1, block_executed_by_fauly_MS =None): #result is a list for by reference
    #divide the touples
    thread_list =[]
    for n in range(number_of_CTAs_per_MS):
        A,B = input[n]
        thread_list.append(threading.Thread(target=MS_executor, args=(A,B,result,initial_index+n,faulty_MS, block_executed_by_fauly_MS)))

    for n in range(number_of_CTAs_per_MS):
        thread_list[n].start()
    for n in range(number_of_CTAs_per_MS):
        thread_list[n].join()


def MS_simulator_uncontiguos_index(input, number_of_CTAs_per_MS,result,initial_index,faulty_MS = -1, block_executed_by_fauly_MS =None): #result is a list for by reference
    #divide the touples
    thread_list =[]
    
    for n in range(number_of_CTAs_per_MS):
        A,B = input[n]
        thread_list.append(threading.Thread(target=MS_executor, args=(A,B,result,initial_index[n],faulty_MS, block_executed_by_fauly_MS)))

    for n in range(number_of_CTAs_per_MS):
        thread_list[n].start()
    for n in range(number_of_CTAs_per_MS):
        thread_list[n].join()