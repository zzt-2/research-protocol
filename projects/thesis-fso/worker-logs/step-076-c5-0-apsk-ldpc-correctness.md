# Step 076 — C5-0 APSK→LDPC correctness 与 action selection

> 2026-08-30 | T076 / D055 / V030 / CP017 | correctness-only
> terminal: `CORRECTNESS_PASS_B2_ACTION`

## 1. 控制与范围

- Fresh task-control validator：`PASS`（`rdl.task-control.v2` / epoch 17 / CP017 / `C5_LLR_CORRECTNESS_ACTION_SELECTION`）。
- 起点：`0fa836caee3058b0de1b95aaa491774b31740164`。
- 只新增 target correctness 模块、一个集中测试文件和本 worker log；未修改 `common/`、全局 `params.py`、旧 `coded-decoder-feedback/`、Ch3/Ch4、Skill/controller、正式正文或治理文件。
- 未运行 natural occurrence、headroom、BER/FER grid、GMI optimization、调参或新损伤。高可靠 roundtrip 仅作接口与位序测试。

## 2. TDD RED → GREEN

### RED 1：目标模块不存在

```powershell
& 'C:\Users\zzt\.venvs\torch\Scripts\python.exe' -m pytest `
  'projects\simulation\tests\test_ch5_apsk_llr_calibration_correctness.py' -q
```

结果：`10 failed in 0.48s`。10 项均因新 `correctness.py` 不存在而按预期失败；测试先于实现落盘。

### GREEN 1：最小 APSK adapter + live backend wrap

同一命令结果：`10 passed in 8.45s`。实现只 wrap 原 `coded-decoder-feedback/codec.py::_SionnaBackend`，没有复制 LDPC encoder/decoder 算法。

### RED/GREEN 2：补强 coded-group→LLR flatten receipt

```powershell
& 'C:\Users\zzt\.venvs\torch\Scripts\python.exe' -m pytest `
  'projects\simulation\tests\test_ch5_apsk_llr_calibration_correctness.py::test_c6_four_case_target_apsk_ldpc_roundtrip_receipt' -q
```

先得到 `1 failed in 7.79s`（缺 `coded_group_shape` receipt），最小补入 4-bit grouping/sign/hash 后，全文件新鲜结果为 `10 passed in 7.80s`。

### RED/GREEN 3：真实 B1 parity、真实调用顺序与外层 clip 行为

先补 `runtime_fixed_scalar` 的真实 B1 arm，C4/C5 focused RED 为 `2 failed, 1 passed, 7 deselected in 7.74s`（旧 API 不接受该参数），最小实现后全文件 `10 passed in 7.86s`。随后把 live placement 更正为 decoder 内部真实顺序，并要求观察外层 backend clamp 行为；focused RED 为 `2 failed, 8 deselected in 6.79s`，最小修复后全文件 `10 passed in 7.96s`。最后增加 live source 的相对顺序 receipt，单项先 `1 failed in 7.05s`，实现 `out_int_inv < filler injection < super().call` 且 BP source 含 internal clamp 的检查后 `1 passed in 6.70s`。

既有 backend 参考测试：

```powershell
& 'C:\Users\zzt\.venvs\torch\Scripts\python.exe' -m pytest `
  'projects\simulation\tests\test_d0_receiver_codec_methods.py' -q `
  -k 'ldpc_noiseless_roundtrip_one_cw or every_decode_fresh_state or b1_exact_reencode_nll'
```

结果：`3 passed, 15 deselected in 7.72s`。

## 3. C0–C6 receipt

| 门 | 结果 | 证据 |
|---|---|---|
| C0 identity/sign/noise factor | PASS | `m16apsk_mod` 与 `codec_metrics.apsk16_table()` 联合 hash=`684fa7045c351f816e77eb1480784b013d8c100b3939b63d71b05b3b9b8ed879`；16 labels×4 bits mapper/低噪 exact-APP sign 全对；`N0=E|n|²`、per-real=`N0/2`；origin ring-bit 使用 `1/N0`，错误 `1/(N0/2)` negative control 被排除。 |
| C1 max-log B2=B3 | PASS | 16 points+确定性 generic grid、3 组正 variance、4 bits、float64 `max_abs<=1e-12`；未裁剪。placement 另列，不用 clip 效应伪装新变换。 |
| C2 exact-APP | PASS | origin identity `max_abs=7.105427357601002e-15`；3 variance pairs；4 bits 均 `NONIDENTITY`，最大差依次 `2.16455 / 2.68089 / 2.61910 / 1.63833`。B3 保留 distinct strong comparator。 |
| C3 NMS / fixed boundaries | PASS | 两 check、无 clip/filler 最小 NMS 图在 `{0.25,0.5,2,4}` 下 20 轮 message-by-message 正齐次且 hard output 相同；构造小数组验证固定 clip 与 fixed filler 均可破坏齐次。`alpha=.75`、interleaver、punctured zero、fixed iterations 均正确列为齐次。 |
| C4 parity / one scalar | PASS | 一个物理帧只估一个 B2 scalar；两偏振、全部 codewords 共用。B1 由显式 `runtime_fixed_scalar` 生成，运行时固定且不调参；matched control 只要求 B0=B2=B3。真实 B0/B1/B2/B3 每 arm 一次 fresh decode、相同 20-iteration call budget。 |
| C5 truth firewall | PASS | receiver API 不接收 true noise/SNR、payload bits/labels、decoder truth 或 future samples；scorer-only truth 无 receiver 参数、未传入。重复相同 allowed inputs 时 B0/B1/B2/B3 LLR bytes 确定性相同；不声称已构建 scorer integration mutation。 |
| C6 target codec | PASS | all-zero、single-one、walking-label、random 四例：`encode (4,1536) → groups (4,384,4) → APSK (4,384) → exact-APP flatten (4,1536) → fresh decode`，coded→LLR sign error 与 decoded info-bit error 均为 0；hard-output hash=`9c64b8660795f494601c42938140e8d76abd0250f232c9ba8b926f4438435d23`。 |

