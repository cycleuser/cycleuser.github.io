# -*- coding: utf-8 -*-
"""
无人机平飞所需速度 vs 有利速度 —— 完整建模 + 可视化动态演示

参考来源:
  - FAA Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25C), Chapter 11: Aircraft Performance
  - Anderson, "Introduction to Flight"
  - 无人机驾驶员航空知识手册, Chapter 3: 飞行原理与飞行性能

核心概念:
  平飞所需速度 (V_req): 匀速平飞时,升力=重力所需的速度。每个迎角对应一个需用速度。
  平飞有利速度 (V_best): 分两种——
    V_best_range (最大航程速度): 对应 (L/D)_max，也就是总阻力最小点的速度
    V_best_endurance (最大航时速度): 对应最小需用功率点的速度

关键公式:
  平飞条件: L = W  =>  V = sqrt(2W/(ρ S C_L))
  阻力: D = (1/2)ρ V^2 S C_D,  C_D = C_D0 + k C_L^2
  需用功率 (propeller): P_req = D × V
  航程 R ∝ (L/D) × (1/sfc)  →  最大航程在 (L/D)_max
  航时 E ∝ (C_L^(3/2)/C_D) × (1/sfc)  →  最大航时在 (C_L^(3/2)/C_D)_max

对螺旋桨无人机:
  V_best_endurance < V_best_range
  因为 P_req ∝ V^3 × C_D0 + (k W^2)/(ρ S V)
  最小功率点出现在比最小阻力点更低的速度
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.ticker as ticker
import os

plt.rcParams["font.sans-serif"] = ["PingFang HK","Heiti TC","STHeiti","SimHei"]
plt.rcParams["axes.unicode_minus"] = False
OUT = "/Users/fred/Documents/GitHub/cycleuser/blog/images"
os.makedirs(OUT, exist_ok=True)

# ============ 无人机参数 (JL-6 型参考) ============
W  = 20 * 9.81     # 重力 [N], ~20kg
S  = 0.65          # 机翼面积 [m²]
rho = 1.225         # 海平面空气密度 [kg/m³]
C_D0 = 0.025        # 零升阻力系数
k = 0.045            # 诱导阻力因子 (1/(π e AR))
AR = 8.0             # 展弦比

# ============ 气动计算函数 ============
def CL_from_V(V):
    return 2 * W / (rho * S * V**2)

def CD(CL):
    return C_D0 + k * CL**2

def drag(V):
    """总阻力 [N]"""
    CL = CL_from_V(V)
    return 0.5 * rho * V**2 * S * CD(CL)

def lift(V):
    """升力 [N]"""
    CL = CL_from_V(V)
    return 0.5 * rho * V**2 * S * CL

def L_over_D(V):
    CL = CL_from_V(V)
    return CL / CD(CL)

def power_required(V):
    """需用功率 propeller: P_req = D × V [W]"""
    return drag(V) * V

# ============ 计算关键速度 ============
V_stall = np.sqrt(2 * W / (rho * S * 1.6))  # 设 CL_max=1.6
V_max = 60  # [m/s] 最大速度

V_range = np.linspace(V_stall, V_max, 500)

drag_vals = np.array([drag(v) for v in V_range])
power_vals = np.array([power_required(v) for v in V_range])
LD_vals = np.array([L_over_D(v) for v in V_range])
CL_vals = np.array([CL_from_V(v) for v in V_range])

# 找关键点
idx_min_drag = np.argmin(drag_vals)
idx_min_power = np.argmin(power_vals)
idx_max_LD = np.argmax(LD_vals)

V_min_drag = V_range[idx_min_drag]
V_min_power = V_range[idx_min_power]
V_max_LD = V_range[idx_max_LD]

print(f"失速速度: {V_stall:.1f} m/s")
print(f"最小阻力速度 V_min_drag = {V_min_drag:.1f} m/s (对应 (L/D)_max)")
print(f"最小需用功率速度 V_min_power = {V_min_power:.1f} m/s")
print(f"最大升阻比速度 V_(L/D)max   = {V_max_LD:.1f} m/s")
print(f"  → 最大航程速度 = V_min_drag = {V_min_drag:.1f} m/s")
print(f"  → 最大航时速度 = V_min_power = {V_min_power:.1f} m/s")
print(f"  比值 V_range/V_endurance = {V_min_drag/V_min_power:.2f}")

# ============ 图 1: 静态综合分析图 ============
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# 1a: 总阻力 vs 速度
ax = axes[0, 0]
ax.plot(V_range, drag_vals, 'b-', lw=2, label='总阻力 D (Total Drag)')
D_parasitic = 0.5 * rho * V_range**2 * S * C_D0
D_induced = np.array([0.5*rho*v**2*S*k*CL_from_V(v)**2 for v in V_range])
ax.plot(V_range, D_parasitic, '--', color='#16a085', lw=1.2, label='寄生阻力 Parasitic Drag')
ax.plot(V_range, D_induced, '--', color='#e74c3c', lw=1.2, label='诱导阻力 Induced Drag')
ax.axvline(V_min_drag, color='#2980b9', ls=':', lw=2, label=f'V_min_drag = {V_min_drag:.1f}')
ax.axvline(V_min_power, color='#8e44ad', ls=':', lw=2, label=f'V_min_power = {V_min_power:.1f}')
ax.plot(V_min_drag, drag(V_min_drag), 'o', color='#2980b9', ms=10, zorder=5)
ax.plot(V_min_power, drag(V_min_power), 'o', color='#8e44ad', ms=10, zorder=5)
ax.set_xlabel('速度 V (m/s)'); ax.set_ylabel('阻力 D (N)')
ax.set_title('总阻力曲线: D = D_parasitic + D_induced')
ax.legend(fontsize=8, loc='upper left'); ax.grid(True, alpha=0.3)

# 1b: 需用功率 vs 速度
ax = axes[0, 1]
ax.plot(V_range, power_vals/1000, 'g-', lw=2, label='需用功率 P_req (kW)')
ax.axvline(V_min_power, color='#8e44ad', ls=':', lw=2, label=f'V_min_power = {V_min_power:.1f}')
ax.axvline(V_min_drag, color='#2980b9', ls='-.', lw=2, label=f'V_min_drag = {V_min_drag:.1f}')
ax.plot(V_min_power, power_required(V_min_power)/1000, 'o', color='#8e44ad', ms=10)
ax.plot(V_min_drag, power_required(V_min_drag)/1000, 's', color='#2980b9', ms=8)
ax.set_xlabel('速度 V (m/s)'); ax.set_ylabel('需用功率 P_req (kW)')
ax.set_title('需用功率曲线: P_req = D × V')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# 1c: 升阻比 vs 速度
ax = axes[1, 0]
ax.plot(V_range, LD_vals, 'r-', lw=2, label='L/D')
ax.axvline(V_max_LD, color='#2980b9', ls=':', lw=2, label=f'V_(L/D)max = {V_max_LD:.1f}')
ax.plot(V_max_LD, LD_vals[idx_max_LD], 'o', color='#c0392b', ms=10)
ax.set_xlabel('速度 V (m/s)'); ax.set_ylabel('升阻比 L/D')
ax.set_title(f'升阻比曲线: (L/D)_max = {LD_vals[idx_max_LD]:.1f}')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# 1d: 航程/航时相对值 vs 速度
ax = axes[1, 1]
R_rel = LD_vals / LD_vals[idx_max_LD] * 100  # 相对航程
E_rel_prop = (CL_vals**1.5 / np.array([CD(cl) for cl in CL_vals])) / (CL_vals[idx_min_power]**1.5 / CD(CL_vals[idx_min_power])) * 100
ax.plot(V_range, R_rel, 'b-', lw=2, label='相对航程 Range (∝ L/D)')
ax.plot(V_range, E_rel_prop, 'g-', lw=2, label='相对航时 Endurance (propeller)')
ax.axvline(V_min_drag, color='#2980b9', ls='--', lw=1.5)
ax.axvline(V_min_power, color='#8e44ad', ls='--', lw=1.5)
ax.axhline(100, color='gray', ls=':', lw=0.8)
ax.set_xlabel('速度 V (m/s)'); ax.set_ylabel('相对值 (%)')
ax.set_title('航程 vs 航时: 最大航程用 V_min_drag，最大航时用 V_min_power')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

plt.suptitle('无人机平飞性能综合分析\nV_min_drag (最大航程) vs V_min_power (最大航时)', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "uav-speed-analysis.svg"), bbox_inches='tight')
fig.savefig(os.path.join(OUT, "uav-speed-analysis.png"), dpi=150, bbox_inches='tight')
plt.close(fig)
print("saved analysis charts")

# ============ GIF: 动画展示气动力随速度变化 ============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.35)

def draw_frame(i):
    ax1.clear(); ax2.clear()
    idx = i * 4  # step through V_range
    if idx >= len(V_range): idx = len(V_range) - 1
    V = V_range[idx]
    
    # 上图: 阻力分解条形图
    CL_v = CL_from_V(V)
    D_p = 0.5 * rho * V**2 * S * C_D0
    D_i = 0.5 * rho * V**2 * S * k * CL_v**2
    D_t = D_p + D_i
    L_v = 0.5 * rho * V**2 * S * CL_v
    
    bars = ax1.barh(['寄生阻力\nParasitic', '诱导阻力\nInduced', '总阻力\nTotal'], 
                     [D_p, D_i, D_t], color=['#16a085', '#e74c3c', '#2980b9'], height=0.6)
    for bar, val in zip(bars, [D_p, D_i, D_t]):
        ax1.text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2, f'{val:.1f}N', va='center', fontsize=10)
    ax1.set_xlim(0, max(25, D_t*1.3))
    ax1.set_title(f'速度 V = {V:.1f} m/s | 升力 L = {L_v:.1f}N (需≥{W:.0f}N)', fontsize=12, fontweight='bold')
    
    # 下图: 四个关键曲线上标记当前位置
    # Mini plot of D/V curve with current point
    ax2.plot(V_range, drag_vals, 'b-', lw=1.5, alpha=0.3, label='阻力曲线')
    ax2.plot(V_range, power_vals/10, 'g-', lw=1.5, alpha=0.3, label='功率/10')
    ax2.plot(V_range, LD_vals, 'r-', lw=1.5, alpha=0.3, label='L/D')
    
    ax2.axvline(V, color='#e67e22', lw=2, alpha=0.8)
    ax2.plot(V, drag(V), 'bo', ms=10, label=f'当前阻力={drag(V):.1f}N')
    ax2.plot(V, power_required(V)/10, 'go', ms=10, label=f'当前功率={power_required(V)/10:.1f}W/10')
    ax2.plot(V, L_over_D(V), 'ro', ms=10, label=f'当前 L/D={L_over_D(V):.1f}')
    
    ax2.axvline(V_min_drag, color='#2980b9', ls='--', lw=1, alpha=0.6, label=f'最大航程 V={V_min_drag:.0f}')
    ax2.axvline(V_min_power, color='#8e44ad', ls='--', lw=1, alpha=0.6, label=f'最大航时 V={V_min_power:.0f}')
    
    # Annotate flight mode
    if abs(V - V_min_drag) < 1:
        mode = '← 最大航程速度!'
    elif abs(V - V_min_power) < 1:
        mode = '← 最大航时速度!'
    elif V < V_min_power:
        mode = '(低于最有利速度 → 诱导阻力主导)'
    elif V < V_min_drag:
        mode = '最大航时区域'
    else:
        mode = '(高于最有利速度 → 寄生阻力主导)'
    
    ax2.set_title(mode, fontsize=11, color='#e67e22')
    ax2.set_xlabel('速度 V (m/s)'); ax2.set_ylabel('力/功率/比值')
    ax2.legend(fontsize=7, loc='upper right', ncol=2)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(V_stall, V_max)

frames = 120
ani = FuncAnimation(fig, draw_frame, frames=frames, interval=120)
ani.save(os.path.join(OUT, "uav-speed-demo.gif"), writer=PillowWriter(fps=12))
plt.close(fig)
print("GIF saved")
print("\n=== DONE ===")
