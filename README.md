
---

# MPC Optimization Project

### Project Overview
We perform **path optimization** between random start and goal points using:
- **Baseline (Naive straight-line paths)**
- **Optimized (MPC - Model Predictive Control)**

We optimize based on a **custom cost function** that includes:
- Travel Time
- Collision Risk (simulated)
- Off-Road Penalty (real aerial map-based)

The goal is to show that **MPC** improves over **Naive** path planning by minimizing total cost.

---

### Objective Function

The **optimization objective** we use is:

$$
\text{Total Cost} = \text{Travel Time} + \lambda_{\text{collision}} \times \text{Collision Risk} + \lambda_{\text{offroad}} \times \text{Off-road Penalty}
$$

Where:
- **Travel Time**: Proportional to number of path steps.
- **Collision Risk**: (Simulated / faked) number of likely collisions.
- **Off-road Penalty**: Based on map brightness (penalty if off the road).

**λ values**:
- $\lambda_{\text{collision}}$ = 1.0 (penalty per collision)
- $\lambda_{\text{offroad}}$ = 2.0 (penalty per off-road pixel)

---

### File Structure
| File/Folder | Purpose |
|:------------|:--------|
| `run_mpc_simulation.py` | Runs a single random start-goal simulation (for testing/debugging). |
| `run_batch_mpc_simulation.py` | Runs **10 random simulations** in batch and saves results + plots. |
| `analyze_batch_results.py` | Analyzes batch results, prints summary statistics, saves graphs. |
| `src/` | Contains code modules: `mpc.py`, `cost_function.py`, `data_loader.py`, `utils.py`, etc. |
| `results/logs/batch_results.csv` | CSV log of the batch run (costs for Naive vs MPC paths). |
| `results/plots/` | Saved path plots for each simulation. |

---

### How to Run
**(On Zaratan HPC)**

1. Load environment:
    ```bash
    source venv/bin/activate
    ```

2. Run batch simulation:
    ```bash
    python run_batch_mpc_simulation.py
    ```

3. Analyze batch results:
    ```bash
    python analyze_batch_results.py
    ```

4. Download `results/` folder to your local machine if needed (for reports/plots).

---

### Dataset
- **Source**: [Lyft Motion Prediction for Autonomous Vehicles (Kaggle Competition)](https://www.kaggle.com/competitions/lyft-motion-prediction-autonomous-vehicles/data)
- **Downloaded Files Used**:
  - `scenes/sample.zarr`
  - `scenes/scenes.json`
  - `aerial_map/aerial_map.png`
- **Note**: We **did not use the full dataset** (e.g., no need for `agents`, `traffic_lights`, `timestamps`, etc.).  
  Only the above three were necessary for loading scenes, frames, and basic ego vehicle information.

---

### Notes
- Code was **tested and run** on **Zaratan HPC** (University of Maryland).
- **Python version**: 3.6 (Zaratan default).
- **Key packages**: `matplotlib`, `numpy`, `Pillow`, `zarr`, `pandas`.

---

### Scaling Up (Optional)
To run a **larger batch** (like 100 simulations instead of 10), **edit**:
```python
batch_size = 100
```
inside `run_batch_mpc_simulation.py`.

---

