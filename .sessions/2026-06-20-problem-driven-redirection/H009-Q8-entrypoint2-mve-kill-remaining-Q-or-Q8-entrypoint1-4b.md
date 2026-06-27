# Handoff: Q8 切入点深化 + 切入点 2 MVE FAIL Kill，Q8 剩余 1/4B 或转 Q1

> 来源: S017 | 交接目标: 下一个对话选 Q8 剩余切入点（1/4B）深化 or 转 Q1 对比
> 日期: 2026-06-27
> 文件名: H009-Q8-entrypoint2-mve-kill-remaining-Q-or-Q8-entrypoint1-4b.md

## 到哪了（状态）

**块 E Step 4a 进行中**：Q12 Kill（D006）+ Q8 通过 Step 4a + **Q8 切入点 2 深化后 MVE FAIL Kill**。

- Q8 切入点深化完成：4 候选检索（search-archive/2026-06-27/ +10 JSON）+ 2 子 agent digest + 主线核查关键 DOI 全 PASS
- 4 切入点状态：1（指向×Doppler 空白可做踩 S007 边界）/ 2（真实 SD-FEC **MVE FAIL Kill**）/ 3（DWDM 增量弱）/ 4A（撞死 D006）/ 4B（湍流时变×Doppler 调度空白可做不撞界）
- 用户选切入点 2 → Step 4b MVE → FAIL → Kill

### 🔴 本轮两个关键发现（对下一步最重要）

1. **事实修正（FR-26）**：精读笔记 L08 "FEC 假设理想"**不准**。核对 Fernandes L189 原文：用 **NGMI=0.88** 经验阈值（已含 coding gap，0.88 > R_FEC=5/6=0.833）。切入点 2 剩余增量 = 码型特异散布（0.1-0.3dB）非"理想 vs 真实"全 gap。**教训**：精读笔记判读要核对原文，S012 教训第 N 次复现。
2. **MVE Kill 物理依据**：NGMI 阈值散布来源是 SD-FEC 码型内部特性（Post-FEC BER §480），**跟信道时变无关**。LEO 放大因子 K≈1，"赌 LEO 放大"物理前提不成立。**教训**："赌 X 放大"前先验证放大机制跟变量相关性。

### Q8 状态：切入点 2 Kill，但 Q8 整体未死

Q8 还有 2 个可行切入点：
- **切入点 1（指向×Doppler）**：Fernandes L281 留的口子，至今无人补。但要踩 S007 边界——限定"指向误差对 DSP/符号率调度的影响"（信号处理侧）不撞，纯 pointing 建模/ATP 补偿撞。
- **切入点 4B（湍流时变×Doppler 对符号率调度）**：不撞 D006（改调度不改同步算法）。Fernandes 把湍流当独立 SNR 叠加，4B 改进这个简化。

切入点定后 → Step 4b MVE → 若 Go 进 Contract。

## 下一步干什么

**三条路（用户选）**：

### 路径 A：深化 Q8 切入点 4B（推荐，最干净不撞界）
1. 查切入点 4B 有无已做论文（检索已部分做，但需定向补"湍流时变对符号率调度/Rs 选择的影响"）
2. 定义 4B 的 M-C-A + 四判据 + FR-21 上界（"湍流独立叠加简化"带来多大低估？）
3. Step 4b MVE

### 路径 B：深化 Q8 切入点 1（踩边界但口子最明确）
1. 限定信号处理侧（指向误差对 DSP 的影响，不碰 ATP 控制层）
2. 查"指向误差对 PCS/符号率适配反馈影响"有无已做
3. Step 4b MVE

### 路径 C：转评估 Q1（TS-KF 两阶段解耦 Doppler，四判据全过无旧 Kill 史）
- Q1 是 LEO-LEO 星间（真空无湍流），跟星地场景有差异但方法可迁移
- 评估流程同 Q8（先 B1 换皮核查 + 6 维度）

