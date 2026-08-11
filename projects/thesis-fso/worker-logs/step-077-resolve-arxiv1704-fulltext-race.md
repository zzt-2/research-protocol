# Step 077 — resolve arXiv 1704.04618 fulltext race

> 2026-08-09 | T031 / CP009 / epoch 9 | terminal: `RACE_RESOLVED_FULLTEXT_READ`
> collision: `PARTIAL_CORE_ONLY`

## 1. Scope / gate

- fresh task-control validator：`PASS`；当前 lane=`GROUNDWORK_STEP3_5_SUPPLEMENT`，本轮只执行 `FULLTEXT_READ`。
- 已读 gw-read/gw-supplement、topic-index、D008、T028/step-074、T030/step-076 与 OFC 2015 fulltext note。
- 未重下载；未改 central owner/治理/代码，未实验，未 stage/commit/push，未修改 p05。

## 2. Acquisition-race chronology / root cause

1. T028 首次 normal download 等待 244 s，在其观测点只见 532,480-byte 截断 PDF；Poppler xref/endstream/trailer 全失败，安全删除该文件。
2. forced retry 的 child process 在 parent wait 终止后仍后台写入；T028 止损观察到 1,941,762 bytes、SHA256=`39B485F8CF10CA64863F44FC9A7FE9A200F02D2E7E2DA8B73C9AAFF6E4687E63`且 Poppler 仍报错，终止任务专属进程并删除 corrupt `source.pdf`。
3. T028 在约 `23:31:00` 依当时实际文件状态写入 `UNRESOLVED_FULLTEXT`；这是合法的 observation-time verdict，不是漏读。
4. shared-worktree 中的异步/并行 downloader 在其后才完成 canonical conversion，metadata timestamp=`2026-08-09T23:31:26.692439+08:00`。根因是 parent wait 退出与 child completion 脱节，造成“T028 终态先写、canonical content 后到”的 time-of-observation race。
5. T031 保留该 chronology，但以当前 canonical content 做 fresh read，不延续过期 scientific status。

## 3. Content gate

| 项 | fresh receipt |
|---|---|
| path | `papers/arxiv/1704.04618/content.md` |
| bytes / lines | 143,913 bytes / 1,290 split-lines（文本 1,289 行） |
| SHA256 | `7B8BBD75E0DF07BA7A971561BCA3C0781B8E11C681648102C7CAAF430615FDA1` |
| metadata | `success / arxiv_pdf / good`；downloaded at `23:31:26.692439+08:00` |
| identity | 首 H1 与派遣标题一致；authors=Schmalen / ten Brink / Leven；book DOI `10.1002/9781119078289` 为 chapter self-archiving 声明中的 book-level DOI |
| completeness | Sec. 1–5、phase-slip model、BCJR/LDPC appendix、references 齐全，页码至 60；content gate `PASS` |
| residual limitation | `source.pdf` 已在 T028 止损时删除，无法 fresh render；不影响本次对 canonical text 中 method/window/lineage 的全文裁决 |

## 4. Evidence-backed facts（9 条）

1. 等效信道是 `z[t]=(y[t]+n[t])p[t]` 的 AWGN + random slip model；`P_slip` 可由测量或 pre-FEC BER 和 `gamma` 设定。
2. QPSK slip descriptor 在 modulo-4 下为 `{0,1,2,3}`；附录在 branch metric 中使用 `log P(s=zeta)=|zeta|log(xi)`。
3. naive joint-memory trellis 为 16 states/256 transitions；memory collapse 后为 4 states/64 slip-labelled parallel transitions。
4. modified action 是 model-matched soft BCJR，对 slip-conditioned branch 进行 forward/backward marginalization并吃 LDPC a-priori LLR；不旋转 carrier samples。
5. 调度为常开 turbo loop：首次 BCJR priors=0，之后每次一轮 LDPC message passing 与 BCJR extrinsic exchange。
6. SC window 跟随 termination 产生的 decoding wave，在 parity-check/protograph 子图上运行；不由 slip boundary 触发。
7. `ms=2`，`(w,Iw)=(4,3),(7,2),(16,1)`；窗口覆盖 6/9/18 spatial positions，每 coded bit 等效 18 LDPC iterations，声明 differential executions/bit=6/9/18。
8. clean `gamma=0` 仍运行解码器；只有全局 `(w,Iw)` setup 选择，无 event no-op、failure-conditioned rollback或 local output。
9. `gamma=0.2` 下 SC setup 3 在有限仿真中未观察到 error floor，但无 seeds/CI/runtime/memory/hardware。

