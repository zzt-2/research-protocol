# [S004] MVE-Contract Action Space Alignment Gap

> Date: 2026-05-17
> Trigger: leo-congestion-routing Execute Step 2 — GNN 无法超越 ECMP
> Root cause: MVE 用 K-path 离散动作 beat ECMP 12%，但 Contract 设计了 per-edge 连续动作（单路径路由），表达力不如 ECMP 多路径分流

## 问题描述

MVE (GW Step 4a) 验证了 GNN 在 66 节点 + 8% 故障下超越 ECMP 12%（D4）。结果被直接用于支持 Contract 假设。但 MVE 和正式模型使用了完全不同的架构：

| 维度 | MVE | Contract/正式模型 |
|------|-----|------------------|
| 动作空间 | 离散 K-path 选择 | 连续 per-edge weights |
| 路由方式 | 逐流顺序路由 | 同时路由所有流 |
| 奖励 | delta MLU | 绝对 MLU |
| 路径选择 | K 条候选选最优 | 加权 Dijkstra 单路径 |
| vs ECMP | K-path ≥ ECMP 表达力 | 单路径 < ECMP 多路径表达力 |

MVE 验证的是 "GNN + K-path selection > ECMP"，但 Contract 写的是 "GNN + per-edge weight > ECMP"。后者从未被验证。

## 框架漏洞分析

### 漏洞 1: MVE 结果记录不完整

**位置**: `gw-feasibility.md` §D (MVE)

**问题**: MVE 只记录 ratio（GNN/ECMP=0.88），不记录动作空间架构。后续阶段无法追溯 MVE 实际验证了什么。

**修复**: MVE 结果必须包含架构摘要（动作空间类型、路由范式、奖励设计），不仅是一个 ratio。

### 漏洞 2: MVE → Simulator 设计无对齐门控

**位置**: `gw-experiment.md` Step 6 → Step 7 交接

**问题**: 仿真器设计（simulator-design.md）和 MVE 可以使用完全不同的架构，框架不检查一致性。

**修复**: 新增 FR-11 门控规则。

### 漏洞 3: 动作空间表达力无审计

**位置**: `contract.md` Step 4 (端到端推演)

**问题**: data-flow.md 检查特征完整性和维度匹配，但不检查动作空间表达力是否至少等于最强 baseline。

**修复**: 新增 FR-12 审计规则。

### 漏洞 4: 路由范式语义盲区

**位置**: `code-quality.md` 方法论适配性矩阵

**问题**: 矩阵覆盖图结构×动作空间×学习范式，但不覆盖路由范式差异（单路径 vs 多路径、顺序 vs 同时）。

**修复**: 新增 FR-13 检查规则。

## 建议新增框架规则

### FR-11: MVE-Contract 架构对齐 (gw-feasibility.md)

当 MVE 通过后进入仿真器设计阶段时：
1. 必须提取 MVE 的动作空间架构摘要
2. 与计划的仿真器设计比对
3. 不一致时必须显式论证：(a) 变更原因 (b) 为什么不会降低表达力 (c) 是否需要新的 MVE 验证

### FR-12: 动作空间表达力审计 (contract.md Step 4)

端到端推演增加一节 "动作空间表达力检查"：
- 逐 baseline 对比：模型的动作空间是否至少和该 baseline 一样表达力强？
- 如果不如某个 baseline，必须标注为已知限制并论证为什么仍可行
- 特殊关注：多路径分流能力（ECMP）、离散选择 vs 连续控制、局部 vs 全局决策

### FR-13: 路由范式语义检查 (code-quality.md)

方法论适配性矩阵增加路由范式维度：

| 模型路由范式 | Baseline 路由范式 | 风险 |
|-------------|------------------|------|
| 单路径 | 多路径分流 (ECMP) | **高** — 表达力不足 |
| 同时路由 | 顺序路由 | 中 — credit assignment 更难 |
| 加权最短路 | K-path 选择 | 中 — 取决于候选路径质量 |

## 预防同类问题的通用原则

**MVE 验证 ≠ 架构验证**: MVE 验证方向可行性，不验证具体架构。当从 MVE 跳到设计时，架构变更必须重新论证。

**表达力下界检查**: 模型动作空间的表达力不能低于最强 baseline。如果低于，必须引入额外机制（如 K-path splitting）来补偿。

## 相关文件

- 决策记录: D4 (MVE-2), D10 (仿真器设计), D14 (Quick Test), D15 (根因分析)
- 框架文件: `stages/gw-feasibility.md`, `stages/contract.md`, `code-quality.md`
- 问题代码对比: `mve_env.py` vs `simulator/env.py`, `mve_train.py` vs `simulator/model.py`
