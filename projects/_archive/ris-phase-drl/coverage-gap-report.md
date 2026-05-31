# 文献覆盖面缺口报告

生成日期：2026-05-13

## 文献覆盖面状态

### 成功获取：8 篇

| # | 标题 | 来源 | 行数 |
|---|------|------|------|
| L01 | Deep RL-Based Energy Efficiency Optimization for RIS-Aided Integrated Satellite-Terrestrial | TCOMM (firecrawl) | 2134 |
| L02 | Spectral Efficiency Optimization for RIS-Aided Multiuser MISO System Using DRL | IEEE Access (arxiv_latex) | 142 |
| L03 | Rate-Splitting for IRS-Aided Multiuser VR Streaming | IEEE JSAC (arxiv_latex) | 604 |
| L04 | A Deep RL for Energy Efficient Resource Allocation IRS | Physical Communication (firecrawl) | 102 |
| L05 | Deep RL Optimized Intelligent Resource Allocation in Active RIS-Integrated TN-NTN | arXiv 2501.06482 | 548 |
| L06 | A Heuristic-Integrated DRL Approach for Phase Optimization in Large-Scale RISs | arXiv 2505.04401 | 556 |
| L07 | Deep RL for Trajectory and Phase Shift Optimization RIS-assisted UAV | arXiv 2411.01338 | 508 |
| L08 | Resource Allocation for Reconfigurable Intelligent Surface Aided... | arXiv 2202.06668 | 631 |

### 下载失败（用户待获取）：7 篇

| # | 标题 | DOI | 重要性 |
|---|------|-----|--------|
| F1 | Deep RL-Based Energy Efficiency Optimization of RIS-UAV-Assisted Communication | 10.1109/VTC2025-Fall65116.2025.11310192 | 高（RIS-UAV+DRL能效） |
| F2 | Secure and energy-efficient transmission in UAV-assisted IRS networks | 10.1038/s41598-025-17852-y | 中（安全方向参考） |
| F3 | Self-Attention-Based DRL for Joint Beamforming and Phase Shift Design | 10.1109/ICC52391.2025.11160846 | 高（注意力机制+相移） |
| F4 | Robust Beamforming and Phase Shift Control in RIS-UAV Relay | 10.1109/iWRFAT65352.2025.11102822 | 中（鲁棒性方向） |
| F5 | Fairness-Aware Computation Offloading with Phase-Shift Design in RIS | 10.1109/JIOT.2024.3371395 | 中（公平性+计算卸载） |
| F6 | Optimization Design in RIS-Assisted Integrated Satellite-UAV-Served 6G IoT | 10.1109/IOTM.001.2300111 | 中（系统级集成） |
| F7 | Energy Efficiency Optimization in RIS-assisted ISATRNs with RSMA | 10.1109/WCNC57260.2024.10570820 | 中（RSMA方向） |

## 覆盖面分析

### 技术路线覆盖
- ✅ DRL 相移优化（核心方向）：L01, L02, L04, L05, L06
- ✅ 联合轨迹+相移优化（UAV 场景）：L07
- ✅ 资源分配+相移联合优化：L08
- ✅ IRS + beamforming：L03
- ⚠️ Self-Attention/Transformer + DRL + 相移：仅有 F3（待获取）
- ⚠️ 安全通信+相移：仅有 F2（待获取）

### 来源偏差
- 当前精读论文来源：IEEE (3篇), arXiv (3篇), Elsevier (1篇), IEEE Access (1篇)
- 下载失败全部来自 IEEE/Nature 付费墙
- 可能遗漏的高相关 IEEE 论文：F3（Self-Attention DRL 相移设计）最值得关注

## 引用质量分析

- 正式发表：5 篇（L01, L02, L03, L04, L05 — 其中 L05 有 arXiv 版本但已发表于 WCNC）
- 预印本：3 篇（L06, L07, L08）
- 预印本占比：3/8 = 37.5%
- 预印本中可能已发表的：L06 (2025), L07 (2024) — 需确认

## 用户行动项

### 引用质量
- [ ] 检查 L06 (arXiv 2505.04401) 和 L07 (arXiv 2411.01338) 是否已有正式发表版本
- [ ] 当前预印本占比 37.5% < 50%，可接受

### 手动获取
- [ ] **优先获取 F3**: Self-Attention-Based DRL for Joint Beamforming and Phase Shift Design (DOI: 10.1109/ICC52391.2025.11160846) — 注意力机制+相移，与 DRL 方法创新直接相关
- [ ] F1: RIS-UAV 能效优化 — 补充 UAV 场景覆盖
- [ ] 其余 5 篇可视覆盖面需要决定是否获取
- [ ] 获取后放入 `papers/manual/{slug}/` 并创建 metadata.json，或确认当前覆盖面可接受
