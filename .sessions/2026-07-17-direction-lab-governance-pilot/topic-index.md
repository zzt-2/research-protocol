# Topic Index: Direction Lab 可遵守性与控制器试运行

> 状态: dormant（治理试运行已收口；仅恢复阈值覆盖仍 PARTIAL） | 创建: 2026-07-17 | 最后更新: 2026-07-18

## 专题信息

- **slug**: 2026-07-17-direction-lab-governance-pilot
- **性质**: 框架试运行 / 可遵守性观察，不是正式研究方向

## 范围边界

- **原始目标**：观察 AI 在真实 Direction Lab 推进中如何失守规则，并确定哪些约束应由脚本、状态机或人工判断承担。
- **当前范围**：历史试运行已完成并冻结；只保留 controller/EvidenceGate/state reducer/真实 sandbox 的验证档案。后续正式研究状态不再追加到本专题。
- **明确不含**：不产出论文结论；不把 pilot 结果当研究结果；不大规模重构现有仿真代码；不创建正式 skill；不替代 `framework-evolution` 的协议设计。
- **范围变更记录**：2026-07-17，D004：由纯治理 shadow pilot 扩展为真实地基 sandbox 候选运行；原因是用户显式要求把 pilot v1 用到真实研究地基并跑完第一批。正式 Groundwork/论文晋级仍明确不含。

## 不变量

- pilot 的治理目标继续有效；真实候选仅作为 sandbox 载荷，候选结果不得自动晋级正式 Groundwork 或论文材料。
- 所有运行必须有 `run_id` 和 manifest；无 manifest 的行为只能标记为观察记录。
- pilot 期间发现的违规不得静默修复，必须保留原始违规、拦截点和修复方式。
- 不因 AI 偶然遵守一次就判定规则有效，必须观察重复轮次和恢复场景。

## 已确认结论

### 不变量

- Direction Lab 的生产 schema 先在 pilot 中压测，再决定实现范围。

### 其他结论

- 暂定采用三层控制：脚本硬门、状态机门、AI 判断门。
- 暂定将“违规成本”和“规则复杂度”同时记录，避免只靠增加规则解决问题。

## 进展线索

