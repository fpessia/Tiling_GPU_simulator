import torch
import random
from Tiling2D import Tiling2D


num_of_MS = 4
num_of_CTA_per_MS = 2


common_dim = random.randint(0 , 1000)
A = torch.randn(random.randint(0 , 1000),common_dim)
B = torch.randn(common_dim,random.randint(0 , 1000))

print("Testing Distributed block scheduling \n")
C = torch.matmul(A,B)
C_tilde = Tiling2D(A,B,num_of_MS,num_of_CTA_per_MS,"Distributed_block")
err = C - C_tilde
passed_test = True
x,y = C_tilde.size()
for i in range(x):
    for j in range(y):
        if err[i][j] != 0 :
            passed_test = False
if(passed_test):
    print("Test passed \n")
else:
    print("Test failed \n")
    print(C_tilde)
    print(C)
    
        