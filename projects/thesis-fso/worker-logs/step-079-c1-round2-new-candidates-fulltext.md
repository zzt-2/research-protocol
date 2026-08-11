# Step 079 — C1 round-2 新候选全文裁决

> 日期：2026-08-09  
> 任务：T033 / CP009 / `GROUNDWORK_STEP3_5_SUPPLEMENT`  
> action class：`FULLTEXT_READ`  
> terminal：`PAIR_FULLTEXT_READ`

## 1. 边界与 acquisition

- fresh task-control validator：PASS；只执行两篇全文 acquisition/read/collision，不改中央 owner、治理、代码，不实验，不触碰 p05，不提交/push。
- `arXiv:2604.07004v1`：official arXiv HTML成功；`content.md` 157281 bytes / 756行，SHA256=`817A4D72CC1E630C79B0C20FFF8E6DCB6B5160EDA017C2D58DFF8C3C9B3D0C19`，`FULLTEXT_READ`。
- `doi:10.1364/OFC.2015.TU3B.2`：DOI/OA pipeline失败后，IEEE DOI命中 document `7121844`；PDF 3页/226100 bytes，SHA256=`707BF3EB08632B4C8B4FC6AFAB6797145F1ECCEADCF29447286DD87E0F81FF7A`。PDF metadata与首屏身份PASS，三页渲染完整；转换文本字体乱码不影响逐页全文裁决，`FULLTEXT_READ`。

## 2. 2604.07004：事实与裁决（10条）

1. burst真实语义是 **Gilbert–Elliott (GE) Markov-modulated Wiener innovation variance** 的 G/B时段，不是 discrete cycle slip或 carrier phase segment。
2. phase-domain differential coding后得到 state-dependent zero-mean differential phase noise；正文明确不需要 carrier phase recovery。
3. VA/SOVA/BCJR在两状态trellis上输出逐符号 G/B hard/soft posterior，构成 variance-regime localization。
4. BA用状态后验混合 likelihood并生成 burst-aware LLR；不旋转或重写样本。
5. IBA执行 `LDPC LLR → symbol probability → channel-state posterior/likelihood → new LLR`；每个外迭代重置LDPC。
6. 无 event trigger、clean abstention、finite carrier candidate、affected segment/suffix reprocess或 conditional fallback。
7. budget：15 LDPC iterations、3 outer iterations、VA/SOVA traceback与BCJR window=100、interleaver=1024 rows；均为全流固定预算。
8. output：中间为逐符号G/B后验，最终为full decoded bits/BER/PER；无 boundary/phase action/corrected samples。
9. 直接延伸ECOC 2025 hard-state BA，新增soft state与IBA；与OFC2014/OFC2015/1704的 discrete-slip trellis不是版本重写。
10. `collision=PARTIAL_CORE_ONLY`：占用“burst-state localization + LLR action + decoder feedback”，不覆盖完整 local carrier repair chain。

### 八字段

| input | trigger | localization | action | decoder interaction | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| 全部 `y_k` + GE参数 + decoder messages | always-on | 逐符号G/B后验 | state-aware likelihood/LLR | IBA全码字外迭代 | `NOT_STATED` | 3 outer × 15 inner；100-symbol estimator window | G/B后验 + full decoded bits |

## 3. OFC 2015 Tu3B.2：事实与裁决（10条）

1. differential coding把cycle slip的准永久相位后果限制为局部data-error event；这不是算法显式boundary localization。
2. 论文比较reference、block-symmetric LDPC、TDD、HTDD四种differential-aware FEC设计。
3. TDD可回收differential penalty，但频繁slips造成DD/LDPC disagreement与error floor。
4. HTDD固定执行若干TDD iterations，再执行少量plain LDPC iterations；后段清理slip-induced bit errors。
5. compound LDPC由time-interleaved differential-code “spine”耦合小LDPC components；这是码结构，不是carrier-local window。
6. 无 slip estimator/count/direction/boundary、phase candidates、sample rotation或detected-segment/suffix redo。
7. clean与stressed流量走同一schedule；outer cleanup/plain-LDPC尾段不是conditional fallback。
8. 20% OH、real-time configurable codec、Nyquist DP-QPSK 100G和20×100km ELEAF；迭代数只写“several/few”，无local latency/decode-call上界。
9. 直接延伸同作者ECOC 2014 HTDD工作；与Th3E.6/1704的model-matched slip BCJR + SC window路线不同。
10. `collision=STRONG_NEIGHBOR`：占用differential-aware FEC schedule与decoder re-evaluation，但不检测/定位/修正carrier samples。

### 八字段

| input | trigger | localization | action | decoder interaction | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| 全码字 + differential soft info | always-on | 仅物理上限制error propagation，无boundary输出 | TDD + plain-LDPC cleanup | 固定全码字schedule | `NOT_STATED` | 20% OH；迭代数不精确 | full decoded bits / post-FEC BER |

## 4. Pair conclusion / claim ceiling

`terminal = PAIR_FULLTEXT_READ`：两篇全文和身份都已闭环，无 acquisition debt。没有发现 `EXACT_COMPLETE_CHAIN`。

- arXiv的 burst 是**高/低创新方差状态**，其BCJR window定位的是 G/B regime；不能解释为cycle-slip boundary或 bounded carrier repair。
- OFC的 “localized error event” 是 differential coding限制误差传播的性质；HTDD是always-on code/schedule tolerance，不输出carrier-level repair object。
- round-2只把已知重合上限推进到 `per-symbol burst-state posterior + state-aware LLR + LDPC feedback` 与 `differential-aware FEC schedule`；`trigger → explicit slip boundary → finite carrier action → bounded local reprocess → failure fallback → repair output` 仍未由这两篇构成。

## 5. 产出

- `papers/_read_notes/2604.07004.md`
- `papers/_read_notes/10.1364_ofc.2015.tu3b.2.md`
- `projects/thesis-fso/worker-logs/step-079-c1-round2-new-candidates-fulltext.md`
