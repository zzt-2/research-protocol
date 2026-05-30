# PROMPT-009: 仿真穷举探索 — 从 EXP-001 开始

> 用途：新对话中启动系统性仿真探索
> 专题：thesis-sim-exploration
> 目标：修复并扩展仿真，逐实验验证，找到支撑 L2 创新的性能增益

## 背景

硕士论文 Ch4 声称三个湍流自适应公式，但当前仿真 sim_direction_a.py 有严重缺陷：
- 只自适应了 DPLL 带温（1/3 公式），FOE 和 VV 窗口固定
- 强湍流下增益仅 0.5 dB，不够支撑方法级创新声称
- MMSE 预补偿非标准，序列太短

导师预期 L2（方法级创新），需要找到 ≥1 dB 的性能增益。

## 方法论

分层试错法 + 穷举探索：
1. 每个假设 = 一个实验编号（EXP-XXX），一个独立仿真文件
2. 先修现有代码（Tier 1），再做参数扫描（Tier 2），再试架构变体（Tier 3）
3. 有增益的深挖，没增益的快速截断
4. 结果记录到专题的 topic-index.md 探索表

## 本轮任务：EXP-001 + EXP-002 + EXP-003

这三个是一体的——修完一起跑。

### EXP-001：全三公式自适应
修改 `carrier_recovery_adaptive` 让 FOE 窗口和 VV 窗口也用 adaptive_params 的结果。

### EXP-002：去掉 MMSE 预补偿
删除 run_mve_trial 中的 MMSE 预补偿，用标准接收链路。如果深衰落导致问题，尝试幅度归一化方案。

### EXP-003：加长序列
Ns=20000, n_trials=50。

### 修完后运行

1. 三档湍流 × 固定/自适应 × 多 SNR（10-30 dB，步进 2 dB）
2. 产出 BER vs SNR 曲线图
3. 记录强湍流下的增益（dB）
4. 结果写入 `topic-index.md` 探索表

### 如果时间允许，接着跑 EXP-004/005/006（参数扫描）

## 判据

| 增益（强湍流） | 判定 | 后续 |
|----------------|------|------|
| ≥3 dB | **L2 成立** | 深挖该方向，做消融实验 |
| 1-3 dB | L1→L2 边界 | 继续 Tier 2/3 探索 |
| <1 dB | L1 确认 | 调整创新点定位，继续 Tier 3/4 |

## 代码版本管理

- 创建 `sim_exp_001_full_adaptive.py`（基于 sim_direction_a.py 修改）
- 实验文件放在 `projects/thesis-figures/simulation/`
- 结果记录到 `.sessions/thesis-sim-exploration/topic-index.md`

## 探索表位置

`.sessions/thesis-sim-exploration/topic-index.md` — 包含全部实验假设和结果，持续更新。

## 必读文件

1. `.sessions/thesis-sim-exploration/topic-index.md` — 探索表（本专题核心）
2. `projects/thesis-figures/simulation/sim_direction_a.py` — 当前仿真代码
3. `毕设/写作材料/thesis-status.md` — 全局状态
4. `毕设/写作材料/formulas-ch3ch4-sync.md` — 三个自适应公式

## 验证环境

```bash
~/.venvs/torch/bin/python
```
