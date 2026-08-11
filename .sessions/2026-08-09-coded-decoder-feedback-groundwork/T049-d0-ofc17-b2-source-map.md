# Task Brief: D0 OFC2017 B2 原文与 16QAM 迁移映射

> 来源: D010 / V004 / H003 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-095-d0-ofc17-b2-source-map.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: SOURCE_AUDIT
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## 目标

对子 agent 必读全文 `papers/doi/10.1364_ofc.2017.w2a.56/7937400.md` 做 source-native 算法映射，区分原文事实、合同已冻结外推与尚缺实现细节，判断 `OFC17_16QAM_EXTFRAME_V1` 是否能在 D0 预算内唯一实现。不得写源码、不得跑 D0。

## 必读

- `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md`
- `projects/thesis-fso/worker-logs/step-081-c1-ofc2017-slip-state-fulltext.md`
- `papers/doi/10.1364_ofc.2017.w2a.56/7937400.md`（必须完整读）
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_coded_chain.py` 的 16QAM constellation/demapper
- `毕设/formulas-master.md` BPS/相位模糊相关公式、`projects/simulation/params.py` BPS 参数来源字段

## 必答

1. 原文对 `L=31`、`p_s`、`sigma_e^2`、`q=1-sqrt(1-p_s)`、4-state transition、M nearest pilots、tuple `(M,N)`、pilot placement、one-way FEC/no feedback 的精确证据与公式/段落行号。
2. 合同五个 tuple 与 pilot count `684/325/64/32` 是否内部一致；terminal pilot 与 extended-frame/no-puncture 需要怎样的精确时间索引。
3. 给可直接编码的 4-state transition、pilot emission、distance propagation、log-domain normalization、square-16QAM mixture LLR 数学定义；LLR sign 必须对齐 P08。
4. 列出所有 `[原文] / [合同外推] / [实现选择]`，判断是否存在无法唯一实现、必须重开合同或超过 2.00 日 B2 adaptation 的 hard blocker。
5. 给 B2 单测/identity/metamorphic/source-receipt 清单；尤其 `p_s=0`、`sigma_e2=0`、state permutation、single-state collapse、no feedback、one decode。
6. 明确 `SOURCE_READY / SOURCE_READY_WITH_NAMED_IMPLEMENTATION_CHOICES / >7D_HARD_BLOCKER` verdict。

## 约束与产出

- 只写 `projects/thesis-fso/worker-logs/step-095-d0-ofc17-b2-source-map.md`。
- 不修改任何既有文件，不创建源码/测试/结果，不运行仿真、pytest 或 import probe。
- 不使用 web/search/download；全文只读本地 content；不 commit/push，不触碰 p05。
- 12 分钟目标，15 分钟硬上限。

