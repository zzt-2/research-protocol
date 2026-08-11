# Task Brief: D0 I03 registered waveform assets and data/time maps (TDD)

> 来源: step-116 PASS / d0-implementation-plan I03 / step-106 WC01–WC03、WC08 | 产出位置: `projects/thesis-fso/worker-logs/step-117-d0-i03-registered-waveform-assets.md`
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

- 假设：owner 注册的 Gray-16QAM prefix、pilot cycle/expansion、6144 data-rank 映射和 persistent four-state suffix 旋转，可由无 I/O、无 RNG 隐式状态的 `waveform.py` 精确实现，并由 WC01–WC03/WC08 先 RED 后 GREEN。
- 否决条件：任一注册 bytes/SHA/count 只能近似匹配；known positions 不能保持 `-1`；controlled jump 会改写 base/pre-boundary/sentinel；suffix 未覆盖后续 pilots；需改 owner/contract/其他模块；或 15 分钟仍无有效 RED/GREEN receipt，则写 `INCOMPLETE` 停止，不得扩大范围。

## 冻结输入

```text
contract.py(I02)=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_contract(I02)=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-116=6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Create `projects/simulation/explore/coded-decoder-feedback/waveform.py`
2. Create `projects/simulation/tests/test_d0_waveform_channel.py`
3. Create `projects/thesis-fso/worker-logs/step-117-d0-i03-registered-waveform-assets.md`

不得修改 `contract.py`、owner、plan、其他 tests；不得创建 runner/artifact/result/cache/`__init__.py`。

## TDD 任务

1. 完整读取 T071、plan I03、step-106 WC01–03/WC08、step-105 waveform interface、step-094 asset map、owner waveform/pilot/jump contract、I02 candidate 与 step-116。先核冻结 hash、branch/HEAD/staging、p05 4/4、三目标初态和 cache census。
2. **先创建测试，不写 production**；测试名必须恰为：
   - `test_registered_prefix_bytes_hashes`（WC01）：`PCG64(987654321)`；bits/labels/symbols/even/odd SHA 分别为 `1168a4cce1eef1403b4c609f0d2d15541ffd1cdfd175ca809da6701ad81c6d85`、`31c73fa861c3c9f27bbcb0d8cfcba7fcfccfc59f5e12429946d3720e196616b0`、`69989be842342bf388cf2603be0a260f637da876dc912ed74deaed22ff9123c0`、`81350b996fcc3f6ef91b05b83957c85b182f4df6bf1e31be48a0f31cca89a4bc`、`436cdb61597776f8dc045b0d8465265a3978ca089cdf41f1b50893a86a7e062a`；energy exact `1.025`。
   - `test_registered_pilot_hashes_counts`（WC02）：cycle SHA `db860e05d78202f159e28f16fbe26c8e060fc8c65c4b872c8bb3f7fc5915071e`；N=10/20/100/200 expanded SHA=`2c58efb90b9b4a82b676db4e219f21094cc0a546f54c126b1010764fc68375bd`/`1d14610847c0023475cb03ff7a932fddc1202f02c2a7ca4c25d0fb544504af82`/`17bdb8755470902084e9f1331fb6e36633332f9e2392a7d247e061ec1b0a810c`/`0d515c32e1447d3d8b1a55d367b53feacafbee792989697fd4114161ca2357d4`；pilot counts=684/325/64/32，total symbols=6860/6501/6240/6208。
   - `test_data_time_map_bijective`（WC03）：6144 ranks 各出现一次；known=`-1`；codeword boundaries=1536/3072/4608；terminal/suffix pilots 不得漏映射。
   - `test_controlled_jump_copy_on_write`（WC08）：双偏振；target boundary 后含 pilots 的 persistent suffix 做 integer-only π/2 state rotation；base、pre-boundary 与 sentinel byte-identical。
3. 测试仅把 D0 root 加入 `sys.path`。运行四个 exact nodes，取得有效 RED（首次 module absent 可接受；syntax/fixture/path/collection/dependency error 不接受）。在创建 `waveform.py` **之前**将 exact command/cwd/env、exit code、test SHA、production ABSENT、原始输出 SHA 和关键 failure 原文写入 step-117。
4. 最小实现 registered assets、`build_waveform`、`data_to_time`/`time_to_data` 与 four-state rotation；所有 hash 必须来自规范化 ndarray bytes，不得硬编码“预期 SHA 后直接返回”；无 import-I/O、无 global RNG、无 channel/receiver/codec/science 逻辑。
5. 不改 tests，以同一 exact nodes 取得 GREEN，再跑完整新文件与现有 `test_d0_contract_views.py` 回归。记录 source/test/owner SHA、exact output SHA、counts/duration；无 skip/xfail/warning 隐藏。
6. 终检只三目标变化；staging=0、HEAD 不变、无 commit/push；无新 `.pyc`/`.pytest_cache`；p05 四日志 hash 逐一不变。

## 环境与命令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact nodes or file> -q
```

禁止 WSL Python、安装依赖、benchmark/scientific seed、web/search/download。目标 10 分钟，15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；WC01–03/WC08 RED/GREEN counts；三文件 SHA；唯一写入/protection receipt；terminal 只能是 `I03_READY_FOR_INDEPENDENT_VERIFICATION` 或 named blocker。
