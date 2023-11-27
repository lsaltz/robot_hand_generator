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
    
    def build_finger(self, finger, i, link_length, child):
        segment = f"segment_{i}"
        child.hand[finger][segment].segment_profile = [0.0, 0.0, 0], [0, 0.0, 0]
        child.hand[finger][segment].segment_dimensions = 0.0322, 0.0165, link_length	#return to this
        child.hand[finger][segment].segment_bottom_joint.joint_style = "pin"
        child.hand[finger][segment].segment_bottom_joint.joint_dimensions = 0.0083, 0.006, 0.0108	
        child.hand[finger][segment].segment_bottom_joint.joint_range = 0, 180
        child.hand[finger][segment].segment_bottom_joint.joint_friction = "n/a"
        child.hand[finger][segment].segment_top_joint.joint_style = "pin"
        child.hand[finger][segment].segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
        child.hand[finger][segment].segment_top_joint.joint_range = 0, 180
        child.hand[finger][segment].segment_top_joint.joint_friction = "n/a"
        child.hand[finger][segment].segment_sensors.sensor_qty = 0
        child.update()
        
    def last_link(self, finger, child, i):
        segment = f"segment_{i}"
        
        child.hand[finger][segment].segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
       	child.hand[finger][segment].segment_dimensions = 0, 0, 0    	
        child.hand[finger][segment].segment_bottom_joint.joint_style = "pin"
        child.hand[finger][segment].segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        child.hand[finger][segment].segment_bottom_joint.joint_range = 0, 180
       	child.hand[finger][segment].segment_bottom_joint.joint_friction = "n/a"
       	
       	child.hand[finger][segment].segment_sensors.sensor_qty = 0
       	   
    def build_fingers(self, ls0, ls1, totalfingerlength, finger, child, hand_data, parent):
        seg_ratios = []
        num_segs = len(ls0)+1
        #choice = random.randint(1,2)

        seg_ratios = self.determine_seg_ratios(finger, num_segs)
        
            
            
        child.hand[finger].clear()
        child.hand[finger].segment_qty = num_segs
        
            
        for i in range(num_segs-1):
            link_length = (totalfingerlength*seg_ratios[i])/100
            self.build_finger(finger, i, link_length, child)
        self.last_link(finger, child, len(seg_ratios))
        hand_data[finger].num_segs = num_segs
        hand_data.ratio.segs[finger] = seg_ratios
        
        hand_data.update()
        child.update()
        return child   
    
    def keep_finger(self, ls, totalfingerlength, finger, child, hand_data):
        seg_ratios = ls
        num_segs = len(ls)+1
        child.hand[finger].clear()
        child.hand[finger].segment_qty = num_segs
        
            
        for i in range(num_segs-1):
            link_length = (totalfingerlength*seg_ratios[i])/100
            self.build_finger(finger, i, link_length, child)
        self.last_link(finger, child, len(seg_ratios))
        hand_data[finger].num_segs = num_segs
        hand_data.ratio.segs[finger] = seg_ratios
        
        hand_data.update()
        child.update()
        return child
        
    def choose_palm_width(self, p):
        choice = random.randint(1,3)
        if choice == 1:
            palm_width = p.length.palm
        else:
            palm_width = round(random.uniform(0.05, 0.09), 5)
        return palm_width
        
    def combo(self, parent1, parent2, p0, p1, num, n, nu):
        hand_data0 = Dict()
        hand_data1 = Dict()
        
        c0 = copy.deepcopy(parent1)
        c1 = copy.deepcopy(parent2)
        
        palmz = 0.053
        palmx = 0.032
        
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
        """
        c0.hand.palm.palm_joints.finger_0.joint_pose = ((0.36/(p0p + p0f)) * p0p)/2, 0, 0
        c0.hand.palm.palm_joints.finger_1.joint_pose = ((0.36/(p0p + p0f)) * p0p)/2, 180, -180
        c0.hand.finger_0.finger_pose = ((0.36/(p0p + p0f)) * p0p)/2, 0, 0
        c0.hand.finger_1.finger_pose = ((0.36/(p0p + p0f)) * p0p)/2, 180, -180
        """
        
        
        c0 = self.build_fingers(p1.ratio.segs.finger_0, p0.ratio.segs.finger_0, finger_0_0, "finger_0", c0, hand_data0, parent1)
        c0 = self.keep_finger(p0.ratio.segs.finger_1, finger_0_1, "finger_1", c0, hand_data0)
        hand_data0.finger_1.num_segs = p0.finger_1.num_segs
        
        hand_data0.ratio.segs.finger_1 = p0.ratio.segs.finger_1
        c1 = self.build_fingers(p0.ratio.segs.finger_1, p1.ratio.segs.finger_1, finger_1_1, "finger_1", c1, hand_data1, parent2)
        c1 = self.keep_finger(p1.ratio.segs.finger_0, finger_1_0, "finger_0", c1, hand_data1)
        hand_data1.finger_0.num_segs = p1.finger_0.num_segs 
        hand_data1.ratio.segs.finger_0 = p1.ratio.segs.finger_0
        
        
        
        hand_data0.ratio.finger_0 = p0f0
        hand_data0.ratio.finger_1 = p0f1
        
        hand_data0.length.palm = self.choose_palm_width(p1)
        c0.hand.palm.palm_dimensions = palmx, hand_data0.length.palm, palmz
        c0.hand.palm.finger_0.joint_pose = hand_data0.length.palm/2, 0, 0
        c0.hand.finger_0.finger_pose = c0.hand.palm.finger_0.joint_pose
        c0.hand.palm.finger_1.joint_pose = hand_data0.length.palm/2, 180, -180
        c0.hand.finger_1.finger_pose = c0.hand.palm.finger_1.joint_pose 
        hand_data0.length.finger_0 = finger_0_0
        hand_data0.length.finger_1 = finger_0_1
        hand_data1.ratio.finger_0 = p1f0
        hand_data1.ratio.finger_1 = p1f1
        hand_data1.length.palm = self.choose_palm_width(p0)
        c1.hand.palm.palm_dimensions = palmx, hand_data1.length.palm, palmz
        c1.hand.palm.finger_0.joint_pose = hand_data1.length.palm/2, 0, 0
        c1.hand.finger_0.finger_pose = c1.hand.palm.finger_0.joint_pose
        c1.hand.palm.finger_1.joint_pose = hand_data1.length.palm/2, 180, -180
        c1.hand.finger_1.finger_pose = c1.hand.palm.finger_1.joint_pose
        hand_data1.length.finger_0 = finger_1_0
        hand_data1.length.finger_1 = finger_1_1
        
        
        
        hand_data0.name = c0.hand.hand_name
        
        hand_data1.name = c1.hand.hand_name
        c1.update()
        c0.update()
        hand_data0.update()
        hand_data1.update()
        self.write_to_json(c0)
        self.write_to_json(c1)
        
        return hand_data0, hand_data1
    
    
