# Apapted from Josh Campbell by Marshall Saltz

import random
import numpy as np
import os
import json
from addict import Dict


def mutate(mutationsNum, max_segments, generation):
    robot_gripper = Dict()

    i = 0
    while (i < mutationsNum):

        file_name = "hand_mut_" + str(i) + '_gen_' + str(generation)

        segment_count_1 = np.random.randint(1, max_segments)
        segment_count_2 = np.random.randint(1, max_segments)

        robot_gripper.hand.hand_name = "hand_" + str(i)
        robot_gripper.hand.palm.palm_style = "cuboid"
        robot_gripper.hand.palm.palm_dimensions = 0.032, 0.075, 0.053
        robot_gripper.hand.palm.finger_qty = 2

        random1 = random.random()
        random2 = random.random()
        random3 = random.random()

        robot_gripper.hand.palm.palm_joints.finger_0.joint_pose = 0.02675, 0, 0
        robot_gripper.hand.palm.palm_joints.finger_0.joint_style = "pin"
        robot_gripper.hand.palm.palm_joints.finger_0.joint_dimensions = random1, random2, random3

        robot_gripper.hand.palm.palm_joints.finger_1.joint_pose = 0.02675, 180, -180
        robot_gripper.hand.palm.palm_joints.finger_1.joint_style = "pin"
        robot_gripper.hand.palm.palm_joints.finger_1.joint_dimensions = random1, random2, random3
            
        robot_gripper.hand.finger_0.segment_qty = segment_count_1
        robot_gripper.hand.finger_0.finger_pose = 0.02675, 0, 0

        num1 = 0
        num2 = 0    
        while (num1 < segment_count_1):
            segment_index_f1 = "segment_" + str(num1)

            rand1 = random.random()
            rand2 = random.random()
            rand3 = random.random()
            rand4 = random.random()
            rand5 = random.random()
            rand6 = random.random()
            rand7 = random.random()
            rand8 = random.random()
            rand9 = random.random()
                
            robot_gripper.hand.finger_0[segment_index_f1].segment_profile = [0, 0, 0], [0, 0, 0]
            robot_gripper.hand.finger_0[segment_index_f1].segment_dimensions = rand1, rand2, rand3
            robot_gripper.hand.finger_0[segment_index_f1].segment_bottom_joint.joint_style = "pin"
            robot_gripper.hand.finger_0[segment_index_f1].segment_bottom_joint.joint_dimensions = rand4, rand5, rand6
            robot_gripper.hand.finger_0[segment_index_f1].segment_bottom_joint.joint_range = 0, 180
            robot_gripper.hand.finger_0[segment_index_f1].segment_bottom_joint.joint_friction = "n/a"
            robot_gripper.hand.finger_0[segment_index_f1].segment_top_joint.joint_style = "pin"
            robot_gripper.hand.finger_0[segment_index_f1].segment_top_joint.joint_dimensions = rand7, rand8, rand9
            robot_gripper.hand.finger_0[segment_index_f1].segment_top_joint.joint_range = 0, 180
            robot_gripper.hand.finger_0[segment_index_f1].segment_top_joint.joint_friction = "n/a"
            robot_gripper.hand.finger_0[segment_index_f1].segment_sensors.sensor_qty = 0

            num1 += 1
            
        robot_gripper.hand.finger_1.segment_qty = segment_count_2
        robot_gripper.hand.finger_1.finger_pose = 0.02675, 180, -180
        
        while (num2 < segment_count_2):
            segment_index_f2 = "segment_" + str(num2)
            
            ran1 = random.random()
            ran2 = random.random()
            ran3 = random.random()
            ran4 = random.random()
            ran5 = random.random()
            ran6 = random.random()
            ran7 = random.random()
            ran8 = random.random()
            ran9 = random.random()
                
            robot_gripper.hand.finger_1[segment_index_f2].segment_profile = [0, 0, 0], [0, 0, 0]
            robot_gripper.hand.finger_1[segment_index_f2].segment_dimensions = ran1, ran2, ran3
            robot_gripper.hand.finger_1[segment_index_f2].segment_bottom_joint.joint_style = "pin"
            robot_gripper.hand.finger_1[segment_index_f2].segment_bottom_joint.joint_dimensions = ran4, ran5, ran6
            robot_gripper.hand.finger_1[segment_index_f2].segment_bottom_joint.joint_range = 0, 180
            robot_gripper.hand.finger_1[segment_index_f2].segment_bottom_joint.joint_friction = "n/a"
            robot_gripper.hand.finger_1[segment_index_f2].segment_top_joint.joint_style = "pin"
            robot_gripper.hand.finger_1[segment_index_f2].segment_top_joint.joint_dimensions = ran7, ran8, ran9
            robot_gripper.hand.finger_1[segment_index_f2].segment_top_joint.joint_range = 0, 180
            robot_gripper.hand.finger_1[segment_index_f2].segment_top_joint.joint_friction = "n/a"
            robot_gripper.hand.finger_1[segment_index_f2].segment_sensors.sensor_qty = 0

            num2 += 1
            
        robot_gripper.objects.object_qty = 0

        robot_gripper.update()
        with open('../hand_json_files/hand_queue_json/' + file_name + '.json', mode="w") as jfile:        
            new_json = ""
            new_json += json.dumps(robot_gripper, indent=4)
                
            jfile.write(new_json)
            jfile.close()       
        i += 1
        
        robot_gripper.clear()
    else:
        print("Generation iteration complete")