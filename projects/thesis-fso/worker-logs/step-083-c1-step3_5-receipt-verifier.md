# Step 083 — C1 Step 3.5 fresh-context receipt / physical verifier

> 2026-08-10 | T037 / CP009 / epoch 9 | `PASS`

## 1. Control、范围与结论

- Fresh task-control validator：`PASS`；binding=`rdl.task-control.v2 / FULLTEXT_READ / epoch 9 / CP009`。
- 本次只读磁盘 receipts、worker logs、本地全文及中央 owner；未使用此前聊天回报作证据，未联网、搜索、下载、实验、提交、push 或触碰中央文件。
- `verdict=PASS`；`P0=0 / P1=0 / P2=0`。
- 该 PASS 只接收 Step 3.5 evidence package 与 claim ceiling；不自行修改 D/V/CP，不等于 Step 4a、adapter、defect smoke 或任何科学结果已经获准/通过。

## 2. 检索充分性与双向引文链

### 2.1 Round 1 query matrix

- 关键词矩阵为 9 queries，覆盖 3 个机制变体及每个变体至少 2 类 scenario/locality；实际有效来源为 Crossref 与 arXiv。证据：`projects/thesis-fso/worker-logs/step-067-c1-step3_5-query-matrix.md:34-46`。
- 有效 raw 复算：Crossref `8×6 + 1×0 = 48`，arXiv `1+2+5+3+0+5+0+5+1 = 22`，合计 `48+22=70`。
- 原始容器异常已独立核清：`coded-decoder-c1-step3_5-qm-api-round1.json` 的 q04 把 3 条 arXiv rows 错挂到 `crossref.items`，同时 `arxiv.items` 留有 1 个空对象；剔除空对象并按非空记录来源归位后仍为 70。该异常及 supplement 处置已在 `step-067:96-102` 明示，未被静默删除。
- DOI 优先、否则去版本 arXiv id、否则 normalized title 去重；7 个重复减项后 `70−7=63`。annotated shortlist 逐类计数为 `MUST=2 / SHOULD=5 / abstract exact=0`；与 `step-067:52-61` 及 `search-archive/2026-08-09/coded-decoder-c1-step3_5-qm-annotated-round1.json` 一致。

### 2.2 最高引用核心竞品的 forward/backward

- 同一 S2 endpoint/字段下，L05/TWC 2004=`58` citations，高于 L02/TSP 2006=`37`，故 seed 选择 L05；见 `step-068-c1-step3_5-citation-chain.md:18-21` 和 `coded-decoder-c1-step3_5-citation-seed-counts.json`。
- forward 实际返回 58，含 abstract 11；backward 实际返回 21，含 abstract 1；两方向均执行且非空，合计筛 `11+1=12 >=10` abstracts。见 `step-068:23-36`、`coded-decoder-c1-step3_5-citation-forward-s2.json`、`coded-decoder-c1-step3_5-citation-backward-crosscheck.json`。
- screening JSON 逐条 12 项，`new MUST/SHOULD=0/1`；TCOM 2015 是唯一新增 SHOULD，未被摘要越级为 exact collision。见 `step-068:42-55,72-78,86`。
- S2 citation edge 只对 5 个技术相关 DOI 用 Crossref reference list 独立核验；其余 S2-only 边不承重。OpenAlex backward 为 rate-limited，保留失败 receipt，未写成零结果。

## 3. 三轮离线计数复算

| round | raw 公式 | unique 复算 | known/family → metadata-new | new MUST/SHOULD | 验收 |
|---|---:|---:|---:|---:|---|
| R1 query matrix | `48 Crossref + 22 arXiv = 70` | `70−7 duplicates=63` | 本轮初始补检，不作跨轮 known 减项 | `2/5` | PASS |
| R2 | `8×10 Crossref + 20 arXiv + 1 S2 exact = 101` | `101−4 duplicate rows=97` | `97−6=91` | `0/2` | PASS |
| R3 | `8×10 Crossref + 1+1 arXiv = 82` | `82−3 duplicate rows=79` | `79−7=72` | `0/1` | PASS |

### 3.1 R2 细目

