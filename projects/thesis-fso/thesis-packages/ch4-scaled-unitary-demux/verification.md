# Verification — Ch4 write package

> 当前阶段：`DELIVER`
> 终态：`CH4_WRITE_PACKAGE_READY`

## 1. 生成身份

| artifact | authoritative input | command | result |
|---|---|---|---|
| CSV + BER SVG/PNG | `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/confirmation_raw.json` | `python plot_ch4_results.py` | PASS；脚本不读取 confirmation aggregate/development |
| raw/V027 consistency | 同上 + D052/V027 锚点 | `python plot_ch4_results.py --check-only` | PASS；4 cell + pooled Np=2 |
| method SVG/PNG | semantic brief + implementation formulas | `python generate_method_figure.py` | PASS；editable text/shape SVG + PNG preview |

执行环境：Windows PowerShell，Python 3 + NumPy + Matplotlib；工作目录为本包目录。最终 fresh build=`2026-08-30T07:33:08+08:00` 至 `07:33:12+08:00`，两个生成脚本均 exit 0。

| artifact | bytes | SHA256 |
|---|---:|---|
| `data/ch4-confirmation-summary.csv` | 907 | `12f1248d10e85b15e9f7e4b9717dd0240573083bfdd7daae6387f24b56165d7c` |
| `figures/ch4-ber-comparison.svg` | 86858 | `cc737012f75d4c506d11673292b3185141e57a1be1ce3ddf195a36a12fbd637a` |
| `figures/ch4-ber-comparison.png` | 114497 | `72413c7c92f5d84892e3efce103b48011218c39e77cc9c9ec75fdb85d765b124` |
| `figures/ch4-method-flow.svg` | 27423 | `e496e32c1f50cdb316cca6f4fa3fc0f7f61d639937b97ab191e44a618b3397c9` |
| `figures/ch4-method-flow.png` | 143619 | `d6fff2a6ba590b4a41886443d9d667089708cd0a71728af852751739a6d83b20` |

## 2. CSV 对 raw/V027 逐值检查

| row | B2 BER | C4 BER | C4−B2 mean | 95% CI | relative | V027/D052 |
|---|---:|---:|---:|---:|---:|---|
| 14 dB, Np=2 | 0.08277035 | 0.07667112 | -0.00609922 | [-0.00954738,-0.00306168] | 7.37% | PASS |
| 14 dB, Np=4 | 0.07178736 | 0.06990385 | -0.00188351 | [-0.00354064,-0.00019817] | 2.62% | PASS |
| 18 dB, Np=2 | 0.03875256 | 0.03550529 | -0.00324726 | [-0.00548053,-0.00143516] | 8.38% | PASS |
| 18 dB, Np=4 | 0.02216578 | 0.02104330 | -0.00112247 | [-0.00216106,-0.00026414] | 5.06% | PASS |
| pooled Np=2 | 0.06076145 | 0.05608821 | -0.00467324 | [-0.00686385,-0.00282661] | 7.69% | PASS |

额外确定性门：256 unique seeds；每 cell 64 windows；每 arm/window payload bits=32768；BER 等于 raw numerator/denominator；arms=`B0/B1/B2/C4/O1`；pooled Np=2=128 paired windows。

## 3. 图形与语义 QA

### BER 结果图

- 四格全部存在，B2/C4 为主色，B0/O1 保留上下文；B1 仍完整保存在 CSV。
- 纵轴固定从 0 起，未裁轴放大差异；每格标注 raw-derived relative reduction。
- 颜色同时配合 hatch，黑白打印仍可区分；legend 不遮挡 bars。
- PNG 为 1760×880 preview；SVG 保留文本与矢量 bar。

### 方法图

- 标签包含双偏振短导频、pilot-LS、SVD/缩放酉投影、逆矩阵解复用、两路 Ch3 CPR。
- 蓝色实线为 payload 数据流；橙色点划线为 pilot estimation/control。
- 未画 PDL/PMD/FIR/LDPC/时变 SOP/CFO 或 `rho` gate。
- 首版的橙色 `W` 控制箭头压字已局部修复；fresh PNG 中诊断文字移至左侧空白走廊，箭头源/目标与冻结标签不变。
- 独立 reviewer 与主控均实际查看修复后 PNG；未见文字截断、错误端点或新增重叠。

## 4. Paper-writing gate report

| Gate | status | evidence | remaining action |
|---|---|---|---|
| applicable constraints | PASS | `venue=N/A`；T073 内部材料范围 | 无 |
| artifact freshness | PASS | final build 时间、bytes、SHA256 见上 | 无 |
| source-build success | PASS | 两个生成脚本 exit 0 | 无 |
| claims/evidence | PASS | fact matrix + exact source pointers；review P0/P1=0/0 | 无 |
| numbers/metrics | PASS | raw-only reducer + V027 anchors；独立最大绝对差 `4.8633e-11` | 无 |
| method/formula | PASS | algorithm box + caller/callee trace；同 `UV^H` 身份独立复核 | 无 |
| information access | PASS | receiver_action 不含 truth；O1/scorer 隔离 | 无 |
| metric signature | PASS | counts/denominator/bootstrap 与 pooled 定义独立复核 | 无 |
| state lifecycle | PASS | per-window PCG64；无跨 window state | 无 |
| citations | PASS | ledger 标明 exact local pointers 与摘要级候选边界 | 正式落 bib 时仍须核对候选全文 |
| figures/tables | PASS | 两 SVG+PNG+CSV；P2 修复后独立视觉复核 | 无 |
| formal paper prose | N/A | 本包不改正式论文正文 | 无 |
| independent review | PASS | `independent-review.md`；fix re-review `0/0/0` | 无 |

## 5. 独立 reviewer

独立 reviewer 未参与生成，直接从 raw spot-check CSV、核对 B2/C4 实现身份、检查九类交付，并实际查看两张 PNG/SVG。首轮为 `P0/P1/P2=0/0/2`，两项均为局部视觉问题；修复后 fresh re-review 为：

- `remaining P0/P1/P2=0/0/0`
- `verdict=PASS`
- 完整证据：`independent-review.md`

据 T073 终态合同，本包满足 `CH4_WRITE_PACKAGE_READY`。该 terminal 只表示内部章级写作材料已就绪，不表示正式论文正文或完整论文实验已经完成。
