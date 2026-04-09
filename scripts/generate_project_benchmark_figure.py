from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


BENCHMARKS = ["mk", "la (r)", "la (e)", "la (v)"]
BASELINE = np.array([184.40, 1030.83, 1175.53, 944.85])
SOLVER = np.array([178.10, 961.53, 1059.05, 926.45])
ORTOOLS = np.array([173.90, 933.53, 1026.80, 920.40])


def annotate_bars(ax, bars, values):
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.018,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#31465d",
        )


def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "assets" / "benchmark-comparison.png"

    colors = {
        "baseline": "#B8C0CA",
        "solver": "#3E86C6",
        "solver_edge": "#215C92",
        "or": "#57B89C",
        "or_edge": "#2B856B",
        "accent": "#24384B",
        "grid": "#D8E0E7",
        "bg": "#FBFCFE",
    }

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 15,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(11.6, 4.8),
        dpi=220,
        gridspec_kw={"width_ratios": [1.6, 1.0]},
    )
    fig.patch.set_facecolor(colors["bg"])

    x = np.arange(len(BENCHMARKS))
    width = 0.24

    ax = axes[0]
    ax.set_facecolor("white")
    bars_base = ax.bar(
        x - width,
        BASELINE,
        width,
        label="Best RL Baseline",
        color=colors["baseline"],
        edgecolor="#8C99A6",
        linewidth=1.0,
    )
    bars_solver = ax.bar(
        x,
        SOLVER,
        width,
        label="RL Solver",
        color=colors["solver"],
        edgecolor=colors["solver_edge"],
        linewidth=1.1,
    )
    bars_or = ax.bar(
        x + width,
        ORTOOLS,
        width,
        label="OR-Tools",
        color=colors["or"],
        edgecolor=colors["or_edge"],
        linewidth=1.1,
    )

    annotate_bars(ax, bars_solver, SOLVER)
    annotate_bars(ax, bars_or, ORTOOLS)

    ax.set_title("A. Average makespan across benchmark families", loc="left", color=colors["accent"], pad=14)
    ax.set_ylabel("Average makespan")
    ax.set_xticks(x)
    ax.set_xticklabels(BENCHMARKS)
    ax.grid(axis="y", color=colors["grid"], linewidth=0.8, alpha=0.9)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#A5B1BC")
    ax.spines["bottom"].set_color("#A5B1BC")
    ax.legend(loc="upper left", frameon=False, ncol=3, bbox_to_anchor=(0.0, 1.02))

    ax2 = axes[1]
    ax2.set_facecolor("white")
    baseline_gap = (BASELINE - ORTOOLS) / ORTOOLS * 100
    solver_gap = (SOLVER - ORTOOLS) / ORTOOLS * 100
    y = np.arange(len(BENCHMARKS))

    ax2.hlines(y, solver_gap, baseline_gap, color="#B9C5D0", linewidth=3.0, zorder=1)
    ax2.scatter(baseline_gap, y, s=92, color=colors["baseline"], edgecolor="#8C99A6", linewidth=1.0, zorder=3, label="Best RL Baseline")
    ax2.scatter(solver_gap, y, s=96, color=colors["solver"], edgecolor=colors["solver_edge"], linewidth=1.0, zorder=4, label="RL Solver")

    for gap, yi in zip(solver_gap, y):
        ax2.text(gap - 0.1, yi + 0.16, f"{gap:.1f}%", ha="right", va="bottom", fontsize=9, color=colors["solver_edge"])

    ax2.set_title("B. Gap to OR-Tools", loc="left", color=colors["accent"], pad=14)
    ax2.set_xlabel("Relative gap (%)")
    ax2.set_yticks(y)
    ax2.set_yticklabels(BENCHMARKS)
    ax2.invert_yaxis()
    ax2.grid(axis="x", color=colors["grid"], linewidth=0.8, alpha=0.9)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_color("#A5B1BC")

    max_gap = max(float(baseline_gap.max()), float(solver_gap.max()))
    ax2.set_xlim(0, max_gap * 1.18)

    fig.suptitle(
        "Benchmark performance summary for the RL solver",
        fontsize=17,
        fontweight="bold",
        color=colors["accent"],
        y=1.02,
    )

    fig.text(
        0.015,
        -0.02,
        "Values are summarized from the CDC 2025 paper. Lower is better in both panels.",
        fontsize=10,
        color="#627181",
    )

    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")


if __name__ == "__main__":
    main()
