import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from src.config import LAMBDA_COLLISION, LAMBDA_OFFROAD

# Load aerial map
AERIAL_MAP_PATH = "./data/aerial_map/aerial_map.png"
aerial_img = np.array(Image.open(AERIAL_MAP_PATH).convert('L'))

# Map settings
MAP_ORIGIN = np.array([-3000, -3000])
MAP_SCALE = 0.1  # meters per pixel

def world_to_pixel(xy):
    pixel = (xy - MAP_ORIGIN) / MAP_SCALE
    pixel = pixel.astype(int)
    return pixel

def compute_travel_time_cost(path, step_size=1.0):
    return len(path) * step_size

def compute_offroad_penalty(path):
    pixels = world_to_pixel(np.array(path))
    x, y = pixels[:, 0], pixels[:, 1]
    
    # Filter in-bound points
    mask = (x >= 0) & (x < aerial_img.shape[1]) & (y >= 0) & (y < aerial_img.shape[0])
    valid_x, valid_y = x[mask], y[mask]
    brightness = aerial_img[valid_y, valid_x]
    
    offroad = np.sum(brightness < 128)
    out_of_bounds = len(path) - np.sum(mask)
    penalty = offroad + 5 * out_of_bounds
    return penalty


def compute_collision_risk(path, agents, safe_radius=10.0):
    if not agents:
        return 0

    path = np.array(path)
    agents = np.array(agents)
    path_exp = path[:, np.newaxis, :]
    agents_exp = agents[np.newaxis, :, :]
    dists = np.linalg.norm(path_exp - agents_exp, axis=2)
    return np.sum(np.any(dists < safe_radius, axis=1))  # number of risky steps
    
def compute_smoothness(path):
    path = np.array(path)
    if len(path) < 3:
        return 0
    diffs = np.diff(path, axis=0)
    angles = np.arctan2(diffs[:,1], diffs[:,0])
    angle_diffs = np.diff(angles)
    return np.sum(np.abs(angle_diffs))


def total_cost(path, agents=None):
    travel_time = compute_travel_time_cost(path)
    offroad = compute_offroad_penalty(path)
    collision = compute_collision_risk(path, agents) if agents else 0
    cost = travel_time + LAMBDA_COLLISION * collision + LAMBDA_OFFROAD * offroad
    return cost, travel_time, collision, offroad

