# Task Brief: C5-0 target APSK→LDPC correctness 与 B2/B3 action selection

> 来源: S028 / D055 / T075 / V030 | 产出位置: `projects/simulation/explore/ch5-apsk-llr-calibration/` + `projects/thesis-fso/worker-logs/step-076-c5-0-apsk-ldpc-correctness.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 17
  action_class: C5_LLR_CORRECTNESS_ACTION_SELECTION
  mission_checkpoint: CP017
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在独立目录内把 project DP-(8,8)-16APSK mapper/exact-APP|max-log demapper 接到既有 Sionna 2.0.1 5G BG2 `k=1024,n=1536,Qm=4` encoder/decoder，形成可审计的 target codec receipt，并执行 T075 C0–C6 deterministic correctness。唯一科学输出是 B2 是否在真实冻结接口中形成合法 action，以及 B3 exact APP 是否为 distinct strong comparator。

这不是性能任务：不得运行 natural occurrence、headroom、BER/FER grid、GMI optimization、参数调优或新损伤。高 SNR roundtrip 只作 codec correctness，不得包装成 BER 结果。

## 开始前强制读取

1. 根 `AGENTS.md`、`sim-preflight` skill 全文及其当前必读 references、`code-quality.md` 和相关 sim-template。
2. 本 brief、topic-index 页首 CP017、D055/V030、T075 `step4a-paper-feasibility.md`。
3. `projects/simulation/common/_modulation.py:145-229`。
4. `projects/simulation/explore/ch5-apsk-structured-covariance/codec_metrics.py`。
5. `projects/simulation/explore/coded-decoder-feedback/codec.py:113-330` 及其现有 codec tests/fixtures。
6. T074 `step3-5-exact-recipe-closure.md` 的 max-log/exact-APP 边界。

先运行 task-control validator。采用 TDD：先写 RED tests 并记录失败，再做最小 GREEN；不得修改 `common/`、全局 `params.py` 或原 `coded-decoder-feedback/` 实现。

## 冻结实现缝

- 新目录：`projects/simulation/explore/ch5-apsk-llr-calibration/`。
- 可通过窄 adapter 复用既有 Sionna backend/encoder/decoder；不得复制出第二套未经核对的 LDPC 算法。
- mapper 必须调用 project `m16apsk_mod`；constellation/labels 必须由 `apsk16_table()` fingerprint 到同一表。
- LLR 语义固定 `log P(bit=1|y)-log P(bit=0|y)`；complex noise power `N0=E|n|^2`，per-real covariance=`N0/2`。
- 输出顺序必须由 `encoder coded bits → 4-bit APSK groups → symbol-order LLR flatten → live 3GPP out_int/out_int_inv → decoder` receipt 证明，不凭“Qm 都是 4”假定；不得在 seam 手工再执行 `out_int_inv`，因为 live decoder 内部负责反交织。
- B0：固定/名义 auxiliary `N0`，`s=1`；B1 仅 runtime-fixed scalar；B2 为 demapper/fixed preclip 后、black-box LDPC 前的 per-frame positive scalar；B3 使用同一 statistic 直接更新 auxiliary `N0`。
- B2 每个物理帧只能有一个 scalar，并由该帧两偏振共同 pilots 估计；同一帧的两偏振及全部 codewords 共享它。不得静默增加为 per-polarization、per-codeword 或 per-bit 自由度。

## C0–C6 必须测试

### C0 identity / labels / sign / noise factor

- 16 labels × 4 bits 的 mapper roundtrip 0 error；fingerprint 与 `codec_metrics.py` 完全一致。
- 每个 constellation point 的低噪 exact-APP LLR sign 等于 label。
- 手算 `y=0` ring-bit case 与 `N0`/`N0/2` 二倍因子；错误因子测试必须 RED。

### C1 max-log B2=B3

- 未裁剪、uniform/no-prior/common-variance/fixed-geometry 下，deterministic grid、4 bits、≥2 positive variances，float64 `max_abs<=1e-12`。
- 实际 placement receipt 单列并按目标 candidate 尝试闭合：`APSK demapper clip30 → B2 scale → decode_fresh clip30 → backend/input/internal clip20 → rate recovery + fixed filler`；若 live target seam 不能合法继承该合同，输出相应 B2-invalid/invalid-testbed terminal，不得悄悄移动 scalar 或裁剪位置救结果。
- 分别审计 `s<1` 与 `s>=1`。任何由 preclip placement 产生的非等价必须标为部署接口效应，不得写成新 LLR 变换。

### C2 exact-APP B2/B3 identity / non-identity

- 对 16 constellation points、origin、ring midpoint、axis/off-axis generic points和≥3 variance pairs逐 bit分类。
- origin 作 identity control；至少一个 bit 稳定 non-identity 才把 B3 exact APP 保留为 distinct comparator。全恒等只关闭 B3 分叉，不自动判 B2 PASS。

### C3 NMS homogeneity / nonhomogeneity controls

- 最小 unclipped/no-filler NMS graph 对 scales `{0.25,0.5,2,4}` message-by-message 正齐次、hard output一致。
- 目标 backend 分别核对 demapper/decode/backend clip 与 rate-recovery fixed filler 的准确位置、值、数量和 sign；当前源码预期为 BG2 `Z=104`、`k_ldpc=1040`、16 个 bit-0 filler LLR=`-20`，必须由 live receipt 验证。不得把 fixed `alpha=.75`、interleaver、punctured zero、20 iterations 错列为非齐次源。
- 用小数组/构造消息验证某个自然固定边界确可破坏 homogeneity；这只证明 action existence，不是 headroom。
- 解释性 adaptive threshold/filler clone 只核理论重参数化，不进入主 arms，也不自动否决 frozen-interface B2。

### C4 comparator parity

- B0/B1/B2/B3 共享 constellation、labels、pilots/statistic/window、codeword、decoder、clip合同与调用次数；B3 exact APP 只差 auxiliary `N0`。
- matched/no-mismatch negative control 下 receiver action 不得产生伪差。

### C5 truth firewall

- receiver API 禁止 true noise/SNR、payload bits/labels、decoder truth、future samples；这些只允许进入 test oracle/scorer。
- 突变 forbidden truth 时，每个 receiver arm 自身的 LLR/decode input 必须 byte-identical。

### C6 paired target codec receipt

- all-zero、single-one、walking-label、random codeword：`encode 1536 bits → APSK map → deterministic low-noise exact-APP → flatten → fresh decode` 的 bit order/sign/interleaver receipt成立。
- 所有 arrays finite；每 arm fresh-state，configured iterations/calls一致；记录 live Sionna version、BG/Z、out_int/out_int_inv hash、clip/filler合同与 hard-output hash。

## 禁止项

- 不跑真实/合成湍流、Jones、Ch3/Ch4 residual、natural occurrence 或任何 BER/FER/headroom grid。
- 不选择/调 pilot count、scalar mapping、clip、decoder alpha/iterations。
- 不新增损伤，不改 Ch3/Ch4、Skill/controller、正式论文正文、`common/`、全局 params 或旧实验结果。
- 不以构造 sample 的 decoder flip、高 SNR roundtrip、GMI/ASI 作为性能证据。

## 唯一 terminal

1. `CORRECTNESS_PASS_B2_ACTION`：C0–C6 全 PASS，target APSK codec receipt闭合，真实冻结接口含自然固定非齐次边界，B2 placement/action 有效；B3 exact APP identity/non-identity 如实记录。只允许主控另开单格 headroom。
2. `CORRECTNESS_B2_INVALID_B3_REMAINS`：target receipt闭合，但 B2 仅是理想零效应、错误 placement 或目标接口不存在固定非齐次作用；B3 exact APP 至少一个 bit稳定 non-identity。禁止性能，回主控显式迁移身份。
3. `CORRECTNESS_FAIL_NO_DISTINCT_ACTION`：target receipt闭合，但 B2 无合法 action 且 B3 exact APP 也无 distinct action。关闭 C5-0。
4. `INVALID_TESTBED`：label/sign/noise factor/bit order/backend 或 dependency 无法在时限内正确闭合。列出一个最小 blocker，不跑性能补洞。

## 时限、验证与提交

- 墙钟 60 分钟；前 15 分钟完成 RED 与接口 inventory，40 分钟前 GREEN/terminal，余下时间做独立 reviewer 和收口。
- 独立 reviewer 必须只审 C0–C6、action identity、禁止性能与唯一 terminal；P0/P1 修到 0，P2 记 debt。
- 运行 targeted tests、task-control validator、`git diff --check`、source/reference receipt 与 scope/diff 白名单。
- worker log 必须记录 RED→GREEN、实际命令、测试数、terminal、blocker/debt；一次 commit，不 push。
