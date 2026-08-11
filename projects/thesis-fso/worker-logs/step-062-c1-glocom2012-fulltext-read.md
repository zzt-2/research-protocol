# Step 062 — GLOBECOM 2012 hard/soft DD CPR 全文精读

> 日期：2026-08-09  
> 任务：T016  
> 状态：`FULLTEXT_READ / STRONG_NEIGHBOR`  
> 范围：仅 Groundwork Step 2 acquire/read；不改中央 owner/治理/代码，不形成 Q#、Go/Kill，不实验、不提交。

## 1. Task-control

| 检查项 | 结果 |
|---|---|
| schema / epoch / checkpoint | `rdl.task-control.v2 / 6 / CP006` 与 topic control 一致 |
| action class | `FULLTEXT_READ` 在 allowed actions 内 |
| forbidden boundary | 未进入 adapter/MVE/Contract/Execute/thesis claim |
| validator | `python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py .sessions\2026-08-09-coded-decoder-feedback-groundwork\T016-c1-glocom2012-fulltext-read.md` → `PASS` |

## 2. Acquisition receipts

| 顺序 | 通道/命令 | 结果 |
|---:|---|---|
| environment | `~/.venvs/torch/bin/python -c "import requests, pymupdf, pymupdf4llm, serpapi, tavily"` | `OK` |
| 1 | `tools/download --doi 10.1109/GLOCOM.2012.6503711`；CRLF 后按 T016 用 `tr -d '\r' < download | bash -s -- --doi ...` | FAIL：`all_failed`；failure metadata timestamp `2026-08-09T22:02:56+08:00` |
| 2 | arXiv API exact-title query + existing global-index `arxiv_id` check | `totalResults=0`；index `arxiv_id=null` |
| 3 | `tools/blit '<exact title>' --source ieee --max 3 --download <DOI dir>` | PASS 1/1；IEEE arnumber `6503711`；PDF 392,644 bytes |
| convert | repository `tools/convert source.pdf --quality standard` | `content.md` 322 lines / 41,170 bytes；39 extracted figures |

三轮后停止；未用 webReader、ResearchGate 或 Google Scholar 页面抓全文，未追加第四通道。

## 3. Title/quality/body gate

- `6503711.meta.json`: `title_check=match`, overlap `0.4166666667`；`content.md:1` 与 expected title 一致。
- 原 PDF 6 页；method/algorithm/system：Sec. II–IV (`content.md:21–218`)；experiment/results：Figs. 2–5 与 Sec. IV (`content.md:90–218`)；conclusion：`content.md:220–222`；hard/soft derivation appendices：`content.md:224–322`。
- 原 PDF text layer 复核：`I=50` footnote 明确“该 code/setting 用于后续分析”；“four LDPC codes”=基准 `(3,6)` 加后列三种。

## 4. 关键事实（≤10 条）

1. 每个 outer iteration 的因果顺序是：previous-phase compensation → 1 decoder iteration → temporary hard/soft decisions → 1 full-codeword second-order PLL pass。
2. 最大 outer iterations 为 50；initial phase estimate 来自 short pilot preamble 的 DA estimator。
3. hard QPSK decisions 是 APP-sign 对 `±sqrt(2)/2` I/Q components 的量化；soft decisions 是 symbol posterior mean，QPSK 用 APP-LLR `tanh`。
4. tracker state 为 per-symbol `theta_hat_k`，但算法每轮处理 whole codeword；无 segment/suffix selective repair。
5. 无 cycle-slip trigger、boundary localization、candidate bank、clean no-op 或 explicit fallback。
6. phase model 只有 initial phase + small constant CFO；实验特意设 `omega N T_s=0.1` 避免 codeword edge large offset。
7. decoder extrinsic 变弱时 CA detector 连续退化到 NDA；可靠 decision/small offset 时接近 DA/MCRB。
8. ISDD 在低 SNR 略优于 IHDD；论文只定性指出 IHDD 成本较低，未报告 runtime/latency/memory。
9. 同 receiver information 可使其成为 B2 conventional comparator，但 published 50 次 full-frame decoder/PLL budget 必须与 proposed bounded local method 做独立预算匹配。
10. `collision_verdict=STRONG_NEIGHBOR`；不是 finite-hypothesis core collision，更不是完整 local-repair chain collision。

## 5. 缺口与 claim ceiling

- `NOT_STATED`：preamble length、decoder convergence criterion、Monte Carlo trials/seeds/error bars、measured latency/memory、clean false-action、fallback、open-source code。
- 未验证：phase-noise/cycle-slip injection、boundary/segment recovery、fading/turbulence/FSO、higher-order modulation、同预算 bounded repair。
- 高 SNR/large phase offset 下 cross-talk Gaussian approximation 变差；论文自己只声称低 SNR 更准确。
- `claim ceiling=SLICE`：只支持 AWGN/QPSK/constant-CFO 下 conventional B2 身份与预算原料，不支持 family/domain 级 strongest 或 target defect disposition。

## 6. 写入清单

- `papers/_read_notes/10.1109_glocom.2012.6503711.md`
- `projects/thesis-fso/worker-logs/step-062-c1-glocom2012-fulltext-read.md`
- acquisition assets：`papers/doi/10.1109_glocom.2012.6503711/{source.pdf,6503711.meta.json,metadata.json,content.md,figures/}`

未修改 topic-index、decisions、mission-log、master-state、registry、voice/profile、代码或 p05；共享 worktree 中既有脏状态不由本 worker 清理或归因。

## 7. 时间、git 与 p05 保护

- acquisition receipt 起点 `2026-08-09T22:02:56+08:00`；正文与两份指定笔记在 15 分钟预算内收口。
- 未 stage、未 commit、未 push。
- 收尾保护基线：
  - `p05_run.log` 641 bytes / `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log` 2417 bytes / `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log` 929 bytes / `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log` 1430 bytes / `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`

