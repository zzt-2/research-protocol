# Worker Log — T012 C1 arXiv 2511.21340 全文获取与精读

> 2026-08-09 | executor: `/root/c1_arxiv2511_read` | evidence worktree only

## 1. Task-control 与范围

- 任务书：`.sessions/2026-08-09-coded-decoder-feedback-groundwork/T012-c1-arxiv2511-fulltext-read.md`
- validator：`python .agents/skills/research-direction-lab/scripts/validate_task_control.py <T012>`
- 结果：`PASS`
- control binding：epoch `6` / action `FULLTEXT_READ` / checkpoint `CP006`
- 范围确认：仅全文获取、title check、精读、single-paper collision ceiling；未改 topic/master/decision/mission/literature owner，未做 adapter/MVE/experiment/Go/Kill，未提交。

## 2. 获取命令、通道与结果

1. 初次 dry-run 从仓库根 pipe wrapper，失败：wrapper 将 `paper_download.py` 错解析到仓库根；无论文产物。
2. 按 T012 明示的 CRLF 等价调用切到 `tools/`：
   - dry-run：`cd tools && tr -d '\r' < download | bash -s -- --dry-run --arxiv 2511.21340` → PASS，目标 `papers/arxiv/2511.21340`。
   - 正式：`cd tools && tr -d '\r' < download | bash -s -- --arxiv 2511.21340` → `[OK] arxiv_latex ... content.md (good)`。
3. 下载通道：`arxiv_latex`。
4. 源文件：
   - `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/arxiv/2511.21340/source.tar.gz`
   - `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/arxiv/2511.21340/content.md`
   - `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/arxiv/2511.21340/metadata.json`
5. `content.md`：172 行，29980 bytes；metadata quality=`good`。

## 3. Title check

- metadata：title 空、`title_check=unverifiable`，故按 gw-read 人工抽检。
- 派遣标题与 source package `main.tex:84` 的 `\title{Phase-Aware Code-Aided EM Algorithm for Blind Channel Estimation in PSK-Modulated OFDM}` 逐字一致。
- token overlap：`1.00`。
- verdict：`PASS`，继续全文精读。
- 注意：`content.md:5` 的 Shell sample header 是 IEEEtran 页眉占位，不作为真实标题。

## 4. 关键结论（≤10 条）

1. 方法处理 **frame-global constant phase ambiguity**，不是 local/time-varying slip。
2. `C` 个 PSK circular-label hypotheses覆盖 entire observation matrix；QPSK时 `C=4`。
3. 每个 hypothesis 经 parallel demapper/deinterleaver/convolutional decoder 得 posterior，再形成 whole-frame model evidence。
4. 选择在 20-EM initialization 后运行一次；后续 turbo iterations不重复 candidate search。
5. 相对 conventional branch 一次性新增 `C-1` decoder-equivalent evaluations；QPSK为3；未报告wall-clock latency。
6. 输出是全局 `φhat` 和 `Hhat exp(-jφhat)`；无 boundary、segment 或 suffix output。
7. evidence ratio不足 `10^3` 时不做 refinement；clean-frame false trigger / identity test `NOT_STATED`。
8. 实验为5000 runs、固定三抽头+global random phase+AWGN；SNR≥6 dB 时 FR从约78%降至近0。
9. dynamic fading/rapid phase/per-subcarrier ambiguity 被列为 future work，不能据此预写 target defect。
10. `collision_verdict=PARTIAL_CORE_ONLY`；只碰撞 global one-shot core，不覆盖局部 repair 完整链。

## 5. 未决/失败项

- 正式发表 venue/DOI：`NOT_STATED`，本任务未作外部检索。
- general turbo-iteration 总数：正文 `NOT_STATED`；source Fig. 2 仅标出 EM 25/30/35 的 code-aided updates。
- selected decoder branch 后续如何 hand off、unresolved ambiguity 的具体 fallback：`NOT_STATED`。
- local slip occurrence、boundary observability、segment/suffix recoverability、clean-frame no-op：均未覆盖。
- 第一次 dry-run 的 cwd 解析失败已按任务书允许的 `cd tools` 调用修正；不是下载通道失败。

## 6. 写入文件

- `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/_read_notes/2511.21340.md`
- `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/thesis-fso/worker-logs/step-058-c1-arxiv2511-fulltext-read.md`

下载器另按仓库既有行为写入 `papers/arxiv/2511.21340/` 并更新 `papers/index.json`；未手工编辑中央研究状态或 literature owner。

## 7. 耗时与 git/protection 检查

- 开始读取任务书：约 `2026-08-09 21:44 +08:00`。
- 产出与 fresh protection check 完成：`2026-08-09 21:59 +08:00`。
- 总耗时：约15分钟。
- 初始 worktree 已有主控/并行任务改动；本任务未覆盖或回退它们。
- 四个受保护日志初始 SHA-256：
  - `p05_run.log`：`7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log`：`735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log`：`c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log`：`95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- 结束 fresh protection check：上述四个 SHA-256 **4/4 unchanged**；`git status --short -- <4 logs>` 无修改项。
- 结束目标状态：read-note 与论文目录受既有 ignore 规则管理；worker-log 为 untracked；`papers/index.json` 在初始检查时已 modified，下载器追加 `arxiv:2511.21340` 索引；未暂存任何文件。
- git commit：未执行。
