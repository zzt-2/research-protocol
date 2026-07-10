# [S004] 阶段 1 地勘前置第 1 批执行（组 1-3 检索 → landscape-equalization.md 初版）

> 2026-07-10 | GW Step 1 地勘前置 | 状态：完成（第 1 批产出落盘，待第 2 批组 4-6）
> 来源：PROMPT-001 任务书（S001 产出，用户"写吧"确认后派发）

## 目标

执行阶段 1 地勘前置第 1 批：跑组 1-3 检索（equalization 总览 + 偏振 + MIMO），产出 `projects/simulation/landscape-equalization.md` 初版（全留拉表 + 7 子地带分类 + 死地记忆 + seed.md 交叉核 + 档级标注）。**角色 = 执行地勘检索 + 拉表，不判方向不判 Go/Kill**。

## 记录

### 1. 执行方式

3 个子 agent 并发执行（每批 ≤3 并发，AGENTS.md 规则）：
- 组 1（equalization 总览）：2 个查询（S2+OpenAlex + problem-driven preset）+ 1 blit IEEE → 12 篇相关
- 组 2（偏振/PMD/PolDemux）：2 个查询 + 1 blit IEEE → 8 篇 FSO 相关 + 6 篇光纤背景
- 组 3（MIMO/spatial diversity/multi-aperture）：2 个查询 + 1 blit IEEE（命中 1 篇关键 JLT）→ 26 篇相关

子 agent 耗时：277s / 289s / 314s，均远低于 900s 上限 ✅。

### 2. 源状况（诚实标注，影响后续召回策略）

| 源 | 状态 | 影响 |
|---|---|---|
| S2 + OpenAlex | 正常 | 本批主力 |
| **Exa** | **信用额度耗尽**（NO_MORE_CREDITS）| 失去语义搜索，可能漏关键词不匹配但语义相关论文 |
| SerpAPI / Tavily | 未安装 / 连接重置 | 召回源减少 |
| **IEEE blit** | **3 次查询均 0 命中**（会话用量 1/50）| venue 字段靠 OpenAlex/S2 container_title，可能漏 IEEE 全文库独有论文（PTL/CL 等）|

**对第 2 批的建议**：Exa 失效后召回能力下降，第 2 批组 4-6 要么靠 S2+OpenAlex 裸跑（关键词质量更关键），要么先解决 Exa 信用/装 SerpAPI。ISI 子地带本批仅孤证，第 2 批组 4 是重点追对象。

### 3. 产出：landscape-equalization.md 初版

`projects/simulation/landscape-equalization.md`，含：
- **7 子地带**：multi-aperture coherent combining(MDCC) / OAM-MIMO / 偏振均衡 / ISI 均衡 / OFDM-FSO / DNN-NN 均衡 / AO-DSP 残余补偿
- **29 篇主表**（每篇 8 字段：子地带/做的事/档级/年份/湍流相关/baseline/缝潜力初判）
- **3 个 🔴 死地**：OAM-MIMO 族（12 年饱和）/ 偏振经典外差奠基思路 / OFDM 解析性能类
- **seed.md 交叉核**：核心 7 篇 Trans/Letters 命中一致；OAM 🔴 确认；MDCC 🟢 强确认；ISI 对不上（seed 11 篇含 TCOMM 2026，本批仅 1 篇）→ 组 4 重点追
- **范围出界标注**：ISL(Vieira 2023) / 纯仿真(PDM-256QAM 2023) 只标不砍
- **红线检查**：2 篇偏同步排除，无载波同步混入主表 ✅

### 4. 子地带活跃度初步观察（abstract 粗判，**不判 baseline 真失效**）

