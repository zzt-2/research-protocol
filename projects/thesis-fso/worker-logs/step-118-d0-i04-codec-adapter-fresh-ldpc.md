# step-118 — D0 I04 codec adapter / fresh LDPC

> 2026-08-10 | executor: `/root/i04_codec` | task: T072 | status: **INCOMPLETE**

## 1. Terminal

```text
STATUS=INCOMPLETE
TERMINAL=I04_INCOMPLETE_AT_RM07
BOUNDARY=RM07-RM10_TESTS_AND_VALID_RED_RECEIPTS_COMPLETE__NO_RM_GREEN__PRODUCTION_ABSENT
REASON=15_MINUTE_HARD_LIMIT_REACHED_BEFORE_FIRST_PRODUCTION_SLICE
```

没有把超时写成环境 blocker。按 T072 的 `receipt-before-production` 与 15 分钟
纪律停止；`codec.py` 从始至终不存在，没有写仓促 production、benchmark 或 science。

## 2. Scope / protection preflight

- evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- branch / HEAD: `codex/rdl-method-production-v2` / `715a65884b988ee737f21982f3bbf372860a1da8`
- staged paths: `0`
- initial targets: `codec.py=ABSENT`, `test_d0_receiver_codec_methods.py=ABSENT`, `step-118=ABSENT`
- initial and terminal cache census under D0 root + tests: `12` pre-existing entries; no new entry from this task (`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`)
- protected p05 logs: `4/4` present:
  - `p05_run.log`: `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log`: `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log`: `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log`: `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`

Frozen-input SHA checks:

| input | observed SHA256 | result |
|---|---|---|
| `contract.py` | `074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713` | MATCH |
| `test_d0_contract_views.py` | `e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80` | MATCH |
| step-116 | `6fb1b4056f2395e4e979258fb741f0c009130ffd25b84d6507b7052ad035892c` | MATCH |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | MATCH |
| plan | `52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b` | MATCH |
| step-106 | `67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2` | MATCH |
| step-105 | `e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d` | MATCH |
| `p08r_chain.py` | `174daad20f4fadbb0710cdee5faf7d49f360b6a8a6609b9a1ea46ccb41288404` | MATCH |
| H004 | `f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4` | MATCH |

## 3. Live environment metadata

Exact environment for probes/tests:

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
pytest flags=-B -m pytest -p no:cacheprovider
```

Live PyTorch Sionna receipt (exit `0`):

```text
python=3.11.9
torch=2.6.0+cu124
sionna=2.0.1
encoder_module=sionna.phy.fec.ldpc.encoding
decoder_module=sionna.phy.fec.ldpc.decoding
encoder_signature=(k: int, n: int, num_bits_per_symbol: Optional[int] = None, bg: Optional[str] = None, precision: Optional[str] = None, device: Optional[str] = None, **kwargs)
decoder_signature=(encoder: sionna.phy.fec.ldpc.encoding.LDPC5GEncoder, cn_update: Union[str, Callable] = 'boxplus-phi', vn_update: Union[str, Callable] = 'sum', cn_schedule: Union[str, numpy.ndarray, torch.Tensor] = 'flooding', hard_out: bool = True, return_infobits: bool = True, num_iter: int = 20, llr_max: Optional[float] = 20.0, v2c_callbacks: Optional[List[Callable]] = None, c2v_callbacks: Optional[List[Callable]] = None, prune_pcm: bool = True, return_state: bool = False, harq_mode: bool = False, precision: Optional[str] = None, device: Optional[str] = None, **kwargs)
```

TensorFlow 不存在不是 blocker：Sionna 2.0.1 live API 是上述 PyTorch 路线；后续不得再按旧
TensorFlow 路线实现。

## 4. RED receipt-before-production

Receipt-common facts:

```text
test_sha256=38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef
production_codec.py=ABSENT
collection=PASS
failure_class=EXPECTED_FIRST_MODULE_ModuleNotFoundError
skip=0
xfail=0
warning=0
```

每个节点都在 test body 内失败；不是 syntax、fixture、path、collection 或 dependency error。

| RM | exact node | exit | output SHA256 | key failure | RED |
|---|---|---:|---|---|---|
| RM07 | `test_gray16_roundtrip_rotation` | 1 | `110375e54809bc793598a3ed1010610ff4c1a4e2e706fc157a86fd255b13d466` | `ModuleNotFoundError: No module named 'codec'` | VALID |
| RM08 | `test_ldpc_noiseless_roundtrip_one_cw` | 1 | `59b9e3ee69f07023fd656182991fe0eac81bbf96b92bafbb19bc541b280f8de2` | `ModuleNotFoundError: No module named 'codec'` | VALID |
| RM09 | `test_every_decode_fresh_state` | 1 | `8bc5495a0a00b129ba84bc4d5d232d29470efb2b706fb1b6eb3920f1afb4a52a` | `ModuleNotFoundError: No module named 'codec'` | VALID |
| RM10 | `test_b1_exact_reencode_nll` | 1 | `a3b0bc4a51014bd8e1074d7dcdf42646d3528ffd7d062efbb72bcb6c88ba50c2` | `ModuleNotFoundError: No module named 'codec'` | VALID |

Exact command template, instantiated once per node in table order:

```powershell
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_receiver_codec_methods.py::<exact-node> -q
```

## 5. RM status and continuation boundary

| RM | test authored | valid RED | production | GREEN | status |
|---|---|---|---|---|---|
| RM07 | YES | YES | ABSENT | NOT RUN | PENDING |
| RM08 | YES | YES | ABSENT | NOT RUN | PENDING |
| RM09 | YES | YES | ABSENT | NOT RUN | PENDING |
| RM10 | YES | YES | ABSENT | NOT RUN | PENDING |

DONE:

1. T072/plan I04/step-106 RM07–RM10/step-105 codec interface and frozen-hash preflight.
2. Four exact test nodes authored before production.
3. Four valid, individually executed RED receipts captured while `codec.py=ABSENT`.
4. Windows Python 3.11 / PyTorch Sionna 2.0.1 live API receipt captured.

PENDING (next executor must continue from RM07; do not rewrite tests without invalidating all RED receipts):

1. Finish remaining source/owner/P08-R2 semantic read that the hard stop interrupted.
2. Implement minimal lazy `codec.py` for RM07, run exact RM07 GREEN, then proceed RM08 → RM09 → RM10 in order.
3. Capture live BG/Z/interleaver from constructed encoder and fail closed on mismatch.
4. Run full new test file plus `test_d0_contract_views.py` regression and terminal protection census.

No commit, push, benchmark, scientific seed/run, web, dependency install, cache cleanup, legacy runtime import,
owner/contract/test drift, or modification outside the three-file write set occurred.
