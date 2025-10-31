import numpy as np
from scipy.integrate import solve_ivp
from src.tools.constants import mu_earth

# Function describing the two-body differential equation with m_earth >> m_satellite, 3D.
def two_body_3D(t,coord):
    x,y,z,vx,vy,vz = coord
    r = np.sqrt(x**2 + y**2 + z**2)

    ax = -mu_earth*x/(r**3)
    ay = -mu_earth*y/(r**3)
    az = -mu_earth*z/(r**3)

    return [vx, vy, vz, ax, ay, az]

# Function computing the position of the satellite, given initial conditions.
def solve(timespan, x_0, y_0, z_0, vx_0, vy_0, vz_0,):
    time_eval = np.linspace(*timespan, 50000)
    coord_0 = [x_0, y_0, z_0, vx_0, vy_0, vz_0]
    solution = solve_ivp(two_body_3D, timespan, coord_0, t_eval = time_eval, rtol=1e-12, atol=1e-15, method = "RK45")
    return solution