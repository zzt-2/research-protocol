# Coded decoder-feedback Groundwork Step 3.5 补充检索报告

> 日期：2026-08-10  
> 专题：`.sessions/2026-08-09-coded-decoder-feedback-groundwork/`  
> 状态：`COMPLETE / INDEPENDENTLY_VERIFIED_WITH_COVERAGE_LIMITS`  
> 研究边界：只裁 C1 完整 deployable action chain 碰撞；不裁 defect occurrence、recoverability 或方法贡献

## 1. 结论先决条件

Step 3 已冻结的 Q1 不变：L01/L02 型全帧单一 finite phase-hypothesis decoder selection，在一帧内出现局部 constellation-symmetry slip / piecewise ambiguity 时，是否因无法同时对齐前后两段且不输出 boundary 而产生可恢复损失；receiver-visible decoder evidence 能否驱动有界局部 repair。

本步骤只比较以下完整签名：

`receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`

只有八字段全链等价才构成 exact collision。相同的 phase hypothesis、Markov slip state、decoder iteration 或局部误差容忍原子均不足以单独 Kill reference-method extension。

## 2. 检索充分性 receipts

| 门槛 | 执行事实 | 证据 |
|---|---|---|
| 关键词矩阵 | 9 组查询，覆盖 local boundary/segment repair、decoder/syndrome interaction 与 coherent-optical slip；Crossref + arXiv 为有效来源；raw 70、unique 63；初筛 MUST 2 / SHOULD 5，摘要级 exact 0 | `step-067-c1-step3_5-query-matrix.md` |
| 双向引用链 | 最高引用可读核心 L05/TWC 2004；forward 58 中 11 篇有摘要，backward 21 中 1 篇有摘要；共筛 12 篇，新增 MUST 0 / SHOULD 1 | `step-068-c1-step3_5-citation-chain.md` |
| physical/B2 | 6 个来源；OFC/ICTON 给 slip-rate/phase-slip 模型邻接证据，PAPU/CSSC/CS-DC 给 pilot/non-data-aided B2 候选，JLT 2020 给 coherent-FSO 参数锚 | `step-069-c1-step3_5-physical-b2.md` |
| Round 2 | 8 个精确机制查询；raw 101、unique 97、known 6、metadata-new 91；新增 MUST 0 / SHOULD 2 | `step-078-c1-step3_5-convergence-round2.md` |
| Round 3（上限） | 8 个全文术语查询；Crossref 80 + arXiv 2，raw 82、unique 79、known/family 7、metadata-new 72；新增 MUST 0 / SHOULD 1 | `step-080-c1-step3_5-convergence-round3.md` |

Round 3 的唯一 SHOULD 为 OFC 2017 `10.1364/OFC.2017.W2A.56`。全文已在上限轮之后作为 acquisition debt 单独关闭，没有启动第 4 轮搜索。第三轮搜索执行 agent 超时且未落盘；独立 salvage 只读既有 receipts 离线复算并记录该操作债，未将聊天回报当作证据。

## 3. 新增全文与方法家族裁决

