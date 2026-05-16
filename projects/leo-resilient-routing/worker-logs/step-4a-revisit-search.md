# Worker Log: Step 4a Revisit — 定向检索 MARL 抗毁路由

> 执行时间: 2026-05-16 | Worker: 无状态检索

## 检索执行

3 组关键词，均从项目根目录调用 `tools/search`：

| # | 关键词 | 原始/去重 | 保留 |
|---|--------|-----------|------|
| 1 | `multi-agent reinforcement learning satellite routing` | 75/52 | 30 |
| 2 | `curriculum learning satellite network fault` | 64/62 | 30 |
| 3 | `MARL LEO constellation routing` | 64/59 | 30 |

## 相关论文筛选（MARL + LEO/卫星 + 路由 直接相关）

### 高相关（MARL + 卫星路由，2024-2026）

| 标题 | 年份 | 被引 | 方法概述 | 来源搜索 |
|------|------|------|----------|----------|
| Research on Multi-agent DRL-Based Routing in LEO | 2026 | 1 | 多智能体DRL路由优化 | #1, #3 |
| Traffic-aware Multi-Agent RL-based Routing for LEO | 2026 | 0 | 流量感知MARL路由 | #1, #3 |
| Queue-Aware and Resilient Routing in LEO Satellite Networks | 2026 | 0 | 队列感知抗毁路由 | #1 |
| An adaptive multi-agent DRL routing strategy for LEO | 2025 | 0 | 自适应MARL路由 | #1, #3 |
| Asynchronous Risk-Aware Multi-Agent Packet Routing for LEO | 2025 | 2 | 异步风险感知MARL | #3 |
| Multi-Agent DRL-Based Offloading and Routing in LEO | 2025 | 0 | MARL卸载+路由联合 | #1 |
| Multi-Service Distributed Routing Based on MARL for LEO | 2025 | 0 | 多业务MARL路由 | #1 |
| Routing Strategy in LEO: A Multi-Agent Approach | 2024 | 1 | 多智能体路由策略 | #3 |
| Multi-agent DRL for distributed routing in satellite networks | 2024 | 11 | 分布式MARL路由 | #1 |
| An open source multi-agent DRL framework for satellite routing | 2024 | 7 | 开源MARL路由框架 | #1 |

### 中等相关（CL/抗毁 + 卫星，非纯MARL路由）

| 标题 | 年份 | 被引 | 方法概述 | 来源搜索 |
|------|------|------|----------|----------|
| Continual DRL for decentralized routing in satellite networks | 2025 | 22 | 持续学习DRL路由 | #1 |
| Recovery Routing Based on Q-Learning for Satellite Networks | 2020 | 6 | Q-Learning恢复路由 | #2 |
| Enhancing Fault Resilience in RL-Based Satellite Autonomy | 2025 | 1 | RL增强抗毁性 | #2 |
| Resilient Virtual Constellation-based Load-balancing Routing | 2025 | 0 | 抗毁负载均衡路由 | #3 |
| Curriculum RL-based computation offloading in space-air-ground | 2021 | 18 | 课程RL+计算卸载 | #2 |
| Automating Curriculum Learning for RL | 2025 | 0 | 自动化课程学习框架 | #2 |

### CL + 卫星领域（故障诊断，非路由）

| 标题 | 年份 | 被引 | 方法概述 |
|------|------|------|----------|
| Curriculum Learning Framework for Fault Diagnosis in Electric Systems | 2025 | 0 | CL+故障诊断 |

## 竞争格局判断

### MARL + LEO 路由：**已有竞品，2024-2026 密集涌现**
- 至少 10 篇直接相关论文，多数发表于 2025-2026
- 被引普遍偏低（0-11），说明领域新但竞争正在加剧
- 覆盖了：流量感知、队列感知、风险感知、多业务、分布式等角度

### MARL + 课程学习 + LEO 路由：**基本空白**
- "curriculum learning + satellite routing" 无直接命中
- 课程学习在卫星领域仅出现在**故障诊断**（L010, L020 from search #2）和**计算卸载**（L023 from search #2）
- 未见将课程学习引入 LEO 路由训练的论文

### MARL + 抗毁路由（resilient routing）：**弱竞品**
- "Queue-Aware and Resilient Routing in LEO"（2026）标题含 resilient，但待确认是否真正做抗毁
- "Enhancing Fault Resilience in RL-Based Satellite Autonomy"（2025）涉及抗毁但非路由
- 无论文同时覆盖 MARL + 抗毁 + 课程学习

## 总结（≤200 字）

**MARL 用于 LEO 路由已是热门方向**（2024-2026 至少 10 篇直接竞品），纯 MARL 路由不再有新颖性。但 **MARL + 课程学习 + 抗毁路由** 的组合尚无人涉足。课程学习在卫星领域仅见于故障诊断和计算卸载。本方向的差异化空间在于：(1) 课程学习引入 MARL 路由训练——解决故障场景下稀疏奖励和分布偏移问题；(2) 抗毁（resilient）维度而非单纯吞吐/延迟优化。**建议聚焦"课程学习 + 抗毁"双差异化点**，避免与已有 MARL 路由论文正面竞争。

## 质量门检查

- [x] 至少执行 3 组关键词搜索
- [x] 筛选结果标注了与本研究方向的关联度
- [x] 给出了空白/已有竞品的明确判断
