# [S004] 真实地基 Candidate Universe 与首批 paired batch

> 2026-07-17 | 真实地基 sandbox 运行 | COMPLETE
> 2026-07-18 | v2 gate、B002 与独立 synthesis 闭环
> 2026-07-18 | v3 replacement governance 与 smoke

## 目标

在双偏振星地 OSL 已冻结地基上建立完整 ML Candidate Universe，形成 CandidateMap 与 BatchQueue，通过门控后运行第一批小型 paired batch，并交独立 verifier 审查。

## 记录

- D004 已登记本轮显式 scope change：真实候选是治理 pilot 的 sandbox 载荷，不等同正式 Groundwork 或论文晋级。
- 地基独立核验发现 master-state 与最新 D/V 存在状态漂移；历史批次事实可引用，正式 Step 3.5/Step 4a 晋级继续阻断。
- 统一 batch runner 只存在于 `.worktrees/unified-batch-runner` 的未提交快照；主树不可直接复现。运行前必须冻结逐文件源码哈希并在 manifest 标注 sandbox provenance。
- 新鲜定向测试暴露 Windows memmap 释放缺陷；根因是 `TemporaryDirectory` 清理时 `shared` 中的 memmap 仍持有文件句柄。已有回归测试先 RED，最小关闭映射修复后定向 20 tests PASS。
- Candidate Universe 完成全处理链扫描：26 个应用点、13 个方法族、12 个改进维度、32 个候选 archetype；CandidateMap 与 BatchQueue 均通过独立门控，未将历史 CandidateMap 当作封闭全集。
- B001 已通过 controller 与 EvidenceGate：30 个 paired cells、30 个 baseline calls、46,860 行 block 结果；manifest/result/source closure 与 receipt hash 均一致，EvidenceGate 为 `ACCEPTED/TRUSTED`。
- 独立 verifier 对 B001 给出 `PASS (sandbox evidence integrity)`。监督式线性与浅层 MLP 检测器在预注册域内 `ADVANCE_SPECIFIC`；clean-reconstruction AE 为 `RETIRE_SPECIFIC`。这些是机制级观察，不是方法族 Go/Kill、正式 Step 4a 或论文结论。
- 原始大结果与 evidence ledger 保留在隔离 batch 目录；仅小型 manifest、audit、verifier report 与 synthesis 进入版本控制，避免将 240MB 级运行产物混入代码提交。
- 完成性审计将 `batch-queue.yaml` 明确为 manifest 绑定的 pre-run 冻结合同，不回写其 `QUEUED_NOT_RUN` 字段；新增 `execution-status.yaml` 作为运行后状态源，记录 B001 为 `COMPLETED_SANDBOX_VERIFIED`，避免队列合同与运行状态混为一谈。
- 地基五类核验均保留源指针而不复制结论：候选族与 Batch 0.5/1/2 见 foundation `S041–S074/V006–V029`；具体 Kill/FAIL/DEFER/observation-only 见 `D040–D056`；standard-CMA/current-CMA 身份见 `D040/D045`；fixed/PI 双口径见 `D018`；有效域与证据等级逐条以相应 D/V 原记录为准。
- V008 的深审查推翻“流程整体已闭合”：CandidateMap v1 的手写 score 与声明权重不一致；`C24-SSL-AE` 实际用 train fixed-label 筛 clean rows，不符合“不需要 event labels”的预注册机制。B001 的运行/hash/指标完整性继续有效，但流程结论降为 PARTIAL，旧 AE 结果只限 oracle-supervised clean-row AE，不得扩成 SSL-AE Kill。
- V009 完成 pre-Queue 修复复审：Universe v2 扩为 34 archetype，Map v2 与真实 import/source/registry 门控通过；真正无 event-label AE 与 default production runner 均通过反例和最小真实链测试。该 PASS 仅释放 Queue v2 编制，不释放 B002 运行。
- V010 独立门控 Queue v2；13 类对抗变异全部被拒，Queue 只在 PASS 三联和证据指针闭合后释放 B002。
- B002 使用默认 production runner 完成 30 个共享 cells，经 controller/EvidenceGate `ACCEPTED/TRUSTED`；V011 独立审查 PASS。linear/MLP 仅为 exact-domain `ADVANCE_SPECIFIC`，无标签 AE 仅为 exact-mechanism `RETIRE_SPECIFIC`，无论文或方法族晋级。
- B002 对账确认历史哈希链内部一致，但 ledger 含完整结果且结果重复存储，六个显式运行字段未冻结；B002 保持不可变 exploratory evidence，不修、不重跑。
- v3 新建 B003 Queue/Registry/Runner 快照，显式绑定 Universe/Map lineage、run_v2/run_b001/controller/validator helper fingerprints；运行前重新执行静态 binding gate；11 项基础治理测试、strict pointer 测试和 12 项 v3 smoke/contract 测试通过。
- 独立 verifier 复核确认 v3 的哈希、helper binding、显式 batch_id、contract_override 禁止、lean ledger、artifact pointer、source-closure smoke 均通过；CandidateMap 仅证明 archetype 分区，不证明方法空间穷尽。
- D006 将 `fade_threshold_h` 与 `clip_norm` 在 v3 contract 标为 `audit_only/non-operative`，不修改 canonical baseline；V012 独立复核后 Queue gate 已通过。
- B003 在新隔离目录完成 30 paired cells 与 30 次 standard-CMA 调用；V013 独立 post-run verifier PASS。Logistic/MLP 为 exact-contract `ADVANCE_SPECIFIC`，无标签 AE 为 exact-contract `RETIRE_SPECIFIC`；结果仅 exploratory，不晋级论文。
- S009 续接完成 B003 completion-event/reducer 对账、机制级覆盖审计和 5 批 BatchPlan；本轮不启动 B004。

## 决策引用

- D003：真实地基是约束与证据源，不是 ML 候选边界
- D004：pilot 扩展为真实地基 sandbox 运行但不等同正式 Groundwork 晋级（新建）
- D005：B001 保留为带 protocol deviation 的历史证据，corrected v2/替代批次另行闭环
- D006：v3 显式区分 operative 与 audit-only 运行字段（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D004 scope change record）

## 后续

本 session 已完成 B003 小型 paired batch、独立 post-run verifier 与 exploratory synthesis；S009 已完成 state reconciliation、机制覆盖审计和 BatchPlan。下一步只能补 P01 action/replay 接口或切换 Scout，不启动 B004；B002/v2 不改写、不覆盖。
