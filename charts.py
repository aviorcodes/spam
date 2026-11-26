import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import config as C

# Global dark style — matches the app theme
plt.rcParams.update({
    "figure.facecolor":  C.BG_PANEL,
    "axes.facecolor":    C.BG_PANEL,
    "savefig.facecolor": C.BG_PANEL,
    "axes.edgecolor":    C.BORDER,
    "axes.labelcolor":   C.TEXT,
    "xtick.color":       C.TEXT_MUTED,
    "ytick.color":       C.TEXT_MUTED,
    "text.color":        C.TEXT,
    "grid.color":        C.BORDER,
    "grid.alpha":        0.4,
    "font.family":       "Segoe UI",
    "font.size":         9,
})


def _embed(fig, parent):
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas


def subject_bar(parent, stats):
    """Bar chart of subject-wise class averages."""
    fig, ax = plt.subplots(figsize=(5.2, 3.0), dpi=90)
    subjects = list(stats["subject_avg"].keys())
    values   = list(stats["subject_avg"].values())
    colors   = plt.cm.plasma(np.linspace(0.2, 0.9, len(subjects)))
    bars = ax.bar(subjects, values, color=colors,
                  edgecolor=C.BORDER, linewidth=0.8)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.0f}",
                ha="center", color=C.TEXT, fontsize=8, fontweight="bold")
    ax.set_title("Subject-Wise Averages", color=C.TEXT,
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_ylim(0, 115)
    ax.grid(axis="y", linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    _embed(fig, parent)
    return fig


def pass_pie(parent, stats):
    """Pie chart of pass vs fail distribution."""
    fig, ax = plt.subplots(figsize=(4.2, 3.0), dpi=90)
    p = stats["pass_rate"]
    f = 100 - p
    if p + f == 0:
        ax.text(0.5, 0.5, "No Data", ha="center", color=C.TEXT_MUTED)
    else:
        ax.pie([p, f],
               labels=[f"Pass\n{p:.1f}%", f"Fail\n{f:.1f}%"],
               colors=[C.SUCCESS, C.DANGER],
               startangle=90,
               wedgeprops={"edgecolor": C.BG_PANEL, "linewidth": 2},
               textprops={"color": C.TEXT, "fontsize": 10, "weight": "bold"})
    ax.set_title("Pass / Fail", color=C.TEXT, fontsize=11,
                 fontweight="bold", pad=10)
    fig.tight_layout()
    _embed(fig, parent)
    return fig


def top_students_bar(parent, df, top_n=8):
    """Horizontal bar chart of top students by total marks."""
    fig, ax = plt.subplots(figsize=(5.5, 3.0), dpi=90)
    top = df.sort_values("total", ascending=False).head(top_n)
    if top.empty:
        fig.tight_layout()
        _embed(fig, parent)
        return fig
    names  = top["name"].tolist()[::-1]
    totals = top["total"].tolist()[::-1]
    bars = ax.barh(names, totals, color=C.ACCENT,
                   edgecolor=C.ACCENT_3, linewidth=0.8)
    for b, v in zip(bars, totals):
        ax.text(v - 10, b.get_y() + b.get_height()/2, str(int(v)),
                va="center", ha="right", color="white",
                fontsize=8, fontweight="bold")
    ax.set_title(f"Top {len(top)} Students", color=C.TEXT,
                 fontsize=11, fontweight="bold", pad=10)
    ax.grid(axis="x", linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    _embed(fig, parent)
    return fig


def radar_student(parent, student, subjects):
    """Radar chart of a single student's subject profile."""
    labels = subjects
    values = [student[s.lower()] for s in subjects]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(4.5, 3.4), dpi=90)
    ax  = fig.add_subplot(111, polar=True)
    ax.set_facecolor(C.BG_PANEL)
    ax.plot(angles, values, color=C.ACCENT_3, linewidth=2)
    ax.fill(angles, values, color=C.ACCENT, alpha=0.35)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=C.TEXT, fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"],
                       color=C.TEXT_DIM, fontsize=7)
    ax.grid(color=C.BORDER, alpha=0.5)
    ax.set_title(f"{student['name']} — Subject Profile",
                 color=C.TEXT, fontsize=11, fontweight="bold", pad=15)
    fig.tight_layout()
    _embed(fig, parent)
    return fig