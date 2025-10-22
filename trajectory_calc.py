import numpy as np
from scipy.integrate import solve_ivp

G = 6.67430e-11

# Function describing the two-body differential equation.
def two_body(t,y,m1,m2):
    x1,y1,vx1,vy1,x2,y2,vx2,vy2 = y
    r12 = np.sqrt((x2-x1)**2 + (y2-y1)**2)

    ax1 = G*m2*(x2-x1)/(r12**3)
    ay1 = G*m2*(y2-y1)/(r12**3)

    ax2 = G*m1*(x1-x2)/(r12**3)
    ay2 = G*m1*(y1-y2)/(r12**3)

    return [vx1,vy1,ax1,ay1,vx2,vy2,ax2,ay2]

# Function solving the two-body problem, given initial conditions.
def solve(timespan, x1_0, y1_0, x2_0, y2_0, vx1_0, vy1_0, vx2_0, vy2_0, m1, m2):
    time_eval = np.linspace(*timespan, 50000)
    y0 = [x1_0, y1_0, vx1_0, vy1_0, x2_0, y2_0, vx2_0, vy2_0]
    solution = solve_ivp(two_body, timespan, y0, t_eval=time_eval, args=(m1,m2))
    return solution

# Function computing the coordinates of the center of mass.
def center_of_mass(x1,y1,x2,y2,m1,m2):
    x = (x1*m1 + x2*m2)/(m1+m2)
    y = (y1*m1 + y2*m2)/(m1+m2)
    return [x,y]