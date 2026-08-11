# Step 078 — C1 Step 3.5 convergence round 2

> 2026-08-09 | T032 / CP009 / epoch 9 | `ROUND2_NOT_CONVERGED_NEW_FULLTEXT`

## 1. Control 与范围

- Fresh validator：`PYTHONDONTWRITEBYTECODE=1 python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T032-c1-step3_5-convergence-round2.md` → `PASS`。
- 已读 `gw-supplement`、`tools-guide` §1–2、topic-index、D008、step-067–076 及相应 read notes；用 DOI/arXiv/title 对 round1、引文链、physical/B2 与已知全文家族去重。
- 本包只做 search/abstract crosscheck；未下载全文、未改中央 owner/治理/代码、未实验、未 stage/commit/push、未触碰 `p05`。

## 2. 八 query 与 source receipts

| ID | query | Crossref | 第二来源 / receipt |
|---|---|---:|---|
| q01 | Markov cycle-slip state turbo demodulation LDPC boundary localization | 10 | arXiv exact=0 |
| q02 | phase-slip-aware differential BCJR SC-LDPC windowed local repair | 10 | arXiv exact=0 |
| q03 | block-symmetric LDPC phase-slip transparent segment correction | 10 | arXiv exact=0 |
| q04 | Tikhonov mixture slip confidence decoder change point recovery | 10 | arXiv exact=0；mechanism-preserving `phase noise LDPC` supplement=20 |
| q05 | pilot phase unwrapping cycle-slip PAPU FEC local correction | 10 | S2 exact DOI crosscheck=1 |
| q06 | unsatisfied parity check syndrome cycle-slip localization | 10 | Crossref有效；无相关抽象命中 |
| q07 | cumulative-average phase-slip boundary decoder reprocessing | 10 | Crossref有效；均为词义假阳性 |
| q08 | decoder anomaly phase candidate suffix selective re-decode | 10 | Crossref有效；均为异域假阳性 |

- S2 search 与 OpenAlex fresh 首次均 `HTTP 429`，receipt 分别为 `...r2-s2-receipt.json`、`...r2-openalex-receipt.json`；按止损规则没有重试，也没有把 429 当零结果。
- 有效来源为 **Crossref + arXiv**；另对新 DOI `10.1364/OFC.2015.TU3B.2` 的 S2 exact endpoint 得到 HTTP 200 identity，但 `abstract=null`。
- 所有 raw/annotated JSON 均位于 `search-archive/2026-08-09/coded-decoder-c1-step3_5-convergence-r2-*.json`。

## 3. Raw / unique / known / new

| count | value | 口径 |
|---|---:|---|
| raw | 101 | Crossref 80 + arXiv 20 + S2 exact-DOI 1；429/零结果不计 |
| identity unique | 97 | lowercase DOI；否则 arXiv 去 version；否则 normalized title |
| known identity | 6 | 与 round1/Step3.5 integrated receipts exact match |
| metadata-new unique | 91 | identity 层新；多数为词义/异域假阳性 |
| domain-plausible truly new | 2 | 经题名/abstract 与已知家族去重后 |
| new MUST / SHOULD | **0 / 2** | MUST 要求 abstract 可能同时命中 explicit boundary + bounded local carrier action + decoder interaction |

已知家族不重报：OFC 2014→OFC 2015→arXiv 1704，ECOC 2014，ICTON 2016，arXiv 1204/1306，CSSC/CS-DC，PAPU，TVT/TWC/TSP。新召回 `arXiv:1210.5198` 与 1204/1306 为同作者 multiple-hypothesis/Tikhonov-mixture 家族成员，按 family alias 合并，不计新增 SHOULD。

## 4. 真正新候选八字段（2）

### N1 — arXiv `2604.07004v1`（`SHOULD_FULLTEXT`, priority 1）

*Channel Estimation and LDPC Decoding for Bursty Phase Noise*, Han Cui / Frank R. Kschischang / Magnus Karlsson / Erik Agrell, 2026。官方 arXiv abstract pointer：`...r2-arxiv-effective2.json:L001`。摘要支持 bursty differential phase-noise model、burst-aware LDPC，以及 channel estimation↔LDPC iterative IBA；不支持 explicit boundary 或 bounded local carrier action。

