# Step 143 — D0 I06 fresh final verifier

> 2026-08-10 | T097 | fresh non-author final-byte verification

## Findings first

`VERDICT=PASS`，`P0/P1/P2=0/0/0`。

- 126 个预先标记 `EXPECT_ACCEPT` / `EXPECT_REJECT` 的独立合同用例全部与预期一致：错误接受 0，承重合法 control 错误拒绝 0。
- 四个 T094 exact nodes 为 4/4 PASS；显式展开的全部 `test_d0_*.py` 为 43/43 PASS。两条有效 pytest 均为 0 fail/error/skip/xfail/warning。
- 四组、每组双偏振的独立 `C_pre` 复算为 8/8 match；物理方程、双偏振 sharing、payload chain 与 receiver receipt truth-free 检查全部通过。
- final source/tests、owner、step-140/142、HEAD、staging、P05 与 cache census 均保持冻结；本 verifier 只创建本日志。

因此 I06 可以交还 I05 后续工作；该结论只闭合普通本地 Python 数据契约/数值单元验收，不授权 benchmark、D0 scientific S1–S4、MVE 或 held-out experiment。

## 冻结输入与范围

完整读取了 T097、D012–D013、step-140/142、最终 `contract.py` / `channel.py`、两份最终测试，以及 owner 的 views / population physical / physical realization / receiver front-end 段。专题当前 action 属于 `D0_UNIT_TEST` 范围；`D0=NOT_RUN`、method signal=`NONE` 保持不变。

```text
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
channel.py=af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6
test_contract=30fe6b67b6b26c9fc962476fef8287159b10e95bb046a67b0ee25cdf76b47779
test_waveform_channel=f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1
step-140=c54866255c88bbb379e597bdc45f88135a6ca403b864245cce2bb995d303af73
step-142=e76f76de0751c4dce29a0067c98e1052410b444a9b89c7b0a90f2cc123984ffc
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
```

## Fresh pytest

固定环境为 `PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11 `-B -m pytest -p no:cacheprovider`。

```text
four_exact=4 passed in 5.25s
fail/error/skip/xfail/warning=0/0/0/0/0
output_sha256=cfe705ecc55884446cb0b793f0457adc36c4fc4388d5f2baa08a6883aaea4138

