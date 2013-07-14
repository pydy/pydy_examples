
//First we have to parse the JSON object we get
var frames = JSONObj.frames



var controls,scene,camera,renderer,reset; 
var $reset_button;
var $canvas;
var sphere_geometry;

init_canvas();
visualize();

function init_canvas(){
	
	//This function initiates a basic canvas, with trackball controls, 
	//all drawing work occurs in init() function.
	
	// first of all , a renderer ...
	renderer = new THREE.WebGLRenderer();
	
	//show the IPython handle container
	container.show();
	
	// create a canvas div
	$canvas = $("<div/>").attr("id", "#canvas");
	//giving background color
	
	$canvas.attr("style","background-color:rgb(104,104,104)");
	
	// Adding our canvas to IPython UI
	
	
	// Now lets add a scene ..
	
	// set the scene size
	 var WIDTH = JSONObj.width,
	    HEIGHT = JSONObj.height;
	    
	scene = new THREE.Scene();
	
	
	//Add a camera to the scene..
	
	// set some camera attributes
	var VIEW_ANGLE = 45,
	    ASPECT = WIDTH / HEIGHT,
	    NEAR = 0.1,
	    FAR = 1000;
	    
	camera = new THREE.PerspectiveCamera(  VIEW_ANGLE,
	                                ASPECT,
	                                NEAR,
	                                FAR  );
	    
	        
	// the camera starts at 0,0,0 so pull it back
	camera.position.z = 10;
	
	
	// Add trackball controls
	
	controls = new THREE.TrackballControls(camera, renderer.domElement);
	
	
	reset = function(){ controls.reset();}
	
	
	scene.add(camera);
	
	

    $reset_button = $('<button/>').attr('style','margin-left:40px;').click(reset);
    $reset_button.append('Reset Camera');                             
    $canvas.append($reset_button)
	
	$canvas.append(renderer.domElement);
	element.append($canvas);
	// start the renderer
	renderer.setSize(WIDTH, HEIGHT);
	
	
	// Add  axes ...
	
	var axesMaterial = new THREE.MeshLambertMaterial(
	{
	    color: 0xFFFFFF
	    
	});
	var x_axis = new THREE.Mesh(
	   new THREE.CubeGeometry(WIDTH, 0.03, 0.03),
	   axesMaterial);
	   
	scene.add(x_axis);
	
	var y_axis = new THREE.Mesh(
	   new THREE.CubeGeometry(0.03, HEIGHT, 0.03),
	   axesMaterial);
	   
	scene.add(y_axis);
	
	var z_axis = new THREE.Mesh(
	   new THREE.CubeGeometry(0.03, 0.03, 10),
	   axesMaterial);
	   
	scene.add(z_axis);
	
	// create a point light
	var pointLight = new THREE.PointLight( 0xFFFFFF );

	// set its position
	pointLight.position.x = 100;
	pointLight.position.y = 100;
	pointLight.position.z = 100;

	// add to the scene
	scene.add(pointLight);
	
	renderer.render(scene, camera);    
	
	
}
// This function provides mouse controls to the system

function visualize() {
	
	
	controls.update();
	
	
    
    renderer.render(scene, camera);
	
	requestAnimationFrame(visualize);    
	
   
}



