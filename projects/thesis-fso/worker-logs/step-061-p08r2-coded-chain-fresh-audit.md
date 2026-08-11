# Step 061 — P08-R2 corrected coded-chain fresh audit

> 2026-08-09 | T015 | action class=`CODED_CHAIN_AUDIT` | control=`CP006 / epoch 6`
> 边界：fresh、只读；未运行 BER/FER、decoder、仿真或科学实验，未修改源码、artifact、中央治理或四个 `p05_run*.log`，未提交。

## 1. Task-control 与读取证据

### 1.1 Validator

执行：

```text
PYTHONDONTWRITEBYTECODE=1 python -B \
  C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py \
  .sessions\2026-08-09-coded-decoder-feedback-groundwork\T015-p08r2-coded-chain-audit.md
```

结果：`PASS`。任务绑定为 `rdl.task-control.v2 / epoch 6 / CP006 / CODED_CHAIN_AUDIT`；当前 topic 允许 `CODED_CHAIN_AUDIT`，禁止 experiment/adapter/MVE/Contract/Execute。

### 1.2 完整读取

以下 T015 必读文件均从头至尾读取；后文所有判断优先引用源码，旧日志只用于核对一致性和查错。

| 文件 | 完整行数 | 本日志主要证据行 |
|---|---:|---|
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py` | 373 | `54-69,88-178,185-216,257-365` |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_chain.py` | 289 | `56-70,77-145,152-277` |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py` | 257 | `33-38,128-216,219-250` |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_run.py` | 391 | `38-96,99-147,221-274,369-386` |
| `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_verify.py` | 423 | `58-143,208-289,297-324,368-405` |
| `projects/simulation/results/p08r_coded_chain_repair/p08r_identity_freeze.md` | 34 | `6-22,28-34` |
| `projects/thesis-fso/worker-logs/step-047-coded-decoder-lineage-recovery.md` | 86 | `19-30,32-43,55-65,67-82` |
| `projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md` | 219 | `7-49,51-90,92-131,133-197,199-219` |

为闭合被调用源码，另只读核对：

- `projects/simulation/common/_dual_pol_channel.py:56-149`；
- `projects/simulation/common/_equalizer.py:5-25`；
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_coded_chain.py:46-106,149-215,431-490`；
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_metamorphic_gate.py:1-147`；
- 本机 Sionna 2.0.1 `encoding.py:24-44,172-180,303-344,770-796` 与 `decoding.py:100-160,733-910,1320-1402,1438-1545,1571-1701`。

本机只做模块版本/签名/源码位置 introspection（无 decoder call）：Python `3.11.9`，Sionna `2.0.1`；`LDPC5GDecoder.call(llr_ch, *, rv=None, num_iter=None, msg_v2c=None)`。

## 2. Codec、BICM、interleaver 与 identity receipt

### 2.1 源码身份

| 项 | fresh 源码事实 | 证据 |
|---|---|---|
| 编码器 | `LDPC5GEncoder(k=1024,n=1536,num_bits_per_symbol=4)`；码率 `1024/1536=2/3`；Sionna 按参数自动选 BG，contract 写 `bg2`，但构造调用没有显式传 `bg=contract.bg` | `p08r_chain.py:88-120,126-133` |
| rate matching / BICM interleaver | `num_bits_per_symbol=4` 使 rate-matched 长度 1536 的输出应用 3GPP TS 38.212 §5.4.2.2 output permutation；encoder 输出已经是 on-air/interleaved bit order | `p08r_chain.py:128-156`; Sionna `encoding.py:32-34,172-180,303-344,791-793` |
| 调制 | Gray 16QAM，4 个相邻 on-air bits `[b0,b1,b2,b3]` 映到一个符号，平均功率 1 | `p08_coded_chain.py:46-80`; `p08r2_chain.py:206-215` |
| soft demap | max-log logits，约定 `log p(b=1)/p(b=0)`；输出 `(Nsym,4)`，顺序与 modulator 相同 | `p08_coded_chain.py:83-106` |
| decoder | 自定义 **normalized offset min-sum**：`0.75 * cn_update_offset_minsum(offset=0)`；configured 20 iterations；`hard_out=True`、`llr_max=20`；未显式改变的 defaults 为 `return_infobits=True, return_state=False, callbacks=[]` | `p08r_chain.py:97-103,134-178`; Sionna `decoding.py:1438-1454,1532-1544` |
| 当前公开 adapter 返回 | final `(B,1024)` hard information bits + `num_iter_configured=20`；没有 posterior、extrinsic、syndrome trajectory、actual iteration count 或 callback trace | `p08r_chain.py:158-178` |

