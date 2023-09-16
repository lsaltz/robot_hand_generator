#!/bin/bash
mkdir ~/software
cd ~/software
wget https://oregonstate.box.com/shared/static/895kxxvztksqcbjmlzyq7jg1flslseru.xz
tar xf 895kxxvztksqcbjmlzyq7jg1flslseru.xz
mv blender-2.93.7-linux-x64 ./blender-2.93
echo "alias blender="~/software/blender-2.93/blender"" >> ~/.bashrc
source ~/.bashrc
sudo apt update
sudo apt install -y python3-pip
sudo apt install python3-dev
cd ~/robot_hand_generator_MLS/
pip3 install -r requirements.txt
cd ~/software/
git clone https://github.com/bulletphysics/bullet3.git
cd ./bullet3/
python3 setup.py build
python3 setup.py install
~/software/blender-2.93/2.93/python/bin/python3.9 -m ensurepip
~/software/blender-2.93/2.93/python/bin/python3.9 -m pip install upgrade pip
~/software/blender-2.93/2.93/python/bin/python3.9 -m pip install numpy
~/software/blender-2.93/2.93/python/bin/python3.9 -m pip install pathlib
cd ~/robot_hand_generator_MLS/
python3 first_run.py 0 ~/software/blender-2.93/blender

