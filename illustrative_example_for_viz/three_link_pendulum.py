
#For this one we assume RigidBody links
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
omega = dynamicsymbols('omega1 omega2 omega3')
delta = dynamicsymbols('delta1 delta2 delta3')

#Mass of each bob:
m = symbols('m:'+str(N_bobs))


#Length and mass of each link ..
l = symbols('l:' + str(N_links)) 
M = symbols('M:' + str(N_links)) 
#For storing Inertia for each link :
Ixx = symbols('Ixx:'+str(N_links))
Iyy = symbols('Iyy:'+str(N_links))
Izz = symbols('Izz:'+str(N_links))

#gravity and time ....
g, t = symbols('g t')


#Now defining an Inertial ReferenceFrame First ....

I = ReferenceFrame('I')

#And some other frames ...

A = ReferenceFrame('A')
A.orient(I,'Space',[alpha[0],beta[0],0],'ZXY')
B = ReferenceFrame('B')
B.orient(A,'Space',[alpha[1],beta[1],0],'ZXY')
C = ReferenceFrame('C')
C.orient(B,'Space',[alpha[2],beta[2],0],'ZXY')


#Setting angular velocities of new frames ...
A.set_ang_vel(I, omega[0] * I.z + delta[0] * I.x)
B.set_ang_vel(I, omega[1] * I.z + delta[1] * I.x)
C.set_ang_vel(I, omega[2] * I.z + delta[2] * I.x)



# An Origin point, with velocity = 0
O = Point('O')
O.set_vel(I,0)

#Three more points, for masses ..
P1 = O.locatenew('P1', -l[0] * A.y)
P2 = O.locatenew('P2', -l[1] * B.y)
P3 = O.locatenew('P3', -l[2] * C.y)

#Setting velocities of points with v2pt theory ...
P1.v2pt_theory(O, I, A)
P2.v2pt_theory(P1, I, B)
P3.v2pt_theory(P2, I, C)
points = [P1, P2, P3]

Pa1 = Particle('Pa1', points[0], m[0])
Pa2 = Particle('Pa2', points[1], m[1])
Pa3 = Particle('Pa3', points[2], m[2])
particles = [Pa1, Pa2, Pa3]



#defining points for links(RigidBodies)
#Assuming CoM as l/2 ...
P_link1 = O.locatenew('P_link1', -l[0]/2 * A.y)
P_link2 = P_link1.locatenew('P_link2', -l[1]/2 * B.y)
P_link3 = P_link2.locatenew('P_link3', -l[2]/2 * C.y)

#setting velocities of these points with v2pt theory ...
P_link1.v2pt_theory(O, I, A)
P_link2.v2pt_theory(P_link1, I, B)
P_link3.v2pt_theory(P_link2, I, C)

points_rigid_body = [P_link1, P_link2, P_link3]


#defining inertia tensors for links

inertia_link1 = inertia(A, Ixx[0], Iyy[0], Izz[0])
inertia_link2 = inertia(B, Ixx[1], Iyy[1], Izz[1])
inertia_link3 = inertia(C, Ixx[2], Iyy[2], Izz[2])

#Defining links as Rigid bodies ...

link1 = RigidBody('link1', P_link1, A, M[0], (inertia_link1, P_link1))
link2 = RigidBody('link2', P_link2, B, M[1], (inertia_link2, P_link2))
link3 = RigidBody('link3', P_link3, C, M[2], (inertia_link3, P_link3))
links = [link1, link2, link3]


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

kinematic_differentials = []
for i in range(0,N_bobs):
    kinematic_differentials.append(omega[i] - alpha[i].diff(t))
    kinematic_differentials.append(delta[i] - beta[i].diff(t))

#Adding particles and links in the same system ...
total_system = links + particles

q = alpha + beta

u = omega + delta

kane = KanesMethod(I, q_ind=q, u_ind=u, kd_eqs=kinematic_differentials)
fr, frstar = kane.kanes_equations(forces, total_system)

print fr