两个必须保留的身份限定：

1. `CodedContractR.bg="bg2"` 是 declarative 字段，当前 encoder constructor 未把它传给 Sionna。对当前 `k/n`，Sionna 自动选择结果应由未来 receipt 记录并断言为 `bg2`，不能只信 dataclass 文本。
2. `net_rate` 在 `__post_init__` 中直接等于 code rate `2/3`（`p08r_chain.py:118-120`），没有扣除每帧 32-symbol known prefix；它不是 end-to-end frame spectral efficiency。

### 2.2 Identity receipt hash 与字段

指定 identity receipt：

```text
path    = projects/simulation/results/p08r_coded_chain_repair/p08r_identity_freeze.md
bytes   = 3277
sha256  = 0457ca047048b1cf52f25ab8943674511fe78b9eac680b9f7e7356dfbc78a3b2
```

receipt 冻结字段为：`k=1024`、`n=1536`、BG2 rate-matched 5G NR LDPC component、Gray-16QAM、`num_bits_per_symbol=4`、§5.4.2.2 output interleaver、20 configured iterations、hard output、`llr_max=20`；并记录 `out_int.shape=(1536,)`、1536 unique、`n_moved=1534/1536`、前 12 项与 inverse round-trip，以及 noise-free 8-frame BER/FER=0 的历史工程回执（`p08r_identity_freeze.md:6-22`）。这些只作为 identity/engineering receipt，不恢复旧科学 terminal。

fresh 本地源文件哈希：

```text
Sionna encoding.py  ae35ae6ed5c71a905fb4b3dc734bf50fdf0213d6c2483735e86e44991daa4ed3
Sionna decoding.py  684be6a0699cfdff93001c9bd8a489aed6c5f2fda690034b94a6b8667eaa89be
Sionna 5G_bg2.csv   4f4db6f7607446984c0b1dc6243bff4286f6fbad3a477f29d84a5e0edab523fb
```

receipt 的两个语义缺口：

- `p08r_identity_freeze.md:11` 写 `cn_update="minsum"` 只是近似描述；实际不是 Sionna 字符串 `"minsum"`，而是 `alpha=0.75` 的 custom normalized offset-minsum closure（offset=0）。未来 source receipt 必须记录 callable/hash/alpha/offset。
- receipt 正文声称 source-auditable，但文件内没有 encoder/decoder/BG CSV hash、commit 或 immutable pre-test binding。上列 hash 是本次 fresh 外部读取结果，不把旧 receipt 升格为 confirmatory chronology。

## 3. Fresh caller→callee 与信息流

```text
p08r2_run.main
  -> build_realization(scene, fG, snr_db, seed)
     -> CodedRealizationR2.realize                         [CHANNEL / TRUTH SIDE]
        -> CodecAdapterR.encode(info_X/info_Y)
        -> qam16_mod(interleaved coded bits)
        -> generate_shared_realization_dp -> h, theta(SOP), AWGN
        -> rX/rY + stores full sX/sY, cw_info_*, cw_bits_*, h, theta, gamma_bar
     -> CodedRealizationR2.equalize                        [RECEIVER SIDE]
        -> prefix slice of rX/rY and known prefix slice of sX/sY
        -> estimate_pre_eq_noise_from_prefix -> sigma2_pre, H_eff
        -> gamma_vis_from_prefix
        -> per-block receiver power h_use_X/Y
        -> mmse_equalize + amp_limit -> eqX/eqY
  -> run_method
     -> method_B0/B1/B2
        -> split prefix/data
        -> estimate_sigma2_from_prefix(known prefix only)
        -> maxlog_soft_demap_16qam(data) -> L_ch (on-air order)
        -> reshape(n_cw,1536)
        -> CodecAdapterR.decode -> final hard info_hat
     -> score_trajectory(info_hat, cw_info_* truth)         [EVALUATION ONLY]
```

