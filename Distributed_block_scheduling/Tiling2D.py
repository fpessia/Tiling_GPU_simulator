import torch
import threading
from Scheduler import Scheduler


tiling_strategies = [ "Not defined","Small", "Medium", "Large", "Tall", "Wide", "Huge"]

def zero_padding(tensor, x_init, y_init):
    
    x = x_init
    y = y_init

    if(x < 16) :
        x = 16
    if(y < 16):
        y = 16

    mod_x = x % 16  #the matrix must have dimentions that are multiples of 16 otherwise I cannot properly slice into blocks
    mod_y = y % 16

    if( mod_x != 0):
        while((x % 16) != 0):
            x += 1

    if( mod_y != 0):
        while((y % 16) != 0):
            y += 1

    tensor_padded = torch.zeros(x, y)
    tensor_padded[0 : x_init, 0 : y_init] = tensor

    return tensor_padded

def result_reordering(result_list,n_ms,n_ks,n_ns, x_space, y_space):
    C = torch.zeros(x_space*n_ms,y_space*n_ns)
    C_sublock = []
    for i in range(int(len(result_list)/n_ks)):
        for k in range(n_ks):
            if k == 0 :
                C_sublock.append(result_list[i*n_ks])
            else :
                C_sublock[i] += result_list[i *n_ks + k]
    
    for m in range(n_ms):
        for n in range(n_ns):
            C[m*x_space : (m+1)*x_space, n*y_space : (n+1)*y_space] = C_sublock[n_ns+n_ms]
    return C





