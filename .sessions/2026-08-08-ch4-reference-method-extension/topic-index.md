# Topic Index: Ch4 参考方法扩展

> 状态: dormant | 创建: 2026-08-08 | 最后更新: 2026-08-08（科学执行迁入独立 RML-FSTS Groundwork 专题）

## 专题信息

- **slug**: `2026-08-08-ch4-reference-method-extension`
- **title**: Ch4 参考方法扩展
- **性质**: 学位论文 Ch4 方法章的受控方法生产专题

## 范围边界

**原始目标**：在星地相干 FSO 总伞下，为 Ch4 产出一个真实方法章；从可复现 reference baseline 出发，经 observed defect、one deployable action、fair comparator 与 bounded testbed，形成完整方法包。

**当前范围**：本专题转为 dormant 来源 owner，保留 D004/R002/H003 与 protected history；RML-FSTS 的正式 Groundwork 科学执行迁入 `.sessions/2026-08-08-rml-fsts-groundwork/`，当前只运行 Step 1–2 并在覆盖面报告后停止。Step 3/3.5/4a、预注册 smoke、实现和仿真均不授权。

**明确不含**：

- 不把 P1 shared-M0 reuse 作为 Ch4 独立方法；
- 不建设 decoder-feedback coded-chain 基础设施；
- 不反复包装 `SUPPORTING_ONLY` / `REJECT` 资产；
- 不立即全领域 pivot，仍保持星地相干 FSO 总伞；
- 不在 baseline 可复现性、observed defect、deployable action 与 comparator 入口门通过前启动实现或实验；
- 不写正式论文正文。
- 不把 entry screening 当成 method-bearing package 或 research-object failure 计数。

**范围变更记录**：

- **[2026-08-08] D003**：从“本地入口无 survivor 后立即战略决定”改为“有界扩展 reference source，选择至多一个 defect-reproduction 入口”。
  - 原因：T001 G3 在禁止实验时要求目标场景 defect 已成立，且把入口审计误算为对象包失败，造成方法构造前过早停止。
  - 新范围：允许一次有界检索/本地索引复用；入口可凭外部 defect、FSO 迁移机制与 0.5–1 天 smoke 合同准备就绪。
  - 影响的未决项：取消“是否立即换领域”的当前阻断；先执行 T002，仍不授权 smoke/GW/实现/仿真；胜者后续从 GW Step 1 开始。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. 候选必须从可复现的外部或权威 reference baseline 与可观察/可复现的具体缺陷出发，不从内部 supporting leftovers 反推方法名。
2. 每个方法包只增加一个可部署动作；廉价替代默认进入公平 comparator/实验，除非已有证据证明 exact existing-action collision，不得在概念期凭想象预杀。
3. 基础设施工作量是投资预算，不是科学否决理由；只有入口门通过的单一胜者可获 3–7 天最小 testbed 预算。
4. 每个 research object 最多执行 2 个 method-bearing package；两个机制不同对象真正完成已授权 defect smoke 或 method-bearing package 后仍无方法增量，才必须回用户做战略范围决策。entry screening 不计数。
5. `SUPPORTING_ONLY` / `REJECT` 不关闭 Ch4 方法槽位，也不允许继续消耗包装轮次。
6. 每轮恢复先回答防偏三问：
   - 当前工作是否直接产生或裁决一个方法？
   - 它是否是最小构造前不可缺的步骤？
   - 是否已触发“每对象 2 包 / 两对象失败”的停止条件？
7. defect-reproduction 入口不要求目标 FSO defect 预先成立；最低证据合同是外部已发表 defect、明确的 FSO 迁移物理机制、0.5–1 天可证伪 smoke 设计。该合同只授权进入 GW Step 1，不等于 defect 成立或方法成立。

### 其他结论

