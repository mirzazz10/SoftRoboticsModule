# -*- coding: utf-8 -*-
import Sofa.Core
import Sofa.constants.Key as Key
from stlib3.physics.deformable import ElasticMaterialObject
from stlib3.physics.constraints import FixedBox
from softrobots.actuators import PullingCable
from stlib3.physics.collision import CollisionMesh
from splib3.loaders import loadPointListFromFile
import Sofa
import Sofa.Gui


def get_logging_data( node, root, direction = None, action_type = "grasp"):
    time = str( root.time.value)
    time = time.split(".")
    time = "_".join(time)[:10]
    if len(time) < 10:
        temp_string = "0"*(10 - len(time))
        time += temp_string
    finger_data = {}
    cable_data = {}
    action_data = {}        
    for i in range( 1,4):
        examplefinger = node.getChild( "Finger" + str(i))                
        key = time + str(i)
        m = examplefinger.getChild("ElasticMaterialObject")                    
        mecaobject = m.getObject("dofs")
        # print( dir( mecaobject))
        pos = mecaobject.position.value
        vel = mecaobject.velocity.value
        # print( pos.shape, vel.shape, type( pos), type( pos))
        pos = mecaobject.position.value.tolist()
        vel = mecaobject.velocity.value.tolist()
        # print( type(pos), type( vel))        
        finger_data[key] = [pos, vel]
        # print( pos, f"This position for finger {i}")
        # print( vel, f"This position for finger {i}")
        # force/ action taken   
        cable = m.getChild( "PullingCable")  
        # print( dir( cable))
        # mech_cable =  cable.getObject( "MechanicalObject")        
        displacement_action = cable.CableConstraint.value[0] # displacement or force applied at the pull point location    
        print( displacement_action, type( displacement_action))
        cable_pos = cable.CableConstraint.pullPoint.value.tolist()        
        cable_data[key] = [displacement_action, cable_pos]
        action_data[ action_type + str(i)] = [ displacement_action, direction, cable_pos]  # total action for each cable
    
    # cube data
    # Assuming rootNode is the main node in your simulation 
    cs = 3

    # cube_pos_data = root.Cube.getObject( "MechanicalObject").getData("position")
    # print(type(cube_pos_data), cube_pos_data.value)
    cube_pos = [round(float(k), cs) for k in root.Cube.mstate.position.value.reshape(-1)]  # orginal value method 

    # cube_pos = [round(float(k), cs) for k in cube_pos_data.value.reshape(-1)]

    # timeStep     
   
    # print( time)

    # saving the image for the timestep ##


    

    # can include the goal pos, and the distance of the object from the goal position 
     

    # 
    
    return finger_data, cube_pos, action_data, time


