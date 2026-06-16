# Handoff: A3 §4a 维度 A0/A'/A/B 全过，进维度 D（MVE）

> 来源: S009（对话甲续 6）| 交接目标: 下一个对话启动 A3 MVE 设计 + 执行
> 日期: 2026-06-16 续 6
> 文件名: H006-a3-mve-handoff.md

## 到哪了（状态）

A3（导频前馈 CPE 替代 VV/AGC 相位估计角色，幅度归 AGC）已过 **§4a 维度 A0/A'/A/B 全部四个分析维度**，只剩维度 D（MVE）这一道实验门。S008（H005 汇总）推荐的"A3 继续进 §A"已完成并超额（按 gw-feasibility.md 纠正后的正确顺序 A0→A'→A 做了三维度）。

**进度全景**：
- 维度 B（新颖性-可行性解耦）= PASS（S006/D006）：空白零假设检查 4 原因全反驳
- 维度 A0（DSP 适配版）= PASS（S009）：性能间隙 2.3dB[实证] / 负面证据无针对 A3 失败 / FR-01 先验覆盖不触发
- 维度 A'（竞争维度分解）= PASS（S009）：创新只建在维度 1（相位估计精度）
- 维度 A（结构优势）= 4/5 通过（S009）：A-1/2/3/5 过，A-4（FR-03 增强基线对比）是**已知债务留 MVE 闭环**
- 维度 D（MVE）= **待做**（这就是下一个对话的任务）

**关键新约束（本轮新增 BC-4）**：前馈 CPE 通用失效边界 = phase unwrap cycle slip（low SNR + 深衰落），**对 pilot 前馈 CPE 同样适用**。修正了 BC-2 的措辞——"不迁移"仅指 VV 的 M-次方块边界盲估计失效；cycle slip 是前馈 CPE 族的共享边界，pilot CPE 不豁免。A3 必须含 PAPU 类 cycle slip 应对设计（Li 2019 的 pilot-aided phase unwrap，0.78% pilot 救回 3dB）。

## 下一步干什么

**启动 A3 维度 D（MVE）**。打开新对话后第一件事：

1. **读 `thesis-lessons.md`**（AGENTS.md 强制，MVE 前必读）——至少速查表 + 最近 3 条（TL-20/22/23/25）。TL-25 起飞检查单必须过。
2. **读 `stages/gw-feasibility.md` §4a 维度 D（L122-156）**——MVE 的 9 项 [MUST] + FR-11/14/15 不可降级条件。
3. **设计 MVE 假设**（一句话）：验证 pilot 前馈 CPE（含 PAPU 类 cycle slip 应对）在 deep fade（σ²_I≈0.684，Paillier 条件）下相位估计方差 < AGC+DPLL，且 cycle slip 不触发（BC-4）。
4. **最小实例**：能测该假设的最小规模——建议单载波 QPSK/16-QAM + Gamma-Gamma deep fade 信道（复用 Paillier 参数 σ²_I=0.684）+ pilot tone 注入 + 前馈 CPE（含/不含 PAPU 两种）vs AGC+DPLL 对比。临时脚本，≤1 天，不建正式仿真环境。
5. **子 agent 执行**（AGENTS.md 上下文管理规则），主对话只接结果数字。

## 纪律（和 MVE 直接相关的约束）

1. **BC-4 cycle slip 必验**：MVE 必须验证 deep fade 下 pilot 前馈 CPE 不触发 phase unwrap cycle slip。若触发，A3 须含 PAPU 类应对，重新验。**这是本轮负面证据搜索的新发现，不能跳。**
2. **BC-2 修正版**：MVE 含 VV 在 deep fade 失效 vs pilot CPE 对比，但注意——cycle slip 是共享边界，"不迁移"只指 VV 的 M-次方块边界盲估计。
3. **BC-1 PASC 作 FR-15 目标 baseline**：MVE 必须含 PASC 路线（self-coherent pilot tone）作"贡献声称要超越的对手"。若 PASC 难在 MVE 阶段实现，用最接近可用 baseline 近似并记录差距（gw-feasibility.md L136）。
4. **FR-14 先验对照**：MVE pass 标准必须含 "pilot CPE > AGC+DPLL（最强简单先验）"，非仅 > 无处理。
5. **FR-11 架构摘要必填**：A3 是 DSP 非 RL，架构摘要语义对应——处理粒度（per-block/per-symbol）/ 对比范式（pilot CPE vs AGC+DPLL 闭环）/ 性能指标（相位估计方差、BER）/ 先验对照（AGC+DPLL 得分 + pilot 得分 + 比值）。
6. **A-4 债务闭环**：MVE 的 BC-1/BC-3 增量实证就是 A-4（FR-03 增强基线对比）的闭合点。
7. **增益预期锚 Valjus +1dB 量级**（非 Wang 4 支路 +19dB 分集贡献）——别把分集增益误当 pilot 增益。
8. **不跳 MVE**：A3 是"组合新颖性"（光纤 pilot CPE 迁移 FSO 湍流），gw-feasibility.md L152 明文"组合新颖性不应跳过 MVE"。

