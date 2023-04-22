import random

def random_delay_generator_simulator(input_list, l):
    
    output_list = []
    for i in range(l):
        input_list.append(i)

    for i in range(l):
        if((len(input_list)-1) != 0):
            element = random.randint(0, len(input_list)-1)
            output_list.append(input_list[element])
            input_list.remove(input_list[element])
        else:
            output_list.append(input_list[0])
   
    
    return output_list

    
