# Self-contained demo: simulate self-assessment profiles and plot a skills roadmap.
import os

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COMPETENCIES = [
    "programming",
    "statistics",
    "genomics",
    "data_wrangling",
    "visualisation",
    "communication",
    "reproducibility",
]

IMPORTANCE = np.array([0.8, 0.9, 0.7, 0.6, 0.6, 0.9, 0.8])


def simulate_profile(seed):
    # Generate a plausible beginner-to-intermediate current profile and a target.
    rng = np.random.default_rng(seed)
    current = np.clip(rng.normal(loc=5.0, scale=1.8, size=len(COMPETENCIES)), 0, 10)
    target = np.clip(current + rng.uniform(1.0, 4.0, size=len(COMPETENCIES)), 0, 10)
    return np.round(current, 1), np.round(target, 1)


def priority(current, target, importance):
    gap = np.clip(target - current, 0, None)
    return gap * importance


def main():
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    current, target = simulate_profile(seed=42)
    prio = priority(current, target, IMPORTANCE)

    df = pd.DataFrame(
        {
            "competency": COMPETENCIES,
            "current": current,
            "target": target,
            "importance": IMPORTANCE,
            "priority": np.round(prio, 3),
        }
    ).sort_values("priority", ascending=False).reset_index(drop=True)

    df.to_csv(os.path.join("results", "summary.csv"), index=False)

    fig = plt.figure(figsize=(12, 5))

    # Radar chart of current vs target.
    n = len(COMPETENCIES)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    ax1 = fig.add_subplot(1, 2, 1, polar=True)
    cur = current.tolist() + [current[0]]
    tgt = target.tolist() + [target[0]]
    ax1.plot(angles, cur, color="#1f77b4", label="current")
    ax1.fill(angles, cur, color="#1f77b4", alpha=0.25)
    ax1.plot(angles, tgt, color="#d62728", label="target")
    ax1.fill(angles, tgt, color="#d62728", alpha=0.10)
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(COMPETENCIES, fontsize=8)
    ax1.set_ylim(0, 10)
    ax1.set_title("Competency radar")
    ax1.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=8)

    # Ranked priority bar chart.
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.barh(df["competency"][::-1], df["priority"][::-1], color="#2ca02c")
    ax2.set_xlabel("weighted priority (gap x importance)")
    ax2.set_title("What to learn next")

    fig.tight_layout()
    fig.savefig(os.path.join("figures", "demo.png"), dpi=120)
    print("Top priority:", df.iloc[0]["competency"])
    print("Wrote figures/demo.png and results/summary.csv")


if __name__ == "__main__":
    main()
