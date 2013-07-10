#This file contains all the essential methods for the
#illustrative example
#It only contains the basic implementations of pydy-viz
#also it doesnot check for TypeErrors etc.
import numpy as np

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
        self._transform = np.eye(4)
        
    def transform(self,rframe):
        rotation_matrix = self._reference_frame.dcm(rframe)
        self._transform[0:3,0:3] = rotation_matrix
        return self._transform

    def add_simulation_data(self,file_name=None):
        #TODO
        pass
    
    def generate_json():
        #TODO
        pass
        
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
    
