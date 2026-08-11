# Step 070 — C1 FEC-assisted cycle-slip fulltext pair

> 2026-08-09 | T024 / CP009 / Groundwork Step 3.5 | `PAIR_FULLTEXT_READ`

## 1. Scope 与 fresh control

- 唯一工作树：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。
- 已读：`stages/gw-acquire.md`、`stages/gw-read.md`、`stages/gw-supplement.md`、topic-index、D008、step-069、RDL long-horizon-control 与 mission-log。
- Fresh validator：`PYTHONDONTWRITEBYTECODE=1 python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T024-c1-fec-cycle-slip-fulltext-pair.md` → `PASS`。
- Control：epoch 9 / CP009 / `GROUNDWORK_STEP3_5_SUPPLEMENT`；只执行 `FULLTEXT_READ`。未改中央 owner/治理/代码，未运行实验，未 stage/commit/push。

## 2. Acquisition receipts 与正文质量

| Paper | Channel | Receipt | 结果 |
|---|---|---|---|
| `10.1364/OFC.2014.M3A.3` | 1. `tools/download --doi` | normalized target=`papers/doi/10.1364_ofc.2014.m3a.3` | `all_failed`，如实保留 |
| 同上 | 2. `tools/blit --source ieee` exact title | IEEE Xplore doc 6886573；208273-byte PDF | 成功，使用2/3合法渠道 |
| `10.1109/ICTON.2016.7550341` | 1. `tools/download --doi` | normalized target=`papers/doi/10.1109_icton.2016.7550341` | `all_failed`，如实保留 |
| 同上 | 2. `tools/blit --source ieee` exact title | IEEE Xplore doc 7550341；321892-byte PDF | 成功，使用2/3合法渠道 |

- 两次 `tools/blit` 自动 `TITLE-MISMATCH` 均由页眉/版权行误判。`pdfinfo` 的 Title逐词匹配目标，Subject分别明列 DOI；首页题名/作者也逐项匹配，故人工 title gate=`PASS`。
- 按 `tools/convert --quality fast` 转换：OFC=`328 lines / 18352 bytes`；ICTON=`146 lines / 20419 bytes`。均包含 method/algorithm、全部 figures、simulation/measurement 与 conclusion。
- PDF视觉核验：OFC pp. 1/3；ICTON pp. 1/4。题名、方法框图/曲线、结论清晰；正文抽取中的少量公式字符乱码不影响本任务字段。

## 3. OFC 2014：正文事实（8 条）

1. Slip源于 blind V&V CPR的 phase-state transition；论文先在5230-km coherent fiber实验测 occurrence，再在仿真中用 Markov transition model注入，不是 decoder生成的 slip。
2. 10.7-GBd DP-QPSK测量中，FEC-limit区 pre-FEC BER>`10^-2`时 slip rate>`10^-3`，且至少约为 pre-FEC BER十分之一。
3. Markov max-log-MAP trellis同时读 scattered pilots/data并隐式跟踪 slip states；可容纳多次 transition，但不输出 boundary/direction/affected suffix。
4. LDPC VND/CND做 inner BP，VND soft LLR通过 outer loop反馈至 MAP demodulator；最终输出 full-codeword decoded bits。
5. 无 event trigger、clean no-op、confidence abstention或 failure-conditioned fallback；DQPSK/更多pilot/长interleaver只是 baseline/设计替代。
6. 公平预算为无turbo `32 inner` 对比 turbo `4 inner × 8 outer`；另付1/2/3% pilot overhead，trellis operation/latency未给。
7. 3% pilot时 turbo gain=`1.05 dB` @ post-FEC BER `10^-5`，距 ideal QPSK=`0.3 dB`；比无turbo DQPSK好1.4 dB、比turbo DQPSK好0.6 dB。
8. Collision=`PARTIAL_CORE_ONLY`：占用 slip-aware Markov demod + LDPC feedback core，不含 explicit local boundary、segment/suffix action与 fallback。

## 4. ICTON 2016：正文事实（9 条）

1. 物理叙述是 laser phase noise + XPM大phase jump让CPR跳至相邻 `pi/2` stable point；simulation显式用 uniform random CS probability注入。
2. Differential QPSK消除 stable-point ambiguity，但AWGN error会error doubling；CS导致DD channel sequence与LDPC a-priori矛盾并诱发outer-loop reliability oscillation。
3. 方法不估 phase/slip；核心是 regular `(3,20)` length-20000 rate-0.85 LDPC的layered scaled-min-sum schedule。
4. 每outer iteration存estimated codeword并计unsatisfied checks；count恶化时保留旧codeword，若旧count<10则停止并输出last best。
5. 无 slip trigger/boundary/phase candidate/local suffix repair；正文明确说把phase recovery纳入iterative decoder因复杂度似乎不可行。
6. 预算=`N_outer<=15`、`N_inner=1..4`；layered在no-slip时把所需outer/DD steps约减30%；主stop方案每outer为2 inner。
7. 无stop时1/2 inner的error floor近`10^-3`且错误帧平均>1000 errors，clean-up code失败；3 inner仍会oscillate。
8. layered在`P_CS<=2×10^-3`大致可容忍，更高概率不稳定；layered+stop在`10^-3`取得<`10^-7` error floor、最大weight 4，可由2% clean-up code处理。
9. Collision=`STRONG_NEIGHBOR`：有全码字decoder fallback/预算但没有carrier local-repair core。

## 5. 八字段并排裁决

| 字段 | OFC 2014 | ICTON 2016 |
|---|---|---|
| input | V&V后observations + pilots/data + transition model + VND soft LLR | differential channel/decoder LLR + codeword + unsatisfied-check count |
| trigger | 固定outer loop，无event trigger | 固定turbo loop；check<10且count恶化触发stop |
| localization | trellis latent symbol state；无boundary输出 | whole-codeword / iteration；无slip localization |
| action | full-codeword Markov max-log-MAP LLR重算 | layered LDPC + reject worse whole-codeword / stop |
| decoder interaction | VND/CND inner BP + VND→MAP soft feedback | SISO differential MAP↔scaled-min-sum LDPC extrinsic |
| fallback | `NOT_STATED` | last-better codeword + outer clean-up code；非carrier fallback |
| budget | 4 inner×8 outer vs 32 inner；1–3% pilots；local cost未给 | <=15 outer，1–4 inner；threshold10；20% coding overhead |
| output | full-codeword LLR/decoded bits | final whole codeword/bits；无slip/boundary output |

两篇均只做 whole-codeword turbo processing，不实现 `detect/localize boundary → finite candidate correction → only segment/suffix reprocess → selective decode re-evaluation → fallback`。缺 local action/boundary（OFC另缺fallback）即足以阻断 exact。

## 6. Claim ceiling、保护与 terminal

- OFC claim ceiling：`PARTIAL_CORE_ONLY`；任何“decoder LLR + slip-aware Markov turbo demodulation”声称已被占用，但 Q1 complete local chain未被占用。
- ICTON claim ceiling：`STRONG_NEIGHBOR`；layered schedule、unsatisfied-check rollback/stop与clean-up code必须作为decoder-side absorption comparator，但不等于 local carrier repair。
- Pair：两篇均取得合格全文、逐字段完成，无 unresolved fulltext debt；未确认 exact complete-chain collision。
- p05：未修改，仅在终验读取哈希；4个冻结SHA256=`4/4 MATCH`。Git staging=`EMPTY`；并发 dirty/untracked未清理、未归因。PDF视觉核验临时目录经 absolute-path guard 后已删除，`TEMP_EXISTS=False`。

`PAIR_FULLTEXT_READ`
