# Coded decoder-feedback 方法主线 Groundwork

> 状态：closed | 创建：2026-08-09 | 当前阶段：Step 1 candidate-set exhausted / verified

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 5
  role: METHOD_PRODUCTION_GROUNDWORK
  mission: produce one thesis-usable Ch4 coded decoder-feedback method or a canonical evidence-backed terminal
  active_lane: CLOSED
  authority_pointer: projects/thesis-fso/master-state.md
  decision_gate: D004/V002 retain STEP1_NO_METHOD_ACTION_SURVIVOR and STEP1_CANDIDATE_SET_EXHAUSTED; canonical_mapping is null and Problem was not evaluated because no Q# was formed
  allowed_actions: []
  forbidden_actions:
    - SCIENTIFIC_EXPERIMENT
    - ADAPTER_IMPLEMENTATION
    - MVE
    - CONTRACT
    - EXECUTE
    - THESIS_CLAIM
  mission_log_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/mission-log.md
  mission_checkpoint: CP005
  next_legal_action: none; reopening requires explicit scope change plus evidence for a genuinely different carrier-recovery action
```
<!-- RDL-CONTROL:END -->

## 范围边界

**原始目标**：以“形成可写入毕业论文章节的方法”为明确目标，完成 coded decoder-feedback 候选收敛、Groundwork、Step 4a、最小 adapter 和公平方法比较的连续推进；除真实硬 blocker 外，不以入口检查、计划、单个上游步骤或 adapter identity 作为终点。

**当前范围**：

- Ch4 coded carrier-recovery / decoder-feedback 方法章槽位；最多保留两个机制不同候选。
- receiver-local、因果合法的 decoder extrinsic、syndrome/CRC、iteration callback、bounded recovery/re-evaluation 所需最小接口。
- 3–7 天量级 method-bearing testbed；只有 Step 3 合法 Q# 与 Step 4a problem gate 通过后才能建设。
- B0/B1/B2/O1/C1/C2 baseline ladder、defect smoke、paired fair comparison、机制消融和 fresh-context verifier。

**明确不含**：

- 不恢复 P08 LLR calibration 或 P08/P08-R 旧科学结论。
- 不把 coded-chain correctness、信息边界修复、adapter identity 或 deterministic validator 包装成方法。
- 不扩建完整通用通信平台；不修改 `common/` 或原 coded-chain 资产来掩盖 adapter 身份。
- 不允许 TX payload truth、true phase/CFO/h/SNR 或 post-hoc final correctness 进入 deployable decide path。
- 不修改或暂存四个既有 `p05_run*.log`；不 push；默认本对话统一一次提交。

**范围变更记录**：

- **[2026-08-09] [决策 D001]**：把 T010 旧“design-only / ≤1 天 adapter”资产阻断扩为独立的 3–7 天 coded decoder-feedback 方法生产 Groundwork。
  - 原因：用户明确把 Ch4 方法产出设为本轮目标，并授权建设最小 method-bearing adapter/testbed。
  - 新范围：允许在 canonical Step 1–3/必要 3.5/4a 通过后建设实际需要的 decoder 中间信息与外层 callback/recovery 接口，并运行公平比较。
  - 影响的未决项：T010 `CODED_CHAIN_ASSET_BLOCKED` 保留为旧授权下的 readiness 事实；C1/C2/C3 需重新核对，不自动晋级、不恢复旧科学数字。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. Groundwork 顺序是唯一合法路径；Step 3 与 Step 4a 是硬门控，上游不通过即按 canonical terminal 收口。
2. 问题必须是具体 `M-C-A`：传统载波恢复方法在 coded/phase impairment 条件下因可观测机制产生可恢复 decoder failure，decoder-visible 信息能驱动不同且合法的 recovery action。
3. adapter 只提供方法所需接口；receiver-visible-only 信息边界、no-feedback identity、callback lifecycle、metamorphic test 和 raw receipt 必须可执行验证。
4. oracle 只作 headroom/Kill；Go 对手是经独立调谐、任务匹配、同信息的 conventional comparator，且必须测试 strongest cheap alternative。
5. 公平比较使用 fresh disjoint dev/test seeds、paired realizations、raw codeword/trajectory rows、cluster CI、固定标签 coded metrics、复杂度与迭代账本。
6. `FAIR_COMPARISON_RUN` 是最低方法生产增量；只有问题不存在、传统 baseline 已解决、执行无效/证据不足或 3–7 天内无法解除的真实 hard blocker 可提前终止。

### 其他结论

1. 旧 T010 的 `CODED_CHAIN_ASSET_BLOCKED` 只证明当时 ≤1 天资产预算不够，不是 decoder-feedback 科学 Kill。
2. C2 旧卡在动作身份上碰撞最少，但仍须与 turbo/iterative carrier recovery 直接竞品、P08 scalar calibration 和 hard-DD/CMA cheap alternative 重新核对。
3. D002 将 C2 true-extrinsic soft-symbol CPR 与 C1 finite phase-hypothesis re-evaluation 保留为仅供 Step 1 证伪的 `HYPOTHESIS_ONLY` 预卡；C3 因 recovery action 与 C1/D047 同族，不再作为独立候选。
4. Sionna 2.0.1 的 soft output、message state、iteration override、callback 与 coded-bit↔16QAM 映射属于 bounded adapter work；当前 corrected P08-R2 缺载波 phase/CFO impairment、CPR state 和可调用 recovery action anchor。该事实是当前 testbed blocker，不是已证明超出 3–7 天的终态 hard blocker。
5. D003/T008 的 repaired integrated Step 1 语料质量门 PASS（93 annotated rows→66 unique，7 source families，必读 6，正式发表 50/66=75.76%）；自动镜像 28/28 已处置为 duplicate 8 / irrelevant 10 / strong neighbor 4 / baseline 2 / unknown 4。C1/C2 均保持 `CORE_ACTION_EXACT`，replacement=0；local terminal=`STEP1_NO_METHOD_ACTION_SURVIVOR`。
6. 此终态来自 direct-action collision，不是 testbed hard blocker、传统 baseline 性能结论或 P08 旧数字；因此不建设 adapter，也不进入 Step 2。
7. D004 撤销 D003 的 `NO_VALID_PROBLEM` 映射：本轮未进入 Step 2/3、未形成 canonical M-C-A Q#，因此 problem disposition=`NOT_EVALUATED_NO_Q_FORMED`；“候选动作无 survivor”不能重定义成“问题无效”。

## 进展线索

- **S001 / D001 / CP001**：证据 worktree HEAD 与用户起点一致；目标专题查重为无；登记 3–7 天 scope change 并激活 RECOVER_MAP。
- **S001 / D002 / CP002**：T001–T003 三路恢复完成并由主控核证；候选收敛为 C2、C1 两张 Step-1 预卡，C3 合并为 C1 的 syndrome evidence/ablation；控制面进入 GROUNDWORK_STEP1_SEARCH。
- **S001 / D003 / CP003（历史 mapping，已由 D004 取代）**：T004–T006 完成两轮检索与独立整合；C1/C2 core action 均 exact collision、0 replacement；当时写入的 terminal mapping=`NO_VALID_PROBLEM` 已撤销，Step 2/adapter 冻结事实保留。
- **S001 / T007 / CP003**：fresh-context 终验为 FAIL（P0/P1/P2=`0/2/1`）；C1/C2 collision receipts 与 65→46 合并口径通过，但发现一个 28-result 自动镜像只与 integrated corpus 精确重合 4 条，剩余 24 条未逐条处置；当前仅允许 T008 补齐镜像裁决和 integrated v2，随后另起 T009 复验。
- **S001 / T008 / CP003**：自动镜像 28/28 已逐条处置，独立分类反馈纠正了一次摘要指纹过合并；最终 integrated v2=93→66、50/66 published、6 must-read、7 sources，4 个 unknown 均不含可识别 action，replacement=0 与 D003 不变；进入 T009 独立复验。
- **S001 / T009 / CP003**：A/B/C 均 PASS，D 因主控把压缩摘要中的哈希缩写错误扩写为不存在的完整 SHA 而 FAIL（P0/P1/P2=`0/1/0`）。HEAD 内三组权威记录与 fresh 日志完全一致，确认不是文件变化；改由 T010 动态读取 HEAD receipt 复验。
- **S001 / D003 / V001 / H001**：T010 动态读取 HEAD receipt/T022 后 A/B/C/D 全 PASS，P0/P1/P2=`0/0/0`；其 artifact/protection 结论保留，但 staged reviewer 发现 canonical mapping 与 H/V/T/report 治理问题，原关闭状态撤回。
- **S001 / D004 / CP004**：staged reviewer 无 Critical、4 个 Important；D004 保留 local terminal、撤销 `NO_VALID_PROBLEM` 映射，problem disposition 改为 `NOT_EVALUATED_NO_Q_FORMED`；T009 恢复派发快照，H checklist 复位，V001 降为 PARTIAL，报告 v1 标历史，进入 T011。
- **S001 / D004 / V002 / H001 / CP005**：T011 在 `00:04:08.356` 内完成最终复查，P0/P1/P2=`0/0/0`、A/B/C/D 全 PASS；三层语义、integrated v2.1、current/history、T/H/V 模板、HEAD/staging 与 p05 4/4 均接收，专题关闭。

## 当前状态

- 当前模式：`closed / verified Step-1 candidate-set exhaustion`。
- 当前 Q#：无；两张预卡在 Step 1 被 direct-action collision 否决，未进入 Step 3 问题形成。
- 当前 survivor：0。
- 当前 method delta：`NONE`。
- 当前 local terminal：`STEP1_NO_METHOD_ACTION_SURVIVOR`。
- 当前 framework disposition：`STEP1_CANDIDATE_SET_EXHAUSTED`。
- 当前 problem disposition：`NOT_EVALUATED_NO_Q_FORMED`（没有 Q#，不是 `NO_VALID_PROBLEM`）。
- 当前验证：V002 PASS；P0/P1/P2=`0/0/0`；无自动科学下一动作。

## 未决项

1. 未来重开须出现与 C1/C2/C3/D047/P08/P05/CCISP/Ch5 均不同、且有 problem/action evidence 的新 carrier-recovery action，并经显式 scope change。

## 当前位置

`CP005 / CLOSED`：Step 1 candidate set exhausted 已由 V002 接收；新检索、全文获取、Step 2、adapter、实验和论文方法声称均无授权。只有显式 scope change + 新的不同 action evidence 才能重开。
