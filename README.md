[![DOI](https://zenodo.org/badge/449414021.svg)](https://zenodo.org/badge/latestdoi/449414021)
# robot_hand_generator_MLS: evolutionary algorithm edition
A tool used to generate an optimal two-fingered gripper design for grasping an object of a certain width. Achieves this by using an evolutionary algorithm to find the design, and runs three different tests whose results can be compared.
This tool can run three different tests and generates the best two-fingered gripper as found by each of those tests. The tests are:
- Straight (default): Number of point pairs separated horizontally by width
- Angle: The number of reachable angles around a center point
- Area: Number of points within the overlapping workspaces of both fingers
After testing at a coarse precision, the program takes the top few hands and tests them at a finer precision.

Parameters are in src/params.py and may be adjusted. 
  
## Requirements:
- Linux OS or WSL with ubuntu

## Install and Setup:

1. Run the following commands:

    First, update your machine:
    
    ```console
    sudo apt update
    sudo apt upgrade
    ```
    Next, copy the following lines into the terminal:
    ```
    cd ~/
    ```
    ```
    git clone https://github.com/lsaltz/robot_hand_generator_MLS.git
    ```
    ```
    cd ~/robot_hand_generator_MLS/
    ```
    ```
    chmod u+x setup.sh
    ```
    ```
    ./setup.sh
    ```

    * This will set up the environment.
    
2. After the environment has finished setting up (this will take some time), run the evolutionary algorithm, open:

    ```console
    cd ~/robot_hand_generator_MLS/src/
    ```
   
   And run:
    
    ```console
    python3 ea.py
    ```
    and specify for how many generations you would like to run it for. The more you enter, the longer it will take. For example, 5000 generations on my desktop takes 2-3 days.
    
   
## output Folder:

After ea.py finishes running, it will send the data it gathered from each test on the top few grippers to two different results files located in ~/robot_hand_generator_MLS/output and ~/robot_hand_generator_MLS/points. In this folder you can find:
- charts of the reachable space of the gripper when run through the test set in params
- figure depicting the changes in maximum fitness score per generation
- figures comparing segment lengths to fitness score
- palm width to fitness score figure
- brief summary of the results as a text file.

Please see Results.md for the current results.

## Additional Notes:
Requires numpy 1.25.0, you may have to downgrade your numpy version.
If you wish to run this software more than once, clear your outputs, hand_archive, and points folders. If you run into issues with MESA and OpenGL, add the following to ~/.bashrc:
```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```
This project was originally created by Josh Campbell, and has been adjusted by me. The original repository can be found at:
https://github.com/OSUrobotics/robot_hand_generator

Advised by Kyle DuFrene, Keegan Knave, and Dr. Cindy Grimm.
