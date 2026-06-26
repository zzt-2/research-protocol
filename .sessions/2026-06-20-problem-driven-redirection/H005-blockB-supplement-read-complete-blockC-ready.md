# Handoff: 块 B 补精读完成（本轮新增 6 篇）+ 候选池充实 → 块 C 综合分析就绪

> 来源: 本轮执行（2026-06-26，续接 H004）| 交接目标: 进块 C 综合分析（7+篇 M-C-A 汇总过四判据产 Q# 清单）
> 文件名: H005-blockB-supplement-read-complete-blockC-ready.md

## 到哪了（状态）

**本轮在 H004 选样返工基础上，完成了"补检索 + 补精读"，把有效 Q# 候选池从 3-4 篇扩到 7-10 篇，达 gw-read.md ≥5 篇门槛，可进块 C**。

具体做了 5 件事，全在 D005 务实路线 + H004 下一轮范围内：

1. **方案 A 定向补检索**：8 个 tools/search 词（H004 给的 5 + 我补 3 个更宽的），32 条去重召回，存档 `search-archive/2026-06-26/planA-*.json`。偏航检查 A 过（覆盖均衡/同步/Doppler/估计/载波恢复多 DSP 环节，不锁单一模块）。

2. **下载障碍 → blit 绕过**：`tools/download`（urllib 不走代理）对 MDPI/IEEE/SPIE/Optica 全 fail。改用 `tools/blit --source ieee`（Playwright 走系统代理 7897）成功下 3 篇 IEEE 全文 PDF + 转 markdown。**诊断根因：tools/download 的 urllib 没继承系统代理（S005 修过 blit 的 _detect_proxy，download 没修）**。

3. **发现 papers/doi/ 库存金矿**：11 篇光通信 DSP 类未精读全文（之前各专题下的）。

4. **精读 6 篇强候选**（子 agent 精读 + 主线 grep 核查全 PASS，无 S011 型造假），笔记落 `papers/_read_notes/` + read-log.md 追加：
   - **非 PS 3 篇**：11350922（Doppler跟踪 BUPT）/ 10155111（LEO-LEO 调制SP, c=33）/ 10.1109_ACCESS.2025.3535789（自相干 FSO）
   - **PS 3 篇**（用户放行"可以精读"+"总得弄出点东西"）：10.1109_JLT.2023.3281082（=landscape #580, PCS+符号率治Doppler）/ 10.1109_LPT.2025.3647750（PS+RCM 治湍流）/ 10.3390_app11219805（PS-QAM Gamma-Gamma 理论）

5. **voice.md 补登**：H004 更新段引用的 2 条选样返工触发原话（"我希望做的是和同门类似的那种东西。以及，最好多挑点？"+ "感觉你挑的不好呢?"）本轮已补登。

## 候选池当前状态（合并 H004 + 本轮 = 10 篇）

