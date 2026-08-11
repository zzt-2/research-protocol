# Step 063 — IWCMC 2023 adjustable-range CA synchronization 全文精读

> 日期：2026-08-09  
> 任务：T017  
> 状态：`FULLTEXT_READ / PARTIAL_CORE_ONLY`  
> 范围：仅 Groundwork Step 2 acquire/read；不改中央 owner/治理/代码，不形成 Q#、Go/Kill，不实验、不提交。

## 1. Task-control

| 检查项 | 结果 |
|---|---|
| schema / epoch / checkpoint | `rdl.task-control.v2 / 6 / CP006` 与 topic control 一致 |
| action class | `FULLTEXT_READ` 在 allowed actions 内 |
| forbidden boundary | 未进入 adapter/MVE/Contract/Execute/thesis claim |
| validator | `python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T017-c1-iwcmc2023-fulltext-read.md --repo-root .` → `PASS` |

## 2. 执行规范

- 已按当前上下文执行 `gw-acquire` 三轮止损、`gw-read` title/content gate、glossary M/C/A 四判据与 `domain-comms §1.1` 参数提取。
- 当前仍为 `CP006 / GROUNDWORK_STEP2_ACQUIRE_READ`；本 worker 只写独立 read note 与 worker log。

## 3. Acquisition receipts

| 顺序 | 通道/命令 | 结果 |
|---:|---|---|
| preflight | `tools/download --doi 10.1109/IWCMC58020.2023.10182805 --dry-run`（CRLF workaround） | PASS；规范化目录正确 |
| 1 | `tools/download` DOI | FAIL：`[FAIL] all_failed`；failure metadata timestamp `2026-08-09T22:02:57+08:00` |
| 2 | Semantic Scholar DOI + arXiv exact title | S2=`CLOSED`/无 OA PDF；arXiv `totalResults=0` |
| 3 | 当前 `tools/blit` IEEE exact-title，`--max 3 --download ../papers/doi/10.1109_iwcmc58020.2023.10182805` | PASS 1/1；`10182805.pdf` 1,335,613 bytes |
| convert | 项目 `tools/convert --quality fast` | `content.md` 317 lines / 30,797 bytes |

三轮后停止；未用 webReader/ResearchGate/Google Scholar 页面抓全文，未追加第四通道。

## 4. Title/quality gate

- expected title 与 `content.md:1` 完全一致。
- `10182805.meta.json`: `title_check=match`, overlap `0.5555555556`。
- PDF method/algorithm/experiment/conclusion 完整；视觉核验 pp. 808–811 的公式、Algorithm 1、Figs. 2–8。
- `metadata.json` 的 `all_failed` 只对应第一轮；实际 PDF/content 由 IEEE blit + convert 获得。

## 5. 关键事实（≤10 条）

1. 输入是 full-frame samples、hard demod、LDPC parity/syndrome 与 decoder soft LLR；不使用 transmitted truth/CRC。
2. Algorithm 1 先做 global phase/NFO grid syndrome scan，再对 top-`NQ` candidates 解码算 CMF，选一项初始化 EM。
3. joint 示例为 27 个 cheap grid points→5 个 decoder-CMF candidates→1 个 global initializer。
4. 之后做 3 轮 whole-frame EM；每轮最多 10 BP iterations，不是 local slip repair。
5. coarse CMF 只需额外 5 decoder iterations，论文报为一个 EM process 的 17%。
6. 前置假设包含 correct timing/gain/frame sync 与 frame preamble；“no additional pilots”不等于完全无同步资源。
7. phase experiment明确 offset constant within a frame；没有 slip boundary、segment/suffix correction 或 change-point detection。
8. 无 clean trigger/no-op 或 failure fallback；算法每帧固定运行。
9. 它是可复现的 global large-offset strong-cheap B2 candidate，可压住单纯“扩大 operating range/减少 global candidate decode”的声称。
10. 对拟议 local repair chain 的 verdict 是 `PARTIAL_CORE_ONLY`，claim ceiling `SLICE`。

## 6. 未决/失败项

- `NOT_STATED`：Monte Carlo trial count/seeds/error bars、measured latency/memory、clean false-correction rate、fallback、开源代码。
- 未验证：fading/FSO/turbulence、真实时变 Doppler trajectory、cycle-slip injection、segment/suffix recovery、跨 code/modulation 泛化。
- 单篇不能证明它是全领域 strongest B2；只能给出可复现实例与明确预算。

## 7. 写入清单

- `papers/_read_notes/10.1109_iwcmc58020.2023.10182805.md`
- `projects/thesis-fso/worker-logs/step-063-c1-iwcmc2023-fulltext-read.md`
- 工具生成 acquisition assets：`papers/doi/10.1109_iwcmc58020.2023.10182805/{10182805.pdf,10182805.meta.json,metadata.json,content.md}`

未修改 topic-index、decisions、mission-log、master-state、registry、voice/profile、代码或 p05；共享 worktree 中既有脏状态不由本 worker 清理或归因。

## 8. 时间、git 与 p05 保护

- acquisition receipt 起点 `2026-08-09T22:02:57+08:00`；在 15 分钟预算内收口。
- 未 stage、未 commit、未 push。
- p05 收尾应保持：
  - `p05_run.log` `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log` `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log` `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log` `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`

