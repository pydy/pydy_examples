//THis file basically creates a Canvas class like object.
container.show();

function Canvas(JSONObj) 
{
    
    this.visualization_frames = JSONObj.frames;
    this.width = JSONObj.width;
    this.height = JSONObj.height;
    
    this.initialize = function (){
        // This function initializes a simple Canvas, with mouse controls
        
        // first of all , a renderer ...
	    this.renderer = new THREE.WebGLRenderer();
        
        //show the IPython handle container
        container.show();
    
        // create a canvas div
	    this.canvas = $("<div/>").attr("id", "#canvas");
        this.canvas.attr("style","background-color:rgb(104,104,104)");
        
        // Now lets add a scene ..
        
        this.scene = new THREE.Scene();
        
        // A Camera ..
        var VIEW_ANGLE = 45,
	    ASPECT = WIDTH / HEIGHT,
	    NEAR = 0.1,
	    FAR = 1000;
        
        this.camera = new THREE.PerspectiveCamera(  VIEW_ANGLE,
	                                ASPECT,
	                                NEAR,
	                                FAR  );
                                    
         // the camera starts at 0,0,0 so pull it back
	     this.camera.position.z = 10;
	                           
         // Add trackball controls ...                                  
    
         this.controls = new THREE.TrackballControls(camera, renderer.domElement);
         
         this.reset = function(){ controls.reset();}
         
         this.scene.add(this.camera);
         
         this.reset_button = $('<button/>').attr('style','margin-left:40px;').click(reset);
         this.reset_button.append('Reset Camera');                             
         this.canvas.append(this.reset_button)
	
	     this.canvas.append(this.renderer.domElement);
	     element.append(this.canvas);
         
         // start the renderer
         this.renderer.setSize(this.width, this.height);
         
         
         // Add Axis to this scene ...
         // Add  axes ...
	
	    var axesMaterial = new THREE.MeshLambertMaterial(
	    {
	        color: 0xFFFFFF
	    
	    });
       this.x_axis = new THREE.Mesh(
	                      new THREE.CubeGeometry(this.width, 0.03, 0.03),
	                         axesMaterial);
	   
	    this.scene.add(this.x_axis);
        
        var y_axis = new THREE.Mesh(
	                  new THREE.CubeGeometry(0.03, this.height, 0.03),
	                                 axesMaterial);
	   
	    this.scene.add(this.y_axis); 
        
        this.z_axis = new THREE.Mesh(
	                 new THREE.CubeGeometry(0.03, 0.03, 10),
	                      axesMaterial);
	   
	    this.scene.add(this.z_axis);
        
        // create a point light
	    this.pointLight = new THREE.PointLight( 0xFFFFFF );

	    // set its position
	   this.pointLight.position.x = 100;
	   this.pointLight.position.y = 100;
       this.pointLight.position.z = 100;

	    // add to the scene
	    this.scene.add(this.pointLight);
	
	    this.renderer.render(scene, camera);    
    }
    
}    
