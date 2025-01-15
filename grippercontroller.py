# -*- coding: utf-8 -*-
import Sofa.Core
import Sofa.constants.Key as Key
from finger import get_logging_data
from math import cos, sin, pi

def getTranslated(points, vec):
    r = []
    for v in points:
        r.append([v[0] + vec[0], v[1] + vec[1], v[2] + vec[2]])
    return r



# rotation function for the gripper 
#
# 

def getRotated(rotate, points, angle, rotationCenter):
    r = []
    for v in points:
        r.append(rotate(v, angle, rotationCenter))
    return r

def getRotationCenter(fingers):
    """Find the rotation center.

    Parameters:
    ----------
        fingers: list
            The fingers.

    Returns:
    -------
        The rotation center.

    """
    rotation_center = [0, 0, 0]

    for finger in fingers:
        m = finger.getChild("ElasticMaterialObject")        
        cable = m.getChild("PullingCable").getObject("CableConstraint")
        p = cable.pullPoint
        rotation_center = [rotation_center[0] + p[0]/len(fingers),
                           rotation_center[1] + p[1]/len(fingers),
                           rotation_center[2] + p[2]/len(fingers)]
    return rotation_center

def rotate_x(point, angle, rotationCenter):
    translated = [point[0]-rotationCenter[0], point[1]-rotationCenter[1], point[2]-rotationCenter[2]]
    rotated = [translated[0],
               translated[1]*cos(angle)-translated[2]*sin(angle),
               translated[1]*sin(angle)+translated[2]*cos(angle)]
    return [rotated[0]+rotationCenter[0], rotated[1]+rotationCenter[1], rotated[2]+rotationCenter[2]]


def rotate_y(point, angle, rotationCenter):
    translated = [point[0]-rotationCenter[0], point[1]-rotationCenter[1], point[2]-rotationCenter[2]]
    rotated = [translated[0]*cos(angle)+translated[2]*sin(angle),
               translated[1],
               -translated[0]*sin(angle)+translated[2]*cos(angle)]
    return [rotated[0]+rotationCenter[0], rotated[1]+rotationCenter[1], rotated[2]+rotationCenter[2]]


def rotate_z(point, angle, rotationCenter):
    translated = [point[0]-rotationCenter[0], point[1]-rotationCenter[1], point[2]-rotationCenter[2]]
    rotated = [translated[0]*cos(angle)-translated[1]*sin(angle),
               translated[0]*sin(angle)+translated[1]*cos(angle),
               translated[2]]
    return [rotated[0]+rotationCenter[0], rotated[1]+rotationCenter[1], rotated[2]+rotationCenter[2]]


def rotateFingers(fingers, rotate, rot):
    rotationCenter = getRotationCenter(fingers)
    for finger in fingers:
        # mecaobject = finger.tetras
        # mecaobject.getData('rest_position').value = getRotated(rotate, mecaobject.getData('rest_position').value, rot,
        #                                                        rotationCenter)
        m = finger.getChild("ElasticMaterialObject")
        mecaobject = m.getObject("dofs")
        # mecaobject.findData('rest_position').value = getTranslated(mecaobject.rest_position.value, direction)

        mecaobject.getData('rest_position').value = getRotated(rotate, mecaobject.getData('rest_position').value, rot,
                                                               rotationCenter)
                
        cable = m.getChild("PullingCable").getObject("CableConstraint")
        p = cable.pullPoint
        cable.getData("pullPoint").value = rotate(p, rot, rotationCenter)

class GripperController(Sofa.Core.Controller):

    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
              
        self.logObj = args[0]
        self.fingers = args[1]  
        self.node = args[2]
        self.root = args[3]
        self.name = "GripperController"
        self.rotateAngle = 0 
        self.centerPosY = 0
        self.centerPosZ = 0


    # def __logger_gripper( self, ): # clean the code a little bit to log the values accordingly 

    
    def onKeypressedEvent(self, e):    
        direction = None
        rot = None
        rotate = None
        action = None 


        c = e["key"]
        if c == 'C':
            rot = 1/(2*pi)
            rotate = rotate_y
        elif c == 'A':
            rot = -1/(2*pi)
            rotate = rotate_y
        elif c == '5':
            rot = 1/(2*pi)
            rotate = rotate_x
        elif c == '6':
            rot = -1/(2*pi)
            rotate = rotate_x
        elif c == '7':
            rot = 1/(2*pi)
            rotate = rotate_z
        elif c == '8':
            rot = -1/(2*pi)
            rotate = rotate_z
        elif c == Key.uparrow:
            direction = [0.0, 1.0, 0.0]
        elif c == Key.downarrow:
            direction = [0.0, -1.0, 0.0]
        elif c == Key.leftarrow:
            direction = [1.0, 0.0, 0.0]
        elif c == Key.rightarrow:
            direction = [-1.0, 0.0, 0.0]


        f_data, cube_data, action, time = get_logging_data( self.node, self.root, direction, "rest" )        
        self.logObj.create( f_data, cube_data, action, time)
        Sofa.Gui.GUIManager.SaveScreenshot(self.logObj.img_path + "/" + time + ".png")  

        if direction is not None and self.fingers is not None:
            for finger in self.fingers:
                m = finger.getChild("ElasticMaterialObject")
                mecaobject = m.getObject("dofs")
                mecaobject.findData('rest_position').value = getTranslated(mecaobject.rest_position.value, direction)
                
                cable = m.getChild("PullingCable").getObject("CableConstraint")
                p = cable.pullPoint.value
                
                cable.findData("pullPoint").value = [p[0] + direction[0], p[1] + direction[1], p[2] + direction[2]]                

            # log after the action is taken 

            f_data, cube_data, action, time = get_logging_data( self.node, self.root, direction, "translation" )        
            self.logObj.create( f_data, cube_data, action, time)
            Sofa.Gui.GUIManager.SaveScreenshot(self.logObj.img_path + "/" + time + ".png")  

        if rot is not None:
            rotateFingers(self.fingers, rotate, rot)


def createScene(rootNode):
    rootNode.addObject(GripperController(None))

    return
