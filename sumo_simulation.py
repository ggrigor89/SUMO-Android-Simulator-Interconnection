# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:09:37 2016

@author: ga24rag
"""
'''This script initiates a SUMO test simulation where information is exchanged among a server a mobile android application and a sumo simulation client or another client
Communication is facilitated over a VPN network in HAMACHI
Running this script without an active server will result is lagging simulation
'''


import os, sys, time, random,subprocess
import xml.etree.ElementTree as ET
#sys.path.append(os.path.join('C:\\sumo-git\\sumo-git\\tools'))#to be changed!!!
sys.path.append(os.path.join('C:\\sumo-git\\tools'))#to be changed!!!



from numpy import *
from scipy import *
import traci


#sys.path.append(os.path.join('C:\sumo\sumo-0.31.0','tools'))#to be changed!!!
import winsound
import pylab as pl
from win32com.client import GetObject
import sumolib
from sumolib import checkBinary
import math
import random
import csv
import itertools
from shutil import copyfile
import datetime
import traci.constants as tc

import simulator_client
import json



intn = "_Test_Android"
#sumocfg="C:\\Users\\ggrig\\OneDrive\\sumo_ios\\example\\test_networks\\intersection_6_bikes_test.sumo.cfg"
#sumocfg=r"C:\Users\ga24rag\OneDrive - tum.de\sumo_ios\example\test_networks\intersection_6_bikes_test.sumo.cfg"
sumocfg=r"D:\sumo_android_simulator_rep\test_networks\intersection_6_bikes_test.sumo.cfg"

#sumocfg="Y:\\hbs_simulation\\intersection_6.sumo.cfg"
#sumoBinary = "C:\\sumo-git\\sumo-git\\bin\\sumo-gui"
sumoBinary = "C:\\sumo-git\\bin\\sumo-gui"

#sumoBinary = "C:\\sumo-git\\bin\\sumo-gui"
sumoCmd = [sumoBinary, "-c", sumocfg]

SIM_WARMUP_TIME = 100 # warm-up time for the simulation (seconds)
SIM_DURATION = 900 # duration of the simulation (seconds)
SIM_STEP = 0.1
sim_end=str(SIM_WARMUP_TIME+SIM_DURATION)
K=int(sim_end)/SIM_STEP
counter=0  
port=random.randint(8000,8900)
sumoCFG = ET.parse(sumocfg).getroot()
SUMO_CFG_TIMESTEP = float(sumoCFG.find("time").find("step-length").get("value"))
print (SUMO_CFG_TIMESTEP)
if SUMO_CFG_TIMESTEP!=SIM_STEP:
    tree = ET.parse(sumocfg)
    root = tree.getroot()
    elems = tree.find("time").find("step-length")
    print('elems', elems)
    elems.set("value",str(SIM_STEP))
    tree.write(sumocfg)
    print ("SIM STEP CHANGED SUCCESSFULLY TO ",SIM_STEP)    


k=0      # Startvalue for counter of simulation steps

#### begin main loop (simulation) 
#while k<K:
#
#   traci.simulationStep()    
# 
#   k=k+1
#traci.close()

def test_sim_info(vid_list):
    if sim_info_id is None:
        for vid in vid_list:
    #        print (vid,traci.vehicle.getVehicleClass(vid))
            if traci.vehicle.getVehicleClass(vid) == "bicycle":
                
#                traci.vehicle.highlight(vid, color=(255, 0, 0, 255), size=2, alphaMax=-1, duration=-1, type=0)
                traci.vehicle.setColor(vid, color=(255, 0, 0, 255))
                speed = traci.vehicle.getSpeed(vid)
                angle = traci.vehicle.getAngle(vid)
                print (vid," is new sim_info_id ",angle,speed)
                return vid,angle,speed
    else:
                traci.vehicle.setColor(sim_info_id, color=(255, 0, 0, 255))
                speed = traci.vehicle.getSpeed(sim_info_id)
                angle = traci.vehicle.getAngle(sim_info_id)
                print ("sim_info_id",sim_info_id,angle,speed)      
                return sim_info_id,angle,speed
                



print("Running iOS Test Simulation")
traci.start([sumoBinary, "-c", sumocfg], port=port, numRetries=15, label='sim'+str(intn))
k=0      # Startvalue for counter of simulation steps
vid_current = []
sim_info_id = None
while k < K and traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
    
#    if traci.simulation.getTime()%500==0:
#        print (traci.simulation.getTime())    
    
        vid_current = list(traci.simulation.getDepartedIDList())+vid_current
        for vid in list(traci.simulation.getArrivedIDList()):
            if vid in vid_current:
                if vid == sim_info_id:
                    sim_info_id = None
                vid_current.remove(vid)
        sim_info_id,angle_info,speed_info = test_sim_info(vid_current)
        output_dict = {"client_id":"SUMO","id":sim_info_id,"angle":k,"speed":speed_info}
        output_json = json.dumps(output_dict)
    
    #    transmission = str("TESTING SUCCESS TIME "+str(traci.simulation.getTime()))
        transmission = output_json
    #    output_json_string = output_json.encode("Utf-8")
    #    output_json_string_to_json = json.loads(output_json_string)
        if traci.simulation.getTime()%2==0:
    #    output_json_string_to_json["color"] = (255,192,203)
            try:
                
                
                data_rc = simulator_client.transmit(transmission)
                output_server_rc = json.loads(data_rc)
                traci.vehicle.setColor(output_server_rc["id"], color=output_server_rc["color"])
                print (output_server_rc["smartphone"])
                
            except:
                continue
    
    
       
        k+=1
print("Simulation ended on step "+str(k)+".")
traci.close()
sys.stdout.flush()
time.sleep(10)        
current_time=datetime.datetime.now()




        
        
        
        
        
        
        
        
        
        
        
    
    
    
    