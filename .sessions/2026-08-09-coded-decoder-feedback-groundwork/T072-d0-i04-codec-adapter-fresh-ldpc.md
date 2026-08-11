# Task Brief: D0 I04 codec adapter, Gray mapping and fresh LDPC (TDD)

> 来源: step-116 PASS / d0-implementation-plan I04 / step-106 RM07–RM10 | 产出位置: `projects/thesis-fso/worker-logs/step-118-d0-i04-codec-adapter-fresh-ldpc.md`
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

- 假设：以 Windows Sionna 2.0.1 的 live LDPC5G API 为唯一运行实现、以 P08-R2 为 source-bound 语义参考，可在无旧模块 runtime import、无 decoder warm/message state 复用下闭合 RM07–RM10。
- 否决条件：需要 runtime import `p08*_chain.py`/run scripts；正 LLR 语义无法证明为 bit=1；无法取得 live BG/Z/interleaver receipt；每次 decode 不能 fresh state；只能 skip/private-metadata 猜测；需改 owner/contract/其他模块；或 15 分钟到期仍未完成当前 RM test-ID，则在最近一个完整 test-ID 边界写 `INCOMPLETE` 停止，不得扩展范围。

## 冻结输入

```text
contract.py(I02)=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_contract(I02)=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-116=6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
p08r_chain(source)=174daad20f4fadbb0710cdee5faf7d49f360b6a8a6609b9a1ea46ccb41288404
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Create `projects/simulation/explore/coded-decoder-feedback/codec.py`
2. Create `projects/simulation/tests/test_d0_receiver_codec_methods.py`
3. Create `projects/thesis-fso/worker-logs/step-118-d0-i04-codec-adapter-fresh-ldpc.md`

不得修改 `contract.py`、P08/P08-R/P08-R2、owner、plan 或其他 tests；不得创建 runner/artifact/result/cache/`__init__.py`。

## TDD 任务

1. 完整读取 T072、plan I04、step-106 RM07–RM10、step-105 codec interface、step-094 coded-chain asset map、owner codec/B1 contract、P08-R2 source 与 I02/step-116。核冻结 hash、Windows Python 3.11/Sionna 2.0.1 live imports、branch/HEAD/staging、p05 4/4、三目标初态和 cache census。旧源码只能读取并在新模块 source-bind，禁止 runtime import（它们有 `sys.path`/执行副作用）。
2. **先创建测试，不写 production**，按以下顺序，每完成一个 test-ID 再继续：
   - `test_gray16_roundtrip_rotation`（RM07）：16 labels 按 `[b0,b1,b2,b3]` roundtrip；axis `[-3,-1,3,1]/sqrt(10)`；四个 π/2 coordinate rotations 与 integer states 精确对应。
   - `test_ldpc_noiseless_roundtrip_one_cw`（RM08）：固定 1024 information bits → 1536 coded bits → 无噪声 decode 原 bits；禁止 truth correction；记录 live Sionna version、BG/Z/interleaver receipt，metadata 不符显式 FAIL。
   - `test_every_decode_fresh_state`（RM09）：counting factory；每次 call 都从 fresh empty message/warm state 开始；B1 frame=8 batches、B2=2；故意 reuse tripwire 必须失败；decoder object 可缓存但 state 不得缓存；receipt 含 CW batch、restart、`20*CW` BP iterations。
   - `test_b1_exact_reencode_nll`（RM10）：fresh hard decode 后 exact re-encode；mean `softplus((1-2*c_hat)*L)`，same-bit denominator；positive LLR means bit=1；preclip 30 → decoder clamp 20；fixed 20 iterations；`complex_noise_power/2` 仅转换一次。
3. 首轮可一次写四 tests，或严格按 RM07→08→09→10 增量；但 `codec.py` 创建前必须至少有四 exact-node 的有效 RED receipt（module absent 可接受；syntax/fixture/path/collection/dependency error 不接受），并立即把 exact command/cwd/env、exit code、test SHA、production ABSENT、output SHA 与关键 failure 原文写入 step-118。
4. 最小实现须 lazy construct Sionna；import `codec.py` 不得创建 encoder/decoder、读写文件或改 global path。source-bound 实现 Gray map/max-log/LDPC adapter，不复制运行时旧模块对象。环境/API/private metadata 不符必须 fail closed，不得 skip/fallback 到伪 codec。候选正序/反序 bit-identical。
5. 不改 tests，跑 exact nodes GREEN；再跑完整新文件及 `test_d0_contract_views.py` 回归。记录 RED/GREEN receipts、source/test/owner/P08-R2 SHA、环境 metadata、无 skip/xfail/warning。
6. 到 12 分钟评估剩余工作；预计越过 15 分钟则在最近完整 RM ID 边界写 `INCOMPLETE`，清楚列明 DONE/PENDING，不做仓促宽松实现。终检只三目标变化；p05/cache/staging/HEAD保护；不 commit/push。

## 环境与命令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact nodes or file> -q
```

Windows Python only；禁止 WSL Python、安装依赖、benchmark/scientific seed、web/search/download、隐式 skip。15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；RM07–RM10 每项 RED/GREEN 状态与 counts；三文件 SHA；live Sionna metadata/protection receipt；terminal 只能是 `I04_READY_FOR_INDEPENDENT_VERIFICATION`、`I04_INCOMPLETE_AT_RMxx` 或 named blocker。
