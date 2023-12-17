# By Marshall Saltz
import random
import numpy as np
import os
import json
import mutations
from addict import Dict
import matplotlib.pyplot as plt
import testing
import time
import main
from pathlib import Path
import basic_load
import combination
import first_generation
import copy
import pandas as pd
import shutil
import sqlite3

if __name__ == "__main__":
    print("Please input the integer number of generations you would like to run this for: ")
    gen = int(input())+1  #generations ea runs for
    connection1 = sqlite3.connect('hand_points.db')
    connection2 = sqlite3.connect('hand_json.db')
    cr1 = connection1.cursor()
    cr2 = connection2.cursor()
    cr1.execute("drop table if exists hand_data")
    cr2.execute("drop table if exists hand_files")
    cr1.execute("create table hand_data (ID, name, data)")
    cr2.execute("create table hand_files (ID, name, data)")
    print("generating coordinate array...")
    val = 0.05
    coords0, coords1 = coordinate_array(val)
    
    ls = []    #total list of grippers
    cycle_fitness = []
    fitnesses = []
    genList = []
    mutatedList = []
    sortedScoring = []
    generational_fitness = []
    tmpList = []
    combine = combination.crossoverFunctions(0)
    for n in range(50):
        g0 = first_generation.First_Generation(0, n)
        tmpList.append(g0.build_hand())
    main.MainScript() 
    genList.extend(tmpList)
    
    cycle_fitness.extend(gui_test(tmpList, 0, coords0, coords1))
    ls.extend(tmpList)
    
    
    
    first = max(cycle_fitness, key=lambda item:item[0])[1].split(".")[0]
    mx = 10
    mut_ran = []
    for i in range(mx):
        mut_ran.extend(mut_on_first(ls, ls[random.randint(0,len(ls)-1)].name, 0))
    mutatedList = mut_on_first(ls, first, 0)   #performs mutations on first fittest file overall
    genList.extend(mut_ran)
    genList.extend(mutatedList)
    
    
    cycle_fitness.extend(gui_test(mut_ran, 0, coords0, coords1))
    cycle_fitness.extend(gui_test(mutatedList, 0, coords0, coords1))
    print(cycle_fitness)
    ls.extend(mutatedList)
    ls.extend(mut_ran)
    
    sortedScoring.extend(cycle_fitness)
    
    first = max(sortedScoring, key=lambda item:item[0])[1]

    
    ls, sortedScoring, genList = death(ls, sortedScoring, genList, first)
    print(sortedScoring)
    add_to_database(genList, connection1, connection2, first)
    fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
    generational_fitness.append(max(fitnesses))
    cycle_fitness.clear()
    fitnesses.clear()
    genList.clear()
    mutatedList.clear() 
    tmpList.clear()  
    for num in range(1, gen):
        genList = []
        cycle_fitness = []
        fitnesses = []
        
        first = max(sortedScoring, key=lambda item:item[0])[1]
        
        combine = combination.crossoverFunctions(num)    #set up crossover class
        
        main.MainScript()                                                              #run mainscript to generate URDF files
        genList.extend(tmpList)
        ls, cycle_fitness = helper_function(ls, tmpList, cycle_fitness, num, coords0, coords1)   #testing getting scores of brand new hands generated   
        
        mut_ran = []
        for i in range(mx):
            mut_ran.extend(mut_on_first(ls, ls[random.randint(0,len(ls)-1)], 0))
        mutatedList = mut_on_first(ls, first, 0)   #performs mutations on first fittest file overall
        genList.extend(mutatedList)
        genList.extend(mut_ran)
        
        ls, cycle_fitness = helper_function(ls, mutatedList, cycle_fitness, num, coords0, coords1)    #testing and getting scores of mutated hands
    
    
        carrierList = carrier(genList, ls, first, num)    #performs combination
        genList.extend(carrierList)
        ls, cycle_fitness = helper_function(ls, carrierList, cycle_fitness, num, coords0, coords1)   #testing and getting scores of those combinations
        
        
        sortedScoring.extend(cycle_fitness)
        
        ls, sortedScoring, genList = death(ls, sortedScoring, genList, first)
        
        
        
        first = max(sortedScoring, key=lambda item:item[0])[1]
        add_to_database(genList, connection1, connection2, first)
    
        fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
        generational_fitness.append(max(fitnesses))   #get max fitness of that generation
        
        genList.clear()
        fitnesses.clear()
        cycle_fitness.clear()
        
    print("Cleaning up and generating graphs...")
    sortedScoring = sort_scores(sortedScoring)
    
    #ten = int(len(sortedScoring)*0.3)
    first = max(sortedScoring, key=lambda item:item[0])[1]
    #bottom = get_bottom_10(ten)
    new_fitness = []
    top = get_top_10(sortedScoring)
    coords0, coords1 = coordinate_array(0.03)
    
    new_fitness.append(gui_test(top, 0, coords0, coords1))
    first = max(new_fitness, key=lambda item:item[0])[1]
    #get_from_database(bottom, connection1, first)
    #get_from_database(top, connection1, first)
    #generate_ten_perc_graphs(bottom)
    #generate_ten_perc_graphs(top)
    #overall_graph(top)
    #connection1.close()
    #connection2.close()
    write_to_file(ls, first, sortedScoring, top) #bottom)
    plot_fitness(generational_fitness, gen)
    open_file(first)
