# Task Brief: D0 owner identity typed loader（I05 binding 前置关口）

> 来源: D015 / V011 / T107 step-153 / I05 open bindings | 产出位置: `projects/thesis-fso/worker-logs/step-154-d0-owner-identity-typed-loader.md`
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

## Scope / hypothesis / terminal

- 只改 `contract.py`、`test_d0_contract_views.py`，并写 step-154；不得改 owner、schemas、channel、waveform、codec、session 治理文件或其他测试。
- 假设：在不改变现有 `D0Contract` / `load_contract` / channel runtime 行为的前提下，可用一个独立 frozen authority wrapper 把 final owner 的 `identity_binding_contract` 变为 schema 可消费的 closed-world immutable typed view。
- 否决条件：必须给 `D0Contract` 增字段、必须在 schema 层做 I/O、无法从 exact final owner 自足复算 identity root、或现有 I02/I06 回归不绿。触发任一项即 `INCOMPLETE`，不得扩大范围。
- PASS 上限：`OWNER_IDENTITY_TYPED_LOADER_READY_FOR_INDEPENDENT_VERIFICATION`。不等于 I05 完成，不开放 benchmark/science。
- 目标 12 分钟，15 分钟硬停止；禁止 install/commit/push/stage。

## Frozen receipt

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
scientific_projection_owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
identity_binding_canonical_json=29d1fc77bc3028861df04e3442de07ffabc0d72a68a2e4666f3b318b98b48ec6
contract=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
contract_tests=30fe6b67b6b26c9fc962476fef8287159b10e95bb046a67b0ee25cdf76b47779
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
R001=ff229de3305c179521474ea37e37a748ed2189d824d75e6779708ac89f3992dd
decisions=ca4b7098e8b9ab77575b58ea2abed07e6e356566e38c0ed8901eb0cfabe0d6e7
verifications=848ea9e3e97e6937ceb1dbcecf98350b09cfea135447d35f4815a607dfd785ea
step153=39ded7d15e32bd43e625782b143406e45e8390ef451279d1c05ed239491b8443
```

P05 四日志必须保持既有 SHA；tracked pycache 不得写。schemas/owner/R001/decisions/verifications/step153 必须只读且末尾复核。

## Mandatory strict RED

先只编辑测试，生产源码不动；运行以下 exact nodes，必须因 public API 缺失而真实非零，并将完整命令、输出、exit code、stdout SHA 先写 step-154：

1. `test_owner_identity_authority_exact_frozen_view`
2. `test_owner_identity_grid_commitments_recompute_exact`
3. `test_owner_identity_mutations_fail_closed`
4. `test_owner_identity_loader_preserves_existing_contract_runtime`

测试不得从 production private helper 派生 expected roots。RED 不红则停止。

## Required public boundary

在 `contract.py` additive 实现，保持 `D0Contract` 四字段、`load_contract(path) -> D0Contract` 和现有 public 行为不变：

```python
@dataclass(frozen=True, slots=True)
class IdentityBindingContract:
    # exact 13 owner sections；三个 header scalar 及十个 section 均显式字段
    ...

@dataclass(frozen=True, slots=True)
class D0OwnerIdentityAuthority:
    contract: D0Contract
    identity_binding: IdentityBindingContract
    owner_sha256: str
    scientific_projection_sha256: str
    identity_binding_sha256: str

def load_owner_identity_authority(path: str | Path) -> D0OwnerIdentityAuthority:
    ...
```

具体要求：

- exact 13 top-level keys/order语义：`schema_version`、`decision_ref`、`scientific_contract_change`、`canonical_serialization`、`grid_authority`、`payload_schemas`、`hmm_authority`、`ledger_accounting`、`cache_source`、`consumer_bindings`、`runtime_content`、`golden_vectors`、`validator_obligations`；拒绝 omitted/extra/type drift。
- 三个 header 必须分别为 `coded_decoder_feedback.d0.identity_binding.v1` / `D015` / `none`。
- 十个 section 必须成为递归不可变、detached exact values；不得保存 caller mutable dict/list，也不得公开 mutable internal reference。owner 中 `grid_authority.p_s.anchors` 与 `golden_vectors.grid_commitments.p_s_anchors` 含合法 integer keys，必须先规范化为 typed `(index, float64_hex)` tuples；不得为此放宽通用 `_deep_freeze` 的 string-key closed-world 规则。其余纯 string-key mapping 可复用 `_deep_freeze`。
- exact owner bytes SHA、scientific projection SHA、identity canonical JSON diagnostic seal 必须为 Frozen receipt 三值。`29d1...` 是对 V011 final parsed identity view 的实现期防漂移 seal，不得表述为 owner 自身声明的新 root。canonical JSON 使用 owner 冻结通则：UTF-8、`sort_keys=True`、`separators=(",", ":")`、`ensure_ascii=False`、`allow_nan=False`、无尾换行；JSON float 禁止。
- `load_owner_identity_authority` 只能显式调用时读文件；strict duplicate-key parse，读取前后 owner bytes 必须一致；复用现有 `load_contract`，并对 wrapper 内 contract 调 `assert_frozen_d0_identity`。不得在 import 时 I/O。
- direct dataclass replacement/伪造 wrapper 必须被 public validation 或消费前 revalidation fail closed；至少冻结并复算 identity root，不可只相信对象自带 hash 字符串。
- identity view 必须允许后续 schemas 只读查询，但本任务不得解释/补造 owner 缺失的 work-key、phase、operation 语义。
- loader 只复算三项 grid commitment 与 owner 已冻结的六组静态 accounting counts；其余 clean/target/sentinel/M3/S2/BPS/runtime 七组 golden 只做 closed-world shape/type/format 存储，留给后续 compiler 独立复算，禁止在 loader 内复制第二套 schema compiler。

## Independent test oracle / mutation gate

- 测试侧自写 canonical encoder；从 exposed frozen view 独立复算 122 `p_s` + 6 `sigma_e2` literal、standalone 2 roots和combined root，命中：
  - `bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864`
  - `0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca`
  - `0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf`
- 递归 mutation 至少 15 项：top-level omitted/extra、三个 header type/value、section nonmapping、duplicate key、literal index/hex/order/root、combined deep-equality、golden root、consumer binding kind、ledger count、cache source rule；每项均从临时 owner 文件调用 public loader，必须 fail closed。
- 验证 identity view 不可 item assignment，源 YAML object/外部容器变化不影响 view；两个 fresh loads 不共享 nonprimitive mutable reference。
- `load_contract(OWNER)` 与 wrapper.contract exact equality；`authorized_action_classes` unchanged；现有全部 `test_d0_contract_views.py`、`test_d0_waveform_channel.py` 必须 GREEN。不得运行 science/benchmark。

## Commands / evidence / return

Windows：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

step-154 必须记录 RED/GREEN exact counts、mutation 数、回归 counts、三文件 final SHA、source diff 摘要、保护核验、P0/P1/P2。只能返回上述 PASS terminal、`FAIL` 或 `INCOMPLETE`。
