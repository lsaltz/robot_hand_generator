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

class Manage_Files:
   def __init__(self, ls):
        self.ls = ls
        
        
        
    def return_duplicates(self):    
        lis = copy.deepcopy(self.ls)
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
    def death(self, fitness, genList, first):
        copied_fitness = copy.deepcopy(fitness)
        dups = self.return_duplicates()
    
        if len(dups) > 0:
            for d in dups:
                name = d
                if f'{name}.json' != first:
                    for t in copied_fitness or t == []:
                        if f'{name}.json' == t[1]:
                            copied_fitness.remove(t)
                    for l in self.ls:
                        if d == l['name'] or l == []:
                            self.ls.remove(l)
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
        return self.ls, copied_fitness, genList
                    
