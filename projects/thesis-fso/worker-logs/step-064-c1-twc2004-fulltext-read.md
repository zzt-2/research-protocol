# Step 064 — TWC 2004 iterative decoder-aided CPR 全文精读

> 日期：2026-08-09  
> 任务：T018  
> 状态：`FULLTEXT_READ / PARTIAL_CORE_ONLY`  
> 范围：仅 Groundwork Step 2 acquire/read；不改中央 owner/治理/代码，不形成 Q#、Go/Kill，不实验、不提交。

## 1. Task-control

| 检查项 | 结果 |
|---|---|
| schema / epoch / checkpoint | `rdl.task-control.v2 / 6 / CP006` 与 topic control 一致 |
| action class | `FULLTEXT_READ` 在 allowed actions 内 |
| forbidden boundary | 未进入 adapter/MVE/Contract/Execute/thesis claim |
| validator | `python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T018-c1-twc2004-fulltext-read.md` → `PASS` |

## 2. 执行规范

- 已按 `gw-acquire` 三轮止损、`gw-read` title/content gate、glossary M/C/A 四判据和 `domain-comms §1.1` 通信参数字段执行。
- 当前仍为 `CP006 / GROUNDWORK_STEP2_ACQUIRE_READ`；本 worker 只写独立 read note 与 worker log。
- PDF 版面核验覆盖 article pp. 2267–2276：title/abstract、Eqs. (1)–(29)、Figs. 1–4、实验配置、Figs. 5–10 与 conclusion。

## 3. Acquisition receipts

| 顺序 | 通道/命令 | 结果 |
|---:|---|---|
| preflight | `tools/download --doi 10.1109/TWC.2004.837407 --dry-run`（CRLF workaround） | PASS；规范化目录 `papers/doi/10.1109_twc.2004.837407` |
| 1 | `tools/download --doi 10.1109/TWC.2004.837407` | PASS：Unpaywall → White Rose author-deposited PDF；自动转换 `content.md` quality=`good` |
| 2/3 | arXiv / IEEE blit fallback | `NOT_RUN`；第一轮已成功，按止损规则不扩通道 |

获取资产：`source.pdf` 596142 bytes；`content.md` 2028 lines / 87392 bytes；`metadata.json` 记录 `download_method=unpaywall`、`download_status=success`。

## 4. Title/quality gate

- 派遣标题与 `content.md:29`、PDF p. 2267 标题完全一致；人工 normalized overlap=`1.0`，`PASS`。
- metadata 自动 `title_check=unverifiable` 仅因元数据 expected title 空，不否定人工 exact match。
- 存档封页 DOI 多一个 0（`TWC.20004...`），但 article 页脚与 metadata 均为正确 DOI；不是错文。
- 全文方法、实验、结论完整；公式通过 PDF 视觉核验，未用摘要承担 collision 裁决。

## 5. 关键事实（≤10 条）

1. APPA 使用上一轮 component-decoder extrinsic/a-priori bit LLR，不是硬判决或 transmitted truth；LLR 被转成 symbol prior 后进入 block phase LLF。
2. outer iteration `l` 同时运行一次 estimator pass 与一次 turbo decoding iteration；decoder/corrector 用 `l-1` 的相位/LLR，新结果在 `l+1` 生效。
3. 首轮相位与 LLR 均初始化 0，phase correction 为 identity、estimator 自动退化为 NDA；典型联合收敛为 6 轮。
4. phase state 是每 whole block/fixed sub-block 一个 continuous scalar；没有 slip flag、boundary index、change-point 或 adaptive localization。
5. 可固定切短 sub-block 容忍更大 CFO/slow fading，但正文明确不稳健于 large CFO/fast fading；这不是局部 slip detector。
6. base APPA 有 BPSK 180°/QPSK 90° ambiguity；可选 2/4 个完整 joint units 按 whole-block mean-square LLR 选解，只是 global finite hypotheses。
7. clean/no-slip 仍固定运行全部 estimator/decoder iterations；无 clean no-op、false-trigger rate 或 identity guarantee。
8. Fourier + piecewise lookup 降低 estimator 非线性成本，但 block buffering、4/6/8 decoder iterations及可选 2x/4x bank 都没有 measured runtime/memory budget。
9. 实验为 AWGN、rate-1/2 16-state PCCC、BPSK/QPSK、block-constant phase；未注入 cycle slip 或测试 segment/suffix recovery。
10. 对 C1-ext 完整链 verdict=`PARTIAL_CORE_ONLY`：decoder-feedback/global CPR core 已碰撞，local trigger→boundary→segment/suffix action→fallback 没有碰撞。

## 6. 未决/失败项

- `NOT_STATED`：Monte Carlo trials/seeds/error bars、精确 operation count、runtime/memory/throughput、clean-frame cost、failure confidence、fallback、开源代码。
- 未验证：coherent FSO/turbulence、abrupt within-frame slip、动态 boundary localization、selective re-decode、higher-order modulation、fast fading。
- optional 2/4-unit ambiguity bank 的性能在 [16]/[17]，本篇只给结构性描述；不得把外部结果当作本篇完整实验。
- 2004 论文可作历史 direct comparator，但不独自满足本项目“近期 baseline”门，不生成 canonical Q#。

## 7. 写入清单

- `papers/_read_notes/10.1109_twc.2004.837407.md`
- `projects/thesis-fso/worker-logs/step-064-c1-twc2004-fulltext-read.md`
- 工具生成 acquisition assets：`papers/doi/10.1109_twc.2004.837407/{source.pdf,content.md,metadata.json}`

未修改 topic-index、decisions、mission-log、master-state、registry、voice/profile、代码或 p05；共享 worktree 中既有脏状态不由本 worker 清理或归因。

## 8. 时间、git 与 p05 保护

- acquisition/read receipt 起点：`2026-08-09T22:11:01+08:00`；在 15 分钟预算内收口。
- 未 stage、未 commit、未 push；收尾要求 cached diff 为空。
- p05 收尾必须保持：
  - `p05_run.log` `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log` `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log` `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log` `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
