# Campaign-level Thesis Contribution Synthesis

> 2026-08-03 | 权威状态：D058/V084（receiver campaign closeout）+ D008/V009（AMC freeze）
> 性质：campaign-level thesis spine 综合判断。本文件**不升级任何资产的科学有效性**，只做证据-backed 的论文落位判断。
> 证据规则：每条 claim 必须有路径；INVALIDATED/UNAUTHORIZED 资产不得晋级；不得把弱资产机械拼成一个方法。

## 0. 本综合的输入与边界

- **输入**：`method-production-campaign-thesis-map.md`（D058/V084）、`harvest/current.yaml`、`state/current.yaml`、AMC `feasibility_report_v2.md`（D008/V009）、AMC `topic-index.md`、CCISP 工程（`projects/simulation/paper/ccisp2026/`）、独立 verifier 取证（git 取证 + tune_C1 行号 + 资产 ls）。
- **不做**：不跑新方法仿真，不重开 Q-A/Q-A′/Q-B，不修改 Skill，不写正式论文正文，不复活 INVALIDATED 资产。
- **唯一推荐原则**：不堆选项，输出一个 thesis spine；工程贡献只当所有部分围绕同一 M-C-A + 同一 receiver action + 同一验证链时才合成 THESIS_ENGINEERING_COMPONENT。

---

## 1. Phase B — 全项目 contribution inventory（证据-backed）

> tier 定义（R010 §6 + 本综合）：T3 = THESIS_MAIN_METHOD（独立方法贡献）；T2 = THESIS_ENGINEERING_COMPONENT（围绕同一工程问题的可复用设计规则/系统组件）；T1 = SUPPORTING_MATERIAL（实现纪律/边界/工具）；T0 = INVALIDATED / DO_NOT_USE。