- **S001**：试运行目标、观察矩阵和退出条件（本专题首 session）。
- **H001**：新对话启动交接，冻结首轮范围为 sandbox 选择、3-5 个最小硬门、RED 压力测试和独立验证。
- **H002**：第二阶段改为一个主对话连续运行；实现 receipt/evidence gate 后依次完成正常、诱惑、stale/绕过和无历史上下文恢复四轮测试。
- **H003**：冻结提交 `44adff7` 的 pilot v1，进入 5 个真实 shadow 工作循环或一个完整候选批次的单主对话观察期；观察结束后分析完整对话历史。
- **H004**：将 pilot v1 接到双偏振星地 OSL Groundwork 真实地基，先导入 anchor/CandidateMap/BatchQueue，再启动第一批小型 paired batch。
- **D003/H004 修正**：地基是场景、baseline、证据和死路的约束源，不是 ML 候选边界；真实运行先枚举完整处理链的 ML Candidate Universe，再统一排序和批跑。
- **D004/S004**：用户显式批准 scope change；本专题进入真实地基 sandbox 批次，但正式 Groundwork/论文晋级继续阻断。
- **S002**：收 H002 核验、receipt/evidence gate 最小设计、TDD 计划与四轮压力测试过程记录。
- **S003**：完成 5 个真实 shadow 工作循环；核心行为/P0 隔离 PASS，恢复阈值未覆盖，整体 PARTIAL。
- **D001**：选择审计账本背书的最小 receipt/evidence gate；签名与不可变存储留作债务。
- **D002**：execute 结果必须有 execution audit/result hash，并防止同一 receipt replay。
- **V004/V005**：独立 verifier 先发现 result provenance/replay 漏口；修复后 34 tests 与黑盒复核通过，Round 4 hash provenance 仍为 PARTIAL。
- **V001**：B5 隔离输入的首版控制器 RED/GREEN 与独立 verifier PASS（9 tests）。
- **V002**：独立黑盒复核发现 PROMOTE 证据缺失、未知动作和 baseline stale 处理等漏口；结论 PARTIAL，暂不扩展 schema。
- **V003**：修复最小硬门并由独立 verifier 复核，22 tests PASS；manifest 签名/来源绑定列为正式 schema 阶段债务。
- **S004**：完成真实地基 Candidate Universe/Map/Queue v2、B002 production paired batch、独立 post-run verification 与 synthesis；范围保持 sandbox-only。
- **V007**：B001 controller/EvidenceGate/source closure/指标泄漏审计及独立 verifier 均 PASS；监督式线性/MLP 仅作机制级 `ADVANCE_SPECIFIC`，AE 为 `RETIRE_SPECIFIC`，未晋级正式研究或论文。
- **D005/V008**：完成性深审查发现 CandidateMap v1 评分算术错误与 `C24-SSL-AE` 预注册/实现错配；B001 runtime integrity 保留，但流程结论降为 PARTIAL，进入不可变 v2 gate + 替代批次返工。
- **V009/V010**：Universe/Map/runner 与 Queue v2 分别通过独立 pre-run gate；真实 import closure、静态 registry、无标签 AE 与 Queue 对抗变异闭合。
- **V011**：B002 artifact/contract/evidence integrity 独立 PASS；linear/MLP exact-domain advance，无标签 AE exact-mechanism retire，不作家族/论文结论。
- **D006/V012**：v3 将六个运行字段按实际消费者区分 operative 与 audit-only；Queue/Registry/Runner/Validator/Controller 绑定和 strict lean-ledger smoke 独立 PASS，允许进入新的 B003 sandbox batch。CandidateMap 完整性仍仅为 archetype 分区覆盖。
- **V013**：B003 post-run artifact/evidence/contract integrity 独立 PASS；Logistic 与 MLP 仅 exact-contract `ADVANCE_SPECIFIC`，无标签 AE 仅 exact-contract `RETIRE_SPECIFIC`，未晋级方法族、formal Groundwork 或论文。
- **D007/S005**：将已验证流程固化为 `Scout → Sandbox Batch → Promotion/Deep Evidence` 三层执行规范；B003 与 B002 的 U24 exact contract 结果重合，下一批必须换机制族或产生明确新信息；新增 `projects/thesis-fso/direction-lab/process.md` 作为项目级流程唯一拥有者。
- **D008/S009/V014**：completion event 成为状态转换事实源，canonical-state 改为 reducer 投影视图；B003 对账 PASS。机制级 Universe 覆盖审计为 PARTIAL，新增 U35–U44 retained-neutral 接口候选与 5 批 BatchPlan，B004 保持禁止启动。
- **D009/S006**：P01 U25 contract 层实现完成：因果事件校验、固定安全策略、动作集合、无动作恒等性、确定性 replay 与 fingerprint 已有测试；事件生成器、fork-replay 数据和 runner/registry binding 仍未就绪，不能建立 PASS Queue。
- **D010/S007**：P01 causal adapter 已绑定 B003 真实 standard-CMA trace 并闭合字段 provenance/禁入边界；但当前链无 receiver state snapshot/action hook，真实干预效果不可观察，且 run_v3 仍硬编码 U24，故结论为 `P01_BLOCKED`，未创建 Queue/Registry。P02 仅为 `SCOUT_CONTRACT_ASSETS_PARTIAL`。
- **D011/S008/V017**：按 DL-Process v0.3 改用 Universal Core + Communications Profile + dual-pol OSL Project Adapter；P01 状态固定为 `DEFERRED_ARCHITECTURE`。P02/U10 缺双偏振 carrier→CPR→event 链，P03/U19 缺 z-window artifact、合法 CSI/noise 和同信息 comparator；两者均 `NOT_RUNNABLE`，结果为 `B_ALL_CANDIDATES_NOT_RUNNABLE`。P03 是最短闭合路径但未 READY，未创建 Queue/Registry/fingerprint，B004 继续禁止。
- **D012/S008 续接/V018**：P03/U19 完成完整 Interface Closure Sprint；真实 z-window、CSI_NONE comparator、residual artifact、source closure 与 deterministic one-cell smoke 通过独立复核，达到 `P03_SCOUT_CONTRACT_READY`，但 Sandbox/B004/Queue/Registry 继续阻断。
- **D013/S010**：完成 formal/sandbox/Scout 三层控制面收口和重复 S005 修复；研究当前态回归项目目录，本专题因恢复阈值覆盖仍 PARTIAL 转 `dormant`。
- **V019/S010**：独立复核控制面状态、P03 唯一当前状态、历史 hash、编号引用和 dirty worktree 审计均 PASS；无 B004、无历史批次改动。

## 未决项

- governance recovery 阈值覆盖仍为 PARTIAL；只有专门恢复该验证时才重新激活本专题。
- v2 runner 已实现 31-file closure 与静态 registry，但 snapshot 仍含本机绝对路径；跨机器/canonical 前须改相对路径并记录 workspace identity。
- 机制级 Candidate Universe 仍未闭合；AP×method×information-interface 差集、重复归并和 D031–D039 历史 lineage 修正已登记在 `candidate-coverage-audit.v3.yaml`。
- P01 exact implementation 已因 `STATE_SNAPSHOT_MISSING/ACTION_EFFECT_NOT_OBSERVABLE/RUNNER_U24_HARDCODED` 阻断；负结论只作用于当前 standard-CMA 接口实现，不否决 U25/U42 整个方法族。
- P02 有 FOE/VV/BPS/DPLL 和 phase-noise 邻接资产，但当前双偏振链缺 carrier impairment/CPR/event library；只能先做轻门控 contract。
- P03 的 residual-aware estimative/detection 接口已在 CSI_NONE 等级闭合；下一步 residual headroom probe 由项目目录管理，不在本专题追加。receiver-estimated CSI、multi-cell stability、正式 evaluation evaluator、真实 U19 ML mechanism 与 Sandbox Queue 仍缺。

## 当前位置

治理试运行已收口：B003 state-projection reconciliation 完成，P03 当前状态已交回项目目录，重复 S005 已修复为 S005/S009。本专题转 `dormant`；只有恢复阈值专项验证可重新激活。正式研究仍 BLOCKED，B004 继续禁止。
