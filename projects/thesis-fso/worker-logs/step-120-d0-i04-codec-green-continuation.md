# step-120 — D0 I04 codec GREEN continuation

> 2026-08-10 | executor: `/root/i04_codec` | task: T074 | status: **PASS**

## 1. Terminal

```text
STATUS=PASS
TERMINAL=I04_READY_FOR_INDEPENDENT_VERIFICATION
RM07=GREEN
RM08=GREEN
RM09=GREEN
RM10=GREEN
```

本轮只创建 `codec.py` 与本日志；冻结测试、step-118、owner、contract、旧链均未修改。

## 2. Frozen continuation receipt

| item | expected SHA256 | observed | result |
|---|---|---|---|
| frozen test | `38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef` | same | MATCH |
| step-118 | `cccdfb0d149fbd925918d68957dd487b6d30921d126146e8b219f04d92df4fc3` | same | MATCH |
| contract | `074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713` | same | MATCH |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` | same | MATCH |
| plan | `52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b` | same | MATCH |
| P08-R source | `174daad20f4fadbb0710cdee5faf7d49f360b6a8a6609b9a1ea46ccb41288404` | same | MATCH |
| initial production | `ABSENT` | `ABSENT` | MATCH |
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` | same | MATCH |
| staging | `0` | `0` | MATCH |

既有四份 valid RED output SHA 保持 step-118 冻结值，未重写测试。

## 3. Minimal implementation

`codec.py` 只包含 I04 所需职责：

1. `[b0,b1,b2,b3]` / `[-3,-1,3,1]/sqrt(10)` Gray map、hard demap、四态整数旋转与逆识别。
2. import 时不加载 Sionna、不构造 encoder/decoder、不读写文件、不改 `sys.path`。
3. 首次 encode/decode/metadata 请求时在 CPU 构造 PyTorch Sionna 2.0.1 `LDPC5GEncoder(1024,1536,num_bits_per_symbol=4)` 与 fixed-20 decoder。
4. 每次 `decode_fresh` 显式传 `message_state=None,warm_state=None`；backend 对非空 state 有 tripwire。对象可缓存，message/warm state 不缓存。
5. 正 LLR 表示 bit=1；demapper preclip 30、decoder clamp 20；`complex_noise_power/2` 仅由单一 helper 转换。
6. `reencode_nll` 严格为同 shape coded bits 上的 `mean(softplus((1-2*c_hat)*L))`。

没有 runtime import `p08*`、truth correction、skip/fallback 或 TensorFlow 路径。

## 4. Exact RM GREEN receipts

Common environment:

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
flags=-B -m pytest -p no:cacheprovider
```

| RM | exact node | count | duration | exit | output SHA256 |
|---|---|---:|---:|---:|---|
| RM07 | `test_gray16_roundtrip_rotation` | 1 passed | 0.23s | 0 | `d8c86ff2390d5c0b0a3bcad71d7128e77c8592a4448e5ac2e0d3986f26a080d9` |
| RM08 | `test_ldpc_noiseless_roundtrip_one_cw` | 1 passed | 5.40s | 0 | `217bce2a5c77c14bd34a2dc6c3ca615652ae8ca6f57ba90ec92b380b1f29fcbe` |
| RM09 | `test_every_decode_fresh_state` | 1 passed | 0.29s | 0 | `db4ce22a81508ccb886f409bf6d5791df57d3810dd37302d8c4c62e5f45a28a3` |
| RM10 | `test_b1_exact_reencode_nll` | 1 passed | 0.28s | 0 | `88bd8dfdb7a94b6010ba5e505610de7af6f1c0243a48a0fdf1fe146c619a4fa4` |

Exact command was instantiated per node:

```powershell
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_receiver_codec_methods.py::<node> -q
```

No skip, xfail or warning occurred.

## 5. Aggregate and regression

| suite | result | duration | exit | output SHA256 |
|---|---|---:|---:|---|
| `test_d0_receiver_codec_methods.py` | 4 passed | 5.39s | 0 | `e73fef14cbcbaa6b62c823df240b1862bd2d60e435b64b5f611c77a300bef37e` |
| `test_d0_contract_views.py` | 6 passed | 0.33s | 0 | `1b2f5d88896d8f687e32c91e815b0ad11778b6d1d3a8a5e6c35e2f037fff8bc7` |

## 6. Live metadata / source receipt

```text
python=3.11.9
torch=2.6.0+cu124
sionna=2.0.1
base_graph=bg2
lifting_size=104
num_bits_per_symbol=4
interleaver=3gpp-ts-38.212-5.4.2.2
interleaver_length=1536
interleaver_inverse_check=True
out_int_sha256=87fe62c1ff62c632dd7afac243002e6f178072c2005fe12bba35e0d0683bfa7f
out_int_inv_sha256=6709a1c54053c653fa9789bb45c2e3d397dd9e547290c73e98c56dc423c659da
encoder_source_sha256=ae35ae6ed5c71a905fb4b3dc734bf50fdf0213d6c2483735e86e44991daa4ed3
bg2_csv_sha256=4f4db6f7607446984c0b1dc6243bff4286f6fbad3a477f29d84a5e0edab523fb
lazy_import_sionna_loaded=False
legacy_modules_loaded=[]
```

## 7. Handoff boundary

I04 的实现与冻结单元 oracle 已 GREEN；本日志只授权进入独立 I04 verification，不授权
benchmark、science、D0 execution、C1 extension 或修改治理 owner。

未安装依赖、未联网、未运行 benchmark/scientific seed、未 commit/push、未改测试或旧链。
