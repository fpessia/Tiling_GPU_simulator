import torch
import threading

def MS_executor(A,B,result,CTA_number):
    result[CTA_number] = torch.matmul(A,B)


def MS_simulator(input, number_of_CTAs_per_MS,result): #result is a list for by reference
    #divide the touples
    thread_list =[]
    for n in range(number_of_CTAs_per_MS):
        A,B = input[n]
        thread_list.append(threading.Thread(target=MS_executor, args=(A,B,result,n)))

    for n in range(number_of_CTAs_per_MS):
        thread_list[n].start()
    for n in range(number_of_CTAs_per_MS):
        thread_list[n].join()