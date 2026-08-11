# Step 072 — C1 Tikhonov-mixture joint decoding 全文精读

> 日期：2026-08-09  
> 任务：T026 / CP009 / epoch 9  
> terminal：FULLTEXT_READ  
> collision：STRONG_NEIGHBOR

## 1. Task-control 与边界

- 已读取 gw-acquire、gw-read、gw-supplement、topic-index、D008、step-068 与 L05 read note。
- fresh validator：validate_task_control.py 对 T026 输出 PASS。
- FULLTEXT_READ 属 CP009 allowed action；未改 literature owner、topic governance、master-state 或代码，未实验、stage、commit、push。

## 2. Identity 与正文质量

- arXiv API：1306.3693v2，2013-06-22，标题 *Message Passing Algorithms for Phase Noise Tracking Using Tikhonov Mixtures*，作者 Shachar Shayovitz / Dan Rapaheli（API 拼写）。
- 原始 source.tar.gz 内 final.tex 与 Crossref DOI 10.1109/TCOMM.2015.2506553 均给作者 Dan **Raphaeli**；正式身份为 IEEE Transactions on Communications, 64(1):387–401, Jan. 2016。
- content.md 607 行 / 75,370 bytes / SHA-256 6DE0772A6BC4866EBF3CB7FDB841137F909C5DBFA6346A16B8AF4D18EFFA48C3，system、Algorithms 1–3、complexity、numerical results、discussion 与 appendices 齐全。转换文本漏 title/abstract，故自动 title check 不可判；原始 TeX + 两个官方 API 使人工 title/content gate=PASS。

## 3. 正文事实（9 条）

1. phase latent state 是逐符号 continuous Wiener trajectory；没有 discrete slip state、jump angle 或 change-point index（content.md:23-28）。
2. 无 a-priori 时 MPSK 产生 M 条相隔 2pi/M 的 trajectory branches；pilots 增强正确分支，split/merge 改变 mixture order，split 被类比为 PLL slip 时点（:126-138）。
3. LDPC soft symbol probability P_d 进入 forward/backward phase SPA；channel 产生 P_u 回送 LDPC，形成整块 joint iterations（:40-53）。
4. Algorithm 1 用 KL-neighborhood + CMVM merge，输出 variable order，并保证 reduction KL 不超过 epsilon（:221-288）。
5. Algorithm 2 以最大阶 L 截断 mixture，并用 phi_k^f/phi_k^b 累积 correct trajectory 仍被保留的近似概率；被舍弃正确分支才被论文称为 cycle slip（:297-312）。
6. Algorithm 3 只在固定 pilot 到达时以 phi p+(1-phi) uniform 重新播种 tracker；它没有估计 boundary，也没有 rollback/redecode local suffix（:314-325）。
7. clean/no-slip 时 phi=1 使 pilot blend 在消息层退化为 identity，但全套 tracker/decoder 仍运行；clean false-action/compute bypass 未测。
8. 8PSK slice 为 LDPC length 4608/rate 0.89、sigma_Delta=0.05、pilot every 20；unlimited、limited order 2/3 与 reduced order 3 接近 DP，32PSK order 1 因 recovery 也近 DP（:371-410）。
9. reduced order-3 的 8PSK operation table 给 iterations 1–4 的 312/292/273/238 MULS，远低于 DP 68,360；但无 runtime/latency、selective decoder-call 或 abrupt-slip experiment（:424-436）。

## 4. 八字段 adjudication

| 字段 | 全文事实 | 裁决 |
|---|---|---|
| input | samples + phase-noise/AWGN model + pilots + LDPC soft symbols | 合法 receiver information；依赖 pilots |
| trigger | fixed per-symbol/per-iteration recursion；scheduled pilot recovery | 无 event/slip/decoder-anomaly trigger |
| localization | internal per-symbol mixtures 与 phi | 无 explicit boundary/affected segment output |
| action | trajectory expansion/merge/prune + pilot uniform re-seeding | 无 boundary-conditioned bounded segment/suffix correction |
| decoder | P_d ↔ phase SPA ↔ P_u 的全块 joint iterations | 无 selective rollback/redecode |
| fallback | low-confidence pilot re-acquisition；forward/backward four-case weighting | tracking fallback 有；B1/B2/abstain/failure-conditioned local fallback 无 |
| budget | adaptive/limited mixture order 与 operation formulas；每轮全序列 forward/backward | 非 bounded-local decoder/latency budget |
| output | phase messages、symbol LLR、decoded bits | 无 slip flag、boundary 或 repaired interval |

逐符号 dynamic posterior 只说明 estimator 有细时间粒度；本文动作图仍是连续 full-sequence tracking。它不等价于 detect boundary → bounded segment/suffix rollback/redecode。

## 5. Collision 与 claim ceiling

STRONG_NEIGHBOR：论文覆盖 dynamic multi-modal trajectory、decoder-assisted ambiguity resolution、有限阶置信度与 pilot-assisted slip recovery，必须成为 Q1 的强全文邻居；但既没有 Q1 baseline 的 whole-frame finite decoder-selection core，也没有 local extension 的 trigger/boundary/bounded repair/selective re-decode/clean compute no-op/B1-B2 fallback/local output，故不是 PARTIAL_CORE_ONLY 或 EXACT_COMPLETE_CHAIN。

claim ceiling=SLICE/HISTORICAL_STRONG_NEIGHBOR：只能承重 LDPC/MPSK/Wiener phase-noise 下的 joint tracking/recovery 先例；不能证明 coherent-FSO abrupt local slip 的 occurrence、可恢复 headroom 或完整链 novelty。

## 6. 产出、耗时与保护检查

- 产出：papers/_read_notes/1306.3693.md；本 worker log。
- 获取资产：papers/arxiv/1306.3693/{source.tar.gz,content.md,metadata.json}；使用仓库 downloader 的 Python entry，设置 PYTHONDONTWRITEBYTECODE=1。papers/index.json 若有变化仅为 downloader 自动维护，未手工编辑中央 owner。
- elapsed：约 12 分钟（下载锚点 23:05:43+08:00；在 15 分钟 task budget 内收口）。
- p05 四文件未写入；收尾复核 hash/size 与起始基线一致。未 stage/commit/push。
