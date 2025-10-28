import matplotlib.pyplot as plt
from earth_satellite_solve import solve
from readfile import read_input_file
import sys
#from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    # Recovering initial conditions from the input file
    filename = sys.argv[1]
    params = read_input_file(filename)
    
    t = params.get("time_days")
    x_0 = params.get("x_0")
    y_0 = params.get("y_0")
    z_0 = params.get("z_0")
    vx_0 = params.get("vx_0")
    vy_0 = params.get("vy_0")
    vz_0 = params.get("vz_0")

    # We solve the two-body differential equation and then plot the results.
    solution = solve((0,t*24*3600), x_0, y_0, z_0, vx_0, vy_0, vz_0)    
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