# Handoff: RML-FSTS Step 2 覆盖面停止点

> 来源: S001 | 交接目标: 只交付覆盖面状态并等待用户确认
> 文件名: H001-step2-coverage-stop.md

## 已完成边界

正式 Step 1 PASS；正式 Step 2 获得 5 篇合格 CORE 并覆盖 C1–C4，terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。coverage report、search/acquisition receipts、R001/R002/D002 已落盘。Step 3 未启动。

## 不要做什么

不得把 READY 视为 Step 3 授权；不得运行 Step 3/3.5/4a、Q# 裁决、smoke、实现、仿真、MVE、Contract 或 Execute；不得把 source fixed-lag condition-dependence 偷换为 target coherent-FSO lag-ranking crossover；不得削弱 dev-frozen conditioned single-lag lookup comparator。

## 必读

1. `.sessions/2026-08-08-rml-fsts-groundwork/topic-index.md`
2. `projects/thesis-fso/rml-fsts-groundwork/step2-coverage-report.md`
3. `search-archive/2026-08-08/rml-fsts-step2-acquisition-receipt.json`
4. `search-archive/2026-08-08/rml-fsts-step1-canonical-ledger.json`
5. `.sessions/2026-08-08-rml-fsts-groundwork/decisions.md` D002

## 接口变更（如有代码改动）

无。

## 失败数据附录（如涉及路线失败）

5 篇全文在止损链后仍缺失；Tang 2022 与 WiSEE 2024 因 metadata/provenance 矛盾不计 CORE。详见 coverage report。此为覆盖缺口，不是 research-object 或 method-bearing package failure。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 5 篇 shortlist 全文缺失 | Step 2 应显式暴露通道偏差 | 已列人工补件动作，不影响最低四类覆盖 | 用户要求补齐后合法取得 PDF |
| Tang/WiSEE provenance 矛盾 | identity/provenance 必须同时闭合 | 不计入 5 篇 CORE | 提供一致 metadata/来源记录 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| Step 2 CORE 门 | ≥5 篇、每篇有效行≥50、C1–C4 齐全 | T003 §3.3 | 本轮 5/5；四类 4/4 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

只等待用户确认当前 5 篇 CORE 覆盖面是否可接受，或用户指定先补哪项全文/provenance。未确认前无进一步科学执行动作。
