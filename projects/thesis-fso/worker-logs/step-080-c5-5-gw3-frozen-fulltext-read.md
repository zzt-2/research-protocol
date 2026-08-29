# Step 080 — C5-5 GW Step 3 frozen-fulltext read

> 2026-08-30 | T080 / D059 / V034 / CP021 | fulltext-read-only package

## 1. Terminal

```text
STEP3_C5_5_Q_SURVIVES_READY_FOR_STEP3_5
```

- read count：`2/2`；identity：`2/2 PASS`。
- Q#：`Q-C5-5`，唯一，M-C-A 四判据 `4/4`。
- ordinary early-stop：`NOT_COMPLETE_ABSORPTION / MANDATORY_CHEAP_COMPARATOR / EMPIRICAL_ABSORPTION_UNKNOWN`。
- claim ceiling：目标 DP-(8,8)-16APSK coherent-FSO 接收机中，当前码字 LLR 派生的 receiver-visible predecode reliability 驱动 fixed NMS/OMS per-codeword iteration cap 的经典预算迁移/扩展。
- blocker：无 candidate-level Step 3 blocker；P0 2019 合格全文缺失仍是 Step 3.5 exact-collision/provenance debt，且 ordinary early-stop 的实证吸收与 equal-update 公平性尚未验证。

## 2. 起点与控制

- worktree：`C:\Users\zzt\.codex\worktrees\7190\research-protocol`
- start/authority HEAD：`bc5c0cbff3528d1c24db9a2775b3d23dc1aff232`
- start branch：detached HEAD；start `git status --short` 为空。
- task-control：epoch `21` / CP021 / `C5_5_GW_STEP3_FROZEN_FULLTEXT_READ`；fresh validator=`PASS`。
- 本任务只允许 frozen two-paper Step 3；未修改 `.sessions/`、Skill/controller、论文正文或 decoder；未搜索、下载、实现、仿真、实验或进入 Step 3.5。

## 3. 前置读取

读取并核对：T080、topic-index CP021、D059/V034、S028 mission checkpoint chain、master-state current authority、T078/T079 及其报告/worker logs、`stages/groundwork.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md`、`templates.md` literature-notes/experiment-completeness 模板、`thesis-lessons.md` TL-31–33/速查、两篇 metadata、既有 He read note 与项目 read-log。authority commit 与当前 HEAD 完全一致。

## 4. 全文分工与主任务复核

1. 只读 subagent A 完整精读 Liu 2025；按 14+字段、7 子表、实验完备性、C5-5 专属动作链和九字段返回。identity PASS；无文件写入、联网或实验。
2. 只读 subagent B 完整精读 He 2021；从 canonical content 重核既有 note 的 C5-5 视角。identity PASS；保留 plaintext `source.pdf` debt；无文件写入、联网或实验。
3. 主任务逐行复核 Liu `content.md:53-145,161-203` 与 He `content.md:47-111,139-202` 的承重位置，重点核对 input/action/granularity、stop/cap 与成本口径。
4. Liu `content.md` 缺公式图像；subagent 用同目录 canonical PDF 核对 Eq. (1)/(11)。He 只用 canonical `content.md` 承重，没有把 plaintext legacy source 称为 PDF。

## 5. 科学裁决

- Liu RL-CBP 的 direct state 是 decoder-internal check-belief residual，动作是局部 check-node/edge 更新顺序，fixed max=50；不是 current-codeword LLR-derived predecode reliability、每码字 `num_iter` 或跨码字预算。因此为 `STRONG_NEIGHBOR/PRIMITIVE_OVERLAP`，非 exact collision。
- He first stage 是 fixed cap=100 的 layered quantized NMS + CRC success stop；failure 后用 syndrome/TS 做 bit-flip rescue。ordinary stop 只在成功后停止，不能预先给困难码字更高 cap；但它可能吸收大部分平均成本收益，故必须作为同 decoder cheap comparator。
- 两篇都没有给 high-cap+ordinary-stop 与 external-reliability LUT 的 equal-total-update、平均/P95 cost 比较。故不能判 `ABSORBED_CLOSE`，也不能预写 BER/FER 或复杂度增益。
- P0 缺失阻止 prior-art closure/first claim，但 Liu recent direct substitute 足以在 candidate level 分离 internal schedule 与 external predecode budget interface；债务移交 Step 3.5，不使 Q#/IAO 为空。

## 6. 写入范围

1. `projects/thesis-fso/apsk-soft-receiver-groundwork/c5-5-step3-fulltext-read.md`
2. `papers/_read_notes/10.1587_transfun.2024eal2080.md`
3. `papers/_read_notes/10.1109_wcsp52459.2021.9613326.md`（仅追加 C5-5 重读段）
4. `projects/thesis-fso/read-log.md`（新增 Liu；He reread 0→1）
5. `projects/thesis-fso/worker-logs/step-080-c5-5-gw3-frozen-fulltext-read.md`

## 7. 独立审查

未参与两篇提取的 reviewer 直接回查全文与所有产物，结论 `PASS_WITH_P2 / P0-P1-P2=0-0-4`，并独立确认 terminal、Q#、ordinary early-stop verdict、claim ceiling 与 blocker 均成立。四项 P2 已全部修订：

1. v0 input 从未证实的 pilot/channel summary 收窄为当前码字 LLR-derived predecode statistic；pilot summary 降为 Step 3.5 可选证据债务。
2. M-C-A 不再把 easy codeword 作为承重错配；聚焦 ordinary stop 尚未解决的 hopeless vs difficult-but-recoverable 统一 cap。
3. He 的 CRC timing 统一为 `CRC-pass stop / check cadence UNKNOWN`。
4. VVUQ 统一写成带分母的三元评分。

原 reviewer 对四项修订 fresh 复核为 `RECHECK: PASS`，确认无残留旧表述或产物矛盾，terminal 与 ordinary early-stop verdict 均未被修订破坏。

## 8. Fresh 收尾验证

- task-control validator：`PASS`。
- authority HEAD：`bc5c0cbff3528d1c24db9a2775b3d23dc1aff232`，精确匹配。
- deterministic identity：`2/2 PASS`；read-log：Liu=`1` row、He=`1` row，He reread=`1`。
- report tokens：唯一 terminal、Q#、ordinary early-stop 三段 verdict、LLR-derived v0、P0 debt 与 `2/2 PASS` 均存在。
- reviewer receipt：`PASS_WITH_P2 / P0-P1-P2=0-0-4`，修订后 `RECHECK: PASS`。
- scope audit：无 `.sessions/`、Skill/controller、decoder、仿真或论文正文改动。
- `git diff --check`：exit `0`；deterministic verifier failures=`0`。

## 9. 唯一下一步

回主控决定是否另开 bounded Step 3.5 exact-recipe/collision closure。本任务不自行进入 Step 3.5。