| 证据/家族 | 全文 verdict | 承重事实 | 缺失的完整链字段 |
|---|---|---|---|
| OFC 2014, `10.1364/OFC.2014.M3A.3` | `PARTIAL_CORE_ONLY` | Markov slip-state trellis + LDPC soft feedback；whole-codeword fixed turbo schedule | decoder-anomaly trigger、explicit boundary、bounded local carrier action、conditional fallback |
| ICTON 2016, `10.1109/ICTON.2016.7550341` | `STRONG_NEIGHBOR` | layered LDPC + unsatisfied-check rollback/stop | carrier-state localization、local phase correction、repair output |
| TCOM 2015 / arXiv 1306.3693 | `STRONG_NEIGHBOR` | per-symbol Tikhonov-mixture phase tracking、pilots/phase recapture、full-sequence decoder loop | event boundary、local rollback/selective re-decode |
| arXiv 1204.2660 | `PARTIAL_CORE_ONLY` | whole-codeword joint phase/LDPC message passing；per-symbol confidence | boundary/range、failure-triggered local action、fallback |
| ECOC 2014, `10.1109/ECOC.2014.6963875` | `STRONG_NEIGHBOR` | block-symmetric LDPC phase-slip tolerance | slip localization、carrier correction、selective repair |
| OFC 2015 Th3E.6 → arXiv 1704.04618 | `PARTIAL_CORE_ONLY` | model-matched slip BCJR + LDPC/SC-LDPC code-graph window | slip-boundary-local repair；window 是固定码图波而非 detected segment |
| OFC 2015 Tu3B.2 | `STRONG_NEIGHBOR` | differential coding 将 slip 后果限制为 local error event；HTDD 固定执行 TDD→plain-LDPC cleanup | 无 boundary 输出、carrier samples 修正、条件触发/fallback |
| arXiv 2604.07004 | `PARTIAL_CORE_ONLY` | Gilbert–Elliott Markov-modulated Wiener burst state；逐符号 G/B posterior + 全序列 IBA LDPC feedback | burst 不是 discrete slip；无 phase candidate/rotation、局部 reprocess、clean no-op |
| PAPU, `10.3390/app9132749` | `STRONG_NEIGHBOR / B2_TASK_MATCHED` | 0.78% pilot；per-127-symbol；filter `{4,8,16,20,32,48}`；pilot unwrap/post-unwrapping | 无 decoder feedback；精确插值/阈值公式仍欠 Cheng 2013 |
| OFC 2017, `10.1364/OFC.2017.W2A.56` | `STRONG_NEIGHBOR` | pilots + 4-state Markov soft slip probability + fully-parallel bit-LLR marginalization | 明确 no decision feedback；无 event trigger、boundary/range、local sample repair、selective redecode/fallback |
| JLT 2020, `10.1109/JLT.2020.3003561` | `NOT_COMPARABLE / PHYSICAL_ANCHOR` | HV/Bufton/TURANDOT + AO、paired 2 s `rho/phi`、100 MHz residual CFO、AGC/DPLL；fading 稳定门槛约移 5 dB、BER penalty 2.3 dB | 未建模 discrete slip，不能支持“湍流导致 slip”因果声称 |

全文身份、算法、参数、八字段和 claim ceiling 见 `papers/_read_notes/`；执行日志为 `step-070`–`step-081`。arXiv 1704 的初始 unresolved 是 downloader/read 竞态；随后以 143,913-byte 正文和 SHA receipt 关闭，历史 chronology 保留在 `step-077`。

## 4. 八字段合成

| 字段 | 检索切片已覆盖 | Q1 extension 仍未被覆盖的组合 |
|---|---|---|
| receiver-visible input | samples/CPE output、pilots、demodulator LLR、syndrome、decoder soft messages | receiver-only decoder anomaly 与 carrier observations 的冻结接口 |
| trigger | 多为 always-on 固定迭代；少量阈值/stop 作用于 decoder schedule | defect-conditioned trigger + clean abstention |
| localization | per-symbol phase/burst/slip-state posterior、统计峰、码图 window | 显式 onset/boundary + affected range，且可驱动 action |
| candidate action | BCJR/Tikhonov/LLR marginalization、differential tolerance、pilot unwrap、global bank | 有限 local phase hypotheses 对 detected segment/suffix 的 rotate/remap/re-evaluate |
| decoder interaction | full-codeword fixed outer iterations、one-way refined LLR、rollback schedule | 只重评 touched region/codeword 的 bounded decoder comparison |
| fallback | 大多未陈述；HTDD/PAPU 为固定 schedule | failure-conditioned B1/B2 fallback + clean no-op |
| budget | 全流迭代、pilot overhead 或 parallel 声称 | local candidate/decode-call/latency 的硬上界和 matched ledger |
| output | decoded bits/BER、phase trajectory、refined LLR/corrected stream | boundary + selected local repair + abstain/failure outcome |

`PROVISIONAL_COLLISION_VERDICT = NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE`。

