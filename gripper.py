# -*- coding: utf-8 -*-
from grippercontroller import GripperController
from finger import Finger


def Gripper(logObj, parentNode=None):
    
    selfNode = parentNode.addChild("Gripper")    
    rootNode = parentNode

    f1, translation_f2 = Finger(logObj, rootNode, selfNode, "Finger1",
                   rotation=[0, 0, 105],
                   #rotation=[0, 0, 180],
                   translation=[20.0,0.0, 0.0],
                   fixingBox=[-20, -10, 0, 20, 10, 15],
                   pullPointLocation=[3, 10.5, 3])

    f2, translation_f2 = Finger(logObj, rootNode, selfNode, "Finger2",
                   rotation=[180, 0, 65],
                   translation=[-10.0,0.0, -4.0],
                   fixingBox=[-20, -10, -30, 20, 10, 0],
                   pullPointLocation=[3, 10.5, -7])

    f3, translation_f2 = Finger(logObj, rootNode, selfNode, "Finger3",
                   rotation=[180, 0, 65],
                   translation=[-10.0,0.0, 34.0],
                   fixingBox=[-20, -10, 0, 20, 10, 50],
                   pullPointLocation=[3, 10.5, 31.5])

    selfNode.addObject(GripperController(logObj, [f1,f2,f3], selfNode, parentNode))
    
    return selfNode


def createScene(rootNode):
    from stlib3.scene import MainHeader, ContactHeader
    MainHeader(rootNode, gravity=[0.0, -981.0, 0.0], plugins=["SoftRobots"])
    ContactHeader(rootNode, alarmDistance=4, contactDistance=3, frictionCoef=0.08)
    rootNode.VisualStyle.displayFlags = "showBehavior showCollisionModels"

    Gripper(parentNode=rootNode)
    return rootNode
