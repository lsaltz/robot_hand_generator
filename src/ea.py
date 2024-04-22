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





class coordinate_generation:
        
    def angles_coordinates():
        finger_z = 0.2
        val = 0.01
    
        total_height = 0.2
        
        bottom_x = -abs(total_height)
        bottom_y = -abs(total_height)
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = 8
      
        center_pt = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        
        x1 = [(c[0] + (np.cos(a)*self.rad)) for c in center_pt for a in angles]
    
   
        y1 = [(c[1] + (np.sin(a)*self.rad)) for c in center_pt for a in angles]
        
        coords1 = list(zip(x1, y1))
        angles = [a+np.pi for a in angles]
        x2 = [(c[0] + (np.cos(a)*self.rad)) for c in center_pt for a in angles]
    
   
        y2 = [(c[1] + (np.sin(a)*self.rad))for c in center_pt for a in angles]
        
        coords2 = list(zip(x2, y2))
        
        c1 = np.reshape(np.asarray(coords1), (-1, n, 2))
        c2 = np.reshape(np.asarray(coords2), (-1, n, 2))
          
        r = np.asarray(coords1)
        l = np.asarray(coords2)
        
        return center_pt, c1, c2

    def straight_coordinates():
        finger_z = 0.2
        val = 0.01
    
        total_height = 0.2
        coords1 = []
        coords2 = []
        bottom_x = -abs(total_height)
        bottom_y = -abs(total_height)
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = 8
        rad = 0.039
      
        center_pt = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        x1 = [(c[0] + rad) for c in center_pt]
        y1 = [c[1] for c in center_pt]
        
        
        coords1 = list(zip(x1, y1))
        
        x2 = [(c[0] - rad) for c in center_pt]
        y2 = [c[1] for c in center_pt]
        
        coords2 = list(zip(x2, y2))
        
        
        r = np.asarray(coords1)
        l = np.asarray(coords2)
        
        return center_pt, r, l
"""
Calls combine to combine two files
Parameters:
    p0: parent 0
    p1: parent 1
    num: generation number
    s: a letter indicating which mode of combining
    l: child index
"""
def crossover(p0, p1, num, s, l):
    tmpList = []
    d0 = Dict()
    d1 = Dict()
    c = combination.crossoverFunctions(num)                   
    d0, d1 = c.combo(p0, p1, num, s, l)
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
def carrier(genList, ls, first, generation):    ###
     oddDics = []
     evenDics = []
     newList = []
     fittest_dic = next((d for d in ls if d['name'] == first), None)
     name = fittest_dic['name']
     
     for l in range(len(genList)):
         recipient_dic = genList[l]
         newList.extend(crossover(fittest_dic, recipient_dic, generation, "w", l))
     for c in range(len(newList)):     
         if c%2 == 0:
             oddDics.append(copy.deepcopy(newList[c]))
         else:
             evenDics.append(copy.deepcopy(newList[c]))
             
     for m in range(min(len(evenDics), len(oddDics))):
         newList.extend(crossover(evenDics[m], oddDics[m], generation, "eo", m))
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
 

def test(dicList, num, coords0, coords1):
    tmpFitness = []
    name0 = "finger_0"
    name1 = "finger_1"
    
    
    for l in dicList:
        print(l.name)
        links0 = []
        links1 = []
        gripper_name = l['name']
        width = l.length.palm
        length0 = l.length.finger_0
        
        for i in l.ratio.segs.finger_0:
            links0.append(length0*(i/100))
        
        if len(links0) == 2:
            links0.append(0)
            
        w0 = nt.WorkSpace_Test(links0, width, name0, coords0)     
        i0, p0 = w0.main()

        length1 = l.length.finger_1
        
        for i in l.ratio.segs.finger_1:
            links1.append(length1*(i/100))
            
        if len(links1) == 2:
            links1.append(0)
            
        w1 = nt.WorkSpace_Test(links1, 0, name1, coords1)
        i1, p1 = w1.main()
        f = nt.WorkSpace_Fitness(i0, i1, p0, p1).main()
        print(f)
        tmpFitness.append([f, f"{gripper_name}.json"])
        
    return tmpFitness
    
 
    
    
    
def get_top_10(sortedScoring):
    top_ten = []
    top_ten.extend(sortedScoring[-10:])
    top_ten = list(map(lambda x:x[1].split('.')[0], top_ten))
    return top_ten    
    
    
def write_to_file(ls, fittestFirst, sortedScoring, top_10):#, bottom_10):
    winning_ratios = Dict()
    winning_file_names = []
    winning_10_ratios = []
    name = fittestFirst.split('.')[0]
    rt = f"../output/{name}/hand"
    for i in range(len(ls)):
        if ls[i].name == str(fittestFirst.split('.')[0]):
            winning_ratios = ls[i]
    winning_file_names = top_10
    for x in range(len(ls)):
        if ls[x].name in winning_file_names:
              winning_10_ratios.append(ls[x])    
    with open("../output/results.txt", mode="w") as resultsFile:
        resultsFile.write("The fittest of them all is: " + str(fittestFirst) + "\n")
        resultsFile.write("Overall top 10 results are: \n" + str(sortedScoring[-10:]) + "\n")
        for j in range(len(winning_10_ratios)):
            resultsFile.write(f"{winning_10_ratios[j]}\n")
        #resultsFile.write("Overall bottom 10% results are: \n" + str(bottom_10) + "\n")
    resultsFile.close()    

