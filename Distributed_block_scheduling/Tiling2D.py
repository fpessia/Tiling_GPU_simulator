import torch
import math
import threading

tiling_strategies = [ "Not defined","Small", "Medium", "Large", "Tall", "Wide", "Huge"]

def zero_padding(tensor, x_init, y_init):
    
    x = x_init
    y = y_init

    if(x < 16) :
        x = 16
    if(y < 16):
        y = 16

    mod_x = math.log2((x/16)) % 1  #the matrix must have dimentions that are power of 2  multiples of 16 otherwise I cannot properly apply Strassen's Algorithm
    mod_y = math.log2((y/16)) % 1 

    if( mod_x != 0):
        while( (math.log2((x/16)) % 1 ) != 0):
            x += 1

    if( mod_y != 0):
        while( (math.log2((y/16)) % 1 ) != 0):
            y += 1

    tensor_padded = torch.zeros(x, y)
    tensor_padded[0 : x_init, 0 : y_init] = tensor

    return tensor_padded
    



def Tiling2D(tensor1, tensor2):
    x1,y1 = tensor1.size()
    x2,y2 = tensor2.size()

    initial_x1 = x1
    initial_x2 = x2
    initial_y1 = y1
    initial_y2 = y2

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
        
        
