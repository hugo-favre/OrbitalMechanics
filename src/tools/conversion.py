import numpy as np
from .constants import mu_earth

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

    energy = v_norm**2 / 2 - mu_earth / r_norm

    if abs(energy) > 0:
        a = -mu_earth / (2 * energy)
    else:
        a = np.inf

    e_vec = (1/mu_earth) * ( (v_norm**2 - mu_earth/r_norm)*r - np.dot(r, v)*v )
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
    h = np.sqrt(mu_earth * p)

    r_orb = np.array([r*np.cos(nu), r*np.sin(nu), 0.0])
    v_orb = np.array([-mu_earth/h * np.sin(nu), mu_earth/h * (e + np.cos(nu)), 0.0])

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

# Function computing the period of an orbit knowing a.
def calc_period(a):
    return 2*np.pi*np.sqrt(a**3/mu_earth)

# Function computing the coordinates of the center of mass.
def center_of_mass(x1,y1,x2,y2,m1,m2):
    x = (x1*m1 + x2*m2)/(m1+m2)
    y = (y1*m1 + y2*m2)/(m1+m2)
    return [x,y]