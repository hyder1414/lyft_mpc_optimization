# run_mpc_simulation.py

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

if __name__ == "__main__":
    main()
