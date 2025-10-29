import matplotlib.pyplot as plt
from earth_satellite_solve import solve
from earth_satellite_solve import rv_to_oe
from earth_satellite_solve import oe_to_rv
from earth_satellite_solve import calc_period
from readfile import read_input_file
import sys

if __name__ == "__main__":
    # Recovering initial conditions from the input file
    filename = sys.argv[1]
    params = read_input_file(filename)
    if 'a' in params:
        # In this case, we input orbital elements. to solve, we first convert to cartesian.
        a = params['a']
        r_vec, v_vec = oe_to_rv(a=a, e=params['e'], i_deg=params.get('i_deg', 0),
        RAAN_deg=params.get('RAAN_deg', 0), argp_deg=params.get('argp_deg', 0), nu_deg=params.get('nu_deg', 0))
        x0, y0, z0 = r_vec
        vx0, vy0, vz0 = v_vec
        n_orbits = params['n_orbits']
        t = calc_period(a)*n_orbits
        
    else:
        # In this case, we already input cartesian values.
        t = params["time_days"]*24*3600
        x0 = params["x0"]
        y0 = params["y0"]
        z0 = params["z0"]
        vx0 = params["vx0"]
        vy0 = params["vy0"]
        vz0 = params["vz0"]

    # We solve the two-body differential equation and then plot the results.
    solution = solve((0,t), x0, y0, z0, vx0, vy0, vz0)    
    x, y, z = solution.y[0], solution.y[1], solution.y[2]

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x/1e3, y/1e3, z/1e3, color='royalblue', lw=1.5, label='Satellite')
    ax.scatter(0, 0, 0, color='black', s=80, label='Terre')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.legend()
    plt.show()

    

