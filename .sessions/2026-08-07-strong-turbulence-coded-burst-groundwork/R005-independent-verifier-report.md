# [R005] Step 1 独立验证报告

> 2026-08-07 | 关联：T004 | 仅静态复算；未运行 Python/import/测试/仿真

## 验证方法

只用 PowerShell、`rg`、`Get-Content`、`git`；不信任 R001–R004 摘要，回到 JSON、全文、源码、原始结果和历史验证记录。

## 验收表

| # | 项目 | 结论 | 证据 |
|---:|---|---|---|
| 1 | HEAD | PASS | `12c54b3409dcc46c3bf4bf202380a38eae069562`，与 S001 一致 |
| 2 | registry | PASS | 目标 slug 仅 1 条，closed，2 个 depends_on，conflicts=[] |
| 3 | 治理模板 | PASS | topic/S001/D001-D002 锚点齐全，topic 与 master-state 进度一致 |
| 4 | 6/6 query | PASS | T001 两组本地检索 + T002 四个固定 JSON，无第 7 组 |
| 5 | count/hash | PASS | 独立解析与 R004 全同，见下 |
| 6 | 三源门 | PASS（未过） | 四 JSON 均仅 `s2,openalex`；本地全文不是第三搜索 API |
| 7 | 近期严格 baseline | PASS | 仅 Sun & Noh 2025 一篇，故为 1，不是 0，也未达 2 |
| 8 | R001 物理门 | PASS | 强起伏/GG 有推导；目标 occurrence+threshold-conditioned AFD 未闭合 |
| 9 | R002 collision | PASS | 2012 是 burst-information-driven depth switching；P08/AMC action 均不同 |
| 10 | R003 四门 | PASS | lifecycle=PARTIAL、controllability=NO、schema=PARTIAL、metric=NO 均有源码支持 |
| 11 | 预卡/reopen | PASS | A/B/C 各 12 字段；6 项 reopen gate 无候选全 PASS |
| 12 | outage 六问 | PASS | 六问齐全，target oracle/AFD/weak-block count 仍 UNKNOWN |
| 13 | Step 2 | PASS（未执行） | papers 无 Git 变化；5 个 CORE 候选目录均不存在；无 coded-chain 新结果 |
| 14 | forbidden paths | PASS | common/、params.py、旧 raw/result、Skill、p05 logs 未被本轮改动 |

## 8 条以上原始事实复算

1. SPIE 1999/2002 abstract 只支持大天顶角强起伏与 GG；无 target 数值/AFD。
2. TVT 2022 原文称其 HV 条件下 LEO-ground `Rytov<1`；`Cn²=1e-13` strong 是仿真分组。
3. 同文 200 blocks/burst 缺 block→symbol 映射，不能等同 810 symbols。
4. 2023 外场为 53.42 km terrestrial surrogate；few-ms、SI 1–4 不能移植为星地 occurrence。
5. OJCOMS 2024 的 10 ms、2.5 Gbaud、PSI=10 是模型输入；不证明 recoverable burst。
6. TAES 2024 测量 Rytov=0.0075/0.1020，均为弱区；1 ms 是采样间隔。
7. Sun 2025 abstract 同时含 temporal correlation、burst、interleaving depth 与 reliability，严格 baseline=1。
8. Zhang 2012 abstract 明示按更新 burst information 改 depth，属旧 4b#1 exact collision。
9. P08-R2 源码一次生成 6176 symbols；16×384=6144 data+32 prefix；底层为全长 blockwise AR(1)。
10. raw 未保存 `cw_err` 向量/boundary，final 的 `elapsed_sec` 不是通信 delay。
11. 工期独立加总：adapter 3.75–5.0 人日；完整 testbed 8.5–12.0 人日。
12. P08-R2 原始 gate：B0 all-cw-fail=3/40，O2=2/40；与 R004 一致。
13. 旧 4b#1 原始验证：Lburst=60–428、capacity=810、overflow=0/15、BER gain=0 dB。

## JSON count + SHA256

- correlated-interleaving：20；`ac06590665000c45e31c73aa580274f3982d05dfd0d50a63033cf97f31f94972`
- channel-aware-mapping：7；`e29f269e4ab22623eea5cd28a283e50737209fa7ab2c2decb23debbe5d36f932`
- parity-placement：20；`37a3988ea807251e63995ed53b4f7ee176de0cc0fdb289b6835b1a6ca6f86232`
- recent-baselines：0；`c40794548a87b0d37a0b2c509ba2f77dbaf5e6e0f4b04f317b725f10da5f7747`

## Terminal

应为 `STEP1_EVIDENCE_INSUFFICIENT`：target occurrence/AFD、recoverable cross-block span、第二篇 strict baseline、三源门均未闭合。

- 非 `OUTAGE_NOT_INTERLEAVING_PROBLEM`：只有风险锚点，无 target oracle/AFD。
- 非 `NO_2019_PLUS_TASK_MATCHED_BASELINE`：已有 1 篇，不是 0。
- 非 `TESTBED_SCOPE_EXCESSIVE`：>5 天是下游工程风险，不能覆盖上游证据门。

## 文件卫生与结论

Tracked 变化：registry、master-state、5 个 `tools/litsearch/__pycache__/*cpython-312.pyc`；后者时间与检索相邻，判工具副作用，提交前清理但不构成科学 blocker。Untracked 为本专题文件及 4 个既有 `p05_run*.log`；日志 mtime 为 2026-07-30，早于本专题。本 verifier 只写 R005。

**结论：ACCEPT；blocker=0。** 支持 D002/closed/Step 2 NOT_RUN；不授权 Step 2、coded-chain、MVE 或 claim。
