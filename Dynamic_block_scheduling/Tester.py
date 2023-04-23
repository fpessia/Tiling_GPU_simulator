import torch
import random
from Tiling2D import Tiling2D
from Tiling2D import schedule_protocols

num_of_cluster = 3
num_of_MS_per_cluster = 4
num_of_CTA_per_MS = 3


print("Testing  all  scheduling techiniques \n")
for schedule in range(1):#len(schedule_protocols)
    n_correct = 0
    for i in range(5):
        common_dim = random.randint(0 , 1000)
        A = torch.randn(random.randint(0 , 1000),common_dim)
        B = torch.randn(common_dim,random.randint(0 , 1000))
     
        C = torch.matmul(A,B)
        C_tilde = Tiling2D(A,B,num_of_cluster,num_of_MS_per_cluster,num_of_CTA_per_MS,"Distributed_CTA")#schedule_protocols[schedule]

        err = C - C_tilde
        passed_test = True
        x,y = C_tilde.size()
        for i in range(x):
            for j in range(y):
                if err[i][j] >= 0.001 or err[i][j] <= -0.001:
                    passed_test = False

        if(passed_test):
            n_correct += 1
            print("Test passed \n")
        else:
            print("Test failed \n")
            print(C)
            print("\n\n")
            print(C_tilde)
            break
        
    acc = 100* n_correct/5  
    print ("acc over 5  tests" + str(acc)+ "%" + " of "+ str(schedule_protocols[schedule])+ "\n")
    
    
    
        