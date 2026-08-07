# 2A region-calibration authority reconciliation

> 2026-08-07 | authority: D037 / CP020 / T009 | terminal: `SUPPORTING_ONLY`

## 授权与执行边界

本次 scope change 的授权是转述授权：主控先提出完整受限解冻方案，用户随后回复“行”。该回复只批准
一次 P01/P02/T004 authority reconciliation；它不是主控方案的逐字复述，也不授权重开 T004、修改 CCISP
或运行无条件新实验。D037、CP020、epoch 33 与 T009 构成执行控制链，task-control guard 为 PASS。

## 三对象分账

| 对象 | 实际输入与动作 | 证据裁决 | authority |
|---|---|---|---|
| P01 receiver-visible pilot-SNR adapter | 当前窗接收样本与已知导频 → 估计工作点 → 原 CCISP selector 的 DA/NDA 命令 | 历史 5 个 harm cells 恢复 4 个；是局部 receiver-visible robustness adapter | 保留为 supporting adapter；不与 P02/T004 合并 |
| P02 weak/low-SNR retune | truth-defined `weak@{5,7,9}` 只用于选择评估切片；`decide_adapter_weakretune(...)` 无 region 参数；所有 cell 使用同一 dev-frozen `ref_snr_db=11` | 不是真正 region rule，而是一个全局单标量 retune；虽使 207/210 cell-seed 聚合 branch occupancy 改变，仍未产生至少二区不同动作 | conventional tuning/design rule，不能进入 Ch4 方法包装 |
| T004 online estimated-SNR map | current-pilot estimate → 三区域 frozen map → 原 CCISP selector | dev 中 M `+0.26750 dB`，低于 nominal-region B2 `+0.30846 dB` 共 `0.04096 dB`；immutable pre-test gate 在一次修复后仍 FAIL | `REJECT` 保持；不存在合法 held-out 正结果，也不是科学 null |

P02 的局部数字不证明 T004 成立；T004 的 evidence-control 失败也不否定 P01/P02 的历史局部事实。

## 方法语义门

| 门 | 结果 | caller/raw 事实 |
|---|---|---|
| 部署时区域已知或 receiver-visible | FAIL | P02 runtime decide 无 region 输入；weak/true-SNR 只定义评估切片 |
| test truth、真实标签、真实 SNR 不进入 decide | PASS | P02 decide 使用 raw、known pilots 与冻结标量 |
| 可复用 observation→rule/table→CCISP action 链，而非孤立标量 | FAIL | 实现只有全局 `ref_snr_db=11` |
| 至少二区产生不同合法动作 | FAIL | distinct calibration actions=`1` |
| original 与 global 公平 comparator | FAIL | P02 未冻结 global-vs-region calibration ladder |
| 名称、步骤、消融、主图和边界可闭合 | FAIL | shuffled-region/global-mean 消融对单标量无定义 |

因此在 sim-preflight 之前停止；没有运行新 held-out，也没有临时发明 classifier。

## 确定性复算

- P01 chronology：dev seeds `0–9`，held-out `30–49`，互斥。adapter 严格恢复 4/5；`weak@9, -3 dB`
  残留 `-0.32285 dB`，seed-cluster 95% CI `[-0.35679,-0.28891]`。在 15 个 nominal-safety cells
  中，`weak@9` 同样是唯一达到冻结 `-0.3 dB` material-degradation 门的 cell（1/15）；其余 14/15
  未达该门。历史 preprocessing 含 truth-assisted 诊断环节，故不扩大成端到端 deployable claim。
- P02 chronology：dev seeds `50–59`；held-out `60–70 ∪ 81–99`，与 dev 互斥。首批 20 seeds 的结果
  被观察后才追加 `90–99`，所以不是 pristine one-shot 30-seed confirmation。
- P02 `weakretune-adapter=+0.45387 dB`；seed-cluster 95% CI `[+0.43404,+0.47370]`。历史报告按
  90 个 cell-seed pairs 展平的 CI 为 `[+0.43330,+0.47444]`。
- P02 `cand_rank-weakretune=-0.09609 dB`；seed-cluster 95% CI `[-0.10275,-0.08942]`；历史展平 CI
  `[-0.10597,-0.08620]`。四个 boundary cells 的 retune-adapter 均值为 `+0.10888` 至 `+0.17024 dB`，
  未见 catastrophic cell；这只支持冻结切片内的 tuning boundary。
- T004 original/global/nominal-region/online 表全部是 dev-only、6 seed clusters；没有 chronology/raw/summary
  held-out artifacts。

可复跑入口：`python projects/simulation/results/2a_region_calibration_authority_reconciliation/recompute_existing_evidence.py`。

## Claim ceiling 与终态

允许保留：P01 是 receiver-visible 局部 robustness adapter；P02 说明在冻结 weak/low-SNR 诊断切片上，
常规全局 `ref=11` retune 吸收 cand_rank。不得称“工作点失配下的 region-calibrated robust CCISP
extension”已经成立，不得称 online calibration、第二主算法、新 selector、CPR estimator 或通用自适应阈值理论。

唯一 terminal：`SUPPORTING_ONLY`。