def Tiling2D(tensor1, tensor2, number_of_MS, number_of_CTA_per_MS, scheduling_protocol):
    x1,y1 = tensor1.size()
    x2,y2 = tensor2.size()

    initial_x1 = x1
    initial_x2 = x2
    initial_y1 = y1
    initial_y2 = y2

    if( initial_y1 != initial_x2):
        print("Error invalid matrix dimentions for multiplication \n")
        return torch.zeros(x1,y2)

    strategy = tiling_strategies[0]

    #Zero padding
    tensor1_padded = zero_padding(tensor1, initial_x1, initial_y1)
    x1,y1 = tensor1_padded.size()
    tensor2_padded = zero_padding(tensor2, initial_x2, initial_y2)
    x2,y2 = zero_padding.size()

    #I have to decide the blocks size according to CUTLASS strategies of block sizing
    if((x1 % 128) == 0 and (y2 % 128) == 0):
        strategy = tiling_strategies[6]
    elif((x1 % 32) == 0 and (y2 % 128) == 0):
        strategy = tiling_strategies[5]
    elif((x1 % 128) == 0 and (y2 % 32) == 0):
        strategy = tiling_strategies[4]
    elif((x1 % 64)== 0 and (y2 % 64)):
        strategy = tiling_strategies[3]
    elif((x1 % 32) == 0 and (y2 % 32)== 0):
        strategy = tiling_strategies[2]
    elif((x1 % 16) == 0 and (y2 % 16)== 0):
        strategy = tiling_strategies[1]

    CTA_list = []
    if(strategy == "Huge"): 
        n_ms = x1/128
        n_ks = y1/8
        n_ns = y2/128

        for ms in range(n_ms):
            for ns in range(n_ns):
                for ks in range(n_ks):
                    A = tensor1_padded[128* ms : 128*(ms+1), 8*ks : 8*(ks +1)]
                    B = tensor2_padded[8*ks : 8*(ks +1), 128 * ns : 128 * (ns+1)] 
                    CTA_list.append((A,B)) 
        #Scheduler
        result_list= Scheduler(CTA_list, number_of_MS,number_of_CTA_per_MS,scheduling_protocol)
        C_padded = result_reordering(result_list,n_ms,n_ns,128,128)
        return C_padded[0: initial_x1, 0 : initial_y2]

    elif(strategy == "Wide"):
        n_ms = x1/32
        n_ks = y1/8
        n_ns = y2/128

        for ms in range(n_ms):
            for ns in range(n_ns):
               for ks in range(n_ks):
                   A = tensor1_padded[32* ms : 32*(ms+1), 8*ks : 8*(ks +1)]
                   B = tensor2_padded[8*ks : 8*(ks +1), 128 * ns : 128 * (ns+1)] 
                   CTA_list.append((A,B)) 
        #Scheduler
        result_list = Scheduler(CTA_list, number_of_MS,number_of_CTA_per_MS,scheduling_protocol)
        C_padded = result_reordering(result_list,n_ms,n_ns,32,128)
        return C_padded[0: initial_x1, 0 : initial_y2]

    elif(strategy == "Tall"):
        n_ms = x1/128
        n_ks = y1/8
        n_ns = y2/32

        for ms in range(n_ms):
           for ns in range(n_ns):
               for ks in range(n_ks):
                   A = tensor1_padded[128* ms : 128*(ms+1), 8*ks : 8*(ks +1)]
                   B = tensor2_padded[8*ks : 8*(ks +1), 32 * ns : 32 * (ns+1)] 
                   CTA_list.append((A,B)) 
        #Scheduler
        result_list = Scheduler(CTA_list, number_of_MS,number_of_CTA_per_MS,scheduling_protocol)
        C_padded = result_reordering(result_list,n_ms,n_ns,128,32)
        return C_padded[0: initial_x1, 0 : initial_y2]

    elif(strategy == "Large"):
        n_ms = x1/64
        n_ks = y1/8
        n_ns = y2/64

        for ms in range(n_ms):
           for ns in range(n_ns):
               for ks in range(n_ks):
                   A = tensor1_padded[64* ms : 64*(ms+1), 8*ks : 8*(ks +1)]
                   B = tensor2_padded[8*ks : 8*(ks +1), 64 * ns : 64 * (ns+1)] 
                   CTA_list.append((A,B)) 
        #Scheduler
        result_list = Scheduler(CTA_list, number_of_MS,number_of_CTA_per_MS,scheduling_protocol)
        C_padded = result_reordering(result_list,n_ms,n_ns,64,64)
        return C_padded[0: initial_x1, 0 : initial_y2]

    elif(strategy == "Medium"):
        n_ms = x1/32
        n_ks = y1/8
        n_ns = y2/32

        for ms in range(n_ms):
           for ns in range(n_ns):
               for ks in range(n_ks):
                   A = tensor1_padded[32* ms : 32*(ms+1), 8*ks : 8*(ks +1)]
                   B = tensor2_padded[8*ks : 8*(ks +1), 32 * ns : 32 * (ns+1)] 
                   CTA_list.append((A,B)) 
        #Scheduler
        result_list = Scheduler(CTA_list, number_of_MS,number_of_CTA_per_MS,scheduling_protocol)
        C_padded = result_reordering(result_list,n_ms,n_ns,32,32)
        return C_padded[0: initial_x1, 0 : initial_y2]
    elif(strategy == "Small"):
        n_ms = x1/16
        n_ks = y1/16
        n_ns = y2/16

        for ms in range(n_ms):
           for ns in range(n_ns):
               for ks in range(n_ks):
                   A = tensor1_padded[16* ms : 16*(ms+1), 8*ks : 8*(ks +1)]
                   B = tensor2_padded[8*ks : 8*(ks +1), 16 * ns : 16 * (ns+1)] 
                   CTA_list.append((A,B)) 
        #Scheduler
        result_list = Scheduler(CTA_list, number_of_MS,number_of_CTA_per_MS,scheduling_protocol)
        C_padded = result_reordering(result_list,n_ms,n_ns,16,16)
        return C_padded[0: initial_x1, 0 : initial_y2]
    else:
        print("Padding when wrong since no strategy from the available ones got chosed \n")
        return torch.zeros(initial_x1, initial_y2)
       
               

        

        
