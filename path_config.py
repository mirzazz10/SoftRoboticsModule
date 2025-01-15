import os
import random
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
rand_int = random.randint(1, 100)   
folder_name = f"{timestamp}"
store_path = "/home/rahman/ext_plugin_repo/SoftRobots/examples/tutorials/CableGripper/details/dataSet/cable_gripper_cube" # change this when the object is changed
os.makedirs( store_path + "/" + folder_name, exist_ok= True)
image_file_path = store_path + "/" + folder_name +'/images'
json_file_path = store_path + "/" + folder_name +'/json'
os.makedirs( image_file_path, exist_ok= True)
os.makedirs( json_file_path, exist_ok= True)

