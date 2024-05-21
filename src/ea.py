# By Marshall Saltz
import random
import numpy as np
import os
import json
import mutations
from addict import Dict
import matplotlib.pyplot as plt
import time
import main
from pathlib import Path
import basic_load
import combination
import first_generation
import copy
import test as nt
import build_hand as bh
import angles_plot
#CHANGE PLOTTING FITNESS TO ANGLES_PLOT!

"""
Calls combine to combine two files
Parameters:
    p0: parent 0
    p1: parent 1
    num: generation number
    s: a letter indicating which mode of combining
    l: child index
"""
def crossover(p0, p1, num, s, l, letter):
    tmpList = []
    d0 = Dict()
    d1 = Dict()
    c = combination.crossoverFunctions(num)                   
    d0, d1 = c.combo(p0, p1, num, s, l, letter)
    tmpList.append(copy.deepcopy(d0))
    tmpList.append(copy.deepcopy(d1))
    return tmpList

"""
Acts like a pollen carrier to "spread" the fittest hand's genes to the other hands in the generation. Also loops
through even and odd dictionaries to combine them
Parameters:
    genList: generational list of grippers
    ls: total list of grippers
    first: gripper with highest fitness score
    generation: generation number
"""
def carrier(genList, ls, first, generation, letter):    
     
    newList = []
    fittest_dic = next((d for d in ls if d['name'] == first), None)
    name = fittest_dic['name']
     
    for l in range(len(genList)):
        recipient_dic = genList[l]
        newList.extend(crossover(fittest_dic, recipient_dic, generation, "w", l, letter))
    return newList

def even_odd(genList, generation, letter):
     oddDics = []
     evenDics = []
     newList = []
     for c in range(len(genList)):     
         if c%2 == 0:
             oddDics.append(copy.deepcopy(genList[c]))
         else:
             evenDics.append(copy.deepcopy(genList[c]))
             
     for m in range(min(len(evenDics), len(oddDics))):
         newList.extend(crossover(evenDics[m], oddDics[m], generation, "eo", m, letter))
     return newList
     
def mut_on_first(tomutate, file_to_mutate, num, i):
    firstList = []
    
    
    c = combination.crossoverFunctions(num)
    for l in tomutate:
        if str(l['name']) == str(file_to_mutate):
            m0 = l
    
    
    m = mutations.Mutate(m0, num, i)
    firstList.append(m.build_hand())
    return firstList
 

def test(dicList, num):
    tmpFitness = []
    
    for l in dicList:
        
        gripper_name = l['name']
        
            
        w = nt.WorkSpace_Test(gripper_name, l)     
        area_fit, angles_fit, straight_fit = w.main()

      
        tmpFitness.append([area_fit, angles_fit, straight_fit, f"{gripper_name}.json"])
        
    return tmpFitness
    
 
    
    
    
def get_top_10(sortedScoring):
    top_ten = []
    top_ten.extend(sortedScoring[-10:])
    top_ten = list(map(lambda x:x[3].split('.')[0], top_ten))
    return top_ten    
    
    
def write_to_file(ls, fittestFirst, sortedScoring, top_10, metric):#, bottom_10):
    winning_ratios = Dict()
    winning_file_names = []
    winning_10_ratios = []
    name = fittestFirst.split('.')[0]
    
    for i in range(len(ls)):
        if ls[i].name == str(fittestFirst.split('.')[0]):
            winning_ratios = ls[i]
    winning_file_names = top_10
    for x in range(len(ls)):
        if ls[x].name in winning_file_names:
              winning_10_ratios.append(ls[x])    
    with open(f"../output/results_{metric}.txt", mode="w") as resultsFile:
        resultsFile.write(f"The fittest of them all in {metric} is: " + str(fittestFirst) + "\n")
        resultsFile.write("Overall top 10 results are: \n" + str(sortedScoring[-10:]) + "\n")
        for j in range(len(winning_10_ratios)):
            resultsFile.write(f"{winning_10_ratios[j]}\n")
        #resultsFile.write("Overall bottom 10% results are: \n" + str(bottom_10) + "\n")
    resultsFile.close()    

def plot_fitness(generational_fitness, generations, letter):
    epochs = []
    plt.figure()
    plt.xlim(0, generations)
    plt.ylim(0, max(generational_fitness))
    for i in range(generations):
        epochs.append(i)
    plt.xlabel("Generation")
    plt.ylabel("Percentage of points reached")
    plt.title("Max fitness of each generation")
    generational_fitness = list(generational_fitness)
    plt.plot(epochs, generational_fitness, color='blue', linestyle='solid')
    plt.savefig(f"../output/fitness_trend_{letter}")
    with open(f"../output/generational_{letter}.json", mode="w") as resultsFile:
        new_j = json.dumps(list(zip(epochs, generational_fitness)))
        resultsFile.write(new_j)
    resultsFile.close()

