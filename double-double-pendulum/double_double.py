from sympy import symbols
from sympy.physics.mechanics import *
from code import numeric_right_hand_side
from scipy.integrate import odeint
from numpy import hstack, ones, zeros, linspace, pi

q1, q2, q3 = dynamicsymbols('q1 q2 q3')
q1d, q2d, q3d = dynamicsymbols('q1 q2 q3', 1)
u1, u2, u3 = dynamicsymbols('u1 u2 u3')
u1d, u2d, u3d = dynamicsymbols('u1 u2 u3', 1)
l, m, g = symbols('l m g')

N = ReferenceFrame('N')
A = N.orientnew('A', 'Axis', [q1, N.z])
B = N.orientnew('B', 'Axis', [q2, N.z])
C = N.orientnew('C', 'Axis', [q3, N.z])

A.set_ang_vel(N, u1 * N.z)
B.set_ang_vel(N, u2 * N.z)
C.set_ang_vel(N, u3 * N.z)

O = Point('O')
P = O.locatenew('P', l * A.x)
R = P.locatenew('R', l * B.x)
Q = P.locatenew('Q', l * C.x)

O.set_vel(N, 0)
P.v2pt_theory(O, N, A)
R.v2pt_theory(P, N, B)
Q.v2pt_theory(P, N, C)

ParP = Particle('ParP', P, m)
ParR = Particle('ParR', R, m)
ParQ = Particle('ParQ', Q, m)

kd = [q1d - u1, q2d - u2, q3d - u3]
forces = [(R, m * g * N.x), (Q, m * g * N.x)]
bodies = [ParP, ParR, ParQ]

kane = KanesMethod(N, q_ind=[q1, q2, q3], u_ind=[u1, u2, u3], kd_eqs=kd)

(fr, frstar) = kane.kanes_equations(forces, bodies)

rhs = numeric_right_hand_side(kane, [l, m, g])

x0 = hstack(( [pi / 3.0, pi / 3.0, pi / 4.0], 1e-13 * ones(3) )) # Initial conditions, q and u
t = linspace(0, 10, 1000)                                          # Time vector
y = odeint(rhs, x0, t, args=((5.0, 6.0, 9.8),))         # Actual integration
