# Verifications — 论文写作专题（自适应 CPR 方向）

## V001: Fig.2--4 数据、视觉与输出格式验证

> date: 2026-07-13
> 关联：S011 / D009 / R018

### 验证项

- [x] 三个绘图脚本可独立运行并生成 PDF/PNG。
- [x] Fig.2 保留六场景且无卖点数字、箭头和图内 headline。
- [x] Fig.3 共 3×7=21 点，逐点等于 `_a4_switch_30seed_fixed.json` 的 `switch_vs_nda_db_mean`，正值方向为相对固定 NDA 的 BER reduction。
- [x] Fig.4 的显示曲线、交叉点求解与标记位置共用原始点间 log-BER 线性插值，交叉点为 18.0/16.9/10.7 dB（显示精度一位小数）。
- [x] 三图坐标命名、字体层级和图例在最终尺寸下可读；PDF 为矢量输出且字体嵌入。
- [x] Fig.1 未修改；未运行实验或改动结果 JSON。

### 证据

- `python -m py_compile plot_fig2_ber.py plot_fig3_gain.py plot_fig4_crossover.py`：exit 0。
- 三个脚本重新运行：exit 0；Fig.3 输出 21 个源数据值；Fig.4 输出 weak=18.0129、moderate=16.8661、strong=10.7026 dB。
- PNG：Fig.2 2291×2640 @ 320 dpi；Fig.3 1072×801 @ 300 dpi；Fig.4 2113×1153 @ 300 dpi。
- PDF：Fig.2 7.16×8.25 in；Fig.3 3.5686×2.6735 in；Fig.4 7.0524×3.8485 in；均为矢量内容且字体嵌入。
- 独立 verifier 复核结论：Critical=0，Important=0，PASS。
- 目标脚本及本轮新增规格/日志的定向 `git diff --check`：exit 0。全仓检查仅命中既有无关文件 `.sessions/2026-06-20-problem-driven-redirection/decisions.md:1300` 的 EOF 空行，本轮未改该文件。

### 结论

PASS
