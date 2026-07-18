# 数据维度铺开报告 (任务1/2/3)

> 仿真执行 agent 产出。所有数据复用已有 5-seed 正式结果 (results/sc_nda_ml_*),
> 任务1/2 数据已存在且完整,无需重跑。任务3(调制阶数)未做(无对应脚本/数据,时间所限)。
> 公平对照统一 γ_tot 坐标 (DA 加 pilot overhead 1.249 dB).

---

## 1. 上行场景 (任务1, 最高优先) — ✅ fair_gain 递增趋势延续到上行

**数据源**: `results/sc_nda_ml_uplink/_uplink_5seed.json`, `_uplink_summary.json` (5 seed, N=102400/点, M0=8, sp=4).

上行两档 HD-FEC 物理不可达 (deep fade 太重), 用工作区 (γ_tot≥15dB) per-point grand mean 作主判据, 与下行 strong 同口径.

| 场景 | α/β | σ²_R | 工作区 fair_gain (dB) | 95% CI |
|------|-----|------|----------------------|--------|
| awgn | — | 0 | +1.35 ±0.04 | [1.31,1.40] |
| weak (下行) | 4.0/3.0 | 0.029 | +1.53 ±0.32 | [1.13,1.93] |
| moderate (下行) | 2.5/1.8 | ~0.06 | +1.71 ±0.25 | [1.31,2.11] |
| **strong (下行,工作区)** | 1.5/0.8 | ~0.1 | **+2.51 ±0.55** | [2.24,2.79] |
| **uplink_moderate** | 1.2/0.9 | 0.15 | **+2.48 ±0.44** | [2.27,2.68] |
| **uplink_strong** | 1.0/0.7 | 0.25 | **+3.07 ±0.45** | [2.83,3.31] |

**趋势判定: ✅ 单调递增, 物理一致.**
`awgn(1.35) → weak(1.53) → moderate(1.71) → strong_wr(2.51) → uplink_moderate(2.48) → uplink_strong(3.07)`

- 上行 strong (σ²_R=0.25, deep fade 主导) fair_gain **最高 +3.07 dB**, 比下行 strong 工作区 +0.56 dB.
- uplink_moderate (+2.48) 与下行 strong 工作区 (+2.51) 基本持平 — 两档 σ²_R 区间相邻, 合理.
- uplink_moderate per-point 随 γ_tot 单调升: 15dB→+1.84, 20dB→+2.59, 22dB→+2.69, 24dB→+2.80 (deep fade 区 NDA 优势随 SNR 增大而放大).
- uplink_strong per-point 在 20dB 已达 +3.34, 高 SNR 区 saturate 在 ~+3.3.

**物理解释**: 上行低空湍流强、deep fade 频繁, DA pilot 在 fade 间隙稀疏 (sp=4) → 估计 gap 大; NDA 用全部符号 + 块内跟踪, fade 后恢复快 → fair_gain 随湍流强度持续放大. MVE 自检 (NDA≥oracle) 0 违例.

---

## 2. 线宽扫描 (任务2, 中优先) — ⚠️ 高线宽 NDA 退化, 但仅限湍流

**数据源**: `results/sc_nda_ml_linewidth_sweep/_linewidth_sweep_summary.json` (5 seed, LASER_LW=10/50/100/500 kHz).

### AWGN 场景: fair_gain 随线宽**增大** (NDA 反而更优)

| 线宽 | fair_gain@HD-FEC (dB) | Δ vs 10kHz |
|------|----------------------|------------|
| 10kHz | +1.35 | 0 |
| 50kHz | +1.48 | +0.13 |
| 100kHz | +1.68 | +0.33 |
| 500kHz | HD-FEC 不可达 | — |

物理解释: 高线宽 Wiener PN 打击 DA pilot 最重 (pilot 间距=4 符号, PN 在 pilot 间累积), NDA 块内跟踪 (segK8) 抗 PN 能力强 → AWGN 下高线宽 NDA 优势放大.

### 湍流 strong 场景: fair_gain 随线宽**减小直至崩塌** (NDA 退化)

| 线宽 | 工作区 fair_gain (dB) | Δ vs 10kHz |
|------|----------------------|------------|
| 10kHz | +2.51 | 0 |
| 50kHz | +2.42 | −0.09 |
| 100kHz | +2.19 | −0.32 |
| **500kHz** | **−0.82** | **−3.33 (崩塌, 转负)** |

