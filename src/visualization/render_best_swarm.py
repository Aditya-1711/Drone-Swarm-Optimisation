
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib.lines as mlines

def render_best_swarm(history, targets, obstacles=None,
                      out_name="outputs/best_swarm.mp4"):

    history = np.asarray(history)
    targets = np.asarray(targets)[:, :2]

    W = 50
    DRONE_SIZE = 120
    TARGET_SIZE = 140

    fig, ax = plt.subplots(figsize=(8,8), dpi=120)

    ax.set_xlim(0, W)
    ax.set_ylim(0, W)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title("Best Swarm Convergence", fontsize=14, pad=12)

    # HUD
    hud = ax.text(
        0.02, 0.98, "",
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=11,
        bbox=dict(facecolor="white", alpha=0.9, boxstyle="round")
    )

    # Symbol index legend
    drone_handle = mlines.Line2D([], [], color="tab:blue", marker="o",
                                 linestyle="None", markersize=8,
                                 label="Drone")

    target_handle = mlines.Line2D([], [], color="red", marker="X",
                                  linestyle="None", markersize=8,
                                  label="Target")

    obstacle_handle = mlines.Line2D([], [], color="black", marker="o",
                                    linestyle="None", markersize=8,
                                    markerfacecolor="none",
                                    label="Obstacle")

    ax.legend(
        handles=[drone_handle, target_handle, obstacle_handle],
        loc="upper right",
        framealpha=0.95,
        title="Symbol Index"
    )

    # Initial swarm
    p0 = history[0][:, :2]

    drone_scatter = ax.scatter(
        p0[:,0], p0[:,1],
        s=DRONE_SIZE,
        color="tab:blue",
        edgecolors="black",
        zorder=5
    )

    target_scatter = ax.scatter(
        targets[:,0], targets[:,1],
        s=TARGET_SIZE,
        marker="X",
        color="red",
        zorder=6
    )

    # obstacles
    if obstacles is not None:
        for ox, oy, r in obstacles:
            circ = plt.Circle((ox, oy), r,
                              fill=False,
                              edgecolor="black",
                              linewidth=2)
            ax.add_patch(circ)

    def draw(i):
        pos = history[i][:, :2]
        drone_scatter.set_offsets(pos)

        hud.set_text(
            f"Iteration: {i+1}/{len(history)}\n"
            f"Drones: {len(pos)}"
        )

        return drone_scatter, hud

    anim = FuncAnimation(
        fig, draw,
        frames=len(history),
        interval=40,
        blit=True
    )

    writer = FFMpegWriter(fps=10)
    anim.save(out_name, writer=writer)
    plt.close(fig)

    print("Saved:", out_name)
