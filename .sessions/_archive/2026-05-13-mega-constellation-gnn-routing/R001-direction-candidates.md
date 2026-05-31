# 候选方向分析

> 基于 2026-05-13 大规模文献检索，覆盖 6 组关键词、180+ 条候选文献、5 个子方向。
> 检索存档：`search-archive/2026-05-13/` 下 6 个 JSON 文件。

## 方向 1：GNN-based routing optimization for LEO mega-constellation networks

- **核心问题**：巨型 LEO 星座（Starlink/Guowang/G60）中 ISL 组网拓扑动态变化，传统路由算法（最短路径、SDN 集中式）难以适应高动态、大规模、多约束场景，如何用图神经网络实现可扩展、抗毁、自适应的星座路由？
- **与导师方向关联度**：**高**。导师给的方向是"LEO 卫星链路"，ISL 路由是星间链路层的核心网络问题。参考方向 ISL ACM 预测也是 ISL 相关。
- **论文密度**：**低-中**，但快速上升。OpenAlex 趋势：2022(2) → 2023(9) → 2024(4) → 2025(10) → 2026(13)。5 年累计仅 ~38 篇。属于蓝海。
- **创新空间**：
  - GNN size generalization：训练在小星座上，部署到 Starlink 级 ~4000+ 节点
  - 联合路由+拓扑优化：现有工作分开处理，联合优化空间大
  - 弹性路由：链路故障/攻击场景下的快速重路由
  - 多目标路由：时延+吞吐+负载均衡+能耗联合优化
- **最小可发表单元**：GNN-based routing algorithm for LEO mega-constellation that achieves size generalization (train on small constellation, generalize to 1000+ nodes) with lower end-to-end delay and better load balancing than OSPF/SDN baselines.
- **代表文献**：
  - [必读] (2024) GNN-Based Routing for Link Reliability Optimization in SD-LEO Satellite Networks, NFV-SDN 2024, doi:10.1109/NFV-SDN61811.2024.10807492
  - [必读] (2026) Geographic-Based Auxiliary Routing Scheme in SDN-Based Mega Constellation Networks, IEEE IoTJ, doi:10.1109/JIOT.2025.3638842
  - [必读] (2025) Multi-Attribute Consistency Segment Resilient Routing for LEO Satellite Mega Constellation, IEEE TMC, doi:10.1109/TMC.2025.3570670
  - [必读] (2024) Clustered Multi-Criteria Routing Algorithm for Mega LEO Satellite Constellations, IEEE TVT, doi:10.1109/tvt.2024.3396350 (22 cites)
  - [必读] (2025) A Scalable Multicontroller SDN Framework for LEO Mega-Constellation via Topology Virtualization, IEEE IoTJ, doi:10.1109/JIOT.2025.3576912

## 方向 2：AI-driven beam hopping + resource allocation for multi-beam LEO satellite

- **核心问题**：多波束 LEO 卫星如何在波束间动态分配功率、带宽和时间资源（beam hopping），以适应地面用户非均匀分布和时变业务需求？DRL/GNN 能否优于传统启发式方法？
- **与导师方向关联度**：**高**。直接是 LEO 卫星链路层的资源管理问题，波束管理是 LEO 系统设计的关键技术。
- **论文密度**：**中**，稳步增长。beam hopping + DRL 是 2023-2025 的热点。历史检索中已有 beamforming-optimization 和 multi-beam-satellite 相关结果。
- **创新空间**：
  - DRL-based 动态 beam hopping pattern 生成（现有多为启发式）
  - 联合 beam hopping + ACM + 功率分配
  - 考虑用户 QoS 差异的多目标优化
  - GNN for 可扩展的多波束资源分配（规模泛化）
- **最小可发表单元**：DRL/GNN-based joint beam hopping and power allocation for multi-beam LEO satellite with improved traffic-matched throughput and user fairness over baseline schemes.
- **代表文献**：
  - [必读] (2025) AI-Driven Optimization Frameworks for Next-Generation Satellite Communication Systems, score=1.0
  - [必读] (2026) DNN-Based Energy-Efficient Resource Management for Beam-Hopping LEO Satellite Communications, published
  - [必读] (2026) Reliable AI for Decision-Making and Resource Allocation in Integrated Terrestrial/Non-Terrestrial Networks, published
  - [建议读] (2025) Joint Beam Hopping with Adaptive Coding and Modulation for LEO Satellite Communications, score=0.8
  - [建议读] (2024) Leveraging deep-learning for adaptive coding and modulation for LEO satellite-terrestrial links, 8 cites

## 方向 3：NTN-terrestrial integrated network resource management for 6G

- **核心问题**：6G 非地面网络（NTN）中，如何联合优化卫星-地面-空中多层级网络的频谱、功率、计算资源分配，以实现无缝覆盖和差异化 QoS？
- **与导师方向关联度**：**中**。NTN 是卫星通信的扩展叙事，6G 标准化方向，但范围比导师给的"LEO 链路"更广。
- **论文密度**：**高**，且快速增长。OpenAlex 趋势：2022(43) → 2023(121) → 2024(167) → 2025(199)。竞争激烈。
- **创新空间**：
  - Transformer-based 动态资源分配（刚出现，2026 年首篇）
  - 联邦学习在卫星边缘计算中的应用
  - RIS 辅助的星地协同传输
  - 但领域太宽泛，需要收窄到具体子问题
