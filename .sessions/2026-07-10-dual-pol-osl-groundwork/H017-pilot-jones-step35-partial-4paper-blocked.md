# Handoff: 战略切换 Pilot-Jones formal GW 线；Step 3.5 PARTIAL（backward PASS，4 篇全文 BLOCKED）

> 来源: S074（续接）| 交接目标: 用户裁决 4 篇全文获取路径，再决定 Step 3.5 是否闭合 / 进 Step 4a
> 日期: 2026-07-22
> 文件名: H017-pilot-jones-step35-partial-4paper-blocked.md

## 到哪了（状态）

用户战略裁决（D061）：**P03 routing 选项①**——P03 暂停回候选池（不 Kill，family 不关闭，沿用 D057/D058 `P03_DOMAIN_ADEQUACY_UNRESOLVED`）；**Pilot-Jones = thesis-fso 当前 formal Groundwork 工作线**。current formal GW step = **Pilot-Jones Step 3.5 IN_PROGRESS**。

**Step 3.5 终验结果**：
- **backward-chain 独立终验 V035 = PASS**：JLT 2022 `10.1109/JLT.2022.3224805` Crossref refs=21 / screened_relevant=7 / new=0（7 篇全已知，含 OE 2021 = 直接前作）；forward 25 citers ∩ backward 21 refs = ∅（语义正确）；provenance 真实。**gw-supplement 判据 #3（双向引用链已分析）闭合**。这是 V029 标 UNAVAILABLE 后缺失的终审。
- **4 篇直接竞品全文获取 = BLOCKED**（D056: TCOMM `10.1109/TCOMM.2024.3522036` / JLT2025 `10.1109/JLT.2025.3640695` / JLT2022 `10.1109/JLT.2022.3224805` / JLT2023 `10.1109/JLT.2023.3284489`）：`tools/download --doi` 四篇均 `all_failed`（non-OA IEEE paywalled）；OA scout 子 agent 验证 Semantic Scholar/Unpaywall/OpenAlex/arXiv 四源均 closed（无 arXiv 预印本、无 green-OA）。
- **已全文精读**：OE 2021（L08）+ LCOMM 2026（S069）两篇。
- **Step 3.5 最终裁决 = PARTIAL/BLOCKED**：backward PASS + 收敛 PASS，但 D056 全文门 BLOCKED。**不进 Step 4a**（FR-22 + D056）。

**纠正 170c00c 审计错误**：上一轮（science-scout SCIENCE_FREEZE）的 H015/S014/D022 误写"LCOMM 2026/JLT2022-23 仅 abstract"——实际 LCOMM 2026（S069）+ OE 2021 均已全文精读；真正缺全文的是 TCOMM2024/JLT2025/JLT2022/JLT2023 四篇。master-state:96 "待V030" stale（V030 属 P03 非 Pilot-Jones）已纠正。这是 TL-33"自欺式核查/把联想当证据"的实例——未查 read-log 就写 abstract-only。

## 下一步干什么

**第一件事：用户裁决 4 篇全文获取路径**（4 选 1）：
- (a) **机构 VPN/proxy 获取 IEEE 全文**后精读（最完整，推荐）；获取后走 gw-read 结构化提取（M-C-A + 8 问）。
- (b) **邮件联系通讯作者**（Shuai Liu / Yiyang Feng / Linsheng Fan×2）求全文。
- (c) **带债豁免**：以 2 篇全文（OE 2021 + LCOMM 2026）+ V035 backward 证据（7 篇已知 backward refs）+ 4 篇摘要级证据"带债推进"Step 4a（需用户显式豁免 D056 全文门，并把 4 篇未精读列为阻断性债务）。
- (d) **等 OA / 换近似竞品**。

若选 (a)/(b) 且获取全文 → 子 agent 按 gw-read.md 精读（含 7 子表 + 问题提取 M-C-A + 实验完备性），主线接收结构化摘要，更新 literature_notes，再判 Step 3.5 是否 PASS → Step 4a。

## 纪律（和下一步直接相关）

- **不用 abstract 冒充全文过 Step 3.5**（gw-read.md 浅读不计入精读门槛 + 用户提示 §五 + TL-33）。4 篇 BLOCKED 必须显式记录。
- **不强行进 Step 4a**（FR-22 + D056）；Step 3.5 PARTIAL。
- **Q2 裁决门**（D055/D056）：若只是 OSL 场景替换或 EMA=.9 参数差异 → Kill；若存在既有方法未处理的结构性 GG/低 pilot 病态且需改变算法结构 → 允许 Step 4a。**4 篇全文未读无法判定**——这是 PARTIAL 的根因。
- 不复活 science-scout campaign（D022 dormant）；本轮工作在 formal GW 链（dual-pol-osl-groundwork 专题），不在 dormant 专题写新 S/D/V/H。
- 不跑仿真/MVE；不进 Step 4a A0/A/B/D；不创建 F2 Scout；不重做第四轮关键词泛搜。
- protected 文件（STATUS.v1.md / project.v1.yaml / canonical-state）不改。
- EMA09 15/15 + clean 0/9 是 family-promotion 到 GW Step 1，**非 Go**。

## Q2 当前 M-C-A（基于已读全文 OE 2021 + LCOMM 2026 + V035 backward 证据）

