# Topic Index: Ch4 参考方法扩展

> 状态: active | 创建: 2026-08-08 | 最后更新: 2026-08-08（R001/D002/V002：无 survivor 终态独立验收通过，等待战略决定）

## 专题信息

- **slug**: `2026-08-08-ch4-reference-method-extension`
- **title**: Ch4 参考方法扩展
- **性质**: 学位论文 Ch4 方法章的受控方法生产专题

## 范围边界

**原始目标**：在星地相干 FSO 总伞下，为 Ch4 产出一个真实方法章；从可复现 reference baseline 出发，经 observed defect、one deployable action、fair comparator 与 bounded testbed，形成完整方法包。

**当前范围**：入口选择已收口，terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`。本专题等待用户决定是否改变 reference-object 来源或显式重开旧 rejected object；决定前不检索、不实现、不仿真、不进入 Groundwork。

**明确不含**：

- 不把 P1 shared-M0 reuse 作为 Ch4 独立方法；
- 不建设 decoder-feedback coded-chain 基础设施；
- 不反复包装 `SUPPORTING_ONLY` / `REJECT` 资产；
- 不立即全领域 pivot，仍保持星地相干 FSO 总伞；
- 不在 baseline 可复现性、observed defect、deployable action 与 comparator 入口门通过前启动实现或实验；
- 不写正式论文正文。

**范围变更记录**：

- 无。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. 候选必须从可复现的外部或权威 reference baseline 与可观察/可复现的具体缺陷出发，不从内部 supporting leftovers 反推方法名。
2. 每个方法包只增加一个可部署动作；廉价替代默认进入公平 comparator/实验，除非已有证据证明 exact existing-action collision，不得在概念期凭想象预杀。
3. 基础设施工作量是投资预算，不是科学否决理由；只有入口门通过的单一胜者可获 3–7 天最小 testbed 预算。
4. 每个 research object 最多执行 2 个 method-bearing package；两个机制不同对象均无方法增量后，必须回用户做战略范围决策。
5. `SUPPORTING_ONLY` / `REJECT` 不关闭 Ch4 方法槽位，也不允许继续消耗包装轮次。
6. 每轮恢复先回答防偏三问：
   - 当前工作是否直接产生或裁决一个方法？
   - 它是否是最小构造前不可缺的步骤？
   - 是否已触发“每对象 2 包 / 两对象失败”的停止条件？

### 其他结论

1. 旧 RDL system 专题停止继续承载科学执行与新 S###；它只作为历史、方法论和 dead-end 证据源。
2. P1 可作为 Ch5 内部数据流优化素材，但不占用本专题的 Ch4 方法对象名额。
3. D002 裁决本地入口无 survivor：Paillier FG-DRC exact collision 于旧 K01 REJECT，LBS-RDE 缺星地 FSO defect；Ch4 方法槽位仍未关闭。

## 进展线索

- **S001 / D001**：冻结 reference-method extension 的目标、入口边界、预算与停止条件。
- **H001**：交接下一对话只做最多 3 个 research object / reference baseline 的入口选择。
- **V001**：fresh-context verifier 12/12 PASS，P0/P1/P2=0/0/0；Skill 完整回归 116 passed, 1 skipped。
- **T001**：自包含入口选择任务；最多比较 3 个机制不同对象、推荐至多 1 个，不检索、不实现、不仿真。
- **R001 / D002**：比较 Paillier AGC+DPLL 与 LBS-RDE 两个机制不同对象；前者因 exact K01 rejected-package collision 失败，后者因星地 FSO defect 未建立失败；terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`。
- **V002**：fresh-context verifier 初审发现 exact K01 复活并 REJECT；修正后复核 ACCEPT，P0/P1/P2=0/0/0，范围纪律与日志隔离通过。
- **H002**：交回用户作战略范围决定；没有决定前不得进入 Groundwork。

## 未决项

- 是否改变 reference-object 来源，寻找未被旧 D027 覆盖的新对象？
- 是否有新证据与显式 scope/decision change 足以授权重开旧 K01？

## 当前位置

`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`。本对话停止；不得补候选、继续包装、检索、实现、仿真或进入 Groundwork，等待用户战略决定。
