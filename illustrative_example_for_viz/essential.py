#This file contains all the essential methods for the
#illustrative example
#It only contains the basic implementations of pydy-viz
#also it doesnot check for TypeErrors etc.
import numpy as np
from sympy.matrices.expressions import Identity
from sympy import lambdify

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
    
    def generate_data(self):
        self._data = {}
        self._data['type'] = 'Mesh'
        self._data['name'] = self.name
        self._data['points'] = self.points
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
        self._transform = Identity(4).as_mutable()
        
    def transform(self, reference_frame, point):
        _rotation_matrix = self._reference_frame.dcm(reference_frame)
        
        self._transform[0:3,0:3] = _rotation_matrix[0:3,0:3]
        
        _point_vector = self._origin.pos_from(point).express(reference_frame)
        
        self._transform[0,3] = _point_vector.dot(reference_frame.x)
        self._transform[1,3] = _point_vector.dot(reference_frame.y)
        self._transform[2,3] = _point_vector.dot(reference_frame.z)
        
        return self._transform
        
    def generate_simulation_data(self,values_list):
        self.simulation_matrix = []
        for vals in values_list:
            evaluated = self._transform.evalf(subs=vals).tolist()
            temp_list = []
            for vals in evaluated:
                temp_list1 = []
                for val1 in vals:
                    temp_list1.append(float(val1))
                temp_list.append(temp_list1)    
                
            print 'evaluated = %s \n'%evaluated
            
            self.simulation_matrix.append(temp_list)
        
            
        return self.simulation_matrix
     
    def generate_simulation_dict(self):
        self._data = {}
        self._data['name'] = self._name
        
        self._data['shape'] = {}
        
        self._data['shape'] = self._shape.generate_data() #hidden method
        self._data['simulation_matrix'] = self.simulation_matrix
        return self._data
        
class Scene():
    def __init__(self,name,reference_frame,origin,height=800,width=800):
        self._name = name
        self._reference_frame=reference_frame        
        self._origin = origin  #contains point
        self._child_frames = []
        self._height = height 
        self._width = width 
    
    
    def add_visualization_frames(self,vframes):
        for _vframe in vframes:
            self._child_frames.append(_vframe)    
    
    def add_visualization_frame(self,vframe):
        self._child_frames.append(vframe)
    
    
    def generate_json(self,values_list):
        
        self._scene_data = {}
        self._scene_data['name'] = self._name
        self._scene_data['height'] = self._height
        self._scene_data['width'] = self._width
        self._scene_data['frames'] = {}
        
        for frame in self._child_frames[0]:
            
            frame.transform(self._reference_frame,self._origin)
            frame.generate_simulation_data(values_list)
            self._scene_data['frames'][frame._name] = frame.generate_simulation_dict()
            
        return self._scene_data    
            
            
                
       
    