逐段字段边界：

| 边 | receiver-visible / legal | truth / privileged / deny from decide |
|---|---|---|
| channel generation | 无 deployable decide；这里只生成被冻结的 `rX/rY` | `seed, scene, alpha, beta, f_g, sop_rate, gamma_bar, info bits, coded bits, sX/sY, h, theta` 均属 generator/evaluation side |
| equalize | `rX/rY`、单独声明的 `known_prefix_X/Y`、由其导出的 `sigma2_pre/H_eff/gamma_vis/h_use/eq` | true `gamma_bar/h/theta`、payload `sX/sY` 禁止；当前实现从携带全量 truth 的 `real.sX/sY` 取 prefix slice，值合法但接口不安全 |
| B0/B1/B2 demap/decode | `eq`、known-prefix residual、frozen temperature/clip/decoder contract、`L_ch`、decoder outputs | payload truth、oracle sigma、true channel state、scoring result |
| oracle O0/O1/O2 | 无 deployable 字段 | 明确读取 payload `sX/sY` 形成 truth residual，只能作 headroom（`p08r2_phaseA.py:197-216`） |
| score | final hard output | `cw_info_X/Y`、BER/FER/correctness；必须在 action 已冻结后消费 |

fresh 接口风险：B0/B1/B2 的 `prefix` 参数实际未使用，方法仍从 `real.sX/sY` 取 prefix（`p08r2_phaseA.py:150-194`）。因此“只取合法 slice”目前依靠代码约定，不是类型边界；C1 不得接收 `real`。

`build_realization()` 还把由 test `snr_db` 算出的真 `g` 返回给 caller（`p08r2_run.py:53-62`）。旧方法没有消费它，但 C1 receiver action 的签名必须完全排除该返回值。

## 4. Carrier impairment、action anchor 与 controller 事实

| 能力 | fresh 结果 | 证据 |
|---|---|---|
| carrier phase noise | **ABSENT** | `CodedRealizationR2.realize` 只生成 GG `h`、SOP mixing `theta=sop_rate*n` 与 AWGN；无 complex carrier phase process，`p08r2_chain.py:199-234`; `_dual_pol_channel.py:103-149` |
| CFO | **ABSENT** | 五份必读源码无 CFO state/estimator/callee |
| cycle slip / localized ambiguity | **ABSENT** | 五份必读源码无 slip state/injection/detector |
| phase-hypothesis callee | **ABSENT** | 无 hypothesis bank、rotation action、score-all-hypotheses 或 switch argument |
| local rollback / re-demap / re-decode | **ABSENT** | B0/B1/B2 每条路径只做一次 demap 和一次 `codec.decode`; `p08r2_phaseA.py:150-194` |
| persistent controller | **ABSENT** | `scan_workspace`/test loop 按 cell/seed 创建 realization，未跨 frame/block 传 state；`p08r2_run.py:77-96,248-274` |
| current phase-like field | **NOT CARRIER PHASE** | `theta` 是双偏振 SOP real rotation 的 truth，不能被重命名为 carrier phase/CFO/slip；`_dual_pol_channel.py:123-140` |

所以当前因果时序严格是：

```text
whole frozen frame -> one equalize -> one demap -> fixed BP decode -> hard bits -> offline truth score
```

不存在 decoder output 回到 carrier front-end 的边。该事实是 `TESTBED_GAP`，不是科学 Kill，也没有单凭“缺 anchor”证明 `>7D_BLOCKER`。

