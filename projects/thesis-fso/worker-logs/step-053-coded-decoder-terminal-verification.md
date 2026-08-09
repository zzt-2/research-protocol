# Step 053 — Coded decoder-feedback Step 1 terminal verification

> 2026-08-09 | T007 | action class: `VERIFY`
> fresh task-control validator: `PASS`
> verdict: `FAIL`

## Findings first

计数：**P0=0 / P1=2 / P2=1**。

### P1-1 — 首轮自动镜像未进入 integration，`replacement=0` 尚不可独立验收

- `search-archive/2026-08-09/code-aided-phase-ambiguity-finite-phase-hypothesis-ldpc-deco.json` 可解析，`total=28`、`results=28`，但无 `priority`、route relation 或逐条 disposition。
- 以 DOI → arXiv → normalized title 与 integrated 46 records 对齐时，仅 **4/28 exact overlap**，其余 **24/28 exact-key unmatched**。其中部分显然是截断题名/同族材料，但至少 row 14 `Phase Estimation by Message Passing`、row 20 `Joint Carrier-Phase Synchronization and LDPC Decoding - Tech Briefs`、row 22 `An Efficient Iterative Synchronization Scheme for LDPC- ...` 含 joint decoding/phase recovery 或 carrier-synchronization 动作线索，不能在未标注时视作已排除。
- integrated JSON 的 `input_globs` 仅含 `coded-decoder-c1-*.json` 与 `coded-decoder-c2-*.json`，因此 65 annotated rows、46 unique 和 replacement sketch 均未覆盖该镜像。现有 C1/C2 collision receipts 可能被这些条目加强，但“没有不同 action、replacement=0”是全语料排除结论；在 24 条未处置 exact-key unmatched rows 存在时，终验不能代替 route reviewer 作科学补标。
- 其他 generic mirrors：`code-aided-phase-ambiguity-resolution-ldpc.json` 为 15 results、15/15 exact overlap；`code-aided-carrier-synchronization-phase-estimation-ldpc.json`、`crc-syndrome-parity-check-aided-cycle-slip-detection-correct.json`、`cycle-slip-correction-fec-coherent-optical.json` 均为 0 results。它们不形成同等级 blocker。

**最小修复**（不新检索、不全文、不实验）：对上述 28 rows 逐条给出 deterministic duplicate/irrelevant/action-relation disposition 和 provenance；把有效非重复项纳入同一 DOI→arXiv→title 合并，重生成 integrated JSON/report。若仍维持 terminal，必须 fresh 复算并证明：所有镜像 rows accounted-for、C1/C2 collision receipts 不降级、replacement accepted 仍为 0。不得为了维持原 disposition 反向补标。

### P1-2 — T007 超过 8 分钟硬上限

本 verifier 未在任务书规定的 8 分钟内收口。该过程违规不改变已取得的文件证据，但违反 T007 的执行完整性合同，因此不能给出 `PASS`。

**最小修复**：完成 P1-1 后，用 fresh context 在预先冻结的 ≤8 分钟命令清单内重跑 validator、计数、镜像 coverage、git/status 四组检查；日志记录开始/结束时间与每组 exit code。

### P2-1 — 注册表/专题展示元数据滞后于 CP003

`.sessions/_registry.yaml` 的本专题 `last_updated/description` 仍停在 D001/CP001；`topic-index.md` 顶部“当前阶段”仍写“入口恢复与候选收敛”，而同文件 foreground control、master、D003、mission-log 已到 CP003/TERMINAL_VERIFICATION。权威 control block 本身一致，故不升为科学 blocker，但恢复入口存在误导风险。

**最小修复**：治理收口时只刷新 registry 与 topic-index 展示字段到 CP003/terminal-verification；不改变 D003 scientific disposition。

## 逐项验证

| # | 项目 | 结果 | fresh evidence |
|---|---|---|---|
| 1 | JSON、65/46/39/6/7、R2=2/2、IDC 2007 别名 | **PASS（仅 contracted prefixed corpus）** | 全部 `coded-decoder-c1/c2-*.json` 均可解析；结果数 C1=28、C2=37，共 65。普通 DOI/arXiv/title union 得 47 components、40 published、6 must-read；将 `LDPC Code Aided Phase Ambiguity Resolution` 与长题名 `...for QPSK Signals Affected by a Frequency Offset` 按同一 DOI `10.1109/IDC.2007.374550` 合并后为 46 unique、39 published。integrated 记录列出两题名 variants。C1/C2 各有 2 个 `-r2` 文件，integrated source families=7。P1-1 限制语料完备性，不否定这组 prefixed 复算。 |
| 2 | C1/C2 collision receipts 与 TSP ceiling | **PASS** | C2：`coded-decoder-c2-r1-direct-s2.json#row-1` 摘要支持 turbo-decoder extrinsic LLR → iterative ML phase estimation。C1：`coded-decoder-c1-r2q1-finite-bank-action.json#row-1`/official arXiv `2511.21340` receipt 支持 decoder extrinsic model evidence → finite candidates → one selection。integrated adjudication 将 TSP 2006 降为 `STRONG_NEIGHBOR`，未用题名过度声称 exact timing/budget。 |
| 3 | replacement=0 与历史边界 | **FAIL** | D028 仅 stale rollback、D047 仅 observation/relock family、P05 仅 dual-pol swap slice、F4-C 仅 final relabel 的 scope ceiling 在 integrated report 中保持；但 P1-1 的 28-row 未审镜像使 replacement=0 的穷尽性不可验收。 |
| 4 | `NO_VALID_PROBLEM` scope ceiling | **PASS** | topic/D003/mission/master 均把它限定为本专题 Step-1 action-survivor terminal；未声称领域无问题、B2 已解决或 testbed 不可建。 |
| 5 | topic/master/decision/mission、下游冻结、P08 ceiling | **PASS WITH P2** | foreground control、master Step table、D003、CP003 一致：survivor=0、Step 2/adapter/MVE/Contract/Execute 禁止，P08/R/R2 仍为 PARTIAL ceiling；仅展示元数据见 P2-1。 |
| 6 | protected files、p05 logs、pyc noise | **PASS（提交前仍须排除噪声）** | `git diff --cached --name-status` 为空；无 `.py`/adapter/scientific artifact 变更。四个 `p05_run*.log` 仍为 2026-07-30 的既有 untracked/unstaged 文件；五个 `tools/litsearch/__pycache__/*cpython-312.pyc` 为 tracked modified noise、均未 staged，最终提交必须显式排除。 |

## Verdict

`FAIL`

失败仅表示当前 terminal evidence package 的**完备性/执行合同**未通过独立终验；本 verifier **不改写** D003 的 scientific disposition，也不授权 Step 2、adapter、实现或实验。
