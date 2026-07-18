# T005 — Batch 0 基线/参数域审计

> 来源: S041 | 产出位置: `.sessions/2026-07-10-dual-pol-osl-groundwork/S042-batch0-baseline-audit.md`
> 日期: 2026-07-16

## 0. TL;DR

只做 Batch 0：验证现有 CMA-fade/SOP lock-swap 基线和指标口径，不能加入新机制，不能修改 `params.py`、`common/` 或旧结果。使用共享信道、现有脚本和 `save_results`；结果若受 CRITICAL 参数溯源债务影响，标为 provisional，不写入论文结论。

## 1. 必读

1. `D:\code\study\research-protocol\.sessions\2026-07-10-dual-pol-osl-groundwork\S041-candidate-family-map-batch-plan.md`
2. `D:\code\study\research-protocol\projects\thesis-fso\master-state.md`
3. `D:\code\study\research-protocol\.agents\skills\sim-preflight\SKILL.md`
4. `D:\code\study\research-protocol\.agents\skills\sim-preflight\scenarios\run.md`
5. `D:\code\study\research-protocol\.agents\skills\sim-preflight\rules\constraints.md`
6. `D:\code\study\research-protocol\.agents\skills\sim-preflight\rules\param-source.md`
7. `D:\code\study\research-protocol\.agents\skills\sim-preflight\rules\mve-validation.md`
8. `D:\code\study\research-protocol\projects\simulation\params.py`
9. `D:\code\study\research-protocol\毕设\CONCLUSIONS.md`
10. `D:\code\study\research-protocol\毕设\formulas-master.md`

## 2. 允许动作

- 先运行 `audit_params()`，把 summary 和涉及 GG/SOP/CMA 的参数真实值记录下来。
- 检查 `prompt015_unified_baseline.py`、`mve_cma_vs_ml.py`、`prompt030_domain_swap_audit.py` 是否仍可复现；优先 smoke/短切片，若运行时间可接受再跑注册域。
- 复现至少：standard-CMA（必须含 Godard z）、current-CMA（仅作为实现审计，不能称标准）、ML-only、CMA-only、oracle/PI 口径；所有方法必须同一信道 realization、同一 seed/条件。
- 输出 fixed-label BER、PI-BER、swap 率/首次 swap、发散概率/恢复延迟（若脚本已有），并指出指标是否逐项可比。
- 独立从原始 JSON 复核 worker 的主要归因；不要只信脚本报告。

## 3. 禁止动作

- 不改参数、不修算法、不新增候选、不跑 Batch 1。
- 不把 `common/_cma.py` current 版本写成 standard-CMA。
- 不把 PI-BER 改善写成 fixed-label 方法改善；不把 oracle/post-hoc 标签写成可部署方法。
- 不把当前 CRITICAL 参数审计债务隐藏；没有来源推导的数字只能标 provisional。

## 4. 产出格式

写 `S042-batch0-baseline-audit.md`，必须包含：

- 命令与输入脚本路径、运行时间、是否成功
- 参数审计 summary、关键参数真实值、CRITICAL/WARNING 清单
- 每个基线的原始结果路径和关键数字
- fixed/PI/swap/fade 指标口径审计
- standard/current CMA 实现差异
- Batch 0 结论：PASS（基线可横向比较）/PARTIAL（可探索但有债务）/FAIL（不能继续）
- 下一步仅给 Batch 1 是否可开始的条件，不做任何新方法判断

## 5. 验收

- [ ] 没有修改 `params.py`、`common/`、旧结果
- [ ] 共享信道与 paired seeds 得到证据
- [ ] standard-CMA z 因子实现路径核对
- [ ] 关键数字从原始 JSON 复核
- [ ] S042 明确 provisional 与正式证据的边界