| # | 资产 | tier | 真实 action | 信息源 | 与传统 baseline 的差异 | 有效数字 | claim ceiling | 可放哪章 | 缺什么证据 | 独立贡献? |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DA/NDA adaptive CPR（per-window CV gate + 固定 13 dB effective-SNR 决策） | **T3** | per-block SNR 驱动的 DA/NDA 估计器切换 | CCISP `abstract.tex`；`_recovery.py:153/213,232-233`；`_a4_switch_30seed_fixed.py` | 26/29 工作点选对估计器；强湍流 net gain 约 1.2–1.9 dB（naive，扣 pilot overhead 后） | 26/29；约 1.2–1.9 dB naive（强湍流/上行）；弱湍流归零（+0.09/+0.18/+0.19，CI 跨 0）—— 不利数字不进正文（领域惯例 R016 §4.1） | **既有主贡献**；非本 campaign 新产出 | Ch4 主贡献 | ⚠️ headline gain 仅在 abstract.tex 正文；results JSON 无 `gain`/`fair_gain` 字段（机器不可查）—— 转学位论文前需补可复现数字溯源 | **是（唯一 T3）** |
| 2 | fixed-point / bit-true Q-format 实现 | **T1** | 饱和二补码 Q(W,F) + 块浮点归一化的 selector | `nda-awgn-tracking-sandbox/_p03_fixed_point.py`；`results/p03_fixed_point_codesign/phaseA_uniform.json` | uniform Q(8,6) 已到性能地板；mixed-precision 最多 +0.0166 dB | uniform Q(8,6) floor；mixed ≤ +0.0166 dB | **不得声称真实 FPGA 资源/功耗/吞吐**（无 HDL 综合） | Ch5 定点实现/附录 | HDL 综合、时序、板级证据 | 否（实现纪律，非算法创新） |
| 3 | corrected coded-chain（5G NR BG2 LDPC + 3GPP bit interleaver + Gray-16QAM BICM + 轨迹级 FER） | **T1** | 标准 3GPP 编码链实现 + 轨迹统计 | `nda-awgn-tracking-sandbox/p08_coded_chain.py` / `p08r_chain.py` / `p08r2_chain.py`；`results/p08r2_receiver_info_repair/` | 复用 verbatim 3GPP interleaver；非新编码方案 | PARTIAL（chronology 修复后未独立 pre-test freeze 确认重跑） | **不得引用 P08/P08-R 旧科学结论**（chronology 仅 PARTIAL） | Ch5 接收链/FEC 或附录 | 独立 pre-test freeze 后确认性重跑 | 否（标准组件实现，非性能方法） |
| 4 | receiver-visible prefix-LS calibration（32-symbol） | **T1** | 已知 32-symbol prefix 上 LS 噪声方差估计 | `nda-awgn-tracking-sandbox/p08r2_chain.py` `CalibrationPrefix`；H7 fix | 仅用 receiver-visible 信息（不含 hidden gamma） | — | 工程机制有效；chronology 仅 PARTIAL | Ch5 实现纪律/附录 | 不可变冻结闭环 | 否（标定工具） |
| 5 | metamorphic gate + 递归 AST 信息边界检查 | **T1** | 运行时证明 deployable path 忽略 hidden gamma；递归 AST 审计 forbidden refs | `p08r2_metamorphic_gate.py`；`p08r2_verify.py`（H7/H8 fix） | 证明 deployable 路径不含 TX-truth/CSI 泄漏 | — | 工程机制有效；chronology 仅 PARTIAL | Ch5 实现纪律/附录 | 不可变冻结闭环 | 否（验证纪律，非方法） |
| 6 | linear Butterfly FIR / LS calibration 边界（强传统 comparator） | **T1** | region retune / standard CMA / last-value persistence / gain calibration 作 local boundary | thesis-map B 行；`pilot-jones-step4a/` B0/B1/B2 ladder；P03/P06/P07-R 局部负面 | 这些传统方法直接吸收多数 ML 修改 | P11 = 固定 20 dB partial（**不是** 9–15 dB；generator 无 gamma 参数，默认 100） | 有效 local boundary；P11 仅 20 dB partial 不可跨 SNR | Ch3/Ch4 对比边界 + 鲁棒性 | 统一 testbed + 共同指标 + 跨切片验证 | 否（对比边界） |
| 7 | AMC Q-A′ dev-only engineering seed（corrected_v2 probe） | **T0（UNAUTHORIZED_DEV_ONLY）** | 两动作契约（Contract A/B）下的 rate-selection probe | `corrected_v2/probe_corrected.py`；`probe_corrected_v2_raw.json` | Contract B 下 9/27 弱湍流 cells feasible，2 cells 胜 baseline 5–7% goodput | 9/27 feasible；2 cells +5.1–6.7% goodput；**调参合同错配**（line 362 未传 allow_no_transmit） | **NONBINDING / HYPOTHESIS_GENERATING**（D008）；Contract B 未获用户授权；tune_C1 缺陷未修；**不得作 Go/scope/METHOD_SIGNAL 判据**；最多 THESIS_ENGINEERING_COMPONENT *候选种子*，但本轮不晋级 | 不放正文（dev-only）；仅 future-work 一句 | 用户授权新 GW + 修 tune_C1 + 合法 baseline + testbed | 否（UNAUTHORIZED，不晋级） |
| 8 | reliable local negatives（P01–P07-R） | **T1** | 局部负面/边界包 | thesis-map C 行；各 P## worker-logs | 这些 ML 修改被强传统方法吸收 | ceiling = `LOCAL_SLICE` | **不得拆成七项创新**；合并为一张 limitations/鲁棒性表 | limitations/鲁棒性章 | — | 否（局部负面，非主贡献） |
| 9 | scale-artifact / metric / lifecycle / oracle 撤回链（G1/P09 + consistency≠correctness） | **T0 / T1 方法论** | INVALID scientific result（G1 scale artifact / P09）→ 方法论反例 | thesis-map C 行；R010 §4；current.yaml dispositions | 撤回链本身是有效实验方法材料 | — | G1/P09 **不得当方法**；G1 图降格或重标；撤回链可作审计 checklist | threats-to-validity/附录 | — | 否（方法论反例，非贡献） |

### Phase B 结论

- **唯一 T3**：DA/NDA adaptive CPR（资产 1）。
- **T2 候选**：资产 2–6 的全部组件**单独**都是 T1（工具/纪律/边界）。只有当它们围绕**同一工程问题、同一 receiver action、同一验证链**时，才可能合成一个 T2 THESIS_ENGINEERING_COMPONENT（Phase C 判）。
- **T0 不晋级**：资产 7（AMC Q-A′）+ 资产 9（G1/P09）。

