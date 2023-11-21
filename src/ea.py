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

"""
Returns copy files from overall list
Parameters:
    ls: total list of grippers
"""
#def return_duplicates(ls):    
"""
    new_ls = [l.to_dict() for l in ls]
    df = pd.DataFrame(new_ls)
    dup = df[df[['ratio']].duplicated(keep='last') == True]
    dupDics = dup.to_dict('records')
"""
def return_duplicates(ls):    
    lis = copy.deepcopy(ls)
    names = [l.pop('name') for l in lis]
    dup_names = []
    for l in range(len(ls)):
        for j in range(l+1, len(ls)):
            if ls[l].items() == ls[j].items():
                dup_names.append(names[j])
    
    
    return dup_names
    
"""
Kills the copies and weaker grippers
Parameters:
    ls: total list of grippers
    fitness: list of fitnesses
    genList: generational list of grippers
    first: hand with highest fitness
"""   
def death(ls, fitness, genList, first):
    weak_name = []
    copied_fitness = copy.deepcopy(fitness)
    dups = return_duplicates(ls)
    
    if len(dups) > 0:
        for d in dups:
            name = d
            if name != first:
                for t in copied_fitness or t == []:
                    if f'{name}.json' == t[1]:
                        copied_fitness.remove(t)
                for l in ls:
                    if d == l['name'] or l == []:
                        ls.remove(l)
                for g in genList or g == []:
                    if d == g['name']:
                        genList.remove(g)
                path1 = f"../output/{name}"
                path2 = f"../points/{name}.json"
                path3 = f"../hand_json_files/hand_archive_json/{name}.json"
                if os.path.exists(path1):
                    shutil.rmtree(path1)
                if os.path.exists(path2):
                    os.remove(path2)
                if os.path.exists(path3):
                    os.remove(path3)
    
    """
    for i in copied_fitness:
        if i[0] == 0:
            weak_name.append(i[1].split('.')[0])
            copied_fitness.remove(i)
    if weak_name is not None:
        for n in weak_name:
            for g in genList:
                if n == g['name']:
                    genList.remove(g)
            for l in ls:
                if n == l['name']:
                    ls.remove(l)
            path1 = f"../output/{n}"
               
            path2 = f"../points/{n}.json"
        
            path3 = f"../hand_json_files/hand_archive_json/{n}.json"
            if os.path.exists(path1):
                shutil.rmtree(path1)
            if os.path.exists(path2):
                os.remove(path2)
            if os.path.exists(path3):
                os.remove(path3) 
    """        
    return ls, copied_fitness, genList
  
"""
Converts json to binary BLOB for storage
Parameters: 
    jfile: file to be converted 
"""
def json_to_binary(jfile):
    with open(jfile, mode="r") as f:
        hand_data = json.load(f)
        data_binary = json.dumps(hand_data).encode('utf-8')
    f.close()     
    return data_binary

"""
Adds files to SQLite Database
Parameters:
    genList: generational list of grippers
    connection1: connection to points list database
    connection2: connection to gripper json database
    first: gripper with highest fitness score
"""
def add_to_database(genList, connection1, connection2, first):
    cursor1 = connection1.cursor()
    cursor2 = connection2.cursor()
    
    for i in range(len(genList)):
        if genList[i].name + '.json' != str(first):
            f_name = genList[i].name + ".json"
            
            jfile1 = f"../points/{genList[i].name}.json"
            bin1 = json_to_binary(jfile1)
            cursor1.execute("insert into hand_data (ID, name, data) values(?,?,?)",(i, f_name, bin1))
            connection1.commit()
            jfile2 = f"../hand_json_files/hand_archive_json/{genList[i].name}.json"
            bin2 = json_to_binary(jfile2)
            cursor2.execute("insert into hand_files (ID, name, data) values(?,?,?)",(i, f_name, bin2))
            connection2.commit()   
            os.remove(jfile1)
            os.remove(jfile2)
         
"""
Gets top/bottom 10 from database and converts them from binary back to json
Parameters:
    ten_list: bottom or top ten percent of grippers
    connection: database to be opened
    first: gripper in first place 
"""
def get_from_database(ten_list, connection, first):
    cr = connection.cursor()
    for t in ten_list:
        f_name = t
        if f"{f_name}.json" != str(first):
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
    f1 = os.path.expanduser(('../hand_json_files/hand_archive_json/') + p1['name'] + '.json')
    par1 = c.json_to_dictionaries(f1)
    f0 = os.path.expanduser(('../hand_json_files/hand_archive_json/') + p0['name'] + '.json')
    par0 = c.json_to_dictionaries(f0)                    
    d0, d1 = c.combo(par0, par1, p0, p1, num, s, l)
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
     fittest_file =f'../output/{name}/{name}.json'
     print(len(genList))
     for l in range(len(genList)):
         recipient_dic = genList[l]
         newList.extend(crossover(fittest_dic, recipient_dic, generation, "w", l))
         print(l)
     print(newList)
     
     main.MainScript()
     for c in range(len(newList)):     
         if c%2 == 0:
             oddDics.append(copy.deepcopy(newList[c]))
         else:
             evenDics.append(copy.deepcopy(newList[c]))
             
     for m in range(min(len(evenDics), len(oddDics))):
         newList.extend(crossover(evenDics[m], oddDics[m], generation, "eo", m))
         
     #returned_List = death(carriedList)
     
     main.MainScript()
     return newList
     
