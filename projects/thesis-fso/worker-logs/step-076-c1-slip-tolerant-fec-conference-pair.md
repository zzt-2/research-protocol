# Step 076 — C1 slip-tolerant FEC conference pair fulltext adjudication

> 2026-08-09 | T030 / CP009 / epoch 9 | terminal: `PAIR_FULLTEXT_READ`

## 1. Scope / gate

- fresh task-control validator：`PASS`。
- 已读 `gw-acquire.md`、`gw-read.md`、`gw-supplement.md`、topic-index、D008、step-067、OFC 2014与ICTON 2016全文笔记。
- 本轮只获取/精读两篇 conference候选并核版本链；未改 central owner/治理/代码，未实验，未 stage/commit/push。

## 2. Acquisition 与质量

| Paper | canonical DOI pipeline | institutional channel | fulltext / QA |
|---|---|---|---|
| `10.1109/ECOC.2014.6963875` | dry-run PASS；actual `all_failed` | IEEE exact-title=0；exact doc id `6963875`命中并下载。末尾仅 GBK状态打印失败 | `6963875.pdf`，3页/518041 bytes，SHA256 `4D28...D8F99`；转换文本因字体映射乱码，160-dpi渲染逐页全文判读 |
| `10.1364/OFC.2015.TH3E.6` | dry-run PASS；actual `all_failed` | IEEE exact-title命中 doc `7121707`并下载。末尾仅 GBK状态打印失败 | `7121707.pdf`，3页/205512 bytes，SHA256 `A4EFF...3F87`；转换123行且三页渲染核验 |

两篇均使用2/3合法渠道，未绕过付费墙。arXiv `1704.04618`另由官方 arXiv channel取得 `content.md`，只用于版本血缘交叉核验。

## 3. ECOC 2014：≤10 fresh facts

| # | fact / action-chain field |
|---|---|
| 1 / input | carrier-recovery后 BPSK/8-QAM/QPSK observations进入固定 demap→BS-LDPC→differential→outer-code链。 |
| 2 / trigger | 无 slip-event trigger；每帧常开，clean帧也无 abstention/no-op。 |
| 3 / localization | 不输出真实 slip `t`/方向/count；`S`只定义预置子块边界，任意位置事件由最近合法边界近似吸收。 |
| 4 / action | block-symmetric LDPC故意对 slip-induced subblock inversion透明；differential decoder把每次 slip压成单错误，outer code cleanup。无 carrier rotation/local reprocess。 |
| 5 / decoder | 串行一次 BS-LDPC + differential + outer decode，不是 turbo feedback或 selective re-decode。 |
| 6 / fallback | outer code/interleaver为常开层，不是 failure-conditioned fallback；其他 fallback未述。 |
| 7 / budget | 8-QAM `R=.85,S=40,12` layered iterations；QPSK `Z4 R=.85,S=30`；outer rate `239/255`，overall OH 25%，sufficiently long interleaver；pilot未述。 |
| 8 / output | final decoded bits；无 slip/boundary/repaired-sample output。 |
| 9 / experiment | AWGN + Bernoulli `P_slip=10^-6/10^-5/10^-4`；报告8-QAM约0.4 dB、结论最高1.3 dB增益；无统计置信度/硬件。 |
| 10 / collision | `STRONG_NEIGHBOR`：占 FEC/differential tolerance，不占 decoder-triggered local carrier repair。 |

## 4. OFC 2015：≤10 fresh facts

