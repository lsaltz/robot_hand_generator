# By Marshall Saltz
import random
import numpy as np
import os
import json
import mutations as mutation
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
     
    for l in range(5):
        recipient_dic = genList[random.randint(0,len(genList)-1)]
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
     minlen = min(len(evenDics), len(oddDics))       
     for m in range(5):
         newList.extend(crossover(evenDics[random.randint(0, (len(evenDics) - 1))], oddDics[random.randint(0, (len(oddDics) - 1))], generation, "eo", m, letter))
     return newList
     
def mut_on_first(tomutate, file_to_mutate, num, i):
    firstList = []
    
    
    c = combination.crossoverFunctions(num)
    for l in tomutate:
        if str(l['name']) == str(file_to_mutate):
            m0 = l
    
    
    m = mutation.Mutate(m0, num, i)
    firstList.append(m.build_hand())
    return firstList
 

def test(dicList, num):
    tmpFitness = []
    
    for l in dicList:
        
        gripper_name = l['name']
        
            
        w = nt.WorkSpace_Test(gripper_name, l)     
        #area_fit, angles_fit, straight_fit = w.main()

        fit = w.main()

        tmpFitness.append([fit, f"{gripper_name}.json"])
        
    return tmpFitness
    
 
    
    
    
def get_top_10(sortedScoring):
    top_ten = []
    top_ten.extend(sortedScoring[-15:])
    top_ten = list(map(lambda x:x[1].split('.')[0], top_ten))
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
    

def save_all_hands(ls, filename):
    with open(f"../output/{filename}.json", mode="w") as handsFile:
        new_j = json.dumps(ls)
        handsFile.write(new_j)
        handsFile.close()   

def get_data(filename, gen):
    data = []
    for i in range(gen):
        if i % 50 == 0 and i != 0: ################################change to 50!!!!!!!!!!!!!!!!
            with open(f"../output/{filename}{i}.json", mode="r") as p:
                data.extend(json.load(p))
    return data    

                      