def get_every_eight(dicList):
    count = 0
    newls = []
    lsls = []
    cnt = 0
    for l in dicList:
        count +=1
        cnt +=1
        newls.append(l)
        if count == 8 or cnt ==len(dicList):
            count = 0
            lsls.append(newls)
            newls = []
    return lsls

def test(dicList, num, coords0, coords1):
    tmpFitness = []
    testls = get_every_eight(dicList)
    for l in testls: 
        sim_test = testing.sim_tester(None, None, l, coords0, coords1)
        tmpFitness.extend(sim_test.main())
        
    return tmpFitness
    

def gui_test(dicList, num, coords0, coords1):####
    tmpFitness = []
    
    for l in dicList:
        name = l['name']
        rt = f"../output/{name}/hand"
        sim_test = testing.sim_tester(name, rt, l, coords0, coords1)
        tmpFitness.append(sim_test.gui_test())
        
    return tmpFitness

def final_test(dicList, num, coords0, coords1):####
    tmpFitness = []
    
    for l in dicList:
        name = l
        rt = f"../output/{name}/hand"
        sim_test = testing.sim_tester(name, rt, l, coords0, coords1)
        tmpFitness.append(sim_test.gui_test())
        
    return tmpFitness    

"""
Sorts scores
Parameters:
    scoring: unsorted fitness list
"""    
def sort_scores(scoring):###
    sortedScoring = sorted(scoring, key = lambda x: float(x[0])) #Sorts array by fittness scores
    
    return sortedScoring

"""
Runs mutations. Gets fittest file and mutates on that
Parameters:
    tomutate:P list of files to mutate
    first: gripper with highest fitness score
    num: generation number
"""
def mut_on_first(tomutate, file_to_mutate, num, i):
    firstList = []
    
    
    c = combination.crossoverFunctions(num)
    for l in tomutate:
        if str(l['name']) == str(file_to_mutate):
            m0 = l
    
    m_d = c.json_to_dictionaries(f"../hand_json_files/hand_archive_json/{file_to_mutate}.json")
    m = mutations.Mutate(m_d, m0, num, i)
    firstList.append(m.build_hand())
    main.MainScript()
    return firstList
 
 
"""
Gets numerical amount of 10% of overall number of hands
Parameters:
   sortedScoring: sorted fitness list
"""    
def get_10_percent(sortedScoring):
    #length = len(sortedScoring)
    #ten_perc = int(0.3 * length)    
    #if ten_perc == 0:
        #ten_perc = 1
    ten_perc = 5
    return ten_perc

"""
Gets list of bottom ten
Parameters:
    ten_num: numerical amount of 10% of grippers generated
"""  
def get_bottom_10(ten_num):
    bottom_10 = []
    bottom_10.extend(sortedScoring[0:ten_num])
    return bottom_10

"""
Gets list of top ten
Parameters:
    ten_num: numerical amount of 10% of grippers generated
"""    
def get_top_10(sortedScoring):
    top_ten = []
    top_ten.extend(sortedScoring[-50:])
    print(top_ten)
    top_ten = list(map(lambda x:x[1].split('.')[0], top_ten))
    print(top_ten)
    return top_ten

"""
Generates top and bottom 10% data
Parameters:
    ten_perc_list: list of bottom or top 10% grippers
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
            axis[0].set_aspect('equal')
            axis[1].set_aspect('equal')
            axis[2].set_aspect('equal')
            axis[0].set_xlabel("X Coords")
            axis[1].set_xlabel("X Coords")
            axis[2].set_xlabel("X Coords")
            axis[0].set_ylabel("Y Coords")
            axis[1].set_ylabel("Y Coords")
            axis[2].set_ylabel("Y Coords")
            for k in range(len(nr_R)):
                axis[0].scatter(nr_R[k][0], nr_R[k][1], s=2, color='red')
                axis[2].scatter(nr_R[k][0], nr_R[k][1], s=2, color='red')
            for z in range(len(nr_L)):
                axis[1].scatter(nr_L[z][0], nr_L[z][1], s=2, color='red')
                axis[2].scatter(nr_L[z][0], nr_L[z][1], s=2, color='red')
            for j in range(len(coordsR)):
                axis[0].scatter(coordsR[j][0], coordsR[j][1], s=2, color='blue')
                axis[2].scatter(coordsR[j][0], coordsR[j][1], s=2, color='blue')
            for x in range(len(coordsL)):   
                axis[1].scatter(coordsL[x][0], coordsL[x][1], s=2, color='blue')
                axis[2].scatter(coordsL[x][0], coordsL[x][1], s=2, color='blue')
            plt.savefig(f"../output/{g_name}")
            plt.close('all')  

"""
Generates a graph of overall top 10% data. Output is a graph of hard to reach (yellow), easy to reach(blue), and impossible(red) points
Parameters:
    ten_perc_list: top 10% of grippers