def generate_json(ls, first):
    for l in ls:
        if l.name == str(first.split('.')[0]):
            hand_data = l
            break
    b = bh.Build_Json(l)
    b.build_hand()
    main.MainScript()
    
def open_file(fittestFirst):
    name = fittestFirst.split('.')[0]
    rt = f"../output/{name}/hand"
    fittest_file = f"{rt}/{name}.urdf"
    basic_load.load(fittest_file) 
    

def save_all_hands(ls):
    with open("../output/hands.json", mode="w") as handsFile:
        new_j = json.dumps(ls)
        handsFile.write(new_j)
        handsFile.close()    
                
if __name__ == "__main__":
    print("Please input the integer number of generations you would like to run this for: ")
    gen = int(input())+1  #generations ea runs for
    
    
    
    ls = []    #total list of grippers
    cycle_fitness = []
    fitnesses = []
    genList = []
    mutationArea = []
    mutationAngle = [] 
    mutationStraight = [] 
    sortedScoring = []
    generational_fitness = []
    tmpList = []
    generational_fitness_area = []
    generational_fitness_angle = []
    generational_fitness_straight = []
    combine = combination.crossoverFunctions(0)
    
    for n in range(50):
        g0 = first_generation.First_Generation(0, n)
        tmpList.append(g0.build_hand())
    genList.extend(tmpList)
    
    #cycle_fitness.extend(test(tmpList, 0))
    ls.extend(tmpList)
    
    
    
    #firstArea = max(cycle_fitness, key=lambda item:item[0])[3].split(".")[0]
    #firstAngle = max(cycle_fitness, key=lambda item:item[1])[3].split(".")[0]
    #firstStraight = max(cycle_fitness, key=lambda item:item[2])[3].split(".")[0]
    mx = 10
    #mut_ran = []
    
    for i in range(mx):
        genList.extend(mut_on_first(ls, ls[random.randint(0,len(ls)-1)].name, 0, i))
    #genList.extend(mut_ran)
    
    #mutationArea = mut_on_first(ls, firstArea, 0, "a")
    #mutationAngle = mut_on_first(ls, firstAngle, 0, "t")
    #mutationStraight = mut_on_first(ls, firstStraight, 0, "s")
    
    #genList.extend(mutationArea)
    #genList.extend(mutationAngle)
    #genList.extend(mutationStraight)
    
    cycle_fitness.extend(test(genList, 0))
    #cycle_fitness.extend(test(mutationArea, 0))
    #cycle_fitness.extend(test(mutationAngle, 0))
    #cycle_fitness.extend(test(mutationStraight, 0))
    
    #ls.extend(mutationArea)
    #ls.extend(mutationAngle)
    #ls.extend(mutationStraight)
    #ls.extend(mut_ran)
    
    sortedScoring.extend(cycle_fitness)
    ls.extend(genList)
    firstArea = max(cycle_fitness, key=lambda item:item[0])[3].split(".")[0]
    firstAngle = max(cycle_fitness, key=lambda item:item[1])[3].split(".")[0]
    firstStraight = max(cycle_fitness, key=lambda item:item[2])[3].split(".")[0]
    
    
    areafitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
    anglefitnesses = copy.deepcopy([t[1] for t in cycle_fitness])
    straightfitnesses = copy.deepcopy([t[2] for t in cycle_fitness])
    
    generational_fitness_area.append(max(areafitnesses))
    generational_fitness_angle.append(max(anglefitnesses))
    generational_fitness_straight.append(max(straightfitnesses))
    
    cycle_fitness.clear()
    areafitnesses.clear()
    anglefitnesses.clear()
    straightfitnesses.clear()
    
    mutationArea.clear() 
    mutationAngle.clear() 
    mutationStraight.clear() 
    
    tmpList = copy.deepcopy(genList)
    
    for num in range(1, gen):
        print(num)
        genList = []
        cycle_fitness = []
        areafitnesses = []
        anglefitnesses = []
        straightfitnesses = []
        
        firstArea = max(sortedScoring, key=lambda item:item[0])[3].split(".")[0]
        firstAngle = max(sortedScoring, key=lambda item:item[1])[3].split(".")[0]
        firstStraight = max(sortedScoring, key=lambda item:item[2])[3].split(".")[0]
            
        combine = combination.crossoverFunctions(num)    #set up crossover class
        
        mut_ran = []
        for l in tmpList:
            if str(l['name']) == str(firstArea) or str(l['name']) == str(firstAngle) or str(l['name']) == str(firstStraight):
                genList.append(l)
            
        for i in range(mx):
            mutt = tmpList[random.randint(0,len(tmpList)-1)]
            mut_ran.extend(mut_on_first(tmpList, mutt.name, num, i))
            genList.append(mutt)
        
        mutationArea = mut_on_first(ls, firstArea, num, "a")
        mutationAngle = mut_on_first(ls, firstAngle, num, "t")
        mutationStraight = mut_on_first(ls, firstStraight, num, "s")
        genList.extend(mut_ran)
        genList.extend(mutationArea)
        genList.extend(mutationAngle)
        genList.extend(mutationStraight)
        print(genList)
        
        
        cycle_fitness.extend(test(genList, num))
        ls.extend(genList)
        
    
    
        carrierList1 = carrier(genList, ls, firstArea, num, 'a')    #performs combination
        
        cycle_fitness.extend(test(carrierList1, num))
        carrierList2 = carrier(genList, ls, firstAngle, num, 't')
        
        cycle_fitness.extend(test(carrierList2, num))
        carrierList3 = carrier(genList, ls, firstStraight, num, 's')
        cycle_fitness.extend(test(carrierList3, num))
        eoList = even_odd(genList, num, "eo")
        cycle_fitness.extend(test(eoList, num))
        genList.extend(carrierList1)
        genList.extend(carrierList2)
        genList.extend(carrierList3)
        genList.extend(eoList)
        ls.extend(carrierList1)  #testing and getting scores of those combinations
        ls.extend(carrierList2) 
        ls.extend(carrierList3) 
        
        sortedScoring.extend(cycle_fitness)

        firstArea = max(sortedScoring, key=lambda item:item[0])[3].split(".")[0]
        firstAngle = max(sortedScoring, key=lambda item:item[1])[3].split(".")[0]
        firstStraight = max(sortedScoring, key=lambda item:item[2])[3].split(".")[0]
        
    
        areafitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
        anglefitnesses = copy.deepcopy([t[1] for t in cycle_fitness])
        straightfitnesses = copy.deepcopy([t[2] for t in cycle_fitness])
        generational_fitness_area.append(max(areafitnesses))
        generational_fitness_angle.append(max(anglefitnesses))
        generational_fitness_straight.append(max(straightfitnesses))
        tmpList.clear()
        tmpList = copy.deepcopy(genList)
        
        genList.clear()
        cycle_fitness.clear()
        areafitnesses.clear()
        anglefitnesses.clear()
        straightfitnesses.clear()
    
        
    
    sortedScoringArea = sorted(sortedScoring, key = lambda x: float(x[0]))
    sortedScoringAngle = sorted(sortedScoring, key = lambda x: float(x[1]))
    sortedScoringStraight = sorted(sortedScoring, key = lambda x: float(x[2]))
    
    firstArea = max(sortedScoringArea, key=lambda item:item[0])[3].split(".")[0]
    firstAngle = max(sortedScoringAngle, key=lambda item:item[1])[3].split(".")[0]
    firstStraight = max(sortedScoringStraight, key=lambda item:item[2])[3].split(".")[0]
    topArea = get_top_10(sortedScoringArea)
    topAngle = get_top_10(sortedScoringAngle)
    topStraight = get_top_10(sortedScoringStraight)
    
    save_all_hands(ls)
    write_to_file(ls, firstArea, sortedScoringArea, topArea, "area") #bottom)
    write_to_file(ls, firstAngle, sortedScoringAngle, topAngle, "angle")
    write_to_file(ls, firstStraight, sortedScoringStraight, topStraight, "straight")
    plot_fitness(generational_fitness_area, gen, "a")
    plot_fitness(generational_fitness_angle, gen, "t")
    plot_fitness(generational_fitness_straight, gen, "s")
    
    
    generate_json(ls, firstArea)
    generate_json(ls, firstAngle)
    generate_json(ls, firstStraight)
    
    for top in topArea:
        name = top
        
        p = angles_plot.Plot(name)
        p.main()
    for top in topAngle:
        name = top
        p = angles_plot.Plot(name)
        p.main()
    for top in topStraight:
        name = top
        p = angles_plot.Plot(name)
        p.main()
    #open_file(first)   
