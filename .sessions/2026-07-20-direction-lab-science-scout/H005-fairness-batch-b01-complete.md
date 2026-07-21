# Handoff: B01 完成 + 条件授权 B02 ML detector batch

> 来源: S005 / D008 | 交接目标: 在 clean context 中运行 B02 ML detector batch（narrowed claim）
> 日期: 2026-07-21
> 文件名: H005-fairness-batch-b01-complete.md

## 已完成边界

S005 在一个连续对话内完成 H004 的三个宏阶段：

**A. Portfolio v3 扩图**（`portfolio-refresh.v3-fairness.yaml`）
- 13 个机制级候选（C01-C13）覆盖 9 个功能簇
- 纠正 C01-C04 readiness（C03 = INFRASTRUCTURE_BLOCKED；C01/C02/C04 = NEEDS_SMALL_ADAPTER）
- 任务专属 comparator 分层（C05 检测器 / C07 控制器 / blind_affine 修正器 / anchor 均衡器）

**B. Fairness Batch B01 运行**（`fairness-batch-b01/`）
- 合同冻结、4 个候选实现、7/7 sanity PASS、43-59s 全量运行
- 11 cells × 10 paired seeds × {anchor, C05, C08, C10, C11}
- per-method tuning budget + divergence penalty + frozen-before-held-out

**C. 综合 + 收获 + 独立复核**
- synthesis: PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT
- harvest H023-H028
- 独立 verifier: CONFIRM, HIGH confidence, 20/20 PASS

## 不要做什么

- **不要** 在 B02 之前训练任何 ML 检测器（B01 仅条件授权 narrowed-claim B02）
- **不要** 把 C11 的 long-cell 小改善（0.01-0.03）写成 PI-SER 胜利（headroom 仍 ≥6×MDE）
- **不要** 把 C05 detector AUROC=1.000（在 long cells）外推到所有 cells（pooled=0.6546，short cells AUROC=0.5）
- **不要** 重新打开 H021 基础设施缺口假设（C10 per-symbol 直接测试已否定）
- **不要** 把 B01 数字写入论文正文（Scout/Sandbox，晋级需用户 strategy 决策）
- **不要** 修改 B001-B003 / P03 / CB1 raw / canonical-state（protected history）
- **不要** 创建 legacy B004
- **不要** push 或 merge

## 必读

按优先级：

1. `.sessions/2026-07-20-direction-lab-science-scout/H005-fairness-batch-b01-complete.md`（本文件）
2. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（更新后的全貌）
3. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` D008（B01 完成 + B02 授权条件）
4. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/fairness-batch-b01/artifacts/fairness-batch-b01-v1-synthesis.md`（科学结论）
5. `projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/harvest-addendum.v2-b01.yaml`（H023-H028）
6. `projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/portfolio-refresh.v3-fairness.yaml`（13 候选 + 9 簇 + readiness + comparator）
7. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/fairness-batch-b01/batch-contract.v1.yaml`（B01 合同，作为 B02 合同模板）
8. `.agents/skills/research-direction-lab/references/baseline-adjudication.md` + `batch-and-atlas.md`
9. `.agents/skills/research-direction-lab/references/evidence-and-claims.md`（claim ceiling 纪律）

## 接口变更（B01 → B02）

B01 产出可被 B02 复用的接口：

```yaml
# b01_candidates.py 公开接口（B02 可 import）
c05_threshold_detector(trace, *, z2_ratio_threshold, cusum_drift, R2=1.32) -> dict
# 返回 alerts 列表 + baseline + provenance
# B02 把它作为 task-specific comparator

c05_label_from_oracle(per_seed_oracle_pi_ser, *, collapse_threshold=0.3) -> int
# B02 用于监督训练标签（FR-14 允许 oracle-derived labels）

