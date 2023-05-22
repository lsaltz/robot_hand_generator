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
import first_generation
import operator
import copy
import pandas as pd
import shutil
import sqlite3

"""
Returns copy files from overall list
"""
def return_duplicates(ls):
    new_ls = [l.to_dict() for l in ls]
    df = pd.DataFrame(new_ls)
    dup = df[df[['palm', 'fingers', 'proximal', 'distal']].duplicated(keep='last') == True]
    dupDics = dup.to_dict('records')
    return dupDics

"""
Kills the copies
"""   
def death(ls, fitness, genList, first):    ####drops all the duplicates from EVERYTHING
    returned_ls = []
    returned_fitness = []
    copied_fitness = copy.deepcopy(fitness)
    dups = return_duplicates(ls)
    returned_genList = []
    if dups is not None:
        for d in dups:
            name = d['name']
            if f'{name}.json' != first:
                for t in copied_fitness:
                    if f'{name}.json' == t[1]:
                        copied_fitness.remove(t)
                for l in ls:
                    if d['name'] == l['name']:
                        ls.remove(l)
                for g in genList:
                    if d['name'] == g['name']:
                        genList.remove(g)
                path1 = f"../output/{name}"
                print(path1)
                path2 = f"../points/{name}.json"
                print(path2)
                path3 = f"../hand_json_files/hand_archive_json/{name}.json"
                print(path3)
                if os.path.exists(path1):
                    shutil.rmtree(path1)
                    print(path1 + " removed")
                if os.path.exists(path2):
                    os.remove(path2)
                    print(path2 + " removed")
                if os.path.exists(path3):
                    os.remove(path3)
                    print(path3 + " removed")
    return ls, copied_fitness, genList
  
"""
Converts json to binary BLOB for storage
"""
def json_to_binary(jfile, index):
    with open(jfile, mode="r") as f:
        hand_data = json.load(f)
        data_binary = json.dumps(hand_data).encode('utf-8')
    f.close()     
    return data_binary

"""
Adds files to SQLite Database
"""
def add_to_database(genList, connection1, connection2, first):
    cursor1 = connection1.cursor()
    cursor2 = connection2.cursor()
    for i in range(len(genList)):
        if genList[i].name + '.json' != str(first):#
            f_name = genList[i].name + ".json"
            jfile1 = f"../points/{genList[i].name}.json"
            bin1 = json_to_binary(jfile1, i)
            cursor1.execute("insert into hand_data (ID, name, data) values(?,?,?)",(i, f_name, bin1))
            connection1.commit()
            jfile2 = f"../hand_json_files/hand_archive_json/{genList[i].name}.json"
            bin2 = json_to_binary(jfile2, i)
            cursor2.execute("insert into hand_files (ID, name, data) values(?,?,?)",(i, f_name, bin2))
            connection2.commit()   
            os.remove(jfile1)
            os.remove(jfile2)
         
"""
Gets top/bottom 10 from database and converts them from binary back to json
"""
def get_from_database(ten_list, connection, first):
    cr = connection.cursor()
    for t in ten_list:
        f_name = t[1]
        if f_name != str(first):
            cr.execute("select data from hand_data where name=?", (f_name,))
            connection.commit()
            for row in cr:
                
                with open(f"../points/{f_name}", mode="w") as f:
                    s_data = b''.join(row)
                    json_file = json.loads(json.dumps(s_data.decode('utf-8'), indent=4))#.decode('utf-8')
                    f.write(json_file)
                f.close()

"""
Calls combine to combine two files
"""
def crossover(p0, p1, num, s, l):
    tmpList = []
    d0 = Dict()
    d1 = Dict()
    f1 = os.path.expanduser(('../hand_json_files/hand_archive_json/') + p1['name'] + '.json')
    par1 = combine.json_to_dictionaries(f1)
    f0 = os.path.expanduser(('../hand_json_files/hand_archive_json/') + p0['name'] + '.json')
    par0 = combine.json_to_dictionaries(f0)                    
    d0, d1 = combine.combo(par0, par1, p0, p1, num, s, l)
    tmpList.append(copy.deepcopy(d0))
    tmpList.append(copy.deepcopy(d1))
    return tmpList

"""
Acts like a pollen carrier to "spread" the fittest hand's genes to the other hands in the generation. Also loops
through even and odd dictionaries to combine them
"""
def carrier(genList, ls, first, generation):    ###
     oddDics = []
     evenDics = []
     newList = []
     fittest_dic = next((d for d in ls if (d['name']+'.json') == first), None)
     name = fittest_dic['name']
     fittest_file =f'../output/{name}/{name}.json'
     
     for l in range(len(genList)):
         recipient_dic = genList[l]
         newList.extend(crossover(fittest_dic, recipient_dic, generation, "l", l))
     #carriedList = death(newList)
     
     main.MainScript()
     for c in range(len(newList)):     
         if c%2 == 0:
             oddDics.append(copy.deepcopy(newList[c]))
         else:
             evenDics.append(copy.deepcopy(newList[c]))
             
     for m in range(min(len(evenDics), len(oddDics))):
         newList.extend(crossover(evenDics[m], oddDics[m], generation, "m", m))
     #returned_List = death(carriedList)
     
     main.MainScript()
     return newList

