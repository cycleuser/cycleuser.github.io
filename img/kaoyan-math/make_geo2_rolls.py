import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from PIL import Image
import os, shutil

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY, BROWN, CREAM = "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230", "#d8c9b4"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5
T = 12.0
SCRATCH = os.environ.get("JCODE_SCRATCH_DIR", "/tmp")

# ============ 图 A：星形线内摆线滚动 gif（图 6.20）============
R, r = 4.0, 1.0
k = (R - r) / r
t_all = np.linspace(0, 2*np.pi, 800)
X = (R - r)*np.cos(t_all) + r*np.cos(k*t_all)
Y = (R - r)*np.sin(t_all) - r*np.sin(k*t_all)
frames = []
th = np.linspace(0, 2*np.pi, 200)
N_FRAMES = 60
for i in range(N_FRAMES):
    tt = 2*np.pi * i / N_FRAMES
    fig, ax = plt.subplots(figsize=(6.4, 6.0), dpi=120)
    ax.set_xlim(-5.3, 5.3); ax.set_ylim(-5.3, 5.3)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp_ in ax.spines.values():
        sp_.set_color("#cccccc")
    ax.plot(R*np.cos(th), R*np.sin(th), color="#c9a887", lw=1.8, ls="--")
    drawn = t_all <= tt + 1e-9
    ax.plot(X[drawn], Y[drawn], color=BLUE, lw=2.2)
    trail = np.linspace(max(0, tt - 0.6), tt, 40)
    XT = (R - r)*np.cos(trail) + r*np.cos(k*trail)
    YT = (R - r)*np.sin(trail) - r*np.sin(k*trail)
    ax.plot(XT, YT, color=RED, lw=3.0, alpha=0.9)
    cx, cy = (R - r)*np.cos(tt), (R - r)*np.sin(tt)
    circ = Circle((cx, cy), r, fill=False, edgecolor=ORANGE, lw=2.2, zorder=6)
    ax.add_patch(circ)
    ax.plot([cx], [cy], "o", color=ORANGE, ms=5, zorder=7)
    # 小圆内半径线 + 定点
    px, py = cx + r*np.cos(-k*tt), cy + r*np.sin(-k*tt)
    ax.plot([cx, px], [cy, py], color=GREY, lw=1.0, ls=":", zorder=6)
    ax.plot([px], [py], "o", color=RED, ms=7, zorder=8)
    ax.text(-5.0, 4.55, "$t=%.2f$" % tt, fontsize=F-1, color=INK)
    ax.set_title("星形线：小圆在大圆内壁滚动（$R=4r$）", fontsize=T-1, color=INK, pad=8)
    fig.tight_layout()
    fp = os.path.join(SCRATCH, "f_astroid_%03d.png" % i)
    fig.savefig(fp, dpi=120); plt.close(fig)
    frames.append(Image.open(fp).convert("P", palette=Image.ADAPTIVE))
frames[0].save(BASE + "geo2-astroid-roll.gif", save_all=True, append_images=frames[1:],
               duration=70, loop=0, optimize=True)
for i in range(N_FRAMES):
    os.remove(os.path.join(SCRATCH, "f_astroid_%03d.png" % i))
print("ok astroid gif")

# ============ 图 B：内摆线 R=3r/4r/5r 三档 gif（图 6.21）============
from PIL import Image as PImage
def make_hypo(R, r, N_FRAMES=60, dur=70):
    k = (R - r) / r
    t_all = np.linspace(0, 2*np.pi*k + 0.0001, 900)
    X = (R - r)*np.cos(t_all) + r*np.cos(k*t_all)
    Y = (R - r)*np.sin(t_all) - r*np.sin(k*t_all)
    frames = []
    th = np.linspace(0, 2*np.pi, 200)
    span = 2*np.pi*k
    for i in range(N_FRAMES):
        tt = span * i / N_FRAMES
        fig, ax = plt.subplots(figsize=(5.6, 5.3), dpi=110)
        lim = R + 0.6
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        for sp_ in ax.spines.values():
            sp_.set_color("#cccccc")
        ax.plot(R*np.cos(th), R*np.sin(th), color="#c9a887", lw=1.5, ls="--")
        drawn = t_all <= tt + 1e-9
        ax.plot(X[drawn], Y[drawn], color=BLUE, lw=2.0)
        cx, cy = (R - r)*np.cos(tt), (R - r)*np.sin(tt)
        circ = Circle((cx, cy), r, fill=False, edgecolor=ORANGE, lw=2.0, zorder=6)
        ax.add_patch(circ)
        px, py = cx + r*np.cos(-k*tt), cy + r*np.sin(-k*tt)
        ax.plot([cx, px], [cy, py], color=GREY, lw=0.9, ls=":", zorder=6)
        ax.plot([px], [py], "o", color=RED, ms=6, zorder=8)
        ax.set_title("$R=%dr$" % (R/r), fontsize=T-1, color=INK, pad=6)
        fig.tight_layout()
        fp = os.path.join(SCRATCH, "f_hypo_%d_%03d.png" % (int(R/r), i))
        fig.savefig(fp, dpi=110); plt.close(fig)
        frames.append(Image.open(fp).convert("P", palette=Image.ADAPTIVE))
    out = BASE + "geo2-hypocycloid-%d.gif" % int(R/r)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=dur, loop=0, optimize=True)
    for i in range(N_FRAMES):
        os.remove(os.path.join(SCRATCH, "f_hypo_%d_%03d.png" % (int(R/r), i)))
    print("ok", out)

make_hypo(6, 2)   # R=3r
make_hypo(8, 2)   # R=4r
make_hypo(10, 2)  # R=5r
print("done gifs")
