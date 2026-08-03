# Journal Extension Readiness Assessment

> **SUPERSEDED / PAUSED — D025→D026 (2026-08-03)：旧评估保留作证据；当前唯一条件式 spine 与 Ch4/Ch5 方法状态见 D026。**

> 2026-08-03 | 关联: conference-to-thesis-map.md、bounded-package-recommendation.md
> venue = **N/A**（brief 指定：不查询/假设具体期刊要求）
> 本文件评估 brief Phase C 的四种包装（A 学位论文 / B journal extension / C engineering note / D 边界论文），给出各包可行性 + **唯一推荐**。

---

## 包装评估总表

每包按 brief Phase C 字段评估：一句话题目 / 中心问题 / contribution / 已有资产 / 关键数字 / 缺口 / 最小补实验 / 可发表形态 / 最大风险 / tier。

### Package A — CCISP → 学位论文扩展（唯一推荐）

| 字段 | 内容 |
|---|---|
| 一句话题目 | Turbulent satellite–ground FSO adaptive carrier phase recovery: method, robustness boundaries, and implementation verification |
| 中心问题 | 会议 adaptive CPR 方法在 SNR 失配/连续 GG/工作区变化下是否稳定？部署实现（branch-compute/定点/coded）是否保持选择与性能？ |
| contribution | (1) 主方法 adaptive CPR（Ch3，来自会议）(2) 鲁棒性边界研究（Ch4）(3) 部署实现验证（Ch5，限定实现可行性） |
| 已有资产 | A01 主方法 + A02–A06 鲁棒性/边界 + A07–A09 实现 |
| 关键数字 | 9 dB 0.8–1.5 dB；P01 0.32–0.70 dB 损害 + adapter 恢复 4/5；P04 +0.146 dB；P03 Q(8,6) 0/132000 identity；branch-routing 990/990 |
| 缺口 | 统一鲁棒性表（小验证）；branch-compute formal timing；float-vs-Q BER；coded freeze rerun |
| 最小补实验 | 见 `bounded-package-recommendation.md` 唯一小包（统一鲁棒性表优先） |
| 可发表形态 | 硕士学位论文（Ch1–Ch6） |
| 最大风险 | Ch4/Ch5 的 contribution ceiling 限定（非新算法、非 FPGA 资源）；但学位论文要求低于期刊，风险可控 |
| **tier** | **T_A（推荐）** |

### Package B — CCISP → journal extension

| 字段 | 内容 |
|---|---|
| 一句话题目 | （若可行）Received-power-aware adaptive CPR for turbulent FSO downlinks: robustness and implementation verification |
| 中心问题 | 会议内容加什么才构成"实质扩展"而非"会议稿加长"？ |
| contribution | 候选：新问题（SNR 失配/连续 GG）+ 新实现（branch-routing/定点/coded）+ 新分析（边界） |
| 已有资产 | 同 Package A |
| 关键数字 | 同上 |
| **缺口（实质扩展判据）** | **关键**：journal extension 需"实质扩展"（新问题/新维度/新实现/新理论/新图表）。逐项核：|
| | • 新问题？P01/P04 是边界/适用性，不是新方法问题（`NO_DIAGNOSTIC`/`ABSENT_ON_CONTINUOUS_GG`）|
| | • 新实验维度？SNR 失配 + 连续 GG = 边界研究，不是新机制 |
| | • 新实现？branch-routing/定点/coded = 实现验证，claim ceiling 限定（非 FPGA 资源、coded 无 freeze）|
| | • 新理论/分析？无（campaign `NO_SECOND_CONTRIBUTION`，D058 饱和）|
| | • 新图表？统一鲁棒性表 + branch-compute 图（小验证可补）|
| | • 会议内容重复比例风险：Ch3 = 会议稿几乎全文复用，重复比例高（典型期刊要求 <30–40%）|
| 最小补实验 | 同 Package A + 必须显著降低 Ch3 重复比例（需新机制或新理论，当前无） |
| **可发表形态判断** | **当前不足以投稿**。原因：(1) 无新机制/新理论（campaign 已饱和）；(2) Ch3 与会议稿重复比例过高；(3) Ch5 实现 claim ceiling 受限（无 FPGA、coded PARTIAL）|
| 最大风险 | 期刊拒稿（"增量不足/与会议稿重复过高"）；被迫夸大 claim（违反 ceiling）|
| **tier** | **T_B（不推荐现在投）** |