## 已知债务（principle vs reality）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| A-4 FR-03 增强基线对比未实证 | 结构优势须对增强 baseline（非裸方法）证 <5% 差距 | 推断未验证（Phase B 子agent 标 abstract 推断）| MVE 执行时 BC-1(PASC)/BC-3(residual carrier) 增量实证 |
| S2 交叉验证未完成 | web 断言须 Semantic Scholar API 交叉验证 | A0-5 子agent 的 S2 curl 全超时（5min），各失效报告靠 Exa/SerpAPI 单源摘要 | 下强结论前下载 Wang 2019/Li 2019 正文核对 |
| Phase B "dB 属模态非 CPE" 归类未验证 | 同上 | PASC 系列 dB 数字归"模态/混频指标"是 abstract 推断 | 下载 Zhou 2023 + McDonald 2025 正文确认 DSP 链路有无 pilot→数字 CPE |
| query 3 deep-fade loss-of-lock 检索缺口 | 负面证据搜索应穷尽 | SerpAPI 配额耗尽中断 | query 1+2+WebSearch 已覆盖同失效机制，影响有限，非阻塞 |

## 验证阈值（MVE 须达）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| pilot CPE vs AGC+DPLL 相位估计方差 | pilot < DPLL（deep fade σ²_I=0.684）| Paillier 2.3dB gap（实证）| 待 MVE |
| pilot CPE vs AGC+DPLL BER | pilot 优于 DPLL ≥0.5dB | Valjus +1dB 量级锚（实证）| 待 MVE |
| cycle slip 不触发（BC-4）| deep fade 下 pilot CPE cycle slip 率 < VV blind | Ip&Kahn 2009 / Li 2019 失效边界 | 待 MVE |
| FR-14 先验对照 | pilot CPE > AGC+DPLL（最强简单先验），非仅 > 无处理 | gw-feasibility FR-14 | 待 MVE |
| FR-15 目标基线对照 | pilot CPE ≥ PASC 路线（或记录差距）| gw-feasibility FR-15 + BC-1 | 待 MVE |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（A3 现在是 A0/A'/A/B 四维度全过 + 4 条 BC）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] A3 四维度全过（查 S009 维度进度表）
  - [ ] BC-4 是 phase unwrap cycle slip（查 D006 BC-4 行 + S009 A0-5）
  - [ ] 性能间隙 2.3dB[实证]（查 Paillier content.md:200）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（MVE 在原始目标"系统性扫描找方向"+ D001 后续阶段链内，但**不碰 Contract/Execute/仿真代码**）
- [ ] 已读 thesis-lessons.md（MVE 前强制，AGENTS.md）

## 下一轮

**A3 维度 D（MVE）启动**——按 gw-feasibility.md §4a 维度 D 的 9 项 [MUST] 设计并执行。子 agent 执行，≤1 天。MVE 通过 → A3 §4a Go → Step 5（baseline 选定）。MVE 失败 → 回 D006 否决条件（§4a 维度 A 发现无增量 / MVE 发现导频 CPE 同失效 / 导师不要 / Contract baseline 增量 <0.5dB）。

**并行可选**（不阻塞 A3 MVE）：N1 §B（S008 推荐的上行期权，#3 强湍流风险优先）。但 N1 §B 不在本 handoff 范围。

## 附：A3 §4a 各维度一句话结论速查（供接收方快速建立全貌）

| 维度 | 结论 |
|---|---|
| A0（DSP 适配版）| PASS。性能间隙 2.3dB[实证]/负面证据无针对 A3 失败（新增 BC-4 cycle slip）/FR-01 不触发 |
| A' | PASS。创新只建维度 1（相位估计精度），频谱效率/复杂度不声称创新 |
| A | 4/5 通过。结构优势=开环无失锁 vs 闭环 critical SNR；范式=光纤 pilot-aided CPE 迁移；A-4 债务留 MVE |
| B | PASS（S006）。空白零假设检查 4 原因全反驳 |
| D | **待做（本 handoff 目标）**|
