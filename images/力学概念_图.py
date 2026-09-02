# -*- coding: utf-8 -*-
"""
材料力学基础概念配图生成脚本
运行方式：在本目录（content/）下执行  python images/力学概念_图.py
产物输出到 content/images/ 下
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon, Wedge, Arc

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Hiragino Sans GB', 'Heiti TC', 'Songti SC', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 110

os.makedirs('images', exist_ok=True)
OUT = 'images'

RED = '#e74c3c'
BLUE = '#2980b9'
GREEN = '#2ecc71'
DARK = '#2c3e50'
GRAY = '#95a5a6'


def save(fig, name):
    fig.savefig(f'{OUT}/{name}.svg', format='svg', bbox_inches='tight')
    fig.savefig(f'{OUT}/{name}.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('saved', name)


def force_arrow(ax, x, y, dx, dy, color=RED, lw=2.2, head=0.18):
    ax.add_patch(FancyArrowPatch((x, y), (x + dx, y + dy),
                                 arrowstyle='-|>', mutation_scale=20,
                                 lw=lw, color=color))


def rot_arrow(ax, cx, cy, r, t1, t2, color=GREEN, lw=2.2):
    """从 t1 到 t2 画顺时针（角度递减）的圆弧箭头，角度单位为度"""
    th = np.linspace(np.radians(t1), np.radians(t2), 120)
    x = cx + r * np.cos(th)
    y = cy + r * np.sin(th)
    ax.plot(x, y, color=color, lw=lw, solid_capstyle='round')
    t = np.radians(t2)
    ang_deg = np.degrees(np.arctan2(-np.cos(t), np.sin(t)))
    ax.add_patch(mpatches.RegularPolygon((x[-1], y[-1]), 3, radius=0.10,
                 orientation=np.radians(ang_deg), color=color))


# ============================================================
# 1. 应力：正应力 与 切应力
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# 正应力（拉）
ax = axes[0]
s = 1.0
ax.add_patch(Rectangle((-s, -s), 2 * s, 2 * s, fc='#dff0f7', ec=DARK, lw=2))
for y in (0.45, 0.0, -0.45):
    force_arrow(ax, -s, y, -1.0, 0)
    force_arrow(ax, s, y, 1.0, 0)
ax.text(0, 0, 'σ', ha='center', va='center', fontsize=24, color=DARK)
ax.text(0, -2.0, '拉力 ÷ 截面积', ha='center', fontsize=13, color=RED)
ax.set_xlim(-3, 3); ax.set_ylim(-2.5, 2.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('正应力 σ：力垂直作用在面上', fontsize=15)

# 切应力
ax = axes[1]
ax.add_patch(Rectangle((-s, -s), 2 * s, 2 * s, fc='#fdf0d6', ec=DARK, lw=2))
for x in (-0.45, 0.0, 0.45):
    force_arrow(ax, x, s, 0, 1.0)
    force_arrow(ax, x, -s, 0, -1.0)
ax.text(0, 0, 'τ', ha='center', va='center', fontsize=24, color=DARK)
ax.text(0, -2.0, '切向力 ÷ 截面积', ha='center', fontsize=13, color=RED)
ax.set_xlim(-3, 3); ax.set_ylim(-2.5, 2.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('切应力 τ：力平行（相切）作用在面上', fontsize=15)

fig.suptitle('应力 = 单位面积上分摊到的力', fontsize=17, y=1.02)
fig.tight_layout()
save(fig, 'stress')

# ============================================================
# 2. 应变：正应变 与 切应变
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# 正应变
ax = axes[0]
L = 2.0
dL = 0.8
ax.add_patch(Rectangle((-L / 2, -0.6), L, 1.2, fill=False, ls='--', ec=GRAY, lw=1.8))
ax.add_patch(Rectangle((-L / 2, -0.6), L + dL, 1.2, fc='#dff0f7', ec=BLUE, lw=2))
for y in (0.3, -0.3):
    force_arrow(ax, -L / 2, y, -0.9, 0, color=RED)
    force_arrow(ax, L / 2 + dL, y, 0.9, 0, color=RED)
ax.annotate('', xy=(L / 2 + dL, 1.35), xytext=(L / 2, 1.35),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.6))
ax.text(L / 2 + dL / 2, 1.6, 'ΔL（伸长量）', ha='center', fontsize=12, color=BLUE)
ax.annotate('', xy=(0.9, -1.1), xytext=(-0.9, -1.1),
            arrowprops=dict(arrowstyle='<->', color=GRAY, lw=1.6))
ax.text(0, -1.5, '原长 L', ha='center', fontsize=12, color=GRAY)
ax.text(L / 2 + dL + 0.3, 0, 'ε = ΔL / L', ha='left', va='center', fontsize=14, color=DARK)
ax.set_xlim(-3.3, 5.5); ax.set_ylim(-2.2, 2.2); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('正应变 ε：拉长（或压短）的比例', fontsize=15)

# 切应变
ax = axes[1]
shift = 0.9
ax.add_patch(Rectangle((-L / 2, -0.6), L, 1.2, fill=False, ls='--', ec=GRAY, lw=1.8))
corners = [(-L / 2, -0.6), (L / 2, -0.6), (L / 2 + shift, 0.6), (-L / 2 + shift, 0.6)]
ax.add_patch(Polygon(corners, closed=True, fc='#fdf0d6', ec=BLUE, lw=2))
for x in (0.0, 0.45, 0.9):
    force_arrow(ax, x - 0.6, 0.6, 0, 0.85, color=RED)
    force_arrow(ax, x - 0.6 + L, -0.6, 0, -0.85, color=RED)
ang = np.degrees(np.arctan2(shift, L))
ax.add_patch(Arc((-L / 2, -0.6), 0.9, 0.9, theta1=0, theta2=ang, color=GREEN, lw=2))
ax.text(-L / 2 + 0.55, -0.6 + 0.22, 'γ', fontsize=16, color=GREEN)
ax.text(-L / 2 + shift / 2, 1.35, '上边沿横向滑移', ha='center', fontsize=12, color=BLUE)
ax.text(L / 2 + 1.9, 0, 'γ = 滑移量 / 高度', ha='left', va='center', fontsize=13, color=DARK)
ax.set_xlim(-2.2, 5.8); ax.set_ylim(-2.2, 2.4); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('切应变 γ：形状发生"剪切"倾斜', fontsize=15)

fig.suptitle('应变 = 变形量与原来尺寸的比值', fontsize=17, y=1.02)
fig.tight_layout()
save(fig, 'strain')

# ============================================================
# 3. 应力-应变曲线（低碳钢 vs 铸铁 vs 橡胶）
# ============================================================
def steel_curve():
    e_y, sig_y = 0.002, 400.0
    E = sig_y / e_y
    e_plateau, e_hard, e_neck, e_break = 0.02, 0.18, 0.22, 0.235
    sig_u = 600.0
    e1 = np.linspace(0, e_y, 60); s1 = E * e1
    e2 = np.linspace(e_y, e_plateau, 40); s2 = np.full_like(e2, sig_y)
    t = (np.linspace(0, 1, 120)) ** 0.9
    e3 = e_plateau + (e_hard - e_plateau) * t
    s3 = sig_y + (sig_u - sig_y) * t
    t2 = np.linspace(0, 1, 60) ** 1.4
    e4 = e_hard + (e_break - e_hard) * t2
    s4 = sig_u - (sig_u - 500.0) * t2
    e = np.concatenate([e1, e2, e3, e4]); s = np.concatenate([s1, s2, s3, s4])
    return e, s, (e_y, sig_y), (e_hard, sig_u), (e_break, s4[-1])

fig, ax = plt.subplots(figsize=(11, 6))

e, s, (ey, sy), (eu, su), (ef, sf) = steel_curve()
ax.plot(e, s, color=BLUE, lw=2.4, label='低碳钢（韧性材料）')

# 铸铁（脆性）
e_ci = np.linspace(0, 0.0045, 60)
s_ci = 38000 * e_ci * (1 - 8 * e_ci)
s_ci = np.clip(s_ci, 0, 140)
ax.plot(e_ci, s_ci, color=RED, lw=2.4, label='铸铁（脆性材料）')

# 橡胶（高弹性）
e_r = np.linspace(0, 4.0, 120)
s_r = 3.2 * (np.exp(0.75 * e_r) - 1)
ax.plot(e_r, s_r, color=GREEN, lw=2.4, label='橡胶（高弹性材料）')

ax.scatter([ey], [sy], color=BLUE, s=40, zorder=5)
ax.annotate('屈服点 σy\n（开始永久变形）', xy=(ey, sy), xytext=(0.05, 620),
            arrowprops=dict(arrowstyle='->', color=DARK), fontsize=12, color=DARK)
ax.annotate('抗拉强度 σu\n（材料能扛的最大应力）', xy=(eu, su), xytext=(0.13, 500),
            arrowprops=dict(arrowstyle='->', color=DARK), fontsize=12, color=DARK)
ax.annotate('断裂', xy=(ef, sf), xytext=(0.13, 180),
            arrowprops=dict(arrowstyle='->', color=DARK), fontsize=12, color=DARK)

ax.text(0.0004, 300, '弹性阶段\n（撤力就复原，\n遵循胡克定律）', fontsize=11, color=BLUE)
ax.text(0.006, 425, '屈服\n平台', fontsize=11, color=BLUE, ha='center')
ax.text(0.10, 520, '强化阶段', fontsize=12, color=BLUE)
ax.text(0.20, 360, '颈缩', fontsize=12, color=BLUE)

ax.text(0.0004, 100, '脆性材料：\n没怎么变形就断了', fontsize=11, color=RED)
ax.text(1.6, 40, '橡胶：\n能抻出好几倍的\n长度不断', fontsize=11, color=GREEN)

ax.set_xlabel('应变 ε', fontsize=13)
ax.set_ylabel('应力 σ（MPa）', fontsize=13)
ax.set_title('应力-应变曲线：同样的变形，不同材料各有各的"脾气"', fontsize=15)
ax.set_xlim(0, 4.3); ax.set_ylim(0, 700)
ax.grid(True, alpha=0.3)
ax.legend(loc='lower right', fontsize=11)
fig.tight_layout()
save(fig, 'ss_curve')

# ============================================================
# 4. 力矩：力 × 力臂
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.add_patch(Circle((0, 0), 0.32, fc='#bdc3c7', ec=DARK, lw=2))
ax.add_patch(Circle((0, 0), 0.14, fc=DARK))
# 扳手
ax.plot([0, 3.4], [0, 0.65], color=DARK, lw=8, solid_capstyle='round')
ax.plot([3.0, 3.4], [0.55, 0.65], color=DARK, lw=8, solid_capstyle='round')
# 力：在扳手末端竖直向下
fx, fy = 3.4, 0.65
force_arrow(ax, fx, fy + 0.9, 0, -1.5, color=RED, lw=3)
ax.text(fx + 0.18, fy + 0.45, '力 F', fontsize=15, color=RED)
# 力臂：支点到力作用线的垂直距离
ax.plot([0, 3.4], [0, 0], color=BLUE, lw=1.4, ls='--')
ax.plot([3.4, 3.4], [0, 0.2], color=BLUE, lw=1.4, ls='--')
ax.add_patch(Rectangle((3.15, 0), 0.25, 0.25, fill=False, ec=BLUE, lw=1))
ax.annotate('', xy=(3.4, 0.42), xytext=(3.4, -0.42),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.6))
ax.text(3.5, 0.05, '力臂 d', fontsize=14, color=BLUE, ha='left')
# 转动方向（顺时针：力向下，扳手顺时针拧）
rot_arrow(ax, 0, 0, 1.0, 15, -75, color=GREEN)
ax.text(0.25, -0.75, 'M = F × d', fontsize=16, color=GREEN, fontweight='bold')
ax.text(0.3, -1.15, '（力臂越长越省力）', fontsize=12, color=GREEN)
ax.text(0, -2.0, '固定螺母', ha='center', fontsize=12, color=GRAY)
ax.set_xlim(-1.3, 5.2); ax.set_ylim(-2.4, 2.0); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('力矩（扭矩）：让物体转动的"扭转本领"', fontsize=15)
fig.tight_layout()
save(fig, 'moment')

# ============================================================
# 5. 力偶：大小相等、方向相反、不共线的一对力
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
d = 2.6
ax.add_patch(Rectangle((-d / 2 - 0.35, -0.55), d + 0.7, 1.1, fc='#dff0f7', ec=DARK, lw=2))
force_arrow(ax, -d / 2, 0.75, 0, 1.3, color=RED, lw=3)
force_arrow(ax, d / 2, -0.75, 0, -1.3, color=RED, lw=3)
ax.text(-d / 2 - 0.15, 1.6, '力 F', fontsize=15, color=RED, ha='center')
ax.text(d / 2 + 0.15, -1.6, '力 F（方向相反）', fontsize=15, color=RED, ha='center')
ax.annotate('', xy=(d / 2, 1.35), xytext=(-d / 2, 1.35),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.6))
ax.text(0, 1.65, '两力之间的距离 d', fontsize=13, color=BLUE, ha='center')
# 转动方向：左上推、右下压，整体顺时针转（沿绕中心的圆弧箭头）
rot_arrow(ax, 0, 0, 0.85, 25, -65, color=GREEN)
rot_arrow(ax, 0, 0, 1.15, 205, 115, color=GREEN)
ax.text(0, 0.42, '合力 = 0，\n不移动，只转动', fontsize=12, color=DARK, ha='center')
ax.text(0, -1.15, '力偶矩 M = F × d', fontsize=16, color=GREEN, fontweight='bold', ha='center')
ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.3, 2.3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('力偶：一对大小相等、方向相反的平行力（不共线）', fontsize=15)
fig.tight_layout()
save(fig, 'couple')

# ---- 力偶让物体纯旋转的动图 ----
fig, ax = plt.subplots(figsize=(5.0, 5.0))
frames = 30
W, H = 2.2, 1.0


def draw_frame(i):
    ax.clear()
    ang = -np.radians(i * 360 / frames)   # 左手上推、右手下压，整体顺时针转
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    corners = np.array([[-W / 2, -H / 2], [W / 2, -H / 2], [W / 2, H / 2], [-W / 2, H / 2]])
    rc = corners @ R.T
    ax.add_patch(Polygon(rc, closed=True, fc='#dff0f7', ec=DARK, lw=2))
    p1 = np.array([-W / 2, 0]) @ R.T
    p2 = np.array([W / 2, 0]) @ R.T
    v = np.array([0, 1]) @ R.T
    ax.add_patch(FancyArrowPatch(p1, p1 + v * 1.0, arrowstyle='-|>', mutation_scale=22, lw=2.6, color=RED))
    ax.add_patch(FancyArrowPatch(p2, p2 - v * 1.0, arrowstyle='-|>', mutation_scale=22, lw=2.6, color=RED))
    ax.text(0, 0, '力偶矩 M\n只转动，不移动', ha='center', va='center', fontsize=12, color=DARK)
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-2.3, 2.3); ax.set_aspect('equal'); ax.axis('off')


from matplotlib.animation import FuncAnimation
anim = FuncAnimation(fig, draw_frame, frames=frames, interval=60)
anim.save(f'{OUT}/couple_rotate.gif', writer='pillow', fps=15)
plt.close(fig)
print('saved couple_rotate.gif')

# ============================================================
# 6. 弯曲：弯矩在截面里产生正应力
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 悬臂梁受弯
ax = axes[0]
ax.add_patch(Rectangle((-0.6, -1.4), 0.6, 2.8, fc='#bdc3c7', ec=DARK, lw=2))
for y in np.linspace(-1.3, 1.3, 7):
    ax.plot([-0.6, -0.05], [y, y - 0.0], color=GRAY, lw=1.2)
x = np.linspace(0, 5, 100)
y_def = 0.4 * (x / 5) ** 2 * 0.0 + 0.9 * (x / 5) ** 2
ax.fill_between(x, -0.35 - 0.0, 0.35 - 0.9 * (x / 5) ** 2, color='#dff0f7', ec=BLUE, lw=1.5)
force_arrow(ax, 5.0, 0.35, 0, -0.8, color=RED, lw=2.6)
ax.text(5.15, -0.55, '载荷 F', fontsize=13, color=RED, ha='left')
ax.text(2.3, 0.75, '梁发生弯曲\n上边受压、下边受拉', fontsize=12, color=DARK, ha='center')
ax.set_xlim(-0.8, 6.0); ax.set_ylim(-1.9, 1.9); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('一根梁被压弯：弯矩 M 引起弯曲', fontsize=14)

# 截面应力分布
ax = axes[1]
ax.add_patch(Rectangle((-0.8, -1.6), 1.6, 3.2, fc='#fdf0d6', ec=DARK, lw=2))
ax.plot([0, 0], [-1.6, 1.6], color=GRAY, lw=2.2, ls='--')
for yy in np.linspace(0.2, 1.5, 5):
    ln = 0.12 + 0.5 * (yy / 1.5)
    force_arrow(ax, 0.8, yy, ln, 0, color=RED, lw=1.8)
for yy in np.linspace(-0.2, -1.5, 5):
    ln = 0.12 + 0.5 * (abs(yy) / 1.5)
    force_arrow(ax, -0.8, yy, -ln, 0, color=BLUE, lw=1.8)
ax.text(1.85, 1.05, '压应力', fontsize=13, color=BLUE, ha='center')
ax.text(1.85, -1.05, '拉应力', fontsize=13, color=RED, ha='center')
ax.text(0, 0.18, '中性轴\n（既不受拉也不受压）', fontsize=11, color=GRAY, ha='center')
ax.text(0, -2.3, 'σ = M·y / I\n离中性轴越远应力越大', fontsize=13, color=DARK, ha='center')
ax.set_xlim(-1.9, 2.6); ax.set_ylim(-2.6, 2.0); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('弯曲在截面里产生的正应力分布', fontsize=14)

fig.suptitle('弯矩 → 弯曲正应力', fontsize=16, y=1.02)
fig.tight_layout()
save(fig, 'bending')

# ============================================================
# 7. 扭转：力偶矩（扭矩）在圆轴截面里产生切应力
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 圆轴受扭
ax = axes[0]
ax.add_patch(Rectangle((-0.6, -1.5), 1.2, 3.0, fc='#dff0f7', ec=DARK, lw=2))
ax.add_patch(Rectangle((2.0, -1.5), 1.2, 3.0, fc='#dff0f7', ec=DARK, lw=2))
ax.plot([0.6, 2.0], [0, 0], color=DARK, lw=6, solid_capstyle='butt')
ax.plot([0.6, 2.0], [-1.1, -1.1], color=GRAY, lw=1.2, ls='--')
ax.plot([0.6, 2.0], [1.1, 1.1], color=GRAY, lw=1.2, ls='--')
for cx, t1, t2, label in [(0.0, 200, 340, '力偶矩 M'), (2.6, 200, 340, '力偶矩 M')]:
    a = Arc((cx, 0), 0.7, 0.7, theta1=t1, theta2=t2, color=RED, lw=2.2)
    ax.add_patch(a)
    ax.text(cx, 1.55, label, fontsize=12, color=RED, ha='center')
ax.text(1.3, 0.42, '圆轴', fontsize=14, color=DARK, ha='center')
ax.set_xlim(-1.2, 3.8); ax.set_ylim(-2.1, 2.2); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('两端施加力偶矩：轴被"拧"', fontsize=14)

# 圆截面剪应力分布
ax = axes[1]
th = np.linspace(0, 2 * np.pi, 100)
r = 1.5
ax.plot(r * np.cos(th), r * np.sin(th), color=DARK, lw=2)
ax.plot(0, 0, 'o', color=DARK, ms=5)
Rr = 1.5
n = 6
for i in range(1, n + 1):
    rr = Rr * i / n
    for ang in (np.pi / 2, -np.pi / 2):
        ln = 0.25 + 1.0 * (i / n)
        dx = np.cos(ang) * ln
        dy = np.sin(ang) * ln
        ax.add_patch(FancyArrowPatch((rr, 0), (rr + dx, dy), arrowstyle='-|>',
                                     mutation_scale=16, lw=1.7, color=RED))
ax.text(0, -1.95, 'τ = T·ρ / J', fontsize=14, color=DARK, ha='center')
ax.text(0, 0, '0', fontsize=12, color=GRAY, ha='center')
ax.text(-1.6, 1.2, '中心应力为 0', fontsize=11, color=GRAY)
ax.text(1.55, -1.15, '边缘应力最大 τmax', fontsize=11, color=RED, ha='right')
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.4, 2.2); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('扭矩在圆截面里产生的切应力分布（线性增大）', fontsize=14)

fig.suptitle('力偶矩（扭矩）→ 扭转切应力', fontsize=16, y=1.02)
fig.tight_layout()
save(fig, 'torsion')

print('全部配图完成')
