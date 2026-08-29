# Task Brief: C5-5 reliability-prioritized LDPC scheduling/budget 候选级 Groundwork Step 1

> 来源: S028 / D057 / V032 / T041 / T044 / T046 / T077 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step1-authority-reconciliation.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 19
  action_class: C5_5_GW_STEP1_AUTHORITY_RECONCILIATION
  mission_checkpoint: CP019
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在 45 分钟内复用已有本地文献、全文笔记、codec/interface 证据和 C5-0 负结果，完成 C5-5 的候选特定 Groundwork Step 1。必须判断能否形成一个诚实的硕士级问题：在共同 DP-(8,8)-16APSK+BICM/LDPC 接收机中，固定 NMS/OMS 的更新顺序或计算预算没有利用当前码字的 receiver-visible reliability/syndrome/stall 状态，因此能否用 bounded 的 reliability-prioritized scheduling/budget，在公平 edge-update 预算下改善 BER/FER，或在近似 BER/FER 下减少平均/P95 计算量。

本任务只冻结问题、动作链、比较合同、全文缺口和接口门。不得实现、仿真、下载论文、补 decoder adapter、进入 Step 2，亦不得预设候选成立。

## 开始前强制读取

1. 根 `AGENTS.md`、`research-direction-lab` 与 `session-governance` 的相关要求；运行 task-control validator。
2. `stages/groundwork.md` 的 Step 1、`stages/glossary.md` 的问题四判据、`domain-comms.md` 与 `thesis-lessons.md` 速查表/最近三条。
3. `.sessions/2026-07-09-thesis-writing/T041-gw1-ldpc-receiver-authority.md`、T044、T046；如实际文件名不同，按编号定位。
4. `projects/thesis-fso/direction-lab/harvest/ldpc-receiver-authority.md`、`projects/thesis-fso/apsk-soft-receiver-groundwork/step2-coverage-report.md`、现有 Step 3/3.5/4a 报告。
5. `projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md`、`step-076-c5-0-apsk-ldpc-correctness.md`、`step-077-c5-0-single-cell-natural-headroom.md`、`step-118-d0-i04-codec-adapter-fresh-ldpc.md`。
6. 本地有关 adaptive NOMS/OMS、residual/informed scheduling、layered/flooding、early stopping 与 equal-update fairness 的全文或 read notes。先查 `papers/index.json` 和 `papers/_read_notes/`；不得把标题或摘要当全文结论。

## 必须回答的六件事

1. **M-C-A / Q#**：指出一个具体传统方法 `M`、目标条件 `C`、可审计原因 `A`。不能写成“没人做过星地 APSK 上的调度”，也不能仅写“动态比固定先进”。
2. **receiver-visible IAO**：列出 input、action、output 以及明确禁用的 truth。优先审查当前码字 syndrome/unsatisfied checks、posterior 或 message reliability、stall/iteration state；若当前项目接口拿不到，必须判 interface-blocked，而不是假定存在。
3. **方法身份与独立性**：候选必须只改变 LDPC decoder 内部更新顺序、layer/edge priority、提前停止或计算预算；不得改 Ch3 CPR、Ch4 demux、APSK demapper LLR 或重新包装 C5-0/C5-1。
4. **baseline 与廉价替代**：主 baseline 至少是同 BG2/Z/clip/early-stop 下充分调优的 fixed NMS/OMS；必须列 equal-edge-update 的额外固定迭代、标准 flooding/layered schedule、静态 per-iteration alpha/beta LUT。已知这些替代会限制 claim ceiling，但 Step 1 不因强邻居自动否决迁移型方法。
5. **全文与 collision ledger**：区分 exact collision、primitive、related、background；确认至少一个可执行调度/预算原子和一个正确 fixed decoder authority 已有全文。缺口只能留给 Step 2，不能在本任务下载补齐。
6. **接口与时限门**：审计本地 Sionna 2.0.1 与项目 adapter 已证实的 `cn_schedule`、`num_iter`、callback、state、soft/hard output能力；把“库可能支持”与“项目 seam 已可用”分开。若最小合法动作需要自写整套 BP decoder、不可控内部 patch 或预计超过硕士三月窗口，直接记录 blocker。

## 首选候选 recipe 仅作待证假设

- input：同一 codeword 的 receiver-visible channel/posterior reliability、unsatisfied-check 或 stall 状态；
- action：在固定总 CN/VN edge-update 预算内，优先更新与不满足校验和低可靠变量相邻的 layer/edge，或将剩余预算分配给高风险码字；
- output：decoded bits、syndrome/stop reason、总 edge updates、平均/P95 latency；
- comparator：tuned fixed NMS/OMS + 相同 early-stop 和相同 edge-update 预算；
- claim ceiling：经典调度/复杂度控制在本共同星地 APSK 接收链上的 bounded migration/extension，不声称首创调度、SOTA 或全面领先。

必须用本地证据验证、改写或否决该假设；不得因 brief 给出 recipe 就宣布 Step 1 PASS。

## Terminal

1. `STEP1_C5_5_PASS_READY_FOR_STEP2`：问题四判据、receiver-visible IAO、正确 baseline/cheap alternatives、至少一个全文方法原子、最小接口路径均闭合；只授权主控另派 Step 2。
2. `STEP1_C5_5_EVIDENCE_GAP_BOUNDED`：M-C-A/IAO/接口原则上合法，但缺少可定位的直接全文或库/API authority；列最多三个精确缺口及 Step 2 的 bounded 获取问题，不实现、不仿真。
3. `STEP1_C5_5_NO_LEGAL_Q`：问题被 fixed/layered/extra-iteration 等价吸收，receiver-visible 原因不存在，或只能靠“场景不同”命名而没有动作链差异；关闭该形态。
4. `STEP1_C5_5_INTERFACE_OR_TIME_BLOCKED`：科学问题可能成立，但当前最小动作需不可见 decoder state、自写整套 decoder 或超出三月窗口；不得用工程开洞替代 Step 1 成立。

## 交付与停机

- 主报告：`projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step1-authority-reconciliation.md`。
- worker log：`projects/thesis-fso/worker-logs/step-078-c5-5-gw1-authority-reconciliation.md`。
- 仅在 canonical Step 1 tracking 确有需要时更新 `projects/thesis-fso/literature_notes_apsk_soft_receiver.md`；不改 `.sessions/`、Skill/controller、仿真代码、论文正文或任何旧结果。
- 报告必须 facts-first，包含证据指针、Q#/IAO、collision/absorption、baseline/fairness、interface audit、UNKNOWN、terminal 和唯一下一步。
- 45 分钟硬停；运行 task-control validator、路径白名单与 `git diff --check`；一次 commit、不 push。若证据不够，交付 bounded gap，不自行进入 Step 2。
