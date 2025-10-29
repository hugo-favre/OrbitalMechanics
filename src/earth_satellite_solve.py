import numpy as np
from scipy.integrate import solve_ivp
mu = 3.986004418e14 

# Function describing the two-body differential equation with m_earth >> m_satellite, 3D.
def two_body_3D(t,coord):
    x,y,z,vx,vy,vz = coord
    r = np.sqrt(x**2 + y**2 + z**2)

    ax = -mu*x/(r**3)
    ay = -mu*y/(r**3)
    az = -mu*z/(r**3)

    return [vx, vy, vz, ax, ay, az]

# Function computing the position of the satellite, given initial conditions.
def solve(timespan, x_0, y_0, z_0, vx_0, vy_0, vz_0,):
    time_eval = np.linspace(*timespan, 50000)
    coord_0 = [x_0, y_0, z_0, vx_0, vy_0, vz_0]
    solution = solve_ivp(two_body_3D, timespan, coord_0, t_eval = time_eval, rtol=1e-12, atol=1e-15, method = "RK45")
    return solution

# Function converting the cartesians coordinates of the satellite to its orbital elements.
def rv_to_oe(r_vec, v_vec):
    r = np.array(r_vec, dtype=float)
    v = np.array(v_vec, dtype=float)
    r_norm = np.linalg.norm(r)
    v_norm = np.linalg.norm(v)

    h = np.cross(r, v)
    h_norm = np.linalg.norm(h)

    k = np.array([0.0, 0.0, 1.0])
    n = np.cross(k, h)
    n_norm = np.linalg.norm(n)

    energy = v_norm**2 / 2 - mu / r_norm

    if abs(energy) > 0:
        a = -mu / (2 * energy)
    else:
        a = np.inf

    e_vec = (1/mu) * ( (v_norm**2 - mu/r_norm)*r - np.dot(r, v)*v )
    e = np.linalg.norm(e_vec)

    i = np.arccos(h[2] / h_norm)

    if n_norm != 0:
        RAAN = np.arctan2(n[1], n[0])
        RAAN = RAAN % (2*np.pi)
    else:
        RAAN = 0.0

    if n_norm != 0 and e > 1e-12:
        argp = np.arctan2(np.dot(np.cross(n, e_vec), h) / h_norm,
                        np.dot(n, e_vec))
        argp = argp % (2*np.pi)
    else:
        argp = 0.0

    if e > 1e-12:
        nu = np.arctan2(np.dot(np.cross(e_vec, r), h) / (h_norm * e),
                np.dot(e_vec, r) / e)
        if nu < 0:
            nu += 2*np.pi
    else:
        if n_norm != 0:
            nu = np.arccos(np.dot(n, r) / (n_norm * r_norm))
            if r[2] < 0:
                nu = 2*np.pi - nu
        else:
            nu = 0.0

    return [a,e,np.degrees(i), np.degrees(RAAN), np.degrees(argp), np.degrees(nu), h, energy]

# Function converting the orbital elements of the satellite to its cartesians coordinates.
def oe_to_rv(a, e, i_deg, RAAN_deg, argp_deg, nu_deg):
    i = np.radians(i_deg)
    RAAN = np.radians(RAAN_deg)
    argp = np.radians(argp_deg)
    nu = np.radians(nu_deg)

    p = a * (1 - e**2)
    r = p / (1 + e*np.cos(nu))
    h = np.sqrt(mu * p)

    r_orb = np.array([r*np.cos(nu), r*np.sin(nu), 0.0])
    v_orb = np.array([-mu/h * np.sin(nu), mu/h * (e + np.cos(nu)), 0.0])

    R3_W = np.array([[ np.cos(RAAN), -np.sin(RAAN), 0],
                     [ np.sin(RAAN),  np.cos(RAAN), 0],
                     [ 0, 0, 1]])
    R1_i = np.array([[1, 0, 0],
                     [0, np.cos(i), -np.sin(i)],
                     [0, np.sin(i),  np.cos(i)]])
    R3_w = np.array([[ np.cos(argp), -np.sin(argp), 0],
                     [ np.sin(argp),  np.cos(argp), 0],
                     [ 0, 0, 1]])

    R = R3_W @ R1_i @ R3_w
    r_ECI = R @ r_orb
    v_ECI = R @ v_orb
    return r_ECI, v_ECI

def calc_period(a):
    return 2*np.pi*np.sqrt(a**3/mu)