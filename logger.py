import json
class Logger:
    def __init__(self, image_file_path, json_file_path ):
        self.filename = json_file_path + "/log.json"
        # Open the file in append mode and keep it open
        self.file = open(self.filename, mode='a')
        self.img_path = image_file_path
    
    def create(self, gripper_state_space, object_state_space, gripper_action_space, time):
        log = {
            "Timestep": time,
            "Object State Space": object_state_space,
            "Gripper State Space": gripper_state_space,
            "Gripper Action Space": gripper_action_space,
            # "relative_pos_gripper_obj": relative_pos_gripper_obj include later when other objects are used 
        }
        
        # Write log entry to the file as a JSON object
        json.dump(log, self.file)
        self.file.write("\n")  # Add a newline for readability

    def close(self):
        # Close the file when done
        if self.file:
            self.file.close()

