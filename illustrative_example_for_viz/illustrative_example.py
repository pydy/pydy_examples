#This program represents a hypothetical situation for a complete workflow
#for simulating a three link pendulum with links as rigid bodies
from sympy import symbols,sympify
from sympy.physics.mechanics import *

#Number of links = 3
N_links = 3

#Number of masses = 3
N_bobs = 3

#Defining Dynamic Symbols ................

#Generalized coordinates(angular) ...

alpha = dynamicsymbols('alpha1 alpha2 alpha3')
beta = dynamicsymbols('beta1 beta2 beta3')    

#Generalized speeds(angular) ...
alphad = dynamicsymbols('alpha1 alpha2 alpha3',1)
betad = dynamicsymbols('beta1 beta2 beta3',1)

#Mass of each bob:
m = symbols('m:'+str(N_bobs))


#Length mass and radii of each link(assuming as rods) ..
l = symbols('l:' + str(N_links)) 
M = symbols('M:' + str(N_links)) 
radii = symbols('radii:' + str(N_links)) 

#For storing Inertia for each link :
Ixx = symbols('Ixx:'+str(N_links))
Iyy = symbols('Iyy:'+str(N_links))

#gravity and time ....
g, t = symbols('g t')


#Now defining an Inertial ReferenceFrame First ....

I = ReferenceFrame('I')

#And some other frames ...

A = ReferenceFrame('A')
A.orient(I,'Body',[alpha[0],beta[0],0],'ZXY')
B = ReferenceFrame('B')
B.orient(I,'Body',[alpha[1],beta[1],0],'ZXY')
C = ReferenceFrame('C')
C.orient(I,'Body',[alpha[2],beta[2],0],'ZXY')


#Setting angular velocities of new frames ...
A.set_ang_vel(I, alphad[0] * I.z + betad[0] * I.x)
B.set_ang_vel(I, alphad[1] * I.z + betad[1] * I.x)
C.set_ang_vel(I, alphad[2] * I.z + betad[2] * I.x)



# An Origin point, with velocity = 0
O = Point('O')
O.set_vel(I,0)

#Three more points, for masses ..
P1 = O.locatenew('P1', l[0] * A.y)
P2 = O.locatenew('P2', l[1] * B.y)
P3 = O.locatenew('P3', l[2] * C.y)

#Setting velocities of points with v2pt theory ...
P1.v2pt_theory(O, I, A)
P2.v2pt_theory(P1, I, B)
P3.v2pt_theory(P2, I, C)
points = [P1,P2,P3]

Pa1 = Particle('Pa1', points[0], m[0])
Pa2 = Particle('Pa2', points[1], m[1])
Pa3 = Particle('Pa3', points[2], m[2])
particles = [Pa1,Pa2,Pa3]



#defining points for links(RigidBodies)
#Assuming CoM as l/2 ...
P_link1 = O.locatenew('P_link1', l[0]/2 * A.y)
P_link2 = O.locatenew('P_link1', l[1]/2 * B.y)
P_link3 = O.locatenew('P_link1', l[2]/2 * C.y)

#setting velocities of these points with v2pt theory ...
P_link1.v2pt_theory(O, I, A)
P_link2.v2pt_theory(P_link1, I, B)
P_link3.v2pt_theory(P_link2, I, C)

points_rigid_body = [P_link1,P_link2,P_link3]


#defining inertia tensors for links

inertia_link1 = inertia(A,Ixx[0],Iyy[0],0)
inertia_link2 = inertia(B,Ixx[1],Iyy[1],0)
inertia_link3 = inertia(C,Ixx[2],Iyy[2],0)

#Defining links as Rigid bodies ...

link1 = RigidBody('link1', P_link1, A, M[0], (inertia_link1, O))
link2 = RigidBody('link2', P_link2, B, M[1], (inertia_link2, P1))
link3 = RigidBody('link3', P_link3, C, M[2], (inertia_link3, P2))
links = [link1,link2,link3]


#Defining a basic shape for links ..
rod1 = Cylinder(length=l[0],radii=radii[0])
rod2 = Cylinder(length=l[1],radii=radii[1])
rod3 = Cylinder(length=l[2],radii=radii[2])

link1.shape(rod1)
link2.shape(rod2)
link3.shape(rod3)

#Applying forces on all particles , and adding all forces in a list..
forces = []
for particle in particles:
    
    mass =  particle.get_mass()
    point =  particle.get_point()
    forces.append((point, -mass * g * I.y) )

#Applying forces on rigidbodies ..
for link in links:
    mass = link.get_mass()
    point = link.get_masscenter()
    forces.append((point, -mass * g * I.y) ) 

kinetic_differentials = []
for i in range(0,N_bobs):
    kinetic_differentials.append(alphad[i] - alpha[i])
    kinetic_differentials.append(betad[i] - beta[i])

#Adding particles and links in the same system ...
total_system = []
for particle in particles:
    total_system.append(particle)

for link in links:
    total_system.append(link)

q = []
for angle in alpha:
	q.append(angle)
for angle in beta:
	q.append(angle)
print q
u = []

for vel in alphad:
	u.append(vel)
for vel in betad:
	u.append(vel)

print u		
kane = KanesMethod(I, q_ind=q, u_ind=u, kd_eqs=kinetic_differentials)
fr, frstar = kane.kanes_equations(forces, total_system)

print fr

#Now we have symbolic equations of motion. ..
# we integrate them numerically. ..

params = [g ,l1,l2,l3,m1,m2,m3,M1,M2,M3]

param_vals = [9.8 ,1.0,1.0,1.0,2,2,2,5,5,5]

right_hand_side = code_generator(kane,params)   

#setting initial conditions ..
init_conditions = [radians(45),radians(45),radians(30),\
                   radians(30),radians(15),radians(15),\
                           0,           0,         0,\
                           0,           0,          0]
t = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

numerical_vals = odeint(right_hand_side,init_conditions,t)

#Now for each t, we have numerical vals of coordinates ..
#Now we set up a visualization frame, 

frame1 = VisualizationFrame('frame1',I,O)

frame1.add_rigidbodies(links)

frame1.add_particles(particles)

param_vals_for_viz = {'g':9.8 ,'l1':1.0,'l2':1.0,'l3':1.0,'m1':2,'m2':2,'m3':2,'M1':5,'M1':5,'M1':5]

json = frame1.generate_json(initial_conditions,q)
#Here we can replace initial_conditions with the conditions at any 
#specific time interval ....

##This line does following things ...
##calls RigidBody.transform_matrix() on all rigidbodies, 
#so that we have info of rigidbodies(CoM,rotation,translation)
# w.r.t VisualizationFrame('I' in this case) 
##Even if they are defined in any other frame ....
##calls point.set_pos() for all particles with arg 
##as Point in VisualizationFrame(O here) ..
##With these and init_conditions, we have a starting point of visualization ..

scene = Scene()
Scene.view(json)      # Just visualize/view the system at initial_conditions,
                      #w.r.t VIsualizationFrame(I in this case) 
                      # No simulation here. ..
                      
Scene.simulate(json,numerical_vals)  # modify the input json,
									 #Add the values at different times from numerical_vals,
									 #To the json, which is then passed to 
									 #javascript
									 #
									 #(alpha1,alpha2,alpha3,beta1,beta2,beta3) at time=t 						 	