- 四个重复减项可从 raw receipts 复现：ECOC 2014 同 DOI 出现 3 次（减 2）、OFC 2015 Th3E.6 出现 2 次（减 1）、OFC 2015 Tu3B.2 的 Crossref 与 S2 exact 身份重复（减 1），故 `101−4=97`。
- `known/family=6` 的实际构成是 5 个 prior exact identities 加 `arXiv:1210.5198` 这一已知 Tikhonov-mixture family alias；annotated 的 `family_collapses` 与 worker-log 后文均显式说明，故 `metadata-new=97−6=91`。表头“known identity”不能脱离这段 family 口径单独解读。证据：`step-078-c1-step3_5-convergence-round2.md:30-39,70` 与 `coded-decoder-c1-step3_5-convergence-r2-annotated.json`。
- 两个真正新候选为 `arXiv:2604.07004` 与 `10.1364/OFC.2015.TU3B.2`，均是 SHOULD、非 MUST；后续 step-079 已全文裁为 non-exact。

### 3.2 R3 细目与唯一新增身份

- 三个重复减项：`arXiv:2604.07004` 在 q01/q03 重复；`10.1109/APCC.2006.255801` 与 `10.1109/LCOMM.2010.091710.101062` 均在 q02/q03 重复。因此 `82−3=79`。见 `step-080-c1-step3_5-convergence-round3.md:30-38`。
- 7 个 known/family 与先前 receipts/read logs 均有本地血缘：`2604.07004`、ECOC 2014/2015、ECEOC 2012、ICTON 2016、SPA 2015、OFC 2015 Tu3B.2；故 `79−7=72`。
- 在 82 个 raw rows 中，DOI `10.1364/OFC.2017.W2A.56` 恰好命中 1 次；R3 annotated 的 `new_candidates` 也恰为该 1 项，分类 `SHOULD_FULLTEXT`，所以 `new MUST/SHOULD=0/1`。
- OFC 2017 全文已落盘并闭债：`papers/doi/10.1364_ofc.2017.w2a.56/7937400.md`。正文明确 pilot soft-state、4-state Markov 与 fully-parallel LLR modification，而且 “no decision feedback or sequential update”（`7937400.md:41-49`）；结果是 GMI，不是 coded FER/FSO（`7937400.md:47-53`）。因此 `CLOSED_NO_EXACT / STRONG_NEIGHBOR` 成立，全文 debt=`NONE`。

### 3.3 三轮终态

- 第 3 轮新增 SHOULD 非零，不能写 `CONVERGED_ZERO_NEW`；三轮上限已到，正确终态为 `ROUND3_CAP_REACHED_WITH_NEW`。
- 上限轮唯一新增 OFC 2017 已作为 acquisition/read debt 单独关闭；没有启动第 4 轮。见 `step-080:45-58`、`step-081-c1-ofc2017-slip-state-fulltext.md:45-55`、supplement report `:28,78`。

## 4. 本地全文 physical / B2 spot-check

### 4.1 OFC 2014 与 ICTON PCS

- OFC 2014 原文把 blind V&V CPR slip 建成 Markov transition，并用 pilots/data + LDPC feedback 做 whole-codeword turbo demodulation（`papers/doi/10.1364_ofc.2014.m3a.3/content.md:27-31,125`）；没有 explicit boundary、bounded local repair 或 fallback。
- 实测 fiber setup 在 pre-FEC BER>`1e-2` 区域 slip rate>`1e-3` 且不低于 pre-FEC BER 的十分之一（`content.md:129-131`）；synthetic coded slice 冻结 `slip rate=0.1×pre-FEC BER`、pilot `1/2/3%`（`:135-137,307`）。它只能给 coherent-optical stress order，不能移植为 coherent-FSO occurrence 常数。
- ICTON 2016 本地正文的 synthetic `P_CS` 主值 `1e-3`、sweep `2/3/4e-3` 可复核（`papers/doi/10.1109_icton.2016.7550341/content.md:101,118`）；它是 sensitivity range，不是目标 FSO 的自然 slip 分布。

### 4.2 PAPU

