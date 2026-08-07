# Handoff: Q1 Step 4a semantic smoke Kill/Pivot

> 来源: S003 | 交接目标: 保存 Q1 negative-evidence terminal，并阻止自动进入正式 MVE/testbed
> 文件名: H005-step4a-semantic-smoke-kill-pivot.md

## 已完成边界

- D010/H004 的 ≤1 天 deterministic semantic smoke 已由 T015 执行；T016 full re-verification PASS、
  blocker=`0`，V008 已登记。
- 四项 semantic gates PASS；180 paired cells、720 method rows、180 surfaces 与 hashes 闭合。
- B1/C 在同 receiver-visible input、grid、score、window、normalization、tie-break 下 180/180 exact-equivalent；
  并非 result alias。noiseless 四法 0/75；-6 dB diagnostic B0/B2=58/75、B1/C=59/75；无稳定 2×2。
- D012 正式 terminal=`STEP4A_PREFLIGHT_KILL_OR_PIVOT`；formal topic closed。

## 不要做什么

- 不建 5.5–7.5 日 testbed，不跑正式 MVE，不进入 Step 5、Contract 或 Execute。
- 不通过换 preamble、扩 seed、降低 SNR 或加密 grid 追逐正结果。
- 不把 surface 非可分、B1/C 有限网格等价或 deterministic false-lock frequency 外推为方法收益、连续
  estimator 等价、外场概率或论文数字。
- 不把工程加速组件直接包装成 Q1 的独立方法；complexity pivot 必须新建 M-C-A 并重走前置门。
- 不修改 `projects/simulation/common/`、`params.py`、旧实验、Skill 或四个 `p05_run*.log`；不 push。

## 必读

1. `.sessions/2026-08-06-oversampled-coherent-sync-groundwork/decisions.md` D012
2. `.sessions/2026-08-06-oversampled-coherent-sync-groundwork/verifications.md` V008
3. `projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-report.md`
4. `projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-independent-verifier-report.md`
5. `projects/simulation/explore/oversampled-coherent-sync-q1/artifacts/terminal.json`

## 接口变更（如有代码改动）

```yaml
probe_only:
  root: projects/simulation/explore/oversampled-coherent-sync-q1
  receiver_visible: rx_samples + known_preamble + frozen_config + hypothesis_grid
  truth_scoring: separate TruthMetadata
  outputs: manifest/observations/truth/method_results/surfaces/summary/terminal/provenance
production_interface_change: none
common_or_params_change: none
```

## 失败数据附录（如涉及路线失败）

| Layer | B0 | B1 | B2 | C | C vs B0 | stable B0 2×2 |
|---|---:|---:|---:|---:|---:|---:|
| noiseless residual | 0/75 | 0/75 | 0/75 | 0/75 | 0% | 0 |
| -6 dB diagnostic residual | 58/75 | 59/75 | 58/75 | 59/75 | -1.7241% | 0 |
| noiseless stress（隔离） | 0/30 | 0/30 | 0/30 | 0/30 | 不进 reducer | N/A |

B1/C common-grid equivalence=`180/180`。这些是 frozen diagnostic grid 的 exhaustive frequencies，不是概率估计。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| exact literature preamble 不可得 | FR-20 参数溯源 | fixed-seed diagnostic sentinel | 仅当新问题合法重开且用户提供/允许获取 exact sequence |
| JOCN 2026 全文不可得 | novelty claim ceiling | 保留限制 | exact novelty claim 前 acquire→read；不影响本 Kill |
| continuous estimator 未比较 | claim boundary | 本结论只覆盖 frozen grid | 新的连续估计 M-C-A 通过 Step 1–4a 后另立合同 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| semantic gates | identity/paired/truth/score 全 PASS | D010/T015 | 4/4 PASS |
| cheap coverage Kill | B1/B2 coverage ≥95% 或 B1/C exact-equivalent | D010 | B1/C 180/180 exact-equivalent |
| practical gain | C vs B0 `G_C>=5%` 才保留 | D010 | 0% / -1.7241%，FAIL |
| stable wrong basin | 同 frame/layer 下同 wrong label 的相邻 2×2 | T015 | 0，FAIL |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

只等待用户选择：归档 Q1；或显式批准一个以 latency/complexity 为唯一贡献维度的新 M-C-A pivot。未获新授权，
不得继续实验、建 testbed 或进入 Step 5。
