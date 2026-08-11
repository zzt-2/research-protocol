# step-128 — D0 I03 waveform independent reverification

> 2026-08-10 | verifier: `/root/i04_codec`（未参与 I03 实现或 P1 修复） | task: T082
> Verdict: **PASS** | terminal: `I03_VERIFIED_READY_FOR_BATCH1`

## 1. Findings first

```text
P0=0
P1=0
P2=0
TERMINAL=I03_VERIFIED_READY_FOR_BATCH1
```

未发现新的可执行 finding。step-123 的 P1 精确复现现已在公开
`WaveformBuild.__post_init__` owning boundary fail closed；同时，完全一致的普通公开构造、
未旋转 build 和 24 个合法旋转 build 均仍可构造，未观察到修复过严导致的合法路径回归。

`PrefixAsset`/`PilotAsset` 的公开构造器没有被扩大为本轮 P1：生产 consumer 不接受调用方
构造的这两类对象，注册 waveform 的 owning path 会自行派生注册 reference；本轮未发现它们
可直接绕过 `WaveformBuild` 关系门。

## 2. Frozen-input / protection preflight

| input | expected SHA256 | observed | result |
|---|---|---|---|
| `waveform.py` | `7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f` | same | MATCH |
| frozen test | `f11fe29b3a83583514a2f10811645e78f9ff6af114f2910ba0bd00beef852157` | same | MATCH |
| step-123 | `c899f896ebb7a4d59c7031688295ab26af3f99f16e9a3f72164e508f62778d72` | same | MATCH |
| step-125 | `092f535d64781f1ef9a0353ee70b85c55bb176cecd2b2327d2c0b79731b4974e` | same | MATCH |
| `contract.py` | `074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713` | same | MATCH |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | same | MATCH |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` | same | MATCH |
| staging | `0` | `0` | MATCH |

step-128 初始为 `ABSENT`；production/tests/step-123/step-125 只读。

## 3. Fresh pytest receipts

共同环境：

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
python -B -m pytest -p no:cacheprovider ... -q
```

| command/gate | result | wall | output SHA256 |
|---|---:|---:|---|
| 新 regression `test_waveform_build_relational_validation_fail_closed` | 1 passed | 0.637s | `f69b41b567fe2583118441e8e8390afa756eecb8625fa01f5e10bcff2c1cef10` |
| 原 WC01/WC02/WC03/WC08 exact nodes | 4 passed | 0.690s | `006ba2e6e18954ad086677bc060e3290380048985a443818578f6ef51ed1b21b` |
| full `test_d0_waveform_channel.py` | 5 passed | 0.694s | `1966890ba6efc09f86dd998039477f6271ab6aa52cc7ff72888f7d6b6a9bc479` |
| I02 `test_d0_contract_views.py` regression | 6 passed | 0.710s | `e294d58817276d5377bf3bcb35039ecb555722eb3cfdba356c1a9238baaf8280` |

Fresh command executions=`16 passed`；unique tests=`11/11 GREEN`；
failed/error/skip/xfail/warning=`0/0/0/0/0`。

## 4. Independent public-constructor / registered-layout matrix

不落 repo 文件的 Windows Python `-B` inline matrix：

```text
exit=0
wall=0.352s
output_sha256=f32dd32dd283cc80248dece704295c661c3f204ed381e9837a4e8cedecb9f799
exact_step123_rejected=1
registered_N_cases=4
mutation_rejections=26
accepted_invalid=0
rotation_cases=24
k0_copy_cases=6
positive_assertions=232
MATRIX=PASS
```

26 个 public-constructor 拒绝项按关系族分解如下：

- step-123 原始 `N=999`、`waveform=(2,1)`、互相矛盾 maps 的精确伪造对象：1/1 拒绝；
- N：unregistered/bool/float 及 3 个 registered-but-layout-mismatched N，6/6 拒绝；
- waveform/known/mask/data-map/inverse-map shape，5/5 拒绝；
- duplicate、out-of-range、broken inverse、self-consistent-but-reordered maps，4/4 拒绝；
- prefix/first-pilot/terminal/data-position known schedule，4/4 拒绝；
- prefix/first-pilot/terminal/data-position known reference，4/4 拒绝；
- waveform/known nonfinite，2/2 拒绝。

合法路径审计：

- N=`10/20/100/200` 的总长、pilot/known 数、6144 rank/time inverse、terminal known、
  data byte recovery 与 nested read-only 全部成立；
- 每个 N 的完全一致普通 `WaveformBuild(...)` 公开构造均接受、defensive copy 且不别名；
- `2 pol × 3 boundaries × 4 k = 24` 的 pre-boundary、clean polarization、目标 suffix、
  maps、known reference 均精确；返回对象均通过修复后的公开构造门；
- 6 个 `k=0` case 仍 copy-on-write，不与 source waveform 共享内存；source caller data
  后续突变不影响 build。

## 5. Import / static audit

```text
global_np_random_state_unchanged=True
filesystem_unchanged=True
sys_path_unchanged=True
import_roots=[__future__, dataclasses, math, numpy]
dynamic_imports=[]
io_calls=[]
global_rng_calls=[]
```

AST/source audit 未发现 import-time I/O、global RNG、dynamic/legacy/runner import 或 `np.exp`
rotation drift。registered assets 使用局部 `Generator(PCG64(...))`，不消费全局 RNG。

## 6. Final protection / terminal

终检前保护基线仍为：

```text
cache_file_count=222
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
```

四个保护性 `p05_run*.log` SHA256 仍分别为：

```text
7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

```text
VERDICT=PASS
P0=0
P1=0
P2=0
FRESH_UNIQUE_TESTS=11/11 GREEN
PUBLIC_CONSTRUCTOR_MUTATIONS=26/26 REJECTED
REGISTERED_N=4/4 PASS
ROTATIONS=24/24 PASS
TERMINAL=I03_VERIFIED_READY_FOR_BATCH1
```

未运行 benchmark/science/web/search/download/install，未 commit/push/stage，未修改
production/tests/executor logs。
