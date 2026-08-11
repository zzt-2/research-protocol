# step-126 — D0 I04 P1 repair（late RED receipt process deviation）

> 2026-08-10 | executor: `/root/i04_codec` | task: T080
> Status: **INCOMPLETE / PROCESS_DEVIATION**

## 1. Terminal

```text
STATUS=INCOMPLETE
TERMINAL=I04_REPAIR_PROCESS_DEVIATION_LATE_RED_RECEIPT
PROCESS_DEVIATION=RED_WAS_ACTUALLY_RUN_BEFORE_PRODUCTION_BUT_STEP126_RECEIPT_WAS_NOT_PERSISTED_BEFORE_PRODUCTION
READY_FOR_REVERIFICATION=NO
```

三条 RED 的实际执行时序是真实 test-first，但 executor 在 production 修改前没有先创建本日志。
因此本文件**不得**被描述为 `receipt-before-production`；它是事后如实封存原始工具输出身份。
主线程发现门控遗漏后，executor 立即停止进一步源码/测试改动与完整回归。

## 2. Actual chronology

1. 冻结输入核验：
   - old test SHA=`38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef`
   - old codec SHA=`1f03b278054cb380c73b98e5211c0c5a37b41d2c47d5966f50bc5803d4e74dcb`
   - step-122 SHA=`2517832d5d31a84ff251bc1520e58b21b49143b825c655c28b23986130064247`
   - step-120 SHA=`1b79aad9be86027d6fef91ad9e9a3931bce0bf53aa7e6cbd86f8f9a1c13ab1b4`
   - HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`；staging=`0`；step-126=`ABSENT`
2. 只修改 test，追加三条 T080 exact regressions。主线程观测 test mtime=`16:24:42`。
3. production 仍为 old SHA `1f03...74dcb` 时，逐节点实际运行三条 RED；见 §3。
4. **门控遗漏**：此时没有创建 step-126，故没有 production-before 的持久化 receipt。
5. 随后最小修改 `codec.py`；主线程观测 codec mtime=`16:25:25`，新 SHA见 §4。
6. 三条新节点逐项 GREEN；见 §5。
7. 主线程指出 receipt 持久化门遗漏；executor 停止，不再跑 RM07–10/full/I02/import/protection 终检。

## 3. Genuine RED executions, persisted late

RED common facts:

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
flags=-B -m pytest -p no:cacheprovider
new_test_sha256=4045a68843400518c999db836533528c1452af9c5f8b9e940c2fd24b24b90348
production_sha256_at_every_RED=1f03b278054cb380c73b98e5211c0c5a37b41d2c47d5966f50bc5803d4e74dcb
step126_at_every_RED=ABSENT
```

| exact node | exit | wall | output SHA256 | key raw failure |
|---|---:|---:|---|---|
| `test_codec_rejects_wrong_contract_identity` | 1 | 0.752s | `da2ebc9914c4f81c2729bc223d1019611b55e5e34006d98b7235ba6537e555a9` | `Failed: DID NOT RAISE any of (TypeError, ValueError, PermissionError)` |
| `test_codec_rejects_nonbinary_backend_output` | 1 | 0.746s | `0d8d9d7bdce878abec5591c56a8602809743f65b84c37824b523d402206e91a8` | `Failed: DID NOT RAISE any of (TypeError, ValueError, RuntimeError)` |
| `test_codec_rejects_boolean_noise_power` | 1 | 0.720s | `13812bb081e75da3cfd60cbde84daa8885279f78d05c7f83f68345bc50c8fb20` | `Failed: DID NOT RAISE any of (TypeError, ValueError)` |

Exact command instantiated per node:

```powershell
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_receiver_codec_methods.py::<node> -q
```

这些输出证明测试在 old production 上确实 RED；但由于当时 step-126 不存在，只能由后续独立
verifier 判断其证据可接受性，executor 不自行升级。

## 4. Minimal production delta already made before stop

```text
test_sha256=4045a68843400518c999db836533528c1452af9c5f8b9e940c2fd24b24b90348
codec_sha256=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
```

Delta 限于三项 review root cause：

1. `D0Contract` exact type + 复用 `assert_action_authorized("D0_TESTBED_IMPLEMENTATION", contract)`，
   再核 owner code family/1024/1536/20；未复制第二套 control identity。
2. decoder raw output 在 cast 前核 plain real numeric/bool dtype、shape、finite、值域 `{0,1}`。
3. `per_real_noise_power` 在 `float()` 前拒绝 Python/NumPy bool。

没有改 NLL reduction、LLR sign、Sionna metadata、decoder state 或 science semantics。

## 5. New-node GREEN executions completed before stop

| exact node | result | wall | output SHA256 |
|---|---|---:|---|
| `test_codec_rejects_wrong_contract_identity` | 1 passed | 0.797s | `88bd8dfdb7a94b6010ba5e505610de7af6f1c0243a48a0fdf1fe146c619a4fa4` |
| `test_codec_rejects_nonbinary_backend_output` | 1 passed | 0.908s | `0bd96cd6d7d3e36dea7a7c6e054236fc80eec4d3cff0f00701c9b871b790cb1d` |
| `test_codec_rejects_boolean_noise_power` | 1 passed | 0.839s | `e595c9dd5a9edc1722d0f72303c939afef026f4ec243dac3267b63461a9fa194` |

## 6. Incomplete verification boundary

DONE:

- 三条 regression tests 实际先于 production，并各自取得 valid target RED。
- 三项最小 production gate 已实现；三条新节点分别 GREEN。
- 1-ULP NLL 项未修改。

PENDING / NOT CLAIMED:

- 原 RM07–RM10 fresh rerun；
- full codec file；
- I02 regression；
- fresh import probe；
- terminal p05/cache/staging/HEAD/write-set census；
- 独立 verifier 对 late-persisted RED evidence 与 repair 的裁决。

未运行 benchmark/science/web/install，未 commit/push；主线程发出停止指令后未再修改
production/tests 或执行后续验证。