"""
def overall_graph(ten_perc_list):
    figure, axis = plt.subplots(3, 1)
    axis[0].set_title("Finger 0")
    axis[1].set_title("Finger 1")
    axis[2].set_title("Total")
    axis[0].set_xlabel("X Coords")
    axis[1].set_xlabel("X Coords")
    axis[2].set_xlabel("X Coords")
    axis[0].set_ylabel("Y Coords")
    axis[1].set_ylabel("Y Coords")
    axis[2].set_ylabel("Y Coords")
    axis[0].set_aspect('equal')
    axis[1].set_aspect('equal')
    axis[2].set_aspect('equal')
    name_graph = "overall_graph.png"
    coordsR = []
    nr_R = []
    coordsL = []
    nr_L = []
    
    for i in range(len(ten_perc_list)):
        name = ten_perc_list[i][1]
        with open(f"../points/{name}", mode="r") as f:
            fi = json.load(f)
            dictionary = Dict(fi)
            coordsR.extend(list(dictionary.finger_0.reached))
            coordsL.extend(list(dictionary.finger_1.reached))
            nr_R.extend(list(dictionary.finger_0.not_reached))
            nr_L.extend(list(dictionary.finger_1.not_reached))
        
       
    
    for k in nr_R:
        if k not in coordsR:
            axis[0].scatter(k[0], k[1], s=2, color='red', alpha=0.3)
            axis[2].scatter(k[0], k[1], s=2, color='red', alpha=0.3)
        else:
            axis[0].scatter(k[0], k[1], s=2, color='yellow', alpha=0.3)
            axis[2].scatter(k[0], k[1], s=2, color='yellow', alpha=0.3)                
    for z in nr_L:
        if z not in coordsL:
            axis[1].scatter(z[0], z[1], s=2, color='red', alpha=0.3)
            axis[2].scatter(z[0], z[1], s=2, color='red', alpha=0.3)
        else:
            axis[1].scatter(z[0], z[1], s=2, color='yellow', alpha=0.3)
            axis[2].scatter(z[0], z[1], s=2, color='yellow', alpha=0.3)       
    for j in coordsR:
        if j not in nr_R:
            axis[0].scatter(j[0], j[1], s=2, color='blue', alpha=0.3)
            axis[2].scatter(j[0], j[1], s=2, color='blue', alpha=0.3)
        else:
            axis[0].scatter(j[0], j[1], s=2, color='yellow', alpha=0.3)
            axis[2].scatter(j[0], j[1], s=2, color='yellow', alpha=0.3)   
    for x in coordsL:
        if x not in nr_L:
            axis[1].scatter(x[0], x[1], s=2, color='blue', alpha=0.3)
            axis[2].scatter(x[0], x[1], s=2, color='blue', alpha=0.3)
        else:
            axis[1].scatter(x[0], x[1], s=2, color='yellow', alpha=0.3)
            axis[2].scatter(x[0], x[1], s=2, color='yellow', alpha=0.3)
    plt.savefig(f"../output/{name_graph}")
    plt.close('all')      
            
"""
Opens the fittest file in PyBullet, called after everything has been completed.
Parameters:
    fittestFirst: fittest file
"""    
def open_file(fittestFirst):
    name = fittestFirst.split('.')[0]
    rt = f"../output/{name}/hand"
    fittest_file = f"{rt}/{name}.urdf"
    basic_load.load(fittest_file)

"""
Writes data to results file
Parameters:
    ls: total list of grippers
    fittestFirst: fittest gripper
    sortedScoring: sorted list of fitnesses
    top_10: top 10% of grippers
    bottom_10: bottom 10% of grippers
"""  
  
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
        resultsFile.write("Overall top 50 results are: \n" + str(sortedScoring[-50:]) + "\n")
        for j in range(len(winning_10_ratios)):
            resultsFile.write(f"{winning_10_ratios[j]}\n")
        #resultsFile.write("Overall bottom 10% results are: \n" + str(bottom_10) + "\n")
    resultsFile.close()


"""
Plots fitness trend over generations
Parameters:
    generational_fitness: max fitness of generation
    generations: total generation number