## 5. Sionna 2.0.1 decoder 能力矩阵

| 能力 | fresh 源码事实 | 判定 |
|---|---|---|
| 当前 adapter hard output | `hard_out=True, return_infobits=True, num_iter=20, return_state=False, callbacks=[]`；返回 final 1024 info bits | `READY`（仅 single-pass hard decode） |
| posterior soft output | `hard_out=False` 返回 logits；若同时 `return_infobits=False`，5G wrapper rate-recovers并重新应用 `out_int`，返回全部 1536 on-air positions | `LIBRARY_READY / BOUNDED_ADAPTER`；`decoding.py:1332-1394,1677-1701` |
| true extrinsic | API 不直接返回；候选需在同一 on-air order/sign convention 下构造并验证 `L_ext=L_post-L_ch` | `BOUNDED_ADAPTER`；posterior 不得直接命名 extrinsic |
| decoder state | `return_state=True` 返回 flat edge-state `msg_v2c`，后续 `call(...,msg_v2c=...)` 可接收 | `LIBRARY_READY / BOUNDED_ADAPTER`; `decoding.py:1379-1394,1571-1593,1670-1700` |
| iteration override | 每次 `call(...,num_iter=i)` 可覆盖 configured 20 | `LIBRARY_READY / BOUNDED_ADAPTER`; `decoding.py:837-910,1571-1588` |
| v2c callback | current flooding schedule 下，decode 开始前以 `it=0` 调一次，随后每次 VN update 以 `it=1..N` 调用；必须返回同形 `msg_vn` | `LIBRARY_READY / BOUNDED_ADAPTER`; `decoding.py:120-126,779-785,880-894` |
| c2v callback | current flooding schedule 下每 BP iteration 一次，`it=0..N-1`；custom/layered schedule 会按 subiteration 多次，不能泛称永远“一迭代一次” | `LIBRARY_READY / BOUNDED_ADAPTER`; `decoding.py:127-132,753-771,788-830` |
| native early stop / convergence count | 明确无 batch early stopping；state 不是收敛标志或 iteration count | `ABSENT`; `decoding.py:114-118,1342-1344` |
| syndrome trajectory | 无原生 syndrome return；observation-only v2c callback可从 `x_hat` 和所选 graph PCM 派生，但 pruning、hard-decision sign 与 rate-matched/full-graph mapping必须单独冻结 | `BOUNDED_ADAPTER`，不能复用 encoder roundtrip 当 failure detector |

Fresh 发现的语义修正：

1. `CodecAdapterR.decode()` 的 tuple branch 把第二项猜成 `iterations_per_cw`（`p08r_chain.py:164-177`）；启用 `return_state` 后第二项实际是 `msg_v2c`，该 branch 必须废弃或改名，不能沿用。
2. `p08r2_verify.py` 所谓“递归 AST”只把三个本地 `p08r2_*.py` 的 `FunctionDef` 放入 `source_by_name`（`:210-229`）；imported `estimate_sigma2_from_prefix`、`mmse_equalize`、Sionna decoder 并未进入该图。它能证明本地 `equalize` 不读 `gamma_bar`，不能证明完整 external call graph。
3. 同一 verifier 显式 whitelist `equalize` 对 `self.sX/sY` 的读取（`:230-239`），但没有 AST/dataflow 证明 slice 永远止于 prefix；该保证必须由 restricted receiver-view type 替代。
4. `p08r2_metamorphic_gate.py:1-8` 的 prose 声称覆盖 `h/theta/TX data`，实际 runtime 只改 `real.gamma_bar`（`:86-118`），其 receipt 是 hidden-SNR gate，不是全 truth-leakage gate。

## 6. Coded-bit ↔ symbol 可逆映射与局部边界

### 6.1 当前可逆关系

