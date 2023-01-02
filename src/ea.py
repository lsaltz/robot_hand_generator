# Apapted from Josh Campbell by Marshall Saltz

import random
import numpy as np
import os
import json
import mutations
from addict import Dict
import combination
import testing
import glob
import time
import main
from pathlib import Path
import basic_load

finger_0 = "finger_0"
finger_1 = "finger_1"
mutateTimes = 5

max_segs = 10
fitness = []
ext = ('.json')
print("Please input the integer number of generations you would like to run this for: ")
gen = int(input())
for num in range(gen):
    combine = combination.crossoverFunctions(gen)
    mutations.mutate(mutateTimes, max_segs, gen)
    
    main.MainScript()   

    
    file_content = testing.read_json("./../src/.user_info.json")
    location = "../hand_json_files/hand_queue_json/"
    
    directory = os.getcwd()

    file_content = testing.read_json("./../src/.user_info.json")
    file_name = []
    fitness = []

    folder = os.path.dirname("../output/")
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.urdf'):
                hand_name = os.path.basename((file).split('.')[0])
            
                print("hand_name: ", hand_name)
                hand_loc = root
                print("hand_loc: ", hand_loc)
                sim_test = testing.sim_tester(hand_name, hand_loc)
                file_name.append(hand_name + ".json")
                startTime = time.time()
                fitness.append(sim_test.main(startTime))
                print("Fitness for " + str(hand_name) + " is: " + str(fitness[-1]))
            
    print("file_name: ", file_name)
    print("fitness: ", fitness)
    
    scoring = np.array(list(zip(fitness, file_name)))
    columnIndex = 0
    sortedScoring = scoring[scoring[:,0].astype(int).argsort()]

    fittestFirst = sortedScoring[-1][1]
    secondFittest = sortedScoring[-2][1]
    
    
    print("first highest: ", str(fittestFirst))
    print("second highest: ", str(secondFittest))
   
    f0 = os.path.expanduser('~/robot_hand_generator_MLS/hand_json_files/hand_archive_json/') + str(fittestFirst)
    par0 = combine.json_to_dictionaries(f0)
    
    f1 = os.path.expanduser('~/robot_hand_generator_MLS/hand_json_files/hand_archive_json/') + str(secondFittest)
    par1 = combine.json_to_dictionaries(f1)

    count_0_0, count_0_1 = combine.segment_counter(par0)
    count_1_0, count_1_1 = combine.segment_counter(par1)
    print("Gen 0 finger 0: ", count_0_0)
    print("Gen 1 finger 0: ", count_1_0)
    print("Gen 0 finger 1: ", count_0_1)
    print("Gen 1 finger 1: ", count_1_1)

    crossover0_0, crossover1_0 = combine.segment_count_comparator(par0, par1, count_0_0, count_1_0, finger_0)
    crossover0_1, crossover1_1 = combine.segment_count_comparator(par0, par1, count_0_1, count_1_1, finger_1)

    combine.write_to_json(crossover0_0, crossover0_1, 0)
    combine.write_to_json(crossover1_0, crossover1_1, 1)
    
    main.MainScript()
    
    file_content = testing.read_json("./../src/.user_info.json")
    hand_names = []
    location = os.path.expanduser("~/robot_hand_generator_MLS/hand_json_files/hand_queue_json/")
    
    directory = os.getcwd()

    file_content = testing.read_json("./../src/.user_info.json")

    folder = os.path.dirname("../output/")
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.urdf'):
                hand_name = os.path.basename((file).split('.')[0])
            
                print("hand_name: ", hand_name)
                hand_loc = root
                print("hand_loc: ", hand_loc)
                sim_test = testing.sim_tester(hand_name, hand_loc)
        
                file_name.append(hand_name + ".json")
                startTime = time.time()
                fitness.append(sim_test.main(startTime))
                print("Fitness for " + str(hand_name) + " is: " + str(fitness[-1]))
         
    scoring = np.array(list(zip(fitness, file_name)))
    columnIndex = 0
    sortedScoring = scoring[scoring[:,0].astype(int).argsort()]

    fittestFirst = sortedScoring[-1][1]
    secondFittest = sortedScoring[-2][1]
    
    print(sortedScoring)

print("The fittest of them all is: ", str(fittestFirst))
print("Runner up is: ", str(secondFittest))

clearing_path = "../output/"

old_location = "../hand_json_files/hand_archive_json/" + str(fittestFirst)
new_location = "../hand_json_files/hand_queue_json/" + str(fittestFirst)

os.rename(old_location, new_location)


for root, dirs, files in os.walk(clearing_path):
    for file in files:
        os.remove(os.path.join(root, file))


main.MainScript() 
for root, dirs, files in os.walk(clearing_path):
    for file in files:
        if file.endswith('.urdf'):
            hand_name = os.path.basename(file)

            hand_loc = root
            
            fittest_file = os.path.join(root, hand_name)

with open("../results.txt", mode="w") as resultsFile:
    resultsFile.write("The fittest of them all is: " + str(fittestFirst))
    resultsFile.write("Location is: " + str(root))
    resultsFile.write("Runner up is: " + str(secondFittest))
    resultsFile.write("Overall results are: " + str(sortedScoring))
    resultsFile.close()

basic_load.load(fittest_file)