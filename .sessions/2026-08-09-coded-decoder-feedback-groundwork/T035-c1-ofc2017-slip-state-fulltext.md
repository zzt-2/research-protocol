# Task Brief: C1 Step 3.5 round-3 OFC 2017 新候选全文裁决

> 来源: S001 / D008 / T034 | 产出位置: `papers/_read_notes/10.1364_ofc.2017.w2a.56.md` + `projects/thesis-fso/worker-logs/step-081-c1-ofc2017-slip-state-fulltext.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 9
  action_class: FULLTEXT_READ
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

获取并精读 DOI `10.1364/OFC.2017.W2A.56`。第三轮 publisher abstract 仅支持 pilot 上的 soft-decision slip-state estimation 与 parallel recovery；全文必须裁它是否包含 decoder evidence、explicit boundary/range、有限局部载波动作、选择性重解码、clean/fallback 和有界成本的完整链。

## 1. 纪律

1. 先读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、topic-index/D008、T034 与 step-070/075/079；fresh task-control validator PASS 后执行。
2. 用 `tools/download --doi` / `tools/blit` 与最多三条合法 acquisition channel；设置 `PYTHONDONTWRITEBYTECODE=1`。PDF 转 markdown 必须走 `tools/convert`；需目视 QA PDF 身份和页面完整性。
3. 只做该篇 identity/acquisition/fulltext/collision；不搜索新论文、不改中央 owner/治理/代码、不实验、不提交/push、不触碰 p05；hard cap 15 分钟。获取失败也必须以三通道 receipt 和 `UNRESOLVED_FULLTEXT` 收口。

## 2. 必答

- `soft-decision slip-state estimation` 的 input 是 pilots、DD symbols、FEC decoder LLR/extrinsic 还是 transmitter truth；
- slip state 是否输出显式 onset/boundary、持续 range 与相位方向，还是仅全流 hidden state；
- `parallel recovery` 的候选数量、作用粒度、是否旋转/重映射局部 samples、是否重跑 decoder；
- trigger、clean/no-slip no-op、failure fallback、复杂度/latency/decode-call budget、最终 output；
- 与 PAPU/CSSC/CS-DC、OFC2014 Markov turbo、OFC2015 HTDD/SC-LDPC/arXiv1704 的 identity/机制关系；
- 八字段完整签名及 `EXACT_COMPLETE_CHAIN` / `PARTIAL_CORE_ONLY` / `STRONG_NEIGHBOR` / `NOT_COMPARABLE` / `UNRESOLVED_FULLTEXT` verdict。

## 3. 产出

- read note：`papers/_read_notes/10.1364_ofc.2017.w2a.56.md`
- worker log：`projects/thesis-fso/worker-logs/step-081-c1-ofc2017-slip-state-fulltext.md`

worker log 含 acquisition/quality、≤10条全文事实、八字段、collision、claim ceiling、round-3 debt disposition、p05 4/4 hash/staging-empty。Terminal：`FULLTEXT_READ_NO_EXACT` / `EXACT_COMPLETE_CHAIN_CONFIRMED` / `UNRESOLVED_FULLTEXT`。聊天只回 terminal、机制、collision、路径；≤550 字。