每个 codeword：1536 on-air/interleaved bits = 384 个 16QAM symbols。`realize()` 先按 codeword 保持连续，再 flatten；demapper 按同一 `[b0,b1,b2,b3]` 顺序输出，随后 reshape 回 `(n_cw,1536)`。decoder 输入端应用 `out_int_inv`，当输出全 codeword soft logits 时再应用 `out_int`，所以 official soft output 仍是 on-air order（`p08r2_chain.py:206-215`; `p08r2_phaseA.py:128-147`; Sionna `decoding.py:1642-1649,1687-1700`）。不得手工再次 deinterleave。

对 data-part symbol index `j`（prefix 已剥离）：

```text
cw_index        = floor(j / 384)
symbol_in_cw    = j mod 384
onair_bit_slice = [4*symbol_in_cw, 4*symbol_in_cw + 4)
frame_rx_index  = n_prefix(32) + j
```

### 6.2 segment/suffix re-demapping / re-decoding 所需边界

- 必须保存 `pol, frame_id, cw_index, symbol_start/end, onair_bit_start/end, prefix_offset=32`；跨 codeword segment 要拆成逐-CW slice。
- phase action 只改变被冻结 `rx` 的指定 symbol slice；只重算对应 4-bit `L_ch` slice，未触及的 LLR 必须 digest 相同。
- LDPC 不是“局部 codeword decoder”：任何被 segment 触及的 CW 都必须提供完整 1536 LLR 并整 CW restart decode，或走另行验证的 full-state IDD contract。不能只把 suffix LLR 送给当前 decoder。
- 若 front-end action 改变 `L_ch`，最小安全 smoke 是 restart touched CW；直接继续旧 `msg_v2c` 需要独立 state/LLR consistency test，不能默认合法。
- decoder callback 的 pruned graph index 不等同 on-air 1536 bit index；若用 graph-syndrome evidence，必须冻结 `rate recovery -> pruned VN -> full PCM/on-air` 映射，或明确只定义 pruned-graph parity metric。

结论：bit↔symbol identity 已足够复用；“局部译码”接口不存在，但“局部重 demap + touched-CW 全重译码”可作为 bounded adapter。

## 7. Fresh receiver-view schema 与 allowlist / denylist

建议的最小类型边界（仅规格，未实现）：

```text
ReceiverFrameView = {
  frame_id, block_id,
  rx_X, rx_Y,
  known_prefix_X, known_prefix_Y,
  prefix_len,
  code_identity, out_int_identity, mapping_identity,
  decoder_budget, hypothesis_bank,
  receiver_clock
}

ReceiverDerived = {
  sigma2_pre, H_eff, gamma_vis, h_use_X, h_use_Y,
  eq_X, eq_Y, L_ch,
  decoder_soft_or_hard, msg_v2c, callback_evidence
}

EvaluationTruth = {
  tx_info_bits, tx_coded_bits, tx_payload_symbols,
  h_true, sop_theta_true, carrier_phase_true, cfo_true, slip_true,
  gamma_bar/snr_true, seed/cell labels,
  oracle_sigma/action, final_correctness, BER, FER, best_truth_hypothesis
}
```

Caller→callee allowlist：

1. `C1.run(ReceiverFrameView, FrozenC1Contract)`；
2. `equalize(rx, known_prefix) -> ReceiverDerived`；
3. `demap(eq_data, receiver_sigma) -> L_ch`；
4. `decode_evidence(L_ch, fixed_i1) -> observation-only evidence/state`；
5. `apply_phase_hypothesis(rx_slice, frozen_phi)`；
6. `select(scores, fixed_tie_break) -> keep/one switch`；
7. `final_decode(touched_full_cw_llr, fixed_budget)`；
8. action/result 冻结后，单向传给 `score(EvaluationTruth, result)`。

Caller→callee denylist：

- C1 action/trigger 不得接收当前 `real` 对象、`g`、channel generator config/seed、`sX/sY` payload、`cw_info_*`、`cw_bits_*`、true `h/theta/phase/CFO/slip/SNR`；
- 不得接收 `score_trajectory` 输出、BER/FER/correctness、oracle sigma/action 或 post-hoc best-hypothesis label；
- 不得调用 `method_oracle` 或从 artifact/raw row 回读 truth 后选择 action；
- known prefix 必须作为独立字段进入，不得以“从 full truth array 切前 32 项”的接口传入；
- `EvaluationTruth -> C1` 无任何反向 edge。

