# Handoff: PROMPT-011 前提被否证，转 CMA 基线合法性重审

> 来源: S012 | 交接目标: 用标准 CMA 与排列不变 BER 重审历史结论
> 日期: 2026-07-13

## 到哪了（状态）

PROMPT-011 的文献调研、假设建立和一个最小根因切片已完成。通用 DD/酉约束方案已有成熟先例；更关键的是，当前 `_cma.py` 不是标准复数 CMA，且旧 BER 没有消除偏振排列。3 shared seeds 中旧实现固定标签 BER 约 0.474，但排列消歧后约 0.031，3/3 是 X/Y swap；因此“漂入连续酉多解导致断链、需要新代价函数”的前提被否证（D016/V001）。

## 下一步干什么

先读 S012、D016、V001 和 `PROMPT_011_REPORT.md`。在新对话中把根因诊断扩至 ≥10 shared seeds，并建立三种口径：当前 scalar-error 实现、标准复数 CMA、标准 CMA + 帧头/流标识重标。随后逐项审计 S005-S011 中依赖旧 CMA 和固定标签 BER 的结论，输出“仍成立/需重跑/被否证”矩阵。

## 纪律（续接者必须注意的）

- 不实现 DD/正交约束新方法，直到标准 CMA 基线和标签口径合法。
- 不把 X/Y swap 当信息丢失；必须同时报 fixed-label 与 permutation-aware BER。
- 3 seeds 只作阻断性根因证据，正式数字至少 10 seeds，并报 per-seed。
- 不撞 D001：不重新叙述成 SOP 跟踪带宽不足。
- 保留现有工作区改动，不修改共享 `_cma.py`，先在隔离诊断脚本完成审计。

## 失败数据附录

### “修正在线跟踪新代价函数”前提

- 核心失败机制：把盲分离的离散偏振排列误当连续酉混合/通信断开；同时基线更新式遗漏标准 CMA 输出因子。
- 具体数据：current fixed-label `0.4741±0.0201` → permutation-aware `0.0306±0.0253`；swap 3/3；same-source 0/3；diverged 0/3。
- 已排除方向：直接把 DD、酉约束、CMA-SDD 作为原创方法。
- 可复用部分：目标场景下的失锁概率、帧头重标开销、低 SNR 误判传播仍可量化。

## 接口变更

```yaml
contracts:
  - id: C001
    type: interface-change
    description: "新增 PROMPT-011 隔离诊断接口，不改共享 CMA"
    location: "projects/simulation/explore/cma-fade-divergence/prompt011_cma_root_diagnostic.py"
    change: "StandardCMAEqualizer2x2 + permutation-aware metrics + metadata result writer"
    consumed_by: "PROMPT-011 根因重审"
    verification_result: "PASS (3 tests + independent verifier)"
    verified_by: "V001"
```

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| seed 数不足 | 关键 BER ≥10 seeds | 仅 3 seeds 根因切片 | 下一轮正式重审前 |
| 历史 CMA 结论可能受污染 | baseline 公式与评估口径合法 | S005-S011 尚未逐项回查 | 任何论文写作/Contract 前 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 标准 CMA 公式 | 单块权重与解析式误差 <1e-13 | C6/原公式 | 1/1 |
| 排列识别 | synthetic normal/swap/same-source/mixed 分类正确 | verifier 合成测试 | 4/4 |
| 正式根因复核 | ≥10 shared seeds + fixed/PI BER + 2×2 corr | seed-bias 债务 | 待执行 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - [ ] `_cma.py` 更新缺输出因子 → 查源码与 ACP Eq.(2)
  - [ ] current 3/3 为 swap → 查结果 JSON trials
  - [ ] PI-BER 约 0.0306 → 从 trials 独立重算
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
