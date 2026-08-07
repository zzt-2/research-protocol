# Task Brief: 2A region-calibration authority reconciliation

> 来源: S018 / D037 / CP020 | 产出位置: 2A reconciliation artifacts、Ch4 package、worker-log 与 system D/V/current owners
> 日期: 2026-08-07
> 唯一文档: 执行方以本 T 为动作合同，并按必读路径核对原始证据

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 33
  action_class: THESIS_AUTHORITY_RECONCILIATION
  mission_checkpoint: CP020
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 完成且只完成一次 2A authority reconciliation。
分别裁决 P01 pilot-SNR adapter、P02 weak/low-SNR retune、T004 online estimated-SNR calibration；不把三者混成一个方法。

**最高纪律：**

1. 先复用和确定性复算已有 raw evidence；证据闭合时禁止重复跑实验。
2. P02 只有在 deployable region identity、无 truth leakage、非单标量动作、至少二区不同合法动作、original/global 公平 comparator 与完整成章链同时满足时，才可进入方法包装/确认。
3. 若 weak region 只由 truth label 定义或实现只是 `ref 9→11` 单标量调参，直接 `SUPPORTING_ONLY` 或 `REJECT`；禁止发明 classifier。
4. T004 immutable pre-test gate REJECT 与无合法 held-out 结果冻结；P02 数字不能证明 T004，T004 失败不能自动否定 P02。
5. 不改 common/、params.py、CCISP 本体或论文正文；不恢复 cand_rank、online calibration、P1/C3/AMC/coded-burst；不 push。

## 1. 冻结对象与事实

- P01：receiver-known pilots → pilot-SNR estimate → original selector branch command。
- P02：历史 weak/low-SNR target slice 上 dev-tuned reference retune；必须沿实际代码判断它是区域规则还是全局标量。
- T004：current-window estimated-SNR → equal-capacity three-region map → unchanged selector；dev B2 `+0.30846 dB`，M `+0.26750 dB`，且 held-out 前 evidence gate REJECT。
- P02 冻结数字：weakretune−adapter `+0.4539 dB`；cand_rank−weakretune `−0.0961 dB`，CI `[−0.1060,−0.0862]`。

## 2. 执行顺序

1. 完整读取 system control、D021–D023/D036/D037、T002/T004/T009、inventory、P01/P02 worker logs/artifacts、T004 commit package/results/verifier、thesis-lessons 速查与 TL-31–33。
2. 生成 deterministic raw→aggregate artifact：seed/chronology、region source、paired delta、cluster CI、harm recovery、safety、branch-command effect。
3. 执行六项方法语义门；门不过即停止新实验。
4. 仅在语义门 PASS 且缺 held-out 时使用 sim-preflight，冻结 B0 original、B1 global、M deployable region rule、O truth oracle，并按一次 Commit 1/Commit 2 合同执行。
5. 形成 authority reconciliation、Ch4 package、流程图、original/global/region 主表、claim ceiling、适用边界与唯一 terminal。
6. 同步 D/V/mission/topic/inventory；fresh-context verifier 独立检查授权、deployable identity、truth、chronology、raw aggregation、公平性和 terminal 唯一性。

## 3. Terminal

只允许：`THESIS_METHOD_EXTENSION_READY / THESIS_ENGINEERING_COMPONENT_READY / SUPPORTING_ONLY / REJECT / EXECUTION_INVALID / EXTERNAL_BLOCKED`。

最高合法表述仅为“工作点失配下的 region-calibrated robust CCISP extension”；不得称新 selector、CPR estimator、online calibration 胜出、通用自适应阈值理论、METHOD_SIGNAL 或第二主算法。

## 4. 验收

- [x] control epoch 33 / CP020 / D037 绑定并通过 guard
- [x] P01/P02/T004 三对象分账
- [x] raw→aggregate 与 chronology 有可复现 artifact
- [x] deployable-region 与 truth-leakage 由 caller-level 证据裁决
- [x] 未通过语义门时没有运行新 held-out
- [x] Ch4 package、流程图、主表、claim ceiling 与 terminal 齐全
- [x] fresh-context verifier 独立通过：V021 PASS，P0/P1/P2=0/0/0

## 5. Completion

`SUPPORTING_ONLY`。P01 保留 local adapter supporting asset；P02 是 truth-defined target slice 上的全局
单标量 retune；T004 继续 pre-test `REJECT` 且无 held-out。epoch 34 / CP021 / D038 是完成投影。

## 附：产出回传位置

- `projects/simulation/results/2a_region_calibration_authority_reconciliation/`
- `projects/thesis-fso/direction-lab/harvest/region-calibrated-ccisp-authority-package.md`
- `projects/thesis-fso/worker-logs/step-045-2a-region-calibration-authority-reconciliation.md`