| # | fact / action-chain field |
|---|---|
| 1 / input | differential-QPSK observations + slip-extended AWGN transition model + SC-LDPC messages。 |
| 2 / trigger | 无 event trigger；每个预定迭代调用 differential decoder，`P_slip`只作全局 setup选择。 |
| 3 / localization | 4-state BCJR用 parallel slip edges隐式覆盖逐符号 transition，不输出 boundary/direction/range。 |
| 4 / action | model-matched differential BCJR + SC-LDPC window message passing；不旋转 carrier samples，不建 local phase candidate bank。 |
| 5 / decoder | `w=6,I=3` / `9,2` / `18,1`，每种均18次 differential calls；window沿 decoding wave推进，不由 slip event定位。 |
| 6 / fallback | proposed scheme无 failure rollback；reference error floor所需 strong outer code不是 proposed conditional fallback。 |
| 7 / budget | rate .8 / 25% OH，`mu=2,L=200,dv=3,dc=15`；1837 protographs→top50→index3；pilot/interleaver未述。 |
| 8 / output | full decoded bitstream/BER；无 local repair artifact。 |
| 9 / experiment | `P_slip=0/0.01`；SC setup3有限仿真未见 error floor，未给 trials/CI/runtime/硬件。 |
| 10 / collision | `PARTIAL_CORE_ONLY`：占 slip-aware BCJR+LDPC feedback+windowed computation，缺 explicit boundary/local correction/fallback。 |

## 5. Identity chain / duplicate control

1. **OFC 2014 M3A.3 → OFC 2015 Th3E.6（method predecessor）**：OFC 2015正文与ref `[3]`直接归因其 slip-model-aware differential/turbo trellis；OFC 2015再加入 differential-code trellis、SC-LDPC protograph与windowed decoding。作者与稿件不同，不按身份重复。
2. **OFC 2015 → 2016 book chapter → arXiv 1704.04618（direct extension/rewrite）**：同三位作者；章 Section 4.4引用 `[88]`即OFC 2015并复现/扩展矩阵、lifting与结果。章中 `w=4/7/16 + mu=2` 对应 conference总 stages `6/9/18`。这一链按一个方法家族计数。
3. **ECOC 2014 → JLT 2015（conference→journal lineage）**：同一作者与 block-symmetric/phase-slip-transparent核心；1704章把两者并列为 `[33,34]` 的非迭代 slip-resilient alternative。JLT增量未在本任务精读。
4. **ECOC 2014 vs OFC 2015**：虽共享 Schmalen，但前者是 code transparency + outer cleanup，后者是 iterative slip-aware trellis + SC window；不是版本链。
5. **ICTON 2016**：不同作者、基于 layered schedule + unsatisfied-check rollback，且无 slip-aware carrier trellis；是独立 schedule/fallback neighbor，不是上述论文extension。

## 6. Pair verdict / Q1 boundary

`PAIR_FULLTEXT_READ`。两篇都不形成 `event trigger → explicit boundary → carrier candidate/local segment-or-suffix repair → selective decoder re-evaluation → clean no-op/failure fallback → bounded local outcome` 完整链；不存在 `EXACT_COMPLETE_CHAIN`。

- ECOC 2014：`FULLTEXT_READ / STRONG_NEIGHBOR`，本质是 FEC tolerance。
- OFC 2015：`FULLTEXT_READ / PARTIAL_CORE_ONLY`，本质是 model-matched slip-aware iterative differential/FEC decoding。
- “window/sub-block”不能自动等同于 Q1 local repair：ECOC的 `S` 是码结构粒度，OFC的 `w` 是 SC-LDPC decoding-wave窗口，两者都不由显式 slip boundary触发。

## 7. Outputs

- `papers/_read_notes/10.1109_ecoc.2014.6963875.md`
- `papers/_read_notes/10.1364_ofc.2015.th3e.6.md`
- `projects/thesis-fso/worker-logs/step-076-c1-slip-tolerant-fec-conference-pair.md`

## 8. Protection

- 未 stage、未 commit、未 push；未修改 central owner/治理/代码。
- fresh task-control validator=`PASS`；两份 note 的八字段与 terminal token均通过确定性检查，两份 PDF均为3页且大于100 kB。
- p05 fresh SHA256 与派遣基线逐项一致：
  - `p05_run.log`=`7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log`=`735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log`=`C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log`=`95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
