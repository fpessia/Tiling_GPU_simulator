import torch
import threading


def MS_executor(A,B,result,CTA_number):
    result[CTA_number] = torch.matmul(A,B)


def MS_simulator_contiguos_index(input, number_of_CTAs_per_MS,result,initial_index): #result is a list for by reference
    #divide the touples
    thread_list =[]
    for n in range(number_of_CTAs_per_MS):
        A,B = input[n]
        thread_list.append(threading.Thread(target=MS_executor, args=(A,B,result,initial_index+n)))

    for n in range(number_of_CTAs_per_MS):
        thread_list[n].start()
    for n in range(number_of_CTAs_per_MS):
        thread_list[n].join()


def MS_simulator_uncontiguos_index(input, number_of_CTAs_per_MS,result,initial_index): #result is a list for by reference
    #divide the touples
    thread_list =[]
    
    for n in range(number_of_CTAs_per_MS):
        A,B = input[n]
        thread_list.append(threading.Thread(target=MS_executor, args=(A,B,result,initial_index[n])))

    for n in range(number_of_CTAs_per_MS):
        thread_list[n].start()
    for n in range(number_of_CTAs_per_MS):
        thread_list[n].join()