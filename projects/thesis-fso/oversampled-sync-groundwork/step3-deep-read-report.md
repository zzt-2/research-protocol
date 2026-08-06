# GW Step 3：7 篇 CORE 全文精读与问题裁决

> 日期：2026-08-06
> 证据：`projects/thesis-fso/worker-logs/step-3-sync-read-{a,b,c}.md`
> 边界：只做 Step 3；未进入 Step 3.5、Step 4a、方法实现、testbed 或仿真。

## 1. 精读身份结果

| CORE | identity/title | receiver-visible information | action / output | 时序与关键边界 |
|---|---|---|---|---|
| Tang 2022, `10.1109/JPHOT.2022.3161795` | PASS | 1-sps、前级 clock sync/equalization 后的接收样本 + known STSB | frame index → CFO estimate/correction | `clock sync → frame → FOE`；无 fractional timing/SCO |
| Paillier 2020, `10.1109/JLT.2020.3003561` | title-unverifiable，主题人工 PASS | symbol-rate I/Q、power、AGC/DPLL states | continuous AGC + phase NCO；carrier stream | ideal timing；无 timing loop/hold/reacquire |
| Wang 2023, `10.1109/JPHOT.2023.3265847` | PASS | 1-sps dual-pol/multi-branch samples + known FSTS | branch frame indices → coarse/fine CFO | FS→MRC/pol-demux→FOE；无 fractional timing/SCO |
| Wang 2024, `10.1364/OE.520452` | PASS | downsampled samples + stored PRBS/cyclic-QPSK | frame peak → coarse/fine CFO | Rx 先 downsample；symbol-rate FS→FOE |
| Valjus 2025, `10.1002/sat.1553` | PASS | oversampled samples、TED/loop history、pilot/preamble、power/SNR | independent timing NCO, CPE/FOE corrections | 各子系统单独仿真；quasi-static fade；无联合恢复轨迹 |
| Le Bidan 2023, `10.1109/ICSOS59710.2023.10490279` | PASS | blind 2-sps samples + known headers/pilots | CFO bank、timing/interpolation、FSE、frame、fine CFO、CPE | 完整顺序链：2 sps timing/SCO 后 downsample，再 frame/fine CFO |
| Sun 2025, `10.1109/JLT.2025.3533197` / arXiv `2409.14400` | PASS | TS-A/TS-B known preamble；CE 阶段 2-sps | Godard clock → frame → CFO → channel/equalizer | “joint”是同 training unit 复用；不是 `(frame,τ,CFO)` 联合 action |

逐篇标准 14+ 字段、七子表、通信参数与实验完备性见全局 `papers/_read_notes/`；本轮原始结构化提取见三个 worker log。

## 2. Q1：sample-level frame–fractional-timing–CFO acquisition

### 2.1 M-C-A

- **M**：Le Bidan 2023 的 `2-sps coarse CFO → matched filter → Lee timing/interpolation → FSE/downsample → frame → fine CFO` 顺序链；frame/CFO 子链以 Sun 2025 CAZAC 或 Wang 2023/2024 FSTS/mixed-TS 为近期 task-matched comparator。
- **C**：RRC、≥2 sps 的 coherent FSO burst/acquisition，未知 fractional timing、frame offset 与 CFO 同时存在。
- **A**：顺序链假设 timing 可先独立恢复且不会因 frame/CFO 未知而失效；若该假设不成立，才产生联合 sample-level action 的问题。

### 2.2 canonical 四判据

