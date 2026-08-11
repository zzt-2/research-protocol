# Task Brief: D0 I02 immutable views and CP012 action guard (TDD)

> 来源: step-110 PASS / d0-implementation-plan I02 / step-106 CV04–CV05、CV09 | 产出位置: `projects/thesis-fso/worker-logs/step-111-d0-i02-immutable-views-action-guard.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：在保持 I01 3/3 的前提下，可用 deep-frozen value types、显式 Receiver whitelist/recursive truth denylist 和 deny-by-default action registry 闭合 CV04/CV05/CV09，而不提前伪造 CV06–CV08 的跨组件证明。
- 否决条件：Receiver 必须携带 Truth/tx/physical SNR/true phase/fade/event/correctness；dataclass frozen 但内部 ndarray/mapping 仍可变；action 由模糊前缀或当前 owner 单一 action_class 放行；需改 owner/其他模块；或 15 分钟内不能形成有效 RED/GREEN，则写 `INCOMPLETE` 停止。

## 冻结输入

```text
contract.py(I01)=a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775
test(I01)=3d411c35be5ed01e007c92ea6a4488e200eb3053203ef56915cf9eed597ef9e1
step-109=c85d1a2e2fd52750519a3cf8bf48c869fa4e9f5614ea53f546aa46ca0c0d430b
step-110=efbb860af0711228e9e15f5918ab16e0071d51f0e7bdb19eeb3d0ed4f91f8760
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/explore/coded-decoder-feedback/contract.py`
2. Modify `projects/simulation/tests/test_d0_contract_views.py`
3. Create `projects/thesis-fso/worker-logs/step-111-d0-i02-immutable-views-action-guard.md`

## Test-first scope

1. 完整读取 T065、plan I02、step-106 CV04/05/09、step-105 contract interface、owner views/control/H004、I01 candidate 与 step-109/110。核 hash/protection。
2. **先只追加测试**，不要先改 production。保留 I01 三 tests。新增名称必须恰为：
   - `test_receiver_truth_frozen_disjoint`（CV04）：`ReceiverView`/`TruthView`/`WaveformLayout`/`CostLedger`/`ResolvedDevFreeze` 为 frozen+slots value types；Receiver 与 Truth 字段集合不交叉；构造后修改 source ndarray/list/dict 不改变 stored bytes/value；stored ndarray `writeable=False`，nested mappings/sequences 不可变；receiver categories 只含 received/equalized samples、common CPR trace、known prefix/pilots、receiver noise estimate、frozen code/waveform/B2 parameters与非truth receipts。
   - `test_receiver_rejects_truth_and_extra_fields`（CV05）：dataclass extra kwargs 拒绝；Receiver 任意 nested mapping/dataclass key 命中 `truth/tx_payload/information_bits/coded_bits/transmitted_symbols/true_phase/h/snr/fade/slip/event_label/correctness` 等明确 truth aliases 均 fail closed；`common_cpr_phase_trace` 与 source/code/content SHA 名称不得被误杀。
   - `test_scientific_actions_disabled_cp012`（CV09）：public deterministic action-set API 返回恰五个工程类 `D0_TESTBED_IMPLEMENTATION/D0_UNIT_TEST/ENGINEERING_THROUGHPUT_BENCHMARK/SOURCE_AUDIT/CONTRACT_STATIC_CHECK`；DEFECT_SMOKE、S1/S2/S3dev/S3test/S4、C1、MVE、heldout、Contract/Execute 及 unknown 全拒绝；CP/epoch/D/V 或 permission flag mutation 后相应 action fail closed。
3. RED 必须是这三个 exact nodes 的目标 assertion/`NotImplementedError`，不可用 missing import name 导致 collection error。可 `import contract as module` 后断言 public types/API 尚缺。production 修改前立即把 test SHA、old production SHA、exact command/output SHA与目标 failure原文写入 step-111。
4. 最小 GREEN：
   - 添加上述五种 public value types；数组做 defensive copy 后只读，mapping/list/set recursive freeze；Receiver 构造时递归审 key/field aliases；Truth 独立且 evaluator-only data 不得嵌入 Receiver。
   - 类型字段应足以支持后续 waveform/channel/receiver/freeze，但本切片只实现 immutable/validation contract，不实现 waveform/channel/fit/evaluator。
   - 添加 public `authorized_action_classes(contract) -> frozenset[str]`（或等价显式 API）；只依 frozen CP012 identity/booleans，绝不依字符串前缀/substring；保留 I01 `assert_action_authorized` 兼容。
   - 不创建 CV06 truth-mutation receiver result、CV07 production signature scan、CV08 evaluator freeze binding；这些仍留 I17A。
5. 不改 tests，跑新增 exact nodes GREEN，再跑完整文件（应 6 tests）。记录 RED/GREEN/whole-file receipts、source/test SHA、无 skip/xfail/warning。
6. 终检 no import-I/O/sys.path mutation/runner/science；只三目标变化；p05/cache/staging/HEAD保护；不 commit/push。

## 命令/边界

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact nodes or file> -q
```

Windows Python only；禁止 benchmark/science、web/search/download、自动安装、隐式 skip。目标 10 分钟，15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；I01 regression 3/3 + CV04/05/09 RED/GREEN；三目标 SHA；保护 receipt；终态只可 `I02_READY_FOR_INDEPENDENT_VERIFICATION` 或 named blocker。