"""
Tests hands, loops through current generation
"""
def test(dicList, num, coords0, coords1):####
    tmpFitness = []
    for l in dicList:
        name = l['name']
        rt = f"../output/{name}/hand"
        sim_test = testing.sim_tester(name, rt, l, coords0, coords1)
        tmpFitness.append(sim_test.main(num))
        
    return tmpFitness

"""
Sorts scores
"""    
def sort_scores(scoring):###
    sortedScoring = sorted(scoring, key = lambda x: float(x[0])) #Sorts array by fittness scores
    
    return sortedScoring

"""
Runs mutations. Gets fittest file and mutates on that
"""
def mut_on_first(tomutate, first, num):
    firstList = []
    mutateTimes = 2
    max_segs = 3
   
    for l in tomutate:
        if (str(l['name']) + ".json") == str(first):
            m0 = l
    
    m_d = combine.json_to_dictionaries(f"../hand_json_files/hand_archive_json/{first}")
    firstList = mutations.mutate(mutateTimes, max_segs, m_d, m0, num)
    
    main.MainScript()
    return firstList
    
"""
Gets number 10% of overall number of hands
"""    
def get_10_percent(sortedScoring):
    length = len(sortedScoring)
    ten_perc = int(0.1 * length)    
    if ten_perc == 0:
        ten_perc = 1
    return ten_perc

"""
Gets list of bottom ten
"""  
def get_bottom_10(ten_num):
    bottom_10 = []
    bottom_10.extend(sortedScoring[0:ten_num])
    return bottom_10

"""
Gets list of top ten
"""    
def get_top_10(ten_num):
    top_ten = []
    top_ten.extend(sortedScoring[0-ten_num:])
    return top_ten

"""
Generates top and bottom 10% data
"""    
def generate_ten_perc_graphs(ten_perc_list):
    for i in range(len(ten_perc_list)):
        name = ten_perc_list[i][1]
        coordsR = []
        nr_R = []
        coordsL = []
        nr_L = []
        with open(f"../points/{name}", mode="r") as f:
            fi = json.load(f)
            dictionary = Dict(fi)
            coordsR.extend(dictionary.finger_0.reached)
            coordsL.extend(dictionary.finger_1.reached)
            nr_R.extend(dictionary.finger_0.not_reached)
            nr_L.extend(dictionary.finger_1.not_reached)
            g_name = dictionary.name + ".png"
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
             
"""
Opens the fittest file in PyBullet, called after everything has been completed.
"""    
def open_file(fittestFirst):
    name = fittestFirst.split('.')[0]
    rt = f"../output/{name}/hand"
    fittest_file = f"{rt}/{name}.urdf"
    basic_load.load(fittest_file)

"""
writes data to results file
"""    
def write_to_file(ls, fittestFirst, sortedScoring, top_10, bottom_10):
    winning_ratios = Dict()
    winning_file_names = []
    winning_10_ratios = []
    name = fittestFirst.split('.')[0]
    rt = f"../output/{name}/hand"
    for i in range(len(ls)):
        if ls[i].name == str(fittestFirst.split('.')[0]):
            winning_ratios = ls[i]
    for i in range(len(top_10)):
        winning_file_names.append(top_10[i][1].split('.')[0])
    for x in range(len(ls)):
        if ls[x].name in winning_file_names:
              winning_10_ratios.append(ls[x])    
    with open("../output/results.txt", mode="w") as resultsFile:
        resultsFile.write("The fittest of them all is: " + str(fittestFirst) + "\n")
        resultsFile.write("It's winning ratios are: "+ "\n")
        resultsFile.write(f"Palm: {winning_ratios.palm} To Fingers: {winning_ratios.fingers} and Proximal: {winning_ratios.proximal} To Distal: {winning_ratios.distal}\n")
        resultsFile.write("Location is: " + str(rt) + "\n")
        resultsFile.write("Overall top 10% results are: \n" + str(top_10) + "\n")
        for j in range(len(winning_10_ratios)):
            resultsFile.write(f"{winning_10_ratios[j]}\n")
        resultsFile.write("Overall bottom 10% results are: \n" + str(bottom_10) + "\n")
    resultsFile.close()

"""
Plots fitness trend over generations
"""        
def plot_fitness(generational_fitness, generations):
    epochs = []
    plt.figure()
    plt.xlim(0, generations)
    plt.ylim(0, 1)
    for i in range(generations):
        epochs.append(i)
    
    generational_fitness = list(generational_fitness)
    plt.plot(epochs, generational_fitness, color='blue', linestyle='solid')
    plt.savefig("../output/fitness_trend")

