import matplotlib.pyplot as plt
from two_body_solve import solve
from two_body_solve import center_of_mass
from readfile import read_input_file
import sys

if __name__ == "__main__":

    # Recovering initial conditions from the input file
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

    # We choose to represent the initial bodies on the X-axis.
    r1 = (-m2/(m1+m2))*r
    r2 = (m1/(m1+m2))*r

    # We solve the two-body differential equation and then plot the results.
    solution = solve((0,t*24*3600), r1, 0, r2, 0, vx1_0, vy1_0, vx2_0, vy2_0, m1, m2)    
    x1, y1 = solution.y[0], solution.y[1]
    x2, y2 = solution.y[4], solution.y[5]

    xg,yg = center_of_mass(x1,y1,x2,y2,m1,m2)

    # First plot in the Inertial Frame
    plt.figure(figsize=(6,6))
    plt.plot(x1, y1, color='blue', linewidth=0.5, label='m1')
    plt.plot(x2, y2, color='red', linewidth=0.5, label='m2')
    plt.plot(xg,yg , color='black', ls="--", linewidth=0.5, label='G')

    plt.scatter(x1[0], y1[0], color='blue',s=20)
    plt.scatter(x2[0], y2[0], color='red',s=20)
    plt.scatter([0], [0], color="black", s=20)

    plt.scatter(x1[-1], y1[-1], color="blue", marker='s', s=20)
    plt.scatter(x2[-1], y2[-1], color="red", marker='s', s=20)
    plt.scatter(xg[-1], yg[-1], color="black", marker='s', s=20)

    plt.axhline(0, color='gray', linewidth=0.5) 
    plt.axvline(0, color='gray', linewidth=0.5) 
    
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.legend() 
    plt.axis('equal')

    # Plot in the non-rotating frame attached to m1
    plt.figure(figsize=(6,6))
    newx2 = x2-x1
    newy2 = y2-y1
    newxg = xg-x1
    newyg = yg-y1
    plt.plot(newx2, newy2, color='red', linewidth=0.5, label='m2')
    plt.plot(newxg, newyg, color='black', ls='--', linewidth=0.5, label='G')

    plt.scatter([0], [0], color='blue',s=20)
    plt.scatter(newx2[0], newy2[0], color='red',s=20)
    plt.scatter(newxg[0], newyg[0], color="black", s=20)

    plt.scatter(newx2[-1], newy2[-1], color="red", marker='s', s=20)
    plt.scatter(newxg[-1], newyg[-1], color="black", marker='s', s=20)  

    plt.axhline(0, color='gray', linewidth=0.5) 
    plt.axvline(0, color='gray', linewidth=0.5) 

    plt.xlabel("X relative to m1(m)")
    plt.ylabel("Y relative to m1(m)")
    plt.legend()
    plt.axis("equal")

    # Plot in the non-rotating frame attached to G
    plt.figure(figsize=(6,6))
    newx1 = x1-xg
    newy1 = y1-yg
    newx2 = x2-xg
    newy2 = y2-yg
    plt.plot(newx1, newy1, color='blue', linewidth=0.5, label='m1')
    plt.plot(newx2, newy2, color ='red', linewidth=0.5, label='m2')

    plt.scatter([0], [0], color='black',s=20)
    plt.scatter(newx1[0], newy1[0], color='blue',s=20)
    plt.scatter(newx2[0], newy2[0], color="red", s=20)  

    plt.scatter(newx1[-1], newy1[-1], color="blue", marker='s', s=20)
    plt.scatter(newx2[-1], newy2[-1], color="red", marker='s', s=20)

    plt.axhline(0, color='gray', linewidth=0.5) 
    plt.axvline(0, color='gray', linewidth=0.5) 
    
    plt.xlabel("X relative to G(m)")
    plt.ylabel("Y relative to G(m)")
    plt.legend()
    plt.axis("equal")

    plt.show()