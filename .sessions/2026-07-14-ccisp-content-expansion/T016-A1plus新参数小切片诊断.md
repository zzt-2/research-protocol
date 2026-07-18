# Task Brief: A1+ 新参数复算与小切片方向诊断

> 来源: S001 / D016 | 产出位置: `.sessions/2026-07-14-ccisp-content-expansion/R014-A1plus新参数小切片诊断.md`
> 日期: 2026-07-15
> 唯一文档: 执行方先读本 T016，再按本文件列出的必读材料取事实

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol`。当前论文准备把五组无来源 Gamma--Gamma 参数重标定，并采用真实 branch-routed adaptive CPR receiver。

**你的任务**：先闭合 A1+ 上行参数的可复算证据链；只有复算门通过，才运行一个 old-vs-new 小切片，粗看新参数是否保留 DA/NDA 互补性、selector 方向和路线 B 的 bit-exact 等价。

**产出**：R014 诊断报告，以及必要的 probe script/JSON/verifier，均不得升级为投稿权威结果。

**最高纪律**：

1. 不看结果调参数；不改 CV、1.10 margin、13 dB、recovery、demod、resolve、seed 规则或 common-768 指标。
2. 不修改论文、图片、Skill、正式图数据和旧权威 JSON。
3. 本轮不修改正式 `params.py`。候选参数必须由有引用的公式在 probe 中确定性生成并完整写入 metadata，不能只硬编码最终 ((\alpha,\beta))。若 sim-preflight 判定这仍不合规，停在复算阶段并返回 PARTIAL，不得绕过参数真相源门禁。
4. 不把 3-seed probe 写成显著性、最终增益或投稿数字；不授权后续全量重跑。
5. NDA 的 `tx_bits` ambiguity resolution 必须标为 post-hoc evaluation；不得声称可部署。

## 1. 必读与治理

1. 完整读取根目录 `AGENTS.md`。
2. 使用 `session-governance`，续接 `.sessions/2026-07-14-ccisp-content-expansion`；读 `topic-index.md`、`decisions.md` D014--D016、`verifications.md` V010--V011、R008、R008b、R013、voice.md。
3. 使用 `sim-preflight`，按“场景 A 跑实验 + 参数变更重审”读取：
   - `.agents/skills/sim-preflight/scenarios/run.md`
   - `rules/constraints.md`
   - `rules/tech.md`
   - `rules/param-source.md`
   - `rules/mve-validation.md`
   - `rules/doc-discipline.md`
   - `rules/usage-log.md`
4. 按 AGENTS.md 的 TL-20/TL-21/TL-22/TL-23/TL-26/TL-31/TL-33，读取 `thesis-lessons.md` 对应条目；这是物理参数重标定，不得凭摘要或记忆。
5. 必读真相源：
   - `projects/simulation/params.py`
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py`
   - `_a4_branchrouted_30seed.py`
   - `_verify_b_vs_a_equiv.py` 与报告 JSON
   - `projects/simulation/common/` 中上述 caller 实际调用的 channel/recovery/modulation/experiment 依赖
   - `毕设/formulas-master.md` 中 Rytov、Gamma--Gamma 与 scintillation 条目
6. 文献事实必须回到本地全文：Al-Habash 2001、Ghassemlooy 2019、Osborn 2021、Kaushal & Kaddoum 2017。先从 `papers/index.json`/仓库检索 exact path；未读到全文的来源不得承担精确公式或数值。

## 2. 已冻结背景

### 2.1 目标架构

- 路线 B：`raw window → decide → only selected DA/NDA branch → selected complex output → demod/evaluation`。
- 旧参数下 verifier 已给出 990/990 selector bit-exact 与 selected_rx 20/20 抽查通过。
- A 双分支 runner 只作为离线评估 harness，负责 fixed DA/NDA、oracle 与 gain；不得描述为 B 在线执行的一部分。

### 2.2 参数方向

下行候选已冻结为 Family 1：