| input | trigger | localization | action | decoder interaction | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| coded observations + bursty differential phase noise + LDPC messages | fixed BA/IBA；event trigger未述 | burst awareness；boundary/index未述 | channel estimation + BA LDPC；local carrier correction未述 | iterative channel estimation↔LDPC | 未述 | 摘要未述 | BER/PER/bits；无 boundary/local output |

裁决：近期、机制不同且可能吸收“bursty impairment + decoder interaction”，是清晰强邻居，故 SHOULD；但缺 boundary/local action，不能 MUST、不能靠摘要判 exact。

### N2 — DOI `10.1364/OFC.2015.TU3B.2`（`SHOULD_FULLTEXT`, priority 2）

*Cycle Slip Tolerant, Differential Encoding Aware Soft-Decision FEC*, A. Bisplinghoff et al., OFC 2015。Crossref q05 item 3 与 S2 exact DOI 身份一致；S2/Crossref 均 `abstract=null`。

| input | trigger | localization | action | decoder interaction | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| UNKNOWN | UNKNOWN | UNKNOWN | 题名仅称 cycle-slip tolerant / differential-encoding-aware；机制 `AI推断，未验证` | 题名仅称 soft-decision FEC；接口 `AI推断，未验证` | UNKNOWN | UNKNOWN | UNKNOWN |

裁决：直接 optical/FEC/slip 题名且是新身份，足以列 SHOULD 获取债；摘要为空，绝不把它晋级 MUST 或 exact-chain candidate。

## 5. 其他新身份未晋级

| identity | abstract-backed screening | disposition |
|---|---|---|
| `arXiv:1210.6267` | coded SISO/MIMO EM + EKF/EKFS global phase tracking；无 slip boundary/local action | `NOT_PROMOTED_GLOBAL_TRACKING` |
| `10.1109/TCOMM.2019.2909201` / `arXiv:1908.02816` | noncoherent multi-symbol detection + nonbinary LDPC joint graph；无 slip/local repair | `NOT_PROMOTED_PHASE_NOISE_CODE` |
| `arXiv:1308.3772` | coded-MIMO EM/EKFS iterative phase-noise tracking；无 boundary/selective local re-decode | `NOT_PROMOTED_GLOBAL_TRACKING` |
| `arXiv:1210.5198` | multiple-hypothesis mixture reduction；与 1204/1306 已知 Tikhonov family 重合 | `KNOWN_FAMILY_ALIAS` |

Crossref 其余新 identity 为普通 LDPC/SC-LDPC、GNSS/InSAR cycle slip、材料/流体“slip”、量子 LDPC 或 NLP/vision suffix/anomaly 等词义假阳性；不列候选，也不作功能断言。

## 6. 收敛裁决与 claim ceiling

- `new MUST_FULLTEXT=0`，`new SHOULD_FULLTEXT=2`，所以**不能**使用 `ROUND2_CONVERGED_ZERO_NEW`。
- 下一全文优先级：N1（abstract-backed burst-aware iterative chain）→ N2（direct title but abstract-null debt）。两篇全文前均不能裁 exact complete-chain collision。
- Round2 strongest new=N1；它目前只占 burst-aware joint estimation/decoding 邻域，不证明 within-frame slip boundary、bounded suffix candidate reevaluation、clean no-op 或 selective re-decode。

## 7. Coverage limitations 与保护

- S2/OpenAlex 搜索 429；Crossref 的长 conjunctive query 假阳性高；arXiv 对四个长串均零召回，故用保留 phase-noise+LDPC 机制的短式补充。零召回不等于不存在。
- N2 没有 abstract；其八字段除题名词面外全部 fail-closed。没有 DOI/arXiv/S2 abstract 支持的机制统一标 `AI推断，未验证` 或 UNKNOWN。
- 未下载全文；未改 central owner/治理/代码；`p05` 与 staging 需 fresh 终验。

`ROUND2_NOT_CONVERGED_NEW_FULLTEXT`
