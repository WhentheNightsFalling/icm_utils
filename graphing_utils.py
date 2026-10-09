import pandas as pd
import matplotlib.pyplot as plt

def plot_flow_with_peak(flow: pd.Series, title: str,
                        xlabel: str = "Time since start (hours)",
                        ylabel: str = "Flow (m³/s)",
                        save_path: str | None = None):
    peak_time = flow.idxmax()     # index label where the max occurs (hours)
    peak_value = flow.max()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(flow.index, flow.values, color="#1f4e79", linewidth=1.8,
            label="Simulated flow")
    ax.plot(peak_time, peak_value, "o", color="#c0392b", markersize=8, zorder=5,
            label=f"Peak: {peak_value:.4f}")
    ax.annotate(f"Peak {peak_value:.4f}\nat t = {peak_time:.2f} h",
                xy=(peak_time, peak_value),
                xytext=(30, -10), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#c0392b"),
                color="#c0392b", fontsize=10)

    ax.set_title(title, fontsize=14, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    return fig, ax