| regime | \(\sigma_R^2\) | 预期 \((\alpha,\beta)\) |
|---|---:|---:|
| downlink weak | 0.2 | 约 (11.6, 10.1) |
| downlink moderate | 1.6 | 约 (4.0, 1.9) |
| downlink strong | 3.5 | 约 (4.2, 1.4) |

最终值必须由公式重算并报告未四舍五入值，不能直接把本表当计算输入。

上行采用 A1+：以明确仰角/波长/HV5/7 等物理条件为输入，先复现 Osborn 的 plane-wave 环境锚点，再用 Kaushal 的 spherical-wave 上行积分和 Al-Habash spherical mapping 得到两档候选。A2/A3（为强于下行而取 3.5/6.0 或 4.0/6.0）已由 D016 排除。

## 3. Gate P0：证据与复算门

### 3.1 先做定义卡

逐项列出：公式、wave type、积分上下限、\(C_n^2(h)\) profile、波长、仰角、发射/接收高度、孔径/点接收假设、单位、来源 exact file:line/原论文页码与公式号。

必须明确：Osborn 表值究竟是 plane-wave/downlink 还是可直接用于 uplink；若不是，不能改称“上行实测值”。

### 3.2 复现检查

1. 用同一 HV5/7/几何输入数值积分 plane-wave 公式。
2. 复现 Osborn 30° 与 10° 的 \(\sigma_R^2\) 锚点。
3. 预注册容差：相对误差均不超过 **5%** 才通过 P0；需报告积分收敛性，不能放宽容差。
4. P0 通过后，才以同一环境输入计算 spherical-wave 上行 \(\sigma_R^2\)，再经 Al-Habash spherical 公式得到 uplink moderate/strong \((\alpha,\beta)\)。

若缺公式、HV 常数、路径边界或无法在 5% 内复现：停止所有 uplink probe。可继续下行三档并将总结果标 PARTIAL；不得猜输入、调常数贴表或改用 A2/A3。

### 3.3 参数 sanity

- \(\alpha>0,\beta>0\)，公式适用区与强区 caveat 明示。
- 对每组计算 GG mean、variance/scintillation index，检查严重度排序；不得只用“参数更小”作排序依据。
- 区分 plane/spherical mapping；不得混用一套常数。

## 4. Gate P1：诊断小切片

P0 通过后才执行。若只通过下行，则只跑下行并标 PARTIAL。

### 4.1 冻结设计

- 参数集：`old` 五档与 `new_A1plus` 五档。
- SNR：`[5, 13, 17, 19, 25]` dB。
- seeds：`[0, 1, 2]`。
- 每 seed 每点：400 windows，沿用现有 256-symbol/window 与 common-768 mask。
- A evaluator：old/new 全五档，输出 fixed DA、fixed NDA、selected、oracle、branch counts 与 metric signature。
- B receiver：只对 new_A1plus 的三个下行档运行；输出 selected errors、branch counts、selected_rx 审计摘要，并与同 case/seed 的 A selected 端整数逐项比较。
- 同一参数集内 A/B 必须共享确定性 realization identity；不得各自独立随机生成信道。

若 probe 不能使用 `generate_shared_realization()`、`save_results()` 或完整 provenance，自行停止，不得生成结论 JSON。

### 4.2 必须保持冻结

- `decide()` 逻辑、CV threshold、blind-power proxy、1.10 margin、13 dB；
- DA/NDA equalization、recovery、demod、`resolve_m16apsk_blockwise`；
- seed/window 公式、common-768 error population 与 denominator；
- 所有 calibration coefficients。

禁止看到新参数结果后重标 threshold 或换 SNR 点。若怀疑 calibration 失配，只登记为下一轮候选，不在本任务修。

### 4.3 预注册假设

- H1：更换参数会改变旧 headline，方向和幅度未知；不得预设新参数仍给出 3.1 dB。
- H2：只要数据依赖未变，B selected errors/branch counts 应与 A 在全部 `3 scenes × 5 SNR × 3 seeds = 45` 个新下行 case-seed 上严格整数相等；目标 45/45。
- H3：新参数可能使 selector 退化。必须报告两个分支是否都在完整小网格中被选择、fixed winner 是否随场景/SNR 发生变化、selected-vs-fixed-NDA 的符号分布。

