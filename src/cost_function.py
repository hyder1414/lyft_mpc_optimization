# src/cost_function.py

import numpy as np
from src.config import LAMBDA_COLLISION, LAMBDA_OFFROAD

def compute_travel_time_cost(path, step_size=1.0):
    return len(path) * step_size

def compute_offroad_penalty(path):
    distances_from_center = np.linalg.norm(path, axis=1)
    penalty = np.sum(distances_from_center > 1000)  # Penalize if path goes too far
    return penalty

def compute_collision_risk(path):
    return 0.0  # placeholder for now

def total_cost(path):
    travel_time = compute_travel_time_cost(path)
    offroad = compute_offroad_penalty(path)
    collision = compute_collision_risk(path)

    cost = travel_time + LAMBDA_COLLISION * collision + LAMBDA_OFFROAD * offroad
    return cost
