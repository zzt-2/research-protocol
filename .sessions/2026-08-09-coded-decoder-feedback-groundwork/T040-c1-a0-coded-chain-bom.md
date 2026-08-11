# Task Brief: C1 Step 4a A0 P08-R2 coded-chain / observability / BOM audit

> 来源: S001 / D009 / H002 | 产出位置: `projects/thesis-fso/worker-logs/step-086-c1-a0-coded-chain-bom.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 10
  action_class: SOURCE_AUDIT
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

Fresh 只读审计 corrected P08-R2 源码和已安装 decoder API，判断 receiver-visible decoder evidence 能否按 segment/boundary 定位、最小 callback/local-repair adapter 的真实接口与 3–7 日 BOM。不得继承 step-061 的结论，必须回到源码复核。

## 1. 必答

1. 列 caller→callee 文件、函数签名、数组 shape/dtype、codeword/bit/symbol/interleaver mapping、decode次数和当前 soft/hard/state返回语义。
2. 明确可直接复用的 soft LLR、syndrome/parity、message state、iteration override、callback/re-encode likelihood primitive；缺失的 carrier/slip/action/rollback primitive逐项列出。
3. 判断 contiguous received-symbol segment 能否映射为局部 codeword/parity evidence；若 interleaver打散，给最小合法 localization metric（例如 touched-codeword likelihood/parity ownership）及不能声称的粒度。
4. 给 trigger→boundary candidates→local/suffix rotation/remap→bounded decode/re-evaluate→clean no-op→B1/B2 fallback 的最小接口图；逐字段标现成/薄adapter/新testbed。
5. 做 caller→callee truth denylist：TX payload、true phase/CFO/h/SNR/slip boundary、oracle correction/final correctness不得进入 deployable path；指出任何现有函数可能泄漏的位置。
6. 以 0.25 日粒度重新估计 BOM、依赖、测试与风险；给 `>7D_BLOCKER` 判据、可复用产物与最小缩减方案。不得为了过预算删 identity/truth/cost test。

## 2. 产出

写 step-086：source inventory、interface/mapping表、observability verdict、truth audit、最小BOM与hard blocker。只读；不得 web/下载/改中央/代码/pyc/实验/提交/push/触碰p05。hard cap 15分钟，fresh p05/staging 后收口。
