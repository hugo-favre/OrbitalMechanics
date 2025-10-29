import matplotlib.pyplot as plt
from earth_satellite_solve import solve
from earth_satellite_solve import rv_to_oe
from earth_satellite_solve import oe_to_rv
from earth_satellite_solve import calc_period
from readfile import read_input_file
import sys
import numpy as np

if __name__ == "__main__":
    # Recovering initial conditions from the input file.
    filename = sys.argv[1]
    params = read_input_file(filename)

    if 'a' in params:
        # The input is the orbital elements. Conversion to cartesian values.
        a = params['a']
        r_vec, v_vec = oe_to_rv(a=a, e=params['e'], i_deg=params.get('i_deg', 0),
        RAAN_deg=params.get('RAAN_deg', 0), argp_deg=params.get('argp_deg', 0), nu_deg=params.get('nu_deg', 0))
        x0, y0, z0 = r_vec
        vx0, vy0, vz0 = v_vec
        n_orbits = params['n_orbits']
        t = calc_period(a)*n_orbits
        
    else:
        # Input is the cartesian values.
        t = params["time_days"]*24*3600
        x0 = params["x0"]
        y0 = params["y0"]
        z0 = params["z0"]
        vx0 = params["vx0"]
        vy0 = params["vy0"]
        vz0 = params["vz0"]

    # print("DEBUG initial OE:", a, params['e'], params['i_deg'],params['RAAN_deg'], params['argp_deg'], params['nu_deg'])
    # a2, e2, i2, RAAN2, argp2, nu2, h2, energy2 = rv_to_oe(r_vec, v_vec)
    # print("DEBUG roundtrip OE:", a2, e2, i2, RAAN2, argp2, nu2)

    # Solving the two-body differential equation and then plot the results.
    solution = solve((0,t), x0, y0, z0, vx0, vy0, vz0)    
    x, y, z = solution.y[0], solution.y[1], solution.y[2]

    a_list, e_list, i_list = [], [], []
    RAAN_list, argp_list, nu_list = [], [], []

    for k in range(len(solution.t)):
        r_vec = [solution.y[0, k], solution.y[1, k], solution.y[2, k]]
        v_vec = [solution.y[3, k], solution.y[4, k], solution.y[5, k]]
        a, e, i, RAAN, argp, nu, h, energy = rv_to_oe(r_vec, v_vec)

        a_list.append(a)
        e_list.append(e)
        i_list.append(i)
        RAAN_list.append(RAAN)
        argp_list.append(argp)
        nu_list.append(nu)
        
    a_list = np.array(a_list)
    e_list = np.array(e_list)
    i_list = np.array(i_list)
    RAAN_list = np.array(RAAN_list)
    argp_list = np.array(argp_list)
    nu_list = np.array(nu_list)
    

    # Tracé
    plt.figure(figsize=(8,6))
    plt.subplot(3,1,1)
    plt.plot(solution.t/3600, a_list/1e3)
    plt.ylim((np.min(a_list)-1) / 1e3 , (np.max(a_list)+1) / 1e3)
    plt.ylabel("a (km)")

    plt.subplot(3,1,2)
    plt.plot(solution.t/3600, e_list)
    plt.ylim(-0.2, np.max(e_list)+1)
    plt.ylabel("e")

    plt.subplot(3,1,3)
    plt.plot(solution.t/3600, i_list)
    plt.ylim(-10, 190)
    plt.ylabel("i (°)")
    plt.xlabel("Temps (h)")

    plt.figure(figsize=(8,6))
    plt.subplot(3,1,1)
    plt.plot(solution.t/3600, RAAN_list)
    plt.ylim(-10, 370)
    plt.ylabel("RAAN (°)")

    plt.subplot(3,1,2)
    plt.plot(solution.t/3600, argp_list)
    plt.ylim(-10, 370)
    plt.ylabel("atgp (°)")

    plt.subplot(3,1,3)
    plt.plot(solution.t/3600, nu_list)
    plt.ylim(-10, 370)
    plt.ylabel("nu (°)")
    plt.xlabel("Temps (h)")

    plt.suptitle("Évolution des éléments orbitaux")
    plt.show()
        