# By Marshall Saltz
import random
import numpy as np
import os
import json
import mutations
from addict import Dict
import matplotlib.pyplot as plt
import testing
import time
import main
from pathlib import Path
import basic_load
import combination
import first_generation
import copy
import pandas as pd
import shutil
import sqlite3


class Manage_Databases:

    def __init__(self, connection1, connection2):
        self.connection1 = connection1
        self.connection2 = connection2
        self.cursor1 = connection1.cursor()
        self.cursor2 = connection2.cursor()
 
    def json_to_binary(jfile):
        with open(jfile, mode="r") as f:
            hand_data = json.load(f)
            data_binary = json.dumps(hand_data).encode('utf-8')
        f.close()     
        return data_binary

    """
    Adds files to SQLite Database
    Parameters:
        genList: generational list of grippers
        connection1: connection to points list database
        connection2: connection to gripper json database
        first: gripper with highest fitness score
    """
    def add_to_database(genList, first):
        for i in range(len(genList)):
            if genList[i].name + '.json' != str(first):
                f_name = genList[i].name + ".json"
            
                jfile1 = f"../points/{genList[i].name}.json"
                bin1 = self.json_to_binary(jfile1)
                self.cursor1.execute("insert into hand_data (ID, name, data) values(?,?,?)",(i, f_name, bin1))
                self.connection1.commit()
                jfile2 = f"../hand_json_files/hand_archive_json/{genList[i].name}.json"
                bin2 = self.json_to_binary(jfile2)
                self.cursor2.execute("insert into hand_files (ID, name, data) values(?,?,?)",(i, f_name, bin2))
                self.connection2.commit()     
                os.remove(jfile1)
                os.remove(jfile2)
         

    def get_from_database(ten_list, first):
        for t in ten_list:
            f_name = t[1]
            if f_name != str(first):
                self.cursor1.execute("select data from hand_data where name=?", (f_name,))
                self.connection.commit()
                for row in self.cursor1:
                    with open(f"../points/{f_name}", mode="w") as f:
                        s_data = b''.join(row)
                        json_file = json.loads(json.dumps(s_data.decode('utf-8'), indent=4))#.decode('utf-8')
                        f.write(json_file)
                    f.close()
                    