### 4.4 诊断触发器（不自动调参）

以下任一发生，将“直接进入全量重跑”标 BLOCKED，交回用户拍板：

1. B/A 不是 45/45 bit-exact；
2. 三个下行档 × 五个 SNR 的全部窗口中，单一分支选择比例在每个 cell 都 ≥99%，adaptive routing 实质退化；
3. fixed DA/NDA 的胜者在全部 15 个下行 cell 中完全不变，缺少分支互补证据；
4. selected-vs-fixed-NDA pooled gain 在至少 8/15 个 cell 非正；该阈值只作为粗筛，不是论文 PASS 标准；
5. 新参数导致相对旧参数的核心方向反转，或任何 NaN/负参数/metric-signature 漂移；
6. uplink 参数 P0 未过却仍产生 uplink BER。

未触发也只判“值得设计正式重跑合同”，不得自动进入 30-seed。

## 5. 实现边界与允许产物

允许新增，名称可微调但职责不可混：

- `projects/simulation/explore/nda-awgn-tracking-sandbox/_a1plus_newparams_probe.py`
- `_a1plus_newparams_probe.json`
- `_verify_a1plus_newparams_probe.py`
- `_verify_a1plus_newparams_probe_report.json`
- `.sessions/2026-07-14-ccisp-content-expansion/R014-A1plus新参数小切片诊断.md`

禁止修改：

- `params.py`、`common/`、原 A/B runner、原 JSON；
- `paper/ccisp2026/`、`figures/`、Skill；
- `CONCLUSIONS.md` 和正式结果目录。

候选参数必须在 probe 中由已核验公式与物理输入确定性生成；JSON metadata 保存公式版本、输入、文献指针、未四舍五入输出、script/dependency hashes，并标：

`authority_status = diagnostic_probe_not_for_paper`

如果无法在不违反 params.py 单一真相源纪律的前提下实现该 probe，停在 P0 并把合规实现方案写入 R014，不要擅自修改正式参数源。

## 6. R014 强制结构

使用 research note 锚点，并包含：

1. P0 定义卡与 exact evidence pointers
2. Osborn plane-wave 复现表、相对误差和积分收敛证据
3. A1+ 五档候选表：物理输入、\(\sigma_R^2\)、未舍入/展示 \((\alpha,\beta)\)、GG scintillation index、适用边界
4. old-vs-new 诊断矩阵：fixed DA/NDA、selected、oracle、branch counts；不得只报最有利点
5. B-vs-A 45/45 等价核查
6. 六个诊断触发器逐项 PASS/BLOCKED
7. 实现真相三联卡：information_access / metric_signature / state_lifecycle
8. “保留什么、失效什么、下一轮若全量重跑需哪些 runner”的清单
9. 总判定：`GO_TO_FULL_CONTRACT / PARTIAL / BLOCKED`；不得写“论文已验证”

## 7. 验收

- [ ] P0 在任何 BER 运行前完成，引用原文具体公式/数值而非只写文献名
- [ ] plane-wave 两锚点均在预注册 5% 容差内，或明确停止 uplink
- [ ] 参数由公式生成，无结果反向选参、无 A2/A3 回流
- [ ] old/new 使用相同 probe 协议，A/B realization identity 可核验
- [ ] B/A 新下行小网格 45/45 或如实 BLOCKED
- [ ] 3 seeds 未被写成显著性或最终结果
- [ ] 未修改禁止文件，未更新论文数字
- [ ] 独立 verifier 从原始 JSON 重算关键结论
- [ ] 按 sim-preflight 写当月 usage log；失败/中断也写

## 附：返回主线程时只需说

1. P0 是否闭合；五档候选值是什么；
2. 六个诊断触发器哪些命中；
3. 是否值得进入正式全量重跑合同；
4. R014 与 probe/verifier 的 exact paths。
