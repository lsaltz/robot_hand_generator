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
import mutations2
"""
def test()
def mut()
def init()
def get_fitness()
def 

"""
print("Please input the integer number of generations you would like to run this for: ")
gen = int(input())  #generations ea runs for
mutateTimes = 2 #Amount of mutated files per generation
file_name = []  #file name of hands
max_segs = 3  #Max amount of segments per hand
ext = ('.json')
ls = []
scoring = []
sortedScoring = []
totalFitness = []
bottom_10 = []
top_10 = []
hd = []
tmpFitness = []
file_name = []
rt = []
rd, firstList = mutations.mutate(max_segs, 0)
firstList.extend(mutations2.mutate(mutateTimes, max_segs, rd, firstList[0], 0))
ls.extend(firstList)
main.MainScript()
for i in range(len(firstList)):
    file_name.append(f"{firstList[i].name}.json")
    file_content = testing.read_json("./../src/.user_info.json")
    rt = f"../output/{firstList[i].name}/hand"
    sim_test = testing.sim_tester(firstList[i].name, rt, firstList[i])
    tmpFitness.append(sim_test.main(0))
totalFitness.extend(tmpFitness)
tmpFitness.clear()

scoring = (np.array(list(zip(totalFitness, file_name))))   #Combines fitness scores with their files
sortedScoring = (scoring[scoring[:,0].astype(float).argsort()]) #Sorts array by fittness scores

fittestFirst = sortedScoring[-1][1] #Highest
secondFittest = sortedScoring[-2][1]    #and second highest files
for num in range(1, gen):  #run the script for num generations
    combine = combination.crossoverFunctions(num)

    location = "../hand_json_files/hand_queue_json/"

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

    for i in range(len(childList)):
        rt = f"../output/{childList[i].name}/hand"
        print(rt)
        file_name.append(f"{childList[i].name}.json")
        sim_test = testing.sim_tester(childList[i].name, rt, childList[i])
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
    firstList.clear()

    for i in range(len(ls)):
        if (str(ls[i].name) + ".json") == str(fittestFirst):
            m0 = ls[i]
    m_d = combine.json_to_dictionaries(f"../hand_json_files/hand_archive_json/{fittestFirst}")
    firstList.extend(mutations2.mutate(mutateTimes, max_segs, m_d, m0, num))
    main.MainScript()
    for i in range(len(firstList)):
        rt = f"../output/{firstList[i].name}/hand"
        file_name.append(f"{firstList[i].name}.json")
        sim_test = testing.sim_tester(firstList[i].name, rt, firstList[i])

        tmpFitness.append(sim_test.main(num))
        print("Fitness for " + str(file_name[-1]) + " is: " + str(tmpFitness[-1]))
    ls.extend(firstList)
    firstList.clear()

    scoring = (np.array(list(zip(totalFitness, file_name))))
    sortedScoring = (scoring[scoring[:,0].astype(float).argsort()])
    fittestFirst = sortedScoring[-1][1]
    secondFittest = sortedScoring[-2][1]
sortedScoring = sortedScoring.tolist()    
length = len(sortedScoring)
ten_perc = (int)(0.1 * length)
if ten_perc == 0:
    ten_perc = 1
top_10.extend(sortedScoring[(length-ten_perc):])
bottom_10.extend(sortedScoring[0:ten_perc])
for i in range(len(top_10)):
    n = top_10[i][1]
    coordsR = []
    nr_R = []
    coordsL = []
    nr_L = []
    with open(f"../output/{n}", mode="r") as f:
        fi = json.load(f)
        dictionary = Dict(fi)
        coordsR.extend(dictionary.finger_0.reached)
        coordsL.extend(dictionary.finger_1.reached)
        nr_R.extend(dictionary.finger_0.not_reached)
        nr_L.extend(dictionary.finger_1.not_reached)
        g_name = dictionary.name + "_winner" + ".png"
        figure, axis = plt.subplots(3, 1)
        axis[0].set_title("Finger 0")
        axis[1].set_title("Finger 1")
        axis[2].set_title("Total")
        axis[0].set_aspect('equal', 'box')
        axis[1].set_aspect('equal', 'box')
        axis[2].set_aspect('equal', 'box')
        for k in range(len(nr_R)):
            axis[0].scatter(nr_R[k][0], nr_R[k][1], color='red')
            axis[2].scatter(nr_R[k][0], nr_R[k][1], color='red')
        for z in range(len(nr_L)):
            axis[1].scatter(nr_L[z][0], nr_L[z][1], color='red')
            axis[2].scatter(nr_L[z][0], nr_L[z][1], color='red')
        for j in range(len(coordsR)):
            axis[0].scatter(coordsR[j][0], coordsR[j][1], color='blue')
            axis[2].scatter(coordsR[j][0], coordsR[j][1], color='blue')
        for x in range(len(coordsL)):   
            axis[1].scatter(coordsL[x][0], coordsL[x][1], color='blue')
            axis[2].scatter(coordsL[x][0], coordsL[x][1], color='blue')
        plt.savefig(f"../output/{g_name}")
        plt.close('all')
        
for i in range(len(bottom_10)):
    n = bottom_10[i][1]
    coordsR = []
    nr_R = []
    coordsL = []
    nr_L = []
    with open(f"../output/{n}", mode="r") as f:
        fi = json.load(f)
        dictionary = Dict(fi)
        coordsR.extend(dictionary.finger_0.reached)
        coordsL.extend(dictionary.finger_1.reached)
        nr_R.extend(dictionary.finger_0.not_reached)
        nr_L.extend(dictionary.finger_1.not_reached)
        g_name = dictionary.name + "_loser" + ".png"
        figure, axis = plt.subplots(3, 1)
        axis[0].set_title("Finger 0")
        axis[1].set_title("Finger 1")
        axis[2].set_title("Total")
        axis[0].set_aspect('equal', 'box')
        axis[1].set_aspect('equal', 'box')
        axis[2].set_aspect('equal', 'box')
        for k in range(len(nr_R)):
            axis[0].scatter(nr_R[k][0], nr_R[k][1], color='red')
            axis[2].scatter(nr_R[k][0], nr_R[k][1], color='red')
        for z in range(len(nr_L)):
            axis[1].scatter(nr_L[z][0], nr_L[z][1], color='red')
            axis[2].scatter(nr_L[z][0], nr_L[z][1], color='red')
        for j in range(len(coordsR)):
            axis[0].scatter(coordsR[j][0], coordsR[j][1], color='blue')
            axis[2].scatter(coordsR[j][0], coordsR[j][1], color='blue')
        for x in range(len(coordsL)):   
            axis[1].scatter(coordsL[x][0], coordsL[x][1], color='blue')
            axis[2].scatter(coordsL[x][0], coordsL[x][1], color='blue')
        plt.savefig(f"../output/{g_name}")         
        plt.close('all')
        


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
    resultsFile.write("Overall top 10% results are: \n" + str(top_10) + "\n")
    resultsFile.write("Overall bottom 10% results are: \n" + str(bottom_10) + "\n")
    resultsFile.close()
indicies = []
plt.figure()
plt.xlim(0, len(totalFitness))
plt.ylim(0, max(totalFitness)+1)
for i in range(len(totalFitness)):
    indicies.append(i)
plt.plot(indicies, totalFitness, color='blue', linestyle='solid')
plt.savefig("../output/fitness_trend")
print("The fittest of them all is: ", str(fittestFirst))
print("Runner up is: ", str(secondFittest))
basic_load.load(fittest_file)