## 5. Complete-chain eight fields

| field | fulltext adjudication |
|---|---|
| input | differential-QPSK observations、AWGN/slip prior、differential trellis 及 LDPC/SC-LDPC messages |
| trigger | 无 event trigger；固定 iteration/window schedule，仅以全局 `gamma/P_slip` 选 setup |
| localization | per-symbol slip transition 只在 BCJR 中隐式边缘化；不输出 boundary/direction/range；window 是 code-graph position |
| candidate/correction action | model-matched 4-state/64-transition BCJR + SC-LDPC message passing；无 carrier rotation/local rewrite |
| decoder interaction | BCJR extrinsic → LDPC，variable-node extrinsic → BCJR，按预定迭代反复交换 |
| fallback | 无 proposed conditional fallback；outer code/备选 LDPC 是常开系统配置 |
| complexity/latency budget | rate .8/25% OH，`ms=2,dv=3,dc=15`；18 equivalent LDPC iterations/bit，6/9/18 differential executions/bit；无 absolute latency/runtime |
| output | decoded bitstream/BER；无 slip flag、boundary、corrected samples或 local-repair outcome |

## 6. Window/local verdict and lineage

- Window：`WINDOWED_SC_LDPC_GRAPH_SCHEDULE / NO_SLIP_BOUNDARY / NO_SELECTIVE_LOCAL_REDECODE`。每窗做 `Iw` iterations 后固定右移 `n'` protograph variables，左端 bits 视为已解；这是码图调度，不是 affected segment/suffix repair。
- OFC 2015：Sec. 4.4 明确引 `[88]`，同三位作者、同 protograph/lifting/window 结果。谱系是 `OFC 2015 -> 2016 book chapter -> 2017 arXiv self-archive`，按一个方法家族计数。
- 书章增量：capacity/slip 模型、matched trellis 详解、EXIT、regular/irregular LDPC、SC universality 与 appendix；没有隐藏 explicit boundary/local carrier correction。
- ICTON 2016 为不同作者的 slip-mismatched DD + layered-LDPC rollback/schedule 方法，非本家族版本。

## 7. Collision / terminal

`collision_verdict = PARTIAL_CORE_ONLY`。

已碰撞的核心是 `slip-aware BCJR + iterative LDPC feedback + SC graph-window bounded computation`；缺失的完整链是 `event trigger -> explicit boundary -> finite local carrier action -> affected segment/suffix selective re-evaluation -> clean no-op/failure fallback -> local output`。因此 terminal=`RACE_RESOLVED_FULLTEXT_READ`，非 `EXACT_COMPLETE_CHAIN_CONFIRMED`。

## 8. Outputs / fresh protection

- updated note：`papers/_read_notes/1704.04618.md`
- worker log：`projects/thesis-fso/worker-logs/step-077-resolve-arxiv1704-fulltext-race.md`
- content gate/task-control/note requirements：`PASS`；任务专属 downloader process=`NONE`；`source.pdf=ABSENT`。
- Git staging=`EMPTY`；未 commit/push。
- p05 frozen SHA256 fresh check=`4/4 MATCH`：
  - `p05_run.log`=`7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log`=`735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log`=`C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log`=`95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`

`RACE_RESOLVED_FULLTEXT_READ`
