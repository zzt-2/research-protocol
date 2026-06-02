# PROMPT-008: 仿真缺口补充

> 专题: thesis-writing-prep | 优先级: P1（开题后、正式论文前补完）
> Python: `~/.venvs/torch/bin/python`
> 工作目录: `projects/simulation/`

## 必读（按顺序读）

1. **`projects/simulation/SPEC.md`** — 仿真唯一真相源。信号模型、参数、方法定义全在这里
2. **`thesis-lessons.md`**（项目根目录）— 20 条教训。**必须逐条过一遍**，尤其是 TL-01（信号模型）、TL-09（KF bug）、TL-13（共享信道）、TL-20（先有预期再跑）
3. **`毕设/写作材料/verification/verification-report.md`** — 已完成的验证报告，了解已经做了什么、结论是什么
4. **`projects/simulation/common.py`** — 当前活跃代码，所有实验必须从这里导入

## 教训强制执行（TL-20）

**跑任何仿真前，先写理论预期**。本对话的每个实验，在执行前必须：
1. 说明预期结果（数量级、趋势、方向）
2. 如果结果偏离预期 >3×，暂停排查
3. 结果"出奇地好"时同样暂停（TL-12）

## 待补缺口（4 项）

### 缺口 1: NMSE 扩展至弱/强湍流

**现状**: `nmse_expanded.json` 只有中等湍流（α=2.5, β=1.8），5 个 SNR 点 (0-20dB)
**需要**: 补弱湍流（α=4.0, β=3.0）和强湍流（α=1.5, β=0.8）

**预期**:
- 弱湍流: h 波动小（接近 1），NMSE 影响应更小甚至为零
- 强湍流: h 波动大（0.01-5），MMSE 均衡系数受 h 影响更大，但 DPLL 带宽 B_L∝h 与 γ∝h 对消仍应成立
- 如果强湍流下 NMSE 突然有影响（>1dB），那是一个重要发现

**执行**: 改造 `nmse_expanded.json` 的生成脚本，加弱/强两档湍流。产出追加到 `nmse_expanded.json` 或新建文件。

### 缺口 2: 复数噪声模型

**现状**: 只测了两种实值噪声模型:
- A: 乘性 `h_noisy = h * (1 + noise)` (noise 实值)
- B: 加性 `h_noisy = h + noise` (noise 实值)

**需要**: 加复数噪声模型:
- C: `h_noisy = h * (1 + noise_amplitude) * exp(j * noise_phase)`
- noise_phase 应该有多大？参考文献中的信道估计 MSE。典型 NMSE=-10dB 时，noise_amplitude ~ 0.1，noise_phase ~ arctan(0.1) ≈ 0.1 rad

**预期**:
- 如果之前的数学推导正确（QPSK sign() 判决对正缩放免疫），复数噪声的相位分量可能：
  - 被 MMSE 均衡吸收（W = h*/(|h|²+c) 中 h* 的共轭会反转相位误差？）
  - 或者不被吸收，直接传递到判决变量中
- **不确定就对了** — 这正是需要验证的点
- 如果复数噪声下 BER 有显著变化（>1dB），之前的"QPSK 免疫"结论就需要限定条件

**注意**: 先读 `毕设/写作材料/verification/investigation-nmse-mmse-analysis.md` 和 `investigation-nmse-noise-model-comparison.md`，理解之前的噪声模型设计和数学推导，避免重复劳动或与已有分析矛盾。

### 缺口 3: DPLL ω_n 扫参

**现状**: VV/BPS 的 Nw 已扫（7 个值 × 3 湍流），但 DPLL 的 ω_n 未扫
**需要**: ω_n 扫参，至少 5 个值，覆盖合理范围

**参数范围**:
- SPEC.md 默认 ω_n = 8e6 rad/s，最优 ω_n = 20e6 rad/s
- 建议扫: [2e6, 5e6, 10e6, 20e6, 50e6, 100e6]
- 每个湍流等级一条 BER vs ω_n 曲线

**预期**:
- ω_n 太小: 跟踪不上频偏，BER 高
- ω_n 太大: 噪声带宽大，BER 也高
- 最优 ω_n 应在某个中间点，且可能随湍流强度变化
- 强湍流可能需要更大的 ω_n（因为深衰落块内相位跳变更剧烈）

**注意**: DPLL 的 ζ（阻尼系数）也需要考虑。SPEC.md 默认 ζ=√2/2。可以先固定 ζ 只扫 ω_n，如果时间允许再扫 ζ。

### 缺口 4: Nw 低 SNR 补种子

**现状**: `nw_sweep_low_snr.json` 只有 SNR=10/15dB × 2 seeds × VV/BPS
**需要**: 补到 10 seeds（与 20dB 的 `nw_sweep.json` 对齐）

**注意**: 不需要重新跑已有的 2 seeds，只需追加 8 个新 seeds。追加时必须用不同的随机种子（如 seed=1020, 1030, ..., 1090），确保与已有 seeds 不重复。

## 执行策略

### 每个实验的流程（强制）

1. **读相关代码**: `common.py` 中对应的函数，确认参数和实现
2. **写预期**: 在代码注释或日志中写明"预期 BER 在 X~Y 范围"
3. **跑仿真**: 使用 common.py 的函数，不从旧文件复制代码
4. **对照预期**: 偏离 >3× 立刻停止排查
5. **写结果**: JSON 结果写入 `projects/simulation/results/`，简要分析写入验证目录

### 批次安排

- **Batch 1**: 缺口 1（NMSE 弱/强湍流）— 改造脚本 + 跑 3 组（弱/中/强 × 5 SNR × 2 噪声模型）
- **Batch 2**: 缺口 2（复数噪声模型）— 加模型 C，跑中等湍流验证（如果中等有影响再扩展弱/强）
- **Batch 3**: 缺口 3（DPLL ω_n 扫参）— 6 个 ω_n × 3 湍流 × 10 seeds
- **Batch 4**: 缺口 4（Nw 低 SNR 补种子）— 追加 8 seeds × 2 SNR × 7 Nw × 2 方法 × 3 湍流

每个 batch 跑完后先检查结果是否符合预期，再开下一个。

## 不要做什么

- 不修改 common.py 的核心函数（如果需要修改，先讨论）
- 不修改 SPEC.md 中的参数定义
- 不写论文正文
- 不做新的文献检索
- 不创建新的仿真目录（所有代码放在 `projects/simulation/experiments/` 下）

## 产出

| 产出 | 路径 |
|------|------|
| NMSE 弱/强数据 | `results/nmse_turbulence_sweep.json` |
| 复数噪声数据 | `results/nmse_complex_noise.json` |
| DPLL ω_n 数据 | `results/dpll_omega_sweep.json` |
| Nw 低 SNR 补种子 | `results/nw_sweep_low_snr.json`（追加） |
| 分析摘要 | `毕设/写作材料/verification/phase2-results/supplementary-experiments.md` |

## 质量标准

1. 每个实验有理论预期文档化
2. 结果符合预期或偏离有合理解释
3. 至少 10 seeds（缺口 4 补完后）
4. 所有参数与 SPEC.md 一致
5. 代码从 common.py 导入，不复制粘贴
