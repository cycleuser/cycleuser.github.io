import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"

HALF = 45.0   # 圆锥半顶角
cases = [(0.42, 1.00, (-1.55, 1.55), "椭圆"),
         (1.00, 0.75, (-1.95, 1.95), "抛物线"),
         (1.85, 0.55, (-2.20, 2.20), "双曲线")]


def curves(m, c, vrange):
    vs = np.linspace(vrange[0], vrange[1], 900)
    if abs(m - 1) < 1e-9:
        B = -np.sqrt(2) * c
        return [((vs ** 2 - c ** 2) / (-B), vs)], B, 0.0
    A = (1 - m ** 2) / (1 + m ** 2)
    B = -2 * c * m / np.hypot(1, m)
    disc = B ** 2 - 4 * A * (vs ** 2 - c ** 2)
    ok = disc >= 0
    vs, disc = vs[ok], disc[ok]
    up = (-B + np.sqrt(disc)) / (2 * A)
    um = (-B - np.sqrt(disc)) / (2 * A)
    if A > 0:
        return [(np.concatenate([up, um[::-1], up[:1]]),
                 np.concatenate([vs, vs[::-1], vs[:1]]))], B, A
    return [(up, vs), (um, vs)], B, A


def theta_deg(m):
    return np.degrees(np.arcsin(1 / np.hypot(1, m)))


fig = plt.figure(figsize=(13.8, 8.2), dpi=150)