**建议**：Q8 已花 2 轮深化（S016-S017），切入点 2 Kill 后 Q8 整体增量空间收窄。若 4B/1 再 Kill，Q8 整体该立 D### Kill。**优先 4B（不撞界最干净）**，同时可并行评估 Q1 作 backup。若 Q8 和 Q1 都不 Go，回块 A 扩检索。

## 纪律（和下一步直接相关的约束）

1. **D005 务实路线 INVARIANT**：Go=赢传统 baseline 几 dB。FR-21 oracle 上界降为参考但不豁免（<0.5dB 仍倾向 Kill）
2. **B1 换皮核查前置**（S016 教训）：每个 Q#/切入点评估前先查 thesis-direction-pivot 有无同构方向被 Kill
3. **FR-26 证据链 + 精读笔记核对原文**：S017 又一次复现精读笔记判读偏差（L08 FEC 假设），任何基于精读笔记的判断要核对 content.md 原文
4. **四判据不可放水**（topic-index 不变量 3）
5. **"赌 X 放大"前验证放大机制**（S017 新教训）：切入点 4B 若声称"湍流时变放大某效应"，先验证放大机制跟变量相关
6. **S007 处理技术边界**：ATP/指向不算通信处理（切入点 1 必踩此边界）

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（8 条，D005 务实路线最高优先级）
- [ ] 已验证至少 3 条关键事实声称：
  - [ ] Q8 切入点 2 Kill 在 feasibility_report.md（核查 `grep "切入点 2 Kill" projects/thesis-fso/feasibility_report.md`）
  - [ ] Fernandes L189 NGMI=0.88 事实修正（核查 `grep "0.88" papers/blit-downloads/2026-06-26/10138358.md`）
  - [ ] master-state Step 4a 🔄 含切入点 2 Kill（核查 `grep "切入点 2 Kill\|MVE FAIL" projects/thesis-fso/master-state.md`）
  - [ ] 4 切入点检索存档存在（核查 `ls search-archive/2026-06-27/ | grep -E "pointing|fec|dwdm|turb"`）
- [ ] 已检查 _registry.yaml depends_on/conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| MVE Kill 依据"散布跟信道无关 K≈1"未经文献验证 | FR-26 证据链 | 物理推理（通信理论常识）| 若有人质疑或要更硬证据，补检索"时变信道 NGMI 散布"文献 |
| 切入点 2 Kill 未立正式 D### | decisions.md 规范 | 记 feasibility_report（切入点级非方向级）| 若 Q8 整体也 Kill（1/4B 都不行），立 D### 记 Q8 整体 |
| Fernandes 式 10 公式图被 blit 省略 | MVE 精确复现障碍 | 方案 2 反推绕过 | 若切入点 4B/1 需精确复现，用 arXiv LaTeX 版或重转 PDF 获取公式 |
| 3 篇下不到（Rustum2026/Tang2024/Mosnier2025）| Step 3.5 补充 | SPIE/IET 非 OA | 块 E 按需 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 切入点 MVE | 增量 >0.5dB（FR-21）/ >2dB（D005 务实） | FR-21 + D005 | 切入点 2 FAIL（0.1-0.3dB）|
| Q# Go | 至少 1 个 Q# 过 Step 4a + Step 4b | FR-22 门控 | Q12 Kill / Q8 切入点 2 Kill，暂 0 Go |

## 下一轮

1. 读 H009 + feasibility_report.md（切入点 2 Kill + 4 候选状态）
2. **用户选路径**：A（深化 Q8 切入点 4B）/ B（深化 Q8 切入点 1）/ C（转评估 Q1）
3. 选定后：B1 换皮核查 → 四判据 → FR-21 上界 → Step 4b MVE
4. 若 Q8（4B/1）和 Q1 都不 Go → 回块 A 扩检索（glossary.md "候选全被筛掉时"）
5. **Step 4a/4b 前必读**：gw-feasibility.md（本轮已读）/ TL-30/31 / decisions.md D004-c（FR-26）/ D005（务实 INVARIANT）/ D006（Q12 Kill）/ S017 教训（精读核对原文 + 赌放大前验证机制）
