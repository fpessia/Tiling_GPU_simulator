import torch
import random
import numpy
from Tiling2D import Tiling2D
from Tiling2D import schedule_protocols

num_of_cluster = 3
num_of_MS_per_cluster = 4
num_of_CTA_per_MS = 3

faulty_BLOCK = [] 

print("Testing  all  scheduling techiniques \n")
for schedule in range(len(schedule_protocols)):#
    n_correct = 0
    for i in range(30):
        common_dim = random.randint(0 , 1000)
        A = torch.randn(random.randint(0 , 1000),common_dim)
        B = torch.randn(common_dim,random.randint(0 , 1000))
     
        C =  torch.from_numpy(numpy.matmul(A.numpy(),B.numpy()))# torch.matmul(A,B)
        faulty_BLOCK = [] 
        C_tilde = Tiling2D(A,B,num_of_cluster,num_of_MS_per_cluster,num_of_CTA_per_MS,schedule_protocols[schedule], -1, faulty_BLOCK)

        err = C - C_tilde
        passed_test = True
        x,y = C_tilde.size()
        for i in range(x):
            for j in range(y):
                if err[i][j] >= 0.0001 or err[i][j] <= -0.0001:
                    passed_test = False
                    print(C_tilde[i][j])
                    print(C[i][j])
                    print("\n")

        if(passed_test):
            n_correct += 1
            
            #print(faulty_BLOCK)
            #print("Test passed \n")
        else:
            print("Test failed \n")
            
            #print(C)
            #print("\n\n")
            #print(C_tilde)
            
    #print(faulty_BLOCK)   
    acc = 100* n_correct/30  
    print ("acc over 30  tests" + str(acc)+ "%" + " of "+ str(schedule_protocols[schedule])+ "\n")
    
    
    
    
        