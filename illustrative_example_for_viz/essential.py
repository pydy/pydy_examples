#This file contains all the essential methods for the
#illustrative example
#It only contains the basic implementations of pydy-viz
#also it doesnot check for TypeErrors etc.
from sympy.matrices.expressions import Identity
from sympy import lambdify, Dummy
from server import create_server
from numpy import hstack, ones, zeros


class Cylinder(object):

    def __init__(self, name, radius=1, height=1, color='grey'):
        self._name = name
        self._radius = radius
        self._height = height
        self._color = color

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def generate_data(self):
        self._data = {}
        self._data['type'] = 'Cylinder'
        self._data['name'] = self.name
        self._data['radius'] = self._radius
        self._data['height'] = self._height
        self._data['color'] = self.color
        return self._data


class VisualizationFrame(object):
    def __init__(self, name, rigidbody, shape=None):
        #It is only to be used for rigidbody here, as per the
        #specific requirements of the illustrative example
        self._name = name
        self._reference_frame = rigidbody.get_frame()
        self._origin = rigidbody.get_masscenter()
        self._shape = shape
        # I don't think the identity matrix is a correct default. The
        # transloation portion should be all zeros.
        self._transform = Identity(4).as_mutable()

    def transform(self, reference_frame, point):
        # TODO : make sure this actually works correctly
        _rotation_matrix = self._reference_frame.dcm(reference_frame)

        self._transform[0:3, 0:3] = _rotation_matrix[0:3, 0:3]

        _point_vector = self._origin.pos_from(point).express(reference_frame)

        self._transform[3, 0] = _point_vector.dot(reference_frame.x)
        self._transform[3, 1] = _point_vector.dot(reference_frame.y)
        self._transform[3, 2] = _point_vector.dot(reference_frame.z)

        return self._transform

    def generate_numeric_transform(self, dynamic, parameters):
        """Returns a function which returns a transformation matrix given
        the symbolic states and the symbolic system parameters."""

        dummy_symbols = [Dummy() for i in dynamic]
        dummy_dict = dict(zip(dynamic, dummy_symbols))
        transform = self._transform.subs(dummy_dict)

        self.numeric_transform = lambdify(dummy_symbols + parameters,
                                          transform, modules="numpy")

    def evaluate_numeric_transform(self, states, parameters):
        """Returns the numerical transformation matrices for each time step.

        Parameters
        ----------
        states : array_like, shape(m,) or shape(n, m)
            The m states for each n time step.
        parameters : array_like, shape(p,)
            The p constant parameters of the system.

        Returns
        -------
        transform_matrix : numpy.array, shape(n, 4, 4)
            A 4 x 4 transformation matrix for each time step.

        """

        if len(states.shape) > 1:
            n = states.shape[0]
            # first create a shape(n, m + p) matrix
            # states : n x m
            # parameters : p
            # ones : n x p
            #a = ones((n, len(parameters)))
            #b = a * parameters
            #c = hstack((states, b))
            #d = c.T
            #e = list(d)
            #args = list(hstack((states, ones((n, len(parameters))) *
                                #parameters)).T)

            # this is a slow way to do things. technically numeric_transform
            # should take states shape(n, m) or states shape(m,) and still
            # work, but there are some issues in lambdify and I'm not sure
            # what the deal is. I think we need to check lambdify for sympy
            # matrices but offer a numpy array output then we could evaulate
            # these much faster
            new = zeros((n, 4, 4))
            for i, time_instance in enumerate(states):
                args = hstack((time_instance, parameters))
                new[i, :, :] = self.numeric_transform(*args)

        else:
            args = hstack((states, parameters))
            new = self.numeric_transform(*args)

        self.simulation_matrix = new

    def generate_simulation_dict(self):
        self._data = {}
        self._data['name'] = self._name
        self._data['shape'] = {}
        self._data['shape'] = self._shape.generate_data()  # hidden method
        self._data['simulation_matrix'] = self.simulation_matrix.tolist()
        return self._data


class Scene():
    def __init__(self, name, reference_frame, origin, height=400, width=400):
        self._name = name
        self._reference_frame = reference_frame
        self._origin = origin  # contains point
        self._child_frames = []
        self._height = height
        self._width = width

    def add_visualization_frames(self, *vframes):
        for _vframe in vframes:
            self._child_frames.append(_vframe)

    def add_visualization_frame(self, vframe):
        self._child_frames.append(vframe)

    def generate_json(self, state_sym, par_sym, states, parameters):

        self._scene_data = {}
        self._scene_data['name'] = self._name
        self._scene_data['height'] = self._height
        self._scene_data['width'] = self._width
        self._scene_data['frames'] = []

        for frame in self._child_frames:

            frame.transform(self._reference_frame, self._origin)
            frame.generate_numeric_transform(state_sym, par_sym)
            frame.evaluate_numeric_transform(states, parameters)
            self._scene_data['frames'].append(frame.generate_simulation_dict())

        return self._scene_data

    def display(self):
        print("Your visualization is available at http://127.0.0.1/8000 \n \
               Visit it in your favourite browser to see your visualization \
               in all its glory. \n \
               Starting Server at 8000")
        create_server(port=8000)