def plot_fitness(generational_fitness, generations):
    epochs = []
    plt.figure()
    plt.xlim(0, generations)
    plt.ylim(0, 1)
    for i in range(generations):
        epochs.append(i)
    plt.xlabel("Generation")
    plt.ylabel("Percentage of points reached")
    plt.title("Max fitness of each generation")
    generational_fitness = list(generational_fitness)
    plt.plot(epochs, generational_fitness, color='blue', linestyle='solid')
    plt.savefig("../output/fitness_trend")
    with open("../output/generational.json", mode="w") as resultsFile:
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
    
def coordinate_array(val):
    finger_z = 0.2
    
    
    total_height = 0.2
    coords0 = []
    coords1 = []
    bottom_x = -abs(total_height)
    bottom_y = -0.2
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = 10
    column_points = 10
    n = 4
    rad = 0.0195
    
    center_pt = [[x, y, 0] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
    
    x1 = [(c[0] + (np.cos(np.pi/n*x + np.pi/2)*rad)) for c in center_pt for x in range(0, n+1)]
    
   
    y1 = [(c[1] + (np.sin(np.pi/n*x + np.pi/2)*rad)) for c in center_pt for x in range(0, n+1)]
    
    coords0 = np.asarray(list(zip(x1, y1)))
    x2 = [(c[0] + (np.cos(np.pi/n*x+np.pi + np.pi/2)*rad)) for c in center_pt for x in reversed(range(0, n+1))]
    
    y2 = [((c[1] - (np.sin(np.pi/n*x+np.pi + np.pi/2)*rad))) for c in center_pt for x in reversed(range(0, n+1))]
    
    
    coords1 = np.asarray(list(zip(x2, y2)))
    """
    c1 = np.reshape(np.asarray(coords0), (-1, n+1, 3)).tolist()
    
    c2 = np.reshape(np.asarray(coords1), (-1, n+1, 3)).tolist()
    
    c = []
    
    for i in range(len(center_pt)):
        c3 = [center_pt[i], c1[i], c2[i]]
        c.append(c3)
    """ 
    return coords0, coords1

def save_all_hands(ls):
    with open("../output/hands.json", mode="w") as handsFile:
        new_j = json.dumps(ls)
        handsFile.write(new_j)
        handsFile.close()    
                
if __name__ == "__main__":
    print("Please input the integer number of generations you would like to run this for: ")
    gen = int(input())+1  #generations ea runs for
    val = 0.03
    cent_a, r_a, l_a = coordinate_generation.angles_coordinates()
    cent_s, r_s, l_s = coordinate_generation.straight_coordinates()
    
    ls = []    #total list of grippers
    cycle_fitness = []
    fitnesses = []
    genList = []
    mutatedList = []
    sortedScoring = []
    generational_fitness = []
    tmpList = []
    combine = combination.crossoverFunctions(0)
    for n in range(10):
        g0 = first_generation.First_Generation(0, n)
        tmpList.append(g0.build_hand())
    genList.extend(tmpList)
    
    cycle_fitness.extend(test(tmpList, 0, coords0, coords1))
    ls.extend(tmpList)
    
    
    
    first = max(cycle_fitness, key=lambda item:item[0])[1].split(".")[0]
    mx = 5
    mut_ran = []
    for i in range(mx):
        mut_ran.extend(mut_on_first(ls, ls[random.randint(0,len(ls)-1)].name, 0, i))
    mutatedList = mut_on_first(ls, first, 0, "f")   #performs mutations on first fittest file overall
    genList.extend(mut_ran)
    genList.extend(mutatedList)
    
    
    cycle_fitness.extend(test(mut_ran, 0, coords0, coords1))
    cycle_fitness.extend(test(mutatedList, 0, coords0, coords1))
    
    ls.extend(mutatedList)
    ls.extend(mut_ran)
    
    sortedScoring.extend(cycle_fitness)
    
    first = max(sortedScoring, key=lambda item:item[0])[1]
    
    
    fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
    generational_fitness.append(max(fitnesses))
    cycle_fitness.clear()
    fitnesses.clear()
    
    mutatedList.clear() 
    tmpList = copy.deepcopy(genList)
    
    for num in range(1, gen):
        genList = []
        cycle_fitness = []
        fitnesses = []
        
        first = max(sortedScoring, key=lambda item:item[0])[1].split('.')[0]
        
        combine = combination.crossoverFunctions(num)    #set up crossover class
        
        mut_ran = []
        for i in range(mx):
            mut_ran.extend(mut_on_first(tmpList, tmpList[random.randint(0,len(tmpList)-1)].name, num, i))
        mutatedList = mut_on_first(ls, first, num, "f")   #performs mutations on first fittest file overall
        genList.extend(mut_ran)
        genList.extend(mutatedList)
        
        cycle_fitness.extend(test(genList, num, coords0, coords1))
        ls.extend(genList)
        
    
    
        carrierList = carrier(genList, ls, first, num)    #performs combination
        genList.extend(carrierList)
        cycle_fitness.extend(test(carrierList, num, coords0, coords1))
        ls.extend(carrierList)  #testing and getting scores of those combinations
        
        
        sortedScoring.extend(cycle_fitness)
        
        
        
        
        first = max(sortedScoring, key=lambda item:item[0])[1].split('.')[0]
        
    
        fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
        generational_fitness.append(max(fitnesses))   #get max fitness of that generation
        tmpList = copy.deepcopy(genList)
        
        genList.clear()
        fitnesses.clear()
        cycle_fitness.clear()
        
    
    sortedScoring = sorted(sortedScoring, key = lambda x: float(x[0]))
    first = max(sortedScoring, key=lambda item:item[0])[1]
    top = get_top_10(sortedScoring)
    
    
    save_all_hands(ls)
    write_to_file(ls, first, sortedScoring, top) #bottom)
    plot_fitness(generational_fitness, gen)
    
    
    generate_json(ls, first)
    open_file(first)   
