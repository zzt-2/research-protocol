# step-133 — D0 I06 oracle correction and completion

> 2026-08-10 | T087 / D011 / V005 / CP012 | action: `D0_TESTBED_IMPLEMENTATION`
> Verdict: **PASS** | terminal: `I06_READY_FOR_INDEPENDENT_VERIFICATION`

## 1. Findings first / review disposition

```text
WC06_ORACLE_CORRECTION=ACCEPTED
NEW_PRODUCTION_RED=NO
PRODUCTION_MODIFIED=NO
TERMINAL=I06_READY_FOR_INDEPENDENT_VERIFICATION
```

step-130 的四个 `channel.py=ABSENT` RED 保留为生产实现的历史 bootstrap
evidence，未删除、改写或倒签。WC06 的失败根因是测试在完整
`repr(ReceiverView)` 上做 substring 搜索，误命中 owner 明确允许的嵌套
`CodeLayout.information_bits_per_cw`；没有证据表明 ReceiverView 泄漏 TruthView。

本任务只把 oracle 改为结构化检查：直接字段名与 truth aliases 精确比较；对
`receiver.receipts` 的 mapping keys、dataclass/slots field names 和容器成员递归检查，
带 object-id 循环保护。合法 `CodeLayout`/`WaveformLayout` metadata 继续允许，不用
substring/repr，也不隐藏 production 字段。修正后在冻结 production 上直接 GREEN，符合
T087；没有制造或宣称新的 RED。

## 2. Frozen-input preflight

| input | expected SHA256 | observed | result |
|---|---|---|---|
| `channel.py` | `728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde` | same | MATCH |
| test before correction | `ba5ebbacdeab3904554772fec70f3a4d73f1809f0a0d7f35ea8074c4201bd13a` | same | MATCH |
| step-130 | `7d787b55f12b84a654bd87c453669b8bd317f2da6cb2b02a1f2a267e1de706b7` | same | MATCH |
| `waveform.py` | `7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f` | same | MATCH |
| `contract.py` | `074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713` | same | MATCH |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | same | MATCH |
| plan | `52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b` | same | MATCH |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` | same | MATCH |
| staging | `0` | `0` | MATCH |

step-133 初始为 `ABSENT`。唯一代码改动是测试 oracle；production source 保持冻结 SHA。

## 3. Fresh Windows pytest receipts

共同环境：

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ... -q
```

| gate | result | wall | output SHA256 |
|---|---:|---:|---|
| corrected WC06 exact node | 1 passed | 1.112s | `8a5d3f8c1b452931de963c4bdff9775f7404361fdf3f79b4d740fb5a4f7e6e92` |
| WC07 exact node | 1 passed | 1.132s | `91ac28e87543203edb8fac4612b815f59bf36ac9a72ab315b86b2e36637fba30` |
| WC04–WC07 exact group | 4 passed | 1.199s | `2a972e91a01c735ba2f846c2c844201df72eee2228aa3d0387c2185548d2c49b` |
| full waveform-channel file | 9 passed | 1.282s | `2a031d57b22dcf4fa6414cbc235fd89f4f30bcfd3c974a4efcef3384d46eac19` |
| I02 contract regression | 6 passed | 0.692s | `0b0f944787b74eb2f646db3fee5e1b26b43ab1bdfd66a7442728b825a538f187` |

Fresh command executions=`21 passed`；unique tests=`15/15 GREEN`；
failed/error/skip/xfail/warning=`0/0/0/0/0`。

输入防御在 WC04/WC06 内 fresh 执行：invalid root 4 项，以及 bad shape、nonfinite、
unregistered cell、wrong contract identity 各 1 项，共 `8/8 REJECTED`。WC04 同时证明
NamedStreams 不改变 global NumPy RNG state。

WC07 fresh 核验 `tau=1/(2*pi*100)`、block-100 rho、10k/20k/80k 的单次 effective
linewidth variance、`theta[0]=first innovation`，以及 AWGN per-real/complex power exact；
全部 GREEN，未产生 production repair seam。

## 4. Structural sharing / view split / import audit

Final physical/import inline audit（不落 repo 文件）：

```text
exit=0
wall=0.681s
output_sha256=96d28c7ca01060a40fed3af89d0a40a273789e5238a376a004eb4f7348804513
shared_intensity_bytes=True
shared_wiener_bytes=True
independent_awgn_bytes=True
supplied_waveform_equation=True
defensive_after_input_mutation=True
all_physical_arrays_readonly=True
global_rng_unchanged=True
filesystem_unchanged=True
sys_path_unchanged=True
project_legacy_runtime_imports=[]
project_runtime_imports=[contract, channel, waveform]
import_roots=[__future__, contract, dataclasses, math, numpy, scipy, typing, waveform]
STRUCTURAL_AUDIT=PASS
```

一次初始 audit denylist 把第三方/stdlib 的
`charset_normalizer.legacy`、`importlib.resources._legacy`、`unittest.runner`
误报为项目 legacy/runner；第二次仍误报 `unittest.runner`。这两次是 audit harness 的
substring oracle 过宽，不是 production failure。最终规则按 module `__file__` 限定到 evidence
worktree 后通过；未据此修改 production。

独立 view-split audit：

```text
exit=0
wall=0.675s
output_sha256=f645dde0c8e1880885282752107084ac5f37155658815293fef66f8827ba95a6
receiver_matches_physical_received=True
truth_transmitted_symbols=True
truth_phase_fade_channel_noise=True
truth_physical_cell_and_event=True
receiver_truth_arrays_disjoint=True
view_arrays_readonly=True
VIEW_SPLIT_AUDIT=PASS
```

因此 shared GG/Wiener、independent AWGN、identity-SOP supplied-waveform equation、
Receiver direct/receipt truth boundary、Truth physical quantities、frozen/defensive arrays 与纯
import 均有 fresh structured evidence。

## 5. Final identities and protection

```text
channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde
test_after_oracle_correction=ce5b80b262612943ada9e5677ff27713bef8dafd9cf17c6f8e537d464da5c3b0
step-130=7d787b55f12b84a654bd87c453669b8bd317f2da6cb2b02a1f2a267e1de706b7
cache_file_count=222
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
```

四个 protected `p05_run*.log` SHA256 仍为：

```text
7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

```text
VERDICT=PASS
WC06_CORRECTED=1/1 GREEN
WC07=1/1 GREEN
WC04_07=4/4 GREEN
FULL_WAVEFORM_CHANNEL=9/9 GREEN
I02_REGRESSION=6/6 GREEN
NEGATIVE_INPUTS=8/8 REJECTED
PRODUCTION_MODIFIED=NO
NEW_PRODUCTION_RED=NO
TERMINAL=I06_READY_FOR_INDEPENDENT_VERIFICATION
```

未运行 benchmark/science/web/search/download/install，未 commit/push/stage，未修改
contract/waveform/owner/legacy，也未创建 runner/artifact/result/cache。
