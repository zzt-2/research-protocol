# [S001] RML-FSTS Groundwork Step 1–2

> 2026-08-08 | Groundwork Step 1–2 | 完成并在用户确认门停止

## 目标

按 T003 严格完成 RML-FSTS 正式 Groundwork Step 1 检索初筛与 Step 2 全文获取/覆盖面门；在用户覆盖面确认关口停止。

## 记录

### H003 接收验证

- **PASS — D004 terminal**：`.sessions/2026-08-08-ch4-reference-method-extension/decisions.md` 的 D004 明确 terminal=`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`。
- **PASS — source/target defect 分离**：上游 `R002-reference-source-expansion.md` 明确 Wang 2023 只支持 source-domain fixed lag/`BL` 条件依赖与低功率退化；目标星地同一可见条件内 lag-ranking crossover 仍为 UNKNOWN。
- **PASS — failure 计数与 smoke 授权**：上游 R002/H003/topic-index 一致记录 object/package failure=`0/0`，且当前未授权 smoke。
- **PASS — registry 查重**：`.sessions/_registry.yaml` 在 active/dormant 条目中只有上游控制专题提及 RML-FSTS；不存在同名或同 research object 的独立 Groundwork 专题。
- **PASS — 依赖/conflict**：上游控制专题依赖 dormant 的 RDL system 与 active thesis-writing，`conflicts_with: []`；新专题按 T003 依赖上游控制专题，未发现冲突。

### Step 1 过程

完成。7/7 query group；逐条 canonical ledger 可复算 131 个合并输入移除 10 个重复后为 121 unique；4 个实际贡献源；正式发表 71/121=`58.68%`；未去重 priority 为必读/建议读/待确认/备选/排除=`9/13/16/25/60`。路线 A/B 均完成两组二轮定向检索，路线 C 形成 transfer-physics 支撑池；12 篇 Step 2 shortlist 覆盖四类 CORE。terminal=`STEP1_PASS`。

### Step 2 过程

已由 Step 1 PASS 合法启动。12 篇 shortlist 中 5 篇通过独立全文 identity/provenance/正文/≥50 有效行门，C1–C4 四类齐全；Tang/WiSEE 因 provenance 矛盾不计入，另 5 篇止损后仍缺失。terminal=`STEP2_READY_FOR_USER_CONFIRMATION`，已在 coverage report 后硬停止。

## 决策引用

- D001：冻结独立专题的 Step 1–2 范围、source/target defect 分离、strongest conditioned lookup 与 `0/0` 计数（新建）。
- D002：冻结 Step 1 PASS 与 Step 2 READY_FOR_USER_CONFIRMATION，Step 3 保持 NOT_STARTED（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

只等待用户确认当前 5 篇 CORE 覆盖面，或指定先补哪项全文/provenance；未确认前不进入 Step 3。
