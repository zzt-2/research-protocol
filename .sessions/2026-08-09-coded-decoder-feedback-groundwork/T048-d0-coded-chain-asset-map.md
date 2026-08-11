# Task Brief: D0 coded-chain 与公共 API 资产映射

> 来源: D010 / V004 / H003 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-094-d0-coded-chain-asset-map.md`
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

只读映射 D0 可复用的 P08-R2 coded chain、16QAM BPS、双偏振信道、结果保存与 pytest 接口，给出精确到函数/类/路径的实现 BOM。不得写源码、不得运行 D0 或科学实验。

## 必读

- `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- `projects/thesis-fso/worker-logs/step-086-c1-a0-coded-chain-bom.md`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_coded_chain.py`
- `p08r_chain.py`、`p08r2_chain.py`、`p08r2_phaseA.py`、`p08r2_run.py`、`p08r2_verify.py`、`p08r2_metamorphic_gate.py`
- `projects/simulation/common/_dual_pol_channel.py`、`_equalizer.py`、`_modulation.py`、`_recovery.py`、`_experiment.py`
- 相关 `projects/simulation/tests/` 测试模式

## 必答

1. 可直接复用、需包裹、必须新写的对象分别是什么；列 exact signatures、信息边界与依赖。
2. 如何在不修改 `common/` 的前提下建立 `ReceiverView`/`TruthView`、pilot-extended waveform、合法 4-state rotation、persistent boundary、16 CW/pol 的 ownership 与 full decoder restart。
3. P08-R2 interleaver、LLR sign、decode API、CW/symbol 映射、source receipt 的精确事实；禁止 `resolve_qam16` 的替代路径。
4. square-16QAM BPS API 是否支持 `B={32,64}`、`Nw={31,61,127}`；指出任何和 `CONCLUSIONS.md` 旧结论冲突的代码事实，但不要改文档。
5. 建议的新文件/测试文件责任边界与最小 TDD 次序；每项给可独立审查的 deliverable。
6. 预判导入、设备、Sionna、运行时间、缓存/pycache、结果写出风险；给 fail-fast 静态/单测门。

## 约束与产出

- 只写 `projects/thesis-fso/worker-logs/step-094-d0-coded-chain-asset-map.md`。
- 不修改任何既有文件，不创建源码/测试/结果，不运行 pytest/import probe（避免 pycache）或仿真。
- 不使用 web/search/download，不 commit/push，不触碰 p05 日志。
- 结论分 `REUSE_AS_IS / WRAP_ONLY / NEW_D0_CODE / BLOCKER`，附路径与行号。
- 12 分钟目标，15 分钟硬上限。

