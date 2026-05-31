# 文献覆盖面缺口报告 — Beam Hopping + GNN

生成时间：2026-05-15

## 文献覆盖面状态

### 成功获取：7 篇（可用于精读）

| # | 优先级 | 标题 | 来源 | 行数 |
|---|--------|------|------|------|
| 1 | must_read | Joint Beam Scheduling and Power Optimization for BH LEO (Zheng ChinaComm 2023) | arxiv/2312.01292 | 347 |
| 2 | must_read | Demand-Aware BH and Power Allocation for Load Balancing in DT Empowered LEO (Gong TWC 2026) | arxiv/2411.08896 | 1399 |
| 3 | to_confirm | Multi-Satellite BH and Power Allocation Using DRL (Xie arXiv 2025) | arxiv/2501.02309 | 957 |
| 4 | should_read | Duality-Guided Graph Learning for Real-Time Joint Connectivity and Routing in LEO | manual/duality-guided... | 772 |
| 5 | 额外 | Learning Wideband User Scheduling and Hybrid Precoding with GNN | arxiv/2503.04233 | 1528 |
| 6 | 额外 | Enhancing Size Generalization in GNN through Disentangled Representation | arxiv/2406.04601 | 1998 |
| 7 | 额外 | GNN-Based Continual Learning for Resource Allocation (Zhou TVT 2025) | manual/zhou-clgnn-tvt-2025 | 655 |

### 内容质量不达标：1 篇
- `papers/manual/service-driven-dynamic-beam-hopping-with-resource-/content.md` (14行，仅验证页面)

### 下载失败（用户待获取）：18 篇

**最关键的失败论文（DRL baseline + GNN 方法）：**

| # | 优先级 | 标题 | DOI | 重要性 |
|---|--------|------|-----|--------|
| 1 | must_read | Meta-Learning for GNN-Based Power Allocation in LEO (Geng TVT 2025) | 10.1109/TVT.2024.3477601 | **GNN+波束间功率分配，最接近创新点** |
| 2 | must_read | Interference-Suppressed Joint Channel/Power Allocation: Dynamic Hypergraph NN (Zhang TWC 2026) | 10.1109/TWC.2025.3586230 | **超图NN+干扰建模，方法借鉴** |
| 3 | must_read | Distributed BH Scheduling for LEO via Hierarchical MADRL (Gong TWC 2026) | 10.1109/TWC.2026.3659941 | **分层MARL做BH，5ms实时，核心baseline** |
| 4 | must_read | Resource Allocation and Load Balancing for BH Scheduling (Zhao TWC 2025) | 10.1109/TWC.2024.3508741 | **DT+A3C+MARL，高引用baseline** |
| 5 | must_read | Multi-Satellite Coordinated BH for Interference Mitigation: Graph-Theoretic (WCL 2026) | 10.1109/LWC.2026.3676112 | **图论方法做BH干扰抑制** |
| 6 | must_read | Resource Allocation in Multibeam LEO Based on BH and Frequency Reuse (IoTJ 2025) | 10.1109/jiot.2025.3594483 | **多波束BH仿真设置参考** |
| 7 | must_read | DNN-Based Energy-Efficient RM for BH-LEO (IoTJ 2026) | 10.1109/JIOT.2025.3617486 | **DNN方法对比** |
| 8 | should_read | Dependency-Elimination MADRL: Scalable On-Board RA for BH (TCOMM 2025) | 10.1109/TCOMM.2025.3529212 | **可扩展MADRL方法** |
| 9 | must_read | Joint BH and RA for Load Balancing and Interference Avoidance in Multi-LEO (ICC 2025) | 10.1109/ICC52391.2025.11161887 | **多星BH干扰避免** |
| 10 | must_read | Multi-Agent DDPG-Based Joint BH and RA for Cognitive GEO-LEO (NetLet 2025) | 10.1109/LNET.2025.3605531 | **多智能体DDPG方法** |

**次重要失败论文：**
| # | 标题 | DOI |
|---|------|-----|
| 11 | DRL-Based Dynamic RA for Multi-Beam Satellite (PIMRC 2023) | 10.1109/PIMRC56721.2023.10293942 |
| 12 | DRL Based Interference Avoidance BH Allocation (TrustCom 2023) | 10.1109/TrustCom60117.2023.00268 |
| 13 | Joint Frequency/Power Allocation via MADRL (VTC 2023) | 10.1109/VTC2023-Spring57618.2023.10200414 |
| 14 | Sustainable BH and RA for Guaranteed QoS (COMSNETS 2026) | 10.1109/COMSNETS67989.2026.11418189 |
| 15 | Attention-Enhanced Multi-Objective DRL (OJ-COMM 2026) | 10.1109/OJCOMS.2026.3671832 |
| 16 | Spectrum Sharing-Enabled Collaborative Dynamic Beam Pattern (LCOMM 2026) | 10.1109/LCOMM.2026.3681606 |
| 17 | Service Priority-Driven Joint BH and Power Allocation (APNOMS 2025) | 10.23919/APNOMS67058.2025.11181233 |
| 18 | A Framework for Joint Beam Scheduling and RA in BH-Based Satellite | 无DOI |

## 覆盖面分析

- 当前精读论文全部来自 arXiv + manual，可能遗漏 IEEE 付费墙内的高相关论文
- **核心 DRL baseline（Zhao TWC 2025, Gong TWC 2026, Lin TWC 2024, Xie 2025）全部在 IEEE 付费墙后**，仅获取到 1 篇 DRL baseline（Xie arXiv 版）
- **GNN 方法借鉴论文（Geng TVT 2025, Zhang TWC 2026）全部在付费墙后**——这是创新点的直接方法论来源
- 成功获取的 2 篇 GNN 方法论论文（2503.04233 GNN调度, 2406.04601 GNN泛化）不是卫星领域，但方法论可迁移

### 阅读池评估

**精读可用：7 篇**
- BH 直接相关：3 篇（2312.01292, 2411.08896, 2501.02309）
- GNN 方法借鉴：2 篇（2503.04233, zhou-clgnn-tvt-2025）
- 图学习 + LEO：1 篇（duality-guided-graph-learning）
- GNN 泛化：1 篇（2406.04601）

**质量门槛：≥5 篇 → 达标（7 篇）**，但覆盖面有系统性偏差：
- DRL baseline 覆盖不足（只有 3 篇 BH 论文，缺核心竞品）
- GNN 方法论缺卫星领域论文（Geng/Zhang 都没获取到）

## 引用质量分析

- 正式发表：4 篇（2312.01292→ChinaComm, 2411.08896→TWC, zhou→TVT, 2501.02309 待确认）
- 预印本：2 篇（2503.04233, 2406.04601）
- 预印本占比：2/6 = 33%
- 2501.02309 预印本已超 1 年，可能已正式发表 → Step 3 精读时需验证

## 用户行动项

- [ ] **最优先**：手动获取 Geng TVT 2025 (10.1109/TVT.2024.3477601) 和 Zhang TWC 2026 (10.1109/TWC.2025.3586230) — 创新点直接方法论来源
- [ ] 手动获取 Gong TWC 2026 (10.1109/TWC.2026.3659941) — 分层 MADRL 核心 baseline
- [ ] 手动获取 Zhao TWC 2025 (10.1109/TWC.2024.3508741) — DT+MARL 高引用 baseline
- [ ] 手动获取 Lin TWC 2024 — QMIX MADRL 多星 BH 调度（DOI 待查）
- [ ] 或确认当前 7 篇覆盖面可接受，精读时以 arXiv 论文为主
- [ ] 放入 `papers/manual/{slug}/` 并创建 metadata.json
