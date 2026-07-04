# Handoff: 对话 4——B11/B12 评点 + literature_notes 载波同步 v2 章节并入

> 来源: S005 | 交接目标: 对话 4 评 B11/B12 + literature_notes 综合分析并入，全 12 点总表最终合并
> 日期: 2026-07-04
> 文件名: H004-conversation4-b11b12-eval-literature-notes.md

## 到哪了（状态）

对话 3（S005）完成 B8/B9/B10 三点并发评点 + B1-B10 总表续填（**26 个 Q#**）。**纠正对话 2 B5 主线自读全文违规**——本轮 3 子 agent 并发（B8/B9/B10 各 1），主线不碰全文，委托率 100%。

**B8 评点收获（主判定"无核心 Q#" + 2 相邻/边界 Q#）**：
- B8 全称：RL=Reinforcement Learning / GS=Geometric Shaping / SCD=Self-Canceling coherent Detection。重庆邮电大学 Liu 等 JOCN 2023。
- 核心机制：heterodyne + square-law + LPF 使 CFO/相位噪声"自消除"，PAM4 直接判决，**载波同步需求被绕过**（行 119 linewidth 不敏感）。
- **主判定：本篇无核心 Q#**（B8 与 B1-B7 本质正交，B1-B7 改进载波恢复，B8 消除载波恢复需求）。撞 D006 否；D005 不适用；范围 out（地面 FSO 1km）。
- B8-Q1/Q2 相邻/边界候选：mixing efficiency 前提失效 + 调制格式边界（PAM4 一维 vs QAM 二维失效），均 out + 不够格。
- **FR-26 修正**：子 agent 报"全文无 dB"措辞过强，实为"无 vs baseline dB gain"（参数表有 23 次 dB）。

**B9 评点收获（3 Q#，~3dB 跻身第一梯队）**：
- DRE 全称：**Digital Resolution Enhancer**（数字分辨率增强器）——TX 侧动态量化 + block-wise Viterbi 把量化噪声从带内挤到带外。虚拟载波 = 数字域 DSP 插入的 carrier tone。
- 核心机制：自相干架构**用架构"绕开"传统载波同步链**（无 OPLL/Costas/V-V），载波相位靠 RX-DSP DC-Value 后处理重建。DRE 与载波同步正交。
- **B9-Q1（核心）**：DRE 迁移自相干 FSO 深湍流——**够格（量级达标）**，~3dB @ 3 PNOB（行 241/253）与 B3-Q2 +2~3dB 同量级，但 baseline 是内部 w/o DRE 对照非传统相干载波同步。范围 in 倾向（地面 FSO 42m）→待迁移星地深湍流。
- B9-Q2（自相干绕开载波同步的湍流稳健性）：待定量锚。B9-Q3（DRE 与载波同步正交性反向利用）：D006 边界。

**B10 评点收获（3 Q#, ao.581648 全文缺）**：
- 核心机制：导频驱动 RLS 把 CFO+PN 塞进同一线性回归（h1→CFO/h0→PN），128 pilot 训练后切 decision-directed 反馈环，替代 BPS+4OPM。高 CFO(10GHz)/高线宽(1.45MHz) 鲁棒。
- **B10-Q1（核心）**：边际够格（无统一 X dB gain，优势在范围/鲁棒性 BPS+4OPM 失效区）。范围 out（光纤）/待迁移星地 in 候选。
- B10-Q2（湍流鲁棒性）：D006 边界（RLS 状态方程联合建模则撞）。B10-Q3（ao.581648 KRLS PS-64QAM，D011 种子延伸）：待全文核验（摘要 4dB 无法溯源），同作者团队 Deka/Krishnamurthy。

