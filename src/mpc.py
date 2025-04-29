import numpy as np
from src.cost_function import total_cost

def sequential_mpc(start, goal, agents, step_size=2.0, replan_horizon=25, max_steps=100):
    """
    Sequential MPC: Plan small horizons repeatedly until reaching the goal.
    """
    path = []
    current_pos = np.array(start)
    yaw = np.arctan2(goal[1] - start[1], goal[0] - start[0])

    for _ in range(max_steps):
        sub_path = []
        x, y = current_pos
        for _ in range(replan_horizon):
            x += step_size * np.cos(yaw)
            y += step_size * np.sin(yaw)
            sub_path.append((x, y))
        
        sub_path = np.array(sub_path)
        path.extend(sub_path)

        current_pos = sub_path[-1]

        # Check distance to goal
        if np.linalg.norm(current_pos - goal) < 20.0:
            break

        # Recompute yaw direction toward goal
        yaw = np.arctan2(goal[1] - current_pos[1], goal[0] - current_pos[0])

    return np.array(path)

def plan_naive_path(start, goal, step_size=2.0):
    """
    Simple straight-line planner from start to goal.
    """
    start = np.array(start)
    goal = np.array(goal)
    direction = goal - start
    distance = np.linalg.norm(direction)
    if distance == 0:
        return np.array([start])

    direction /= distance  # normalize
    n_steps = int(distance / step_size)

    path = np.array([start + direction * step_size * i for i in range(n_steps + 1)])
    return path