for k, (m, c, vr, name) in enumerate(cases):
    e1 = np.array([1, 0, m]) / np.hypot(1, m)
    e2 = np.array([0, 1, 0])
    P0 = np.array([0, 0, c])
    sets, B, A = curves(m, c, vr)

    # ---------- 上排：3D ----------
    ax = fig.add_subplot(2, 3, k + 1, projection="3d")
    t = np.linspace(0, 2.2, 26)
    th = np.linspace(0, 2 * np.pi, 60)
    T, TH = np.meshgrid(t, th)
    Xc, Yc = T * np.cos(TH), T * np.sin(TH)
    for Z in (T, -T):
        ax.plot_surface(Xc, Yc, Z, color=CREAM, alpha=0.55, linewidth=0, shade=False,
                        antialiased=True, rstride=1, cstride=3)
    for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        ax.plot([0, 2.2 * np.cos(a)], [0, 2.2 * np.sin(a)], [0, 2.2], color=BLUE, lw=0.9, alpha=0.7)
        ax.plot([0, 2.2 * np.cos(a)], [0, 2.2 * np.sin(a)], [0, -2.2], color=BLUE, lw=0.9, alpha=0.7)
    th2 = np.linspace(0, 2 * np.pi, 200)
    for z in (2.2, -2.2):
        ax.plot(2.2 * np.cos(th2), 2.2 * np.sin(th2), z, color=BLUE, lw=0.9, alpha=0.7)
    ax.plot([0, 0], [0, 0], [-2.3, 2.3], color=GREY, lw=1.0, ls="--")
    # 截面
    corners = [(-2.6, vr[0]), (2.6, vr[0]), (2.6, vr[1]), (-2.6, vr[1])]
    pts3 = [P0 + u * e1 + v * e2 for u, v in corners]
    ax.add_collection3d(Poly3DCollection([pts3], facecolor=BLUE, alpha=0.20,
                                          edgecolor=BLUE, linewidths=1.0))
    for u, v in sets:
        ax.plot(P0[0] + u * e1[0] + v * e2[0],
                P0[1] + u * e1[1] + v * e2[1],
                P0[2] + u * e1[2] + v * e2[2], color=RED, lw=3.0, zorder=10)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_zlim(-2.6, 2.6)
    ax.set_box_aspect((1, 1, 1.25))
    ax.view_init(elev=27, azim=-64)
    ax.set_axis_off()
    if abs(m - 1) < 1e-9:
        sub = "θ=%.0f°，与半顶角相等" % theta_deg(m)
    else:
        sub = "θ=%.0f° %s 半顶角 %.0f°" % (theta_deg(m), ">" if m < 1 else "<", HALF)
    ax.set_title("%s：%s" % (name, sub), fontsize=11, color=INK, pad=0)

    # ---------- 下排：截面内的真实形状 ----------
    ax2 = fig.add_subplot(2, 3, k + 4)
    for u, v in sets:
        if A < 0:
            keep = np.abs(v) <= 1.6
            ax2.plot(u[keep], v[keep], color=RED, lw=2.8, zorder=5)
        else:
            ax2.plot(u, v, color=RED, lw=2.8, zorder=5)
    ax2.axhline(0, color="#dcdcdc", lw=0.9, zorder=1)
    ax2.axvline(0, color="#dcdcdc", lw=0.9, zorder=1)

    if abs(m - 1) < 1e-9:                        # 抛物线
        uv = -c * c / B
        p4 = B                                     # v² = B(u-uv) → 4p = B
        focus = uv + p4 / 4
        ax2.plot([uv], [0], "o", color=BLUE, ms=7, zorder=6)
        ax2.plot([focus], [0], "o", color=GREEN, ms=8, zorder=6)
        ax2.annotate("顶点", xy=(uv, 0), xytext=(uv + 0.15, 0.55), fontsize=9, color=BLUE)
        ax2.annotate("焦点", xy=(focus, 0), xytext=(focus - 0.1, -0.75), fontsize=9, color=GREEN)
        ax2.set_title("抛物线（截面内看）", fontsize=10.5, color=INK, pad=5)
    else:
        u0 = -B / (2 * A)
        R = c * c + B * B / (4 * A)
        ax2.plot([u0], [0], "o", color=BLUE, ms=7, zorder=6)
        if A > 0:                               # 椭圆
            au = np.sqrt(R / A); bv = np.sqrt(R)
            if au > bv:
                f = np.sqrt(au * au - bv * bv)
                ax2.plot([u0 - f, u0 + f], [0, 0], "o", color=GREEN, ms=7, zorder=6)
                lab = "长轴 %.2f，短轴 %.2f，焦距 %.2f" % (2 * au, 2 * bv, 2 * f)
            else:
                f = np.sqrt(bv * bv - au * au)
                ax2.plot([u0], [-f], "o", color=GREEN, ms=7, zorder=6)
                ax2.plot([u0], [f], "o", color=GREEN, ms=7, zorder=6)
                lab = "长轴 %.2f，短轴 %.2f，焦距 %.2f" % (2 * bv, 2 * au, 2 * f)
            ax2.annotate("中心", xy=(u0, 0), xytext=(u0 + 0.12, 0.30), fontsize=8.5, color=BLUE)
            ax2.set_title("椭圆（截面内看）：%s" % lab, fontsize=10, color=INK, pad=5)
        else:                                   # 双曲线
            kk = np.sqrt(-A)
            xx = np.linspace(u0 - 3.0, u0 + 3.0, 60)
            ax2.plot(xx, kk * (xx - u0), color=GREY, lw=1.1, ls="--", zorder=2)
            ax2.plot(xx, -kk * (xx - u0), color=GREY, lw=1.1, ls="--", zorder=2)
            if R < 0:                           # 开口沿 ±u
                a2 = np.sqrt(R / A); b2 = np.sqrt(-R)
                f2 = np.sqrt(a2 * a2 + b2 * b2)
                ax2.plot([u0 - f2, u0 + f2], [0, 0], "o", color=GREEN, ms=7, zorder=6)
                ax2.set_title("双曲线（截面内看）：实轴 %.2f，焦点距中心 %.2f，虚线为渐近线"
                              % (2 * a2, f2), fontsize=9.5, color=INK, pad=5)
            else:                               # 开口沿 ±v
                a2 = np.sqrt(R); b2 = np.sqrt(R / (-A))
                f2 = np.sqrt(a2 * a2 + b2 * b2)
                ax2.plot([u0, u0], [-f2, f2], "o", color=GREEN, ms=7, zorder=6)
                ax2.set_title("双曲线（截面内看）：虚线为渐近线", fontsize=9.5, color=INK, pad=5)
            ax2.annotate("中心", xy=(u0, 0), xytext=(u0 + 0.15, 0.35), fontsize=8.5, color=BLUE)
    ax2.set_aspect("equal")
    ax2.set_xlim(-4.0, 3.6)
    ax2.set_ylim(-1.9, 1.9) if A < 0 else ax2.set_ylim(vr[0] - 0.6, vr[1] + 0.6)
    ax2.tick_params(colors="#777", labelsize=7)
    for sp in ax2.spines.values():
        sp.set_color("#cccccc")

fig.suptitle("用平面截双圆锥：上排看截法，下排看截面内的真实形状", fontsize=13.5, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(BASE + "geo6-conic-cut.png", dpi=150)
plt.close(fig)
print("ok")