- 本地全文确认 28-Gbaud SP-QPSK / 56 Gbit/s、300-kHz laser、pilot overhead `0.78%`、每 127 symbols 插入（`papers/doi/10.3390_app9132749/source.md:41,45,59-61`）。
- filter sweep 为 `{4,8,16,20,32,48}`，核心比较用 8/16/20；PRE gain 约 3.1/1.3/0.6 dB、POST gain约 3/1/0.5 dB（`:21,41,80,121,135`）。
- PAPU 是完全前馈 pilot unwrap/interpolation/sample correction，decoder 仅下游（`:68-72`）；论文未给可直接复现的 integer/interpolation/threshold equations，仍欠 2013 predecessor。故只能冻结 `topology-matched independent implementation`，不能称 exact PAPU reproduction。

### 4.3 JLT 2020 coherent-FSO anchor 与 transfer ceiling

- 本地全文确认 HV/Bufton/TURANDOT physical anchor：1550 nm、`C0=1e-13`、`r0=.039 m`、`L0=5 m`、SI=.684、satellite transverse velocity 6.5 km/s、50-cm aperture（`papers/doi/10.1109_jlt.2020.3003561/content.md:37,43-52`）。
- AO 为 91 Zernike modes/12 radial orders、5 kHz、2-frame delay，flux penalty 从 -23 dB 改善到 -4.5 dB（`:59,85`）。
- coarse CFO 后 residual CFO=100 MHz；DPLL bandwidth=5 MHz，lock 约1.4 ms（`:106,145,152,162,186`）。
- 关键 ceiling：fading 使 DPLL critical-SNR 门槛相对 constant-amplitude 情形上移约 5 dB（`:190`），并在 BER=`1e-4` 产生 2.3-dB power penalty（`:200`）；但 AO 后 turbulent phase noise 对 carrier synchronization 的影响为 negligible（`:196,206`）。因此 JLT 的 fading/AO/CFO/penalty 是 parameter anchor，**不是 turbulence/fading 导致 cycle slip 的因果证据**，也没有 slip detector/count、FEC 或 local repair。

## 5. Debt、coverage limitation 与 owner/control 一致性

- supplement report 与 literature owner 对三轮数字、OFC 2017 身份/闭债、B2 角色和终态一致：report `:22-28,42-43,74-78`；`projects/thesis-fso/literature_notes_coded_decoder_feedback.md:43-44,62,103-109`。
- CSSC-CPE 与 universal CS-DC 仍为 `UNRESOLVED_FULLTEXT`；只能保留 identity/abstract-level B2，不得冻结 exact algorithm/parameter/collision。U01/U02 也仍为 `UNRESOLVED_FULLTEXT`。见 report `:74-75`、literature owner `:27-28,62,107`。
- PAPU exact equation debt 完整保留；见 report `:76`、literature owner `:43`。
- S2/OpenAlex 的 429/timeout 与 Crossref/arXiv recall ceiling 完整保留；raw/unique 明确只是 bounded result-set counts，不是领域 recall/novelty closure。见 `step-067:27-30,102`、`step-078:14-25,73-77`、report `:77`。
- topic/control 仍为 `GROUNDWORK_STEP3_5_SUPPLEMENT / CP009 / epoch 9`；allowed actions 只含 search/citation/abstract/fulltext，forbidden 明列 experiment、adapter、defect smoke、MVE、Contract/Execute/claim（`.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md:8-31,117`）。
- master-state 仍将 Step 3.5 标为 `IN PROGRESS`、Step 4a 为 `FORBIDDEN`（`projects/thesis-fso/master-state.md:38-47`）；literature owner 仍为 `EVIDENCE COMPLETE / VERIFY PENDING`（`:5,14`）。没有提前晋级。

## 6. Fresh protection / parse terminal

- 关键 JSON fresh `ConvertFrom-Json`：6/6 PASS（R1 annotated、citation seed、citation screening、R2 annotated、R3 annotated、physical/B2 annotated）。
- protected p05 fresh SHA256：`4/4 MATCH`：
  - `p05_run.log` 641 bytes / `7843B048...F11`
  - `p05_run2.log` 2417 bytes / `735E4650...38B`
  - `p05_run3.log` 929 bytes / `C76887C6...34D`
  - `p05_run4.log` 1430 bytes / `95A1D184...1DE`
- Git staging fresh：`STAGING_COUNT=0`。

`verdict=PASS; P0=0; P1=0; P2=0`