**B1-B10 总表（26 Q#）已落盘 S005 §步骤 2**：
- 撞 D006 明确撞 0 / **边界 5**（B3-Q3/B6-Q2/B7-Q2/🔵B9-Q3/🔵B10-Q2）
- D005 倾向够格 **9**（含 🔵B9-Q1）/ 边际够格 **3**（含 🔵B10-Q1）/ 待定量 **6** / 不够格/不适用 **6**（含 🔵B8 主判定不适用）
- 范围 **out 7**（含 🔵B8×3+B10×2）/ in 或 in 倾向 **18**
- **D005 够格梯度**：第一梯队 B3-Q2 +2~3dB > **🔵B9-Q1 ~3dB（baseline 内部对照需注明）** > B1-Q1/B2-Q2 +1dB；第二梯队 B7-Q1/B10-Q1 结构性优势
- **🔴 总表守 D018 中性提取——不判 Go/Kill**

## 下一步干什么

**新对话打开后**（对话 4 = B11/B12 评点 + literature_notes 并入）：

### 步骤 1：报到（Trigger 1+5）
读 topic-index（不变量 9 条）+ S001 v2 + S003 + S004 + **S005**（B1-B10 总表 26 Q#）+ 本 H004 + gw-read.md + **templates.md literature_notes 模板（综合分析+研究问题清单）** + 原专题 H020。

### 步骤 2：B11 NDA-ML STO+CPE 评点（派 1 子 agent）

**素材**：
- `papers/doi/10.1109_LPT.2024.3523478/`（B11 锚 PTL，226 行）
- cited-by 1 篇（s25164906 边缘 HSR 覆盖，可选）
- 锚极新 cited-by 仅 1，B11 评点靠锚全文 + M-APSK/NDA ML 经典 Wu[11]/Hu[12]

派 1 子 agent 读 B11 锚 + 写 B11 增量笔记（gw-read 14 字段+7 项含 M-C-A），主线 FR-26 grep 核查。**主线不碰全文（守委托纪律）**。

### 步骤 3：B12 频域 pilot 评点（派 1 子 agent，**用户新下 MAP 全文**）

**素材**：
- `papers/doi/10.1109_TCOMM.2022.3171809/`（B12 锚 TCOMM，590 行）
- **🔴 用户新下 `papers/doi/10.23919_oecc-psc62146.2025.11109607/`（B12 MAP Phase Recovery 256-QAM，150 行，2026-07-04 到位）**——原 IEEE 订阅墙已解决
- cited-by 3 篇：COMST.2024.3443158（Phase Noise Survey 1288 行）/ acp ipoc63121（频域 pilot tone，待核）/ oecc-psc62146（已下）

派 1 子 agent 读 B12 锚 + MAP 全文 + cited-by + 写 B12 增量笔记。

### 步骤 4：literature_notes 载波同步 v2 章节并入（主线 + 可派子 agent 辅助）

**任务**：全 12 篇笔记完成后，按 gw-read 综合分析模板写载波同步 v2 章节：
1. **现有方法分类**：按技术路线分类（OPLL 硬件锁相 / DSP 数字 FOE / 自相干架构 / 高阶 QAM CPE / NDA-ML / 频域 pilot 等），每类 2-3 句含具体方法名
2. **已知局限**：从 12 篇 conclusion/future work 提取共同不足
3. **2-3 年趋势**：从发表年份和方法演进推断
4. **研究背景概述**：载波同步子领域时间线 + 核心技术挑战 + 本研究定位
5. **研究问题清单**（[MUST]）：把 12 篇的 Q# 汇总成跨论文问题清单，逐条过 glossary 四判据

**templates.md literature_notes 模板**（综合分析-研究问题清单表格格式）必读。

### 步骤 5：B1-B12 全 12 点总表最终合并（交用户最终排优先级）

B11/B12 评完后，合并 B1-B10 26 Q# + B11/B12 新 Q# = 最终总表，交用户排优先级后对前几名判 Go/Kill。

