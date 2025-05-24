
# 🚗 Trajectory Optimization for Autonomous Vehicles Using Model Predictive Control (MPC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

> **Authors:** Haider Khan, Satwika Konda, Harshit Singh, Sivani Mallangi, Prakhar P. Tiwari  
> **Affiliation:** University of Maryland — MSML604 Project (Spring 2025)  
> **GitHub:** [hyder1414/lyft_mpc_optimization](https://github.com/hyder1414/lyft_mpc_optimization)

---

## 🧠 Problem Formulation

We consider the classical **finite-horizon optimal control** problem in a 2D state space:

\[
\begin{align*}
\mathbf{x}_{k+1} &= \mathbf{x}_k + \mathbf{u}_k \\
J(P) &= T \cdot \Delta s + \lambda_1 \sum_{k=1}^T \mathbb{1}[d(\mathbf{x}_k, \mathcal{A}) < r] + \lambda_2 \sum_{k=1}^T \mathcal{I}_\text{off}(\mathbf{x}_k)
\end{align*}
\]

Where:
- \( \mathbf{x}_k \in \mathbb{R}^2 \): vehicle position at time \( k \)
- \( \mathbf{u}_k \in \mathbb{R}^2 \): control input
- \( \mathcal{A} \): static agent set
- \( \mathcal{I}_\text{off} \): binary off-road indicator from geo-referenced aerial map
- \( \lambda_1 = 1.0, \lambda_2 = 2.0 \)

The control policy is defined by:

\[
\mathbf{u}_k^\ast = \arg\min_{\mathbf{u}_k \in \mathcal{U}} J(P)
\]

---

## 💡 Methodology

### 🔁 MPC Loop
Each timestep, the system:
1. Samples candidate heading vectors \( \theta_i \in [-30^\circ, +30^\circ] \)
2. Simulates corresponding paths \( P_i \)
3. Computes total cost \( J(P_i) \)
4. Selects \( \mathbf{u}_k^\ast = \arg\min J(P_i) \)
5. Repeats at 50 Hz

### 📦 Data + Compute
- **Dataset**: Lyft Level-5 Motion Prediction
- **Execution**: UMD Zaratan HPC
- **Sim Rate**: 50 Hz
- **Planning Horizon**: \( T \leq 50 \)

---

## 📊 Results

### 📈 Boxplot of Total Cost
![boxplot_total_cost](assets/boxplot_total_cost.png)

> **Interpretation:** MPC yields lower mean and variance in cost.

### 🛣️ Off-Road Penalty Distribution
![barplot_offroad_penalty](assets/barplot_offroad_penalty.png)

> MPC reduces off-road violations using aerial map constraints.

### 🟢 Per-run Cost: MPC vs Naive
![total_cost_comparison](assets/total_cost_comparison.png)

> Naive remains constant (red), MPC dynamically optimizes (green).

### 🌍 Per-run Off-Road Penalty
![offroad_penalty_comparison](assets/offroad_penalty_comparison.png)

> MPC stays on the road, avoiding constant penalties.

### ✅ Shaded Area = MPC Win Zone
![lineplot_total_cost_shaded_fixed](assets/lineplot_total_cost_shaded_fixed.png)

> In 8/10 runs, MPC achieves superior total cost (green region).

---

## 🧪 Run Locally

```bash
git clone https://github.com/hyder1414/lyft_mpc_optimization.git
cd lyft_mpc_optimization
pip install -r requirements.txt

python run_batch_mpc_simulation.py
python analyze_batch_results.py
```

---

## 🧾 PDF Report + Presentation

- [📄 IEEE-style Report (PDF)](./IEEE_Conference_Optimization_MPC.pdf)  
- [📊 MSML604 Presentation (Slides)](./MSML604%20Presentation%20(2).pdf)

---

## 📚 Citation

```bibtex
@misc{haider2025mpc,
  title={Trajectory Optimization for Autonomous Vehicles Using Model Predictive Control},
  author={Khan, Haider and others},
  year={2025},
  howpublished={\url{https://github.com/hyder1414/lyft_mpc_optimization}},
  note={MSML604 Course Project}
}
```
