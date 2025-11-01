import matplotlib.pyplot as plt
from src.integrators import solve_twobody
from src.tools import center_of_mass, read_input_file
import sys

import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'outputs')

def twobody_display(params):
    # Retrieving parameters from the dictonary
    t = params["time_days"]
    r = params["r"]
    m1 = params['m1']
    m2 = params['m2']
    vx1_0 = params['vx1_0']
    vy1_0 = params['vy1_0']
    vx2_0 = params['vx2_0']
    vy2_0 = params['vy2_0']

    # Representing the initial bodies on the X-axis.
    r1 = (-m2/(m1+m2))*r
    r2 = (m1/(m1+m2))*r

    # Solving the two-body differential equation and then plot the results.
    solution = solve_twobody((0,t*24*3600), r1, 0, r2, 0, vx1_0, vy1_0, vx2_0, vy2_0, m1, m2)    
    x1, y1 = solution.y[0], solution.y[1]
    x2, y2 = solution.y[4], solution.y[5]

    xg,yg = center_of_mass(x1,y1,x2,y2,m1,m2)

    # Plotting.
    fig, axs = plt.subplots(3, 1, figsize=(6, 18))
    # Inertial Frame. 
    ax = axs[0]
    ax.plot(x1, y1, color='blue', linewidth=0.5, label='m1')
    ax.plot(x2, y2, color='red', linewidth=0.5, label='m2')
    ax.plot(xg, yg, color='black', ls="--", linewidth=0.5, label='G')

    ax.scatter(x1[0], y1[0], color='blue', s=20)
    ax.scatter(x2[0], y2[0], color='red', s=20)
    ax.scatter([0], [0], color="black", s=20)
    ax.scatter(x1[-1], y1[-1], color="blue", marker='s', s=20)
    ax.scatter(x2[-1], y2[-1], color="red", marker='s', s=20)
    ax.scatter(xg[-1], yg[-1], color="black", marker='s', s=20)

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.legend()
    ax.axis('equal')
    ax.set_title("Inertial Frame")

    # Non-rotating frame attached to m1. 
    ax = axs[1]
    newx2 = x2 - x1
    newy2 = y2 - y1
    newxg = xg - x1
    newyg = yg - y1

    ax.plot(newx2, newy2, color='red', linewidth=0.5, label='m2')
    ax.plot(newxg, newyg, color='black', ls='--', linewidth=0.5, label='G')
    ax.scatter([0], [0], color='blue', s=20)
    ax.scatter(newx2[0], newy2[0], color='red', s=20)
    ax.scatter(newxg[0], newyg[0], color='black', s=20)
    ax.scatter(newx2[-1], newy2[-1], color='red', marker='s', s=20)
    ax.scatter(newxg[-1], newyg[-1], color='black', marker='s', s=20)

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlabel("X relative to m1 (m)")
    ax.set_ylabel("Y relative to m1 (m)")
    ax.legend()
    ax.axis('equal')
    ax.set_title("Frame attached to m1")

    # Non-rotating frame attached to G. 
    ax = axs[2]
    newx1 = x1 - xg
    newy1 = y1 - yg
    newx2 = x2 - xg
    newy2 = y2 - yg

    ax.plot(newx1, newy1, color='blue', linewidth=0.5, label='m1')
    ax.plot(newx2, newy2, color='red', linewidth=0.5, label='m2')
    ax.scatter([0], [0], color='black', s=20)
    ax.scatter(newx1[0], newy1[0], color='blue', s=20)
    ax.scatter(newx2[0], newy2[0], color='red', s=20)
    ax.scatter(newx1[-1], newy1[-1], color='blue', marker='s', s=20)
    ax.scatter(newx2[-1], newy2[-1], color='red', marker='s', s=20)

    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlabel("X relative to G (m)")
    ax.set_ylabel("Y relative to G (m)")
    ax.legend()
    ax.axis('equal')
    ax.set_title("Frame attached to G")

    # Saving.
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "two_body_simulation_combined.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close('all')

if __name__ == "__main__":

    # Recovering initial conditions from the input file.
    filename = sys.argv[1]
    params = read_input_file(filename)
    
    t = params.get("time_days")
    r = params.get("distance")
    m1 = params.get("m1")
    m2 = params.get("m2")
    vx1_0 = params.get("vx1_0")
    vy1_0 = params.get("vy1_0")
    vx2_0 = params.get("vx2_0")
    vy2_0 = params.get("vy2_0")

    v1_0 = [vx1_0, vy1_0]
    v2_0 = [vx2_0, vy2_0]
    twobody_display(t,r,m1,m2,v1_0, v2_0)