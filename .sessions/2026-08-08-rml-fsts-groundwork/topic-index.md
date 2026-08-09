# Topic Index: RML-FSTS Groundwork

> 状态: active | 创建: 2026-08-08 | 最后更新: 2026-08-08（Step 2 READY，等待用户覆盖面确认）

## 专题信息

- **slug**: `2026-08-08-rml-fsts-groundwork`
- **title**: RML-FSTS fixed-lag condition-dependence Groundwork
- **性质**: Ch4 reference-method extension 的独立正式 Groundwork 专题

## 范围边界

**原始目标**：验证 RML-FSTS fixed-lag condition-dependence 是否能经完整 Groundwork 成为 Ch4 方法入口。

**当前范围**：仅执行正式 Groundwork Step 1 检索与初筛、Step 2 全文获取与覆盖面缺口报告；在用户覆盖面确认关口硬停止。

**明确不含**：Step 3、Step 3.5、Step 4a、Q# 裁决、预注册 smoke、future action 设计/实现、仿真、MVE、Contract、Execute、METHOD_SIGNAL、Go/Kill。

**范围变更记录**：无。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. source defect 与 target FSO defect 分离：Wang 2023 只支持 fixed lag/`BL` 对 modulation、training length、received power 的依赖及低功率 timing/FOE 退化；星地 lag-ranking crossover 仍为待证伪假设。
2. 最强廉价替代必须保留为 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup；不得只与论文 fixed `BL` 或 global lag 比较。
3. exact historical collision 边界保持：不复活 K01/B10/B3-Q2/C3/P09/P1/oversampled-Q1，不并行启动 BUM-CMA。
4. 当前 research-object failure / method-bearing package failure 计数保持 `0/0`；Step 1/2 门控失败不改变计数。

### 其他结论

1. RML-FSTS 当前只是 research object，不是 Q#、Go、METHOD_SIGNAL、方法或章节贡献。
2. `receiver-visible reliability-weighted multi-lag circular fusion` 仅是未来可能形态背景，本专题 Step 1–2 不设计、不实现、不验证、不宣称新颖。

## 进展线索

- **S001 / D001**：H003 接收验证通过后创建独立专题，冻结 Step 1–2 范围与证据语义。
- **R001**：7/7 query、canonical ledger 可复算 131→121 unique、4 actual sources、71/121 正式发表、12 篇 shortlist；Step 1 PASS。
- **R002 / D002**：5 篇合格 CORE 覆盖 C1–C4；Step 2 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`，不授权 Step 3。
- **V001**：独立终验初审唯一 P1 经 canonical ledger 最小补证后闭合；12 项回归 PASS，P0/P1/P2=`0/0/0`。
- **H001**：只交接覆盖面状态与用户确认动作。

## 未决项

- 用户是否确认 Step 2 覆盖面？

## 当前位置

`STEP2_READY_FOR_USER_CONFIRMATION`。已在覆盖面报告后硬停止；Step 3/3.5/4a、smoke、实现和仿真均未启动，object/package failure=`0/0`。
