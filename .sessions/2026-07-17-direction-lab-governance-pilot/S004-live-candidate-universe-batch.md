# [S004] 真实地基 Candidate Universe 与首批 paired batch

> 2026-07-17 | 真实地基 sandbox 运行 | COMPLETE

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

## 决策引用

- D003：真实地基是约束与证据源，不是 ML 候选边界
- D004：pilot 扩展为真实地基 sandbox 运行但不等同正式 Groundwork 晋级（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D004 scope change record）

## 后续

完成 anchor、Candidate Universe、CandidateMap、BatchQueue、门控、B001 sandbox paired batch、独立 verifier 与 Batch Synthesis。下一步只能对两个监督式检测机制做新的、单独门控的 causal safe-fallback 复验，或转向新的候选族；不自动扩大有效域，不自动进入论文材料。
