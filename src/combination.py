# By Marshall Saltz

import random
import numpy as np
import os
import json
from addict import Dict
import copy

class crossoverFunctions:

    def __init__(self, generation):
        self.generation = generation
    
    def determine_seg_ratios(self, finger, num_segs):
        
        
        list_of_ratios = []
        prev_rat = 95
        nm = num_segs- 2
        ct = 0
        for i in range(0, nm):
            rat = np.random.randint(1, prev_rat+1)
            list_of_ratios.append(rat)
            ct += rat
            prev_rat = 100-ct
            
        list_of_ratios.append(100-ct)
           
        
       
        return list_of_ratios 
    
       	   
    def build_fingers(self, ls0, ls1, totalfingerlength, finger, hand_data):
        seg_ratios = []
        num_segs = len(ls0)+1

        seg_ratios = self.determine_seg_ratios(finger, num_segs)

        hand_data[finger].num_segs = num_segs
        hand_data.ratio.segs[finger] = seg_ratios
        
        hand_data.update()
        
        return hand_data  
    
    def keep_finger(self, ls, totalfingerlength, finger, hand_data):
        seg_ratios = ls
        num_segs = len(ls)+1
        
        
        
        hand_data[finger].num_segs = num_segs
        hand_data.ratio.segs[finger] = seg_ratios
        
        hand_data.update()
        
        return hand_data
        
    def choose_palm_width(self, p):
        choice = random.randint(1,3)
        if choice == 1:
            palm_width = p.length.palm
        else:
            palm_width = round(random.uniform(0.05, 0.09), 5)
        return palm_width
        
    def combo(self, p0, p1, num, n, nu, letter):
        hand_data0 = Dict()
        hand_data1 = Dict()

        
        fn0 = "child_0_" + str(num) + "_" + str(nu) + n + "_" + str(letter)
        fn1 = "child_1_" + str(num) + "_" + str(nu) + n + "_" + str(letter)

        
        p0f0 = random.randint(1,10)
        p0f1 = p0.ratio.finger_1
        
        
        p1f0 = p1.ratio.finger_0
        p1f1 = random.randint(1,10)
        
        
        fingers_length_0 = 0.288
        fingers_length_1 = 0.288
        finger_0_0 = (fingers_length_0/(p0f0+p0f1))*p0f0
        finger_0_1 = (fingers_length_0/(p0f0+p0f1))*p0f1
        finger_1_0 = (fingers_length_1/(p1f0+p1f1))*p1f0
        finger_1_1 = (fingers_length_1/(p1f0+p1f1))*p1f1

        
        
        hand_data0 = self.build_fingers(p1.ratio.segs.finger_0, p0.ratio.segs.finger_0, finger_0_0, "finger_0", hand_data0)
        hand_data0 = self.keep_finger(p0.ratio.segs.finger_1, finger_0_1, "finger_1", hand_data0)
        hand_data0.finger_1.num_segs = p0.finger_1.num_segs
        
        hand_data0.ratio.segs.finger_1 = p0.ratio.segs.finger_1
        hand_data1 = self.build_fingers(p0.ratio.segs.finger_1, p1.ratio.segs.finger_1, finger_1_1, "finger_1", hand_data1)
        hand_data1 = self.keep_finger(p1.ratio.segs.finger_0, finger_1_0, "finger_0", hand_data1)
        hand_data1.finger_0.num_segs = p1.finger_0.num_segs 
        hand_data1.ratio.segs.finger_0 = p1.ratio.segs.finger_0
        
        
        
        hand_data0.ratio.finger_0 = p0f0
        hand_data0.ratio.finger_1 = p0f1
        hand_data0.length.palm = self.choose_palm_width(p1)
        hand_data0.length.finger_0 = finger_0_0
        hand_data0.length.finger_1 = finger_0_1
        hand_data1.ratio.finger_0 = p1f0
        hand_data1.ratio.finger_1 = p1f1
        hand_data1.length.palm = self.choose_palm_width(p0)
        hand_data1.length.finger_0 = finger_1_0
        hand_data1.length.finger_1 = finger_1_1
        
        
        
        hand_data0.name = fn0
        
        hand_data1.name = fn1
        hand_data0.update()
        hand_data1.update()

        
        return hand_data0, hand_data1
    
    