| 子地带 | 活跃度 | 本批证据 | 缝潜力 |
|---|---|---|---|
| **MDCC（multi-aperture coherent combining）** | **最活跃** | Geisler 2016 奠基(OE) → Liu/Ju 2023-2024 DSP 进阶(JLT/OE/OL) → Johst 2024 + Chen 2026 BGAPA | 🟢 |
| 偏振均衡（DP 自相干+湍流偏振混叠切口）| **升温** | Cvijetic 2010 奠基 → ANN 2026 / VAE 2026 / DP 仿真 2025 | 🟢（多孤证）|
| DNN/NN 均衡 | 新兴但 Trans 级少 | Kulmer 2026(OE) / Qin 2025(OFC) / ANN#16 / VAE#17 跨子地带 | 🟢（多孤证）|
| OAM-MIMO | **🔴 饱和** | Ren 2015/2016 + Yousif 2019 + Wang 2021 综述收口 | 🔴 |
| ISI 均衡 | **待查**（本批孤证）| Zhang 2018 单篇；TCOMM 2026 未召回 | 🟡（组 4 补）|
| OFDM-FSO | 偏理论分析 | Wang 2015 解析类；Chen 2014 NE-OFDM 反向；Elsayed 2024 UAV | 🟡 |
| AO-DSP 残余补偿 | 边缘召回 | Horst 2023 / Zhang 2021 / Zhu 2021 | 🟡（组 5 补）|

**⚠️ 守 INVARIANT 6**：以上"活跃/升温/新兴"是 abstract 层观察（多方法并存可能竞争 = 🟢），**不是判 baseline 真失效**。判缝移全文层（阶段 2/3）。

### 5. 信噪比合格判据（PROMPT-001 验收）

- [x] 子地带覆盖 ≥3 个不同 → **7 个** ✅
- [x] 候选论文够多 → 29 篇主表 ✅
- [x] 档级标注完整（Trans/Letters/会议/期刊/preprint 分层）✅
- [x] 🔴死地记忆段有理由 + 代表论文 ✅
- [x] 无载波同步混入（红线 PASS）✅
- [x] 检索覆盖度诚实（列了未覆盖：组 4-6 / Exa 失效 / IEEE blit 0 命中）✅
- [x] **没有判据 A 结论**（没下"baseline 真失效"，只标 🟢/🟡/🔴 粗判）✅

### 6. §7.2 三硬规则自检（造假防线）

- **全文真实性**：所有字段从子 agent 返回的真实检索结果提取，未编造。子 agent 报告中"abstract 未提"的 baseline 老实标"abstract 未提"。
- **立场不可扭曲**：abstract 说啥写啥（如 Cvijetic 2010 说"well-known 均衡消除 XPI"就写这个，不扭曲成"提出新均衡")。
- **孤证就是孤证**：ISI 均衡(Zhang 2018 单篇)/ANN 偏振(#16 单篇)/VAE 偏振(#17 单篇)/NN combining(Kulmer 单篇)/VQ-VAE MIMO(Qin 单篇) 全标了孤证。
- **主线独立核查**：本批 S004 作者 = 主线，对子 agent 返回结果做了交叉核（seed.md 对照 + 子地带归并去重 + 红线检查）。**建议下批前主线随机抽 3 篇 grep 核查 abstract 提取真实性**（守 INVARIANT 7）。

## 决策引用

- 无新建 D###（地勘阶段不判方向，仅产清单）。本批是 PROMPT-001 任务书的执行。
- 引用既有：INVARIANT 6 abstract 工具错位 / INVARIANT 5 地勘前置 / INVARIANT 7 §7.2 / INVARIANT 18 星地 / INVARIANT 19 档级标注

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 1 地勘前置第 1 批，PROMPT-001 框定）
- 未触发 Trigger 3（扩大范围）。严格守"只拉表不判方向"

## 后续

**阶段 1 第 2 批（下一对话，新 PROMPT-002 或续接）**：
- 跑组 4-6（ISI 深查 / AO-DSP 残余补偿 / 湍流补偿）
- 补检索（Exa 失效后的召回缺口，尤其 ISI 子地带 + IEEE PTL/CL 独有论文）
- 信噪比合格终判 → 阶段 1 收尾 → 进阶段 1.5 选地（交主控对话 + 用户拍板）

**主线核查建议**（第 2 批对话开工时做，守 INVARIANT 7）：
- 随机抽 landscape 主表 3 篇，grep 子 agent 返回的原始搜索结果 JSON，核查 abstract 提取是否真实（不编 line/不扭曲立场）

**ISI 子地带是第 2 批重点追**（本批孤证 + seed 标 TCOMM 2026 未召回 + 两表对不上）。
