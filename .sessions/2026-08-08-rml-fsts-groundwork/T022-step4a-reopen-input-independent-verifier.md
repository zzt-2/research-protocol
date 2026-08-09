# Task Brief: RML-FSTS Step 4a reopen-input independent verifier

> 来源: D011-D013 / V007 / H006 / S005 / T020-T021 | 日期: 2026-08-09
> 时间上限: 15 分钟；到点必须给出证据化 PASS/FAIL/PARTIAL，不得启动 repair 或实验
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-reopen-input-verifier.md`

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 37
  action_class: NEW_TOPIC_RECOVERY
  mission_checkpoint: CP024
```
<!-- RDL-TASK-CONTROL:END -->

## 任务

你是 fresh-context 独立 verifier。只审查 D012 的两项重开输入恢复及 D013 候选 reducer；不得设计/修复 source config 或协议，不得联网扩检索，不得运行 estimator、performance grid、diagnostic structural run、C1 或 MVE，不得修改 owner、receipt、治理文件、代码、合同、原 terminal artifact 或 protected logs。唯一允许写入的是指定 verifier worker log。

开始前完整读取并遵守：

1. `using-superpowers`、`research-direction-lab`、`session-governance`、`sim-preflight` skills；
2. 本 T、D009-D013、V006-V007、H006、S005、T020-T021；
3. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-public-source-config-recovery.md`；
4. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-action-before-protocol.md`；
5. `projects/thesis-fso/worker-logs/step-4a-rml-fsts-source-calibration.md`、`step-4a-rml-fsts-physical-transfer.md`、`step-4a-rml-fsts-independent-verifier.md`；
6. `projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-terminal-receipt.json` 与候选 `step4a-reopen-input-receipt.json`；
7. canonical Wang fulltext `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md` 及 T020/T021 引用的一手本地证据；
8. current `topic-index.md`、`literature_notes_rml_fsts.md`、`master-state.md`、registry 与 `verifications.md`。

先运行并记录：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  .sessions/2026-08-08-rml-fsts-groundwork/T022-step4a-reopen-input-independent-verifier.md `
  --repo-root D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
```

非 PASS 立即停止并只写 setup blocker。

## 必验门

### G1：SC1 source-config 证据边界

- 独立确认 T020 覆盖 publisher/DOI、author/institutional、code/data repository 三类 surface，并遵守止损；不把“本轮未发现”扩大成全互联网不存在。
- 核对 exact paper identity：IEEE document/arnumber=`10097873`；`10101698` 只是 issue/media-path id；article sequence=`7302313`。身份纠正不得被写成 executable config recovery。
- 逐字段检查 D012 SC1 的 1–7：是否确实 `EXACT_CLOSED=0/7`；任何一般公式、相似平台、典型值、图像恢复或 scalar Gamma-Gamma 不得算 exact closure。
- 复核 exact canonical content/source identity/hash 与 T020 ledger；若本地 source artifact 不存在，不得要求 executor 伪造下载物。

### G2：AB1 因果与可执行性

- 从 Wang 原文独立核对 structural `(B_N,B_L)` 在发端 FSTS construction 之前冻结，正文没有 previous-frame/common-probe/RSSI/feedback/ACK/action-signaling/lifecycle 的 executable caller path。
- 分别审查 previous-frame 与 common-probe：action-invariant observation、time-series/cadence、feedback、latency/freshness、state/fallback、overhead、paired unit 任一关键项缺失即不得 PASS。
- 复核 Valjus/sat.1553、WiSEE 2024、JLT 2023 的原文边界。generic `>1 ms` 或 intra-frame static 不得推成跨帧 feedback freshness；JLT 的 processing/RTT/Greenwood 边界不得被扩大为本系统的现成协议。
- 特别审查 provenance：T021 parent executor 超时后被中断；fresh child 完成 Wang 455 行全文精读，最终 protocol log 由主控基于 delegated read 与本地 primary line checks 合成。该 log 只能作为待审证据，不得自称独立 verification。

### G3：Reducer 与科学终态唯一性

- D012 reducer 必须唯一：SC1 与 AB1 任一未闭合即 `REOPEN_INPUTS_NOT_CLOSED`，无“部分闭合先跑 diagnostic”出口。
- D013 只闭合本次 recovery Probe；不得取代 D011/V007 的 scientific terminal `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`。
- 确认 Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`、object/package failure=`0/0`。
- B0/B1/B2/O1/C1、paired delta/CI 均必须为 `N/A (NOT_RUN)`；scientific raw rows=`0`；不得从 source/protocol negative 推断 ranking crossover、B2 absorption、residual、Go/Kill/Resolved。
- conditioned `(modulation, TS length, receiver-power bin) -> single structural lag/B_L` lookup 继续是必须保留的 strongest cheap comparator，不得包装为方法。

### G4：Owner、artifact 与机械完整性

- current topic/literature/master/registry/D013/S005/receipt 的候选状态必须一致，V008 写入前均清楚标 pending；原 terminal receipt 不得被改写。
- 复算两份 recovery worker-log SHA-256 并与 candidate receipt 一致；JSON/YAML 可解析，全部引用路径存在，receipt reducer/authority/NOT_RUN 数字一致。
- 运行 `git diff --check`、`git status --short`、必要的 path/hash audit。确认无 `common/`、`params.py`、旧 campaign 或正式论文改动。
- 四个既有未跟踪 `projects/simulation/explore/cma-fade-divergence/p05_run*.log` 必须保持 V007 的 bytes/SHA-256/mtime 且未暂存：
  - `641 / 7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `2417 / 735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `929 / c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `1430 / 95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- 未 commit、未 push；verifier 不得自行 commit/push。

## 输出格式

```markdown
# RML-FSTS reopen-input independent verification
## Verdict
## Control and scope
## SC1 verification
## AB1 verification
## Reducer and scientific-terminal audit
## Owner/artifact/hash audit
## Findings by severity
## Final gate matrix
## Conclusion
```

结论必须使用 `PASS`、`FAIL` 或 `PARTIAL`，并给 P0/P1/P2 计数。`PASS` 只表示 recovery terminal 与证据边界被独立接收，不表示 Q1 scientific success、performance correctness 或 novelty closure。发现问题只报告，不修复；只写指定 worker log，不 commit/push。