## 4. APSK / LDPC source receipt

- APSK owner：`common._modulation.m16apsk_mod`；label/fingerprint owner 对照为 `ch5-apsk-structured-covariance/codec_metrics.py`。
- Sionna：`2.0.1`；5G LDPC `BG2`；`k=1024`、`n=1536`、`Qm=4`、`Z=104`、`k_ldpc=1040`。
- `out_int` hash=`96e1b21c6ec75a66cbe865e5f86c6342b224e49ffcfb44c13317c837a9774919`；`out_int_inv` hash=`6e914d73d48086475228d0d7b18fec59d9e60f8f0137085a500f113f56137516`；两者 live 互逆。
- seam 不手工执行 `out_int_inv`；live decoder 内部执行。
- live rate-recovery capture：decoder 先执行 `out_int_inv`，随后注入 16 个 bit-0 filler，LLR 全为 `-20.0`；进入 BP base class 后才执行 internal clip20。
- backend 外层 clip20 不从 decoder `_llr_max` 同源自证：用 `+100/-100` probe 捕获 live backend 送入 decoder 的 tensor，观察到 `max=+20.0`、`min=-20.0`；外层 source 与 BP internal source 的 clip receipt 均为 true。

## 5. B2/B3、clip/filler 与 terminal

目标 placement 已合法闭合：

```text
APSK demapper clip30
→ B2 positive per-frame scalar
→ decode_fresh clip30
→ backend input clip20
→ decoder out_int_inv
→ rate recovery + 16 fixed bit-0 filler(-20)
→ BP internal clip20
```

- `s<1` 与 `s>=1` 均有固定 clip 非齐次控制；fixed filler 另独立证明非齐次。
- 未裁剪 max-log 下 B2=B3，严格不分叉。
- exact-APP 下四个 bits 均稳定 nonidentity，B3 继续作为同信息预算强 comparator；不与 B2 组合成双自由度。
- fixed clip/filler 是目标接口中的自然固定边界；构造控制只证明 action existence，不证明 BER/FER headroom。
- 因 C0–C6、target receipt 和合法 action identity 全部闭合，terminal=`CORRECTNESS_PASS_B2_ACTION`。下一步只有主控另行授权后才可开预注册单格 headroom；本任务不作该性能声称。

## 6. Truth / lifecycle 三联卡

- `information_access`：online known=`current-frame two-pol pilots/reference/mask + payload samples + nominal auxiliary N0`；genie/oracle=`none`；post-hoc truth=`test oracle/scorer only`。
- `metric_signature`：只核 mapper/LLR/decode interface identity、exact equality/nonidentity 与消息齐次；没有 BER/FER population、分子/分母或 performance aggregation。
- `state_lifecycle`：每 arm 每调用 fresh，`message_state=None`、`warm_state=None`；backend object可缓存，但消息状态不跨 arm/frame；configured iterations 恒为 20。

## 7. 独立 reviewer

- 首轮主控外部预审：`FAIL / P0=0 / P1=2 / P2=2`。P1 为真实 B1 parity 缺失、internal clip 与 rate recovery 顺序错误；P2 为 live clip boolean/外层行为证据不足与 C5 mutation 措辞过强。上述四项均以 RED→GREEN 闭合。
- 修复后独立 reviewer：`PASS / P0=0 / P1=0 / P2=0`；terminal `CORRECTNESS_PASS_B2_ACTION` 由 C0–C6、真实 B1 parity、live source/behavior receipt、B2 fixed-boundary action 与 B3 exact-APP nonidentity 支持。
- reviewer fresh 结果：targeted `10 passed in 8.46s`；既有 backend 参考 `3 passed, 15 deselected in 7.81s`；validator `PASS`；diff-check 与 scope whitelist `PASS`。

## 8. 提交前 fresh 验证

- targeted：`10 passed in 7.84s`。
- 既有 backend 参考：`3 passed, 15 deselected in 7.46s`。
- task-control validator：`PASS`。
- `py_compile`：exit 0。
- `git diff --cached --check`：exit 0。
- 三文件白名单：`WHITELIST_BAD=0`、`WHITELIST_MISSING=0`、`STAGED_COUNT=3`。
