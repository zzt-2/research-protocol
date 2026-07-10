# Handoff: 阶段 1 地勘全部完成 → 阶段 1.5 选地（交主控 + 用户拍板）

> 来源: S004 + S005 | 交接目标: 主控对话 + 用户拍板选均衡子地带
> 文件名: H002-landscape-complete-to-site-selection.md
> 日期: 2026-07-10

## 已完成边界

**阶段 1 地勘前置全部完成（两批 6 组检索）**：
- 第 1 批组 1-3（equalization 总览/偏振/MIMO）+ 第 2 批组 4-6（ISI 深/AO-DSP/湍流补偿）
- 产出 `projects/simulation/landscape-equalization.md` **完整版**：~46 篇主表 / 8 子地带 / 4 🔴死地 / seed 交叉核 / 档级标注 / 范围出界标注 / 红线检查
- §7.2 主线核查两批各抽 3 篇共 6 篇全 PASS（无造假）
- **信噪比合格终判 8 项全过** → 阶段 1 收尾

**做到哪一步**：地勘完成。**下一步是阶段 1.5 选地，不是精读不是判 Go/Kill**。

## 下一步干什么

**阶段 1.5 选地**（主控对话 + 用户拍板）：
1. 打开 `projects/simulation/landscape-equalization.md`，读"子地带活跃度初判表"（文末）+ 各子地带主表
2. 给用户 **8 个子地带的候选摘要**（不预设不替选，守 INVARIANT 5）：
   - 每个子地带：活跃度 / Trans baseline 厚度 / 死地与否 / 已知边界风险
3. 用户拍板选 **1-2 个均衡子地带**进阶段 2 精读
4. **重点提示用户**（facts-first，帮用户决策但不替用户决策）：
   - MDCC 子地带 Trans 基线池最厚（精读效率最高），abstract 层最活跃
   - OAM-MIMO 是 🔴 死地（已饱和）
   - AO-DSP 残余补偿含载波恢复边界风险（Paillier 系落"载波同步已完成"边界附近）

## 不要做什么

1. **不要替用户选地**（profile durable + INVARIANT 5）。主控给候选摘要 + 事实，用户拍板。
2. **不要用 landscape 的 🟢🟡🔴 当 Go/Kill**（INVARIANT 6）。那是 abstract 层粗判（多方法并存可能竞争），不是判 baseline 真失效。判缝移全文层（阶段 2/3）。
3. **不要跳过选地直接精读**（阶段 1.5 → 阶段 2，FR-22）。用户拍板选地后才进阶段 2。
4. **不要碰 OAM-MIMO 死地**（🔴 12 年饱和 + 综述收口）。
5. **不要把 AO-DSP Paillier 系当均衡层 baseline**（DSP 残余实质是载波 PLL，边界警示，阶段 2 精读需核）。
6. **不要在第 1.5 阶段急判方向**（profile durable：看全再判）。选地只选"去哪精读"，不判"哪有缝"。

## 必读（下一对话开始时按优先级读）

1. `projects/simulation/landscape-equalization.md` —— **地勘完整产出**，文末"子地带活跃度初判表"是选地核心参考
2. `.sessions/2026-07-10-equalization-layer-direction-scouting/topic-index.md` —— 20 不变量（INVARIANT 5/6/18/19 重点）
3. `.sessions/2026-07-10-equalization-layer-direction-scouting/S005-landscape-preflight-batch2-and-stage1-closeout.md` —— 第2批 + 收尾细节，§7 子地带活跃度表
4. `.sessions/2026-07-10-equalization-layer-direction-scouting/S004-landscape-preflight-batch1.md` —— 第1批执行细节 + 源状况
5. `.sessions/2026-07-10-equalization-layer-direction-scouting/voice.md` —— 用户原话（"宽：FSO 相干均衡全谱" / INVARIANT 19/20 由来）

## 子地带候选摘要（给主控 + 用户选地用）

