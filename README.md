# Trajectory Optimization Using Model Predictive Control (MPC)

**Graduate Optimization Project (MSML 604)**  
**University of Maryland-College Park**  
Authors: Haider Khan, Satwika Konda, Harshit Singh, Sivani Mallangi, Prakhar Tiwari  
High-performance experiments executed on **Zaratan High-Performance Computing**, UMD

---

## 📌 Overview

This repository presents a trajectory optimization framework for autonomous vehicles using **Model Predictive Control (MPC)**. The system was built from scratch to operate at **50 Hz**, deploying real-time MPC over geo-referenced aerial maps from the **Lyft Level-5 Motion Prediction dataset**. Unlike reactive or sampling-based planners, our formulation solves a **multi-objective optimization** problem at every timestep, minimizing a custom-defined cost:

<img width="675" alt="Screenshot 2025-05-23 at 9 52 29 PM" src="https://github.com/user-attachments/assets/151b7aea-8f75-4153-a313-b3dfdb335fd5" />


---

## 📊 Dataset

**Lyft Level-5 Motion Prediction Dataset** (LL5-Pred)  
- 1,118 hours of real-world AV logs, 250Hz sampling, annotated actors, HD semantic maps  
- Used **high-resolution aerial raster imagery** to compute off-road cost as pixel intensity  
- Only static-agent scenes selected to isolate planner performance from stochastic prediction

Data preprocessing and scene rendering leveraged **L5Kit** for:
- Actor-centric rasterization  
- Semantic map generation @ 25 cm/pixel  
- Ego-state trajectory extraction  

---

## ⚙️ Methodology
<img width="690" alt="Screenshot 2025-05-23 at 9 58 43 PM" src="https://github.com/user-attachments/assets/97a71a80-a314-4da6-b818-51a55d8de642" />
<img width="832" alt="Screenshot 2025-05-23 at 10 00 00 PM" src="https://github.com/user-attachments/assets/fb0d9386-98f5-4c3a-a563-bcc85f46ddf8" />
<img width="676" alt="Screenshot 2025-05-23 at 10 01 22 PM" src="https://github.com/user-attachments/assets/0a4c660d-5d21-423a-b9ec-15574cc37371" />
<img width="681" alt="Screenshot 2025-05-23 at 10 01 38 PM" src="https://github.com/user-attachments/assets/d299df49-5ba8-4aff-bb5f-1020b45181c5" />


---

## 📈 Results & Plots

### 1. Off-road Penalty Comparison  
<img width="655" alt="Screenshot 2025-05-23 at 10 10 48 PM" src="https://github.com/user-attachments/assets/64aa3de3-90b4-4f9c-a34d-4c6520131c52" />

> MPC reduces off-road incursions by dynamically adjusting trajectory to map constraints. Penalty dropped from constant 250 (naive) to average ~235.

### 2. Cost Distribution  
<img width="690" alt="Screenshot 2025-05-23 at 10 11 42 PM" src="https://github.com/user-attachments/assets/3790f664-12af-400f-953c-b34c3e75b3d1" />

> Variance and median total cost significantly improved under MPC. Tighter interquartile range indicates more **robust planning**.

### 3. Run-wise Total Cost with MPC Advantage  
<img width="634" alt="Screenshot 2025-05-23 at 10 12 13 PM" src="https://github.com/user-attachments/assets/800134e9-588c-437a-bb16-93b348b0d032" />

> In 8 out of 10 simulations, MPC outperformed the naive planner in total cost. Highlighted area shows **cost advantage per run**.

### 4. Off-road Penalty Trends  
<img width="690" alt="Screenshot 2025-05-23 at 10 12 46 PM" src="https://github.com/user-attachments/assets/4f21b333-dff5-425d-86a1-4c4c93e62419" />

> Naive planner always incurs maximum penalty (250). MPC adapts to each scenario to remain on-road, showing clear **trajectory intelligence**.

### 5. Total Cost Trends  
<img width="706" alt="Screenshot 2025-05-23 at 10 13 16 PM" src="https://github.com/user-attachments/assets/95449491-119c-4015-b3b7-7cf8e076cf8c" />

> MPC dynamically re-plans and selects cost-minimizing trajectories, leading to a **mean cost reduction of 75.4 units**.

---

## 🧠 Key Achievements
<img width="762" alt="Screenshot 2025-05-23 at 10 17 52 PM" src="https://github.com/user-attachments/assets/59f7d58c-ffa0-4bee-8807-96b804f3a297" />

- 🚀 Designed and implemented an **MPC planner** from first principles.
- 🌍 Incorporated **geo-referenced aerial maps** as soft constraints for off-road avoidance.
- ⚙️ Executed full pipeline on **Zaratan HPC**, enabling fast iteration and 50Hz inference.
- 🧮 Reduced average total cost by **5.8%**, travel time by **2.9 steps**, and off-road penalty significantly.
- 📊 Visualized all runs with cost breakdowns, distributions, and shaded comparison plots.

---

