#For this one we assume massless links
from sympy import symbols
from sympy.physics.mechanics import *

#Number of masses = 3
N_bobs = 3

#Defining Dynamic Symbols ................

#Generalized coordinates ...
q = dynamicsymbols('q:' + str(N_bobs))    

#Generalized speeds ...
u = dynamicsymbols('u:' + str(N_links + 1))

#Mass of each bob:
m = symbols('m:'+str(N_bobs))

#Length of each link ..
l = symbols('l:' + str(N_links)) 


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

#Three more points, for particles ..
P1 = O.locatenew('P1', l[0] * A.x)
P2 = O.locatenew('P2', l[1] * B.x)
P3 = O.locatenew('P3', l[2] * C.x)

#Setting velocities of points with v2pt theory ...
P1.v2pt_theory(O, I, A)
P2.v2pt_theory(P1, I, B)
P3.v2pt_theory(P2, I, C)
points = [P1,P2,P3]

#Defining particles ...
Pa1 = Particle('Pa1', points[0], m[0])
Pa2 = Particle('Pa2', points[1], m[1])
Pa3 = Particle('Pa3', points[2], m[2])
particles = [Pa1,Pa2,Pa3]



#Applying forces on all particles , and adding all forces in a list..
forces = []
for particle in particles:
    
    mass =  particle.get_mass()
    point =  particle.get_point()
    forces.append((point, -mass * g * I.y) )




print forces
kinetic_differentials = []
for i in range(0,N_bobs):
    kinetic_differentials.append(q[i].diff(t) - u[i])

print kinetic_differentials

kane = KanesMethod(I, q_ind=q, u_ind=u, kd_eqs=kinetic_differentials)
fr, frstar = kane.kanes_equations(forces, particles)

print(fr+frstar)


