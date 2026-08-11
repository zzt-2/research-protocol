# Task Brief: C1 Step 4a A0 理论 headroom / 物理 factorization

> 来源: S001 / D009 / H002 | 产出位置: `projects/thesis-fso/worker-logs/step-085-c1-a0-theory-headroom.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 10
  action_class: THEORETICAL_BOUND
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

只做 A0 解析预检：用 C1 reference M、实际 P08-R2 调制/映射/交织源码与本地物理全文，推导单个 within-frame symmetry slip 下 global one-shot B1 的不可消除误差、O1 上界和可证伪理论预期。禁止运行 Monte Carlo/仿真或写代码文件。

## 1. 必答

1. 从源码确认实际 constellation/Gray mapping、coded-bit→symbol 与 on-air interleaver；不得假设 QPSK。
2. 对允许的 symmetry phase jump（实际调制）做有限枚举/纸笔推导：在无噪声、boundary fraction `α` 下，单一 global rotation 的最小残余 symbol/bit error是多少；local truth correction 的上界是什么。可用一次性 shell expression 做有限代数核对，但不得生成 scientific rows。
3. 推导 B0/B1/O1 的趋势、相对排序、boundary-position dependence 与至少 3 个 TL-20 异常锚点；说明 FEC 可能改变 FER、不能由 uncoded bound直接给 coded增益。
4. 审查 on-air interleaver/多 codeword mapping 是否把 contiguous slip 扩散到多个 decoder component，从而削弱或否定“per-segment decoder localization”。这是致命候选，必须 fail-closed。
5. 把 JLT2020 FSO fading/AO/CFO 参数与 OFC/ICTON injected discrete slip 分成正交因素；给最小 factorized testbed 草案和每个参数的本地来源/transfer ceiling。
6. 给 A0 §1 的来源类型标签（实证/外推/论证）、FR-21 可解析上界是否适用、以及明确 kill conditions；禁止把 oracle 上界当 Go 判据。

## 2. 产出

写 step-085：源码证据路径/行号、推导公式、有限映射表、headroom/趋势、interleaver影响、physical factorization、理论预期与 kill条件。只读；不得 web/下载/改中央/代码/pyc/实验/提交/push/触碰p05。hard cap 15分钟，fresh p05/staging 后收口。