## 8. C1 defect smoke 的最小 adapter BOM

以下是门控通过后才可创建的最小边界；本任务未创建任何一个：

| 新文件（建议位置） | 最小职责 / 接口 | 可复用资产 |
|---|---|---|
| `projects/simulation/explore/coded-decoder-feedback/contracts.py` | `ReceiverFrameView/EvaluationTruth/FrozenC1Contract/C1CostLedger`；runtime/evaluation schema 分离；source receipt | `CodedContractR` 字段、identity receipt/hash 模式 |
| `.../coded_phase_fixture.py` | method-local coded carrier impairment（至少一个明确 phase-noise/CFO/slip 定义）和 frozen receiver arrays；no-feedback identity branch | `CodedRealizationR2` codec/frame/prefix/channel envelope；不得改 `common/` 或 P08/R/R2 |
| `.../c1_phase_hypothesis.py` | `apply_phase_hypothesis`、segment→CW index、fixed bank、decoder evidence score、keep/one-switch、touched-CW re-demap/re-decode | prefix-LS equalizer、Gray demapper、Sionna callbacks/iteration override、on-air mapping |
| `.../c1_run.py` | 同一 realization 的 B0/B1/B2/C1 调用、receiver-only raw event receipt、deterministic tie-break、cost/latency ledger；score 仅在 action freeze 后 | P08-R2 paired-realization/row schema，但不用旧科学 cells/numbers或 direct terminal |
| `projects/simulation/tests/test_coded_decoder_feedback_c1.py` | 下节全部断言 | old noise-free/identity/metamorphic test ideas；不复用旧 terminal |

最小接口集合：

```text
make_coded_phase_fixture(config) -> (ReceiverFrameView, EvaluationTruth)
decode_evidence(L_ch, i1, callback) -> EvidenceReceipt
apply_phase_hypothesis(rx_segment, phi) -> rx_candidate
select_and_redecode(view, evidence, bank, budget) -> C1Result
score_after_freeze(eval_truth, result) -> EvalMetrics
```

### 8.1 工作量下界

在以下强假设都成立时——同帧静态/local phase rotation 足以作 action、只做一种 impairment、只用一种 decoder evidence、touched-CW restart、不建 streaming controller、不改 `common/`——fresh 下界约 **5 个工程日**，有界区间 **5–6.5 日**：

- restricted schema + source/identity receipt：0.5 日；
- carrier impairment fixture + phase-hypothesis callee + no-feedback branch：1–1.5 日；
- Sionna split-iteration/evidence adapter：1 日；
- segment/CW mapping、scheduler、runner/raw ledger：1–1.5 日；
- conventional same-information comparator、focused tests、metamorphic/cost/debug：1.5–2 日。

因此当前整体判定是 `TESTBED_GAP`，decoder 子层是 `BOUNDED_ADAPTER`；没有 fresh 证据支持 `>7D_BLOCKER`。

### 8.2 明确触发 `>7D_BLOCKER` 的条件

任一项经 Step 3/3.5 事实确认后成立，才升级：

1. defect/action 必须依赖 streaming carrier estimator、跨块连续状态、relock/reacquisition、rollback/replay，而不能用同一 frozen frame 的 bounded phase rotation 表达；
2. 合法 impairment/action 无法 method-local 包装，必须修改 `common/` 或 P08/R/R2 才能建立 no-feedback identity；
3. decoder evidence 必须改 Sionna 内核/PCM pruning/rate-recovery internals，observation-only callback 在 1 个工程日内无法给出身份正确的 metric；
4. touched-CW restart 不满足问题机制，必须验证 changed-LLR 下的跨轮 `msg_v2c` state reuse 或实现自定义 IDD decoder；
5. strongest cheap conventional comparator 本仓库无可复用 caller，需另建完整 carrier tracker/relock baseline；
6. 固定 hypothesis/budget 下无法形成公平成本账本，必须扩建通用流式平台或多帧调度器。

