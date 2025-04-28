# run_mpc_simulation.py
from src.cost_function import total_cost
from src.mpc import plan_path
from src.data_loader import load_scene_data, extract_ego_from_frame

def main():
    scenes, agents, frames = load_scene_data()
    print("Data loaded successfully!")
    print(f"Number of scenes: {scenes.shape[0]}")
    print(f"Number of frames: {frames.shape[0]}")
    print(f"Number of agents: {agents.shape[0]}")

    # Extract ego from first frame
    position, yaw = extract_ego_from_frame(frames, 0)
    print(f"Ego Position (x, y): {position}")
    print(f"Ego Heading (yaw): {yaw:.4f} radians")
    path = plan_path(position, yaw)
    print(f"Planned path shape: {path.shape}")

if __name__ == "__main__":
    main()
