# -*- coding: utf-8 -*-
from stlib3.scene import MainHeader, ContactHeader
from stlib3.physics.rigid import Floor, Cube
from gripper import Gripper

# import csv 

# class action( ):
#     def __init__(self):
#         self.object = 
    
#     def _get_action_space(self):
        

# class robotArm():
#     def __init( self):
#         self.robotObject = 

#     def _get_state_space(self):
        
# class obj():
#     def __init__(self):
#         pass
#     def _get_state_space(self):
        

def createScene(rootNode):
    """This is my first scene"""
    MainHeader(rootNode, gravity=[0.0, -981.0, 0.0], plugins=["SoftRobots"])
    ContactHeader(rootNode, alarmDistance=4, contactDistance=3, frictionCoef=0.08)
    rootNode.VisualStyle.displayFlags = "showCollisionModels"

    Gripper(rootNode)

    Floor(rootNode, name="Floor",
          color=[1.0, 0.0, 0.0, 1.0],
          translation=[0.0, -160.0, 0.0],
          isAStaticObject=True)

    Cube(rootNode, name="Cube",
         uniformScale=20.0,
         color=[1.0, 1.0, 0.0, 1.0],
         totalMass=0.03,
         volume=20,
         inertiaMatrix=[1000.0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 1000.0],
         translation=[0.0, -130.0, 10.0])

    return rootNode