触发条件尚未被当前源码证明；不得把“现在没有 anchor”直接写成 `>7D` 或科学 terminal。

## 9. 必须可执行的测试断言（本任务 NOT RUN）

| test | 预注册断言 |
|---|---|
| no-feedback identity | 同一 frozen `ReceiverFrameView`，`feedback_enabled=False` 时 `eq/sigma/L_ch/hard_bits` digest 与 untouched P08-R2 path 一致；equalizer/front-end/decoder call 与 BP budget ledger 完全相符 |
| noise-free | interleaved encode→mod→noiseless receiver→decode 的 info BER/FER=0；C1 evidence 为“无需 action”，chosen action=`KEEP`，switch/recovery=0 |
| callback lifecycle | current flooding 下 observation-only v2c trace 严格为 `it=[0..i1]`，c2v（若启用）为 `[0..i1-1]`；callback 返回 tensor byte/digest 不变；异常必须 fail closed |
| state semantics | `return_state` 第二项 schema=`msg_v2c`（shape/dtype/hash），禁止 `iterations_per_cw`；restart 分支不得把旧 state 传给 changed LLR |
| mapping identity | 16 个 one-hot/high-confidence labels逐一 round-trip；`out_int[out_int_inv]==arange(1536)`；`L=0 -> E[s]≈0`；手工 double-deinterleave 必须被 negative test 捕获 |
| segment boundary | data symbol `j` 到 `(cw,j%384,4-bit slice,prefix+frame index)` 的公式对首/末/跨-CW边界成立；只改目标 LLR slice，未触及 slice digest 不变 |
| bounded action | hypothesis 数不超过 frozen `Hmax`；tie-break 固定；每帧最多一次 switch；action 只改预登记 segment；所有 candidates 使用同一 rx digest |
| hidden-SNR metamorphic | 保留旧 `gamma_bar` flip，receiver outputs/evidence/action/final output均不变 |
| full truth-leakage metamorphic | 在 `ReceiverFrameView` 不变时删除/打乱 `tx payload/h/theta/phase/CFO/slip/SNR/info_true/final correctness/best label`，evidence、chosen action、callback trace、hard output digest 完全不变；静态签名断言 action caller 无这些字段 |
| oracle denial | monkeypatch/spy 断言 deployable C1 从不调用 `method_oracle/oracle_sigma*`，raw truth只在 `score_after_freeze` 首次出现 |
| cost/latency | `bp_iter_total=sum(per_decoder_call_iters)`；记录 decoder/front-end/hypothesis/callback/recovery calls；C1 与 comparator 的 matched-budget formula 逐字段重算一致；wall/device time 非负且 raw→aggregate 可重算 |
| receipt/schema | runtime/evaluation 两域必填且互斥；source hashes、decoder flags、permutation/mapping hashes、same-rx digest、evidence、action、reset policy、cost 全存在；未知字段 fail closed |

## 10. 与 step-049 的一致项和修正项

### 10.1 一致

1. 当前 corrected chain 是 single-pass hard decoder，没有 decoder→carrier feedback edge（step-049 `:7-49`）。
2. Sionna 2.0.1 的 soft output、`msg_v2c` state、per-call iteration override、v2c/c2v callback 能力确实存在；当前 adapter 未暴露（`:51-90`）。
3. on-air interleaved coded-bit↔16QAM mapping 可逆；soft full-codeword output不应再次 deinterleave（`:92-119`）。
4. 当前 `real` 把 runtime 与 truth 混装；C1 必须改为 restricted receiver view（`:133-158`）。
5. 旧 gamma metamorphic/AST 只能作 partial pattern，future candidate 必须扩展 truth-leakage 与 raw/cost receipt（`:160-173,199-213`）。
6. 资产 gap 不产生科学结论（`:215-219`）。

### 10.2 Fresh 修正 / 收窄

