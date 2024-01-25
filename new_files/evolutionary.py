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
import combination
import copy
import sqlite3

class sim_evolve:

    def __init__(self):
        
        
    

    """
    Calls combine to combine two files
    Parameters:
        p0: parent 0
        p1: parent 1
        num: generation number
        s: a letter indicating which mode of combining
        l: child index
    """
    def crossover(self, p0, p1, num, s, l):
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
    Acts like a pollen carrier to "spread" the fittest hand's genes to the other hands in the generation. Also loops through even and odd dictionaries to combine them
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
