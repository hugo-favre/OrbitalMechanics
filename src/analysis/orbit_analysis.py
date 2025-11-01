import matplotlib.pyplot as plt
from src.integrators import solve
from src.tools import rv_to_oe, oe_to_rv, calc_period, read_input_file
import sys
import numpy as np

import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'outputs')

def orbit_analysis(params):
    # Retrieving parameters from the dictionary.
    a = params["a"]
    e = params["e"]
    i = params.get("i_deg", 0)
    RAAN = params.get("RAAN_deg", 0)
    argp = params.get("argp_deg", 0)
    nu = params.get("nu_deg", 0)
    n_orbits = int(params.get("n_orbits", 1))

    # Converting them in order to solve.
    r_vec, v_vec = oe_to_rv(a, e, i, RAAN, argp, nu)
    x0, y0, z0 = r_vec
    vx0, vy0, vz0 = v_vec 
    t = calc_period(a)*n_orbits

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
   
    # Crée une figure avec 3 lignes et 2 colonnes
    fig, axs = plt.subplots(3, 2, figsize=(12, 9))

    # === 1. a (demi-grand axe) ===
    ax = axs[0, 0]
    ax.plot(solution.t / 3600, a_list / 1e3)
    ax.set_ylim((np.min(a_list) - 1) / 1e3, (np.max(a_list) + 1) / 1e3)
    ax.set_ylabel("a (km)")
    ax.set_xlabel("Temps (h)")
    ax.set_title("Demi-grand axe (a)")

    # === 2. RAAN ===
    ax = axs[0, 1]
    ax.plot(solution.t / 3600, RAAN_list)
    ax.set_ylim(-10, 370)
    ax.set_ylabel("RAAN (°)")
    ax.set_xlabel("Temps (h)")
    ax.set_title("Ascension droite du nœud ascendant (RAAN)")

    # === 3. e (excentricité) ===
    ax = axs[1, 0]
    ax.plot(solution.t / 3600, e_list)
    ax.set_ylim(-0.2, np.max(e_list) + 1)
    ax.set_ylabel("e")
    ax.set_xlabel("Temps (h)")
    ax.set_title("Excentricité (e)")

    # === 4. Argument du périgée (ω ou argp) ===
    ax = axs[1, 1]
    ax.plot(solution.t / 3600, argp_list)
    ax.set_ylim(-10, 370)
    ax.set_ylabel("ω (°)")
    ax.set_xlabel("Temps (h)")
    ax.set_title("Argument du périgée (ω)")

    # === 5. i (inclinaison) ===
    ax = axs[2, 0]
    ax.plot(solution.t / 3600, i_list)
    ax.set_ylim(-10, 190)
    ax.set_ylabel("i (°)")
    ax.set_xlabel("Temps (h)")
    ax.set_title("Inclinaison (i)")

    # === 6. Anomalie vraie (ν ou nu) ===
    ax = axs[2, 1]
    ax.plot(solution.t / 3600, nu_list)
    ax.set_ylim(-10, 370)
    ax.set_ylabel("ν (°)")
    ax.set_xlabel("Temps (h)")
    ax.set_title("Anomalie vraie (ν)")

    # Ajustement de la mise en page
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.suptitle("Évolution des éléments orbitaux", fontsize=14)

    # Sauvegarde en un seul PNG
    output_path = os.path.join(OUTPUT_DIR, "orbital_elements_evolution_combined.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close('all')
 
    # # Plotting the results.
    # plt.figure(figsize=(8,6))
    # plt.subplot(3,1,1)
    # plt.plot(solution.t/3600, a_list/1e3)
    # plt.ylim((np.min(a_list)-1) / 1e3 , (np.max(a_list)+1) / 1e3)
    # plt.ylabel("a (km)")

    # plt.subplot(3,1,2)
    # plt.plot(solution.t/3600, e_list)
    # plt.ylim(-0.2, np.max(e_list)+1)
    # plt.ylabel("e")

    # plt.subplot(3,1,3)
    # plt.plot(solution.t/3600, i_list)
    # plt.ylim(-10, 190)
    # plt.ylabel("i (°)")
    # plt.xlabel("Temps (h)")

    # output_path = os.path.join(OUTPUT_DIR, "orbital_elements_evolution_1.png")
    # plt.savefig(output_path, dpi=300, bbox_inches='tight')
    # plt.close('all')
        
    # plt.figure(figsize=(8,6))
    # plt.subplot(3,1,1)
    # plt.plot(solution.t/3600, RAAN_list)
    # plt.ylim(-10, 370)
    # plt.ylabel("RAAN (°)")

    # plt.subplot(3,1,2)
    # plt.plot(solution.t/3600, argp_list)
    # plt.ylim(-10, 370)
    # plt.ylabel("atgp (°)")

    # plt.subplot(3,1,3)
    # plt.plot(solution.t/3600, nu_list)
    # plt.ylim(-10, 370)
    # plt.ylabel("nu (°)")
    # plt.xlabel("Temps (h)")

    # plt.suptitle("Évolution des éléments orbitaux")

    # output_path = os.path.join(OUTPUT_DIR, "orbital_elements_evolution_2.png")
    # plt.savefig(output_path, dpi=300, bbox_inches='tight')
    # plt.close('all')