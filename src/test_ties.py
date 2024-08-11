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


def test(dicList, num):
    tmpFitness = []
    
    for l in dicList:
        
        gripper_name = l['name']
        
            
        w = nt.WorkSpace_Test(gripper_name, l)     
        #area_fit, angles_fit, straight_fit = w.main()

        fit = w.main()

        tmpFitness.append([fit, f"{gripper_name}.json"])
        
    return tmpFitness


def open_file(fittestFirst):
    name = fittestFirst.split('.')[0]
    rt = f"../output/{name}/hand"
    fittest_file = f"{rt}/{name}.urdf"
    basic_load.load(fittest_file) 

def generate_json(ls):
    for l in ls:
        b = bh.Build_Json(l)
        b.build_hand()
        main.MainScript()

if __name__ == "__main__":
    fitnesses = []
    ls = [Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [41, 13, 46], 'finger_0': [50, 13, 37]}, 'finger_0': 3, 'finger_1': 3}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05299, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_915_4eo_eo'}), 
          Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [49, 12, 39], 'finger_1': [41, 13, 46]}, 'finger_0': 3, 'finger_1': 3}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05299, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_2832_2w_s'}),
          Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [43, 22, 35], 'finger_0': [50, 6, 44]}, 'finger_0': 3, 'finger_1': 3}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.0511, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_2531_4w_s'}),
          Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [50, 6, 44], 'finger_1': [41, 13, 46]}, 'finger_0': 3, 'finger_1': 3}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05299, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_1720_2w_s'}),
          Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [40, 19, 41], 'finger_0': [50, 13, 37]}, 'finger_0': 3, 'finger_1': 3}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.0513, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_4001_0w_s'}),
          Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [44, 23, 33], 'finger_0': [50, 13, 37]}, 'finger_0': 3, 'finger_1': 3}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.0513, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_4415_4w_s'}),
          Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [45, 13, 42], 'finger_0': [50, 6, 44]}, 'finger_0': 3, 'finger_1': 3}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.0513, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_4550_3w_s'})]
    fitnesses.extend(test(ls, 0))
    print(fitnesses)
    for l in ls:
        p = angles_plot.Plot(l.name)
        p.main()
    generate_json(ls)