1. 旧 RDL system 专题停止继续承载科学执行与新 S###；它只作为历史、方法论和 dead-end 证据源。
2. P1 可作为 Ch5 内部数据流优化素材，但不占用本专题的 Ch4 方法对象名额。
3. R001/D002 的事实边界保留：Paillier FG-DRC exact collision 于旧 K01 REJECT，LBS-RDE 缺星地 FSO defect；D003 只取代“两个对象已失败 / 必须战略耗尽”的强度。
4. 邻近 prior art 只限制 claim，不得扩张成整族禁令；exact object/action collision（如 K01）仍可在入口期拒绝。
5. RML-FSTS 入口的 source defect 仅是 fixed lag/`BL` 对调制、训练长度和低功率条件的依赖；目标星地 lag-ranking crossover 仍为待证伪假设，不能写成已观察事实。
6. C2 BUM-CMA 的 weak-branch gradient pollution 缺 published defect 与 faithful smoke，不得并行启动或用物理推断补 E2。
7. RML-FSTS future smoke 的最强廉价替代是 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup；论文 fixed `BL` 或较弱 global lag 单独失败不能过门，conditioned lookup 若在 MDE 内解决问题则退出。

## 进展线索

- **S001 / D001**：冻结 reference-method extension 的目标、入口边界、预算与停止条件。
- **H001**：交接下一对话只做最多 3 个 research object / reference baseline 的入口选择。
- **V001**：fresh-context verifier 12/12 PASS，P0/P1/P2=0/0/0；Skill 完整回归 116 passed, 1 skipped。
- **T001**：自包含入口选择任务；最多比较 3 个机制不同对象、推荐至多 1 个，不检索、不实现、不仿真。
- **R001 / D002**：比较 Paillier AGC+DPLL 与 LBS-RDE 两个机制不同对象；前者因 exact K01 rejected-package collision 失败，后者因星地 FSO defect 未建立失败；terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`。
- **V002**：fresh-context verifier 初审发现 exact K01 复活并 REJECT；修正后复核 ACCEPT，P0/P1/P2=0/0/0，范围纪律与日志隔离通过。
- **H002**：历史交接；其“立即战略决定”current action 已由 D003 取代，候选事实附录仍有效。
- **D003**：纠正 T001 G3 与停止计数；terminal 改为 `LOCAL_ENTRY_POOL_EXHAUSTED_DEFECT_REPRODUCTION_GATE_REQUIRED`。
- **T002**：允许一次有界 candidate-source expansion，选择至多一个 `READY_FOR_GW_STEP1_DEFECT_REPRODUCTION`；预留 R002/D004/V003/H003。
- **R002 / D004**：4/4 组定向 query 后比较 RML-FSTS 与 BUM-CMA；前者 E1–E8 全过，成为唯一 GW Step 1 defect-reproduction 入口；后者因 E2/E4/E7/E8 失败不入场。entry screening 后计数仍为 `0/0`。
- **H003**：交接下一对话先重读 `stages/groundwork.md`，只从 RML-FSTS research object 的 GW Step 1 启动；禁止直接跑 smoke。
- **V003**：fresh-context verifier 初审 PARTIAL（0/1/2），修复 strongest cheap comparator、receipt 与 prior-art identity 后复核 PASS（P0/P1/P2=`0/0/0`）。
- **T003**：自包含授权独立 RML-FSTS Groundwork 专题的 Step 1 检索初筛与 Step 2 全文获取；覆盖面报告后硬停止，不进 Step 3。

## 未决项

- GW Step 1–2 能否形成 ≥5 篇合格 CORE 全文并覆盖 source defect、直接竞品/传统 baseline、FSO 迁移物理三类证据？
- 用户是否接受 Step 2 覆盖面及关键全文缺口，从而授权未来 Step 3？
- 若合法进入 Step 4a，0.5–1 天 faithful FSTS defect smoke 是否观察到预注册 lag-ranking crossover / fixed-lag regret？

## 当前位置

`DORMANT_SOURCE_OWNER`，current terminal=`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`，V003 PASS。当前科学执行 owner 为 `.sessions/2026-08-08-rml-fsts-groundwork/`；本专题不再新增科学执行内容。
