# By Marshall Saltz

import random
import copy
import numpy as np
import os
import json
from addict import Dict

class crossoverFunctions:

    def __init__(self, generation):
        self.dictionary = Dict()
        self.generation = generation
    
    def read_dict(self, data):
        palm = data['palm']
        fing = data['fingers']
        prox = data['proximal']
        dis = data['distal']
        
        return palm, fing, prox, dis
        
    """
    This converts the json files to dictionaries, and takes in an argument
    of the json file.
    """
    def json_to_dictionaries(self, jfile):
        with open(jfile, mode="r") as parentfile:
            dictionary = json.load(parentfile)
            parent = Dict(dictionary)
            parentfile.close()
        print("parent dictionaries created")
        return parent

    """
    This converts the dictionaries to json files.
    """  
    def write_to_json(self, child):
        with open('../hand_json_files/hand_queue_json/{0}.json'.format(child.hand.hand_name), mode = "w") as f:
            new_json = json.dumps(child, indent=4)
            f.write(new_json)
            f.close()
               
    def combo(self, parent1, parent2, p0, p1, num):
        """
        1. child 1: p1 palm to fingers ratio, p2 proximal to distal ratio
        2. child 2: p2 palm to fingers ratio, p1 proximal to distal ratio
        """
        hand_data0 = Dict()
        hand_data1 = Dict()
        c0 = copy.deepcopy(parent1)
        c1 = copy.deepcopy(parent1)
        c0.hand.hand_name = "child_0_" + str(num)
        c1.hand.hand_name = "child_1_" + str(num)
        palm1, fing1, prox1, dis1 = self.read_dict(p0)#edit all this.
        palm2, fing2, prox2, dis2 = self.read_dict(p1)
        finger_length0 = (0.36 / (palm1 + fing1)) * fing1
        p_length0 = (finger_length0 / (prox2 + dis2)) * prox2
        d_length0 = (finger_length0 / (prox2 + dis2)) * dis2
        finger_length1 = (0.36 / (palm2 + fing2)) * fing2
        p_length1 = (finger_length1 / (prox1 + dis1)) * prox1
        d_length1 = (finger_length1 / (prox1 + dis1)) * dis1
        palmz = 0.053
        
        c0.hand.palm.palm_dimensions = 0.032, (0.36/(palm1 + fing1)) * palm1, palmz
        c0.hand.palm.palm_joints.finger_0.joint_pose = ((0.36/(palm1 + fing1)) * palm1)/2, 0, 0
        c0.hand.palm.palm_joints.finger_1.joint_pose = ((0.36/(palm1 + fing1)) * palm1)/2, 180, -180
        c0.hand.finger_0.finger_pose = ((0.36/(palm1 + fing1)) * palm1)/2, 0, 0
        c0.hand.finger_1.finger_pose = ((0.36/(palm1 + fing1)) * palm1)/2, 180, -180
        c0.hand.finger_0.segment_0.segment_dimensions = 0.0322, 0.0165, p_length0
        c0.hand.finger_1.segment_0.segment_dimensions = 0.0322, 0.0165, p_length0
        c0.hand.finger_0.segment_1.segment_dimensions = 0.0322, 0.0213, d_length0
        c0.hand.finger_1.segment_1.segment_dimensions = 0.0322, 0.0213, d_length0
        
        c1.hand.palm.palm_dimensions = 0.032, (0.36/(palm2 + fing2)) * palm2, palmz
        c1.hand.palm.palm_joints.finger_0.joint_pose = ((0.36/(palm2 + fing2)) * palm2)/2, 0, 0
        c1.hand.palm.palm_joints.finger_1.joint_pose = ((0.36/(palm2 + fing2)) * palm2)/2, 180, -180
        c1.hand.finger_0.finger_pose = ((0.36/(palm2 + fing2)) * palm2)/2, 0, 0
        c1.hand.finger_1.finger_pose = ((0.36/(palm2 + fing2)) * palm2)/2, 180, -180
        c1.hand.finger_0.segment_0.segment_dimensions = 0.0322, 0.0165, p_length1
        c1.hand.finger_1.segment_0.segment_dimensions = 0.0322, 0.0165, p_length1
        c1.hand.finger_0.segment_1.segment_dimensions = 0.0322, 0.0213, d_length1
        c1.hand.finger_1.segment_1.segment_dimensions = 0.0322, 0.0213, d_length1
        
        hand_data0.name = c0.hand.hand_name
        hand_data0.palm = palm1
        hand_data0.fingers = fing1
        hand_data0.proximal = prox2
        hand_data0.distal = dis2
        hand_data0.total_height = palmz + finger_length0
        hand_data0.palm_z = palmz
        hand_data0.finger_z = finger_length0
        hand_data1.name = c1.hand.hand_name
        hand_data1.palm = palm2
        hand_data1.fingers = fing2
        hand_data1.proximal = prox1
        hand_data1.distal = dis1
        hand_data1.total_height = palmz + finger_length1
        hand_data1.palm_z = palmz
        hand_data1.finger_z = finger_length1
        hand_data0.update()
        hand_data1.update()
        self.write_to_json(c0)
        self.write_to_json(c1)
        
        return hand_data0, hand_data1
