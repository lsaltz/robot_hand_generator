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
    
    
    """
    This converts the json files to dictionaries, and takes in an argument
    of the json file.
    """
    def json_to_dictionaries(self, jfile):
        with open(jfile, mode="r+") as parentfile:
            dictionary = json.load(parentfile)
            parent = Dict(dictionary)
        parentfile.close()
        return parent

    """
    This converts the dictionaries to json files.
    """  
    def write_to_json(self, child):
        with open('../hand_json_files/hand_queue_json/{0}.json'.format(child.hand.hand_name), mode = "w") as f:
            new_json = json.dumps(child, indent=4)
            f.write(new_json)
        f.close()
    
    """
    Combo takes two parent files and combines them. returns two dictionaries
    """ 
    def build_fingers(self, ls0, ls1, totalfingerlength, finger, child, hand_data):
        seg_ratios = []
        num_segs = len(ls0)
        if len(ls0) == len(ls1):
            seg_ratios = copy.deepcopy(ls0)
            for i in range(len(ls0)):
                seg = f"segment_{i}"
                child.hand[finger][seg].segment_dimensions = 0.0322, 0.0165, (ls0[i] * totalfingerlength)/100
        else:
            prev_rat = 100
            nm = num_segs - 2
            
            ct = 0
            rat_ct = 0
            for i in range(nm):
                seg = f"segment_{i}"
                rat = np.random.randint(1, prev_rat)
                seg_ratios.append(rat)
                child.hand.finger_0[seg].segment_dimensions = 0.0322, 0.0165, (rat*totalfingerlength)/100
                rat_ct += (rat*totalfingerlength)/100
                prev_rat = rat
                ct += prev_rat
                
            seg_ratios.append(100-ct)
        
            
            
            
               
            seg = f"segment_{nm}"
            child.hand[finger][seg].segment_dimensions = 0.0322, 0.0165, totalfingerlength-rat_ct
        hand_data.ratio.segs[finger] = seg_ratios
        print(seg_ratios)
        hand_data.update()
        child.update()
        return child    
    
    def combo(self, parent1, parent2, p0, p1, num, n, nu):
        hand_data0 = Dict()
        hand_data1 = Dict()
        
        c0 = copy.deepcopy(parent1)
        c1 = copy.deepcopy(parent1)
        
         
        
        c0.hand.hand_name = "child_0_" + str(num) + "_" + str(nu) + n
        c1.hand.hand_name = "child_1_" + str(num) + "_" + str(nu) + n
        
        """
        num_segs_0_0 = parent1.hand.finger_0.segment_qty
        num_segs_0_1 = parent1.hand.finger_1.segment_qty
        num_segs_1_0 = parent2.hand.finger_0.segment_qty
        num_segs_1_1 = parent2.hand.finger_1.segment_qty
        
        hand_data0.finger_0.num_segs = num_segs_0_1
        hand_data0.finger_1.num_segs = num_segs_1
        hand_data0.finger_0.num_segs = num_segs_0
        hand_data0.finger_1.num_segs = num_segs_1
        """
        
        p0f0 = p0.ratio.finger_0
        p0f1 = p0.ratio.finger_1
        
        
        p1f0 = p1.ratio.finger_0
        p1f1 = p1.ratio.finger_1
        
        
        fingers_length_0 = 0.288
        fingers_length_1 = 0.288
        finger_0_0 = (fingers_length_0/(p0f0+p0f1))*p0f0
        finger_0_1 = (fingers_length_0/(p0f0+p0f1))*p0f1
        finger_1_0 = (fingers_length_1/(p1f0+p1f1))*p1f0
        finger_1_1 = (fingers_length_1/(p1f0+p1f1))*p1f1
        """
        c0.hand.palm.palm_joints.finger_0.joint_pose = ((0.36/(p0p + p0f)) * p0p)/2, 0, 0
        c0.hand.palm.palm_joints.finger_1.joint_pose = ((0.36/(p0p + p0f)) * p0p)/2, 180, -180
        c0.hand.finger_0.finger_pose = ((0.36/(p0p + p0f)) * p0p)/2, 0, 0
        c0.hand.finger_1.finger_pose = ((0.36/(p0p + p0f)) * p0p)/2, 180, -180
        """
        
        
        c0 = self.build_fingers(p1.ratio.segs.finger_0, p0.ratio.segs.finger_0, finger_0_0, "finger_0", c0, hand_data0)
        
        c1 = self.build_fingers(p0.ratio.segs.finger_1, p1.ratio.segs.finger_1, finger_1_1, "finger_1", c1, hand_data1)
        
        
        hand_data0.ratio.finger_0 = p0f0
        hand_data0.ratio.finger_1 = p0f1
        hand_data0.length.palm = p1.length.palm
        hand_data0.length.finger_0 = finger_0_0
        hand_data0.length.finger_1 = finger_0_1
        hand_data1.ratio.finger_0 = p1f0
        hand_data1.ratio.finger_1 = p1f1
        hand_data1.length.palm = p0.length.palm
        hand_data1.length.finger_0 = finger_1_0
        hand_data1.length.finger_1 = finger_1_1
        
        
        
        hand_data0.name = c0.hand.hand_name
        
        hand_data1.name = c1.hand.hand_name
        
        hand_data0.update()
        hand_data1.update()
        self.write_to_json(c0)
        self.write_to_json(c1)
        
        return hand_data0, hand_data1
    
    
