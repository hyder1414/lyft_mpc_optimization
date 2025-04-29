import os
import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from src.data_loader import load_scene_data, extract_ego_from_frame
from src.mpc import plan_naive_path, sequential_mpc
from src.cost_function import total_cost
from src.utils import euclidean_distance

os.makedirs("results/plots", exist_ok=True)
os.makedirs("results/logs", exist_ok=True)

def pick_random_start_goal(frames, min_distance=900, max_distance=1100):
    """Pick two ego positions from random frames that are ~1000m apart."""
    while True:
        f1 = random.randint(0, len(frames) - 1)
        f2 = random.randint(0, len(frames) - 1)
        start_pos, _ = extract_ego_from_frame(frames, f1)
        goal_pos, _ = extract_ego_from_frame(frames, f2)
        d = euclidean_distance(start_pos, goal_pos)
        if min_distance <= d <= max_distance:
            return start_pos, goal_pos, d

def main():
    scenes, agents, frames = load_scene_data()
    print(f"Loaded {len(scenes)} scenes and {len(frames)} frames.")

    results = []
    batch_size = 10

    for i in range(batch_size):
        start, goal, distance = pick_random_start_goal(frames)
        print(f"\n[{i+1}/{batch_size}] Distance: {distance:.2f}m")

        naive_path = plan_naive_path(start, goal)
        mpc_path = sequential_mpc(start, goal)

        naive_cost = total_cost(naive_path)
        mpc_cost = total_cost(mpc_path)

        print(f"Naive Cost: {naive_cost:.2f} | MPC Cost: {mpc_cost:.2f}")

        results.append({
            "start_x": start[0], "start_y": start[1],
            "goal_x": goal[0], "goal_y": goal[1],
            "distance": distance,
            "naive_cost": naive_cost,
            "mpc_cost": mpc_cost
        })

        # Plot and save
        plt.figure(figsize=(10, 8))
        plt.plot(naive_path[:, 0], naive_path[:, 1], 'r--', label="Naive")
        plt.plot(mpc_path[:, 0], mpc_path[:, 1], 'g-', label="MPC")
        plt.scatter([start[0], goal[0]], [start[1], goal[1]], c='blue', label="Start/Goal")
        plt.title(f"Path {i+1} | Distance: {distance:.1f}m")
        plt.legend()
        plt.axis('equal')
        plt.savefig(f"results/plots/path_{i+1}.png")
        plt.close()

    # Save all results
    with open("results/logs/batch_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\n✅ Batch evaluation completed. Results saved to results/logs/batch_results.csv")

if __name__ == "__main__":
    main()
