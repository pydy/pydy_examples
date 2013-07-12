#Export method calls and namespace
# from three_link_pendulum example ..

from essential import *
from simulate import *
#setting some shapes for the pendulums ..

shape1 = MeshShape('shape1',[[1,1,1], [0,1,1], [2,1,1]], \
                                color='red',origin=[0,0,0])

shape2 = MeshShape('shape2',[[1,1,1], [0,1,1], [2,1,1]], \
                                color='blue',origin=[0,0,0])
                                
shape3 = MeshShape('shape3',[[1,1,1], [0,1,1], [2,1,1]], \
                                color='green',origin=[0,0,0])

#Setting up some vframes ...
                                
frame1 = VisualizationFrame('frame1', link1, shape=shape1)

#Now these methods would be called from within Scene for generating 
#simulation data, similar for all frames
frame1.transform(I,O)
simulation_matrix1 = frame1.generate_simulation_data(values_list,timesteps=100)
print simulation_matrix1


frame2 = VisualizationFrame('frame2', link2, shape=shape2)

frame3 = VisualizationFrame('frame3', link3, shape=shape3)

scene = Scene('scene1',I,O)
scene.add_visualization_frame([frame1,frame2,frame3])
scene.generate_json()


