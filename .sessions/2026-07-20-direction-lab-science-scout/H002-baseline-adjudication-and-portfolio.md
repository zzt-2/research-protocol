# Handoff: 先裁决传统 baseline，同时继续 Portfolio

> 来源: S002 | 交接目标: 恢复正式 SCIENCE_SCOUT，完成轻量 baseline adjudication shared batch，并并行准备其他机制候选
> 日期: 2026-07-20

---

## 到哪了（状态）

CB1 closure、16QAM Atlas 和历史 artifacts 保持有效，但科学结论已由 D005 收回为 `DIAGNOSTIC/SLICE`。旧 H001 的“直接运行 ML Scout”已被取代：当前单模 CMA 可能对 16QAM 任务失配，且 `N=512/8192` 可能欠收敛。主 Skill 新增务实 baseline 充分性规则；baseline 不必是当前 SOTA，只需正确、任务适配、广泛采用、公平并足以支撑有限主张。

## 下一步干什么

先读 D005、S002 续接段和 `references/baseline-adjudication.md`。为 CB1 冻结一个共享 baseline 裁决合同：保留当前 CMA 诊断锚，选择一个来源闭环且广泛采用的 16QAM 传统主 comparator，处置公平收敛和信息一致性；只有一个直接相关的廉价传统扩展确能排除当前失效解释时才加入。与此同时从完整 Portfolio 准备 2–4 个机制不同、可复用同一地基的候选卡。只有达到 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 才运行 bounded ML Scout。

## 纪律（续接者必须注意的）

- 不追默认 SOTA，不穷举所有传统变体；有限主张有充分 comparator 后即停止 baseline 扩张。
- oracle affine 仍只作 bound/Kill；不能当 Go comparator，也不能把 0.333 写成 ML gain。
- 不修改 B001–B003、P03 Atlas、CB1 raw artifacts 或 canonical history；不创建 legacy B004。
- 新公式、参数和 baseline 实现先完成来源、身份、数值与收敛验证；仿真前使用 `sim-preflight`。
- 单点裁决不阻断 Portfolio；存在合法候选或共享准备工作时自动继续，不逐步请求用户。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 单模 CMA 可能不是 16QAM 充分 comparator | Go 对手必须任务适配 | `DIAGNOSTIC` | ML Scout 前必须完成主传统 comparator 裁决 |
| `N=512/8192` 可能欠收敛 | 比较器配置公平 | 未处置 | baseline shared batch 必须含收敛证据 |
| `_cma.py` 身份与 docstring 不一致 | baseline identity 唯一 | OPEN_ACKNOWLEDGED | 复用该实现或正式晋级前修复 |

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：D005 已取代 D004 的直接 ML 授权 → [PASS/FAIL + decisions.md]
  - 声称2：H001 已标 superseded → [PASS/FAIL + H001]
  - 声称3：主 Skill 已路由 `baseline-adjudication.md` → [PASS/FAIL + SKILL.md]
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