| 子地带 | 活跃度 | Trans baseline 厚度 | 缝潜力 | 已知风险 |
|---|---|---|---|---|
| **MDCC（multi-aperture coherent combining）** | 🟢 最活跃 | **最厚**（JLT/OE/OL: Geisler/Liu/Ju/Johst）| 🟢 | 无 |
| 偏振均衡（DP 自相干+湍流偏振混叠）| 🟢 升温 | 中（Cvijetic JLT + ANN/VAE 2026）| 🟢（多孤证）| 多孤证待补证 |
| DNN/NN 均衡 | 🟢 新兴 | 薄（多孤证 Trans 级少）| 🟢（多孤证）| Trans 级少，D-010 标准4 baseline 凑不齐风险 |
| ISI 均衡 | 🟡 稀疏+新切口 | 薄（TCOMM 2026 单篇）| 🟡 | IRS-induced ISI 是全新切口但仅 1 篇 Trans |
| AO-DSP 残余补偿 | 🟡 中等 | 中（Paillier JLT + Kim EL）| 🟡 | **⚠ 载波恢复边界**（Paillier DSP 残余=PLL）|
| OFDM-FSO | 🟡 偏理论 | 薄 | 🟡 | 解析类饱和，工程实体少 |
| OAM-MIMO | 🔴 死地 | — | 🔴 | 12 年饱和，勿碰 |
| 湍流信道均衡 | 🟡 横切（非独立带）| — | 🟡 | 非独立子地带 |

> **⚠ 这是 abstract 层初判（供选地参考），不是方向结论。守 INVARIANT 6：未判 baseline 真失效。**

## 关键事实（接收方需知道）

### 源状况债务（影响阶段 2 精读下载）
- **Exa 信用耗尽**（两批都失效）→ 失去语义搜索
- **IEEE blit 7 次仅 1 命中** → 近乎失效，可能漏 IEEE 独有论文（PTL/CL）
- **SerpAPI 未装 / Tavily 失效**
- 阶段 2 精读下载主要靠 arXiv + OA PDF + Unpaywall（tools/download），付费墙是常态

### §7.2 核查结果（两批 6 篇全 PASS）
- 第 1 批：Kulmer/VAE/Liu2023（Liu2023 论文真实但来源归因存疑——可能来自 seed 非 blit，非造假）
- 第 2 批：TCOMM2026/Senthilkumar/Ahmad2026 全 PASS
- 阶段 2 每个精读批次后仍需主线独立 grep 核查（守 INVARIANT 7）

### 信噪比合格终判 8 项全过
子地带 8 个（≥3 ✅）/ 候选 ~46 篇 / 档级完整 / 4 死地 / 无载波同步混入 / 覆盖度诚实 / **无判据 A 结论** / §7.2 全 PASS

## 接口变更（代码改动）

无（地勘不写代码，只产 .md）

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Exa/SerpAPI/IEEE blit 召回能力下降 | 全覆盖检索（INVARIANT 5）| 两批靠 S2+OpenAlex 裸跑 | 阶段 2 精读前解决 Exa 信用 / 装 SerpAPI，或接受召回缺口诚实标注 |
| Liu 2023 JLT 来源归因存疑 | §7.2 来源透明（INVARIANT 7）| 论文真实（seed+DOI）但子agent归因blit无法独立验证 | 阶段 2 精读 Liu 2023 时确认来源（若下到全文则归因不重要）|
| AO-DSP Paillier 系载波边界 | 不回头载波同步（红线）| 保留主表标边界警示 | 阶段 2 精读核验 DSP 残余是否纯载波域 |
| 多 DNN 孤证 | 孤证就是孤证（§7.2）| ANN/VAE/Kulmer/Qin 各单篇 | 阶段 2 补证是真孤证还是召回缺口 |
| 本对话 6 步超限 | 单对话 ≤3 步（AGENTS.md）| 用户显式"继续"指令优先 | 下次分对话（用户已知晓）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（INVARIANT 5/6/18/19）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] 验证 1：`landscape-equalization.md` 完整版 ~46 篇 + 8 子地带 + 4 死地（Read 文件文末总结段）
  - [ ] 验证 2：landscape 无判据 A 结论（grep "baseline 真失效"/"失效" 应只在纪律声明里）
  - [ ] 验证 3：信噪比合格终判 8 项 checkbox 全勾（文件末尾）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"（不回头载波同步 / 不预设子方向 / 不跳框架）
- [ ] **选地时不替用户判**（给候选摘要 + 事实，用户拍板）

## 下一轮

**阶段 1.5 选地（主控对话 + 用户）**：
1. 读必读 5 件
2. 给用户 8 子地带候选摘要（本 H002 §子地带候选摘要）
3. 用户拍板选 1-2 个均衡子地带
4. 进阶段 2 精读（Trans 必读 + Letters 扩写溯源 + M-C-A + §7.2 每批核查）

**不在阶段 1.5 做**：不精读（阶段 2）/ 不判 Go/Kill（阶段 4）/ 不下"有没有缝"结论（阶段 3）/ 不建代码（阶段 5 后）。
