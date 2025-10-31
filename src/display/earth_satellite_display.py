import numpy as np
import plotly.graph_objects as go
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip 
import sys
from src.integrators import solve
from src.tools import oe_to_rv, calc_period, read_input_file, R_EARTH

import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'outputs')

def orbit_display(a, e, i, RAAN, argp, nu, n_orbits): 
    r_vec, v_vec = oe_to_rv(a, e, i, RAAN, argp, nu)
    x0, y0, z0 = r_vec
    vx0, vy0, vz0 = v_vec 
    t = calc_period(a)*n_orbits

    # Solving the two-body differential equation and then plot the results.
    solution = solve((0,t), x0, y0, z0, vx0, vy0, vz0)    
    r_x, r_y, r_z = solution.y[0], solution.y[1], solution.y[2]

    ### Plotting the orbit.
    fig = go.Figure()

    r0 = np.array([r_x[0], r_y[0], r_z[0]])
    v0 = np.array([solution.y[3,0], solution.y[4,0], solution.y[5,0]])
    h = np.cross(r0, v0)
    h_hat = h / np.linalg.norm(h)

    # Fictive trace, to be deleted by the animation
    fig.add_trace(go.Surface())

    # Earth sphere.
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    x = R_EARTH * np.outer(np.cos(u), np.sin(v))
    y = R_EARTH * np.outer(np.sin(u), np.sin(v))
    z = R_EARTH * np.outer(np.ones(np.size(u)), np.cos(v))
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, "royalblue"], [1, "royalblue"]],
        opacity=0.9,
        showscale=False
    ))

    # Equatorial plane.
    r_eq = max(a*(1+e)/np.sqrt(2), R_EARTH*np.sqrt(2))
    r_orb = np.linspace(0, r_eq, 60)
    theta = np.linspace(0, 2*np.pi, 60)
    R, TH = np.meshgrid(r_orb, theta)
    Xp = R * np.cos(TH)
    Yp = R * np.sin(TH)
    Zp = np.zeros_like(Xp)

    fig.add_trace(go.Surface(
        x=Xp, y=Yp, z=Zp,
        colorscale=[[0, "rgba(0,255,255,0.5)"], [1, "rgba(0,255,255,0.5)"]],
        opacity=0.4,
        showscale=False,
        showlegend=True,
        name="Equatorial plane"
    ))

    # North-South axis.
    pole_length = R_EARTH * 1.5
    fig.add_trace(go.Scatter3d(
        x=[0, 0],
        y=[0, 0],
        z=[-pole_length, pole_length],
        mode="lines",
        line=dict(color="white", width=4),
        name="Earth rotation axis"
    ))

    # Origin of longitude
    vernal_length = R_EARTH * 1.5
    fig.add_trace(go.Scatter3d(
        x=[-vernal_length, vernal_length],
        y=[0, 0],
        z=[0, 0],
        mode="lines",
        line=dict(color="white", width=5), 
        name="Vernal equinox direction",
        showlegend=True
    ))

    # Orbit.
    fig.add_trace(go.Scatter3d(
        x=r_x, y=r_y, z=r_z,
        mode="lines",
        line=dict(color="orange", width=4),
        name="Orbit"
    ))

    # Initial position of the satellite.
    fig.add_trace(go.Scatter3d(
        x=[r_x[0]], y=[r_y[0]], z=[r_z[0]],
        mode="markers",
        marker=dict(color="red", size=6),
        name="Initial position"
    ))

    max_range = max(np.max(np.abs([r_x, r_y, r_z])), R_EARTH*np.sqrt(2))
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1),
            xaxis_range=[-max_range, max_range],
            yaxis_range=[-max_range, max_range],
            zaxis_range=[-max_range, max_range],
            bgcolor="black"
        ),
        paper_bgcolor="black",
        plot_bgcolor="black",
        showlegend=True,
        legend=dict(
            font=dict(color="white"),
            bgcolor="rgba(0,0,0,0.5)"
        )
    )
    fig.update_layout(scene_camera=dict(
        eye=dict(x=1.5, y=1.5, z=0.8)
    ))

    # Animating
    frames = [
        go.Frame(
            data=[
                go.Scatter3d(
                    x=[r_x[k]], y=[r_y[k]], z=[r_z[k]],
                    mode="markers",
                    marker=dict(color="darkorange", size=6),
                    name="Satellite"
                )
            ],
            name=f"frame{k}"
        )
        for k in range(0, len(r_x), int(len(r_x)/500)) 
    ]
    fig.frames = frames

    fig.update_layout(
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [
                {
                    "label": "▶️ Play",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 20, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 0}
                    }]
                },
                {
                    "label": "⏸ Pause",
                    "method": "animate",
                    "args": [[None], {
                        "frame": {"duration": 0, "redraw": False},
                        "mode": "immediate",
                        "transition": {"duration": 0}
                    }]
                }
            ],
            "x": 0.05, "y": 0.05,
            "xanchor": "left", "yanchor": "bottom",
            "bgcolor": "rgba(0,0,0,0.5)",
            "bordercolor": "white"
        }]
    )
    
    fig.show()
    
    # Video tries
    # frame_step = 100
    # frames = []
    # for k in range(0, len(x), frame_step):
    #     fig = go.Figure()
    #     # Terre
    #     # ...
    #     # Orbite jusqu’à k
    #     fig.add_trace(go.Scatter3d(
    #         x=x[:k+1], y=y[:k+1], z=z[:k+1],
    #         mode="lines", line=dict(color="orange", width=5)
    #     ))
    #     # Satellite
    #     fig.add_trace(go.Scatter3d(
    #         x=[x[k]], y=[y[k]], z=[z[k]],
    #         mode="markers", marker=dict(color="red", size=5)
    #     ))
    #     fig.update_layout(scene=dict(bgcolor="black", aspectmode='data'),
    #                       margin=dict(l=0, r=0, t=0, b=0))
    #     frame_path = os.path.join(OUTPUT_DIR, f"frame_{k:04d}.png")
    #     fig.write_image(frame_path)
    #     frames.append(frame_path)

    # output_video = os.path.join(OUTPUT_DIR, "earth_satellite_orbit.mp4")
    # clip = ImageSequenceClip(frames, fps=30)
    # clip.write_videofile(output_video, codec='libx264')


if __name__ == "__main__":
    # Recovering initial conditions from the input file.
    filename = sys.argv[1]
    params = read_input_file(filename)
    orbit_display(a=params['a'], e=params['e'], i=params.get('i_deg', 0),
    RAAN=params.get('RAAN_deg', 0), argp=params.get('argp_deg', 0), nu=params.get('nu_deg', 0), n_orbits=params['n_orbits'])