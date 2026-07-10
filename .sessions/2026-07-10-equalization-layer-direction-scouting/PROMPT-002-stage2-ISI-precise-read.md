# 新对话提示词：阶段 2 精读批次 1（ISI 均衡子地带）

> 来源: S006（阶段 1.5 选地，用户 2026-07-10 拍板 ISI+AO-DSP 都精读）| 交接目标: 新对话执行阶段 2 精读批次 1
> 文件名: PROMPT-002-stage2-ISI-precise-read.md
> 日期: 2026-07-10
> 专题: `.sessions/2026-07-10-equalization-layer-direction-scouting/`

---

## 你是谁 + 本轮目标

你是均衡层方向侦察专题的**阶段 2 精读批次 1** 工作对话（GW Step 2/3）。**角色 = 精读 ISI 均衡子地带论文 + 提取 M-C-A + 产 Q# 候选，不判 Go/Kill**（那是阶段 4，判地是阶段 3）。

**本轮目标**：精读 ISI 均衡子地带的核心论文，按 gw-read 流程提取 M（方法）/C（条件）/A（失效原因），产出 Q# 候选（≥3 条，禁单假设），写入 literature_notes.md ISI 段。

## 背景（理解任务必需的）

### 已完成的上游（阶段 0-1.5）

1. **阶段 0 流程规划**（S001）+ **索引机制**（S002-S003）
2. **阶段 1 地勘前置**（S004-S005）：6 组检索，产出 `projects/simulation/landscape-equalization.md` 完整版（~46 篇 + 8 子地带 + 4 死地）。信噪比合格 8 项全过。
3. **阶段 1.5 选地**（S006）：
   - 代码核查确认场景 = **单偏振 intradyne 单孔径单链路**星地 GG 湍流（SPEC.md:13/17 + _channel.py + _modulation.py:6）
   - **D002 排除 MDCC**（多孔径冲突，B3-Q2 前车）+ **偏振均衡**（单偏振不匹配）
   - **D003 双偏振物理前置验证倾向伪需求**（Toyoshima 2009 OICETS 实测 DOP 99.4%，大气几乎不退偏，B7 风险）
   - **D004 选 ISI 均衡 + AO-DSP 残余补偿都进精读再筛**（本对话做 ISI，下对话做 AO-DSP）

### 为什么选 ISI 均衡

- **适配场景**：ISI 是标量信号时域损伤，单偏振单孔径 intradyne 相干直接适用，不碰载波同步边界
- **符合用户诉求**："符合标题（星地相干信号处理）+ 不很难做"
- **风险**：原生 Trans 基线薄（仅 TCOMM 2026 Ajam 单篇），要靠光纤领域 DFE/FDE 迁移补 baseline 池

### 最关键的纪律（INVARIANT 6 + 7 + 19）

- **INVARIANT 6（abstract 工具错位）**：地勘阶段 abstract 只标了 🟢🟡/🔴 粗判，**没判 baseline 真失效**。精读全文才能判判据 A。本对话开始判缝（移到全文层了），但仍守"全摸完排优先级不边摸边 Kill"（D018）。
- **INVARIANT 7（§7.2 三硬规则）**：全文真实性 / 立场不可扭曲 / 孤证就是孤证。每个精读批次后**主线独立 grep 核查**。
- **INVARIANT 19（精读分层）**：Trans 必精读作 baseline 池主力；Letters/会议做扩写溯源（已扩成 Trans 读 Trans，未扩写读本身）；**红线：Letters/会议不能当主 baseline**。

## 开工前必读（按优先级）

**开工第一步**：读必读清单 + 做 H003 接收方验证清单。

1. `.sessions/2026-07-10-equalization-layer-direction-scouting/topic-index.md` —— 20 不变量（重点 INVARIANT 6/7/18/19）+ 当前位置（D004）
2. `.sessions/2026-07-10-equalization-layer-direction-scouting/decisions.md` —— **D002（场景适配排除 MDCC/偏振）/ D003（双偏振伪需求）/ D004（选 ISI+AO-DSP）必读**
3. `projects/simulation/landscape-equalization.md` —— **ISI 子地带主表 #29-33**（§子地带 4 补全）
4. `.sessions/2026-07-10-equalization-layer-direction-scouting/H003-stage2-precise-read-ISI-AODSP.md` —— 阶段 2 交接（接收方验证清单在里面）
5. `stages/gw-read.md` —— 精读流程规范（GW Step 3）
6. `papers/doi/10.1002_sat.1553/content.md` —— sat.1553 综述（已落盘，§6 均衡器段，精读 baseline 参考）

**接收方验证（H003 要求，开工时做）**：
- [ ] 已读 topic-index 不变量段 + D002/D003/D004
- [ ] 验证 3 条事实：场景=单偏振（读 _modulation.py:6）/ landscape ISI #29-33 存在 / D003 Toyoshima DOP 99.4% 数据真实
- [ ] 确认范围未违反"明确不含"（不回头载波同步 / 不碰 MDCC/偏振/OAM）