| 判据 | 结果 | 正文证据与理由 |
|---|---|---|
| 1 具体技术矛盾 | ❌ | 7 篇 CORE 没有给出强顺序链在上述 C 下的量化失效。GEO 2023 反而证明 2-sps timing/SCO→frame→CFO 顺序链可成立；当前 A 只是待证假设。 |
| 2 方法产出形态 | ✅（形态） | 显式联合 likelihood/metric 或可验证的 coarse-to-fine coupled estimator 可形成可复用算法；仅共享 preamble/调序不算。 |
| 3 2019+ task-matched baseline | ✅ | GEO 2023 是完整顺序链；Sun 2025 是最近 clock/frame/FOE burst comparator；Wang 2023/2024 是 FSO frame+FOE comparator。 |
| 4 可量化对标 | ✅（形态） | acquisition success、frame miss/false lock、timing/CFO error、BER、overhead、latency、complexity 可同输入比较。 |
| **四判据** | **未全过** | 判据 1 FAIL；Q1 不是 Step 3 survivor。 |

### 2.3 最强 comparator 与 delta

最强廉价 comparator 是 `2-sps coarse CFO + Lee/Gardner timing/interpolation + FSE/downsample + Sun 2025 CAZAC（或 FSTS/STSB）frame/FOE`。Sun 已占用“同一 preamble 支撑 clock/frame/frequency”的资源共享表述；若候选只合并框图、共享序列、中间量或调整顺序，剩余 delta 是 implementation ordering/resource integration，不是已证实的 joint action。

## 3. Q2：fade+SCO 下 timing/carrier maintenance 与 reacquisition

### 3.1 M-C-A

- **M**：Gardner/Gu timing loop 与 Paillier AGC+DPLL、VV/FOE carrier loop 独立运行；明显廉价扩展是 receiver-visible quality threshold 下 shared freeze，并按固定 preamble/reference 周期重启。
- **C**：≥2-sps RRC coherent OSL，持续 SCO/drift、CFO/Wiener PN，并经历 dynamic deep fade。
- **A**：fade 同时污染 TED 和 carrier detector，独立积分器共同/异步失锁，且 shared freeze+fixed reacquisition 仍不足。

### 3.2 canonical 四判据

| 判据 | 结果 | 正文证据与理由 |
|---|---|---|
| 1 具体技术矛盾 | ❌ | Paillier 只量化 carrier DPLL 的 fade 失稳；Valjus 分别讨论 timing/carrier，且 quasi-static/独立仿真。没有共同失锁或 cheap comparator 不足的正文证据。 |
| 2 方法产出形态 | ✅（形态） | shared-confidence update/hold/reacquire FSM、lock indicator 与恢复准则可形成可复用算法/设计规则。 |
| 3 2019+ task-matched baseline | ❌ | Gu 2019、Paillier 2020、Valjus 2025 分别覆盖 timing、carrier 或综述；没有 2019+ integrated maintenance/reacquisition comparator，跨论文拼接不能冒充已验证 baseline。 |
| 4 可量化对标 | ✅（形态） | timing/SCO/CFO/CPE error、cycle-slip、BER、lock-loss rate、post-fade recovery time 可量化；本 CORE 只给部分单环指标。 |
| **四判据** | **未全过** | 判据 1、3 FAIL；Q2 不是 Step 3 survivor。 |

### 3.3 最强 comparator 与正文边界

最强 comparator contract 是 Gardner/Gu timing + AGC/DPLL/VV/FOE，并以同一个 receiver-visible quality threshold 共同冻结，再按固定 known preamble/reference 重启。它尚未作为完整链被本组论文测试，因此既不能写成“已解决”，也不能写成“已经失效”。Paillier 的约 1.4 ms 是初始 carrier capture，不是 post-fade 双环 reacquisition。

## 4. Step 3.5 与 JOCN 2026

Step 3 没有 survivor，故 D004 的条件门不满足，**Step 3.5 未启动**：没有执行关键词矩阵、双向引用链或新论文获取，也没有对 JOCN 2026 开启新一轮抓取。JOCN 2026 保持 `UNRESOLVED_HIGH_RISK`；既不以 abstract 作 exact-action collision 裁决，也不循环突破既有三路径止损。

## 5. Step 3 终态

`STEP3_NO_VALID_PROBLEM`

Q1、Q2 均未通过 canonical 四判据，唯一 survivor：**无**。因此不存在 Step 4a 入口，本轮在 Step 3 停止。