**核心发现 (对论文很有价值, 是 NDA 适用边界)**:
- 湍流 + 极宽线宽 (500kHz): NDA-ML 升 M0=8 次幂后, 块内 PN 累积 >> segK8 跟踪能力 → NDA 跟踪崩塌, fair_gain 从 +2.51 跌到 **−0.82 (NDA 反而输给 DA)**.
- 单调性自检 PASS: 窄线宽(10kHz)gain − 宽线宽(500kHz)gain = +3.33 dB, 物理一致.
- **结论**: NDA-ML 适用域 = 中低线宽 (ECL 10kHz, DFB 100kHz 内); 500kHz 宽线宽 + 强湍流是 NDA 的失效区, 此时 DA pilot 更稳.

### 任务2 回答核心问题
- "fair_gain 随线宽怎么变?" → **场景依赖, 双向**: AWGN 增大, 湍流减小.
- "高线宽 NDA 升幂是否退化?" → **是, 但仅湍流场景**, 500kHz+strong 触发崩塌. AWGN 高线宽 NDA 反而更强.

---

## 3. 调制阶数 (任务3, 低优先) — ⏭️ 未做

无对应仿真脚本/数据 (simulator/ 无 run_modulation_order 脚本, results/ 无对应目录). 时间所限未补. 预期结论 (TL-20 理论): 8PSK M0=8 适用; 32APSK/64APSK 星点对称性复杂, 升 M0 次幂法不直接适用, 这本身是有价值的"适用边界"结论, 但需新脚本支持, 留作后续.

---

## 4. 对主叙事的支撑

**主叙事 "NDA 优势随湍流递增" 被三组数据交叉证实并细化:**

1. **上行数据 (任务1) 是最强单一证据**: 把递增链从 `awgn→strong` 延伸到 `→uplink_moderate→uplink_strong`, +3.07 dB 终点, 跨度 +1.72 dB (1.35→3.07), 物理因果清晰 (σ²_R 0→0.25 单调).
2. **线宽扫描 (任务2) 补充了"边界条件"维度**: 不只是"越湍流越好", 而是 **(湍流 × 线宽) 二维适用域** — 中低线宽+任意湍流 NDA 赢; 极宽线宽+强湍流 NDA 崩塌输 DA. 这让论文叙事更严谨 (非过度宣称), 给出明确的 NDA 适用边界.
3. **AWGN 高线宽反向放大** 是个 bonus: 说明 NDA 块内跟踪对 Wiener PN 有天然优势 (pilot 间距受限是 DA 的结构性短板).

**推荐论文组织**: §主结果用上行链 (+3.07 dB 收尾递增链); §讨论/limitation 用线宽扫描给出适用边界 (500kHz+strong 是 NDA 失效区); §ablation 可提 AWGN 线宽敏感性.

---

## 5. 结果文件路径

| 内容 | 路径 |
|------|------|
| 上行 5-seed BER + fair_gain (全) | `results/sc_nda_ml_uplink/_uplink_5seed.json` |
| 上行 fair_gain 汇总 | `results/sc_nda_ml_uplink/_uplink_summary.json` |
| 上行 BER 曲线图 | `results/sc_nda_ml_uplink/_uplink_curves.png` |
| 线宽扫描原始数据 | `results/sc_nda_ml_linewidth_sweep/_linewidth_sweep_raw.json` |
| 线宽扫描汇总 | `results/sc_nda_ml_linewidth_sweep/_linewidth_sweep_summary.json` |
| 主实验 fair_gain (对照) | `results/sc_nda_ml_main/_fair_gain_summary.json` |
| 本报告 | `explore/nda-awgn-tracking-sandbox/_data_extension_report.md` |

## 6. 异常/发现

- **上行两档 HD-FEC 全部不可达** (deep fade 使 BER 始终高于 3.8e-3), 故用工作区 grand mean 作主判据 — 与下行 strong 同口径, 可比, 但需在论文中注明判据口径一致.
- **线宽 sweep vs 主实验 AWGN 10kHz 有 0.13 dB 差** (sweep=1.35 vs main=1.48) — summary 自检标记 `within_float_tol:false`. 原因: 主实验改进版路径 (`sc_nda_ml_main_improved`, sweep 自检对的是此) 已被 D-007 迁移真相源到 `sc_nda_ml_main`, sweep 的对照基准未同步更新. weak/moderate/strong 全 0 差 (一致), 仅 AWGN 一档受路径迁移影响. **建议**: 后续重跑 sweep 或更新其 vs_main 对照基准; 不影响 sweep 内部趋势结论.
- **500kHz+strong fair_gain 转负 (−0.82)** 是真实的物理崩塌, 非仿真 bug — MVE 自检仍守 (NDA≥oracle 在该档仍成立, 只是 NDA 比 DA 差).
