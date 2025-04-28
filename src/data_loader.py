# src/data_loader.py

import numpy as np
import zarr
from src.config import DATA_PATH

def load_scene_data():
    dataset = zarr.open(DATA_PATH, mode='r')

    scenes = dataset['scenes']
    agents = dataset['agents']
    frames = dataset['frames']

    print(f"Loaded {scenes.shape[0]} scenes.")
    return scenes, agents, frames


# src/data_loader.py

def extract_ego_from_frame(frames, frame_index):
    """Extract ego vehicle position, heading, velocity from a given frame."""
    frame = frames[frame_index]
    ego_translation = frame['ego_translation']  # (x, y, z)
    ego_rotation = frame['ego_rotation']         # 3x3 matrix

    # Get position (x, y)
    position = ego_translation[:2]

    # Get heading (yaw angle) from rotation matrix
    yaw = np.arctan2(ego_rotation[1, 0], ego_rotation[0, 0])

    return position, yaw
