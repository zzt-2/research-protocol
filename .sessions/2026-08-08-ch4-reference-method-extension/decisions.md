# Decisions — Ch4 参考方法扩展

## D001: 冻结 reference-method extension 方法生产合同

> status: active
> date: 2026-08-08
> 取代：无
> 被取代：无
> 依据：critic: S001 三路独立过程/包装/范围审查综合 + 用户原话: `voice.md` 2026-08-08

### 决策

Ch4 不再从内部 supporting leftovers 继续包装，也不立即全领域 pivot；改为在星地相干 FSO 总伞下，从可复现 reference baseline、observed defect、one deployable action 与 fair comparator 出发生产完整方法包。入口门通过的单一胜者可获 3–7 天最小 testbed 预算。

### 理由

CCISP 的可写性来自“真实缺陷—可部署动作—现成 testbed—公平比较”的完整链，而近期流程把大量工作消耗在方法构造前的治理、假想廉价替代与基础设施 hard kill。reference-method extension 保留科学诚信门，但把最重的检索、统计与工程闭包后移到已选中的单一对象上。

### 排除的替代方案

- 不把 P1 shared-M0 reuse 恢复为 Ch4 独立方法；已有 generic shared-compute prior art，最多作 Ch5 内部优化。
- 不建设 decoder-feedback coded-chain 基础设施；当前 extrinsic/syndrome/callback 均未就绪。
- 不继续对 `SUPPORTING_ONLY` / `REJECT` 资产做 authority/package closure。
- 不立即离开 coherent FSO；先改变同领域内的 research object。
- 不把廉价替代当概念期想象性否决，除非存在 exact existing-action collision 证据。

### 影响范围

旧 `2026-07-20-research-direction-lab-system` 专题转 dormant，不再新增 S### 或承载科学执行。新专题下一步只做最多 3 个 research object / reference baseline 的入口选择。每对象最多 2 个 method-bearing package；两个对象失败后必须回用户做战略决策。`SUPPORTING_ONLY` / `REJECT` 继续不关闭 Ch4。

### 来源

S001；用户纠正与批准；三路 subagent 发散及交叉复核。
