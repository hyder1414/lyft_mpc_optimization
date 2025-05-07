#run_batch_mpc_simulation.py
import os
import csv
import random
import numpy as np
import matplotlib.pyplot as plt

from src.data_loader import load_scene_data, extract_ego_from_frame
from src.mpc import plan_naive_path, sequential_mpc_optimized
from src.lqr import ilqr_path_planner
from src.cost_function import total_cost
from src.utils import euclidean_distance

def pick_random_start_goal(frames, min_distance=900, max_distance=1100):
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

    os.makedirs("results/plots", exist_ok=True)
    os.makedirs("results/logs", exist_ok=True)

    batch_size = 10
    results = []

    for i in range(batch_size):
        start, goal, distance = pick_random_start_goal(frames)
        print(f"\n[{i+1}/{batch_size}] Distance: {distance:.2f}m")

        naive_path = plan_naive_path(start, goal)
        mpc_path = sequential_mpc_optimized(start, goal, agents)
        ilqr_path = ilqr_path_planner(start, goal)

        naive_total, naive_time, naive_collision, naive_offroad = total_cost(naive_path)
        mpc_total, mpc_time, mpc_collision, mpc_offroad = total_cost(mpc_path)
        ilqr_total, ilqr_time, ilqr_collision, ilqr_offroad = total_cost(ilqr_path)

        print(f"Naive Total Cost: {naive_total:.2f} (Time={naive_time:.2f}, Coll={naive_collision:.2f}, Offroad={naive_offroad:.2f})")
        print(f"MPC   Total Cost: {mpc_total:.2f} (Time={mpc_time:.2f}, Coll={mpc_collision:.2f}, Offroad={mpc_offroad:.2f})")

        results.append({
            "start_x": start[0], "start_y": start[1],
            "goal_x": goal[0], "goal_y": goal[1],
            "distance": distance,
            "naive_total": naive_total,
            "naive_travel_time": naive_time,
            "naive_collision": naive_collision,
            "naive_offroad": naive_offroad,
            "mpc_total": mpc_total,
            "mpc_travel_time": mpc_time,
            "mpc_collision": mpc_collision,
            "mpc_offroad": mpc_offroad,
            "ilqr_total": ilqr_total,
            "ilqr_travel_time": ilqr_time,
            "ilqr_collision": ilqr_collision,
            "ilqr_offroad": ilqr_offroad
        })

        # Plot
        plt.figure(figsize=(10,8))
        plt.plot(naive_path[:,0], naive_path[:,1], 'r--', label="Naive")
        plt.plot(mpc_path[:,0], mpc_path[:,1], 'g-', label="MPC")
        plt.scatter([start[0], goal[0]], [start[1], goal[1]], c='blue', label="Start/Goal")
        plt.title(f"Path {i+1} | Distance: {distance:.1f}m")
        plt.legend()
        plt.axis('equal')
        plt.savefig(f"results/plots/path_{i+1}.png")
        plt.close()

    # Save CSV
    keys = results[0].keys()
    with open("results/logs/batch_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print("\n✅ Batch run finished. Results saved to results/logs/batch_results.csv")

if __name__ == "__main__":
    main()
