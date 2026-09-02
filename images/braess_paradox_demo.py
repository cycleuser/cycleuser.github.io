#!/usr/bin/env python3
"""
布雷斯悖论 (Braess's Paradox) GIF 动画
========================================
手动逐帧生成 GIF，确保色彩一致、帧数完整。
1. braess_4node_basic.gif     — 无捷径 → 加捷径 → 均衡恶化
2. braess_equilibrium.gif     — Nash均衡 vs 社会最优 成本曲线
3. braess_removal_fix.gif     — 有捷径 → 拆捷径 → 交通恢复

依赖: matplotlib, numpy, pillow
"""

import os
import glob as _glob
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import imageio.v3 as iio

# ================================================================
# 中文字体设置
# ================================================================
import matplotlib.font_manager as fm

_cache_dir = os.path.expanduser('~/.matplotlib')
for _f in (_glob.glob(os.path.join(_cache_dir, 'fontlist*.json')) +
           _glob.glob(os.path.join(_cache_dir, '*.cache'))):
    try:
        os.remove(_f)
    except Exception:
        pass
fm._load_fontmanager(try_read_cache=False)

FONT_CANDIDATES = [
    'Hiragino Sans GB', 'STHeiti', 'Songti SC', 'Kaiti SC',
    'Lantinghei SC', 'Heiti TC',
]

SELECTED_FONT = None
for font in FONT_CANDIDATES:
    try:
        fm.findfont(font, fallback_to_default=False)
        SELECTED_FONT = font
        break
    except Exception:
        continue

if SELECTED_FONT:
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = [SELECTED_FONT, 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ================================================================
# 全局参数
# ================================================================
TOTAL = 4000
DPI = 120
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 颜色
C_CONG  = '#E74C3C'
C_FIXED = '#2980B9'
C_CUT   = '#8E44AD'
C_BG    = '#FAFAFA'
C_NODE  = '#2C3E50'
C_GOOD  = '#27AE60'
C_BAD   = '#C0392B'
C_ROUTE_UP   = '#E74C3C'
C_ROUTE_DN   = '#2980B9'
C_ROUTE_THRU = '#8E44AD'

EDGE_COL = {'OA': C_CONG, 'BD': C_CONG, 'OB': C_FIXED, 'AD': C_FIXED, 'AB': C_CUT}
EDGE_LBL = {'OA': 'T/100', 'BD': 'T/100', 'OB': '45', 'AD': '45', 'AB': '0'}

NODES = {
    'O': np.array([0.0, 0.0]),
    'A': np.array([6.0, 3.5]),
    'B': np.array([6.0, -3.5]),
    'D': np.array([12.0, 0.0]),
}

EDGES = [
    ('O', 'A', 'OA'),
    ('O', 'B', 'OB'),
    ('A', 'D', 'AD'),
    ('B', 'D', 'BD'),
    ('A', 'B', 'AB'),
]


# ================================================================
# 绘图工具
# ================================================================
def _mid(a, b):
    return (a + b) / 2.0

def draw_node(ax, name, pos):
    c = plt.Circle(pos, 0.36, color=C_NODE, zorder=10, ec='white', linewidth=2)
    ax.add_patch(c)
    offs = {'O': (-0.7, -0.9), 'D': (0.7, -0.9), 'A': (0, 0.9), 'B': (0, -0.9)}
    ox, oy = offs.get(name, (0, -0.9))
    ax.annotate(name, pos + np.array([ox, oy]),
                fontsize=14, fontweight='bold', ha='center', va='center', color=C_NODE)

def draw_edge(ax, a, b, key, flow, show=True, alpha=1.0, style='-'):
    if not show and key == 'AB':
        return
    pA, pB = NODES[a], NODES[b]
    lw = 2.0 + 10.0 * flow / TOTAL
    color = EDGE_COL[key]
    if key == 'AB':
        arrow = FancyArrowPatch(pA, pB, arrowstyle='-|>', color=color,
                                lw=lw, alpha=alpha, linestyle=style,
                                connectionstyle="arc3,rad=0.35",
                                mutation_scale=16, zorder=4)
    else:
        arrow = FancyArrowPatch(pA, pB, arrowstyle='-|>', color=color,
                                lw=lw, alpha=alpha, linestyle=style,
                                mutation_scale=16, zorder=4)
    ax.add_patch(arrow)

    mid = _mid(pA, pB)
    offs = {'OA': (-1.5, 1.0), 'OB': (-1.5, -1.0),
            'AD': (1.5, 1.0), 'BD': (1.5, -1.0),
            'AB': (1.4, 0.0)}
    off = offs.get(key, (0, 0.6))
    bbox = dict(boxstyle='round,pad=0.15', facecolor='white',
                alpha=0.92, edgecolor=color, linewidth=1)
    ax.annotate(f'{EDGE_LBL[key]}\n{int(flow)}', mid + off,
                fontsize=7, color=color, ha='center', va='center', bbox=bbox, zorder=7)

def draw_time_badge(ax, minutes, is_bad=False):
    color = C_BAD if is_bad else C_GOOD
    bbox = dict(boxstyle='round,pad=0.4', facecolor='white',
                edgecolor=color, linewidth=2.5, alpha=0.94)
    ax.text(6.0, 5.6, f'{minutes} 分钟/人', fontsize=14, fontweight='bold',
            ha='center', va='center', bbox=bbox, color=color, zorder=15)

def draw_phase_label(ax, text, is_bad=False):
    color = C_BAD if is_bad else C_GOOD
    bbox = dict(boxstyle='round,pad=0.4', facecolor='white',
                edgecolor=color, linewidth=1.8, alpha=0.94)
    ax.text(6.0, -5.3, text, fontsize=11.5, fontweight='bold',
            ha='center', va='center', bbox=bbox, color=color, zorder=15)

def setup_ax(ax, title=None):
    ax.set_xlim(-2.5, 15)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=15, fontweight='bold', pad=14, color='#2C3E50')


