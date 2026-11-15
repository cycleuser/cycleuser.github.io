# 考研数学配图生成说明

本目录下的图片分三类。

## 一、Python 脚本生成的图（全部可复现）

| 脚本 | 产出的文件 |
|---|---|
| `make_shuzhi_methods.py` | `shuzhi-newton.gif`、`shuzhi-damped-newton.gif`、`shuzhi-simplified-newton.gif`、`shuzhi-secant.gif`、`shuzhi-bisection.gif`、`shuzhi-false-position.gif`、`shuzhi-fixed-point.gif`、`shuzhi-muller.gif`、`shuzhi-golden-section.gif`、`shuzhi-hill-climb.gif`、`shuzhi-steepest-descent.gif`、`shuzhi-rk4.gif`、`shuzhi-quadratic.png`、`shuzhi-quintic.png`、`shuzhi-transcendental.png` |
| `make_shulie_figs.py` | `shulie-epsilon-n.png`、`shulie-monotone.png` |
| `make_cauchy_visual.py` | `cauchy-visual.png` |
| `make_arclen_volume.py` | `ga-ds-element.gif`、`ga-ds-accumulate.gif`、`ga-volume-sweep-3d.gif` |
| `make_cycloid_arcvol.py` | `ex-cycloid-arc-vol.png` |
| `make_polar_convergence.py` | `pc-area-convergence.png` |
| `make_geo2_rolls.py` | `geo2-astroid-roll.gif`、`geo2-hypocycloid-3.gif`、`geo2-hypocycloid-4.gif`、`geo2-hypocycloid-5.gif` |
| `make_involute_roll.py` | `geo2-involute-roll.gif` |
| `make_iris*.py`、`make_comb_*.py`、`make_polar_*.py`、`make_google*.py` 等 | 附录 5–8 的解析几何、极坐标、命题逻辑、排列组合、Iris 演示图 |

重新生成全部图片：

```bash
cd output/img/kaoyan-math
for f in make_*.py; do python3 "$f"; done
```

依赖：`matplotlib`、`numpy`、`Pillow`；部分脚本还需要 `scikit-learn`（Iris）、`cairosvg`（SVG→PNG）。

## 二、原始教材扫描图（`*.jpg`，195 张）

文件名形如 `jichu-gaoshu-001.jpg`、`zhenti-1-002.jpg`，是从原书 PDF 里裁出来的例题与插图，
由 Python 脚本无法重绘，只能替换成重绘版本或删掉。

## 三、第三方素材（需注明出处）

- `wm-two-gears-11.gif`、`wm-two-gears-13.gif`：Wikimedia Commons，作者 Jahobr，许可 CC BY-SA 4.0，
  用于附录 6 齿轮啮合的说明。原文已标注来源，替换时需保留署名。

## 引用方式

markdown 里统一写成：

```markdown
https://raw.githubusercontent.com/cycleuser/cycleuser.github.io/main/img/kaoyan-math/<文件名>
```
