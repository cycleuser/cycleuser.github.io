# -*- coding: utf-8 -*-
"""生成《手机产状测量》文章配图与 GIF，并打印数值验证。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Heiti TC", "Arial Unicode MS", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))
d2r = np.deg2rad
r2d = np.rad2deg


# ---------- 基础旋转 ----------
def Rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def Rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def R_from_ypr(yaw, pitch, roll):
    """约定 R = Rz(yaw) Rx(pitch) Ry(roll)，列向量为机体轴在 ENU 中的表示。"""
    return Rz(yaw) @ Rx(pitch) @ Ry(roll)


def ypr_from_R(R):
    pitch = np.arcsin(np.clip(R[2, 1], -1, 1))
    roll = np.arctan2(-R[2, 0], R[2, 2])
    yaw = np.arctan2(-R[0, 1], R[1, 1])
    return yaw, pitch, roll


def attitude_from_normal(n):
    """由单位法线（ENU，向上）求 倾角 dip、倾向 dip_direction（度）。"""
    n = n / np.linalg.norm(n)
    if n[2] < 0:
        n = -n
    dip = r2d(np.arccos(np.clip(n[2], -1, 1)))
    dip_dir = (r2d(np.arctan2(-n[0], -n[1]))) % 360
    return dip, dip_dir


def normal_from_attitude(dip, dip_dir):
    """由 倾角/倾向 反求单位法线（ENU，向上）。"""
    updip = (dip_dir + 180) % 360
    e = np.sin(d2r(dip)) * np.sin(d2r(updip))
    nn = np.sin(d2r(dip)) * np.cos(d2r(updip))
    u = np.cos(d2r(dip))
    return np.array([e, nn, u])


def R_on_plane(n, spin):
    """构造一个机体姿态：机体 z 轴贴合平面法线 n，spin 为绕法线的自转角。"""
    n = n / np.linalg.norm(n)
    up = np.array([0, 0, 1.0])
    u1 = np.cross(n, up)              # 走向（水平）
    if np.linalg.norm(u1) < 1e-9:
        u1 = np.array([1.0, 0, 0])
    u1 /= np.linalg.norm(u1)
    u2 = np.cross(n, u1)             # 面内上倾方向
    xb = np.cos(spin) * u1 + np.sin(spin) * u2
    yb = np.cross(n, xb)
    return np.column_stack([xb, yb, n])


# ================= 数值验证：同一平面，两种摆法 =================
print("=" * 60)
DIP_TRUE, DIPDIR_TRUE = 35.0, 120.0
n_true = normal_from_attitude(DIP_TRUE, DIPDIR_TRUE)
print(f"真实平面: 倾角={DIP_TRUE}°, 倾向={DIPDIR_TRUE}°")
print(f"平面法线 (E,N,U) = ({n_true[0]:.4f}, {n_true[1]:.4f}, {n_true[2]:.4f})")
for spin_deg in (0.0, 137.0):
    R = R_on_plane(n_true, d2r(spin_deg))
    yaw, pitch, roll = ypr_from_R(R)
    n_rec = R @ np.array([0, 0, 1.0])
    dip, dipdir = attitude_from_normal(n_rec)
    print(f"\n摆法(spin={spin_deg:>5.1f}°): "
          f"yaw={r2d(yaw):7.2f}° pitch={r2d(pitch):7.2f}° roll={r2d(roll):7.2f}°")
    print(f"   反算法线=({n_rec[0]:.4f},{n_rec[1]:.4f},{n_rec[2]:.4f})  "
          f"=> 倾角={dip:.2f}°  倾向={dipdir:.2f}°")

# ================= 经纬度：磁偏角与 ENU->ECEF =================
print("\n" + "=" * 60)
lat, lon = 29.563, 106.551      # 重庆
mag_decl = -1.9                 # 磁偏角(西偏为负)，随经纬度变化，示例值
dip, dipdir_mag = DIP_TRUE, DIPDIR_TRUE
dipdir_true_north = (dipdir_mag + mag_decl) % 360
print(f"位置: 纬度{lat}° 经度{lon}° 磁偏角{mag_decl}°")
print(f"磁北倾向={dipdir_mag}° -> 真北倾向={dipdir_true_north:.2f}°")


def enu_to_ecef(vec, lat, lon):
    la, lo = d2r(lat), d2r(lon)
    e, n, u = vec
    X = -np.sin(lo) * e - np.sin(la) * np.cos(lo) * n + np.cos(la) * np.cos(lo) * u
    Y = np.cos(lo) * e - np.sin(la) * np.sin(lo) * n + np.cos(la) * np.sin(lo) * u
    Z = np.cos(la) * n + np.sin(la) * u
    return np.array([X, Y, Z])


ecef = enu_to_ecef(n_true, lat, lon)
print(f"法线在 ECEF(地心地固)中的方向 = ({ecef[0]:.4f}, {ecef[1]:.4f}, {ecef[2]:.4f})")
print("=" * 60)


# ================= 图1：三个角的定义 =================
def draw_phone(ax, R, center=(0, 0, 0), w=0.6, h=1.1, color="#2c3e50"):
    c = np.array(center)
    corners = np.array([[-w/2, -h/2, 0], [w/2, -h/2, 0],
                        [w/2, h/2, 0], [-w/2, h/2, 0]])
    world = (R @ corners.T).T + c
    poly = Poly3DCollection([world], alpha=0.55, facecolor=color,
                            edgecolor="#1a252f", linewidths=1.2)
    ax.add_collection3d(poly)
    axes = {"x(右)": ("#e74c3c", R[:, 0]), "y(顶)": ("#27ae60", R[:, 1]),
            "z(屏幕法线)": ("#2980b9", R[:, 2])}
    for lab, (col, v) in axes.items():
        ax.quiver(*c, *(v * 0.9), color=col, lw=2.5, arrow_length_ratio=0.18)
    return world


fig = plt.figure(figsize=(11, 3.6))
titles = ["Pitch 俯仰 (绕 x)", "Roll 横滚 (绕 y)", "Yaw 偏转/航向 (绕 z)"]
mats = [R_from_ypr(0, d2r(35), 0),
        R_from_ypr(0, 0, d2r(35)),
        R_from_ypr(d2r(45), 0, 0)]
for i, (t, R) in enumerate(zip(titles, mats)):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d")
    draw_phone(ax, R)
    for v, lab, col in [((1.2, 0, 0), "E", "#888"), ((0, 1.2, 0), "N", "#888"),
                        ((0, 0, 1.2), "U", "#888")]:
        ax.quiver(0, 0, 0, *v, color=col, lw=0.8, arrow_length_ratio=0.1, alpha=0.5)
    ax.set_title(t, fontsize=11)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off()
    ax.view_init(elev=22, azim=-60)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "产状-角度定义.svg"))
fig.savefig(os.path.join(OUT, "产状-角度定义.png"), dpi=150)
plt.close(fig)
print("saved 产状-角度定义")


# ================= 图2：实例（同一平面两种摆法） =================
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection="3d")
gx, gy = np.meshgrid(np.linspace(-1.4, 1.4, 2), np.linspace(-1.4, 1.4, 2))
gz = (-n_true[0] * gx - n_true[1] * gy) / n_true[2]
ax.plot_surface(gx, gy, gz, alpha=0.25, color="#95a5a6")
for spin_deg, col, cen in [(0.0, "#2c3e50", (-0.5, -0.4)), (137.0, "#c0392b", (0.5, 0.4))]:
    R = R_on_plane(n_true, d2r(spin_deg))
    z = (-n_true[0] * cen[0] - n_true[1] * cen[1]) / n_true[2]
    draw_phone(ax, R, center=(cen[0], cen[1], z), color=col)
ax.quiver(0, 0, 0, *(n_true * 1.3), color="#8e44ad", lw=3, arrow_length_ratio=0.15)
ax.text(*(n_true * 1.45), "法线", color="#8e44ad", fontsize=11)
ax.set_title(f"同一平面两种摆法 → 倾角{DIP_TRUE:.0f}° 倾向{DIPDIR_TRUE:.0f}°", fontsize=12)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_zlim(-1.5, 1.5)
ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(elev=20, azim=-55)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "产状-实例.svg"))
fig.savefig(os.path.join(OUT, "产状-实例.png"), dpi=150)
plt.close(fig)
print("saved 产状-实例")


# ================= 图3：GIF 旋转不变性 =================
fig = plt.figure(figsize=(7.5, 6.2))
ax = fig.add_subplot(111, projection="3d")
n = n_true
gz = (-n[0] * gx - n[1] * gy) / n[2]


def frame(i):
    ax.clear()
    spin = d2r(i * 6)
    ax.plot_surface(gx, gy, gz, alpha=0.22, color="#95a5a6")
    R = R_on_plane(n, spin)
    z0 = 0.0
    draw_phone(ax, R, center=(0, 0, z0))
    ax.quiver(0, 0, 0, *(n * 1.3), color="#8e44ad", lw=3, arrow_length_ratio=0.15)
    yaw, pitch, roll = ypr_from_R(R)
    dip, dipdir = attitude_from_normal(R @ np.array([0, 0, 1.0]))
    ax.text2D(0.02, 0.97, f"yaw={r2d(yaw):6.1f}°  pitch={r2d(pitch):6.1f}°  roll={r2d(roll):6.1f}°  (随摆放变化)",
              transform=ax.transAxes, fontsize=10, color="#c0392b")
    ax.text2D(0.02, 0.91, f"倾角={dip:5.1f}°   倾向={dipdir:5.1f}°   (恒定不变)",
              transform=ax.transAxes, fontsize=11, color="#27ae60", weight="bold")
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_zlim(-1.2, 1.5)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(elev=20, azim=-55)


ani = FuncAnimation(fig, frame, frames=60, interval=90)
ani.save(os.path.join(OUT, "产状-旋转不变.gif"), writer=PillowWriter(fps=12))
plt.close(fig)
print("saved 产状-旋转不变.gif")
print("ALL DONE")
