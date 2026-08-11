# step-123 — D0 I03 independent waveform verification

> 2026-08-10 | verifier: `/root/i04_codec`（未参与 I03 实现） | task: T077
> Verdict: **FAIL** | terminal: `I03_VERIFICATION_FAIL`

## 1. Findings first

```text
P0=0
P1=1
P2=0
TERMINAL=I03_VERIFICATION_FAIL
```

### P1-1 — `WaveformBuild` 公开构造器缺少关系不变量，invalid build 被 rotation fail-open 接受

**Owner oracle**：T077 要求 invalid `build` 必须拒绝，并显式要求检查“public constructor
可生成内部不一致、后续导致 fail-open”的情况；owner 域只允许 N=`10/20/100/200`、32
prefix、6144 data、匹配的 known/map/total layout。

**Source cause**：`waveform.py:76-97` 的 frozen/slotted `WaveformBuild.__post_init__`
只做 dtype defensive copy/read-only，不核 waveform/known/map shape、6144 bijection、registered
N、terminal/known cardinality等关系不变量。`apply_persistent_rotation` 在 `:222` 只核
`isinstance(build, WaveformBuild)`，随后 `:235` 直接消费 `data_to_time`，并在 `:238`
返回另一个未校验 build。

**Fresh reproduction**（exit `0`，output SHA256
`82146072a89a046d00d90e597c93c8bae850cc1076e9434643ddf811314f53a3`）：

```text
WaveformBuild(
  waveform.shape=(2,1), known_symbols.shape=(1,), known_mask.shape=(1,),
  data_to_time=zeros(6144), time_to_data=zeros(1), N=999
)
apply_persistent_rotation(... target_pol=0, boundary_after_data=1536, k=1)

observed:
ACCEPTED type=WaveformBuild waveform_shape=(2, 1) known_shape=(1,) N=999
readonly=True suffix=np.complex128(1j)
```

**Impact / severity**：这是 owner-exposed typed input 到 controlled suffix callable 的直接可达路径，
不是仅能修改 private constant 的假设攻击。调用方只要持有公开 `WaveformBuild` 构造器，即可用
错误 N、缺 prefix/data/terminal、互相矛盾 maps 的对象通过类型门并产生貌似 frozen/read-only 的
输出；下游不能再把类型身份当作注册 waveform 证明。违反 T077 的 invalid-build fail-closed
门，因此定为 P1，并阻断 `I03_VERIFIED_READY_FOR_BATCH1`。

**Required repair boundary（本 verifier 未修改源码/测试）**：在唯一 owning boundary 对
`WaveformBuild` 做完整关系校验，或把未校验构造器变成不可公开伪造的受控 factory；
`apply_persistent_rotation` 必须拒绝上述复现。修复后需要冻结 test-first RED，并重跑本矩阵。

## 2. Frozen-input / protection preflight

| input | expected SHA256 | observed | result |
|---|---|---|---|
| `waveform.py` | `bab2a491e0afb1b32b188ea0ce1465b9b6fe2a1ee08593c2c2544c1fe3c2b748` | same | MATCH |
| frozen test | `b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d` | same | MATCH |
| step-117 | `9dd643651980c812ae7ef1dd4852faf1849b7b5043656b1d4106deb97b936bbb` | same | MATCH |
| step-121 | `b269ea2973b888a0bd8edfa9de5b945e038449eddfdba70e0f924a4d0481356a` | same | MATCH |
| `contract.py` | `074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713` | same | MATCH |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | same | MATCH |
| plan | `52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b` | same | MATCH |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` | same | MATCH |
| staging | `0` | `0` | MATCH |

step-123 初始为 `ABSENT`；production/tests 只读。

## 3. Fresh unit receipts

Common environment/cwd:

```text
D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider
```

| command/node | result | wall | output SHA256 |
|---|---|---:|---|
| `test_registered_prefix_bytes_hashes` | 1 passed | 0.900s | `b12e2a73d84d814528b4d6d01e360ddb8405c76fc1c543c044a7d96c73905b00` |
| `test_registered_pilot_hashes_counts` | 1 passed | 0.756s | `b12e2a73d84d814528b4d6d01e360ddb8405c76fc1c543c044a7d96c73905b00` |
| `test_data_time_map_bijective` | 1 passed | 0.803s | `420148db9e0b69209165e34674193ac580cc29b79b121aeba98eef98d79c0cbe` |
| `test_controlled_jump_copy_on_write` | 1 passed | 0.769s | `420148db9e0b69209165e34674193ac580cc29b79b121aeba98eef98d79c0cbe` |
| full `test_d0_waveform_channel.py` | 4 passed | 0.969s | `9c59e497271d608c060428b358b09d66d98a3b7b66df69262b5b5fa5e6d14eb1` |
| `test_d0_contract_views.py` | 6 passed | 1.085s | `cc3748ddd64c25121333402d0cdb7c9733f3f0f33f6353f70f65bbf92942eb00` |

Fresh command executions=`14 passed`（unique frozen tests=`10`）；skip/xfail/warning=`0/0/0`。

## 4. One-shot independent negative/metamorphic matrix

不落 repo 文件的 Windows Python inline audit 结果：

```text
registered_N_cases=4
rotation_cases=24
invalid_rejections=42
positive_audit_assertions=455
required_public_constructor_rejection=FAIL (accepted)
matrix_exit=3 (intentional nonzero on finding)
matrix_output_sha256=9de76518d6c36119d2656523050d6722389a175c8f8e6f78ec4c3ae9c11ea6eb
```

通过项：

- prefix/pilot repeated calls bytes 一致、defensive/no alias、nested ndarray read-only；
- 注册 hash 从实际 bytes 计算，source 不含 expected-SHA shortcut；
- N=`10/20/100/200` 的 counts/length、prefix、first/periodic/terminal pilots、6144
  data/time inverse、known=`-1`、terminal known 与 data byte recovery 全部成立；
- source data 构造后突变不影响 build；
- `2 pol × 3 boundaries × 4 k = 24` 全部满足 source/pre-boundary/clean-pol/maps/
  known byte identity，目标 suffix（含 later/terminal pilots）精确整数旋转；k=0 仍 copy-on-write；
- 42 个 invalid N/data shape/object/nonfinite/pol/boundary/k/type/non-build 输入均拒绝；
- dataclasses frozen+slots，返回 nested arrays read-only。

唯一未通过项即 P1-1：typed-but-relationally-invalid public build 被接受。

## 5. Import / static audit

Fresh import probe：

```text
global_np_random_state_unchanged=True
filesystem_digest_unchanged=True
sys_path_unchanged=True
new_legacy_or_runner_modules=[]
```

AST/static scan：imports 仅 `__future__/dataclasses/math/numpy`；无 file I/O、global RNG、
runtime legacy/runner import、expected-hash hardcode、`np.exp` rotation drift。唯一 in-place
rotation 写在 fresh copy 上；正常路径 terminal pilot 未遗漏。

## 6. Terminal / protection

```text
VERDICT=FAIL
P0=0
P1=1
P2=0
FRESH_UNIQUE_TESTS=10/10 GREEN
NEGATIVE_MATRIX=455 PASS / 1 FAIL
TERMINAL=I03_VERIFICATION_FAIL
NEXT_LEGAL_ACTION=bounded test-first repair of WaveformBuild relational validation, then fresh independent reverification
```

未运行 benchmark/science/web/install，未 commit/push，未修改 production/tests/executor logs。
