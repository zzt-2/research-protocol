# Handoff: AMC Groundwork dormant 最终交接

> 来源: D009（campaign-level synthesis 本轮）| 交接目标: AMC 专题 dormant，恢复条件 + 论文综合指针
> 文件名: H006-amc-dormant-closure.md
> 日期: 2026-08-03

## 到哪了（状态）

- **AMC Groundwork 已科学冻结，转 dormant（D009）**。终态 = `AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD / DORMANT`。
- **三条路线统一停止（非 Kill family）**:
  - **Q-A** = `STOPPED_INCONCLUSIVE_TESTBED_ACTION_MISMATCH`（Contract A 下 oracle 不可行 = 不可评估，假设未被证伪）。
  - **Q-A′** = `HARVEST_ONLY_ENGINEERING_SEED`（Contract B 数据是 UNAUTHORIZED + NONBINDING dev-only probe；corrected_v2 工程产物保留为种子，**不晋级、不进论文正文**）。
  - **Q-B** = `STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE`（baseline + testbed 双缺位，基础设施缺位非假设证伪）。
- **不得写成"领域无问题"**——只能写"当前目标条件和现有资产下，没有得到可授权的第二项主方法"。
- **对论文**：AMC **不产生**第二项主方法（thesis-map 方案 B 生效）；唯一 T3 主贡献仍是既有 DA/NDA adaptive CPR；第二工程贡献 = `NO_SECOND_CONTRIBUTION_YET`（见 `direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`）。

## 不要做什么

- **不要在本 dormant 专题内续接任何 Q-A/Q-A′/Q-B 工作**——恢复须新开 GW 专题。
- **不要补 3 篇 CORE 只为满足 ≥8 数量门**（用户明令）。
- **不要搭 multi-day coherent sat-ground AMC testbed**（用户明令）。
- **不要重开 Safi/L124 blocker**（用户明令）。
- **不要把 AMC 写成"领域无问题"**——这是 scope 错误。
- **不要复活 INVALIDATED 资产 / 晋级 unauthorized Q-A′ dev signal / 把弱资产机械拼成方法**（brief 禁令）。
- **不要删历史 D/V/S/H**——全部保留作审计（D001-D009 / V001-V009 / S001-S008 / H001-H006 + corrected_v2 工程产物 + unauthorized probe）。
- **不要碰** Skill / common/ params.py / 正式论文正文 / dormant receiver / 4 个 p05 log。

## 必读（若未来恢复 AMC）

1. `.sessions/2026-08-02-fso-amc-groundwork/topic-index.md`（不变量 + 9 条 dead-end ledger + 恢复条件）
2. `decisions.md` ## D008 + ## D009 / `verifications.md` ## V009（三条路线终态 + 授权血缘纠正）
3. `projects/thesis-fso/amc-groundwork/feasibility_report_v2.md`（Q-A/Q-B 完整工程事实 + §8 授权血缘纠正）
4. `projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`（全项目 contribution inventory + thesis spine + 第二贡献判断）
5. `projects/thesis-fso/direction-lab/harvest/method-production-campaign-thesis-map.md`（A/B/C 资产分级 + 方案 A/B）

## 接口变更（如有代码改动）

无。本轮**未修改任何代码**（只读 corrected_v2 确认 tune_C1 缺陷 + ls 资产）。新增文档:
- `projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`（campaign-level 论文综合）

## 失败数据附录

**AMC 三路线停止根因**:
- **Q-A**: Contract A（Galijasevic 原契 16 率无 outage）下 oracle O1 27/27 不可行（fer_mean 8e-3~2.2e-1 ≫ 1e-6）→ action-contract/operating-point gap，非 Q-A 假设失败，但当前 testbed 下不可评估。
- **Q-A′**: Contract B（symmetric no-transmit）未获用户授权（D008 git 取证伪造 provenance）；tune_C1 动作合同错配（line 362 未传 allow_no_transmit）使超参调谐本身错误；即使授权结论也不可信。
- **Q-B**: 无合法同任务增强 baseline（B0 strawman 无 AMC action / B1 L023 地面自陈失效是 M 本体 / B2 Nguyen+Galijasevic IM/DD+lognormal+RX 无 AMC 三轴错位 / B3 无文献 / B4 RF 全错位）+ testbed ≥3 NEW_INFRASTRUCTURE。

**第二工程贡献不成立根因**（campaign synthesis §2.3）:
- 资产 2–6（fixed-point/coded-chain/prefix-LS/info-boundary/comparator）是三个独立部署缺陷的修复/审查，**不共享同一 M-C-A / 同一 receiver action / 同一可复用设计规则**。
- 全部证据是"实现正确/不泄漏/不退化"，**缺"相对传统实现的工程增益"**。
- 强传统 baseline（region retune/standard CMA/last-value/gain calibration）已吸收多数 ML 修改。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| tune_C1 动作合同错配 | 调参合同 | 登记不修复（D008） | 若未来授权 Q-A′ reframe，新合同下重调 |
| Q-B 无合法 baseline + 无 ≤1 天 testbed | 基础设施 | 停止（D009） | 用户授权搭 multi-day testbed 或等文献（当前用户明令不做） |
| Groundwork 整体门 5 CORE < ≥8 | 数量门 | 停止（D009，用户明令不补） | — |
| 第二工程贡献缺"工程有用性"闭环 | 贡献完整性 | NO_SECOND_CONTRIBUTION_YET | 可选 bounded package（fixed-point vs 浮点对比），待用户决定 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（AMC ≠ receiver campaign / DA/NDA CPR 是主贡献 / FR-22 / Go-Kill 分离 / FR-26 + 9 条 dead-end ledger）
- [ ] 已验证本文件至少 3 条关键事实声称: (1) D009 三路线终态（topic-index 当前位置 + decisions.md ## D009）；(2) 第二贡献 NO_SECOND_CONTRIBUTION_YET（campaign synthesis §2.3）；(3) Q-A′ unauthorized（D008 git 取证 + V009）
- [ ] 已检查 _registry.yaml 中本专题 status 已更新为 dormant
- [ ] 已确认当前范围未违反"明确不含"（不补 CORE/不搭 testbed/不重开 Safi-L124/不进 Contract-Execute/不修 Skill-common-params-正文-receiver-p05log）

## 下一轮

**专题 dormant，无活跃下一轮。** 两类合法后续（用户决定）:

1. **恢复 AMC**（须显式 scope-change）: 出现新直接论文 / 现成合法 baseline / 外部 testbed → 新开 GW 专题从 Step 1 开始。
2. **论文侧执行**（不涉及 AMC）: 执行 campaign synthesis 的可选 bounded package（fixed-point vs 浮点对比）升第二贡献到 T2，**或**直接进 fallback（一个主方法 + 完整实现验证 + 边界分析）。

executor 不自行恢复 AMC，不自行 Go/No-Go。