# Task Brief: Ch4 decoder-feedback CCISP 方法构造预检

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 35
  action_class: DECODER_FEEDBACK_METHOD_CONSTRUCTION_PREFLIGHT
  mission_checkpoint: CP022
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S019 / D039 / CP022 | 产出位置: `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`
> 日期: 2026-08-07
> 唯一任务: 只用本地证据构造并碰撞 3 个 decoder/soft-feedback CCISP 方法形候选，最多保留 1 个 survivor

## 0. TL;DR

在 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 做一次
**design-only、local-only** 方法构造预检。Ch3 CCISP 与 Ch5 select-before-execute 已有方法 authority；
Ch4 仍是开放的方法槽位，`SUPPORTING_ONLY` 不能填槽。

本轮只回答：coded/decoder 输出是否能形成一个不同于阈值重调、LLR 标定、CRC 重标和 online-CMA 的
真实反馈动作链。不得检索、下载或精读新论文；不得进入 GW、实现、修改 coded chain 或跑仿真。

## 1. 必读与冻结边界

按顺序读取并给出 `path:line` 收据：

1. 本专题 `topic-index.md`、D038–D039、CP021–CP022；
2. `.agents/skills/research-direction-lab/references/method-production.md` 的 chapter-slot 与
   concept-construction 规则；
3. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`；
4. `projects/thesis-fso/direction-lab/candidate-coverage-audit.v3.yaml` 中 U38/U39，以及
   `projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/portfolio-refresh.v1.yaml`
   中 U47；
5. F4-A/F4-C 的 probe、artifact、decision/verifier 和 scale/smoothing 边界；
6. P08-R2 corrected coded-chain 的 runner、信息边界、authority 与 partial-asset 裁决；
7. P05 online adaptation、CRC-flip dead end、CCISP caller 与 Ch5 single-branch 方法包。

冻结事实：

- F4-A 只是 LLR/noise calibration oracle，增量薄且 smoothing-fragile；不得当反馈方法正证据。
- F4-C CRC-flip/重标与 PI-BER 或 truth-assisted relabel 碰撞，已 Kill，不得换名恢复。
- P08-R2 的可复用部分是 corrected coded-chain、prefix-LS 与信息边界；其 LLR calibration 不是
  decoder→CPR feedback，深衰落不可恢复边界仍有效。
- P05 online standard-CMA 可解决的动作不能重命名为 decoder feedback。
- 本轮不产生 METHOD_SIGNAL、active carrier、Go 或论文 claim。

## 2. 先做 coded-chain callback readiness 审计

沿实际 caller→callee 回答四项，每项只能是 `READY / NEEDS_SMALL_ADAPTER / NEW_INFRASTRUCTURE`：

1. decoder 是否暴露 per-symbol extrinsic LLR/soft symbol，而非只有最终 bits；
2. 是否暴露 syndrome/CRC/decoder-failure 状态及其因果时点；
3. 是否允许受控迭代或 callback 回 CPR/recovery，而非 post-hoc 评分；
4. iteration、latency、net-rate 与 comparator 是否可统一记账。

任一候选需要两项及以上 `NEW_INFRASTRUCTURE`，该候选最终拒绝。但 readiness 审计不得替代方法构造：
即使三者全部 blocked，也必须先完成下节三张 prototype/concept card，再据此给出
`CODED_CHAIN_ASSET_BLOCKED`，避免本轮退化为纯基础设施审计。

## 3. 必须构造的三张 prototype/concept card

只构造以下三类，不制造第四弱候选：

1. **C1 Decoder-Aided Phase-Hypothesis Feedback**：decoder extrinsic/syndrome 对有限相位假设进行
   因果重评分，并真实改变下一次 CPR 决策；禁止 TX truth、post-hoc relabel 或只挑最好结果。
2. **C2 Extrinsic Soft-Symbol Iterative CPR**：decoder extrinsic soft symbols 回送给 CPR，更新相位/
   频偏估计；必须避免把 a-priori LLR 重复计算成 extrinsic 增益，并冻结迭代次数/时延。
3. **C3 Syndrome-Triggered Recovery Control**：receiver-visible syndrome/CRC failure 触发有限重获取、
   假设切换或窗口调整；必须有 causal downstream action，不能只是 failure flag/统计筛选。

每张 prototype/concept card 必须完整包含：

1. 名称与章节槽位；
2. `M-C-A`；
3. 信息源→动作→输出；
4. 5–8 步算法流程；
5. 相对 CCISP/P08/F4/P05 的新增点；
6. 同码、同净码率、同 iteration/latency 的传统 comparator 与 strongest cheap alternative；
7. 主图；
8. 承重消融；
9. 最小 testbed delta 与工期；
10. claim ceiling 与失败 fallback；
11. collision receipt：existing action / dead end / cheap alternative / reopen condition / classification。

## 4. 七个 survivor 门

候选必须七门全过：

1. 使用不同且 receiver-visible 的 decoder 信息，而非原 selector 特征或 truth；
2. 形成真实闭环动作，不能是一个标量 calibration、离线重排或 post-hoc 评分；
3. 不与 F4-C、P08 LLR calibration、P05 online CMA、CCISP gate 和历史 dead end 碰撞；
4. comparator 在 code、net rate、iteration budget、latency 与信息可见性上公平；
5. testbed 为 `READY` 或总计不超过一天的 `NEEDS_SMALL_ADAPTER`；
6. 实验前已经能写出独立方法流程图、主表和至少一个承重消融；
7. 明确一个可证伪的 baseline failure，而不是“decoder 信息也许有用”。

最多保留 1 个 survivor。若 survivor 存在，只写它回到 GW Step 1 时的 M-C-A 与否决条件；不得写
实现或实验任务。

## 5. 只允许的终态

- `METHOD_SHAPED_SURVIVOR_AVAILABLE`
- `NO_METHOD_SHAPED_SURVIVOR`
- `CODED_CHAIN_ASSET_BLOCKED`

无论哪种终态，都不得创建 active carrier、METHOD_SIGNAL、Go、晋级后的 method card 或论文正文。

## 6. 唯一产出与验收

唯一科学/设计产出：

`projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`

完成后只同步本专题 topic/mission/D/V（若产生新裁决）、worker-log（仅实际执行日志）与必要 current
pointer；不修改 Skill、`common/`、`params.py`、CCISP/coded-chain 代码、正式论文或 dormant campaign。

验收：

- [ ] control epoch 35 / CP022 / D039 绑定并通过 validator；
- [ ] callback readiness 逐 caller→callee 有 `path:line`；
- [ ] 三张卡字段完整、七门逐项裁决；
- [ ] 历史 collision 不靠名字判断；
- [ ] 最多 1 survivor，且只回 GW Step 1；
- [ ] fresh-context verifier 独立检查方法身份、授权范围和 terminal 唯一性；
- [ ] 单次最终 commit，不 push；四个既有 `p05_run*.log` 不修改、不暂存。
