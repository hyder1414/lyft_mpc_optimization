# analyze_batch_results.py
import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_results(csv_path):
    os.makedirs("results/plots", exist_ok=True)

    df = pd.read_csv(csv_path)

    print("\n====== Summary Statistics ======")
    print(f"Number of paths evaluated: {len(df)}")

    # Average total costs
    naive_mean = df['naive_total'].mean()
    mpc_mean = df['mpc_total'].mean()

    print(f"\nAverage Total Cost:")
    print(f" - Naive: {naive_mean:.2f}")
    print(f" - MPC  : {mpc_mean:.2f}")

    # Win rate
    wins = (df['mpc_total'] < df['naive_total']).sum()
    win_rate = wins / len(df) * 100
    print(f"\nMPC beats Naive in {wins}/{len(df)} cases ({win_rate:.1f}%)")

    # Plot total cost comparison
    plt.figure(figsize=(10,6))
    plt.hist(df['naive_total'], bins=10, alpha=0.5, label="Naive", color='red')
    plt.hist(df['mpc_total'], bins=10, alpha=0.5, label="MPC", color='green')
    plt.xlabel("Total Cost")
    plt.ylabel("Count")
    plt.title("Total Cost Distribution (Naive vs MPC)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/plots/total_cost_distribution.png")
    plt.close()

    # Travel time comparison
    plt.figure(figsize=(10,6))
    plt.hist(df['naive_travel_time'], bins=10, alpha=0.5, label="Naive Travel Time", color='blue')
    plt.hist(df['mpc_travel_time'], bins=10, alpha=0.5, label="MPC Travel Time", color='cyan')
    plt.xlabel("Travel Time")
    plt.ylabel("Count")
    plt.title("Travel Time Distribution")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/plots/travel_time_distribution.png")
    plt.close()

    # Collision comparison
    plt.figure(figsize=(10,6))
    plt.hist(df['naive_collision'], bins=10, alpha=0.5, label="Naive Collisions", color='orange')
    plt.hist(df['mpc_collision'], bins=10, alpha=0.5, label="MPC Collisions", color='purple')
    plt.xlabel("Collisions")
    plt.ylabel("Count")
    plt.title("Collision Distribution")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/plots/collision_distribution.png")
    plt.close()

    # Offroad penalty comparison
    plt.figure(figsize=(10,6))
    plt.hist(df['naive_offroad'], bins=10, alpha=0.5, label="Naive Offroad Penalty", color='pink')
    plt.hist(df['mpc_offroad'], bins=10, alpha=0.5, label="MPC Offroad Penalty", color='brown')
    plt.xlabel("Offroad Penalty")
    plt.ylabel("Count")
    plt.title("Offroad Penalty Distribution")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/plots/offroad_distribution.png")
    plt.close()

    print("\n✅ Analysis done. Plots saved to results/plots/.")

if __name__ == "__main__":
    analyze_results("results/logs/batch_results.csv")
