import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 12, 13

a, b = 2.8, 1.8
th = np.linspace(0, 2 * np.pi, 500)
t0 = np.deg2rad(58)
x0, y0 = a * np.cos(t0), b * np.sin(t0)
k = -b * b * x0 / (a * a * y0)

fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
ax.axhline(0, color="#dcdcdc", lw=0.9)
ax.axvline(0, color="#dcdcdc", lw=0.9)
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)

xs = np.linspace(x0 - 1.6, x0 + 1.1, 10)
ax.plot(xs, y0 + k * (xs - x0), color=RED, lw=2.4, zorder=4)
ax.plot([x0, x0], [0, y0], color=GREY, lw=1.1, ls="--", zorder=2)
ax.plot([0, x0], [y0, y0], color=GREY, lw=1.1, ls="--", zorder=2)
ax.plot([0, x0], [0, 0], color=GREY, lw=1.1, ls=":", zorder=2)
ax.plot([x0], [y0], "o", color=ORANGE, ms=9, zorder=6)
ax.text(x0 + 0.12, y0 + 0.14, "$P(x_0,y_0)$", fontsize=F - 0.5, color=ORANGE)
ax.text(x0 / 2 - 0.10, -0.36, "$x_0$", fontsize=F - 0.5, color=GREY)
ax.text(x0 + 0.10, y0 / 2 - 0.06, "$y_0$", fontsize=F - 0.5, color=GREY)
ax.text(-3.6, 2.30, r"切线：$\dfrac{x_0x}{a^2}+\dfrac{y_0y}{b^2}=1$", fontsize=F + 0.5, color=RED)
ax.text(-3.6, 1.75, r"斜率 $k=-\dfrac{b^2x_0}{a^2y_0}$", fontsize=F - 0.5, color=RED)
ax.text(-3.6, -2.15, "把切点坐标代进点斜式，两边乘 $\\dfrac{y_0}{b^2}$", fontsize=F - 1.5, color=INK)
ax.text(-3.6, -2.60, "再用 $\\dfrac{x_0^2}{a^2}+\\dfrac{y_0^2}{b^2}=1$ 化常数项", fontsize=F - 1.5, color=INK)
ax.set_xlim(-3.8, 3.8); ax.set_ylim(-2.9, 2.9)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#bbbbbb")
ax.set_xlabel("$x$", fontsize=10, color=INK)
ax.set_ylabel("$y$", fontsize=10, color=INK)
ax.set_title("椭圆在一点处的切线", fontsize=T, color=INK, pad=10)
fig.tight_layout()
fig.savefig(BASE + "ellipse-tangent.png", dpi=150)
plt.close(fig)
print("ok")
