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
    penalty = 0
    for point in path:
        pixel = world_to_pixel(point)
        x, y = pixel
        if 0 <= y < aerial_img.shape[0] and 0 <= x < aerial_img.shape[1]:
            brightness = aerial_img[y, x]
            if brightness < 128:
                penalty += 1
        else:
            penalty += 5
    return penalty

def compute_collision_risk(path):
    """Fake collision: 5% chance a path collides at each step."""
    risk = 0
    for _ in path:
        if np.random.rand() < 0.05:  # 5% chance
            risk += 1
    return risk

def total_cost(path):
    travel_time = compute_travel_time_cost(path)
    offroad = compute_offroad_penalty(path)
    collision = compute_collision_risk(path)

    cost = travel_time + LAMBDA_COLLISION * collision + LAMBDA_OFFROAD * offroad
    return cost, travel_time, collision, offroad
