# Topic Index: Ch4 参考方法扩展

> 状态: active | 创建: 2026-08-08 | 最后更新: 2026-08-08（T001：reference-method 入口选择任务已准备）

## 专题信息

- **slug**: `2026-08-08-ch4-reference-method-extension`
- **title**: Ch4 参考方法扩展
- **性质**: 学位论文 Ch4 方法章的受控方法生产专题

## 范围边界

**原始目标**：在星地相干 FSO 总伞下，为 Ch4 产出一个真实方法章；从可复现 reference baseline 出发，经 observed defect、one deployable action、fair comparator 与 bounded testbed，形成完整方法包。

**当前范围**：只进行最多 3 个 research object / reference baseline 的入口选择，选出至多 1 个可进入后续 Groundwork 的对象；本专题当前不检索、不实现、不仿真。

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

## 进展线索

- **S001 / D001**：冻结 reference-method extension 的目标、入口边界、预算与停止条件。
- **H001**：交接下一对话只做最多 3 个 research object / reference baseline 的入口选择。
- **V001**：fresh-context verifier 12/12 PASS，P0/P1/P2=0/0/0；Skill 完整回归 116 passed, 1 skipped。
- **T001**：自包含入口选择任务；最多比较 3 个机制不同对象、推荐至多 1 个，不检索、不实现、不仿真。

## 未决项

- 哪个 reference baseline 具备可复现实现、具体缺陷、单一部署动作与公平 comparator？
- 选中的对象能否在后续正式 Groundwork 中形成合法 Q#？

## 当前位置

`ENTRY_SELECTION_READY`。下一对话只比较最多 3 个 research object / reference baseline 并推荐至多 1 个；不得直接检索、实现或仿真。