if __name__ == "__main__":
    print("Please input the integer number of generations you would like to run this for: ")
    gen = int(input())+1  #generations ea runs for
    
    
    prev_gen = []
    ls = []    #total list of grippers
    cycle_fitness = []
    fitnesses = []
    genList = []
    mutations = []
    #mutationAngle = [] 
    #mutationStraight = [] 
    sortedScoring = []
    generational_fitness = []
    tmpList = []
    generational_fitness= []
    #sortedScoringArea = []
    #generational_fitness_angle = []
    #generational_fitness_straight = []
    combine = combination.crossoverFunctions(0)
    
    for n in range(30): ##########################CHANGE TO 30
        g0 = first_generation.First_Generation(0, n)
        tmpList.append(g0.build_hand())
    genList.extend(tmpList)
    
    #cycle_fitness.extend(test(tmpList, 0))
    ls.extend(tmpList)
    
    
    
    #firstArea = max(cycle_fitness, key=lambda item:item[0])[3].split(".")[0]
    #firstAngle = max(cycle_fitness, key=lambda item:item[1])[3].split(".")[0]
    #firstStraight = max(cycle_fitness, key=lambda item:item[2])[3].split(".")[0]
    mx = 20 ##########################CHANGE TO 20
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
    first= max(cycle_fitness, key=lambda item:item[0])[1].split(".")[0]
    cycle_fitness = sorted(cycle_fitness, key = lambda x: float(x[0]))
    topArea = get_top_10(cycle_fitness)
    #firstAngle = max(cycle_fitness, key=lambda item:item[1])[3].split(".")[0]
    #firstStraight = max(cycle_fitness, key=lambda item:item[2])[3].split(".")[0]
    
    
    fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
    #anglefitnesses = copy.deepcopy([t[1] for t in cycle_fitness])
    #straightfitnesses = copy.deepcopy([t[2] for t in cycle_fitness])
    
    generational_fitness.append(max(fitnesses))
    #generational_fitness_angle.append(max(anglefitnesses))
    #generational_fitness_straight.append(max(straightfitnesses))
    
    cycle_fitness.clear()
    fitnesses.clear()
    #anglefitnesses.clear()
    #straightfitnesses.clear()
    
    mutations.clear() 
    #mutationAngle.clear() 
    #mutationStraight.clear() 
    
    tmpList = copy.deepcopy(genList)
    
    for num in range(1, gen):
        
        genList = []
        cycle_fitness = []
        mutations = []
        

        
        #firstAngle = max(sortedScoring, key=lambda item:item[1])[3].split(".")[0]
        #firstStraight = max(sortedScoring, key=lambda item:item[2])[3].split(".")[0
            
        combine = combination.crossoverFunctions(num)    #set up crossover class
        
        mut_ran = []
        """
        for l in tmpList:
            if str(l['name']) == str(firstArea) or str(l['name']) == str(firstAngle) or str(l['name']) == str(firstStraight):
                genList.append(copy.deepcopy(l))
                tmpList.remove(l)
        """
        for i in range(5):
            mutt = copy.deepcopy(tmpList[random.randint(0,len(tmpList)-1)])
            mut_ran.extend(mut_on_first(tmpList, mutt.name, num, i))
            genList.append(mutt)
        for i in range(15):
            mutations.extend(mut_on_first(tmpList, topArea[i], num, (i+5)))
            genList.extend(copy.deepcopy([j for j in tmpList if j.name == topArea[i] and j not in genList]))
            
        #mutationAngle = mut_on_first(ls, firstAngle, num, "t")
        #mutationStraight = mut_on_first(ls, firstStraight, num, "s")
        genList.extend(mut_ran)
        genList.extend(mutations)
        
        #genList.extend(mutationAngle)
        #genList.extend(mutationStraight)
        
        
        cycle_fitness.extend(test(genList, num))
        

        ls.extend(genList)
        
    
    
        #carrierList1 = carrier(genList, tmpList, first, num, 'a')    #performs combination
        carrierList1 = carrier(genList, ls, first, num, 's')
        cycle_fitness.extend(test(carrierList1, num))
        #carrierList2 = carrier(genList, ls, firstAngle, num, 't')
        
        #cycle_fitness.extend(test(carrierList2, num))
        
        #cycle_fitness.extend(test(carrierList3, num))
        eoList = even_odd(genList, num, "eo")
        cycle_fitness.extend(test(eoList, num))
        genList.extend(carrierList1)
        #genList.extend(carrierList2)
        #genList.extend(carrierList3)
        genList.extend(eoList)
        
        ls.extend(genList)

        sortedScoring.extend(cycle_fitness)
        
        
        
        #firstAngle = max(sortedScoring, key=lambda item:item[1])[3].split(".")[0]
        #firstStraight = max(sortedScoring, key=lambda item:item[2])[3].split(".")[0]
        
        generational_fitness.append(max(cycle_fitness, key=lambda item:item[0])[0])
        #generational_fitness_angle.append(max(sortedScoring, key=lambda item:item[1])[1])
        #generational_fitness_straight.append(max(sortedScoring, key=lambda item:item[2])[2])
        tmpList.clear()
        tmpList = copy.deepcopy(genList)
        
        genList.clear()
        first = max(cycle_fitness, key=lambda item:item[0])[1].split(".")[0]
        cycle_fitness = sorted(cycle_fitness, key = lambda x: float(x[0]))
        #topArea = get_top_10(cycle_fitness) 
        topArea = get_top_10(cycle_fitness) 
        cycle_fitness.clear()
        first_fittest_dic = copy.deepcopy([i for i in ls if i['name'] == first])
        if (num % 50) == 0: ###########################################################CHANGE TO 50
            save_all_hands(ls, f"totallist{num}")
            save_all_hands(sortedScoring,f"sortedScoring{num}")
            save_all_hands(generational_fitness, f"generationalfitness{num}")
            ls.clear()
            sortedScoring.clear()
            generational_fitness.clear()
            ls.extend(first_fittest_dic)     
        
    sortedScoring = list(get_data("sortedScoring", gen))
    
    sortedScoring = sorted(sortedScoring, key = lambda x: float(x[0]))
    #sortedScoringAngle = sorted(sortedScoring, key = lambda x: float(x[1]))
    #sortedScoringStraight = sorted(sortedScoring, key = lambda x: float(x[2]))
    
    first = max(sortedScoring, key=lambda item:item[0])[1].split(".")[0]
    #firstAngle = max(sortedScoringAngle, key=lambda item:item[1])[3].split(".")[0]
    #firstStraight = max(sortedScoringStraight, key=lambda item:item[2])[3].split(".")[0]
    #topArea = get_top_10(sortedScoring)
    #topAngle = get_top_10(sortedScoringAngle)
    topArea = get_top_10(sortedScoring)
    ls = list([Dict(i) for i in get_data("totallist", gen)])
    
    save_all_hands(ls, "totallistfile")
    #write_to_file(ls, firstArea, sortedScoring, topArea, "area") #bottom)
    #write_to_file(ls, firstAngle, sortedScoringAngle, topAngle, "angle")
    write_to_file(ls, first, sortedScoring, topArea, "area")
    sortedScoring.clear()
    generational_fitness = list(get_data("generationalfitness", gen))
    plot_fitness(generational_fitness, gen, "a")
    #plot_fitness(generational_fitness_angle, gen, "t")
    #plot_fitness(generational_fitness, gen, "s")
    
    
    generate_json(ls, first)
    #generate_json(ls, firstAngle)
    #generate_json(ls, firstStraight)
    
    ls.clear()
    
    for top in topArea:
        name = top
        
        p = angles_plot.Plot(name)
        p.main()
    """
    for top in topAngle:
        name = top
        p = angles_plot.Plot(name)
        p.main()

    for top in topStraight:
        name = top
        p = angles_plot.Plot(name)
        p.main()
    """
#open_file(first)   
