# PROMPT-002: Ch3→Ch4 衔接实验

> 专题: thesis-simulation-consolidation | 续接: S002
> Python: `~/.venvs/torch/bin/python`
> 工作目录: `projects/simulation/`（新）

## 背景

Ch3 的级联灵敏度分析（`sim_cascade_robustness.py`）发现"载波同步对估计误差鲁棒（NMSE≥-10dB 全通过）"。但 Ch4 所有仿真都用 oracle h（完美信道估计），两者之间缺少直接连接。

**需要补的实验**：在 Ch4 载波同步仿真中引入非完美 h，量化估计误差对载波同步 BER 的实际影响。如果结果确实鲁棒，就论证了 Ch4 使用 oracle h 假设的合理性，同时强化 Ch3→Ch4 的叙事衔接。

## 必读

1. `projects/simulation/SPEC.md` — 仿真规范
2. `projects/simulation/common.py` — 公共模块（新）
3. `.sessions/thesis-simulation-consolidation/S002-ch4-audit-report.md` — 审计报告
4. `projects/thesis-figures/simulation/sim_cascade_robustness.py` — 现有级联灵敏度分析（参考设计）

## 实验设计

### 实验目标

回答问题：信道估计误差对载波同步 BER 的影响有多大？在什么精度水平下可以安全忽略？

### 实验方案

在 `projects/simulation/experiments/` 下新建 `bridge_ch3_ch4.py`。

**核心思路**：在 Ch4 仿真中，MMSE 均衡和 DPLL/KF 不使用 oracle h，而是使用含噪声的 ĥ。

**ĥ 生成方式**：
```python
def noisy_h(h_true, nmse_db):
    """生成含噪信道估计"""
    nmse = 10 ** (nmse_db / 10)
    noise_var = nmse  # E[|h_hat - h|^2] = nmse * E[|h|^2], E[|h|^2]≈1
    h_hat = h_true + np.sqrt(noise_var / 2) * (np.random.randn(*h_true.shape) + 1j * np.random.randn(*h_true.shape))
    return h_hat
```

**注意**：h 是实值辐照度（归一化），不是复信道系数。所以噪声应该是实值的：
```python
h_hat = h_true + np.sqrt(nmse) * np.random.randn(*h_true.shape)
h_hat = np.maximum(h_hat, 0.01)  # 避免负值
```

### 测试矩阵

| 方法 | 湍流 | NMSE (dB) | γ̄ (dB) | Ns | 种子数 |
|------|------|-----------|---------|-----|-------|
| FOE+VV | weak/mod/strong | oracle, -5, -10, -15, -20 | 20 | 10000 | 10 |
| FOE+DPLL | weak/mod/strong | oracle, -5, -10, -15, -20 | 20 | 10000 | 10 |
| FOE+VV+DPLL | weak/mod/strong | oracle, -5, -10, -15, -20 | 20 | 10000 | 10 |

- NMSE = 0 dB：估计≈随机猜测（worst case）
- NMSE = -5 dB：很差
- NMSE = -10 dB：LS 估计器典型水平
- NMSE = -15 dB：MMSE 估计器典型水平
- NMSE = -20 dB：接近完美
- oracle：无噪声 h（当前 Ch4 仿真假设）

### 关键点

1. **使用 common.py 的函数**：`generate_shared_realization`、`chain_foe_vv`、`chain_foe_dpll` 等
2. **统一用 resolve_qpsk 评估**（与 D1/D2 一致）
3. **noisy h 影响两个地方**：
   - MMSE 均衡：`rx * np.sqrt(h_hat) / (h_hat + 1/gamma_bar)`
   - 如果 KF pilot 用导频估计 h，也用 noisy h（但本实验不涉及 KF）
4. **结果输出**：JSON + 图表

### 预期结果

基于 `sim_cascade_robustness.py` 的已有结论（6/6 PASS），预期载波同步对 NMSE≥-10dB 鲁棒。

## 不要做什么

- 不开发新方法
- 不修改 common.py（只导入使用）
- 不涉及 KF（KF 增益已消失，不需要测）
- 不做 SNR 扫描（只测 20dB）
- 不修改旧目录的任何文件

## 输出

1. 结果 JSON：`projects/simulation/results/bridge_ch3_ch4_results.json`
2. BER vs NMSE 曲线图：`projects/simulation/figs/fig_bridge_ber_vs_nmse.png`
3. Session note：`.sessions/thesis-simulation-consolidation/S003-bridge-experiment.md`

结果报告需包含：
- 各方法 × 各湍流 × 各 NMSE 的 BER 数值表
- "安全阈值"：BER 相对 oracle 退化 <1dB 的最低 NMSE
- 对 Ch3→Ch4 叙事衔接的影响分析

## 完成后

更新 topic-index.md：新增 S003 进展线索。
