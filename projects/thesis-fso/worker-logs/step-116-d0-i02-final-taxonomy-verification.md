# Step 116 — D0 I02 iteration-2 final fresh taxonomy verification

> 2026-08-10 | T070 / D011 / V005 / CP012 / epoch 12 | FRESH VERIFIER
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `PASS / P0/P1/P2=0/0/0`

## 1. 权限边界与冻结输入

本轮只执行 CP012 `D0_UNIT_TEST`。未运行 benchmark、科学 seed/estimand、
DEFECT_SMOKE、S1–S4、C1 adapter/policy、web/search/download、commit 或 push；
未修改候选实现与测试。

T070 的冻结身份在测试前和落盘前均匹配：

```text
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test_d0_contract_views.py=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-115=1fc7ef00bc03ce13f0d62ea60ea17508eea4a41541599ae11a56798c906b0695
step-114=505dc4bc42f37d880e954a85ddc93ef7b085b2718551893aa302c6f11b4f4324
step-112=9f906374838236e9d2ac95b52f23b936a9cad92e6af3c5508bb824c8dd7b6342
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
```

Owner 边界保持明确：ReceiverView 仅允许 received/equalized samples、known
prefix/pilots、receiver noise estimate、common CPR/receiver state、frozen
code/B2 参数与非 truth receipts；TX 数据、真实物理状态、事件真值和最终正确性
仅属于 evaluator-only TruthView。

## 2. 新鲜完整测试

