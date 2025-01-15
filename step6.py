# -*- coding: utf-8 -*-
from stlib3.scene import MainHeader, ContactHeader
from stlib3.physics.rigid import Floor, Cube, Sphere
from gripper import Gripper
from logger import Logger
import Sofa
import SofaRuntime
from path_config import image_file_path, json_file_path


# creating logger object only once to log all the data
print(image_file_path, json_file_path)
logObj = Logger(image_file_path, json_file_path)

def add_goal_node(root):
    goal = root.addChild("Goal")
    goal.addObject('VisualStyle', displayFlags="showCollisionModels")
    goal_mo = goal.addObject('MechanicalObject', name='GoalMO', showObject=True, drawMode="1", showObjectScale=3,
                             showColor=[0, 1, 0, 1], position=[0.0, 0.0, 0.0])
    return goal_mo

def createScene(rootNode):
    """This is my first scene"""
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.AnimationLoop') # Needed to use components [FreeMotionAnimationLoop]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Detection.Algorithm') # Needed to use components [BVHNarrowPhase,BruteForceBroadPhase,CollisionPipeline]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Detection.Intersection') # Needed to use components [LocalMinDistance]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Geometry') # Needed to use components [LineCollisionModel,PointCollisionModel,TriangleCollisionModel]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Response.Contact') # Needed to use components [RuleBasedContactManager]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Lagrangian.Correction') # Needed to use components [LinearSolverConstraintCorrection,UncoupledConstraintCorrection]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Lagrangian.Solver') # Needed to use components [GenericConstraintSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Engine.Select') # Needed to use components [BoxROI]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.LinearSolver.Direct') # Needed to use components [SparseLDLSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.LinearSolver.Iterative') # Needed to use components [CGLinearSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mapping.Linear') # Needed to use components [BarycentricMapping]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mapping.NonLinear') # Needed to use components [RigidMapping]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mass') # Needed to use components [UniformMass]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.ODESolver.Backward') # Needed to use components [EulerImplicitSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.FEM.Elastic') # Needed to use components [TetrahedronFEMForceField]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.Spring') # Needed to use components [RestShapeSpringsForceField]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.StateContainer') # Needed to use components [MechanicalObject]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Constant') # Needed to use components [MeshTopology]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Dynamic') # Needed to use components [TetrahedronSetTopologyContainer]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Visual') # Needed to use components [VisualStyle]  
    rootNode.createObject("DefaultContactManager", name="ContactManager", response="FrictionContactConstraint", responseParams="mu=0.8")

    MainHeader(rootNode, gravity=[0.0, -981.0, 0.0], plugins=["SoftRobots"])
    ContactHeader(rootNode, alarmDistance=4, contactDistance=3, frictionCoef=0.08)
    rootNode.VisualStyle.displayFlags = "showBehavior showCollisionModels"


    goal_mo = add_goal_node( rootNode)
    floor = Floor(rootNode,
          color=[1.0, 0.0, 0.0, 1.0],
          translation=[0.0, -160.0, 0.0],
          isAStaticObject=True)
    
    
    # adding different types of objects 
    cube = Cube(rootNode, name = "Cube",
                 uniformScale=20.0,
                 color=[1.0, 1.0, 0.0, 1.0],
                 totalMass=0.03,
                 volume=20,
                 inertiaMatrix=[1000.0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 1000.0],
                 translation=[0.0, -130.0, 10.0])
# #                translation=[0.0, -130.0, 10.0]) # use this to change the position of the object 
    cube.addObject('UncoupledConstraintCorrection')  

#     cube = Sphere(rootNode, name = "Cube",
#             uniformScale= 17.5,
#             color=[1.0, 1.0, 0.0, 1.0],
#             totalMass=0.03,
#             volume=20,
#             inertiaMatrix=[1000.0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 1000.0],
#             translation=[0.0, -130.0, 10.0])
# #                translation=[0.0, -130.0, 10.0]) # use this to change the position of the object 
#     cube.addObject('UncoupledConstraintCorrection')  



#    obj_file_path = "/home/rahman/Documents/bookObj/book.obj"


#    totalMass = 0.03
#    volume = 20.0
#    inertiaMatrix=[1000., 0., 0., 0., 1000., 0., 0., 0., 1000.]


 #   cube = rootNode.addChild("Cube")
 #   cube.addObject('EulerImplicitSolver', name='odesolver')
 #   cube.addObject('CGLinearSolver', name='Solver', iterations=25, tolerance=1e-05, threshold=1e-05)
 #   cube.addObject('MechanicalObject', name="mstate", template="Rigid3", translation2=[0.0, -130.0, 10.0], rotation2=[0., 0., 0.], showObjectScale=25)
 #   cube.addObject('UniformMass', name="mass", vertexMass=[totalMass, volume, inertiaMatrix[:]])
 #   cube.addObject('UncoupledConstraintCorrection')

    #### Collision subnode for the sphere
  #  collision = cube.addChild('collision')
  #  collision.addObject('MeshOBJLoader', name="loader", filename=obj_file_path, triangulate="true", scale=1.0)
  #  collision.addObject('MeshTopology', src="@loader")
  #  collision.addObject('MechanicalObject')
  #  collision.addObject('TriangleCollisionModel')
  #  collision.addObject('LineCollisionModel')
  #  collision.addObject('PointCollisionModel')
  #  collision.addObject('RigidMapping')

    #### Visualization subnode for the sphere
#    sphereVisu = cube.addChild("VisualModel")
 #   sphereVisu.loader = sphereVisu.addObject('MeshOBJLoader', name="loader", filename=obj_file_path)
    # sphereVisu.addObject('OglModel', name="model", src="@loader", scale3d=[10]*3, color=[1.0, 1.0, 0.0, 1.0], updateNormals=False)
  #  sphereVisu.addObject('OglModel', name="model", src="@loader", color=[1.0, 1.0, 0.0, 1.0], updateNormals=False)
   # sphereVisu.addObject('RigidMapping')


    # rest of the code 
    Gripper(logObj, rootNode)
    ###### Camer logic integrate later ######
    SofaRuntime.importPlugin('SofaOpenglVisual')
    SofaRuntime.importPlugin("SofaComponentAll")
    rootNode.addObject('RequiredPlugin', name='Sofa.GL.Component.Shader')
    
    rootNode.addObject("LightManager")
    rootNode.addObject("SpotLight", position=[0,10,0], direction=[0,-1,0])
    rootNode.addObject("InteractiveCamera", name="camera", position=[0,10, 0],
                        lookAt=[0,0,0], distance=37,
                        fieldOfView=45, zNear=0.63, zFar=55.69)

    # start the simulator
    # Sofa.Simulation.init(root)
    # start the gui
    # Sofa.Gui.GUIManager.Init("Recorded_Episode", "qt")
    # Sofa.Gui.GUIManager.createGUI(self.root, __file__)
    return rootNode


print("File closed ---->")