- **M**：传统 block/frame pilot Jones inversion（短 pilot LS 估计 2×2 Jones + inverse derotation）。OE 2021（3 pilot tones 逐 block RSOP 矩阵+inverse）+ LCOMM 2026（FPT→4路→Jones补偿）均属此族。
- **C**：dual-pol OSL 的 GG 湍流 + 高速 SOP + ≤10% pilot 预算。已读全文均**非 OSL 场景**（OE 2021 光纤短距 SCM；LCOMM 2026 光纤 DP-16QAM）。OE 2021 自述短 block 噪声 penalty + 长 block 动态失配 + 矩阵退化/定点溢出风险。
- **A**：fixed-label 恢复不稳定（短 pilot 估计抖动/病态）。
- **关键不确定性**：是否 OSL GG 深衰落引入 OE 2021/LCOMM 2026 未处理的结构性新失效（改变算法结构），还是仅场景替换/EMA 参数差异（→ Kill）。**4 篇全文未读无法判定**。

## 失败数据附录（无新科学实验；acquisition BLOCK 数据）

- `tools/download --doi 10.1109/TCOMM.2024.3522036` → all_failed
- `tools/download --doi 10.1109/JLT.2025.3640695` → all_failed
- `tools/download --doi 10.1109/JLT.2022.3224805` → all_failed
- `tools/download --doi 10.1109/JLT.2023.3284489` → all_failed
- OA scout（S2/Unpaywall/OpenAlex/arXiv）：4 篇均 `is_oa:false` / `openAccessPdf=""` / arXiv 0 命中
- backward-chain V035：Crossref refs=21, screened=7, new=0, all-known（PASS）

## 已知债务（原则与现实差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 4 篇直接竞品全文无法获取 | D056 要求 Step4a 前精读直接竞品 | BLOCKED_NO_FULLTEXT（non-OA IEEE）| 用户裁决获取路径（VPN/邮件/豁免/OA）|
| Step 3.5 PARTIAL 非 PASS | gw-supplement 收敛门 + D056 全文门 | backward PASS + 收敛 PASS，但全文门 BLOCKED | 4 篇全文精读完成或用户显式豁免 |
| 170c00c 审计错误（LCOMM/JLT abstract-only 误判）| TL-33 证据链强制 | 已在 S074 续接段 + literature_notes + D061 纠正 | — |

## 用户/advisor voice（关键指令，verbatim）

- "选择 master-state.md §2 的 P03 routing 选项①：暂停 P03，返回候选池；不关闭 P03 family。激活 Pilot-Jones 为 thesis-fso 当前 formal Groundwork 工作线。" → D061
- "LCOMM 2026 不是 abstract-only。S069、S071 已证明 LCOMM 2026 全文精读完成。"
- "JLT 2022 backward chain 不是尚未获取：S074 已记录 Crossref references=21、相关筛选=7、new=0。当前缺的是对该现成补链的独立终验，不是重新抓取。"
- "真正尚缺全文闭合的四篇应核为：TCOMM 2025；JLT 2026；JLT 2022；JLT 2023。"
- "全文确实不可获得时，明确记 BLOCKED；不得用 abstract 冒充全文，也不得强行通过 Step 3.5。"

（完整原话见 voice.md 2026-07-22。）

## 必读（不超过 8 个）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（不变量 + 当前位置 S074续接/D061/V035）
2. 本文件 `H017-pilot-jones-step35-partial-4paper-blocked.md`
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` 的 D061 + D055/D056
4. `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md` 的 V035 + V028/V029
5. `.sessions/2026-07-10-dual-pol-osl-groundwork/S074-pilot-jones-step35-r2-r3-correction.md`（含 2026-07-22 续接段：审计纠正 + acquisition BLOCK + Q2 M-C-A）
6. `projects/thesis-fso/master-state.md:23-32`（§2 控制面切换）+ `:95-101`（方法层重开轨表 Pilot-Jones 行）
7. `projects/thesis-fso/literature_notes.md`（L06-L10 直接竞品表 + Q2 M-C-A）
8. `stages/gw-supplement.md`（Step 3.5 判据）+ `stages/gw-read.md`（精读提取要求）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落。
- [ ] 已验证至少 3 条关键事实：
  - V035 backward-chain PASS → 读 `verifications.md` V035（Crossref refs=21/screened=7/new=0）；
  - 4 篇 BLOCKED → 读 S074 续接段 acquisition BLOCK + literature_notes L06/L07/L09/L10 `BLOCKED_NO_FULLTEXT`；
  - LCOMM 2026 已全文精读（非 abstract）→ 读 S069 + S071 第1篇。
- [ ] 已检查 `_registry.yaml` 的 depends_on（dual-pol-osl-groundwork 被 science-scout depends_on）。
- [ ] 已确认当前范围不含：仿真/MVE、Step 4a、F2 Scout、第四轮泛搜、protected 修改、dormant science-scout 新 S/D/V/H、push。

## git 状态

- worktree: `D:/code/study/research-protocol/.worktrees/direction-lab-capability-atlas`
- branch: `codex/direction-lab-capability-atlas`
- 本轮 consolidated commit 待提交（不 push）。接收时以 `git log -1` 核验实际 SHA。

## 下一轮

用户裁决 4 篇全文获取路径（VPN/邮件/豁免/OA）。若获取全文 → 子 agent gw-read 精读 4 篇 → 更新 literature_notes → 判 Step 3.5 PASS → Step 4a（Q2 的 M-C-A 是否结构性新失效 vs 场景替换 Kill）。
