# Tiling_GPU_simulator
simulation of GPU behaviour for matrix multiplication in DNN forward methods

HOW TO USE TILING2D MODULE:

(i) import Tiling2D function and schedule_protocol list from Tiling2D module in Dynamic_block_scheduling dir


(ii) Provide to the function the following inputs:
    
    a) tensorA and tensor B to multiply with arbitrary dimentions
    
    
    b) number_of_cluster, number_of_MS_per_cluster, number_of_CTA_per_MS that define the HW of the simulated GPU
       behaviour
    
    c) the desired scheduling protocol from those scpecified by the imported list
    
    
    d) square tiling (avilable sizes 16x16,32x32,64x64,128x128)
       if user wants to select default optimized tiling this parameter should be zero(tiling = 0) 
    
    
    e) faulty multiprocessor, this should be an absolute value in range [0 : (number_of_cluster*number_of_MS_per_cluster) -1] .
       If all multiprocessors are not faulty this parameter must be setted to -1 
    
    
    f) A list passed by refernce that will be updated with all the blocks executed by faulty MS, must be setted to None if all
        multiprocessors are not faulty


(iii) The function will return an output tensor which is the result of tensor moltiplication




DISTRIBUTED BLOCK SCHEDULER

- Distributed block passed 100/100 test with error range 0.01

- Distributed block passed  100 % over 20 test with error range 0.001

- Distributed block passed  96.66 % over 30 test with error range 0.0001

DISTRIBUTED CTA SCHEDULER 
- Distributed CTA passed 100 % over 20 test with error range 0.001
- Distributed CTA passed  96.66 % over 30 test with error range 0.0001

GREEDY-CLUSTERING-SCHEDULER
- greedy-clustering scheduler passed  100 % over 20 test with error range 0.001
- greedy-clustering scheduler passed  96.66 % over 30 test with error range 0.0001

GLOBAL ROUND ROBIN SCHEDULER
- global round robin scheduler passed 100 % over 20 test with error range 0.001
- global round robin scheduler passed  93.33 % over 30 test with error range 0.0001

TWO LEVEL ROUND ROBIN SCHEDULER
- Two level round robin scheduler passed 100 % over 20 test with error range 0.001