---

## 2. Phase C — 唯一推荐 thesis spine

### 2.1 贡献 1（确认）：DA/NDA adaptive CPR 主方法

- **M-C-A**：M = 固定 DA 或固定 NDA 单估计器 baseline；C = 星地相干 FSO + Gamma-Gamma 湍流 + 16APSK + per-block 衰落；A = per-block effective-SNR 不匹配（DA 低 SNR 准但付 1.25 dB pilot 罚 / NDA 省带宽但 squaring loss 低 SNR 差）。
- **核心 action**：per-block effective-SNR gate → DA/NDA 估计器切换（fixed 13 dB threshold）。
- **有效数字**：26/29 工作点选对；强湍流/上行 net gain 约 1.2–1.9 dB naive；弱湍流归零（CI 跨 0）。
- **定位**：量化归因型（非"提出新估计器"），已 CCISP 会议级（`abstract.tex`）。

### 2.2 贡献 2 候选判断：receiver-visible coded hardware-aware 部署接收机工程方法

按 brief 要求逐条回答：

| 判据 | 回答 |
|---|---|
| 贡献 2 的 M-C-A 是什么？ | 候选 M = 浮点/纯盲接收链（无定点、无 receiver-visible 编码闭环、无部署信息边界审查）；C = 部署级星地相干 FSO 接收机（硬件位宽约束 + 编码链 + 信息边界）；A = 三个**独立**的部署缺陷（定点退化 / 编码闭环 chronology / 信息泄漏未审计） |
| 核心 action 是什么？ | **不是一个 action**：fixed-point 位宽选择（资产 2）+ coded-chain 闭环（资产 3）+ 信息边界 AST 审查（资产 5）。三者解决三个不同问题 |
| 是否只是"把已有模块接起来"？ | **是**。资产 2–6 解决的是"实现正确性 + 验证纪律"，不是"同一 receiver action"。fixed-point 是位宽；coded-chain 是 FEC；info-boundary 是审计。它们共享"部署接收机"这个**容器**，但不共享"同一可复用设计规则" |
| 哪一项是可复用设计规则或工程方法？ | metamorphic gate + AST info-boundary（资产 5）是最接近"可复用工程方法"的——但它本身是**验证纪律**，不是部署接收机的性能方法 |
| 最强传统实现是什么？ | 浮点 + 标准 CMA + last-value persistence（资产 6）。这些强传统方法**直接吸收**了多数 ML 修改（资产 8 的 7 个局部负面正是被它们吸收） |
| 有什么证据证明该组件**有用**（不只是实现正确）？ | **无**。资产 2–6 的证据全部是"实现正确/不泄漏/不退化"，**不是"相对传统实现降低复杂度/训练开销/硬件位宽且不退化"**。fixed-point +0.0166 dB 是地板；coded-chain 无 chronology freeze；info-boundary 是审计非增益 |
| 能否形成独立章节 + 方法框图 + 算法表 + 实验表？ | 能形成**实现验证章**（Ch5），但**不是方法章**：无统一 M-C-A → 无方法框图 → 无算法表 → 实验表是"实现验证表"非"性能增益表" |

### 2.3 诚实判断：NO_SECOND_CONTRIBUTION_YET

**贡献 2 当前不成立为 THESIS_ENGINEERING_COMPONENT。** 理由：

1. **无统一 M-C-A**：资产 2–6 是三个独立部署缺陷的修复/审查，不是同一工程问题的同一 receiver action。把它们机械拼成"部署接收机工程方法"= 包装，brief 明令禁止。
2. **无"有用"证据（只有"正确"证据）**：T2 要求"工程方法相对传统实现降低复杂度/开销/位宽且不退化"。现有证据全部是"实现正确/不泄漏/不退化"，缺"相对传统实现的工程增益"。
3. **强传统 baseline 直接吸收**：资产 6 的 region retune/standard CMA/last-value/gain calibration 已吸收多数 ML 修改（资产 8 的 7 个局部负面证明）。工程组件若只复现这些边界，不构成独立贡献。

