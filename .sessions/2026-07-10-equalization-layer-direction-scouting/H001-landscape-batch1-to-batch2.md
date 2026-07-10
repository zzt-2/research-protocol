# Handoff: 阶段 1 地勘前置第 1 批完成 → 第 2 批（组 4-6）

> 来源: S004 | 交接目标: 阶段 1 地勘前置第 2 批对话（跑组 4-6 + 补检索 + 信噪比终判 → 阶段 1 收尾）
> 文件名: H001-landscape-batch1-to-batch2.md
> 日期: 2026-07-10

## 已完成边界

阶段 1 地勘前置**第 1 批（组 1-3）**执行完成：
- 3 个子 agent 并发跑组 1（equalization 总览）/ 组 2（偏振）/ 组 3（MIMO-combining）
- 产出 `projects/simulation/landscape-equalization.md` **初版**：29 篇主表 + 7 子地带分类 + 3 个 🔴死地 + seed.md 交叉核 + 档级标注
- 信噪比合格判据 7 项全过（子地带 ≥3 / 候选够 / 档级全 / 死地有理由 / 无载波同步混入 / 覆盖度诚实 / **无判据 A 结论**）
- §7.2 自检：未编造，孤证已标，立场未扭曲

**做到哪一步**：第 1 批产出落盘，**阶段 1 未收尾**（组 4-6 未跑）。

## 不要做什么

1. **不要用 abstract 判判据 A（baseline 真失效）**（INVARIANT 6，S010 最值钱教训）。abstract 只找候选清单，缝潜力只标 🟢/🟡/🔴 粗判。判缝移全文层（阶段 2/3）。
2. **不要偏回载波同步**（本专题红线）。检索词不加 `synchronization`；混入的载波/定时同步论文标排除。
3. **不要锁子方向**（INVARIANT 5 方法中性）。检索词不加具体方法名（CMA/RDA/MRC 等）。
4. **不要从 seed.md 挑论文精读**（seed 56% unknown 质量参差）。seed 只当参考地图，新检索为主。
5. **不要重复撞 OAM-MIMO 死地**（🔴 12 年饱和，Wang 2021 综述已收口）。
6. **不要单对话超 3 步**（AGENTS.md）。第 2 批 = 跑组 4-6 + 补检索 + 信噪比终判，若超 3 步分对话。
7. **不要急判方向**（profile durable）。地勘阶段只产清单，不排优先级不判 Go/Kill。

## 必读（下一对话开始时按优先级读）

1. `.sessions/2026-07-10-equalization-layer-direction-scouting/topic-index.md` —— 20 不变量（INVARIANT 5/6/7/18/19 重点）
2. `projects/simulation/landscape-equalization.md` —— **本批产出，第 2 批要往里追加组 4-6 结果**
3. `.sessions/2026-07-10-equalization-layer-direction-scouting/S004-landscape-preflight-batch1.md` —— 本批执行细节 + 源状况 + 信噪比自检
4. `PROMPT-001-landscape-preflight.md` —— 任务书（检索策略 / 红线 / 陷阱 / 验收），第 2 批沿用其纪律
5. `search-archive/_index/by-topic/equalization-seed.md` —— 参考地图（只读 16 篇 Trans/Letters 骨架 + 死地标记，不当种子）

## 关键事实（接收方需知道的状态）

### 源状况变化（影响第 2 批召回策略）
- **Exa 信用额度耗尽**（NO_MORE_CREDITS）→ 第 2 批失去语义搜索，关键词质量更关键，或先解决 Exa/SerpAPI
- **IEEE blit 3 次均 0 命中**（会话用量 1/50）→ venue 靠 OpenAlex/S2，可能漏 IEEE 独有论文
- S2 + OpenAlex 正常工作

### ISI 均衡子地带是第 2 批重点追
- 本批仅孤证 Zhang 2018（Opt Eng）
- seed.md 标 11 篇含 **TCOMM 2026 "ISI in IRS-Assisted FSO"**（Trans），本批未召回
- 两表对不上 → 组 4 专门查 ISI（`intersymbol interference` / `dispersion compensation` / `DFE` / `FDE`）重点补

