# Step 059 — C1 TSP 2006 全文获取与完整链精读

> 日期：2026-08-09  
> 任务：T013  
> 状态：`FULLTEXT_READ / PARTIAL_CORE_ONLY`  
> 范围：仅 Groundwork Step 2 acquire/read；不改中央 owner，不形成 Q#、Go/Kill，不实现、不仿真、不提交。

## 1. Task-control

| 检查项 | T013 | 当前控制面 | 结果 |
|---|---|---|---|
| schema | `rdl.task-control.v2` | `rdl.foreground-control.v2` | PASS |
| control epoch | `6` | `6` | PASS |
| mission checkpoint | `CP006` | `CP006` | PASS |
| action class | `FULLTEXT_READ` | `allowed_actions` 含 `FULLTEXT_READ` | PASS |
| forbidden action | no experiment/adapter/claim | topic-index 同步冻结 | PASS |

执行命令：`python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T013-c1-tsp2006-fulltext-read.md --repo-root .`；返回 `PASS`。

## 2. 规范与范围核验

- 已完整读取 T013、`stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`，并读取 `domain-comms.md §1.1`。
- 已按 RDL foreground control 读取 topic-index/mission checkpoint；当前为 `CP006 / GROUNDWORK_STEP2_ACQUIRE_READ`，本任务在 scope 内。
- registry 当前专题 `conflicts_with=[]`；依赖已登记；专题只有 1 个 `S###`，无 inflation blocker。
- 已读取当前 decisions 与 thesis-lessons，避免把历史 core-action collision 越级写成完整链或 problem verdict。

## 3. Acquisition receipts

目标：*Code-Aided Frame Synchronization and Phase Ambiguity Resolution*，DOI `10.1109/TSP.2006.874844`。

| 顺序 | 通道/命令 | 结果 |
|---:|---|---|
| preflight | `cd tools && tr -d '\r' < download \| bash -s -- --doi 10.1109/TSP.2006.874844 --dry-run` | PASS；目标 `papers/doi/10.1109_tsp.2006.874844` |
| 1 | 同命令去掉 `--dry-run` | FAIL：`[FAIL] all_failed`；`metadata.json` 留下 `2026-08-09T21:50:50+08:00` failure receipt |
| 2 | Semantic Scholar DOI + arXiv exact-title query | S2 标为 `CLOSED`/无 OA PDF；arXiv `totalResults=0`，无可核验 alias |
| 3a | 任务书旧式 `blit --download --doi` | 当前 CLI 要求 `--source` 和 `--download DIR`，contract mismatch；未算作科学失败 |
| 3b | 当前 CLI 等价 IEEE 精确题名下载：`--source ieee --max 3 --download ../papers/doi/10.1109_tsp.2006.874844` | 1/1 PASS；`1643913.pdf`，823534 bytes |
| convert | 项目 `tools/convert`，fast quality | 生成 1914 行、89666-byte `content.md`；无自写 PDF 转换器 |

三轮后停止；未用 webReader/ResearchGate/Google Scholar 页面抓全文，未追加第四下载通道。

## 4. Source/title/quality gate

| 字段 | 结果 |
|---|---|
| PDF | `papers/doi/10.1109_tsp.2006.874844/1643913.pdf`，823534 bytes |
| Markdown | `papers/doi/10.1109_tsp.2006.874844/content.md`，1914 lines / 89666 bytes |
| 正文题名 | `content.md:5` 与派遣标题一致；PDF 首页同题名 |
| 自动 mismatch | `1643913.meta.json` 误把期刊页眉当题名；人工复核后 `PASS_FALSE_POSITIVE_AUTO_MISMATCH` |
| 内容质量 | `>50` 行；method/experiment/conclusion 完整，公式/表格另以 PDF pp. 2751–2756 视觉核验 |

## 5. 关键事实（≤10 条）

1. 论文模型是每 burst 一个恒定整数 frame-start shift 与一个恒定 rotational phase ambiguity，不是 within-frame/time-varying cycle slip。
2. 四种 practical code-aided 方法逐一测试全局 `(k_theta,k_tau)` hypotheses；SPA 才把所有 hypotheses 同时放入 overall factor graph。
3. decoder evidence 分为 hard decoded bits/symbols、extrinsic-LLR mode separation、SPA pseudomarginal、APP-derived soft-symbol EM metric。
4. practical flow 是每候选 `I_H` 次 decoder iterations → 一次全局 argmax → winner 剩余 `I_C-I_H` iterations；不是逐 iteration 局部 repair。
5. turbo case 固定 `M_theta=4`, `M_tau=3`, `I_C=10`, `I_H=1`：12 个 candidates 各 1 iteration，再对 winner 做 9 iterations。
6. 论文没有 slip-boundary variable，也没有 segment/suffix rotation、rollback 或 selective re-decode。
7. 没有 clean trigger/no-op、confidence abstention 或 repair-failure fallback；零 ambiguity 只是 candidate bank 中 `(0,0)`。
8. FS 与 PAR 共用同一 code-aided metric family，公式可对 joint pair 直接 argmax；但 FS 的短环失效与 PAR 的旋转对称失效不同。
9. PAR 不要求改 code、CRC、truth 或 known sync word；pilots/uncoded bits可选，code/mapping 可辨识性仍是必要条件。
10. 完整链 verdict 为 `PARTIAL_CORE_ONLY`：确认 B1 的 global core chain，不构成 local-slip complete-chain collision。

十问、额外问、通信参数、非 ML N/A、M/C/A 四判据、实验完备性、八字段矩阵与 `SLICE` claim ceiling 均已写入 read note。

## 6. 未决与证据上限

- `NOT_STATED`：local slip boundary、clean-frame false trigger/no-op、repair failure fallback、measured latency/memory、seeds/error bars/statistical tests、开源代码。
- 未验证：coherent-FSO local slip defect、decoder observability、segment/suffix recoverability、与未来 C1-ext 同信息/同局部性/同预算公平性。
- 不生成 Q#，不判 C1-ext Go/Kill，不把 title 中 “frame synchronization” 当 slip-boundary localization。

## 7. 写入清单

- read note：`papers/_read_notes/10.1109_tsp.2006.874844.md`
- worker log：`projects/thesis-fso/worker-logs/step-059-c1-tsp2006-fulltext-read.md`
- acquisition artifacts（工具生成）：`papers/doi/10.1109_tsp.2006.874844/{1643913.pdf,1643913.meta.json,metadata.json,content.md}`

未修改 topic-index、decisions、mission-log、master-state、registry、voice/profile 或其他中央 owner；共享 worktree 中这些文件的既有脏状态不由本 worker 清理或归因。

## 8. 时间、git 与 p05 保护

- acquisition receipt 起点：`2026-08-09T21:50:50+08:00`；任务在 15 分钟上限内收口。
- 未 stage、未 commit、未 push。
- 四个受保护日志收尾 SHA256 应为：
  - `p05_run.log`: `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log`: `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log`: `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log`: `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
- 收尾复核项：两份指定产出存在；p05 4/4 hashes 不变；`git diff --cached --name-only` 为空；无 commit。