# B01 已建立的 frozen params（B02 应沿用而非重新 tune）：
# 在 fairness-batch-b01/artifacts/frozen-params.v1.yaml
# C05: z2_ratio_threshold=0.25, cusum_drift=0.02 (AUROC=0.6546 pooled)
# C08/C10/C11 不在 B02 范围（它们是 equalizer 变体，不是 detector）
```

B02 需要新建的接口（adapter sprint）：

```yaml
# 待实现：causal feature stacker（C01/C02/C06 共享）
stack_causal_features(trace, *, history_blocks=4) -> np.ndarray
# 输入：CMA anchor 的 trace（list of per-block dicts）
# 输出：(n_blocks, history_blocks × n_features) 的特征矩阵
# 用于 C01 监督分类器、C02 SSL 重构、C06 密度估计
```

## 失败数据附录

| 候选 | 失败模式 | 数据 |
|---|---|---|
| C10 per-symbol | 在 long cells 上略差于 anchor（H021 否定） | snr10-fg100-long: anchor=0.4273 vs C10=0.4371（+0.0098） |
| C08 bandit | short cells 上无显著改善（简单 bandit 局限） | 所有 short cells Δ ∈ [-0.001, +0.001] vs anchor |
| C05 detector | short cells 上 AUROC=0.5（信号弱） | snr=20 short cells: 0 collapse labels → AUROC undefined |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| D007 #2 convergence N | 长序列闭合 | PARTIALLY_CLOSED | B02/B03 在 long cells 上验证 |
| D007 #4 oracle recoverability | receiver-visible 信号 | PARTIALLY_CLOSED（C05 AUROC=0.65 pooled） | B02 ML detector 验证是否能突破 0.65 |
| C03 action hook | runnable 要求 | INFRASTRUCTURE_BLOCKED | 控制族进入 batch 前 |
| C12 coded evaluator | soft-output 路径 | INFRASTRUCTURE_BLOCKED | bundle 2 建设 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| B01 PROBLEM_SURVIVES | ≥6/7 held-out cells headroom ≥ MDE | batch-contract.v1.yaml decision_rule | 6/7（PASS） |
| C05 pooled AUROC ∈ [0.65, 0.85) | batch-contract.v1.yaml B02 授权条件 | 0.6546（PASS，narrowed claim） |
| 独立 verifier CONFIRM | 20/20 检查 PASS | P6 separation of concerns | 20/20（PASS） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 D008、H005、synthesis 至少 3 条关键事实
- [ ] 已检查 `_registry.yaml` 的 depends_on / conflicts_with
- [ ] 已确认 B001-B003/P03/CB1 raw 未改且 legacy B004 不存在
- [ ] 已确认当前范围未违反"明确不含"
- [ ] 已重算 C05 pooled AUROC（应 = 0.6546）
- [ ] 已重算 C11 snr10-fg100-long PI-SER（应 = 0.3984）

## 下一轮

**B02 ML detector batch**（clean-context 对话）：

1. 先做 shared adapter sprint：`causal feature stacker`（half-day，共享 by C01/C02/C06）
2. 冻结 B02 合同（模板：B01 batch-contract.v1.yaml）：
   - 候选：{C01, C02, C06}
   - task-specific comparator：C05 (AUROC=0.6546 pooled)
   - Go metric：pooled AUROC > 0.6546 AND warning lead time on long cells（where C05 already = 1.0）
   - claim ceiling：SLICE，narrowed to "ML improves lead time / calibration in short-cell ambiguous regime"
3. 若 B02 PASS → B03 learned correctors {C04, C09}（task comparator = blind affine）
4. 若 B02 FAIL → record LOCAL_NEGATIVE on ML detection，rotate 到 C13（pilot-aided，不同信息类）

**用户战略决策点**（B02 前可问）：
- 是否授权 B02？还是先停在 B01 的负面/正面收获？
- 是否切换到不同 thesis route（如 U24/RC2 cluster from v1）？
- 是否需要重大算力/时间投入（如 B02 + B03 + B04 连续跑）？

如无战略变化，按 H004 / 用户 §七"局部失败、单候选阻断或模型不工作时自动换候选；不要停下来问我"，B02 可在下一对话直接启动。
