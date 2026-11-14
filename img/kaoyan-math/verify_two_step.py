import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, RED, GREEN, GREY = "#2b2b2b", "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
PI = np.pi
a = 1.0

# 第一步：极坐标平面画 r=a(1+cosθ)
th = np.linspace(0, 2 * PI, 1500)
r = a * (1 + np.cos(th))
X0 = r * np.cos(th)
Y0 = r * np.sin(th)

# 第二步：代入 r=sqrt(x²+y²), cosθ=x/sqrt(x²+y²)，得 (x²+y²-ax)²=a²(x²+y²)
# 按方程求根：对每个 x 解 u²-au-ax=0 → u=... → y²=u²-x²
xs = np.linspace(-a / 4, 2 * a, 3000)
sp = np.sqrt(a * a + 4 * a * xs)
Xc, Yc = [], []
for sgn in (1, -1):
    t = (a + sgn * sp) / 2
    y2 = np.maximum(t * t - xs * xs, 0)
    m = y2 >= 0
    Xc.append(xs[m]); Yc.append(np.sqrt(y2[m]))
    Xc.append(xs[m]); Yc.append(-np.sqrt(y2[m]))

# 核验：第一步的点是否全部满足第二步的方程
res = (X0 ** 2 + Y0 ** 2 - a * X0) ** 2 - a ** 2 * (X0 ** 2 + Y0 ** 2)
print("第一步全部 1500 个点代入第二步方程的残差：max =", np.abs(res).max())

# 第 1 张
fig, ax = plt.subplots(figsize=(6.8, 6.2), dpi=150)
thg = np.linspace(0, 2 * PI, 400)
for rr in np.arange(0.5, 2.6, 0.5):
    ax.plot(rr * np.cos(thg), rr * np.sin(thg), color="#e8e8e8", lw=0.8)
for a0 in np.arange(0, np.pi, PI / 6):
    for sg in (1, -1):
        ax.plot([0, 2.6 * np.cos(a0) * sg], [0, 2.6 * np.sin(a0) * sg], color="#e8e8e8", lw=0.8)
ax.axhline(0, color="#c8c8c8", lw=1.1); ax.axvline(0, color="#c8c8c8", lw=1.1)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_aspect("equal")
ax.plot(X0, Y0, color=GREEN, lw=2.4, zorder=3)
ax.set_title("第一步：用极坐标式逐点画 $r=a(1+\\cos\\theta)$\\n网格：同心圆加射线", fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11); ax.set_ylabel("$y$", fontsize=11)
ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([-2, -1, 0, 1, 2])
ax.tick_params(labelsize=9, colors="#999999", length=2)
for s_ in ax.spines.values():
    s_.set_color("#cccccc")
fig.tight_layout(); fig.savefig(BASE + "verify-pc-cardioid-step1.png", dpi=150); plt.close(fig)

# 第 2 张
fig, ax = plt.subplots(figsize=(6.8, 6.2), dpi=150)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_aspect("equal")
ax.grid(True, color="#ececec", lw=0.8)
ax.axhline(0, color="#c8c8c8", lw=1.1); ax.axvline(0, color="#c8c8c8", lw=1.1)
for xs_, ys_ in zip(Xc, Yc):
    ax.plot(xs_, ys_, color=GREEN, lw=2.4, zorder=3)
ax.set_title("第二步：用代入后的方程单独画\\n$(x^{2}+y^{2}-ax)^{2}=a^{2}(x^{2}+y^{2})$，对每个 $x$ 解出 $y$ 描点",
             fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11); ax.set_ylabel("$y$", fontsize=11)
ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([-2, -1, 0, 1, 2])
ax.tick_params(labelsize=9, colors="#999999", length=2)
for s_ in ax.spines.values():
    s_.set_color("#cccccc")
fig.tight_layout(); fig.savefig(BASE + "verify-pc-cardioid-step2.png", dpi=150); plt.close(fig)

print("saved")
