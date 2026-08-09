# Topic Index: RML-FSTS Groundwork

> 状态: dormant | 创建: 2026-08-08 | 最后更新: 2026-08-09（D013/V008/H007：重开输入未闭合并验证收口）

## 专题信息

- **slug**: `2026-08-08-rml-fsts-groundwork`
- **title**: RML-FSTS fixed-lag condition-dependence Groundwork
- **性质**: Ch4 reference-method extension 的独立正式 Groundwork 专题

## 范围边界

**原始目标**：验证 RML-FSTS fixed-lag condition-dependence 是否能经完整 Groundwork 成为 Ch4 方法入口。

**当前范围**：Step 1–3.5 已完成；D011/V007 的既有 Step 4a scientific terminal 继续有效。D012 blocker-recovery Probe 已得到 SC1=`NOT_CLOSED`、AB1=`NOT_CLOSED`，D013/V008 verified recovery terminal=`REOPEN_INPUTS_NOT_CLOSED`。专题恢复 dormant；performance grid、diagnostic structural run、bounded MVE 与下游继续禁止。

**明确不含**：Contract、Execute、正式论文写作、无门控 controller、repair chain、首次/novelty closure 声称；不复活 K01/B10/B3-Q2/C3/P09/P1/oversampled-Q1，不修改 dormant campaign、`common/`、`params.py` 或四个既有 `p05_run*.log`，不 push。只有 D009 冻结合同内的 Step 4a smoke 与条件式 bounded MVE 获授权。

**范围变更记录**：

- **2026-08-09 D003**：用户接受当前 5 篇合格 CORE 后，当前范围由 Step 1–2 扩大到仅执行 Step 3。
  - 原因：D002 的用户覆盖面确认关口已满足，具备进入 `gw-read` 的最低全文输入。
  - 新范围：精读冻结的 5 篇 CORE，完成 Step 3 全部结构化产出后停止；禁止 Step 3.5+。
  - 影响的未决项：覆盖面确认项关闭；新增 T001 执行与 Step 3 完成/阻塞判定。
- **2026-08-09 D006**：用户明确授权将当前范围从 Step 3 扩大到 mandatory Step 3.5。
  - 原因：Step 3 已由 D005/V003/H003 验收，mandatory Step 3.5 是关闭 Q1 文献竞争边界的下一框架步骤。
  - 新范围：仅执行 Step 3.5 关键词矩阵、多源检索、核心竞品双向引用链、必要全文处理、竞争闭包、独立验证与一次统一提交；到 canonical Step 3.5 terminal 停止。
  - 影响的未决项：启动 Cheng 2020、两篇 Optica 直接竞品、Wang/Enhanced 引用链与 Tang/WiSEE provenance 债务裁决；Step 4a 继续排除。
- **2026-08-09 D009**：用户明确授权将当前范围从 Step 3.5 扩大到仅执行 Step 4a feasibility，并要求持续运行至唯一合法 terminal。
  - 原因：D008/V005/H005 已给 Q1 带全文限制的 Step 4a 入口；用户已冻结 baseline ladder、defect-smoke 门限、廉价替代优先级和 bounded MVE 条件。
  - 新范围：A0 §0–§6 → semantic smoke → 条件式 bounded MVE → fresh-context 独立验证 → Step 4a terminal；无 ranking crossover 或 B2 吸收时立即停止，不制造 controller。
  - 影响的未决项：target crossover/headroom 从 UNKNOWN 进入实证裁决；SSRN 6293357 保持高风险全文债但不是 blanket blocker。
- **2026-08-09 D012**：用户以“你做吧”显式授权执行 H006 的两项唯一重开前置。
  - 原因：D011/V007 已证明性能执行在任何 scientific row 前被 source/config 与 action-before 两类输入阻断；用户授权主控自行推进这些输入，不要求逐项停下确认。
  - 新范围：只做公开/一手 source-config 获取、action-before causal protocol 设计、证据整合与 fresh-context 独立验证；两项均闭合且验证通过后才可恢复 D009 semantic-smoke 合同重冻结。
  - 影响的未决项：D011 terminal 在恢复 Probe 期间仍有效；若任一输入未闭合，则回到 dormant 并保持 terminal 5，不运行 performance grid/MVE。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. source defect 与 target FSO defect 分离：Wang 2023 只支持 fixed lag/`BL` 对 modulation、training length、received power 的依赖及低功率 timing/FOE 退化；星地 lag-ranking crossover 仍为待证伪假设。
2. 最强廉价替代必须保留为 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup；不得只与论文 fixed `BL` 或 global lag 比较。
3. exact historical collision 边界保持：不复活 K01/B10/B3-Q2/C3/P09/P1/oversampled-Q1，不并行启动 BUM-CMA。
4. 当前 research-object failure / method-bearing package failure 计数保持 `0/0`；Step 1/2 门控失败不改变计数。
5. SSRN 6293357 高风险全文债继续保留；Step 4a testbed blocker 不构成 novelty closure，也不消除 strongest cheap comparator。

### 其他结论