**守 3 步上限提醒**：B11/B12 评点 + literature_notes 并入 + 总表最终合并可能超 3 步。建议对话 4 做 B11/B12 评点（2 子 agent 并发）+ literature_notes 并入（主线写综合分析+研究问题清单），总表最终合并 + Go/Kill 判定（用户排优先级后）可交对话 5 或本轮收尾。

## 纪律（和下一步直接相关的约束）

1. **🔴 gw-read 14 字段 + 7 项结构化提取是硬要求**（B7/B8/B9/B10 范例 101-115 行）
2. **🔴 守子 agent 委托**（对话 2 违规教训）：B11/B12 评点各派子 agent，主线不碰全文，委托率 100%
3. **🔴 守 D018 中性提取**：笔记 M-C-A 但不判 Go/Kill（S003+S004+S005 守住 26 个，对话 4 继续）
4. **🔴 D006 红线 + 范围硬门**：M-C-A 提取时标撞/不撞（只标不砍）
5. **守 3 步上限**：对话 4 ≤3 步
6. **子 agent ≤15 分钟**：B11/B12 各 1 子 agent，≤2 并发
7. **主线 grep 核查每条关键声称**（FR-26）
8. **literature_notes 综合分析必含研究问题清单**（gw-read [MUST]，过 glossary 四判据）
9. **总表中性**：合并不判 Go/Kill，交用户最终排优先级
10. **复用旧笔记不重写**：B11/B12 旧笔记查复用

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（9 条）
- [ ] 已验证本文件至少 3 条关键事实声称（建议验证：①S005 §步骤 1 B9-Q1 ~3dB @ 3PNOB 行 241/253 四处一致 ②S005 §步骤 1 B8 主判定"无核心 Q#" ③S005 §步骤 2 总表 26 Q# 计数）
- [ ] 已检查 _registry.yaml depends_on（2026-06-20-problem-driven-redirection）和 conflicts_with（none）
- [ ] 已确认范围未违反"明确不含"（不判 Go/Kill / 不预设 Q# / 不改框架 / 不出星地激光通信大背景）

## 接口变更（如有代码改动）

无代码改动。

## 已知债务（B11/B12 相关）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| **ao.581648 Optica AO 订阅墙**（用户未下）| B10-Q3 高相关 PS-64QAM KRLS 全文 | 仅 content.md 摘要无 PDF（12 行）| B10-Q3 标待全文核验，或用户继续手动下 |
| **~~B12 MAP oecc-psc62146 IEEE 订阅墙~~** | ~~B12 MAP Phase Recovery~~ | ✅ **已解决（用户 2026-07-04 手动下）**：source.pdf(0.6MB)+content.md(150 行) 已落 `papers/doi/10.23919_oecc-psc62146.2025.11109607/`。对话 4 评 B12 受益 | — |
| **B11/B12 图表数值 fast md 占位符** | 笔记量化段需读图 | 未处理（可后置）| 对话 4 涉及前用 `tools/convert --quality standard` 重转 |
| **literature_notes 载波同步 v2 章节未写** | gw-read 综合分析 [MUST] | 12 篇笔记 11 篇就绪（B1-B10+S003 B1-B6）+ B11/B12 对话 4 评 | 对话 4 步骤 4 并入 |

## 下一轮

**对话 4 执行（本轮 handoff 后）**：
1. 报到（读 topic-index/S001 v2/S003/S004/**S005**/本 H004/gw-read.md/templates.md literature_notes 模板/原专题 H020）
2. B11 NDA-ML STO+CPE 评点（1 子 agent，主线不碰全文）
3. B12 频域 pilot 评点（1 子 agent，**用户新下 MAP 全文 150 行**）
4. literature_notes 载波同步 v2 章节并入（综合分析+研究问题清单，主线写可派子 agent 辅助）
5. B1-B12 全 12 点总表最终合并（26+ Q# 交用户最终排优先级）
6. 产出 S006 + H005（如未完成则交对话 5 Go/Kill 判定）