**结论 = `NO_SECOND_CONTRIBUTION_YET`**。不强行包装。

---

## 3. Phase D — bounded evidence-gap audit（推导，不预设）

### 3.1 推导：第二贡献缺的是"工程有用性"闭环，不是新算法

Phase C 判贡献 2 不成立，根因是**缺"工程方法相对传统实现有用"的证据**（不是缺算法）。现有资产有完整的"实现正确"链（fixed-point + coded-chain + info-boundary + 强传统 comparator），但**缺一条**：某条工程规则在相同信息下相对传统实现降低复杂度/开销/位宽且不退化。

### 3.2 是否值得提一个 bounded package？

从现有证据缺口反推（不预设目标）：

- **缺口性质**：缺"工程有用性"证据，**不是**缺科学验证或新算法。这正好是 brief 定义的合法 bounded package 形态。
- **可用 corrected asset**：fixed-point（资产 2，已有 uniform/mixed 结果）+ 强传统 comparator（资产 6）+ 统一 testbed（CCISP 数据）。
- **bounded 程度**：≤1 对话 + ≤半天计算；复用现有 corrected asset；有明确传统 comparator；不改信道模型；不搭多日基础设施。

**判断：值得提一个 bounded package**——但**只作为 fallback 可选**，不作为必须执行项。因为即使它 PASS，也只是把贡献 2 从 NO_SECOND_CONTRIBUTION 升到 T2（工程组件），**不产生第二个主算法**。

### 3.3 唯一 bounded package（推导得到，非预设）

> **目标形态**：在相同 coded performance / receiver-visible 信息下，某条工程实现规则相对传统浮点实现降低硬件位宽（或计算开销），且性能不退化。

**候选具体形态（从缺口推导，非拍脑袋）**：

- **问题**：现有 fixed-point 结果（资产 2）显示 uniform Q(8,6) 已到地板、mixed 最多 +0.0166 dB。这本身是"定点退化可忽略"的证据，但**未对比"传统浮点实现"**——即未证明"定点相对浮点降低了位宽且不退化"。
- **bounded package**：在 CCISP 主方法（DA/NDA adaptive CPR）的相同信道/调制/seed 下，对比 (a) 浮点 selector vs (b) Q-format selector，报告 BER 差异 + 位宽节省。**预注册 PASS/FAIL**：BER 差异 < MDE（如 0.05 dB）且位宽节省 ≥ N bits → PASS（贡献 2 升 T2）；否则 FAIL（贡献 2 维持 NO_SECOND_CONTRIBUTION，定点结果仅作 Ch5 实现验证）。

**合法性核对**（brief 示例）：

| 约束 | 是否满足 |
|---|---|
| 不开新科学方向 | ✅ 复用 CCISP 主方法信道 |
| 不改信道模型 | ✅ GG + 16APSK 不变 |
| 不搭多日基础设施 | ✅ 复用 `_p03_fixed_point.py` |
| ≤1 对话 ≤半天计算 | ✅ 30 seed × selector 对比 |
| 复用现有 corrected asset | ✅ 资产 2 + CCISP 数据 |
| 有明确传统 comparator | ✅ 浮点 selector |
| 有预注册 PASS/FAIL | ✅ 见上 |
| 失败后仍可作工程边界材料 | ✅ 定点退化曲线 = Ch5 实现 |
| 不依赖 oracle 作 Go | ✅ 浮点是传统实现非 oracle |
| 不声称产生第二个主算法 | ✅ 只升 T2 不升 T3 |

**重要**：本 package **不在本轮执行**（brief 明令不跑仿真）。仅作为 Phase E fallback 的可选触发项，待用户决定。

---

## 4. Phase E — 论文落位

### 4.1 唯一推荐章节结构（一个主方法 + 完整实现验证 + 边界分析）

