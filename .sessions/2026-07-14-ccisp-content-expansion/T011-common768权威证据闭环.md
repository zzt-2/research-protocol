# Task Brief: common-768 30-seed 权威证据闭环

> 来源: S001 / D012 | 产出位置: `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py` 与同名 `.json`
> 日期: 2026-07-15
> 唯一文档: 执行方可读取本任务列出的源码、R004/R005 和项目规范；不得修改论文或图资产

---

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol`。现有 30-seed common-768 数字方向正确，但 JSON 尚未闭合论文级 provenance，点估计与 CI 也使用了两个不同统计对象。

**你的任务**：不改变 selector 算法、门限、参数、场景和 seed 设计，只补齐持久化、自检和 provenance，重新运行一次 30-seed × 9 点，产出唯一权威 JSON。

**产出**：更新后的 `_a4_switch_common768_30seed.py/.json`，以及回传中的数值与证据审计报告。

**最高纪律（违反一条即 FAIL）**：

1. 开始前完整读取 `sim-preflight` skill、`thesis-lessons.md` 速查表与最近三条、R004、R005；明确当前属于既有 selector 的证据闭环，不是新算法探索。
2. 不改 estimate/decide/demod、13 dB threshold、CV margin、channel parameters、SNR 点、seed 数、每 seed 400 windows 或 ambiguity-resolution 协议。
3. 论文唯一点估计必须是 30 个 paired-seed dB gains 的均值；95% CI 必须围绕同一组 paired-seed gains。pooled-count ratio 只能标为内部校验字段。
4. common oracle 必须在相同 768-bit population 上逐 window 取两固定分支错误数的较小值；不得沿用 1024/768 mixed oracle。
5. 不修改 `.tex`、绘图脚本、图资产、decisions/topic-index/voice；不提交 git。

---

## 1. 背景

旧 Fig.5 把 DA window 的 768-bit error count 与 NDA window 的 1024-bit error count 混合，不能解释为公平 BER。common-768 将两条路径都限制到同一组 192 个非 pilot 16APSK symbols，即每 window 768 bit。R005 的 30-seed 探针显示九点 paired-seed mean gains 均为正，但当前 JSON 的 `common768.gain_db` 是 pooled-count ratio，而 `gain_ci95` 来自 per-seed log gains；二者最多相差约 0.006 dB。另有 provenance、per-seed raw counts、branch counts 和 common-oracle 缺口。

这些背景只用于理解任务。不得在论文式输出中讨论旧 mixed 指标。

## 2. 必读与事实核验

按顺序读取并在回传中给出路径+行号：

1. `.sessions/2026-07-14-ccisp-content-expansion/R004-Fig5切换指标历史与语义审计.md` 的 metric signature。
2. `.sessions/2026-07-14-ccisp-content-expansion/R005-selector-common768-5seed-probe.md` 的 30-seed 结果。
3. `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py`。
4. `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.json`。
5. 脚本实际 import 的 common/params 文件。

先验证三条事实，再允许改代码：共同 mask 是否严格为 192 symbols；两分支是否共享同一 realization；算法/判据是否与原 5-seed probe 一致。任一 FAIL 则停止，不重跑。

## 3. 冻结的统计与 JSON 契约

每个 scene/SNR/seed 保存：

- `seed_index` 与实际 window seed 范围；
- `n_windows=400`、`n_bits=400*768`；
- `nda_common_errors`；
- `switch_common_errors`；
- `common_oracle_errors`；
- `n_select_da`、`n_select_nda`，且两者和为 400；
- `gain_db = 10*log10(nda_common_errors/switch_common_errors)`。

每个 scene/SNR 的 `paper_summary` 保存：

- `estimand = "mean paired-seed log10 BER ratio"`；
- `n_seeds = 30`；
- `mean_gain_db`；
- `ci95_low_db`、`ci95_high_db`，使用 df=29 的双侧 t 区间；
- `pooled_count_gain_db`，明确标 `diagnostic_only=true`；
- 聚合 raw counts。

`meta.provenance` 至少保存：生成时间、git HEAD、dirty flag、脚本 SHA256、实际 import 的 common/params 文件 SHA256、完整 seed 公式或 seed 列表、Python/NumPy/SciPy 版本、运行命令、elapsed time。最终提交前主控会再次核对这些 hash；本任务不自行 commit。

## 4. 实施与验证顺序

1. 先为 JSON schema、paired-seed mean/CI、branch-count sum 和 common-oracle inequality 写确定性检查。
2. 在现有脚本中仅增加计数、字段与 provenance；保持 DSP 调用链不变。
3. 运行快速 1-seed/1-point smoke test，确认 schema 与断言。
4. 运行 30-seed × 9 点正式任务。
5. 独立从 per-seed raw counts 重算全部 9 个 mean/CI，与 `paper_summary` 比较；绝对误差阈值 `1e-12`。
6. 检查每个 seed：`n_select_da+n_select_nda=400`，`switch_common_errors >= common_oracle_errors`。
7. 与旧 R005 方向核对：九点 CI 下界仍大于 0；若任一点不满足，不得解释原因或改参数，直接回传 FAIL。

## 5. 回传格式（强制）

```markdown
## 状态
PASS / FAIL

## 未改变项
算法、判据、参数、场景、seed/window 设计逐项证据

## 权威统计契约
公式、JSON 字段、paired/pooled 区分

## 九点结果
scene | SNR | mean_gain_db | CI95 | pooled diagnostic | center difference

## 自检
schema、branch counts、common oracle、hash/provenance、旧结果稳定性

## 文件与 hash
脚本/JSON/common/params 的路径与 SHA256

## 下游许可
READY_FOR_FIGURE_AND_TEXT 或 BLOCKED，并说明唯一原因
```

## 6. 验收

- [ ] 九点 point estimate 与 CI 使用同一 paired-seed estimand。
- [ ] 每 seed raw counts、branch counts、common oracle 已持久化。
- [ ] common oracle 只比较同一 768-bit population。
- [ ] provenance 足以把 JSON 绑定到当前源码和参数。
- [ ] 未修改算法、论文、图或治理文件。
- [ ] 未提交 git。