"""        
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
"""
Tests hands and alters lists
Parameters:
    ls: total list of grippers
    tmpList: temporary list of grippers from generation
    num: generation number
    coords0: finger coordinates
    coords1: finger coordinates
"""    
def helper_function(ls, tmpList, cycle_fitness, num, coords0, coords1):
    
    
    #cycle_fitness.extend(test(tmpList, num, coords0, coords1))
    cycle_fitness.extend(gui_test(tmpList, num, coords0, coords1))
    ls.extend(tmpList)
    
    tmpList.clear()
    return ls, cycle_fitness

"""
Generates a coordinate array to test hands on
"""
def coordinate_array(val):
    finger_z = 0.2
    
    
    total_height = 0.2
    coords1 = []
    coords2 = []
    bottom_x = -abs(total_height)
    bottom_y = 0
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = int(row_length/val)
    column_points = int(column_length/val)
    n = 8
    rad = 0.019
    center_pt = [[x, y, 0] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
    #center_pt = [0.3, 0.3, 0]
    x1 = [(c[0] + (np.cos(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, n+1)]
    #x1 = [center_pt[0] + (np.cos(2*np.pi/n*x)*rad) for x in range(0, n+1)]
    #y1 = [center_pt[1] + (np.sin(2*np.pi/n*x)*rad)) for x in range(0, n+1)]
    y1 = [(c[1] + (np.sin(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, n+1)]
    z1 = np.linspace(0, 0, len(x1))
    coords1 = list(zip(x1, y1, z1))
    x2 = [(c[0] + (np.cos(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
    y2 = [(c[1] - (np.sin(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
    #x2 = [center_pt[0] + ((np.cos(2*np.pi/n*x)*rad)+np.pi) for x in range(0, n+1)]
    #y2 = [center_pt[1] + ((np.sin(2*np.pi/n*x)*rad)+np.pi) for x in range(0, n+1)]
    z2 = np.linspace(0, 0, len(x2))
    coords2 = list(zip(x2, y2, z2))
    return(coords1, coords2)

    







    
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
        mut_ran.extend(mut_on_first(ls, ls[random.randint(0,len(ls)-1)].name, 0, i))
    mutatedList = mut_on_first(ls, first, 0, "f")   #performs mutations on first fittest file overall
    genList.extend(mut_ran)
    genList.extend(mutatedList)
    
    
    cycle_fitness.extend(gui_test(mut_ran, 0, coords0, coords1))
    cycle_fitness.extend(gui_test(mutatedList, 0, coords0, coords1))
    
    ls.extend(mutatedList)
    ls.extend(mut_ran)
    
    sortedScoring.extend(cycle_fitness)
    
    first = max(sortedScoring, key=lambda item:item[0])[1]

    
    ls, sortedScoring, genList = death(ls, sortedScoring, genList, first)
    
    
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
        
        ls, cycle_fitness = helper_function(ls, mutatedList, cycle_fitness, num, coords0, coords1)    #testing and getting scores of mutated hands
    
    
        carrierList = carrier(genList, ls, first, num)    #performs combination
        genList.extend(carrierList)
        ls, cycle_fitness = helper_function(ls, carrierList, cycle_fitness, num, coords0, coords1)   #testing and getting scores of those combinations
        
        
        sortedScoring.extend(cycle_fitness)
        
        ls, sortedScoring, genList = death(ls, sortedScoring, genList, first)
        
        
        
        first = max(sortedScoring, key=lambda item:item[0])[1].split('.')[0]
        
    
        fitnesses = copy.deepcopy([t[0] for t in cycle_fitness])
        generational_fitness.append(max(fitnesses))   #get max fitness of that generation
        tmpList = copy.deepcopy(genList)
        genList.clear()
        fitnesses.clear()
        cycle_fitness.clear()
        
    
    sortedScoring = sort_scores(sortedScoring)
    
    #ten = int(len(sortedScoring)*0.3)
    first = max(sortedScoring, key=lambda item:item[0])[1]
    add_to_database(genList, connection1, connection2, first)
    #bottom = get_bottom_10(ten)
    new_fitness = []
    top = get_top_10(sortedScoring)
    
    coords0, coords1 = coordinate_array(0.03)
    
    new_fitness.extend(final_test(top, 0, coords0, coords1))
    first = max(new_fitness, key=lambda item:item[0])[1]
    new_fitness = sort_scores(new_fitness)
    #get_from_database(bottom, connection1, first)
    get_from_database(top, connection1, first)
    #generate_ten_perc_graphs(bottom)
    #generate_ten_perc_graphs(top)
    #overall_graph(top)
    connection1.close()
    connection2.close()
    print("Cleaning up and generating graphs...")
    write_to_file(ls, first, new_fitness, top) #bottom)
    plot_fitness(generational_fitness, gen)
    open_file(first).json
