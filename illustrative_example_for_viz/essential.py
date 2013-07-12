#This file contains all the essential methods for the
#illustrative example
#It only contains the basic implementations of pydy-viz
#also it doesnot check for TypeErrors etc.
import numpy as np
from sympy.matrices.expressions import Identity

class MeshShape(object):
    def __init__(self, name, point_list, color='grey', origin=[0,0,0]):
        self._name = name
        self._points = point_list
        self._color = color 
        self._origin = origin
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, new_name):
        self._name = new_name
                        
    @property
    def points(self):
        return self._points
        
    @points.setter
    def points(self, new_point_list):
        self._points = new_point_list
    
    @property
    def color(self):
        return self._color
        
    @color.setter
    def color(self, new_color):
        self._color = new_color
                 
    @property
    def origin(self):
        return self._origin
        
    @color.setter
    def origin(self, new_origin):
        self._origin = new_origin
        
       
class VisualizationFrame(object):
    def __init__(self, name, rigidbody, shape=None):
        #It is only to be used for rigidbody here, as per the 
        #specific requirements of the illustrative example
        self._name = name
        self._reference_frame = rigidbody.get_frame()
        self._origin = rigidbody.get_masscenter()
        self._shape = shape
        self._transform = Identity(4).as_mutable()
        
    def transform(self, reference_frame, point):
        _rotation_matrix = self._reference_frame.dcm(reference_frame)
        
        self._transform[0:3,0:3] = _rotation_matrix[0:3,0:3]
        
        _point_vector = self._origin.pos_from(point).express(reference_frame)
        
        self._transform[0,3] = _point_vector.dot(reference_frame.x)
        self._transform[1,3] = _point_vector.dot(reference_frame.y)
        self._transform[2,3] = _point_vector.dot(reference_frame.z)
        
        return self._transform
        
    def eval_transform(self):
        self._numerical_transform = self._transform.evalf(subs=vel_dict)
        return self._numerical_transform

    def generate_simulation_data(self,values_list,timesteps=None):
        self.simulation_matrix = []
        for iterator in range(0,timesteps):
            self.simulation_matrix.append(self._transform.evalf(subs=values_list[iterator]))
        return self.simulation_matrix
        
class Scene():
    def __init__(self,name,reference_frame,origin,height=800,width=800):
        self._name = name
        self._reference_frame=reference_frame        
        self._origin = origin  #contains point
        self._child_vframes = []
        self._height = height 
        self._width = width 
    
    
    def add_visualization_frames(self,vframes):
        for _vframe in vframes:
            self._child_vframes.append(_vframe)    
    
    def add_visualization_frame(self,vframe):
        self._child_vframes.append(vframe)
    
    
    def generate_json(self):
        
        #TODO
        pass    
    
