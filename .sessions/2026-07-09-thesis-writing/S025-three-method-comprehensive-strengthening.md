# [S025] 三条既有方法的独立全面补强

> 2026-08-13 | 从战略讨论转入有限执行 | COMPLETE
> 2026-08-13 续接：三项回传、主线程接收核验与裁决分层完成

## 目标

为 P05、P11、P08-R2 各创建一个真正的 Codex 新任务和独立 worktree，在不新建候选、不修改研究流程的前提下，把三个既有方法补强到可供主线程重新选择 Ch4/Ch5 的完整证据包。

## 记录

用户明确要求本轮使用“新对话（session），不是 subagent”。因此三条线不再沿用 T029–T031 的只读深挖方式，而由三个用户可见、相互隔离的 Codex 任务分别执行：

1. T033：P05 固定流标签在线 CMA 均衡；
2. T034：P11 少导频 Complex-LS 2×2 Butterfly FIR；
3. T035：P08-R2 operating-point Offset-Normalized Min-Sum coded receiver。

这次恢复的是**既有方法的 bounded strengthening**，不是自动方法搜索，也不是让三个任务各自重新走一轮开放式 Groundwork。每条线可以做与本方法直接相关的代码真相修复、正式确认实验、统计/消融/复杂度补齐，以及“完整 recipe 是否完全重复”的窄范围检索；不得生成新候选、改 Skill/controller、改正式论文正文或决定总 thesis spine。

三条线使用独立 worktree。每条只写自己的唯一报告与预分配 handoff，避免并行修改 `topic-index.md`、`decisions.md`、`voice.md` 和 `_registry.yaml`；这些聚合文件由主线程在回收时统一更新。

### 共同验收合同

每个方法的最终包至少回答：

1. 实际方法名、receiver-visible 输入—动作—输出、训练/部署边界；
2. 正确且公平的经典 baseline，以及逐字段公平性账本；
3. 清洁重跑的关键场景扫描、paired seeds、CI/离散结果和 metric signature；
4. 能解释增益归因的最小消融，不把共享前缀或无效参数错算成贡献；
5. 复杂度、运行时间、状态生命周期和实现限制；
6. 窄范围 exact-recipe collision 检查。只能写 `未发现完全重复` 或 `发现完全重复`，不得把有限检索写成“证明首次”；
7. 可直接支持方法章的图表清单、有限 contribution、claim ceiling 和明确债务。

已有廉价替代或强邻居不再作为准入门，也不要求三个任务扩大搜索去主动寻找更多否决理由；但不得伪造数字、用 receiver 不可见真值冒充部署、故意削弱 baseline，或保留明知为假的事实命题。

### 共同停机规则

- 每条最多两轮“设计—运行—诊断”主循环；第二轮仍不能得到方向一致、口径合法的改善，则停止并降级，不再调参追正结果。
- 发现 artifact、truth leakage、baseline 不公平或方法动作在源码中不存在时立即停机，先修真相；若修后改善消失，诚实回报该方法不能承重。
- 外部检索只围绕冻结后的完整 recipe；一旦开始扩展到新候选或泛搜强方法，立即停机。
- 不跨方法互相借任务：P05 失败不能转 P11，P11 失败不能转新 estimator，P08-R2 失败不能改成新编码方向。

## 决策引用

- D032：具体 recipe 优先，只有完整 recipe 完全重复才构成碰撞。
- D034：核心方法尽量跨技术对象，CCISP 不是方法名。
- D035：三条跨对象方法已完成只读章级 dossier。
- D036：开放三个独立新任务做全面但有边界的补强（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：否；用户明确把三条既有方法从只读战略讨论扩展到有限执行，见 D036 范围变更记录。

## 后续

三个新任务均已交付唯一报告、handoff、结果和独立验证：

- P05：`fae3c69` 完成正式证据包，`11dbafa` 修正裁决层级。实验强门为 `P05_FIXED_LABEL_RELIABILITY_GATE_FAILED`，但按 D032 仍为 `PACKAGEABLE_WITH_LIMITS`；因与 P11 同属均衡对象且证据/叙事较弱，当前为 `NOT_PREFERRED_CORE`。
- P11：`ad18050` 完成少导频 LS 证据包，`d50c619` 清理格式。终态 `P11_STRENGTHENED`，可作为首选均衡方法章候选。
- P08-R2：`c9bb440` 完成 coded receiver 证据包，`b160f6a` 清理格式。终态 `CONFIRMED_LOCAL_IMPROVEMENT`，可作为技术对象独立但效应较小的第三方法候选。

### Handoff Verification

Verified claims:

- H017 claim 1（30/30 formal grid 与 raw receipt）：PASS — `verification.v1.json` 给出 rows=30、cells=6、每格 5 paired seeds、receipt=PASS。
- H017 claim 2（两个绑定格仅因绝对 CMA mean 门失败）：PASS — 30/100 Hz、20 dB 的 CMA mean 分别为 `0.09763616/0.09935064`，其余 delta/CI/wins 门通过；该强门不再被错误升级为 D032 包装否决。
- H017 claim 3（无 sent truth/Butterfly weights/reset）：PASS — truth audit 三项均为 0；fresh focused pytest `10 passed`。
- H018 claim 1（1% LS BER 非劣）：PASS — LS−Adam pooled BER `−7.7164391e-7`，95% CI `[-1.9641845e-6,0]`。
- H018 claim 2（goodput 改善）：PASS — paired delta `391905.026 bit/frame`，95% CI `[391763.140,392000]`；fresh focused pytest `8 passed`。
- H018 claim 3（180 个 held-out 组合与真相链）：PASS — 独立 verifier 记录 `180/180` unique、true-SNR/shared-realization/metric 均 PASS。
- H019 claim 1（冻结 recipe）：PASS — `(alpha,offset,clip)=(0.875,0.1,30)`。
- H019 claim 2（12 dB FER 改善）：PASS — B0/full=`0.143125/0.1390625`，差 `0.0040625`，95% CI `[0.001875,0.00671875]`。
- H019 claim 3（clip 不计功与 oracle 边界）：PASS — 开发网格 clip20/30 `360/360` 等价，O2 独占 `oracle_payload_truth`；verification `19/19 PASS`，fresh focused pytest `8 passed`。

三个 worktree 均干净；四个 follow-up 后累计 `git diff --check b9072d0..HEAD` 均 PASS。`_registry.yaml` 中本专题 `conflicts_with=[]`，依赖仍为 step4a 既有证据；D036 的三条 bounded strengthening 没有扩成新候选或修改 Skill/controller/正式论文正文。

主线程当前只完成接收和排序，尚未 cherry-pick 三个方法提交，也未拍板最终 thesis spine。下一步应先由用户确认是否采用“Ch3 adaptive CPR / Ch4 P11 / Ch5 P08-R2，P05 作为 Ch4 对照边界”这一现实结构，再做合并与论文整合。