执行命令：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest `
  -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

结果：

```text
......                                                                   [100%]
6 passed in 0.28s
exit_code=0
failed=0
errors=0
skipped=0
xfail=0
warnings=0
stdout_stderr_sha256=3dfd263a5a6b15f9fc444096373fe4cc24dbe0d251b9e14fe6a19ed9f21235f4
```

该结果只证明冻结的六项测试通过；分类语义由下一节未写入 candidate tests 的
独立生成矩阵验证。

## 3. 独立生成 owner taxonomy 矩阵

矩阵通过 PowerShell here-string 直接管道到 Windows Python `-B -`，未写 repo
或 OS 临时脚本。每一行都把生成 key 放在三层 mapping 之后，并调用真实
`ReceiverView(...)`；未直接调用 private predicate。

生成规则与行数：

- TX：`payload`；`{info,information}×{bit,bits}`；
  `coded×{bit,bits}`；`data×{symbol,symbols}`；
  `{tx,transmitted}×{bit,bits,info,information,coded,data,symbol,symbols,payload}`。
- physical：`snr/cfo/fade` 与空/true/physical/actual/oracle/channel 前缀、
  空/value/estimate/receipt/state 后缀的笛卡尔积；exact `h`；
  `channel×{true,physical,actual,oracle,realization,gain,coefficient,response,state,fade,h}`；
  `phase×{truth,true,physical,channel,oracle,actual}`。
- event：`slip/event` 本身及其与 label/boundary/rotation 的组合；
  `{injected,injection,natural}×{label,fixture,boundary,rotation,event}`。
- correctness：`correct/correctness`；
  `final×{cw,codeword,frame,bit,bits}×{error,errors,status,correct,correctness}`。
- 每个 semantic base 均生成 snake、UPPER、hyphen、dot 四行；单 token 的
  punctuation 形式按 normalization 必然与 snake 相同，但仍作为独立 form receipt。

结果：

```text
generated_tx_rows=108
generated_physical_rows=432
generated_event_rows=92
generated_correctness_rows=108
generated_forbidden_total=740
accepted_forbidden_count=0
failure_count=0
exit_code=0
stdout_stderr_sha256=838294c9ca389c17db3b1a04fc6ef7e034a7654fe28a58865ddbfce29f389b85
```

因此无需列出 accepted row；本轮没有 owner-equivalent generated case 进入
ReceiverView。T070 的 mandatory denylist rejection terminal 未触发。

## 4. 容器、safe control 与 action gate

所有检查均通过 public constructor/API：

```text
object/structured/unicode/datetime ndarray rejected=4/4
numeric/bool detached-and-read-only checks=4/4
TruthView under benign key and safe-name key rejected=2/2
explicit nested safe controls accepted=12/12
exact CP012 actions accepted=5/5
positive permission five-minus-one subsets=3/3
identity/execution/science mutations emptied action set=8/8
scientific/unknown/case/whitespace action variants rejected=14/14
```

12 个 safe controls 分别为：

```text
received_samples
equalized_samples
known_prefix
periodic_pilots
receiver_noise_estimate
common_cpr_phase_trace
global_rotation_state
bps_state
source_sha256
code_sha256
content_sha256
channel_source_sha256
```

普通 float64/bool source ndarray 在构造后被修改，stored values 保持原值且
`writeable=False`。TruthView 即使放在 whitelist key `received_samples` 下，仍由
递归 value inspection 拒绝，说明 whitelist 只免除合法 key 名称，不绕过 value
边界。

Action oracle 为精确五项：

```text
D0_TESTBED_IMPLEMENTATION
D0_UNIT_TEST
ENGINEERING_THROUGHPUT_BENCHMARK
SOURCE_AUDIT
CONTRACT_STATIC_CHECK
```

三个 positive permission 分别由 true→false 时，返回集合恰为上述五项减对应
一项，且被移除 action 由 `assert_action_authorized` 拒绝；无新增 capability。
schema/epoch/CP/action_class/D/V 漂移，或 execution/science 变 true，均返回空集。

## 5. 静态边界与历史 finding disposition

静态/动态 import probe 得到：

```text
CV06-CV08 named tests/DeploymentBoundary absent=4/4
production Path.open calls during isolated import=0
production forbidden imports=0
production main guards/runners/future seal=0
production directory files=contract.py only
```

`load_contract` 的显式 caller-selected owner read 保留，但 module import 本身不做
repository I/O。未发现 sys.path mutation、benchmark/scientific runner、dynamic
import bypass 或 I17A placeholder。CV06–CV08 仍按计划留待真实跨组件 I17A，未在
I02 用假对象提前闭合。

最终 disposition：

- **step-112 P1-1 — CLOSED**：literal denylist 已演化为四族组合 taxonomy；独立
  740-row 生成矩阵为 `740/740 rejected`，并且 12 个明示 safe controls 为
  `12/12 accepted`。
- **step-112 P1-2 — CLOSED**：object/structured/non-numeric ndarray 均 fail
  closed；plain numeric/bool ndarray defensive-copy/read-only 成立。
- **step-112 P1-3 — DISPOSED_NON_DEFECT**：permission true→false 只移除对应
  capability，是严格五减一子集；identity 或 execution/science 漂移仍清空全部。
- **step-114 P1-1 — CLOSED**：iteration 2 的 owner taxonomy 对未写入 candidate
  tests 的完整生成族无 bypass；不存在触发 `DENYLIST_ROUTE_REJECTED` 的 accepted
  row。

此结论的 claim ceiling 是 T070 明确定义的 owner token-combination taxonomy；
它不把任意未来自然语言同义词宣称为数学上的无限完备。后续新增 metadata 仍须
受 typed owner contract 与独立边界测试约束。

## 6. 保护项与 terminal

测试/矩阵前后，除本 step116 目标外的 status receipt 与 cache manifest 完全一致：

```text
status_excluding_target_line_count=154 -> 154
status_excluding_target_sha256=28dbe92dce5c9631f5e4cb79b2b5be7520f9fe510e97af03cf25e60ebe77e3aa -> same
cache_file_count=222 -> 222
cache_manifest_sha256=7dc22a9bb758efd96b0815afbaf8a5bfd72f3238db2c1015d2e0496ca01e8fc0 -> same
pyc_count=202 -> 202
__pycache___dirs=41 -> 41
.pytest_cache_dirs=4 -> 4
staging_count=0
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

四个 protected p05 logs 保持 4/4 exact：

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

```text
VERDICT=PASS
FRESH_SIX_TESTS=6/6
GENERATED_FORBIDDEN=740/740 rejected
SAFE_CONTROLS=12/12 accepted
P0_P1_P2=0/0/0
DENYLIST_ROUTE_REJECTED=NO
TERMINAL=I02_VERIFIED_READY_FOR_BATCH1
```
