import matplotlib.pyplot as plt
import trajectory_calc
from trajectory_calc import solve

if __name__ == "__main__":
    t = float(input("Time of simulation (days):"))
    r_str= input("Initial distance (notation scientifique) : ")
    r = int(float(r_str))
    m1_str, m2_str = input("m1, m2 (notation scientifique) : ").split()
    m1 = int(float(m1_str))
    m2 = int(float(m2_str))
    vx1_0, vy1_0 = map(float, input("vx1_0, vy1_0 : ").split())
    vx2_0, vy2_0 = map(float, input("vx2_0, vy2_0 : ").split())
    
    r1 = (-m2/(m1+m2))*r
    r2 = (m1/(m1+m2))*r
    
    solution = solve((0,t*24*3600), r1, 0, r2, 0, vx1_0, vy1_0, vx2_0, vy2_0, m1, m2)    
    x1, y1 = solution.y[0], solution.y[1]
    x2, y2 = solution.y[4], solution.y[5]

    plt.figure(figsize=(6,6))
    plt.plot(x1, y1, label="m1")
    plt.plot(x2, y2, label="m2")
    plt.scatter([0], [0], color="black", s=10)
    plt.show()