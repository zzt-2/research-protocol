# Step 066 — TVT recent code-aided CFO/CPO baseline 全文精读

> 日期：2026-08-09  
> 任务：T020  
> 状态：`FULLTEXT_READ / PASS_RECENT_TOP_JOURNAL_BASELINE / STRONG_NEIGHBOR`  
> 范围：仅 CP008 / Groundwork Step 3 criterion3 repair；未进入 Step 3.5、adapter、MVE、Contract 或 Execute。

## 1. Task-control 与 session 边界

| 检查项 | 结果 |
|---|---|
| schema / epoch / checkpoint | `rdl.task-control.v2 / 8 / CP008` 与 topic control 一致 |
| action class | `FULLTEXT_READ` 在 allowed actions 内 |
| validator | `python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py .sessions\2026-08-09-coded-decoder-feedback-groundwork\T020-tvt2025-recent-baseline-read.md` → `PASS` |
| framework read | 已读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1` |
| forbidden boundary | 未修改 central governance/owner/code；未运行实验；未进入 Step 3.5；未 stage/commit/push |

## 2. Acquisition、title、DOI 与版本对应

| 项目 | 证据/结果 |
|---|---|
| 首选通道 | `tools/download --arxiv 2309.12828`（PowerShell/CRLF 环境用 `tr -d '\r' < tools/download | bash -s -- --arxiv 2309.12828`）→ `arxiv_html / good` |
| acquisition receipt | `papers/arxiv/2309.12828/metadata.json`；downloaded_at `2026-08-09T22:29:51.080256+08:00` |
| content quality | `content.md` 778 lines / 136,320 bytes；method `201–669`、experiments `676–729`、conclusion `733–740` 均存在 |
| current HTML identity | H1 `content.md:17` 为 expected formal title；`content.md:20–21` 六位作者 |
| arXiv API identity | id `2309.12828`；旧题 *Multiple Satellites Collaboration for Joint Code-aided CFOs and CPOs Estimation*；同一六位作者；published 2023-09-22, updated 2023-09-25 |
| Crossref formal identity | DOI `10.1109/TVT.2025.3600028`；current H1 exact title；same six authors；IEEE TVT journal article；created 2025-08-19；issued 2026-02, vol.75(2), pp.2500–2515 |
| mapping conclusion | same arXiv id 的 current official H1/作者与 Crossref 完全一致，正文方法也一致：改题演进，非 materially different version。arXiv API 未显式给 DOI，因此未伪称其单点证明 DOI。 |

`metadata.json` 的 `title_check=unverifiable` 仅表示 downloader 未取得 expected-title comparator；人工 H1 gate 为 exact match。正式年份区分为 “2025 DOI/early identity；2026 formal issue”，二者都满足 2019+。

## 3. 关键事实（≤10 条）

1. ICE-CEM 是具体、可复现的两阶段 estimator：ICE global coarse search，CEM decoder-posterior-assisted global fine estimation。
2. 状态是每帧、每卫星一个 constant residual CFO 和一个 CPO；不是 within-frame phase-jump/change-point state。
3. ICE 每颗卫星用 `D` CFO bits + 1 phase-ambiguity bit，全局 candidate dimension 为 `M(D+1)`；每轮采样 `N_c`、保留 `N_e` elites、更新概率向量。
4. code-aided evidence 是 Polar decoder posterior LLR 转成 BPSK posterior symbol expectation，再进入 combined SNR-loss objective；不是 TX truth。
5. Eq. (25) 最后一行多印了 `exp`；前一行代数明确应为 `tanh(L_pos/2)`，已在 read note 标警告。
6. CEM 每 iteration 明确执行 full-frame compensation/combination + 1 Polar decode，再逐卫星更新 residual CFO/CPO；实际 `N_iter,EM` 未给。
7. 典型 ICE 参数为 `D=6,N_c=120,N_e≈24`；ICE exact decoder-call accounting、runtime、memory 均未报告。
8. baseline 只有 CRLB、ideal synchronization 和参数敏感性；没有同信息同预算 CA estimator head-to-head comparison。
9. Results 与 Abstract/Conclusion 对 M=2/4 的 0.3/0.4 dB 顺序互相矛盾；安全结论仅是两配置均约 0.3–0.4 dB loss @ BER=1e-4。
10. 无 slip trigger、boundary localization、segment/suffix action、clean no-op、failure fallback；输出是 global CFO/CPO + whole-frame decoded data。

## 4. 判定

### criterion3

`criterion3_verdict=PASS_RECENT_TOP_JOURNAL_BASELINE`

- Crossref 正式身份是 IEEE TVT journal article，2025 DOI identity / 2026 formal issue，满足 2019+。
- 全文给出 Eqs. 14–45、Algorithms 1–2、关键参数和算法时序，具体 M 为 `ICE global stochastic coarse search + cooperative posterior-LLR CEM fine estimation`；不是 metadata-only baseline。
- PASS 只承担 Q1 criterion3 repair，不证明 target local-slip defect，也不在本 worker 更新中央 Q1 状态。

### collision

`collision_verdict=STRONG_NEIGHBOR`

- overlap：decoder posterior feedback、carrier CFO/CPO estimation、ICE 中有限 global coarse hypotheses。
- non-overlap：无 within-frame slip trigger/localization、无 bounded segment/suffix repair、无 clean no-op、无 failure fallback；全局 candidate 也不是目标 local symmetry bank。
- 因而不是 `PARTIAL_CORE_ONLY` 或 `EXACT_COMPLETE_CHAIN`。

## 5. 缺口与 claim ceiling

- `NOT_STATED`：ICE exact decoder calls、`N_iter,EM` numeric value、BP internal iteration budget、stopping threshold value、trials/seeds/error bars/CI、wall-clock/runtime/memory、open-source code、failure fallback。
- 不覆盖：within-frame slip injection、boundary accuracy、segment/suffix recovery、clean false action、FSO turbulence/phase-noise trajectories、same-budget local-vs-global comparison。
- 实验正文的 M=2/4 BER loss 顺序与 abstract/conclusion 冲突，未核图前不得挑一个顺序写成确定事实。
- `claim ceiling=SLICE`：仅支持 recent formal global code-aided CFO/CPO baseline 身份及其方法/预算原料。

## 6. 写入清单

- `papers/_read_notes/2309.12828.md`
- `projects/thesis-fso/worker-logs/step-066-tvt2025-recent-baseline-read.md`
- acquisition assets：`papers/arxiv/2309.12828/{source.html,content.md,metadata.json}`

未修改 topic-index、decisions、mission-log、master-state、registry、voice/profile 或代码；共享 worktree 既有脏状态不由本 worker 清理或归因。

## 7. 时间、git 与 p05 保护

- acquisition receipt 起点 `2026-08-09T22:29:51.080256+08:00`；全文与两份指定产出在派遣的 15 分钟窗口内收口。
- 未 stage、未 commit、未 push。
- p05 fresh verification 与派遣基线完全一致：
  - `p05_run.log` 641 bytes / `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log` 2417 bytes / `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log` 929 bytes / `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log` 1430 bytes / `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
