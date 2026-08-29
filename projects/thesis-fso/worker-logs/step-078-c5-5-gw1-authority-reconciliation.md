# Step 078 — C5-5 GW Step 1 authority reconciliation

> 2026-08-30 | T078 / D057 / V032 / CP019 | read-only authority package

## 1. Terminal

```text
STEP1_C5_5_EVIDENCE_GAP_BOUNDED
```

Q-C5-5 的 M-C-A、receiver-visible IAO、baseline/fairness 与 budget-only 最小接口路径成立；直接 residual/informed scheduling 全文缺失，故不升 `PASS_READY_FOR_STEP2`。唯一下一步是主控另派 bounded Step 2 acquisition/read；本任务未自行进入 Step 2。

## 2. 起点与控制

- worktree：`C:\Users\zzt\.codex\worktrees\60fe\research-protocol`
- start HEAD：`d7acd9f7b1e1583d47280ef93cbdb89db58e2df9`
- start `git status --short`：空
- branch authority：`refs/heads/codex/rdl-method-production-v2` 指向同一 start HEAD；未切换到 `D:\code\study\research-protocol` 根检出
- task-control：epoch `19` / CP019 / `C5_5_GW_STEP1_AUTHORITY_RECONCILIATION`
- validator：`PASS`

## 3. 执行事实

1. 完整读取 T078，并读取 Groundwork Step 1、问题四判据、通信领域规则、thesis-lessons 速查/TL31–33、T041/T044/T046、D057/V032 与 master-state CP019。
2. 读取 LDPC receiver authority、T044 coverage、C5-1 Step 3/3.5/4a 报告、coded-decoder-feedback 相邻报告及 T049/T076/T077/T118 指定 worker logs；没有继承旧候选的 formal progress。
3. 检查 `papers/index.json`、`papers/_read_notes/` 与实际 `papers/**/content.md`。Wu 2010、He 2021、Baldi 2016、Zhao 2023 全文存在；2019 residual-decaying informed scheduling 与 Chen–Fossorier exact fulltext 不存在。没有把标题/摘要写成全文结论。
4. 使用 `C:\Users\zzt\.venvs\torch\Scripts\python.exe` 只做 Sionna 2.0.1 import/signature introspection，并读取安装源码；没有调用 decoder 或运行科学样本。
5. 审计目标 wrapper 与 underlying backend：当前为 fixed `alpha=.75`、20 iterations、default flooding、hard info only、fresh state；目标 APSK→BG2/Z=104 correctness 已由 T076 的 fresh tests authority 支持。

## 4. 主要结论

- Q-C5-5：fixed NMS/OMS 在目标 codeword-reliability heterogeneity + bounded compute 条件下，因静态 schedule/统一最大预算不使用当前码字 reliability/syndrome/stall 分配后续 updates；候选只做 decoder budget/order，不改前端或 demapper。
- 最小 v0：channel-LLR risk + fixed checkpoint → bounded `STOP/CONTINUE`/per-codeword iteration allocation；动态 layer/edge priority 暂不作为最小动作。
- 主要吸收：Wu 2010 吸收 syndrome-conditioned alpha/beta；He/Baldi/Zhao 吸收 ordinary early-stop、failure-triggered extra work、syndrome/bit-flipping rescue；fixed extra iterations、flooding/layered 与 static LUT 是强制 cheap alternatives。
- 接口门：Sionna per-call `num_iter`、callbacks、state、soft/full output 属库级能力；当前项目 seam 缺失。budget-only adapter 有界且不需自写 BP；动态 per-codeword CN priority 仍无现成 seam。
- direct collision：UNKNOWN。T041-003 只有 identity/metadata，没有本地 fulltext/read note。

## 5. 写入范围

仅新增：

1. `projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step1-authority-reconciliation.md`
2. `projects/thesis-fso/worker-logs/step-078-c5-5-gw1-authority-reconciliation.md`

未修改 `.sessions/`、Skill/controller、框架、仿真/decoder 代码、论文正文、旧结果或 canonical tracking；未下载论文、未实现 adapter、未仿真、未进入 Step 2。

## 6. 停机与回传

- Q#：`Q-C5-5`，四判据形式 `4/4`，但 direct scheduling fulltext gap 阻塞 Step 1 PASS。
- IAO：`channel LLR / optional syndrome-stall → bounded BP budget/order → hard bits + stop/cost receipts`；truth denylist 已冻结。
- terminal：`STEP1_C5_5_EVIDENCE_GAP_BOUNDED`。
- 唯一下一步：主控另派 C5-5 Step 2，取得 T041-003 并至多补 1–2 篇 recent direct scheduling/budget fulltexts；不实现。
