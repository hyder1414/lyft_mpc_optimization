import matplotlib.pyplot as plt
import numpy as np
import zarr

from src.mpc import sequential_mpc, plan_naive_path
from src.cost_function import total_cost

def pick_start_goal(centroids, min_dist=900, max_dist=1100):
    while True:
        idx_start = np.random.choice(len(centroids))
        idx_goal = np.random.choice(len(centroids))
        start = centroids[idx_start]
        goal = centroids[idx_goal]
        dist = np.linalg.norm(start - goal)
        if min_dist <= dist <= max_dist:
            return start, goal, dist

def main():
    # Load dataset
    dataset = zarr.open_group("./data/scenes/train.zarr", mode='r')
    agents = dataset['agents']
    agents_array = agents[:]
    centroids = np.array([agent['centroid'] for agent in agents_array])

    # Pick random start and goal
    start, goal, dist = pick_start_goal(centroids)
    print(f"Picked Start: {start}")
    print(f"Picked Goal: {goal}")
    print(f"Distance: {dist:.2f} meters")

    # Plan naive straight-line path
    naive_path = plan_naive_path(start, goal, step_size=2.0)

    # Plan sequential MPC path
    optimized_path = sequential_mpc(start, goal, agents, step_size=2.0, replan_horizon=25, max_steps=500)

    # Compute costs
    naive_cost = total_cost(naive_path)
    optimized_cost = total_cost(optimized_path)

    print(f"Naive Path Total Cost: {naive_cost:.2f}")
    print(f"Optimized MPC Path Total Cost: {optimized_cost:.2f}")

    # Plot paths
    plt.figure(figsize=(12, 10))
    plt.plot(naive_path[:,0], naive_path[:,1], 'r--', label='Naive Path')
    plt.plot(optimized_path[:,0], optimized_path[:,1], 'g-', label='Sequential MPC Path')
    plt.scatter([start[0]], [start[1]], c='blue', marker='o', label='Start')
    plt.scatter([goal[0]], [goal[1]], c='purple', marker='*', label='Goal')
    plt.title("Naive vs Optimized Sequential MPC Path")
    plt.xlabel("X position (meters)")
    plt.ylabel("Y position (meters)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    main()
