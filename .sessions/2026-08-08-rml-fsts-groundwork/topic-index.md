# Topic Index: RML-FSTS Groundwork

> 状态: active | 创建: 2026-08-08 | 最后更新: 2026-08-09（D005/V003：Step 3 接收语义纠偏完成）

## 专题信息

- **slug**: `2026-08-08-rml-fsts-groundwork`
- **title**: RML-FSTS fixed-lag condition-dependence Groundwork
- **性质**: Ch4 reference-method extension 的独立正式 Groundwork 专题

## 范围边界

**原始目标**：验证 RML-FSTS fixed-lag condition-dependence 是否能经完整 Groundwork 成为 Ch4 方法入口。

**当前范围**：Step 1–3 已完成；本执行任务已在 Step 3 边界停止。Step 3.5 尚未开始，只有新对话按框架执行才是下一合法动作。

**明确不含**：Step 3.5、Step 4a、预注册 smoke、future action 设计/实现、仿真、MVE、Contract、Execute、METHOD_SIGNAL、Go/Kill；也不补跑新的 Step 1/2 检索或全文获取（Yu 2023 canonical path/title preflight 的字节一致适配除外）。

**范围变更记录**：

- **2026-08-09 D003**：用户接受当前 5 篇合格 CORE 后，当前范围由 Step 1–2 扩大到仅执行 Step 3。
  - 原因：D002 的用户覆盖面确认关口已满足，具备进入 `gw-read` 的最低全文输入。
  - 新范围：精读冻结的 5 篇 CORE，完成 Step 3 全部结构化产出后停止；禁止 Step 3.5+。
  - 影响的未决项：覆盖面确认项关闭；新增 T001 执行与 Step 3 完成/阻塞判定。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. source defect 与 target FSO defect 分离：Wang 2023 只支持 fixed lag/`BL` 对 modulation、training length、received power 的依赖及低功率 timing/FOE 退化；星地 lag-ranking crossover 仍为待证伪假设。
2. 最强廉价替代必须保留为 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup；不得只与论文 fixed `BL` 或 global lag 比较。
3. exact historical collision 边界保持：不复活 K01/B10/B3-Q2/C3/P09/P1/oversampled-Q1，不并行启动 BUM-CMA。
4. 当前 research-object failure / method-bearing package failure 计数保持 `0/0`；Step 1/2 门控失败不改变计数。

### 其他结论

1. RML-FSTS 当前只是 research object，不是 Q#、Go、METHOD_SIGNAL、方法或章节贡献。
2. `receiver-visible reliability-weighted multi-lag circular fusion` 仅是未来可能形态背景，本专题 Step 1–3 不设计、不实现、不验证、不宣称新颖。
3. 用户已接受当前 5 篇 CORE 作为 Step 3 输入边界；该确认不改变 C1/C2 的 Wang 谱系偏斜、C3 仅作 prior-art ceiling、C4 仅作 transfer physics 的证据限制。

## 进展线索

- **S001 / D001**：H003 接收验证通过后创建独立专题，冻结 Step 1–2 范围与证据语义。
- **R001**：7/7 query、canonical ledger 可复算 131→121 unique、4 actual sources、71/121 正式发表、12 篇 shortlist；Step 1 PASS。
- **R002 / D002**：5 篇合格 CORE 覆盖 C1–C4；Step 2 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`，不授权 Step 3。
- **V001**：独立终验初审唯一 P1 经 canonical ledger 最小补证后闭合；12 项回归 PASS，P0/P1/P2=`0/0/0`。
- **H001**：只交接覆盖面状态与用户确认动作。
- **S002 / D003 / T001**：用户确认覆盖面后完成 scope change；Step 3 精读当前 5 篇 CORE 的自包含任务已派发就绪，继续禁止 Step 3.5+。
- **R003 / D004 / V002 / H002**：5/5全文与结构化提取完成；canonical Q1 四判据4/4；Step 3=`✅ completed`，独立验证 PASS 后在边界停止。
- **D005 / V003 / H003**：主控接收时修正 Q1 的 A 逻辑方向与 Wang venue 过度措辞；Step 3 completed 保留，Step 3.5 继续未授权。

## 未决项

- mandatory Step 3.5 能否补齐直接竞品债务并完成 novelty/competition closure？（本轮未执行）

## 当前位置

Groundwork Step 3=`✅ completed`（当前 authority=D005/V003/H003）；Step 3.5=`⬜ NOT_STARTED`。本轮未进入 Step 3.5/4a，未运行 smoke、实现或仿真，object/package failure=`0/0`。下一合法动作仅为用户确认后在新对话执行 mandatory Step 3.5。