class FingerController(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.cable = args[0]
        self.node = args[1]        
        self.logObj = args[2]
        self.parentNode = args[3]
        self.name = "FingerController"

    def onKeypressedEvent(self, e):      
        # log before the action is taken 

        f_data, cube_data, action, time = get_logging_data(self.node, self.parentNode, None, "rest")        
        self.logObj.create( f_data, cube_data, action, time)
        Sofa.Gui.GUIManager.SaveScreenshot(self.logObj.img_path + "/" + time + ".png")    
                
        # print( exampleFinger1.getMechanicalState().rest_position.value, "These are our dofs for the example finger 1 " )
        displacement = self.cable.CableConstraint.value[0]
        if e["key"] == Key.plus:
            displacement += 1.

        elif e["key"] == Key.minus:
            displacement -= 1.
            if displacement < 0:
                displacement = 0
        #print( "displacement values", displacement) 
        self.cable.CableConstraint.value = [displacement]

        # log after the action is taken
        f_data, cube_data, action, time = get_logging_data(self.node, self.parentNode, None, "grasp")  
        self.logObj.create( f_data, cube_data, action, time )
        Sofa.Gui.GUIManager.SaveScreenshot(self.logObj.img_path + "/" + time + ".png")  

def Finger(logObj, rootNode, parentNode=None, name="Finger", 
           rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0],
           fixingBox=[-5.0, 0.0, 0.0, 10.0, 15.0, 20.0], pullPointLocation=[0.0, 0.0, 0.0]):
    finger = parentNode.addChild(name)
    eobject = ElasticMaterialObject(finger,
                                    volumeMeshFileName="data/mesh/finger.vtk",
                                    poissonRatio=0.3,
                                    youngModulus=18000,
                                    totalMass=0.5,
                                    surfaceColor=[0.0, 0.8, 0.7, 1.0],
                                    surfaceMeshFileName="data/mesh/finger.stl",
                                    rotation=rotation,
                                    translation=translation)
    finger.addChild(eobject)    
    FixedBox(eobject, atPositions=fixingBox, doVisualization=True)    

    cable = PullingCable(eobject,
                         "PullingCable",
                         pullPointLocation=pullPointLocation,
                         rotation=rotation,
                         translation=translation,
                         cableGeometry=loadPointListFromFile("data/mesh/cable.json"), valueType = "displacement")

    eobject.addObject(FingerController(cable, parentNode, logObj, rootNode))

    CollisionMesh(eobject, name="CollisionMesh",
                  surfaceMeshFileName="data/mesh/finger.stl",
                  rotation=rotation, translation=translation,
                  collisionGroup=[1, 2])

    CollisionMesh(eobject, name="CollisionMeshAuto1",
                  surfaceMeshFileName="data/mesh/fingerCollision_part1.stl",
                  rotation=rotation, translation=translation,
                  collisionGroup=[1])

    CollisionMesh(eobject, name="CollisionMeshAuto2",
                  surfaceMeshFileName="data/mesh/fingerCollision_part2.stl",
                  rotation=rotation, translation=translation,
                  collisionGroup=[2])

    return finger, translation


def createScene(rootNode):
    from stlib3.scene import MainHeader, ContactHeader

    MainHeader(rootNode, gravity=[0.0, -981.0, 0.0], plugins=["SoftRobots"])
    ContactHeader(rootNode, alarmDistance=4, contactDistance=3, frictionCoef=0.08)
    rootNode.VisualStyle.displayFlags = "showBehavior showCollisionModels"

    Finger(rootNode, translation=[1.0, 0.0, 0.0])
    return rootNode

# # required = dir( self.cable)
        # # obj = self.cable        
        # # Filter and print only attributes (no methods)
        # # attributes = dir(obj) 

        # # for attr in attributes:
        # #     value = getattr(obj, attr)
        # #     print(attr)
        # #     try:
        # #         print(f"{attr}: {value.value}")
        # #     except AttributeError:
        # # #         print(f"{attr}: (no value attribute)")
        # # exampleGripper =  self.node.getChild( "Gripper")
        # # exampleFinger = exampleGripper.Finger1
        # # baseObject = exampleFinger.ElasticMaterialObject
        # # print( baseObject)
        # # use this information to keep a logger file and then do a demonstration of grasping, 
        # # include the cube things also in this. 
        # # Take as much information as possible
        # # make sure every detail is put into a dictionary and then give as demo on thursday 
        # # try to include rotation of the gripper also 
        
        # examplefinger = self.node.getChild( "Finger1")
        # exampleCube = self.node.getChild( "Cube")
        # exampleCable = self.cable
        # print( vars( exampleCube))

        # # print( dir( examplefinger))

        # # attr = dir( examplefinger)



        # # m = examplefinger.getChild("ElasticMaterialObject")
        # # # print( vars( m))
        # # mechState = m.getMechanicalState()
        # # # print( mechState)
        # # mecaobject = m.getObject("dofs")
        # # # print( "This is our position", mecaobject.position.value)
        # # cable = m.getChild("PullingCable").getObject("CableConstraint")
        # # p = cable.pullPoint.value

        # # print(p)

