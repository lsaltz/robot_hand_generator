#Adapted from its original by Marshall Saltz

import pybullet as p
import pybullet_data
import pathlib
import time

def load(file_path):
    # Resource paths
    #current_path = str(pathlib.Path().resolve())

    #hand_path = current_path + "INSERT PATH TO FILE HERE EX: /data/hand.urdf"

    hand_path = file_path

    #hand_path = current_path + "INSERT PATH TO FILE HERE EX: /data/hand.urdf"

    # Setup simulator

    physics_client = p.connect(p.GUI)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0, 0, -10)

    p.resetDebugVisualizerCamera(cameraDistance=.02, cameraYaw=0, cameraPitch=-89.9999, cameraTargetPosition=[0, 0.1, 0.5])



    # load plane object

    plane_id = p.loadURDF("plane.urdf")

    # load hand object, you can also chang the base orientation if you would like
    # Make sure that the z is high enough so it does not clip the ground plane

    hand_id = p.loadURDF(hand_path, useFixedBase=True, basePosition=[0.0, 0.0, 0.05])

    # Keeps sim window open until you exit
    while p.isConnected():
        p.stepSimulation()
        time.sleep(1./240.)
