[![DOI](https://zenodo.org/badge/449414021.svg)](https://zenodo.org/badge/latestdoi/449414021)
# robot_hand_generator_MLS: evolutionary algorithm edition
A tool used to generate the best hand design to pick up and hold onto a sphere.

## Requirements:

- Blender 2.93 (only version tested on possibly will work on newer versions)
- Linux os or WSL with ubuntu
- PyBullet for simple visaulization and joint checking
- Python 3.6+


## Install and Setup(git pull):
WSL is currently the only tested method for executing this program.


1. Run the following commands:

    First, update your machine:
    
    ```console
    sudo apt update
    ```
    Next, copy the following lines into the terminal:
    
    ```console
    /bin/bash -c 'mkdir ~/software; \
    cd ~/software; \
    wget https://oregonstate.box.com/shared/static/895kxxvztksqcbjmlzyq7jg1flslseru.xz; \
    tar xf 895kxxvztksqcbjmlzyq7jg1flslseru.xz;\
    mv blender-2.93.7-linux-x64 ./blender-2.93; \
    echo "alias blender="~/software/blender-2.93/blender"" >> ~/.bashrc; \
    source ~/.bashrc; \
    sudo apt update; sudo apt install -y python3-pip;\
    cd ~/ ; git clone https://github.com/lsaltz/robot_hand_generator_MLS.git;\
    cd ~/robot_hand_generator/; pip3 install -r requirements.txt;\
    pip3 install pybullet;\
    pip3 install addict;\
    cd ~/software/; git clone https://github.com/bulletphysics/bullet3.git; cd ./bullet3/; python3 setup.py build; python3 setup.py install;\
    ~/software/blender-2.93/2.93/python/bin/python3.9 -m ensurepip;\
    ~/software/blender-2.93/2.93/python/bin/python3.9 -m pip install upgrade pip;\
    ~/software/blender-2.93/2.93/python/bin/python3.9 -m pip install numpy;\
    ~/software/blender-2.93/2.93/python/bin/python3.9 -m pip install pathlib;\
    cd ~/robot_hand_generator_MLS/; python3 first_run.py 0 ~/software/blender-2.93/blender;\
    '
    ```

    * This will set up the environment.
    
2. To run the evolutionary algorithm, open:

    ```console
    cd ~/robot_hand_generator_MLS/src/
    ```
   
   And run:
    
    ```console
    python3 ea.py
    ```
    and specify for how many generations you would like to run it for. The more you enter, the longer it will take. 
    
    Currently, I have it set to run only in the terminal. If you wish to view the visual testing process, navigate to:
    
    ```console
    cd ~/robot_hand_generator_MLS/src/
    ```
    Open the file with nano or your editor of choice:
    
    ```console
    nano testing.py
    ```
    And change:
     ```console
     physicsClient = p.connect(p.DIRECT)
    ```
    To:
     ```console
     physicsClient = p.connect(p.GUI)
    ```
   
## What the outputs mean:

After ea.py finishes running, it will send all the data it gathered to a text file called "results.txt" located in ~/robot_hand_generator_MLS.
It will also automatically open the fittest file in the simulation for the user to view and test.

If you run the program in GUI mode, you will get hands such as:

![Strange Grasper 0](/imgs/weirdhand0.png?raw=true "Strange Hand")

![Strange Grasper 1](/imgs/weirdhand1.png?raw=true "Strange Hand")

![Strange Grasper 2](/imgs/weirdhand2.png?raw=true "Strange Hand")

These hands are doing their best to grasp the ball. Eventually, after testing multiple generated hands, it should
settle on one of the original graspers or one of their children:

![Test_Hand](/imgs/first_test_hand.png?raw=true "Winning Grasper")

![Test_Hand Grasp](/imgs/grasp.png?raw=true "Winning Grasper Grasping")

It will display the winning hand in PyBullet for the user to test themselves:

![Output Hand](/imgs/output.png?raw=true "Winning Grasper Test")

It will also write the results to a file:

![Results](/imgs/results.png?raw=true "Results")

## Todo:

- Add performance visualization with matplotlib
- Add comments
- Add self collision and controls to output
- Add size constraints to segments
- Generate different object of different sizes
- Figure out why it is not storing all data

## Additional Notes:
This project was originally created by Josh Campbell, and has been adjusted by me. The original repository can be found at:
https://github.com/OSUrobotics/robot_hand_generator

