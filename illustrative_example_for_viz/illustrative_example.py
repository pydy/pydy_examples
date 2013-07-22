#Export method calls and namespace
# from three_link_pendulum example ..

from three_link_pendulum import I, O, link1, link2, link3, kane
from essential import Cylinder, VisualizationFrame, Scene
from simulate import params, states, param_vals
from server import create_server
import json

# setting some shapes for the pendulums ..
shape1 = Cylinder('shape1', radius=1.0, height=10.0, color='red')
shape2 = Cylinder('shape2', radius=1.0, height=10.0, color='blue')
shape3 = Cylinder('shape3', radius=1.0, height=10.0, color='green')

# setting up some vframes ...
frame1 = VisualizationFrame('frame1', link1, shape=shape1)
frame2 = VisualizationFrame('frame2', link2, shape=shape2)
frame3 = VisualizationFrame('frame3', link3, shape=shape3)

scene = Scene('scene1', I, O, height=800, width=800)
scene.add_visualization_frames(frame1, frame2, frame3)

print('Generating transform time histories.')
data = scene.generate_json(kane._q + kane._u, params, states, param_vals)
print('Done.')
f = open('js/output.json', 'w')

print data
print json.dumps(data, indent=4, separators=(',', ': '))

f.write('var JSONObj=' + json.dumps(data, indent=4, separators=(',', ': ')))

f.close()

create_server()
