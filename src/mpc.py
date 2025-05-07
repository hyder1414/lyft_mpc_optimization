#mpc.py
import numpy as np
from src.cost_function import total_cost

def plan_naive_path(start, goal, num_steps=50):
    """Simple straight-line interpolation."""
    path = np.linspace(start, goal, num_steps)
    return path

def sequential_mpc(start, goal, agents, step_size=20.0, horizon=50):     #Haider's version
    """Very basic MPC: plan small steps toward goal minimizing total cost."""
    path = []
    current = np.array(start)

    for _ in range(horizon):
        direction = goal - current
        direction = direction / np.linalg.norm(direction)  # normalize
        candidates = []

        for delta in np.linspace(-np.pi/18, np.pi/18, 5):  # small yaw variations
            rotation_matrix = np.array([
                [np.cos(delta), -np.sin(delta)],
                [np.sin(delta), np.cos(delta)]
            ])
            move = rotation_matrix @ direction
            next_point = current + step_size * move
            candidates.append(next_point)

        candidates = np.array(candidates)
        costs = []

        for cand in candidates:
            fake_path = np.vstack([path, cand]) if path else np.array([cand])
            total, _, _, _ = total_cost(fake_path)  # ⬅️ Catch all outputs, use only `total`
            costs.append(total)

        best_idx = np.argmin(costs)
        best_next = candidates[best_idx]

        path.append(best_next)
        current = best_next

        if np.linalg.norm(current - goal) < 20.0:
            break

    return np.array(path)
    
def sequential_mpc_optimized(start, goal, agents, step_size=20.0, horizon=50, lambda_heuristic=1.0):  #Satwika's version
    path = []
    current = np.array(start)
    total_dist = np.linalg.norm(goal - start)

    for _ in range(horizon):
        direction = goal - current
        direction = direction / np.linalg.norm(direction)
        candidates = []

        for delta in np.linspace(-np.pi/6, np.pi/6, 9):  # wider range and more samples
            rotation_matrix = np.array([
                [np.cos(delta), -np.sin(delta)],
                [np.sin(delta), np.cos(delta)]
            ])
            move = rotation_matrix @ direction
            next_point = current + step_size * move
            candidates.append(next_point)

        costs = []
        for cand in candidates:
            fake_path = np.vstack([path, cand]) if path else np.array([cand])
            path_cost, _, _, _ = total_cost(fake_path)
            heuristic = lambda_heuristic * np.linalg.norm(cand - goal)
            costs.append(path_cost + heuristic)

        best_idx = np.argmin(costs)
        best_next = candidates[best_idx]
        path.append(best_next)
        current = best_next

        if np.linalg.norm(current - goal) < step_size:
            break

    return np.array(path)