"""
Tests hands
"""    
def helper_function(ls, tmpList, cycle_fitness, num, coords0, coords1):
    
    
    cycle_fitness.extend(test(tmpList, num, coords0, coords1))
    ls.extend(tmpList)
    
    tmpList.clear()
    return ls, cycle_fitness

"""
Generates a coordinate array to test hands on
"""
def coordinate_array():
    finger_z = 0.36 + 0.25
    val = 0.03
    palm_z = 0.053
    total_height = 0.36
    xoffset = 0.2
    coords1 = []
    coords2 = []
    bottom_x = -abs(total_height + 0.25)
    bottom_y = -abs(palm_z/2)
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = int(row_length/val)
    column_points = int(column_length/val)
        
    
    coords1 = [[x1, y1, 0] for x1 in np.linspace(bottom_x, finger_z, num=row_points) for y1 in np.linspace(bottom_y, finger_z, num=column_points)]
    coords2 = [[x2, y2, 0] for x2 in np.linspace(bottom_x - xoffset, finger_z, num=row_points) for y2 in np.linspace(bottom_y, finger_z, num=column_points)]

    return coords1, coords2
    
    
     
print("Please input the integer number of generations you would like to run this for: ")
gen = int(input())+1  #generations ea runs for
mutateTimes = 2 #Amount of mutated files per generation
file_name = []  #file name of hands
max_segs = 3  #Max amount of segments per hand
ls = []
totalFitness = []
bottom_10 = []
top_10 = []
cycle_fitness = []
generational_fitness = []
genList = []
sortedScoring = []
list_after_upload = []
fitnesses = []
connection1 = sqlite3.connect('hand_points.db')
connection2 = sqlite3.connect('hand_json.db')
cr1 = connection1.cursor()
cr2 = connection2.cursor()
cr1.execute("drop table if exists hand_data")
cr2.execute("drop table if exists hand_files")
cr1.execute("create table hand_data (ID, name, data)")
cr2.execute("create table hand_files (ID, name, data)")
print("generating coordinate array...")
coords0, coords1 = coordinate_array()
"""
1. generate a random hand
2. mutate on that hand
3. tests files
4. add existing files that aren't the fittest to the database (SQLite)

5. Loops for gen times:
    a. combines files taking fittest from previous generation
    b. generates completely random file
    c. test
    d. mutates
    e. tests
    f. removes copies
    g. gets generational and overall fittest file
    e. adds remaing files that aren't the fittest to database

6. gets top and bottom 10% from database
7. plots and writes resulting data
"""
tmpFit = []
combine = combination.crossoverFunctions(0)
rd, tmpList = first_generation.generate(max_segs, 0)
main.MainScript() 
genList.extend(tmpList)
ls, cycle_fitness = helper_function(ls, tmpList, cycle_fitness, 0, coords0, coords1)
sortedScoring.extend(cycle_fitness)
first = max(sortedScoring, key=lambda item:item[0])[1]
mutatedList = mut_on_first(genList, first, 0)    #performs mutations on first fittest file overall
genList.extend(mutatedList)
ls, cycle_fitness = helper_function(ls, mutatedList, cycle_fitness, 0, coords0, coords1)
sortedScoring.extend(cycle_fitness[1:])
first = max(sortedScoring, key=lambda item:item[0])[1]

mutatedList.clear()
add_to_database(genList, connection1, connection2, first)
fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
generational_fitness.append(max(fitnesses))
cycle_fitness.clear()
fitnesses.clear()
genList.clear()

for num in range(1, gen):
    first = max(sortedScoring, key=lambda item:item[0])[1]

    combine = combination.crossoverFunctions(num)    #set up crossover class
    rd, tmpList = first_generation.generate(max_segs, num)    #generate brand new hand 
    main.MainScript()                                                              #run mainscript to generate URDF files
    genList.extend(tmpList)
    ls, cycle_fitness = helper_function(ls, tmpList, cycle_fitness, num, coords0, coords1)   #testing getting scores of brand new hands generated   
    
    mutatedList = mut_on_first(ls, first, num)    #performs mutations on first fittest file overall
    genList.extend(mutatedList)
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
    cycle_fitness.clear()    #clear list of all generation fitnesses
    fitnesses.clear()
    genList.clear()

sortedScoring = sort_scores(sortedScoring)
   
ten = int(len(sortedScoring)*0.1)
first = max(sortedScoring, key=lambda item:item[0])[1]
bottom = get_bottom_10(ten)
top = get_top_10(ten)
get_from_database(bottom, connection1, first)
get_from_database(top, connection1, first)
generate_ten_perc_graphs(bottom)
generate_ten_perc_graphs(top)
connection1.close()
connection2.close()
write_to_file(ls, first, sortedScoring, top, bottom)
plot_fitness(generational_fitness, gen)
open_file(first)
 
          

    
    

