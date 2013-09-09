#Export method calls and namespace
# from three_link_pendulum example ..

from three_link_pendulum import I, O, links, particles, kane
from simulate import params, states, param_vals,
from simulate import link_length, link_radius, particle_radius
from pydy_viz.shapes import Cylinder, Sphere
from pydy_viz.scene import Scene
from pydy_viz.visualization_frame import VisualizationFrame

viz_frames = []

for i, (link, particle) in enumerate(zip(links, particles)):

    link_shape = Cylinder('cylinder{}'.format(i), radius=link_radius,
                          length=link_length, color='red')
    viz_frames.append(VisualizationFrame('link_frame{}'.format(i), link,
                                         link_shape))

    particle_shape = Sphere('sphere{}'.format(i), radius=particle_radius,
                            color='blue')
    viz_frames.append(VisualizationFrame('particle_frame{}'.format(i),
                                         link.frame, particle,
                                         particle_shape))

scene = Scene(I, O, *viz_frames)
#scene.visualization_frames = viz_frames

print('Generating transform time histories.')
data = scene.generate_visualization_dict(kane._q + kane._u, params, states,
                                         param_vals)
scene.generate_visualization_json(kane._q + kane._u, params, states,
                                  param_vals)
print('Done.')
scene.display()
