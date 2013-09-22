#Export method calls and namespace
# from three_link_pendulum example ..

from three_link_pendulum import I, O, link1, link2, link3, kane
from simulate import params, states, param_vals
import json
from pydy_viz.shapes import Cylinder
from pydy_viz.scene import Scene
from pydy_viz.visualization_frame import VisualizationFrame
from pydy_viz.server import Server
# setting some shapes for the pendulums ..
shape1 = Cylinder('shape1', radius=1.0, length=10.0, color='red')
shape2 = Cylinder('shape2', radius=1.0, length=10.0, color='blue')
shape3 = Cylinder('shape3', radius=1.0, length=10.0, color='green')

# setting up some vframes ...
frame1 = VisualizationFrame('frame1', link1, shape1)
frame2 = VisualizationFrame('frame2', link2, shape2)
frame3 = VisualizationFrame('frame3', link3, shape3)

scene = Scene(I, O, frame1, frame2, frame3)
scene.visualization_frames = [frame1, frame2, frame3]

print('Generating transform time histories.')
data = scene.generate_visualization_dict(kane._q + kane._u, params, states, param_vals)
scene.generate_visualization_json(kane._q + kane._u, params, states, param_vals)
print('Done.')
#print data
scene.display()
