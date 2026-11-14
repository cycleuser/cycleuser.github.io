import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, RED, BLUE, GREY = "#2b2b2b", "#b03a2e", "#2f4f6f", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
PI = np.pi

# 左：按极坐标公式 r=a(1+cosθ) 算出的点
a = 1.0
th = np.array([0, PI/6, PI/4, PI/3, PI/2, 2*PI/3, 3*PI/4, PI, 5*PI/4, 3*PI/2, 11*PI/6])
r = a * (1 + np.cos(th))
pts = r * np.exp(1j * th)          # 复数=极坐标点
px, py = pts.real, pts.imag

# 右：直角坐标方程 (x²+y²-ax)²=a²(x²+y²)，对同样的 x 解 y
xs = np.linspace(px.min(), px.max(), 3000)
sp = np.sqrt(a * a + 4 * a * xs)
curve = []
for sgn in (1, -1):
    t = (a + sgn * sp) / 2
    y2 = t * t - xs * xs
    m = y2 >= 0
    curve.append((xs[m], np.sqrt(y2[m])))
    curve.append((xs[m], -np.sqrt(y2[m])))

fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.4), dpi=150)
lim = 2.5
for ax in axes:
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.grid(True, color="#ececec", lw=0.8)
    ax.axhline(0, color="#c8c8c8", lw=1.1); ax.axvline(0, color="#c8c8c8", lw=1.1)
    tk = [-2, -1, 0, 1, 2]
    ax.set_xticks(tk); ax.set_yticks(tk)
    ax.tick_params(length=2, colors="#cccccc")
    for s in ax.spines.values():
        s.set_color("#cccccc")

# 左网格：同心圆+射线（极坐标平面）
axL = axes[0]
thg = np.linspace(0, 2*PI, 400)
for rr in np.arange(0.5, lim+0.01, 0.5):
    axL.plot(rr*np.cos(thg), rr*np.sin(thg), color="#e8e8e8", lw=0.8)
for a0 in np.arange(0, np.pi, PI/6):
    for sg in (1, -1):
        axL.plot([0, lim*np.cos(a0)*sg], [0, lim*np.sin(a0)*sg], color="#e8e8e8", lw=0.8)
for xs_, ys_ in curve:
    axL.plot(xs_, ys_, color=RED, lw=1.2, alpha=0.9)
axL.plot(px, py, "o", color=BLUE, ms=9, zorder=5)
axL.set_title("左：极坐标平面\n极坐标公式算的点（10 个，蓝点）"
              , fontsize=12.5, color=INK)
# 右网格：方格（直角坐标平面）
axR = axes[1]
for xs_, ys_ in curve:
    axR.plot(xs_, ys_, color=RED, lw=1.2, alpha=0.9)
axR.plot(px, py, "o", color=BLUE, ms=9, zorder=5)
axR.set_title("右：直角坐标平面\n方程解出的曲线，同 10 个点（蓝点）"
              , fontsize=12.5, color=INK)
for ax in axes:
    ax.set_xlabel("$x$", fontsize=11, labelpad=0)
    ax.set_ylabel("$y$", fontsize=11, labelpad=0)

fig.suptitle("验证：极坐标公式取 10 个点，与直角坐标方程里解出的曲线，逐点重合", fontsize=13.5, color=INK, y=0.99)
fig.tight_layout(rect=(0,0,1,0.96))
fig.savefig(BASE + "verify-pc-cardioid-overlay.png", dpi=150)
print("saved")
