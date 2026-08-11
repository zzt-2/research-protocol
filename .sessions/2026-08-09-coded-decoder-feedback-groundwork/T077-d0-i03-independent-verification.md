# Task Brief: D0 I03 independent waveform verification

> 来源: step-121 executor PASS / frozen waveform source+test | 产出位置: `projects/thesis-fso/worker-logs/step-123-d0-i03-independent-verification.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_UNIT_TEST
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## 审查问题 / fail 条件

- 问题：独立上下文能否证明 I03 注册 bytes、pilot schedule、6144 bijection、immutability 和 controlled suffix 语义对完整 owner domain 成立，而不是只匹配四个示例？
- FAIL：任何 P0/P1；注册 asset 非 source-generated；import 消耗 global RNG/做 I/O；array 可变或 alias；任一 N/boundary/pol/k 失配；known/sentinel/maps 被污染；无效输入 fail-open；或 fresh tests 不全 GREEN。

## 冻结输入

```text
waveform.py=bab2a491e0afb1b32b188ea0ce1465b9b6fe2a1ee08593c2c2544c1fe3c2b748
test=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
step-117=9dd643651980c812ae7ef1dd4852faf1849b7b5043656b1d4106deb97b936bbb
step-121=b269ea2973b888a0bd8edfa9de5b945e038449eddfdba70e0f924a4d0481356a
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

Create only `projects/thesis-fso/worker-logs/step-123-d0-i03-independent-verification.md`。production/tests/logs 只读；不得修复。

## 独立验证

1. 核冻结 SHA/保护；读 owner、step-094/105/106、source/test/log。findings-first，P0/P1/P2 分级，不采信 executor 自证。
2. fresh import probe：import 前后 global `np.random`/filesystem/cache/module census；不得消费 global RNG、加载 runner/legacy、I/O 或 path mutation。
3. fresh 跑四 exact nodes、完整 waveform 文件和 I02 contract 回归，记录 command/count/duration/output SHA/skip/xfail/warning。
4. 临时 one-shot negative/metamorphic matrix（不落 repo 文件），至少：
   - prefix/pilot repeated calls byte-identical、返回 arrays defensive/read-only；注册 hash 从 bytes 实算，source 不含 expected SHA shortcut；
   - N=10/20/100/200 全 schedule：prefix32、6144 data、first+periodic+terminal pilots、counts/lengths、time/data inverse、known=-1、terminal known；从 waveform 反取 data 与输入逐字节一致；
   - invalid N/type、data shape/object/nonfinite 拒绝；构造后修改 source data 不影响 build；
   - target_pol 2 × boundaries 3 × k 4 =24 cases：pre-boundary/base/clean-pol/maps/known byte identity，目标 suffix（含所有 later pilots和terminal）精确乘 integer rotation；k0 仍 copy-on-write；
   - invalid pol/boundary/k/type/build 拒绝；检查 dataclass frozen+slots 及 nested ndarray read-only。若 public constructor 可生成内部不一致、后续导致 fail-open，按 owner reachability 判级并给复现。
5. 静态扫描 import-I/O/global RNG、in-place mutation、hash hardcode、float-state/exp drift、terminal pilot遗漏。每 finding 必须有 owner oracle+复现。
6. 终检只 step-123 新增；p05/cache/staging/HEAD 不变；不 benchmark/science/web/install/commit/push。≤15 分钟，不足则 INCOMPLETE。

## 返回

P0/P1/P2 counts；fresh unit/negative counts；log SHA；terminal=`I03_VERIFIED_READY_FOR_BATCH1`、`I03_VERIFICATION_FAIL` 或 `INCOMPLETE`。
