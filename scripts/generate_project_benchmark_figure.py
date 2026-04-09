from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


BENCHMARKS = ["mk", "la (r)", "la (e)", "la (v)"]
BASELINE = np.array([184.40, 1030.83, 1175.53, 944.85])
SOLVER = np.array([178.10, 961.53, 1059.05, 926.45])
ORTOOLS = np.array([173.90, 933.53, 1026.80, 920.40])


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#aab4bf")
    ax.spines["bottom"].set_color("#aab4bf")
    ax.tick_params(colors="#223548", labelsize=10)


def add_value_labels(ax, bars, values, color):
    offset = max(values) * 0.015
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + offset,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color=color,
        )


def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "assets" / "benchmark-comparison.png"

    baseline_ratio = BASELINE / BASELINE
    solver_ratio = SOLVER / BASELINE
    or_ratio = ORTOOLS / BASELINE
    solver_gap = (SOLVER - ORTOOLS) / ORTOOLS * 100
    baseline_gap = (BASELINE - ORTOOLS) / ORTOOLS * 100

    colors = {
        "ink": "#1e2f3f",
        "muted": "#6b7886",
        "grid": "#dde3ea",
        "baseline_fill": "#d6dce3",
        "baseline_edge": "#9aa6b2",
        "solver_fill": "#4f84b8",
        "solver_edge": "#2f618f",
        "or_fill": "#7eb49a",
        "or_edge": "#4d8a72",
        "paper": "#ffffff",
        "bg": "#fbfcfd",
    }

    plt.rcParams.update(
        {
            "font.family": "STIXGeneral",
            "axes.labelsize": 11,
            "axes.titlesize": 12.5,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "mathtext.fontset": "stix",
        }
    )

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(10.6, 4.0),
        dpi=260,
        gridspec_kw={"width_ratios": [1.45, 1.0]},
    )
    fig.patch.set_facecolor(colors["bg"])

    x = np.arange(len(BENCHMARKS))
    width = 0.22

    ax1 = axes[0]
    ax1.set_facecolor(colors["paper"])
    bars_base = ax1.bar(
        x - width,
        BASELINE,
        width=width,
        color=colors["baseline_fill"],
        edgecolor=colors["baseline_edge"],
        linewidth=0.9,
        label="Best RL Baseline",
        zorder=3,
    )
    bars_solver = ax1.bar(
        x,
        SOLVER,
        width=width,
        color=colors["solver_fill"],
        edgecolor=colors["solver_edge"],
        linewidth=0.9,
        label="RL Solver",
        zorder=3,
    )
    bars_or = ax1.bar(
        x + width,
        ORTOOLS,
        width=width,
        color=colors["or_fill"],
        edgecolor=colors["or_edge"],
        linewidth=0.9,
        label="OR-Tools",
        zorder=3,
    )

    add_value_labels(ax1, bars_solver, SOLVER, colors["solver_edge"])
    add_value_labels(ax1, bars_or, ORTOOLS, colors["or_edge"])

    ax1.set_title("A  Average makespan", loc="left", color=colors["ink"], pad=10)
    ax1.set_ylabel("Average makespan", color=colors["ink"])
    ax1.set_xticks(x)
    ax1.set_xticklabels(BENCHMARKS)
    ax1.grid(axis="y", color=colors["grid"], linewidth=0.8, zorder=0)
    ax1.set_axisbelow(True)
    style_axis(ax1)
    legend = ax1.legend(
        loc="upper left",
        ncol=3,
        frameon=True,
        fontsize=9.5,
        handlelength=1.4,
        columnspacing=1.2,
        borderpad=0.4,
        bbox_to_anchor=(0.0, 1.0),
    )
    legend.get_frame().set_facecolor("#ffffff")
    legend.get_frame().set_edgecolor("#d5dce4")
    legend.get_frame().set_linewidth(0.8)

    ax2 = axes[1]
    ax2.set_facecolor(colors["paper"])
    line_y = np.arange(len(BENCHMARKS))
    ax2.axvline(1.0, color="#c5ced8", linewidth=1.0, linestyle=(0, (3, 3)), zorder=1)
    ax2.hlines(line_y, or_ratio, baseline_ratio, color="#c0cad4", linewidth=2.0, zorder=2)
    ax2.scatter(baseline_ratio, line_y, s=62, color=colors["baseline_fill"], edgecolor=colors["baseline_edge"], linewidth=0.9, zorder=3)
    ax2.scatter(solver_ratio, line_y, s=66, color=colors["solver_fill"], edgecolor=colors["solver_edge"], linewidth=0.9, zorder=4)
    ax2.scatter(or_ratio, line_y, s=62, color=colors["or_fill"], edgecolor=colors["or_edge"], linewidth=0.9, zorder=3)

    for y_value, solver_value, improvement in zip(line_y, solver_ratio, baseline_gap - solver_gap):
        ax2.text(
            solver_value + 0.004,
            y_value + 0.16,
            f"-{improvement:.1f} pts",
            ha="left",
            va="bottom",
            fontsize=8.8,
            color=colors["solver_edge"],
        )

    ax2.set_title("B  Normalized performance", loc="left", color=colors["ink"], pad=10)
    ax2.set_xlabel("Normalized makespan (lower is better)", color=colors["ink"])
    ax2.set_yticks(line_y)
    ax2.set_yticklabels(BENCHMARKS)
    ax2.invert_yaxis()
    ax2.grid(axis="x", color=colors["grid"], linewidth=0.8, zorder=0)
    ax2.set_axisbelow(True)
    ax2.set_xlim(0.88, 1.01)
    style_axis(ax2)
    ax2.spines["left"].set_visible(False)

    fig.text(
        0.012,
        -0.01,
        "Figure generated from the reported averages in the CDC 2025 paper. Panel B highlights the reduction in gap to OR-Tools.",
        fontsize=9.5,
        color=colors["muted"],
    )

    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())


if __name__ == "__main__":
    main()
