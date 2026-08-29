# Step 079 — C5-5 GW Step 2 bounded acquisition

> 2026-08-30 | T079 / D058 / V033 / CP020 | acquisition-only worker package

## 1. Terminal

```text
STEP2_C5_5_READY_FOR_STEP3
```

Qualified fulltexts=`2`：2025 RL-CBP direct scheduling + 2021 NR-LDPC CRC/maximum-iteration early-stop comparator。P0 2019 未取得 canonical fulltext；项目 downloader 的 2007 arXiv 近似题名误配已按 identity mismatch 排除。2025 primary 提供动作等价 recent substitute，因此 Step 3 输入可冻结，但 P0-specific collision 仍不得声称闭合。

## 2. 起点与控制

- worktree：`C:\Users\zzt\.codex\worktrees\878b\research-protocol`
- start HEAD：`9e80cccf9120d5de82cdf6c0ef6cf81cb4b5ab83`
- branch authority：`refs/heads/codex/rdl-method-production-v2` 指向同一 start HEAD；当前 Codex worktree 为 detached HEAD，未切换到 `D:\code\study\research-protocol` 根检出。
- start `git status --short`：空。
- task-control：epoch `20` / CP020 / `C5_5_GW_STEP2_BOUNDED_ACQUISITION`；validator=`PASS`。
- 范围：仅 Step 2 acquisition；无 `.sessions/`、Skill/controller、论文正文、decoder、实现、仿真或旧结果修改。

## 3. 执行事实

1. 读取 T079、CP020、D058/V033、T078 两份产出、Groundwork Step 2 / gw-acquire、tools-guide 与本地 authority；未逐读历史 S/CP 链。
2. 本地复用检查确认 P0 无 canonical fulltext/read note，仅 T041 metadata；He 2021 comparator 已有 readable fulltext。
3. P0 单 DOI 项目 downloader 返回 `all_failed`。复用 T041 `pdf_url` 的定向 batch 下载时，title→arXiv enrichment 误配 `cs/0702111v2`；metadata `title_check=mismatch`，因此 rejected。
4. 使用 2/4 queries。Q1 得到 2025 RL-CBP OA primary；Q2 archive 可解析但候选不比 He 2021 更直接，没有继续扩大检索。
5. 2025 RL-CBP 经 project downloader `oa_pdf` 成功取得并自动转换；PDF 5 pages、content 100 effective lines、title/DOI match，公式、调度步骤和实验段存在。
6. He 2021 经本地 metadata/content 复核：title/DOI match，122 effective lines，maximum iterations、CRC early stop、算法与 results 可定位；legacy `source.pdf` 实为 plaintext，记录 source-format debt，不静默改旧资产。

## 4. Search / download usage

| 序号 | 动作 | 结果 |
|---|---|---|
| Q1 | exact P0 DOI/title，S2+OpenAlex+arXiv+Exa | 2 results；OpenAlex 命中 2025 RL-CBP；S2 rate-limited，arXiv 0，Exa无 key |
| Q2 | adaptive maximum iterations / reliability-aware early termination / iteration budget | 4 results；均未选入 pool |
| D1 | single DOI P0 | `all_failed` |
| D2 | T041-003 P0 batch | downloader success 但 title mismatch；rejected |
| D3 | Q1 L002 2025 RL-CBP | `oa_pdf`, title match；qualified |

Windows worktree 的 bash wrappers 带 CRLF，Git Bash 直接执行报 `line 32: $'\r': command not found`。为保持同一项目管线，本轮用 Windows torch Python 调用 wrapper 指向的 `tools/literature_search.py` 与 `tools/paper_download.py`；没有修改工具文件或使用外部浏览器。

## 5. 写入范围

- 新增主报告：`projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step2-coverage-report.md`
- 新增 worker log：`projects/thesis-fso/worker-logs/step-079-c5-5-gw2-bounded-acquisition.md`
- paper 增量：P0 mismatch metadata receipt（错误 source/content 已删除，避免污染 canonical cache）；2025 RL-CBP canonical DOI 目录。
- search 增量：两份 T079 archive；`papers/index.json` 自动登记 P0 mismatch 与 RL-CBP match。
- 无 read note：本任务禁止 Step 3 精读。

## 6. 冻结回传

- terminal：`STEP2_C5_5_READY_FOR_STEP3`
- qualified：`2/3`
- frozen Step 3 read pool：
  1. `papers/doi/10.1587_transfun.2024eal2080/content.md`
  2. `papers/doi/10.1109_wcsp52459.2021.9613326/content.md`
- anomaly：P0 downloader identity mismatch；不得把 `cs/0702111v2` 当 P0。
- 唯一下一步：主控另派冻结 pool 的 Step 3；本任务停机。