aggregate_files=test_d0_contract_views.py,test_d0_receiver_codec_methods.py,test_d0_schemas_statistics.py,test_d0_waveform_channel.py
aggregate=43 passed in 14.14s
fail/error/skip/xfail/warning=0/0/0/0/0
output_sha256=eebc1efa59a8a0257b545a11dc16b1d0bc5523f53a19b8b638e9b896f708e0ba
```

第一次 aggregate 调用把 `test_d0_*.py` 作为引号内字面参数交给 Windows pytest，收集前即以 `0 tests / exit 4` 退出（output SHA `5253a324...`）。这不是测试结果；随后由 PowerShell 只读展开同一文件集为上述四个显式文件，得到有效 43/43 证据。

## 独立合同矩阵

单个 Windows PowerShell here-string 通过 stdin 送入 Python；不创建仓库脚本。每个 case 执行前均注册唯一名称和 `EXPECT_ACCEPT` / `EXPECT_REJECT`，仅“期望拒绝却返回”或“期望接受却抛异常/后置条件失败”计 mismatch。

| 类别 | total | accepted | rejected | legal controls | mismatch |
|---|---:|---:|---:|---:|---:|
| correctness | 18 | 7 | 11 | 7 | 0 |
| metadata closed-world | 47 | 15 | 32 | 15 | 0 |
| receiver semantic keys | 31 | 3 | 28 | 3 | 0 |
| exact root scalar | 20 | 2 | 18 | 2 | 0 |
| payload / contract / C_pre regression | 10 | 2 | 8 | 2 | 0 |
| **合计** | **126** | **29** | **97** | **29** | **0** |

覆盖明细：

- correctness：确认 evaluated view 无 correctness field/slot/setter；constructor、replace、普通/direct attribute set 均拒绝；错误 decoded shape/dtype/binary/list 均拒绝；全同和单 CW 不同的合法 decoded 输出接受；返回 property 数组被修改后再次读取仍按冻结 truth+decoded 重算。
- metadata：覆盖 `bytearray`、`memoryview`、`range`、bare object、mapping proxy、generator/iterator、标准容器 subclass、自定义 Mapping/Sequence/Set、dataclass、slots/`__dict__` 对象、nested、dict/list cycle、非字符串 key、object/structured/string ndarray、ndarray subclass 与 NumPy scalar；合法 exact plain tree、numeric/bool ndarray、NumPy numeric/bool scalar接受并与构造后源变化脱离。
- receiver keys：28 个 noise/AWGN/N0/SNR/variance/power/sample 的大小写、camel、分隔、复数与嵌套变体全部拒绝；两个 exact receiver-derived safe keys 由内部值覆盖，无关 metadata 与 TruthView physical receipt 接受。
- root：bool、NumPy bool、4 种 NumPy signed、4 种 unsigned、float/string/complex/None、negative/oversize 均拒绝；exact Python `0` 与 `2**63-1` 接受。
- regression：payload shape/dtype/binary、canonical codec relation、Gray-16QAM waveform relation、forged owner、C_pre caller injection 与 PhysicalCell scalar均 fail closed；合法 build 与 changed-observation C_pre recomputation接受。

```text
total_cases=126
mismatch_count=0
matrix_output_sha256=84ffafef6ad0fd86b2e88b3597ca3ad89948854e93cf0b9de6ea4097061c1be0
```

矩阵首次独立 re-encode 直接把冻结、不可写的 TruthView ndarray 交给 PyTorch codec，产生一次 verifier-oracle `UserWarning`；production 的 payload binding 会先构造 writable copy。另起 warnings-as-errors control 使用 writable copy 后通过，payload re-encode match=true，且同一 group-1 received SHA 不变：

```text
WRITABLE_COPY_WARNING_ERROR_CONTROL=PASS
PAYLOAD_REENCODE_MATCH=True
output_sha256=b767607b5f7e9f276b7c443299b2f1c3e9dcc09f003d06f7701ee96311b65132
```

该 warning 是 verifier 独立 oracle 的调用方式，不是 production 路径或 pytest finding，故不计 P2。

## 四组物理与 C_pre 独立复算

独立使用 `vdot(x,r)/vdot(x,x)`、`RSS/31` 逐偏振复算 C_pre；独立检查 `h=sqrt(fade)*exp(j*phase)`、`received=h*tx+noise`、`per_real=1/(2 gamma)`、`complex_power=1/gamma`、共享 fade/phase、独立两偏振 AWGN，以及 codec→coded→独立 Gray-16QAM→waveform data positions。

| group | root | cell | C_pre | equations | sharing | payload | received SHA256 |
|---:|---:|---|---|---|---|---|---|
| 1 | 8000 | snr_10db__linewidth_10000hz | 2/2 | PASS | PASS | PASS | `e46829c0161630841b277ed126195b2c9ffc921f601360a80749c4c3e8ba650b` |
| 2 | 8050 | snr_14db__linewidth_20000hz | 2/2 | PASS | PASS | PASS | `02d749f638990c2b05e34abb98e3459e0c3b7367bf8aa279b4ea4d9d2307aae2` |
| 3 | 8100 | snr_18db__linewidth_80000hz | 2/2 | PASS | PASS | PASS | `964a79b9248c9068f200fc2c1e1731e69b8b126b5687b46e35b95e6973796976` |
| 4 | 8150 | snr_22db__linewidth_80000hz | 2/2 | PASS | PASS | PASS | `88ff76a6b942a2927f1f43e003a27524dc5684028e10072abc06d41121b27ab7` |

总计 `C_pre=8/8`；receiver receipt graph 不含 `samples/per_real_variance/complex_power/physical_snr_db/true_phase/channel_h/fade/noise_receipt`，且 receiver 与 truth arrays 不共享内存。全矩阵前后 legacy global RNG state 均 byte-equivalent。

## Static / import / protection

AST 静态审查 PASS：source 无 `sys.path` 变更、legacy/common import、global RNG convenience call 或 finalizer token；channel 只有局部 `SeedSequence/Generator/PCG64` 构造且无 I/O；contract 唯一 I/O 是显式 `load_contract` 内的 owner read。动态 closed-world/source-mutation cases已验证 receiver metadata 不保留可变源引用。

```text
static_output_sha256=ae199d102e13f0c5ddc94fe1e2c87876bbd6603902341fa72da571de8ce57fca
git_diff_check_exit=0
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
```

`git diff --check` 仅打印工作树既有 LF→CRLF 提示，未报告 whitespace error，exit=0。四个 P05 SHA 保持：

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

第一次 static receipt 把显式 loader 的预期行号误写成 936，而 final source 实际为 899，导致 verifier 自身断言 exit=1；随后改为 AST 动态验证该调用位于 `load_contract` 函数范围内，得到上述有效 PASS。未因此修改 source/tests/governance。

## Terminal

`terminal=I06_VERIFIED_READY_FOR_I05`