### 第 2 批要跑的组（PROMPT-001 §2.2）
- 组 4：`("FSO" OR "free space optical") AND ("intersymbol interference" OR "ISI" OR "dispersion compensation") AND coherent`
- 组 5：`("FSO" OR "free space optical") AND ("adaptive optics" OR "AO" OR "wavefront correction" OR "phase compensation") AND (DSP OR "digital signal processing")`
- 组 6：`("FSO" OR "free space optical") AND ("turbulence compensation" OR "atmospheric turbulence mitigation") AND coherent`

### 子地带活跃度初判（abstract 层，**不判 baseline 真失效**）
- 🟢 MDCC（multi-aperture coherent combining）最活跃：Geisler 2016 奠基 → Liu/Ju 2023-2024 DSP 进阶 → Johst 2024 + Chen 2026
- 🟢 偏振均衡升温（DP 自相干+湍流偏振混叠切口）：Cvijetic 2010 奠基 → ANN 2026 / VAE 2026
- 🟢 DNN/NN 均衡新兴（多孤证）
- 🔴 OAM-MIMO 饱和（12 年 + 综述收口）
- 🟡 ISI / OFDM-FSO / AO-DSP 待组 4-6 补

## 接口变更（代码改动）

无（地勘不写代码，只产 .md）

## 已知债务（原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Exa 信用耗尽 | 多源召回（INVARIANT 5 地勘全覆盖）| 本批靠 S2+OpenAlex 裸跑 | 第 2 批前解决 Exa 信用 / 装 SerpAPI，或接受召回缺口诚实标注 |
| IEEE blit 0 命中 | venue 字段准确（INVARIANT 19 档级标注）| 靠 OpenAlex/S2 container_title | 换 blit 关键词重试 / 接受 venue 待精读确认 |
| ISI 子地带孤证 | 子地带覆盖充分（信噪比合格判据）| 本批仅 1 篇，TCOMM 2026 未召回 | 组 4 专门查 ISI 补 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（重点 INVARIANT 5/6/7/18/19）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] 验证 1：`projects/simulation/landscape-equalization.md` 存在且 29 篇主表 + 7 子地带（Read 文件确认）
  - [ ] 验证 2：landscape 无判据 A 结论（grep "baseline 真失效" / "失效" 应只在纪律声明里，不在子地带结论里）
  - [ ] 验证 3：OAM-MIMO 标 🔴 死地（交叉核 seed 一致）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（problem-driven-redirection / step4a-mve-execution / b3-joint-estimation / framework-evolution）
- [ ] 已确认当前范围未违反"明确不含"（不回头载波同步 / 不预设子方向 / 不跳框架）
- [ ] **§7.2 主线核查**：随机抽 landscape 主表 3 篇，grep 子 agent 原始搜索结果 JSON，核查 abstract 提取真实性（守 INVARIANT 7，本批自检建议）

## 下一轮

**阶段 1 第 2 批（新对话）**：
1. 开工先读必读 5 件（topic-index / landscape / S004 / PROMPT-001 / seed）
2. 做 §7.2 主线核查（抽 3 篇 grep 核查，~5 分钟）
3. 跑组 4-6（ISI 深 / AO-DSP / 湍流补偿），ISI 是重点追
4. 结果追加到 `landscape-equalization.md`（不另建文件）
5. 新检索 vs seed 终极交叉核
6. 信噪比合格终判（子地带覆盖是否仍 ≥3 + ISI 是否补全 + 死地是否确认）
7. 阶段 1 收尾 → 交主控对话 + 用户拍板进阶段 1.5 选地

**不在第 2 批做**：不精读（阶段 2）/ 不判 Go/Kill（阶段 4）/ 不下"有没有缝"结论（阶段 3）/ 不建代码（阶段 5 后）。

**第 2 批产出**：landscape-equalization.md 完整版 + S005 session note + H002（若有未完）或直接进阶段 1.5。
