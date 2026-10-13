
import os
import icm_utils
from icm_utils import Simulation

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

#Graphing function for demo
def plot_flow_with_peak(flow: pd.Series, title: str,
                        xlabel: str = "Time since start (hours)",
                        ylabel: str = "Flow (MGD)",
                        save_path: str | None = None):
    flow = pd.to_numeric(flow, errors="raise")
    valid_flow = flow.dropna()
    if valid_flow.empty:
        raise ValueError("flow must contain at least one numeric value.")

    peak_time = valid_flow.idxmax()     # index label where the max occurs (hours)
    peak_value = valid_flow.max()

    flow_color = "#1976b9"
    peak_color = "#d9534f"

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="white")
    ax.set_facecolor("white")
    ax.plot(flow.index, flow.values, color=flow_color, linewidth=1.8,
            label="Simulated flow", zorder=2)
    ax.axvline(peak_time, color=peak_color, linewidth=0.9, linestyle=":",
               alpha=0.85, zorder=2)
    ax.plot(peak_time, peak_value, "o", color=peak_color, markersize=6,
            markeredgecolor="white", markeredgewidth=1.2, zorder=4,
            label=f"Peak: {peak_value:.4g}")

    y_top = peak_value * 1.18 if peak_value > 0 else 1
    ax.set_ylim(0, y_top)
    ax.margins(x=0.04)
    x_left, x_right = ax.get_xlim()
    peak_x_fraction = (peak_time - x_left) / (x_right - x_left)
    peak_y_fraction = peak_value / y_top
    place_left = peak_x_fraction > 0.72
    place_below = peak_y_fraction > 0.78
    ax.annotate(
        f"Peak: {peak_value:.4g}\nTime: {peak_time:.4g} h",
        xy=(peak_time, peak_value),
        xytext=(-10 if place_left else 10, -12 if place_below else 12),
        textcoords="offset points",
        ha="right" if place_left else "left",
        va="top" if place_below else "bottom",
        arrowprops=dict(arrowstyle="-", color=peak_color, lw=0.9),
        color="#333333", fontsize=8.5,
        zorder=5)

    ax.set_title(title, fontsize=13, fontweight="bold", loc="left", pad=12,
                 color="#222222")
    ax.set_xlabel(xlabel, fontsize=10, labelpad=7, color="#333333")
    ax.set_ylabel(ylabel, fontsize=10, labelpad=7, color="#333333")
    ax.grid(which="major", color="#d9d9d9", linewidth=0.65)
    ax.grid(axis="y", which="minor", color="#eeeeee", linewidth=0.45)
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#777777")
        spine.set_linewidth(0.8)
    ax.tick_params(axis="both", which="major", colors="#425466",
                   labelsize=9, length=3.5, width=0.7)
    ax.tick_params(axis="y", which="minor", length=2, color="#777777")
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    return fig, ax

#Location of the ICMExchange.exe
config = icm_utils.ICMConfig(exchange_path="C:\\Program Files\\Autodesk\\InfoWorks ICM Ultimate 2026\\ICMExchange.exe")

#Location of the .icmm database file
testing_session = icm_utils.ICMSession(config=config, database_path="C:\\Users\\micha\\Desktop\\Infoworks ICM Testing database\\test_database.icmm")

#List all simulations in the database and print their details
simlist = testing_session.list_simulations()
print("There are " + str(len(simlist)) + " simulations in the database.")
for sim in simlist:
    print(f"Simulation: {sim.run_name} / {sim.sim_name} (ID: {sim.id}) - Status: {sim.status}")

input("Press Enter to continue...")


for sim in simlist:
    results = testing_session.extract_simulation_results(sim,selection=2,attributes=[["link", ["us_flow"]]])
    print(results)
    input("Press Enter to continue...")
    model_flows = results.set_index("Seconds")
    model_flows=model_flows.drop(columns=["Time"])
    model_flows.index = model_flows.index / 3600
    for conduit, model_flow in model_flows.items():
        plot_flow_with_peak(model_flow, title=f"{sim.run_name} / {sim.sim_name}: {conduit}",
                            save_path=f"{sim.run_name}_{sim.sim_name}_{conduit}_plot.png")