| 章 | 核心问题 | contribution statement | 证据来源 | 图表清单 | 已有/缺失 | claim ceiling |
|---|---|---|---|---|---|---|
| Ch1 绪论 | 星地相干 FSO 湍流下 CPR 为何需要自适应 | 问题背景 + 一个主方法（DA/NDA 切换）+ 实现验证 + 边界 | CCISP W001 Intro + thesis-map A 行 | — | 已有（CCISP 草稿） | — |
| Ch2 系统模型与背景 | GG 块衰落信道 + DA/NDA CPR 基础 + pilot overhead | 标准 GG + 块结构 + DA/NDA trade-off | CCISP W001 SM + V&V1983 squaring loss | — | 已有 | — |
| **Ch3 主方法：DA/NDA adaptive CPR** | 单估计器在 per-block SNR 下为何不够 | per-block effective-SNR gate → DA/NDA 切换，26/29 选对，强湍流 net gain 约 1.2–1.9 dB naive | CCISP W002 Method + `_recovery.py` + `_a4_switch_30seed_fixed.py` | Fig 方法框图 + Tab 主结果 + BER 主图 | 已有（CCISP 完整）；⚠️ headline gain 需补可复现数字溯源 | **T3 唯一主贡献**；弱湍流归零不进正文（R016 §4.1） |
| Ch4 对比与边界分析 | 强传统方法吸收了多少 ML 修改 | region retune/standard CMA/last-value/gain calibration 作 local boundary；7 个局部负面合并 | 资产 6 + 资产 8（P01–P07-R）+ G1/P09 方法论反例 | Tab 对比边界 + Tab 局部负面合并 | 已有（thesis-map B/C 行） | 局部边界 + 方法论，**非第二主贡献** |
| Ch5 实现验证 | 部署级接收机的实现正确性与验证纪律 | fixed-point + coded-chain + info-boundary + 强传统 comparator 审计 | 资产 2–6 | Tab 定点位宽 + Tab coded-chain + 方法框图（info-boundary） | 已有；⚠️ coded-chain 缺 pre-test freeze 重跑；fixed-point 缺浮点对比（Phase D package） | **实现验证章，非方法章**；不得声称 FPGA 真实资源/吞吐 |
| Ch6 结论与展望 | 总结 + 未来工作 | 主方法 + 实现验证 + 边界；未来工作含 AMC（若用户授权新 GW） | 全文 | — | 已有框架 | — |

### 4.2 保守 fallback（工程贡献证据最终不足时）

**若 Phase D bounded package FAIL（或用户选择不跑）**：

- **论文 = 一个主方法（Ch3）+ 完整实现验证（Ch5）+ 边界分析（Ch4）**。
- 贡献 2 **不**强行升 T2；Ch5 明确定位为"实现与评价扩展"，**明确不是第二个新算法**（thesis-map 方案 B 原文）。
- 最低交付：完成 Ch3 主方法整合 + 至少闭合 coded-chain chronology 重跑 **或** fixed-point 浮点对比之一。
- **禁止声称**："7 包负面=第二贡献"、"全域鲁棒"、"coded loss 已正式定论"、"G1/P09 是方法"。

**现实比较**：与同门普通硕士论文相比——一个主方法（会议级，约 1.2–1.9 dB 增益，26/29 选对率）+ 完整实现验证章 + 边界分析章，是**够毕业的体量**（thesis-writing R002/R014 同门对标：量级够格，机制+数字并重）。不追第二主方法是诚实选择，不是降级。

---

## 5. 五项最终汇报（对应 brief 要求）

1. **AMC freeze 终态与 D/V/H**：见 AMC 专题 D009/V010/H006 + 本综合 §0。AMC = `AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD / DORMANT`；Q-A=STOPPED_INCONCLUSIVE / Q-A′=HARVEST_ONLY_ENGINEERING_SEED / Q-B=STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE。
2. **全项目 contribution inventory**：见 §1 表（9 项，1×T3 + 5×T1 + 1×T0-unauthorized + 1×T1-negative + 1×T0-invalid）。
3. **唯一推荐 thesis spine**：见 §4.1（一个主方法 + 完整实现验证 + 边界分析）。
4. **第二工程贡献判断**：**NO_SECOND_CONTRIBUTION_YET**（§2.3）；缺"工程有用性"闭环（§3.1）；可选 bounded package = fixed-point vs 浮点对比（§3.3），不在本轮执行，待用户决定。
5. **文件/verifier/commit/下一合法动作**：见最终汇报段。
