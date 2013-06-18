#For this one we assume RigidBody links
from sympy import symbols,sympify
from sympy.physics.mechanics import *

#Number of links = 3
N_links = 3

#Number of masses = 3
N_bobs = 3

#Defining Dynamic Symbols ................

#Generalized coordinates ...
q = dynamicsymbols('q:' + str(N_bobs))    

#Generalized speeds ...
u = dynamicsymbols('u:' + str(N_links + 1))

#Mass of each bob:
m = symbols('m:'+str(N_bobs))


#Length and mass of each link ..
l = symbols('l:' + str(N_links)) 
M = symbols('M:' + str(N_links)) 
#For storingInertia for each bob :
i = symbols('i:'+str(N_bobs))


#gravity and time ....
g, t = symbols('g t')


#Now defining an Inertial ReferenceFrame First ....

I = ReferenceFrame('I')

#Getting more referenceframes for RigidBodies ...

A = I.orientnew('A', 'Axis', [q[0], I.z])
B = I.orientnew('B', 'Axis', [q[1], I.z])
C = I.orientnew('C', 'Axis', [q[2], I.z])

#Setting angular velocities of new frames ...
A.set_ang_vel(I, u[0] * I.z)
B.set_ang_vel(I, u[1] * I.z)
C.set_ang_vel(I, u[2] * I.z)



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
#Since links are rods, rotating axis= z-axis
#Hence, xx = yy = (1/12)*m*l**2

i0 = (1.0/3)*M[0]*l[0]**2
i1 = (1.0/3)*M[1]*l[1]**2
i2 = (1.0/3)*M[2]*l[2]**2

inertia_link1 = inertia(A,i0,i0,0)
inertia_link2 = inertia(B,i1,i1,0)
inertia_link3 = inertia(C,i2,i2,0)

#Defining links as Rigid bodies ...

link1 = RigidBody('link1', P_link1, A, M[0], (inertia_link1, O))
link2 = RigidBody('link2', P_link2, B, M[1], (inertia_link2, P1))
link3 = RigidBody('link3', P_link3, C, M[2], (inertia_link3, P2))
links = [link1,link2,link3]


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
    kinetic_differentials.append(q[i].diff(t) - u[i])

#Adding particles and links in the same system ...
total_system = []
for particle in particles:
    total_system.append(particle)

for link in links:
    total_system.append(link)

kane = KanesMethod(I, q_ind=q, u_ind=u, kd_eqs=kinetic_differentials)
fr, frstar = kane.kanes_equations(forces, total_system)

print fr







