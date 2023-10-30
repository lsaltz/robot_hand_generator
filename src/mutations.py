# By Marshall Saltz

import random
import numpy as np
import os
import json
from addict import Dict
import copy

class Mutate:

    def __init__(self, robot_gripper, data, generation):
        
        self.hand_data = Dict()
        self.upper = 10
        self.lower = 1
        self.total_size = 0.36
        self.robot_gripper = robot_gripper
        self.data = data
        self.generation = generation
        
    def mutation_ratios(self):
        ratio = np.random.randint(self.lower, self.upper)
        return ratio
        
    def finger_1(self, palm_width, segment_count_1):
        self.robot_gripper.hand.palm.palm_joints.finger_1.joint_pose = palm_width/2, 180, -180
        self.robot_gripper.hand.palm.palm_joints.finger_1.joint_style = "pin"
        self.robot_gripper.hand.palm.palm_joints.finger_1.joint_dimensions = 0.0083, 0.006, 0.0108
        self.robot_gripper.hand.finger_1.segment_qty = segment_count_1
        self.robot_gripper.hand.finger_1.finger_pose = palm_width/2, 180, -180
        
       	
    def finger_0(self, palm_width, segment_count_0):
        self.robot_gripper.hand.palm.palm_joints.finger_0.joint_pose = palm_width/2, 0, 0
        self.robot_gripper.hand.palm.palm_joints.finger_0.joint_style = "pin"
        self.robot_gripper.hand.palm.palm_joints.finger_0.joint_dimensions = 0.0083, 0.006, 0.0108
        self.robot_gripper.hand.finger_0.segment_qty = segment_count_0
        self.robot_gripper.hand.finger_0.finger_pose = palm_width/2, 0, 0
        
    def build_finger(self, finger, i, link_length):
        segment = f"segment_{i}"
        self.robot_gripper.hand[finger][segment].segment_profile = [0.0, 0.0, 0], [0, 0.0, 0]
        self.robot_gripper.hand[finger][segment].segment_dimensions = 0.0322, 0.0165, link_length	#return to this
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_style = "pin"
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_dimensions = 0.0083, 0.006, 0.0108	
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_range = 0, 180
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_friction = "n/a"
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_style = "pin"
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_range = 0, 180
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_friction = "n/a"
        self.robot_gripper.hand[finger][segment].segment_sensors.sensor_qty = 0

    def last_link(self, finger, i):
        segment = f"segment_{i}"
        
        self.robot_gripper.hand[finger][segment].segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
        self.robot_gripper.hand[finger][segment].segment_dimensions = 0, 0, 0    	
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_style = "pin"
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_range = 0, 180
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_friction = "n/a"
        self.robot_gripper.hand[finger][segment].segment_sensors.sensor_qty = 0
        
        
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
            self.build_finger(finger, i, link_length)
        self.last_link(finger, num_segs-1)
        
    def build_hand(self):
        
        file_name = "hand_mut_gen_" + str(self.generation)
        
        palmz = 0.053
        palmx = 0.032
        self.hand_data.name = file_name
        self.hand_data.finger_0.num_segs = random.randint(3, 4)
        self.hand_data.finger_1.num_segs = random.randint(3, 4)
        
        #palm = self.mutation_ratios()
        #fingers = self.mutation_ratios()
        right = self.mutation_ratios()
        left = self.mutation_ratios()
        
        palm_width = self.data.length.palm
        fingers_total_length = 0.288
        finger_0_length = fingers_total_length/(right+left) * right
        finger_1_length = fingers_total_length - finger_0_length
        
        self.robot_gripper.hand.hand_name = file_name
        self.robot_gripper.hand.palm.palm_style = "cuboid"
        self.robot_gripper.hand.palm.palm_dimensions = palmx, palm_width, palmz
        
        self.robot_gripper.hand.palm.finger_qty = 2
        self.finger_0(palm_width, int(self.hand_data.finger_0.num_segs))
        self.determine_seg_lengths(finger_0_length, "finger_0", int(self.hand_data.finger_0.num_segs))
        self.finger_1(palm_width, int(self.hand_data.finger_1.num_segs))
        self.determine_seg_lengths(finger_1_length, "finger_1", int(self.hand_data.finger_1.num_segs))
        self.robot_gripper.objects.object_qty = 0

        self.robot_gripper.update()
        self.hand_data.ratio.finger_0 = right
        self.hand_data.ratio.finger_1 = left
        self.hand_data.length.palm = palm_width
        self.hand_data.length.finger_0 = finger_0_length
        self.hand_data.length.finger_1 = finger_1_length
        self.hand_data.update()
        
        with open('../hand_json_files/hand_queue_json/' + file_name + '.json', mode="w") as jfile:        
            new_json = ""
            new_json += json.dumps(self.robot_gripper, indent=4)
                
            jfile.write(new_json)
        jfile.close()       
        
        self.robot_gripper.clear()  
        print(self.hand_data)      
        return self.hand_data
            
    
        
    
    