- **最小可发表单元**：需要收窄。例如 "Transformer/FL-based joint spectrum and power allocation for satellite-terrestrial integrated network in specific scenario (e.g., maritime/emergency/UAV)".
- **代表文献**：
  - [必读] (2025) Cooperative Ground-Satellite Scheduling and Power Allocation for Urban Air Mobility Networks, IEEE JSAC, doi:10.1109/JSAC.2024.3460031 (10 cites)
  - [必读] (2025) Multi-Dimensional Modeling and Connectivity Analysis for THz Space-Air-Ground Integrated Networks, IEEE TWC, doi:10.1109/TWC.2025.3542758
  - [必读] (2024) RIS for 6G NTN: Assisting Connectivity and Coverage, IEEE IoT Magazine, doi:10.1109/iotm.001.2300208 (34 cites)
  - [建议读] (2026) Intelligent Resource Allocation for Satellite-RIS-Assisted URLLC-ISAC, IEEE TCCN, doi:10.1109/TCCN.2026.3667139
  - [建议读] (2026) Transformer Actor-Critic for Efficient Freshness-Aware Resource Allocation, arXiv preprint

---

## 排除方向及理由

| 方向 | 排除理由 |
|------|---------|
| Grant-free RA for satellite IoT | **红海**。5 年累计 1700+ 篇，2023 达峰后趋稳/下降。创新空间收窄，核心范式（NOMA-OTFS）已成熟 |
| LEO handover + DRL | **过度饱和**。历史检索中已有 50+ 篇，是之前 leo-ntn-handover-drl 项目的方向，不应重复 |
| ACM prediction for ISL | 历史项目 isl-acm-prediction 已证明该方向为学术负面结果（ISL 信道太确定性，DL 无优势） |
| RIS phase shift + DRL | 当前活跃项目 ris-phase-drl，不重复 |

## 综合推荐排序

### 1. 方向 1：GNN-based routing for LEO mega-constellation（强烈推荐）

**推荐理由**：
- **蓝海+快速上升**：5 年仅 ~38 篇相关论文，但 2025-2026 年增速显著（10→13），说明领域正在爆发前夜
- **与导师方向高度吻合**：ISL + LEO + 链路层问题
- **GNN 是天然工具**：星座网络是图结构，GNN 的 size generalization 问题恰好是该方向的核心挑战
- **最小可发表单元清晰**：不需要复杂仿真器，可以用星座拓扑模拟 + GNN 训练验证
- **导师参考方向 ISL ACM 的延伸**：从 ISL 链路层（ACM）到 ISL 网络层（routing），叙事连贯
- **风险**：论文池小意味着审稿人可能来自传统卫星网络领域，需要充分对比传统方法

### 2. 方向 2：AI-driven beam hopping for multi-beam LEO（推荐）

**推荐理由**：
- **直接在导师方向线内**：LEO 卫星链路层的核心资源管理问题
- **DRL 应用场景明确**：beam hopping pattern 生成是序列决策问题，DRL 天然适配
- **工程导向强**：业界（Starlink beam hopping）有实际需求
- **风险**：beam hopping + DRL 已有一定文献积累，创新需要更具体的切入点

### 3. 方向 3：NTN-terrestrial integration（备选）

**推荐理由**：
- **6G 热点叙事**，容易讲故事
- **Transformer/FL 在卫星领域的应用刚起步**，有先发优势
- **风险**：领域太宽，竞争激烈（近 200 篇/年），需要收窄到非常具体的子问题才有可能做出差异化贡献。且与导师方向关联度中等。

---

## 检索质量报告

| 指标 | 数值 | 门槛 | 状态 |
|------|------|------|------|
| 去重后候选 | 180+ | ≥20 | ✅ |
| 必读 | 29 | ≥5 | ✅ |
| 搜索源覆盖 | S2+OpenAlex+arXiv+SerpAPI+Exa | ≥3 源 | ✅ |
| 正式发表占比 | ~71% | ≥50% | ✅ |
| 子方向覆盖 | 5 个角度 | ≥2 | ✅ |
| 覆盖度 | 含链路层/网络层/接入层/融合/AI | 无明显空洞 | ✅ |

检索存档文件（6 组，`search-archive/2026-05-13/`）：
1. `leo-satellite-adaptive-coding-modulation-acm-channel-estimat.json`（Angle A）
2. `satellite-inter-satellite-link-isl-routing-mega-constellatio.json`（Angle B）
3. `leo-satellite-random-access-non-terrestrial-network-massive-.json`（Angle C）
4. `ntn-terrestrial-integrated-network-satellite-ground-cooperat.json`（Angle D）
5. `transformer-attention-satellite-communication-resource-alloc.json`（Angle E）
6. `leo-satellite-beam-management-resource-allocation-ai-machine.json`（补充）