1. RML-FSTS 当前只是 research object，不是 Q#、Go、METHOD_SIGNAL、方法或章节贡献。
2. `receiver-visible reliability-weighted multi-lag circular fusion` 仅是未来可能形态背景，本专题 Step 1–3 不设计、不实现、不验证、不宣称新颖。
3. 用户已接受当前 5 篇 CORE 作为 Step 3 输入边界；该确认不改变 C1/C2 的 Wang 谱系偏斜、C3 仅作 prior-art ceiling、C4 仅作 transfer physics 的证据限制。
4. D011/V007 已确认唯一 terminal 5：Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`；B0/B1/B2/O1/C1 数字均为 `N/A (NOT_RUN)`。
5. D012 只是重开输入恢复授权，不取代 D011 scientific terminal，也不把 public-source search 或协议设计计为 method progress。
6. D013/V008 确认公开 source-config 1–7 字段 exact-closed=`0/7`，previous-frame/common-probe 均无 executable caller path；这不是 no-crossover 或 B2-resolved 证据。

## 进展线索

- **S001 / D001**：H003 接收验证通过后创建独立专题，冻结 Step 1–2 范围与证据语义。
- **R001**：7/7 query、canonical ledger 可复算 131→121 unique、4 actual sources、71/121 正式发表、12 篇 shortlist；Step 1 PASS。
- **R002 / D002**：5 篇合格 CORE 覆盖 C1–C4；Step 2 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`，不授权 Step 3。
- **V001**：独立终验初审唯一 P1 经 canonical ledger 最小补证后闭合；12 项回归 PASS，P0/P1/P2=`0/0/0`。
- **H001**：只交接覆盖面状态与用户确认动作。
- **S002 / D003 / T001**：用户确认覆盖面后完成 scope change；Step 3 精读当前 5 篇 CORE 的自包含任务已派发就绪，继续禁止 Step 3.5+。
- **R003 / D004 / V002 / H002**：5/5全文与结构化提取完成；canonical Q1 四判据4/4；Step 3=`✅ completed`，独立验证 PASS 后在边界停止。
- **D005 / V003 / H003**：主控接收时修正 Q1 的 A 逻辑方向与 Wang venue 过度措辞；Step 3 completed 保留，Step 3.5 继续未授权。
- **S003 / R004 / D006-D007 / T002-T010 / V004 / H004**：完成 scope change、仓库盘点、8-query R1、三类真实来源、Wang/Enhanced 双向引用链、R2/R3 止损与新增全文处理；Step 3.5 因 8 项关键全文不可得终止为证据阻塞，独立终验 10/10 PASS，未开放 Step 4a。
- **D008 / V005 / H005**：主控接收发现 130981 共享全文漏查和 blanket blocker 过严；保留检索事实，撤回 D007 terminal。Q1 改为 provisional survivor with fulltext limitations，开放后续 Step 4a 讨论入口。
- **S004 / D009**：接收 H005 的 4 项关键事实并完成 scope change；冻结 Step 4a 连续执行边界、baseline ladder、门限和唯一终态集，A0/testbed readiness 审计启动。
- **D010 / V006 / T015–T019 / D011 / V007 / H006**：D010 在 pre-run 独立审查中 rejected；source calibration 与 physical transfer 确认 structural causality、source-channel non-equivalence、power/noise non-identifiability 三类 hard blocker，B0 numeric gate 不可执行。Fig. 403 仅为 recoverable gap。未运行 performance grid/MVE；fresh-context V007 以 P0/P1/P2=`0/0/0` 接收唯一 terminal 5。
- **S005 / D012**：新上下文独立接收 H006 三项事实与 protected-log hash；只重开 source-config/action-before 两项输入恢复，冻结 PASS/stop 边界和不越过 grid/MVE 的范围。
- **T020–T022 / D013 / V008 / H007**：三类 public source surface 未发现 exact executable artifact；SC1=`NOT_CLOSED`。两种 action-before 方案均缺 measurement/time-series/feedback/freshness/cost closure；AB1=`NOT_CLOSED`。fresh verifier 以 P0/P1/P2=`0/0/0` 接收 `REOPEN_INPUTS_NOT_CLOSED`，D011 terminal 5保持，专题 dormant。

## 未决项

- 科学重开输入：authors/source receiver+channel configuration，以及可执行 feedback/time-series testbed；本次公开恢复未闭合，若需联系作者须新增外部沟通授权。
- 高风险全文债：SSRN 6293357；次级 comparator 债：ACP/IPOC 10809664。Cheng、OE.561252、OE.505931、OE.448956、Dong 作为非阻断边界债保留；130981 已由共享全文关闭。

## 当前位置

Groundwork Step 3=`✅ completed`；Step 3.5=`✅ COMPLETE / Q1 PROVISIONAL SURVIVOR WITH FULLTEXT LIMITATIONS`（authority=D008/V005/H005）。Exact collision/conditioned-lookup equivalent 均为 0 confirmed；不允许首次/novelty closure 措辞。Step 4a scientific state 仍为 `🛑 INCONCLUSIVE / VERIFIED`：terminal=`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`（D011/V007/H006），semantic-smoke performance grid/MVE 均 `NOT_RUN`，object/package failure=`0/0`。D013/V008 recovery terminal=`REOPEN_INPUTS_NOT_CLOSED`；专题 dormant，Contract/Execute/论文写作继续禁止。