这不是“领域中不存在”的 novelty closure。它表示在已执行的直接全文、双向引文链、三轮定向查询和全部 MUST/SHOULD debt 中，没有确认与 Q1 同 input、同 trigger、同 boundary/range、同 local carrier action、同 decoder re-evaluation、同 fallback 与相当预算的完整链。

## 5. Physical / B2 可承重边界

- OFC 2014 报告在其 measured optical setup 中，pre-FEC BER 高于 `1e-2` 时 cycle-slip rate 可高于 `1e-3`；其 synthetic model 使用 slip rate 为 pre-FEC BER 的 0.1 倍，并比较 1–3% pilots。该数字只能锚定 coherent-optical stress order，不可直接移植为 coherent-FSO 常数。
- ICTON 2016 使用 synthetic PCS `1e-3`–`4e-3`，可作相邻 sensitivity range，不证明目标 FSO receiver 自然产生同分布 slip。
- PAPU 给出 topology-matched pilot B2 的可实现预算锚；OFC 2017 给出另一个 no-decoder-feedback pilot soft-state/LLR B2。二者必须在 Step 4a 以独立 dev 调谐、同 receiver-visible 信息和真实成本比较。
- JLT 2020 只锚定 coherent-FSO turbulence/AO/CFO/DPLL 参数与 fading penalty。若无 trace，可做 parameter-anchored synthetic approximation，但必须把 turbulence/fading 与 injected discrete symmetry slip 分成两个因素，禁止声称前者已被证明导致后者。

## 6. 覆盖限制与未关闭债

1. CSSC-CPE `10.1109/ACCESS.2019.2934224` 与 universal CS-DC `10.1364/OE.22.031167` 经三条合法通道仍为 `UNRESOLVED_FULLTEXT`；只能保留 identity-level B2/near-neighbor，不能冻结其算法、参数或完整链吸收结论。
2. SPIE `10.1117/12.3107192` 与 ACCESS 2026 U02 仍不可得；现有 metadata 不支持 exact collision。
3. PAPU 的精确 integer/interpolation/threshold equations 欠其 2013 predecessor；Step 4a 若实现 PAPU-like B2，必须标为 topology-matched independent implementation，而非 exact reproduction。
4. S2/OpenAlex 在部分轮次为 429/timeout；有效 query coverage 主要来自 Crossref + arXiv。raw/unique 是受限结果集的可复算计数，不是领域 recall 声明。
5. 第 3 轮新增 SHOULD 非零，因此形式终态为 `ROUND3_CAP_REACHED_WITH_NEW`，不是 `CONVERGED_ZERO_NEW`；但唯一新增已全文裁为 non-exact。按用户已授权的“限制进入”规则，本项不自动构成 NO ENTRY。

## 7. Step 4a 入口裁决

T036/step-082 与 T037/step-083 两个 fresh-context verifier 均为 `PASS, P0/P1/P2=0/0/0`。D009/V003 因而把 Step 3.5 按“达到三轮上限、全部新增 debt 已裁、无 exact complete-chain confirmed、带四项覆盖限制”完成，并只授权 Step 4a A0 §0–§6。

Step 4a 必须重新证伪以下 UNKNOWN，任何一项失败都形成真实 hard terminal，而不是强构方法：

1. 合法目标条件下，B0/B1 是否确有 within-frame local symmetry-slip defect；
2. O1 是否证明该损失有 recoverable headroom；
3. PAPU/OFC2017-like B2 与 independently tuned global retry 是否已吸收 defect；
4. receiver-visible decoder metric 是否能定位/区分异常，且 caller→callee 无 truth leakage；
5. 最小 coded-chain + carrier/action adapter 是否仍在 3–7 日预算内。

控制面已转为 CP010/epoch10 的 `GROUNDWORK_STEP4A_A0_PREFLIGHT`。adapter、defect smoke、MVE 和实验继续禁止；只有 A0 §0–§6 无致命信号并另立控制决策后，才能开放最小 defect smoke。