def compute_flows(shortcut_count):
    x = shortcut_count
    rest = TOTAL - x
    upper = rest / 2
    lower = rest / 2
    return {'OA': upper + x, 'OB': lower, 'AD': upper, 'BD': lower + x, 'AB': x}


# ================================================================
# 帧渲染 → PIL Image
# ================================================================
def render_frame(fig):
    """渲染当前 figure 为 numpy 数组 (RGB)"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=DPI, facecolor=C_BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.1)
    buf.seek(0)
    return iio.imread(buf)


def save_gif(frames, durations, save_path):
    """保存帧列表为 GIF"""
    iio.imwrite(save_path, frames, duration=durations, loop=0)
    print(f'  ✓ {os.path.basename(save_path)} ({len(frames)} frames, {sum(durations):.1f}s)')


# ================================================================
# GIF 1: 基础网络
# ================================================================
def create_gif1(save_path):
    fig, ax = plt.subplots(figsize=(12, 7.5))
    fig.patch.set_facecolor(C_BG)
    frames = []
    durs = []

    # 阶段定义: (start_frame, end_frame_exclusive, shortcut_flow_fn, phase_text_fn, is_bad_fn)
    # 每帧都有细微变化避免被去重（边缘流量数字本身就在变化）

    def render_scene(f, sc, phase, is_bad, show_sc, sc_edge_alpha=1.0):
        ax.clear()
        setup_ax(ax, '布雷斯悖论 — 基础4节点网络')
        tt = int(65 + 15 * sc / TOTAL) if sc > 0 else 65

        flows = compute_flows(sc)

        for a, b, k in EDGES:
            if k == 'AB':
                if not show_sc:
                    continue
                draw_edge(ax, a, b, k, flows.get(k, 0), show=True, alpha=sc_edge_alpha)
                continue
            draw_edge(ax, a, b, k, flows.get(k, 0))
        for name, pos in NODES.items():
            draw_node(ax, name, pos)

        draw_time_badge(ax, tt, is_bad)
        draw_phase_label(ax, phase, is_bad)

        if sc == 0:
            ax.annotate('上路 2000辆', NODES['A'] + np.array([-0.3, 0.6]),
                       fontsize=9, color=C_ROUTE_UP, fontweight='bold', ha='center')
            ax.annotate('下路 2000辆', NODES['B'] + np.array([-0.3, -0.6]),
                       fontsize=9, color=C_ROUTE_DN, fontweight='bold', ha='center')
        elif sc == TOTAL:
            ax.annotate('穿行路 4000辆 (全部!)', np.array([6.0, 0.0]),
                       fontsize=11, color=C_CUT, fontweight='bold', ha='center',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                 edgecolor=C_CUT, linewidth=1.5, alpha=0.9))

        return render_frame(fig)

    # Phase 1 (static): 原始路网, 无捷径 — 1 frame, 1.5s
    frames.append(render_scene(0, 0, '原始路网 (无捷径) — 每人 65 分钟', False, False))
    durs.append(1.5)

    # Phase 2 (animated): 捷径出现, 车流转移
    n_transition = 25
    for i in range(n_transition):
        prog = (i + 1) / n_transition
        sc = int(prog * TOTAL)
        # 渐变显示捷径
        edge_alpha = min(1.0, (i / max(1, n_transition * 0.3)))
        show_sc = i >= 2
        frames.append(render_scene(i, sc,
            f'捷径出现 — 车流正在转移 ({sc}辆走捷径)',
            sc > 500, show_sc, edge_alpha))
        durs.append(0.12)

    # Phase 3 (static): 新均衡 — 1 frame, 2.0s
    frames.append(render_scene(0, TOTAL,
        '新Nash均衡 — 每人 80 分钟 (更慢!)', True, True, 1.0))
    durs.append(2.0)

    plt.close(fig)
    save_gif(frames, durs, save_path)


# ================================================================
# GIF 2: 均衡分析 — Nash均衡 vs 社会最优
# ================================================================
def create_gif2(save_path):
    fig, (ax_net, ax_cost) = plt.subplots(1, 2, figsize=(18, 7),
                                           gridspec_kw={'width_ratios': [1.1, 1]})
    fig.patch.set_facecolor(C_BG)
    frames = []
    durs = []

    x_vals = np.linspace(0, TOTAL, 200)
    c_thru  = 40 + x_vals / 100
    c_route = 65 + x_vals / 200
    c_social = (x_vals * c_thru + (TOTAL - x_vals) * c_route) / TOTAL

    def render_scene(sc, phase, is_bad, show_sc):
        ax_net.clear()
        ax_cost.clear()
        setup_ax(ax_net, '路网流量分布')
        ax_cost.set_facecolor(C_BG)

        tt = int(40 + sc / 100) if sc > 0 else 65
        flows = compute_flows(sc)

        for a, b, k in EDGES:
            if k == 'AB' and not show_sc:
                continue
            draw_edge(ax_net, a, b, k, flows.get(k, 0), show=show_sc)
        for name, pos in NODES.items():
            draw_node(ax_net, name, pos)

        draw_time_badge(ax_net, tt, is_bad)
        draw_phase_label(ax_net, phase, is_bad)

        if sc == 0:
            ax_net.annotate('上路 2000', NODES['A'] + np.array([-0.5, 0.6]),
                           fontsize=9, color=C_ROUTE_UP, fontweight='bold')
            ax_net.annotate('下路 2000', NODES['B'] + np.array([-0.5, -0.6]),
                           fontsize=9, color=C_ROUTE_DN, fontweight='bold')

        # 右侧成本曲线
        ax_cost.plot(x_vals, c_thru, color=C_CUT, lw=2.5, label='穿行路成本')
        ax_cost.plot(x_vals, c_route, color='#E67E22', lw=2.5, label='上路/下路成本')
        ax_cost.plot(x_vals, c_social, color='#7F8C8D', lw=2, ls='--', label='社会平均成本')

        ax_cost.scatter([TOTAL], [80], c=C_BAD, s=150, zorder=6, marker='X',
                       edgecolors='white', linewidths=1.5)
        ax_cost.annotate('Nash均衡\n(80分钟)', (TOTAL, 80),
                        xytext=(TOTAL-1300, 84), fontsize=9, color=C_BAD,
                        fontweight='bold', ha='center',
                        arrowprops=dict(arrowstyle='->', color=C_BAD, lw=1.5))

        ax_cost.scatter([0], [65], c=C_GOOD, s=200, zorder=6, marker='*',
                       edgecolors='white', linewidths=1.5)
        ax_cost.annotate('社会最优\n(65分钟)', (0, 65),
                        xytext=(1100, 47), fontsize=9, color=C_GOOD,
                        fontweight='bold', ha='center',
                        arrowprops=dict(arrowstyle='->', color=C_GOOD, lw=1.5))

        cur_c = 40 + sc / 100
        ax_cost.scatter([sc], [cur_c], c='#2C3E50', s=140, zorder=7, marker='D',
                       edgecolors='white', linewidths=1.5)

        if sc > 2000:
            ax_cost.fill_between([TOTAL*0.55, TOTAL], 40, 90, alpha=0.06, color=C_BAD)
            ax_cost.text(TOTAL*0.78, 43, '个人理性 → 集体损失',
                        fontsize=9, color=C_BAD, ha='center', fontweight='bold')

        ax_cost.set_xlabel('走捷径的车数 (辆)', fontsize=11)
        ax_cost.set_ylabel('通行时间 (分钟)', fontsize=11)
        ax_cost.set_title('Nash均衡 vs 社会最优', fontsize=14, fontweight='bold')
        ax_cost.legend(fontsize=9, loc='upper left', framealpha=0.9)
        ax_cost.set_xlim(-100, TOTAL+100)
        ax_cost.set_ylim(36, 90)
        ax_cost.grid(True, alpha=0.2)
        ax_cost.set_xticks([0, 1000, 2000, 3000, 4000])

        return render_frame(fig)

    # Phase 1: 社会最优
    frames.append(render_scene(0, '社会最优 — 每人 65 分钟', False, False))
    durs.append(1.5)

    # Phase 2: 车流转移
    n_trans = 25
    for i in range(n_trans):
        prog = (i + 1) / n_trans
        sc = int(prog * TOTAL)
        frames.append(render_scene(sc,
            f'车流向捷径聚集 — {int(40+sc/100)} 分钟',
            sc > 400, i >= 2))
        durs.append(0.12)

    # Phase 3: Nash均衡
    frames.append(render_scene(TOTAL,
        'Nash均衡 — 每人 80 分钟 (更差!)', True, True))
    durs.append(2.0)

    plt.close(fig)
    save_gif(frames, durs, save_path)


# ================================================================
# GIF 3: 悖论修复 — 关路
# ================================================================
def create_gif3(save_path):
    fig, ax = plt.subplots(figsize=(12, 7.5))
    fig.patch.set_facecolor(C_BG)
    frames = []
    durs = []

    def render_scene(sc, phase, is_bad, sc_alpha=1.0, sc_style='-', show_blocked=False):
        ax.clear()
        setup_ax(ax, '布雷斯悖论的反直觉解法 — 封路反而改善交通')
        tt = int(40 + sc / 100) if sc > 0 else 65

        flows = compute_flows(sc)

        for a, b, k in EDGES:
            if k == 'AB':
                draw_edge(ax, a, b, k, flows.get(k, 0), show=True,
                         alpha=sc_alpha, style=sc_style)
                if show_blocked:
                    mid = _mid(NODES['A'], NODES['B']) + np.array([1.2, 0])
                    ax.annotate('已封闭 ×', mid, fontsize=10, color='#999',
                               fontweight='bold', ha='center',
                               bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                                         edgecolor='#ccc', alpha=0.85))
                continue
            draw_edge(ax, a, b, k, flows.get(k, 0))

        for name, pos in NODES.items():
            draw_node(ax, name, pos)

        draw_time_badge(ax, tt, is_bad)
        draw_phase_label(ax, phase, is_bad)

        if sc == 0:
            ax.annotate('上路 2000辆', NODES['A'] + np.array([-0.5, 0.6]),
                       fontsize=9, color=C_ROUTE_UP, fontweight='bold')
            ax.annotate('下路 2000辆', NODES['B'] + np.array([-0.5, -0.6]),
                       fontsize=9, color=C_ROUTE_DN, fontweight='bold')

        return render_frame(fig)

    # Phase 1: 有捷径, 拥堵
    frames.append(render_scene(TOTAL, '有捷径 — 每人 80 分钟 (拥堵)', True, sc_style='-'))
    durs.append(1.5)

    # Phase 2: 正在关闭
    n_trans = 25
    for i in range(n_trans):
        prog = (i + 1) / n_trans
        sc = int(TOTAL * (1 - prog))
        alpha = max(0.10, 1 - prog)
        style = '--' if prog > 0.4 else '-'
        phase = f'正在关闭捷径... 车流重新分散 ({TOTAL - sc}辆已离开)'
        frames.append(render_scene(sc, phase, sc > 500, alpha, style,
                                   show_blocked=(prog > 0.7)))
        durs.append(0.12)

    # 悖论高亮帧（额外加一帧停留）
    frames.append(render_scene(1000, '悖论! 封路反而改善交通', False, 0.3, '--', True))
    durs.append(1.0)

    # Phase 3: 封路完成
    frames.append(render_scene(0, '封路完成 — 每人 65 分钟 (恢复!)', False, 0.15, '--', True))
    durs.append(2.0)

    plt.close(fig)
    save_gif(frames, durs, save_path)


# ================================================================
# Main
# ================================================================
def main():
    print(f'使用字体: {SELECTED_FONT}')
    print(f'输出目录: {OUT_DIR}')
    os.makedirs(OUT_DIR, exist_ok=True)

    create_gif1(os.path.join(OUT_DIR, 'braess_4node_basic.gif'))
    create_gif2(os.path.join(OUT_DIR, 'braess_equilibrium.gif'))
    create_gif3(os.path.join(OUT_DIR, 'braess_removal_fix.gif'))

    print('\n全部完成!')


if __name__ == '__main__':
    main()
