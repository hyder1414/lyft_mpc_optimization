# src/mpc.py

import numpy as np

def plan_path(initial_position, initial_yaw, horizon=50, step_size=1.0):
    """
    Plan a straight-line path for now.
    (Later we'll replace with optimized MPC.)
    """
    path = []
    x, y = initial_position
    yaw = initial_yaw

    for _ in range(horizon):
        x += step_size * np.cos(yaw)
        y += step_size * np.sin(yaw)
        path.append((x, y))

    return np.array(path)
