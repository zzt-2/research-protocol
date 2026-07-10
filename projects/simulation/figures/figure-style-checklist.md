# CCISP 图表美化 Checklist

> 基于 S002 用户 5 条反馈（横向太扁/差别太小/点太稀疏/标志难看/线太粗）+ 会议论文惯例（R006 §1.2 对标结论）。
> 每张图生成后逐项打勾。违反 = 需修。

---

## 一、布局（解决「横向太扁」）

- [ ] 子图 aspect ratio > 0.8（宽:高，BER log-y 图纵向拉长让多 decade 可见）
- [ ] 多子图用 3×2 纵向（非 2×3 横向），让每子图更高更方
- [ ] figsize 匹配 IEEE 双栏宽度（单栏 ~3.5 inch，双栏 ~7 inch）；高度按内容给够
- [ ] tight_layout 不挤压子图标题/x轴标签
- [ ] 共享图例放底部（fig.legend），不占子图空间

## 二、线型与配色（解决「标志难看」「线太粗」）

- [ ] **用线型区分方法，不用 marker 形状**：DA=实线 / NDA=虚线 / Oracle=点线
- [ ] marker 只画原始数据点（小圆点 markersize≤3），不用方块/三角
- [ ] **linewidth ≤ 1.5**（主曲线 1.2-1.3，参考线 0.8）
- [ ] colorblind-safe 配色（Okabe-Ito 启发）：
  - DA-ML = `#0072B2`（蓝）
  - NDA-ML = `#D55E00`（朱红/橙红）
  - Oracle = `#009E73`（绿）
  - HD-FEC = `#999999`（灰）
- [ ] **不用红绿对**（色盲不友好）
- [ ] 黑白打印可读（线型可区分）

## 三、差距可视化（解决「差别太小」）

- [ ] 卖点场景（strong/uplink）在 NDA 显著赢的 SNR 点标「NDA +XdB」箭头注释
- [ ] 弱湍流场景（AWGN/weak）曲线几乎重叠时不强标差距（诚实：差距确实小）
- [ ] 可选 zoom inset 在卖点场景放大 DA/NDA 分离区
- [ ] Fig.3 净增益图卖点场景 marker 加粗 + 数字标注，弱湍流段浅色/虚线

## 四、数据点密度（解决「点太稀疏」）

- [ ] **插值画平滑曲线**（scipy interp1d cubic in log-BER domain），不重跑仿真
- [ ] 原始数据点仍标出（小圆点），区分「实测点」vs「插值连线」
- [ ] 30seed 主区间 + 5seed 补点合并，不丢失任何实测点
- [ ] **禁止伪造中间点**：插值仅用于视觉连续，不在正文声称「每 X dB 一个点」

## 五、坐标轴

- [ ] BER 用 log-y（semilogy / set_yscale('log')）
- [ ] 纵轴范围按场景自适应（守不变量 5 deep fade 正确表征）：
  - AWGN/weak/moderate：1e-6 到 1（能到 1e-5）
  - strong/uplink：1e-4 到 0.5（deep fade 不强凑 1e-5，对齐 Paillier JLT 2020 惯例）
- [ ] HD-FEC 参考线（3.8e-3）必画
- [ ] 横轴标签统一 `$\bar{\gamma}_d$ (dB)`（数据 SNR，非总 SNR）
- [ ] grid 只画 major（alpha 0.2），minor 几乎不可见（alpha 0.08）

## 六、标注与图例

- [ ] 子图标题用 `(a)`, `(b)`... 编号 + 场景描述
- [ ] crossover / 卖点点用箭头注释（arrowprops），不遮挡曲线
- [ ] 图例放子图右上或底部，不遮挡数据
- [ ] 字号：标题 9pt / 轴标签 8pt / 刻度 7-8pt / 注释 6.5-7pt
- [ ] 字体 serif（Times New Roman / STIX），匹配 IEEE 模板

## 七、数据完整性检查（TL-21 确定性验证）

- [ ] 图上数字与 `_fair_gain_summary_30seed.json` 一致（grep 核查，不凭印象）
- [ ] D004 口径：报 fair 前 grep `fair_comparison.py:109` 确认 fair = naive + 1.249
- [ ] 弱湍流 naive 归零数字真实但不进正文/不标在图上（导师第 3 点）
- [ ] 切换 vs DA 负增益不进图（导师第 3 点，只标 vs NDA 正增益）

---

## 附：现有脚本与数据源对照

| 图 | 脚本 | 数据源 | 状态 |
|---|---|---|---|
| Fig.1 系统框图 | 手绘 SVG | — | ⏳ 待画 |
| Fig.2 BER 主图 | `plot_fig2_ber.py` | main30seed + ext5seed×2 | ✅ v1 样图生成 |
| Fig.3 净增益 | `plot_fig3_gain.py` | `_fair_gain_summary_30seed.json` | ✅ v1 样图生成 |
| Fig.4 crossover | `plot_fig4_crossover.py` | BER 曲线（weak/mod/strong 三场景叠加） | ✅ v2 多场景 crossover |
| Tab.1 净增益表 | R007 §4.2 | 同 Fig.3 | ✅ 结构已定 |