### Package C — 低复杂度 branch-routed engineering note

| 字段 | 内容 |
|---|---|
| 一句话题目 | Branch-routed execution for adaptive CPR: select-before-execute complexity reduction |
| 中心问题 | branch-routing 能否省 branch-compute？定点是否保持？ |
| contribution | branch-routing 990/990 bit-exact + Q(8,6) identity |
| 已有资产 | A07 (P03) + A08 (branch-routing) |
| 关键数字 | 990/990；Q(8,6) 0/132000；74.6%（单条件 weak@5dB，**不可写**）|
| 缺口 | full-grid formal branch-compute timing（warm-up/重复/多条件）；float-vs-Q BER；end-to-end 复杂度 |
| 最小补实验 | full-grid formal timing + float-vs-Q BER（2 项 SMALL_VALIDATION）|
| 可发表形态判断 | **当前不足以独立成稿**。原因：(1) 74.6% 单条件不可写，full-grid 需新跑；(2) 无 FPGA LUT/DSP/功耗数据（`resource_proxy_note` 明示）；(3) engineering note 需实测复杂度/吞吐，当前仅 wall-clock proxy |
| 最大风险 | 复杂度声称无硬件证据；74.6% 外推违规 |
| **tier** | **T_C（不推荐独立成稿，归入 Package A Ch5）** |

### Package D — 传统 baseline / negative-results 边界论文

| 字段 | 内容 |
|---|---|
| 一句话题目 | Robustness and applicability boundaries of received-power-aware adaptive CPR |
| 中心问题 | selector 的适用边界在哪？（P01–P07-R 负面池） |
| contribution | 统一 benchmark protocol + 边界刻画 |
| 已有资产 | A02–A06（P01/P02/P04/P11 + P05–P07-R 合并）|
| 关键数字 | P01 0.32–0.70；P02 +0.454；P04 +0.146；P11 20dB partial |
| 缺口 | 统一 benchmark protocol 需形式化；负面池多为 LOCAL_SLICE（非 campaign-generalizable）|
| 可发表形态判断 | **边界论文可学术成立但当前资产不足独立成稿**。原因：(1) 负面多为 LOCAL_SLICE，不足以支撑统一 benchmark；(2) 边界论文需"为什么这些边界通用"的理论，当前无；(3) 更适合作学位论文 Ch4 而非独立论文 |
| 最大风险 | "一堆 negative 堆砌"无统一问题（brief Phase B §7 已警示）|
| **tier** | **T_D（不推荐独立成稿，归入 Package A Ch4）** |

---

## 唯一推荐

**Package A（CCISP → 学位论文扩展）= 唯一推荐**。

理由：
1. **资产匹配**：A01 主方法（T3）+ A02–A06 鲁棒性（T1）+ A07–A09 实现（T1）天然填满 Ch3/Ch4/Ch5。
2. **claim ceiling 对齐**：学位论文接受"主方法 + 鲁棒性深化 + 实现验证"，不要求新算法/新理论；Ch4/Ch5 的边界/实现 ceiling 在学位论文中合规。
3. **避免过度包装**：B/C/D 独立成稿都缺关键证据（新机制/硬件复杂度/统一理论），强行成稿会违反 claim ceiling。
4. **与用户 profile 一致**："倾向务实可毕业"（D005）+ "不要重新找第二方法"（brief）+ "复杂流程先完整蓝图再分阶段"（profile）。

**Package B（journal extension）状态**：venue=N/A，**当前不足以投稿**。若未来用户授权跑 AMC（新 GW）产出第二机制，或补齐 Ch5 硬件复杂度 + coded freeze，可重新评估。**本轮不投、不预设 venue**。

**唯一小包**：见 `bounded-package-recommendation.md`（统一鲁棒性表优先）。