| step-049 表述 | fresh 修正 |
|---|---|
| overall `TESTBED_HARD_BLOCKER` | 在当前 3–7 日授权口径下，源码只证明 `TESTBED_GAP`；method-local impairment+phase action 有 5–6.5 日 bounded path。只有 §8.2 条件成立才是 `>7D_BLOCKER` |
| C1 decoder evidence+scheduler `2–3 d`，end-to-end 未闭合 | 2–3 日仅覆盖 decoder-side；加入 carrier impairment/action、schema、comparator、receipt/test 后 fresh 下界 5 日 |
| “递归 AST over deployable call graph” | verifier 未纳入 imported common/Sionna callees，也未证明 `sX/sY` 只读 prefix；应标 `PARTIAL_LOCAL_AST` |
| metamorphic gate覆盖 hidden truth | runtime 只 flip `gamma_bar`；`h/theta/payload/final correctness` 尚未测 |
| receipt 中 decoder `minsum` | actual 是 `0.75 * cn_update_offset_minsum(offset=0)` custom normalized min-sum |
| c2v“一次/BP iteration” | 仅 current flooding 成立；custom/layered schedule 可每 subiteration 调用，测试需绑定 schedule |

## 11. Fresh readiness 判定

| layer | 判定 | 理由 |
|---|---|---|
| corrected codec/interleaver/Gray mapping/single-pass hard decode | `READY` | source identity、on-air mapping和 hard caller已存在；只作工程起点 |
| Sionna soft/state/iteration/callback exposure | `BOUNDED_ADAPTER` | library primitive 存在，当前 wrapper 缺失；tuple state语义必须修正 |
| receiver-view/truth separation | `BOUNDED_ADAPTER` | 当前值流可分，但类型仍混装；需新 restricted schema与扩展 metamorphic |
| carrier phase/CFO/slip + phase-hypothesis/recovery callee | `TESTBED_GAP` | 当前源码完全无 anchor；method-local bounded 建设路径尚可行 |
| C1 end-to-end defect smoke | `TESTBED_GAP` | 最低需 §8 的 5 个新文件/接口与 5–6.5 日；未授权、未运行 |
| >7 日 hard blocker | `NOT_ESTABLISHED` | §8.2 任一触发条件均未由当前只读证据证明 |

最关键事实：**P08-R2 已有可复用的 interleaved coded/BICM hard receiver，Sionna 2.0.1 也具备 soft/state/callback primitives；但当前全链没有 carrier phase-noise/CFO/slip、phase hypothesis callee、局部 re-decode 或 persistent controller，因此 C1 不是 READY，而是可望在 3–7 日内补齐的 `TESTBED_GAP`，不能据此科学 Kill。**

## 12. Git / protected-log 检查

任务启动时 worktree 已有他人 tracked/untracked 改动，包括中央治理、paper index、litsearch/litdownload cache、T012–T019、step-060 与四个 untracked `p05_run*.log`；本任务没有清理、覆盖或归因这些并发状态。

四个 protected log 启动 SHA256：

```text
p05_run.log   7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log  735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log  c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log  95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

Final protection/status check（fresh）：

- task-control 复跑：`PASS`；
- worker-log：存在，358 行（final patch 前计数），必需章节/关键词检查 `missing=[]`；
- 本任务输出的 git status：`?? projects/thesis-fso/worker-logs/step-061-p08r2-coded-chain-fresh-audit.md`；
- 四个 `p05_run*.log` final SHA256 与启动值 4/4 完全一致；
- full status 仍含启动前中央治理、paper index、cache、T012–T019、`p05_run*.log` 等 dirty 状态；审计期间还观察到并发新增/变化的 step-058/059/063 与额外 litsearch cache。它们不属于本任务，本任务未读取后写、清理、覆盖或归因；
- 本任务唯一写入为本 step-061 worker-log；未执行 `git add/commit/push`。

## Terminal

`AUDIT_COMPLETE / TESTBED_GAP / NO_SCIENTIFIC_TERMINAL`
