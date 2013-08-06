
function Canvas(JSONObj) 
{
    
    this.visualization_frames = JSONObj.frames;
    this.width = JSONObj.width;
    this.height = JSONObj.height;
    var parent = this; // This is because of some tricky behaviour of Javascript "this" keyword
    parent.init_canvas = new THREE.Object3D(); // This consists of axes and other init stuff
    parent.animation_counter = 0; // for counting and iterating
    parent.mesh_dict = {}; // for holding meshes as frame as dictionary key 
    parent.i = 0;
    parent.initialize = function ()
        {
            
        // parent function initializes a simple Canvas, with mouse controls
        
        // first of all , a renderer ...
	    parent.renderer = new THREE.WebGLRenderer();
        
        
        
    
        // create a canvas div
	    parent.canvas = $("#canvas");
        
        parent.canvas.attr("style","background-color:rgb(104,104,104); height:"+this.height + ";width:"+this.width);


        
        // Now lets add a scene ..
        
        parent.scene = new THREE.Scene();
        
        // A Camera ..
        var VIEW_ANGLE = 45,
	    ASPECT = parent.width/parent.height,
	    NEAR = 0.1,
	    FAR = 1000;
        
        parent.camera = new THREE.PerspectiveCamera(  VIEW_ANGLE,
	                                ASPECT,
	                                NEAR,
	                                FAR  );
                                    
         // the camera starts at 0,0,0 so pull it back
	     parent.camera.position.z = 100;
	                           
         // Add trackball controls ...                                  
    
         parent.controls = new THREE.TrackballControls(parent.camera, parent.renderer.domElement);
         
         
         parent.reset = function(){ parent.controls.reset();}
         
         parent.scene.add(parent.camera);
         
         parent.reset_button = $('<button/>').attr('style','margin-left:40px;').click(parent.reset);
         parent.reset_button.append('Reset Camera');                             
         parent.canvas.append(parent.reset_button)
	
	     parent.canvas.append(parent.renderer.domElement);
	     $('#my-canvas').append(parent.canvas);
         //alert($('#my-canvas').html());
         
         // start the renderer
         parent.renderer.setSize(parent.width, parent.height);
         
         
         // Add Axis to parent scene ...
         // Add  axes ...
	
        var axesMaterial = new THREE.MeshLambertMaterial(
	     {
	        color: 0xFFFFFF
	    
	     });
        parent.x_axis = new THREE.Mesh(
	                      new THREE.CubeGeometry(parent.width, 0.1, 0.1),
	                         axesMaterial);
	   
	    parent.init_canvas.add(parent.x_axis);
        
        parent.y_axis = new THREE.Mesh(
	                  new THREE.CubeGeometry(0.1, parent.height, 0.1),
	                                 axesMaterial);
	   
	    parent.init_canvas.add(parent.y_axis);
        
        parent.z_axis = new THREE.Mesh(
	                 new THREE.CubeGeometry(0.1, 0.1, 10),
	                      axesMaterial);
	   
	    parent.init_canvas.add(parent.z_axis);
        
        // create a point light
	    parent.pointLight = new THREE.PointLight( 0xFFFFFF );

	    // set its position
	    parent.pointLight.position.x = 10;
	    parent.pointLight.position.y = 10;
        parent.pointLight.position.z = 10;

	    // add to the scene
	    parent.init_canvas.add(parent.pointLight);
	
        parent.scene.add(parent.init_canvas);
	    parent.renderer.render(parent.scene, parent.camera);    
        
        
        
    };
    
    parent.visualize = function()
    {
        
        parent.controls.update();
        
        parent.renderer.render(parent.scene, parent.camera);
        requestAnimationFrame(parent.visualize);
    };    
     
    parent.add_visualization_frames = function()
    
    {   parent.frames = {};
        for(var frame in JSONObj.frames)
        {
            parent.add_shape(JSONObj.frames[frame])
            
        }     
    }    
    
    
    parent.add_shape = function(frame)
     {   
         
         var material = new THREE.MeshLambertMaterial({
            color:              frame.shape.color,
            wireframe:          true,
            wireframeLinewidth: 0.1,
            opacity: 0.5
           })
           
         var geometry = new THREE.CylinderGeometry(frame.shape.radius,frame.shape.radius,frame.shape.height,50,50);
         parent.mesh_dict[frame.name] = new THREE.Mesh(geometry,material);
         var init_orientation = frame.simulation_matrix[0];
         var orienter = new THREE.Matrix4();
         orienter.elements = [];
         for(var i in init_orientation)
             {
               for(var j in init_orientation[i]) 
               { 
                  orienter.elements.push(init_orientation[i][j]) ;
                }
              }  
         parent.mesh_dict[frame.name].applyMatrix(new THREE.Matrix4());
         parent.mesh_dict[frame.name].applyMatrix(orienter);
         parent.mesh_dict[frame.name].autoUpdateMatrix = false;
         parent.scene.add(parent.mesh_dict[frame.name]);
         parent.renderer.render(parent.scene,parent.camera); 
     }    
                        
     parent.run_animation = function()
     {
              
              
              //Please work
              parent.animate(JSONObj.frames[0], parent.i);
              parent.animate(JSONObj.frames[1], parent.i);
              parent.animate(JSONObj.frames[2], parent.i);
              
              parent.i++;
              if(parent.i >= 1000) { parent.i = 0; }    
              console.log(parent.i);
              requestAnimationFrame(parent.run_animation); 
          
              
             
      }
      
      
      parent.animate = function(frame, counter)
      {
          var matrix = frame.simulation_matrix[counter]; 
          var orienter = new THREE.Matrix4();
          orienter.elements = [];
          for(var i in matrix)
                  {
                    for(var j in matrix[i]) 
                    { 
                       orienter.elements.push(matrix[i][j]) ;
                     }
                  }  
              
          // Removing the chaos, bringing heirarchy ..    
          parent.mesh_dict[frame.name].matrix.identity();
          parent.mesh_dict[frame.name].applyMatrix(orienter);   
          
       }    
       
      
            
       
     
}
