# By Marshall Saltz
#REORGANIZE ALL THIS SHIT
import random
import numpy as np
import os
import json
import mutations
from addict import Dict
import matplotlib.pyplot as plt
import testing
import glob
import time
import main
from pathlib import Path
import basic_load
import combination

mutateTimes = 2 #Amount of mutated files per generation
file_name = []  #file name of hands
max_segs = 3  #Max amount of segments per hand
ext = ('.json')
ls = []
scoring = []
sortedScoring = []
totalFitness = []
print("Please input the integer number of generations you would like to run this for: ")
gen = int(input())  #generations ea runs for
for num in range(gen):  #run the script for num generations
    combine = combination.crossoverFunctions(num)
    firstList = mutations.mutate(mutateTimes, max_segs, num)
    ls.extend(firstList)
    main.MainScript()   
    
    file_content = testing.read_json("./../src/.user_info.json")
    location = "../hand_json_files/hand_queue_json/"

    file_content = testing.read_json("./../src/.user_info.json")
    tmpFitness = []
    for i in range(len(firstList)):
        rt = f"../output/{firstList[i].name}/hand"
        print(rt)
        file_name.append(f"{firstList[i].name}.json")
        sim_test = testing.sim_tester(firstList[i].name, rt, firstList[i])

        tmpFitness.append(sim_test.main(num))
        print("Fitness for " + str(file_name[-1]) + " is: " + str(tmpFitness[-1]))
        
        
    totalFitness.extend(tmpFitness)
    tmpFitness.clear()
   
    print("file_name: ", file_name)
    print("fitness: ", totalFitness)
    
    scoring = (np.array(list(zip(totalFitness, file_name))))   #Combines fitness scores with their files
    sortedScoring = (scoring[scoring[:,0].astype(float).argsort()]) #Sorts array by fittness scores

    fittestFirst = sortedScoring[-1][1] #Highest
    secondFittest = sortedScoring[-2][1]    #and second highest files
    
    
    print("first highest: ", str(fittestFirst))
    print("second highest: ", str(secondFittest))
    
    """
    Below calls all of the methods in combination. First, it turns the jsons into
    dictionaries. Next, it counts their segments. Then, it compares the segment counts and decides how to crossover the two files based on that.
    """
    childList = []
    f0 = os.path.expanduser('../hand_json_files/hand_archive_json/') + str(fittestFirst)
    par0 = combine.json_to_dictionaries(f0)
    
    f1 = os.path.expanduser('../hand_json_files/hand_archive_json/') + str(secondFittest)
    par1 = combine.json_to_dictionaries(f1)
    p0 = Dict()
    p1 = Dict()
    for i in range(len(ls)):
        if (str(ls[i].name) + ".json") == str(fittestFirst):
            p0 = ls[i]
            print("First parent: ", p0)
        if (str(ls[i].name) + ".json") == str(secondFittest):
            p1 = ls[i]
            print("Second parent", p1)
    d0, d1 = combine.combo(par0, par1, p0, p1, num)
    ls.append(d0)
    ls.append(d1)
    childList.append(d0)
    childList.append(d1)
    main.MainScript()
    
    file_content = testing.read_json("./../src/.user_info.json")
    location = os.path.expanduser("../hand_json_files/hand_queue_json/")
    

    file_content = testing.read_json("./../src/.user_info.json")

    folder = os.path.dirname("../output/")
    
    tmpFitness = []
    for i in range(len(childList)):
        rt = f"../output/{childList[i].name}/hand"
        print(rt)
        file_name.append(f"{childList[i].name}.json")
        sim_test = testing.sim_tester(childList[i].name, rt, firstList[i])
        tmpFitness.append(sim_test.main(num))
        print("Fitness for " + str(file_name[-1]) + " is: " + str(tmpFitness[-1]))
    totalFitness.extend(tmpFitness)
    tmpFitness.clear()
    childList.clear()
    print("file_name: ", file_name)
    print("fitness: ", totalFitness)         
    scoring = (np.array(list(zip(totalFitness, file_name))))
    
    sortedScoring = (scoring[scoring[:,0].astype(float).argsort()])

    fittestFirst = sortedScoring[-1][1]
    secondFittest = sortedScoring[-2][1]

    print(sortedScoring)
    firstList.clear()
plt.close('all')
print("The fittest of them all is: ", str(fittestFirst))
print("Runner up is: ", str(secondFittest))

name = sortedScoring[-1][1].split('.')[0]
rt = f"../output/{name}/hand"

fittest_file = f"{rt}/{name}.urdf"   
winning_ratios = Dict()    
for i in range(len(ls)):
    if ls[i].name == str(fittestFirst.split('.')[0]):
        winning_ratios = ls[i]
with open("../output/results.txt", mode="w") as resultsFile:
    resultsFile.write("The fittest of them all is: " + str(fittestFirst) + "\n")
    resultsFile.write("It's winning ratios are: "+ "\n")
    resultsFile.write(f"Palm: {winning_ratios.palm} To Fingers: {winning_ratios.fingers} and Proximal: {winning_ratios.proximal} To Distal: {winning_ratios.distal}\n")
    resultsFile.write("Location is: " + str(rt) + "\n")
    resultsFile.write("Runner up is: " + str(secondFittest) + "\n")
    resultsFile.write("Overall results are: \n" + str(sortedScoring) + "\n")
    resultsFile.close()
indicies = []
plt.figure()
plt.xlim(0, len(totalFitness))
plt.ylim(0, max(totalFitness)+1)
for i in range(len(totalFitness)):
    indicies.append(i)
plt.plot(indicies, totalFitness, color='blue', linestyle='solid')
plt.savefig("../output/fitness_trend")

basic_load.load(fittest_file)
