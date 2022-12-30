# Apapted from Josh Campbell by Marshall Saltz

import random
import numpy as np
import os
import json
import shutil
import mutations
import crossover
from addict import Dict
import combination
import testing

combine = combination.crossoverFunctions()
finger_0 = "finger_0"
finger_1 = "finger_1"
mutateTimes = 5
gen = 10
max_segs = 10


for num in range(gen):
    mutations.mutate(mutateTimes, max_segs, gen)
    if num%2 == 0:
        f0 = '../test/hand_mut_'+str(num)+'.json'
    else:
        f1 = '../test/hand_mut_'+str(num)+'.json'

    par0 = combine.json_to_dictionaries(f0)
    par1 = combine.json_to_dictionaries(f1)

    count_0_0, count_0_1 = combine.segment_counter(par0)
    count_1_0, count_1_1 = combine.segment_counter(par1)
    print("Gen 0 finger 0: ", count_0_0)
    print("Gen 1 finger 0: ", count_1_0)
    print("Gen 0 finger 1: ", count_0_1)
    print("Gen 1 finger 1: ", count_1_1)

    crossover0_0, crossover1_0 = combine.segment_count_comparator(par0, par1, count_0_0, count_1_0, finger_0)
    crossover0_1, crossover1_1 = combine.segment_count_comparator(par0, par1, count_0_1, count_1_1, finger_1)

    combine.write_to_json(crossover0_0, crossover0_1, 0, gen)
    combine.write_to_json(crossover1_0, crossover1_1, 1, gen)
    combine.destructor()
    
    directory = os.getcwd()

    file_content = test.read_json("./../src/.user_info.json")
    folders = []
    hand_names = []
    for folder in glob.glob(f'{file_content["hand_model_output"]}*/'):
        folders.append(folder)


    for i, hand in enumerate(folders):
        temp_hand = hand.split('/')
        hand_names.append(temp_hand[-2])
        print(f'{i}:   {temp_hand[-2]}')
        num = temp_hand[-2]    
        
    for i in range(num):
        hand_name = hand_names[num]
        hand_loc = folders[num]
        
        sim_test = testing.sim_tester(hand_name, hand_loc)
        startTime = time.time()
        while (time.time() - startTime) < 600:
            for i in range(10):
                fitness = sim_test.main(startTime)
                print("Fitness for " + hand_name + " is: " + fitness)
                print("The lower the score the better. I think."
                
                """
                1. pass segment counts to sim test
                2. fitness function
                """