## 任务详情

### 要回答的问题（精读完回答）

**ISI 均衡子地带在单偏振 intradyne 单孔径星地相干场景下**：
1. baseline 方法 M 是什么？（TCOMM 2026 Ajam 的 OOK+ZF-LE / OOK+DFE / DCO-OFDM，+ 光纤迁移的 DFE/FDE）
2. 在什么条件 C 下 M 失效或不足？（高速率致 ISI？IRS-induced delay dispersion？湍流加剧 ISI？）
3. 失效原因 A 是什么？（判据 A = baseline 真失效，全文层精读才能判）
4. 有没有改进切口能赢传统 baseline 几 dB？（D005 务实路线）
5. 凑得齐 D-010 标准 4 篇 Trans baseline 吗？（原生 + 光纤迁移）

**不回答**（本对话禁做）：
- ❌ 不判 Go/Kill（阶段 4）
- ❌ 不下"ISI 地有没有缝"结论（阶段 3 判地）
- ❌ 不建代码（阶段 5 后）
- ❌ 不碰 AO-DSP（下对话做）

### 执行方式

#### 精读范围（ISI 子地带，按 INVARIANT 19 分层）

**Trans 必精读（baseline 池主力）**：
1. **TCOMM 2026 Ajam** — Modeling & Mitigation of ISI in High Rate IRS-Assisted FSO Links（landscape #29，DOI 10.1109/TCOMM.2025.3636084）
   - **⚠ 注意**：Ajam 是 IRS-FSO **PD 接收**（非相干？），精读第一步要确认是否跟 intradyne 相干场景匹配。若 PD 接收跟相干差太远，降级为"参考"不当主 baseline
2. **光纤迁移 DFE/FDE 经典 Trans**（凑 D-010 标准 4 篇）—— 这是 ISI 子地带 baseline 池主力来源，因为星地原生 Trans 薄。用 tools/search 找光纤领域 DFE/FDE 的 Trans 级经典（如 Proakis/Digital Communications 的 DFE、Falconer 2002 FDE、或光通信里的电子色散补偿 EDC）

**老孤证参考（快速过，不深读）**：
3. Lee & Kavehrad 2009 — FSO with channel shortening filter + Viterbi（#32，abstract 缺失，老文）
4. Lee & Kavehrad 2006 — Airborne laser comm impulse response shortening + Viterbi（#33，cloud 多散射 ISI）

#### 执行步骤（本对话 ≤3 步，守 AGENTS.md）

**步骤 1：下载 + 找迁移 baseline**
- 下载 TCOMM 2026 Ajam：`bash tools/download --doi 10.1109/TCOMM.2025.3636084`
- 找光纤 DFE/FDE 迁移 Trans：`bash tools/search 'fiber optical decision feedback equalizer frequency domain equalizer electronic dispersion compensation coherent' --format markdown`
- **下载现实**：TCOMM 2026 可能 paywall。若失败：试 arXiv / Unpaywall / 作者主页，如实报告失败不编。若全失败，从 abstract + sat.1553 综述转述提取（标"二手"）

**步骤 2：子 agent 精读（gw-read 流程）**
- 论文全文精读**必须子 agent**（AGENTS.md 强制委托）
- 子 agent 读 content.md，返回按 gw-read 模板的结构化提取（M-C-A + Q# 候选 + baseline 详情 + 四判据初筛）
- 子 agent ≤900s，拆分应确保单个工作量在此范围

**步骤 3：主线集成 + §7.2 核查 + 写 literature_notes**
- 主线汇总子 agent 结果 → 写入 `projects/simulation/literature_notes.md`（ISI 均衡段，若文件不存在新建）
- **§7.2 主线 grep 核查**：抽精读论文的关键声称，grep 原文 content.md 核验（不编 line/不扭曲立场）
- M-C-A 提取 + Q# 候选（≥3 条）+ 四判据初筛
- 写 S007 session note + H004 交批次 2（AO-DSP）

### 产出格式（强制）

#### literature_notes.md ISI 均衡段（每篇论文一条）

按 gw-read 模板（见 stages/gw-read.md），每篇提取：
- **L## 编号** + 标题 + 作者 + 年份 + 档级 + DOI
- **M（方法）**：做了什么，一句话
- **C（条件）**：在什么场景/条件下
- **A（失效原因）**：baseline 在 C 下因 A 失效/不足（判据 A，全文层判）
- **Q# 候选**：改进切口（≥3 条，禁单假设）
- **四判据初筛**：具体技术矛盾 / 有方法产出形态 / 有 2019+ baseline / 能做对比
- **baseline 详情**：对照谁，增益多少 dB，什么场景
- **范围 in/out**：星地 + 湍流 + 不撞载波同步边界？

#### S007 session note（按 S### 模板）

#### H004 handoff（交批次 2 AO-DSP，按 H### 模板 + 接收方验证清单）

## 已知陷阱（基于历史失败的具体案例）