| # | 论文 | 子地带 | 方法形态 | 四判据 | baseline对称 | 改进增益(诚实nuance) |
|---|---|---|---|---|---|---|
| 1 | 两阶段KF(Opt Express 2025) | 均衡/多普勒 | DSP递归估计器 | A✅B✅C✅D✅ | ✅ | 10GHz@18dB OSNR BER<FEC（VV-BPS失效）；0.1GHz小频偏略输 |
| 2 | CPR北理工(Electronics 2025) | 载波同步 | DSP二阶DPLL反馈+前馈 | A✅B✅C✅D✅ | ✅ | BER 6.7e-3 vs 0.25；⚠️利益相关⚠️收敛慢仅QPSK |
| 3 | Time-Packing MMSE(GC 2020) | 均衡/调制/检测 | DSP adaptive MMSE | A✅B✅C✅D✅ | ✅ | 8-PAM 唯一无 error floor；2-PAM 比 Viterbi ~1dB gap |
| 6 | Data-Aided DSP(WiSEE 2024) | 信道估计/DSP | DSP离线均衡 | A✅B✅C⚠️D⚠️ | ⚠️ | SNR≥0dB可靠；⚠️无直接BER对标⚠️实测非星地 |
| **新1** | **11350922 Doppler跟踪(BUPT 2025)** | **Doppler跟踪/载波恢复** | **DSP算法(实时FPGA)+系统设计** | A✅B✅**C❌D❌** | ⚠️ | DFS±8GHz; BER −53dBm@1E-3; ⚠️**无BER-vs-baseline**⚠️仅BPSK OBTB |
| **新2** | **10155111 LEO-LEO调制SP(IEEE Access 2023,c=33)** | **调制+信号处理/DS补偿** | **DSP算法(滤波两阶段CFE)+可行性分析** | **A✅B✅C✅D✅** | **✅** | 10GHz 16-QAM损耗**1.2→0.9dB**;范围8→≥13GHz；⚠️**仅真空星间非星地**⚠️仅仿真 |
| **新3** | **10.1109_ACCESS.2025.3535789 自相干(McMaster 2025)** | **自相干检测/偏振解复用** | **DSP+光学架构(混合)** | A✅B(部分)✅C✅D✅ | ✅ | 三PD消奇异;OSNR penalty 2.21dB下行/3.76dB上行；⚠️**self-coherent比coherent差**⚠️35000km GEO非LEO |
| **新4** | **10.1109_JLT.2023.3281082 PCS+Rs治Doppler(=landscape #580)** | **PS方向/Doppler治理** | **DSP自适应调制(Rs+H联合)** | **A✅B✅C✅D✅** | **✅** | ±15GHz极端Doppler ABR仍~600Gbps,vs固定80Gbaud **~100Gbps增益**；⚠️**增益来自符号率适配非PS**⚠️PS在proposed/baseline都用 |
| **新5** | **10.1109_LPT.2025.3647750 PS+RCM治湍流(西南交大)** | **PS方向/治湍流** | **DSP相位共轭+调制器偏置** | A✅B✅C✅D⚠️ | **⚠️部分(PS/RCM消融不完整)** | BER中强湍流<SD-FEC；⚠️**无具体dB增益**⚠️地面短距非星地无Doppler⚠️PS高SNR趋零(N1同构) |
| **新6** | **10.3390/app11219805 PS-QAM理论(Appl Sci 2021)** | **PS方向/PS-QAM理论** | **编码调制(PMF优化+LDPC)+PEP闭式** | **A✅B✅C✅D✅** | **✅** | 0.4dB(AIR)/1.3dB(post-FEC)；⚠️**高度同构N1**(高SNR>16dB uniform反超PS趋零)⚠️纯仿真无硬件⚠️无相位畸变建模 |

**候选池判定**：10 篇，其中 **6 篇四判据全过（#1/#2/#3/新2/新4/新6）**，远超 gw-read.md ≥5 篇门槛。**块 C 综合分析可启动**。

## 下一步干什么（块 C 综合分析）

**按 gw-read.md 综合分析节撰写**（精读完成后撰写，本轮不做——H004 纪律"不在本轮做综合分析/Q#"，已到步骤上限）：

1. **现有方法分类**：按技术路线分类 10 篇，每类 2-3 句（含具体方法名）。从精读可见的类别：①载波恢复/频率估计（#1/新1/新4）②均衡（#3/新2/新3）③相位恢复（#2）④概率整形（新4/新5/新6）⑤检测架构（新3）
2. **已知局限**：10 篇的共同不足（从 conclusion/future work 提取）
3. **2-3 年趋势**：从发表年份+方法演进推断（PS 趋势？符号率自适应趋势？全数字 vs 光学趋势？）
4. **研究背景概述**：领域脉络时间线+核心技术挑战+本研究定位
5. **研究问题清单 Q# [MUST]**：把 10 篇的 M-C-A 汇总成跨论文问题清单，逐条过 glossary.md 四判据。这是 Contract Step 1 假设的唯一合法引用来源。未过四判据标❌+缺哪条。

**Q# 浮出的观察线索（仅供块 C 参考，不是结论）**：
- 新4（PCS+Rs 治 Doppler）的方法**最有"同门范式"味道**：场景约束(LEO Doppler+COTS带宽限制)→现有方法失效(数字法忽略非对称滤波/光学法难集成)→切入点(符号率+PS联合适配)。增益 100Gbps 量级硬。
- 新1（Doppler跟踪）虽 C/D 不过（无BER-vs-baseline），但方法形态（AFC闭环+CFR前馈实时FPGA）跟同门纯DSP范式最对路，BUPT 同国别团队。块 C 可考虑作"方法借鉴"而非"直接Q#"
- PS 三篇里：新4(PS作使能件，不同构N1，增益来自符号率)> 新5(PS半核心，部分同构N1，消融不全)> 新6(PS纯核心，高度同构N1)。块 C 提炼Q#时，**PS方向优先看新4的角度**（PS+另一个机制治具体失效），避开纯PS gain（N1 已证无效）

## 纪律（和块 C 直接相关的约束）

1. **不跳四判据终审进 Step 4a**（块 C 产 Q# 清单，4a 才判 Go/No-Go）
2. **不塞方向给用户**——综合分析给数据+Q#清单，让用户拍板
3. **Q# 必须从 10 篇 M-C-A 汇总浮出，不从单篇联想**（TL-30/31）
4. **重写 literature_notes.md**（旧文件过时，H004 已知债务）— 块 C 把 10 篇精读条目统一写入
5. **PS 方向警惕 N1 同构**：提炼 PS 相关 Q# 时，必须核查"增益是否依赖时变信道"。纯固定信道 PS gain≈0（N1 已证），只有 PS+另一机制治具体失效（如新4的符号率适配）才有戏
6. **场景对称性核查**：新2 是 LEO-LEO 真空（非星地），新3 是 35000km GEO（非 LEO），新5 是地面短距。提炼 Q# 时注意链路类型匹配用户标题"星地"

## 必读（块 C 综合分析新对话开始时按此顺序读）

1. **本文件 H005**（交接当前状态+候选池表）
2. **H004**（块 A/B 全流程 + 选样返工决定，本文件是其续接）
3. **topic-index.md 不变量段**（D005 务实路线是第1条 INVARIANT；判据A已降级）
4. **decisions.md D005+D004+D003**（务实标准 + 找角度范式 + 回Step3）
5. **thesis-lessons.md TL-30/31/32/33**（跳步/凭记忆/标准不对称/自欺式跳步）
6. **stages/gw-read.md 综合分析节**（方法分类/局限/趋势/背景/研究问题清单 Q# 的撰写要求）
7. **stages/glossary.md 四判据**（注意 D005 把判据 A 从"真缝"降级为"baseline 不够好+改进空间"）
8. **10 篇精读笔记**（papers/_read_notes/ 下，read-log.md 有索引）。重点读 6 篇四判据全过的（#1/#2/#3/新2/新4/新6）的"问题提取"子表

## 接口变更（如有代码改动）

无代码改动（本轮全是检索+下载+精读+笔记落盘+文档交接）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| literature_notes.md 是旧方向 | gw-read.md 要求精读入 literature_notes.md | 10 篇全在 papers/_read_notes/ + read-log.md，未入 literature_notes.md | **块 C 综合分析时重写 literature_notes.md 统一写入** |
| master-state.md GW Progress 表 Step 2/3 仍 ⬜ | FR-22 唯一可查状态 | 本轮精读 10 篇但 Step 3 完成标志=literature_notes.md(含Q#)，综合分析没做完不算 Step 3 完成 | 块 C 产 Q# 清单后更新 GW Progress 表 |
| tools/download urllib 不走代理 | 下载工具应能下 OA/IEEE | 本轮用 blit 绕过，但非 IEEE 源(SPIE/Optica/MDPI)仍下不到 | 需要时修 paper_download.py 加 _detect_proxy（仿 S005 blit 修法） |
| #590 ECOC 2022 无 DOI 未下 | Step 2 下载完整性 | #580(JLT 期刊版)已下，信息更全，#590 暂可缺 | 块 C 若需 #590 细节再处理 |
| PS 方向 N1 同构风险 | D005"不画饼救旧" | 新6 高度同构 N1，新5 部分同构，新4 不同构 | 块 C 提炼 Q# 时按"PS+另一机制治具体失效"筛，避开纯 PS gain |

## 验证阈值（如涉及验证体系）

本轮不涉及验证体系。后续 Go/Kill 标准（务实路线下，D005）：
- **Go**：方法 > 传统未优化 baseline（参考同门 2-4dB 量级，具体阈值块 E 定）
- **Kill**：连传统 baseline 都赢不了 / 方法增益 <0.5dB 且无次指标维度 / MVE FAIL
- **不放水**：不接受孤证/伪命题/标题联想（底线）
- **PS 方向额外**：纯 PS gain（固定信道）≈N1 已证无效；PS+另一机制治具体失效才考虑

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（D005 务实路线是第 1 条 INVARIANT）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 本轮精读 6 篇笔记已落盘（核查：`ls papers/_read_notes/ | grep -E "11350922|3287501|3535789|3281082|3647750|app11219805"`）
  - [ ] read-log.md 已追加 6 条（核查：`grep -c "2026-06-26" projects/thesis-fso/read-log.md` 应≥10）
  - [ ] blit 下载的 3 篇 IEEE 全文已转 markdown（核查：`ls papers/blit-downloads/2026-06-26/*.md`）
- [ ] 已检查 _registry.yaml 中本专题 status = active（无 conflicts_with）
- [ ] 已确认当前范围未违反"明确不含"（仍要导师同意 S007 边界 / 仍不接受孤证凑数 / 方法必须指标提升 / 不跳四判据不跳 Go）

## 下一轮（块 C 综合分析）

**先做完块 C（综合分析+Q#清单）再进块 D（Step 3.5 定向补检索）→ 块 E（Step 4a Go/No-Go）**，严格不跳步：

### 块 C 任务（1 个对话）
1. 读本 H005 + 10 篇精读笔记（重点 6 篇四判据全过的）
2. 按 gw-read.md 综合分析节撰写：方法分类 / 已知局限 / 2-3年趋势 / 研究背景概述 / **研究问题清单 Q#**
3. Q# 清单：10 篇 M-C-A 汇总，逐条过四判据（D005 修正判据 A），标 ✅/❌
4. 重写 literature_notes.md（旧文件过时）— 把 10 篇精读条目统一写入 + 综合分析节
5. Q# 清单非空且至少 1 条四判据全过 → 进块 D；全 ❌ → 回补检索（块 A 重来或扩检索词）

### 块 D（Step 3.5 定向补检索，0.5-1 对话）
- 用块 C Q# 清单的新认知做一轮定向检索弥补盲区（groundwork.md:33 必做）

### 块 E（Step 4a Go/No-Go，1-2 对话）
- 每个 Q# 走 gw-feasibility 维度 A0/A'/A/B/D
- 务实标准：维度 A 对手=传统 baseline；FR-21 只当参考；MVE 快速试错
- 至少 1 个 Q# Go 才进块 F（Step 5-7 baseline 复现）

**关键提醒**：
- **不跳步**：块 C 没做完不进块 D/E
- **Q# 从 10 篇浮出**：不从单篇联想，不标题联想试 MVE（TL-30）
- **PS 警惕 N1 同构**：纯 PS gain 无效，PS+另一机制治具体失效才考虑
- **场景匹配**：新2 星间/新3 GEO/新5 地面，提炼 Q# 时注意链路类型匹配用户标题"星地"
- **导师边界**：S007 已定 feeder/ISL/网络层/ATP/QKD/深空不算处理（新2 是 LEO-LEO 星间，提炼 Q# 时留意——但其 DS 补偿 DSP 模块本身是处理技术，且 S007 边界说"ISL 系统级不算"，DSP 模块级可能算，块 C 需判断）

**不要在块 C 做**：不判 Go（块 E 的事）/ 不跑 MVE（块 E 的事）/ 不改框架文件（D004 待 Step 3 验证后再改）。
