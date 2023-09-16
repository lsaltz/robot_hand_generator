# By Marshall Saltz

import random
import numpy as np
import os
import json
from addict import Dict
import copy

"""
This file mutates the segment amount and size, creating mutated files.
"""
   
def mutate(mutationsNum, max_segments, robot_gripper, data, generation):
    
    list_of_dics = []
    hand_data = Dict()
    upper = 10
    lower = 1
    total_size = 0.36
    for i in range(mutationsNum):

        num = np.random.randint(1, 6)
        if num == 1: #palm:fingers
            ratio_palm = round(random.uniform(lower, upper),2)
            ratio_fingers = round(random.uniform(lower, upper),2)
            ratio_proximal = data['proximal']
            ratio_distal = data['distal']
        elif num == 2: #fingers:proximal
            ratio_fingers = round(random.uniform(lower, upper),2)
            ratio_palm = data['palm']
            ratio_proximal = round(random.uniform(lower, upper),2)
            ratio_distal = data['distal']
        elif num == 3: #palm:proximal
            ratio_proximal = round(random.uniform(lower, upper),2)
            ratio_palm = round(random.uniform(lower, upper),2)
            ratio_fingers = data['fingers']
            ratio_distal = data['palm']
        elif num == 4: #palm:distal
            ratio_proximal = data['proximal']
            ratio_palm = round(random.uniform(lower, upper),2)
            ratio_fingers = data['fingers']
            ratio_distal = round(random.uniform(lower, upper),2)
        elif num == 5: #proximal:distal
            ratio_proximal = round(random.uniform(lower, upper),2)
            ratio_palm = data['palm']
            ratio_fingers = data['fingers']
            ratio_distal = round(random.uniform(lower, upper),2)
        else: #fingers:distal
            ratio_proximal = data['proximal']
            ratio_palm = data['palm']
            ratio_fingers = round(random.uniform(lower, upper),2)
            ratio_distal = round(random.uniform(lower, upper),2)
        
        
        palm_width = (total_size / (ratio_palm + ratio_fingers)) * ratio_palm
        finger_length = (total_size / (ratio_palm + ratio_fingers)) * ratio_fingers
        proximal_length = (finger_length / (ratio_proximal + ratio_distal)) * ratio_proximal
        distal_length = (finger_length / (ratio_proximal + ratio_distal)) * ratio_distal
        palmz = 0.053
        palmx = 0.032
        file_name = "hand_mut_" + str(i) + '_gen_' + str(generation)
        
        hand_data.name = file_name
        hand_data.palm = ratio_palm
        hand_data.fingers = ratio_fingers
        hand_data.proximal = ratio_proximal
        hand_data.distal = ratio_distal
        hand_data.update()
        #print("hd: ", hand_data)
        list_of_dics.append(copy.deepcopy(hand_data))
        hand_data.clear()
        
        #print("Ratios used for: {} are(palm to fingers): {}:{} and(proximal to distal): {}:{}".format(file_name, ratio_palm, ratio_fingers, ratio_proximal, ratio_distal))
        segment_count_0 = max_segments	#np.random.randint(1, max_segments)
        segment_count_1 = max_segments	#np.random.randint(1, max_segments)

        robot_gripper.hand.hand_name = file_name
        robot_gripper.hand.palm.palm_style = "cuboid"
        robot_gripper.hand.palm.palm_dimensions = palmx, palm_width, palmz
        robot_gripper.hand.palm.finger_qty = 2


        robot_gripper.hand.palm.palm_joints.finger_0.joint_pose = palm_width/2, 0, 0
        robot_gripper.hand.palm.palm_joints.finger_0.joint_style = "pin"
        robot_gripper.hand.palm.palm_joints.finger_0.joint_dimensions = 0.0083, 0.006, 0.0108	#return to this

        robot_gripper.hand.palm.palm_joints.finger_1.joint_pose = palm_width/2, 180, -180
        robot_gripper.hand.palm.palm_joints.finger_1.joint_style = "pin"
        robot_gripper.hand.palm.palm_joints.finger_1.joint_dimensions = 0.0083, 0.006, 0.0108	#return to this WDL
            
        robot_gripper.hand.finger_0.segment_qty = segment_count_0
        robot_gripper.hand.finger_0.finger_pose = palm_width/2, 0, 0
       
        robot_gripper.hand.finger_0.segment_0.segment_profile = [0.0, 0.0, 0], [0, 0.0, 0]
        robot_gripper.hand.finger_0.segment_0.segment_dimensions = 0.0322, 0.0165, proximal_length	#return to this
        robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_dimensions = 0.0083, 0.006, 0.0108	
       	robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_style = "pin"
       	robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
       	robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_0.segment_0.segment_sensors.sensor_qty = 0

        robot_gripper.hand.finger_0.segment_1.segment_profile = [0, 0.0, 0], [0, 0.0, 0]
       	robot_gripper.hand.finger_0.segment_1.segment_dimensions = 0.0322, 0.0213, distal_length	
        robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
        robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_dimensions = 0,0,0	#return to this
        robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_0.segment_1.segment_sensors.sensor_qty = 0
        
        robot_gripper.hand.finger_0.segment_2.segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
       	robot_gripper.hand.finger_0.segment_2.segment_dimensions = 0, 0, 0    	
       	robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_friction = "n/a"
       	
       	robot_gripper.hand.finger_0.segment_2.segment_sensors.sensor_qty = 0
       	
       	
        robot_gripper.hand.finger_1.segment_qty = segment_count_1
        robot_gripper.hand.finger_1.finger_pose = palm_width/2, 180, -180

        robot_gripper.hand.finger_1.segment_0.segment_profile = [0, 0, 0], [0, 0, 0]
       	robot_gripper.hand.finger_1.segment_0.segment_dimensions = 0.0322, 0.0165, proximal_length	
        robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_style = "pin"
       	robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_dimensions = 0.008, 0.006, 0.01083	
       	robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_style = "pin"
       	robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
       	robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_1.segment_0.segment_sensors.sensor_qty = 0

        robot_gripper.hand.finger_1.segment_1.segment_profile = [0, 0.0, 0], [0, 0.0, 0]
       	robot_gripper.hand.finger_1.segment_1.segment_dimensions = 0.0322, 0.0213, distal_length	
        robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_style = "pin"
       	robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
       	robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_style = "pin"
        robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_dimensions = 0, 0, 0	#return to this
        robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_1.segment_1.segment_sensors.sensor_qty = 0
        
        robot_gripper.hand.finger_1.segment_2.segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
       	robot_gripper.hand.finger_1.segment_2.segment_dimensions = 0, 0, 0    	
       	robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_friction = "n/a"
       	
       	robot_gripper.hand.finger_1.segment_2.segment_sensors.sensor_qty = 0
        
        robot_gripper.objects.object_qty = 0

        robot_gripper.update()
        
        with open('../hand_json_files/hand_queue_json/' + file_name + '.json', mode="w") as jfile:        
            new_json = ""
            new_json += json.dumps(robot_gripper, indent=4)
                
            jfile.write(new_json)
        jfile.close()       
        
        robot_gripper.clear()        
    return list_of_dics