### 陷阱 1: Ajam PD 接收 vs 相干场景不匹配（本批特有风险）
- **症状**：TCOMM 2026 Ajam 是 IRS-FSO PD（直接检测）接收，不是 intradyne 相干。精读发现 PD 接收的 ISI 机制跟相干差太远
- **避免**：精读第一步确认 Ajam 接收体制。若 PD 跟相干差远，降级为"参考"不当主 baseline，主力靠光纤迁移 DFE/FDE

### 陷阱 2: 光纤迁移 baseline 的合法性（凑池风险）
- **症状**：ISI 原生 Trans 薄，靠光纤 DFE/FDE 迁移凑 4 篇。但光纤 ISI 机制（色散）vs 星地 ISI 机制（湍流/IRS-delay）可能不同
- **避免**：迁移 baseline 要论证"机制同构"（ISI 都是时域色散展宽，DFE/FDE 原理通用）。标"光纤迁移，机制待验证"

### 陷阱 3: 边读边 Kill（profile 第 6 次纠偏 + D018）
- **症状**：读到一篇 baseline 不够强就想 Kill 整个子地带
- **避免**：全摸完排优先级（D018）。本批只产 Q# 候选 + 四判据初筛，不 Kill

### 陷阱 4: 单假设验证（6 次 Kill 教训）
- **症状**：只提 1 个 Q# 就想往下走
- **避免**：**≥3 条 Q# 候选**（INVARIANT）。多候选发现，禁 Q#-A 单假设模式

### 陷阱 5: 造假（§7.2 三硬规则）
- **症状**：论文没下载却报 line 编号 / 立场被扭曲
- **避免**：①全文真实性（abstract 也要从真实结果提取）②立场不可扭曲 ③孤证就是孤证。每批次后主线 grep 核查

### 陷阱 6: 主对话禁 WebSearch（AGENTS.md 强制）
- **避免**：所有检索走 tools/search + tools/blit；web 查询子 agent 消化返回 ≤500 词

## 验收（主线拿到产出后怎么检查）

- [ ] `literature_notes.md` ISI 段存在，每篇 M-C-A + Q# 候选 + 四判据初筛 + baseline 详情
- [ ] Q# 候选 ≥3 条（多候选，禁单假设）
- [ ] §7.2 核查：抽 2 篇 grep 原文核验 abstract/结论提取真实（不编 line/不扭曲立场）
- [ ] Ajam 接收体制确认（PD vs 相干，是否降级）
- [ ] baseline 池凑池可行性评估（原生 + 光纤迁移，够 D-010 4 篇 Trans 吗）
- [ ] **没有 Go/Kill 结论**（只产 Q# 候选 + 四判据初筛，判地/Go-Kill 留阶段 3/4）
- [ ] S007 session note + H004 handoff 落盘

**验收不过 → 补精读或修造假，不进阶段 2.5 矩阵**。

## 纪律（和本任务直接相关的约束）

1. **INVARIANT 6（abstract 工具错位）**：精读才判判据 A（全文层），但全摸完排优先级不边摸边 Kill
2. **INVARIANT 7（§7.2 三硬规则）**：全文真实性 / 立场不可扭曲 / 孤证就是孤证 + 主线 grep 核查
3. **INVARIANT 19（精读分层）**：Trans 必精读作 baseline 主力；Letters/会议扩写溯源；Letters 不当主 baseline
4. **D018（中性提取）**：全摸完排优先级，不边摸边 Kill
5. **≥3 Q# 候选**（禁单假设，6 次 Kill 教训）
6. **不碰 AO-DSP / MDCC / 偏振 / OAM**（D002/D003 排除，本对话只做 ISI）
7. **论文全文精读必须子 agent**（AGENTS.md 强制委托）
8. **主对话禁 WebSearch**（走 tools/search，web 查询子 agent 消化）
9. **单对话 ≤3 步**（下载+找迁移 → 子 agent 精读 → 主线集成+核查+写 note）

## 接口变更（代码改动）

无（精读不写代码，只产 .md）

## 下一轮

**本对话（阶段 2 批次 1）产出**：literature_notes.md ISI 段（M-C-A + ≥3 Q#）+ S007 + H004

**阶段 2 批次 2（下一对话）= AO-DSP 残余补偿**：
- **⚠ 边界检查前置**：Paillier 2020 JLT（#34）DSP 段余是载波 PLL 还是信号域？载波域 → 排除
- 精读 Li 2022 JLT SIC（#40）+ Fontaine 2019 ECOC（#37）+ Kim 2007 EL（#38 扩写溯源）
- 同样 M-C-A + Q# + §7.2 核查

**阶段 2.5（两批精读后）= 方法-改进矩阵**（INVARIANT 20）：横向汇总每方法所有改进+效果，空格=机会

**不在本对话做**：
- 不判 Go/Kill（阶段 4）
- 不下"ISI 地有没有缝"结论（阶段 3）
- 不做 AO-DSP（批次 2）
- 不建代码（阶段 5 后）
