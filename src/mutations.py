# By Marshall Saltz

import random
import numpy as np
import os
import json
from addict import Dict
import copy

class Mutate:

    def __init__(self, data, generation, number):
        
        self.hand_data = Dict()
        self.upper = 10
        self.lower = 1
        self.total_size = 0.36
        self.data = data
        self.generation = generation
        self.number = number
        
    def mutation_ratios(self):
        ratio = np.random.randint(self.lower, self.upper)
        return ratio


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
           
        
        self.hand_data.ratio.segs[finger] = list_of_ratios
        self.hand_data.update()
        return list_of_ratios 
        
    def determine_seg_lengths(self, finger_length, finger, num_segs):
        
        list_of_ratios = self.determine_seg_ratios(finger, num_segs)
        
        sum_ = sum(list_of_ratios)
        
        for i in range(len(list_of_ratios)):
            link_length = (finger_length*list_of_ratios[i])/100
            
        
        
    def build_hand(self):
        
        file_name = "hand_mut_gen_" + str(self.generation) + "_" + str(self.number)
        
        palmz = 0.053
        palmx = 0.032
        self.hand_data.name = file_name
        self.hand_data.finger_0.num_segs = random.randint(3, 4)
        self.hand_data.finger_1.num_segs = random.randint(3, 4)
        
        #palm = self.mutation_ratios()
        #fingers = self.mutation_ratios()
        right = self.data.ratio.finger_0
        left = self.data.ratio.finger_1
        
        palm_width = round(random.uniform(0.05, 0.09), 5)
        
        fingers_total_length = 0.288
        finger_0_length = fingers_total_length/(right+left) * right
        finger_1_length = fingers_total_length - finger_0_length

        self.determine_seg_lengths(finger_0_length, "finger_0", int(self.hand_data.finger_0.num_segs))
        self.determine_seg_lengths(finger_1_length, "finger_1", int(self.hand_data.finger_1.num_segs))
        
        self.hand_data.ratio.finger_0 = right
        self.hand_data.ratio.finger_1 = left
        self.hand_data.length.palm = palm_width
        self.hand_data.length.finger_0 = finger_0_length
        self.hand_data.length.finger_1 = finger_1_length
        self.hand_data.update()
 
        return self.hand_data
            
    
        
    
    
