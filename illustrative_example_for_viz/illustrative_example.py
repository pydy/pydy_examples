#Export method calls and namespace
# from three_link_pendulum example ..

from three_link_pendulum import *
from essential import *

#setting some shapes for the pendulums ..

shape1 = MeshShape('shape1',[[1,1,1], [0,1,1], [2,1,1]], \
                                color='red',origin=[0,0,0])

shape2 = MeshShape('shape2',[[1,1,1], [0,1,1], [2,1,1]], \
                                color='blue',origin=[0,0,0])
                                
shape3 = MeshShape('shape3',[[1,1,1], [0,1,1], [2,1,1]], \
                                color='green',origin=[0,0,0])

#Setting up some vframes ...
                                
frame1 = VisualizationFrame('frame1', link1, shape=shape1)
print frame1.homogeneous_transformation(I)                                

frame2 = VisualizationFrame('frame2', link2, shape=shape2)
frame3 = VisualizationFrame('frame3', link3, shape=shape3)

scene = Scene('scene1',I,O)
scene.vframes = [frame1,frame2,frame3]
print scene.vframes
scene.generate_json()


