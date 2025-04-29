#cost_function.py
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from src.config import LAMBDA_COLLISION, LAMBDA_OFFROAD

# Load the aerial map once globally
AERIAL_MAP_PATH = "./data/aerial_map/aerial_map.png"
aerial_img = np.array(Image.open(AERIAL_MAP_PATH).convert('L'))  # Grayscale

# Define the mapping from world coordinates to pixel coordinates
MAP_ORIGIN = np.array([-3000, -3000])  # Lower left corner (world coordinates)
MAP_SCALE = 0.1  # meters per pixel (adjust if wrong)

def world_to_pixel(xy):
    """Convert (x,y) world coordinates to (i,j) pixel coordinates."""
    pixel = (xy - MAP_ORIGIN) / MAP_SCALE
    pixel = pixel.astype(int)
    return pixel

def compute_travel_time_cost(path, step_size=1.0):
    """Travel time cost based on path length."""
    return len(path) * step_size

def compute_offroad_penalty(path):
    """Penalty for going off-road based on aerial map brightness."""
    penalty = 0
    for point in path:
        pixel = world_to_pixel(point)
        x, y = pixel
        if 0 <= y < aerial_img.shape[0] and 0 <= x < aerial_img.shape[1]:
            brightness = aerial_img[y, x]  # CAREFUL: y first, then x
            if brightness < 128:  # Dark = off-road
                penalty += 1
        else:
            penalty += 5  # Outside map = big penalty
    return penalty

def compute_collision_risk(path):
    """Currently faked to zero (no real collision checking yet)."""
    return 0.0

def total_cost(path):
    """Return total cost and individual components."""
    travel_time = compute_travel_time_cost(path)
    offroad = compute_offroad_penalty(path)
    collision = compute_collision_risk(path)

    cost = travel_time + LAMBDA_COLLISION * collision + LAMBDA_OFFROAD * offroad

    return cost, travel_time, collision, offroad
