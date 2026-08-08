# [S001] Ch4 reference-method extension 范围与执行合同

> 2026-08-08 | 立项 | 完成
> 2026-08-08 续接 | T001 回传纠偏 | T002 待派发

## 目标

把“为 Ch4 产出一个真实方法章”的意图固化成轻量、可恢复、可停止的执行合同，避免继续在 supporting 审计、概念期预算预杀和同一小范围循环中偏航。

## 记录

经三路独立分析与交叉复核，CCISP 能成方法的关键不是先做完整治理闭包，而是已有可复现 baseline、实际性能缺陷、receiver-visible action 与成熟 testbed；近期长程流程则常在方法构造前投入过重 collision、provenance 与基础设施门控。用户接受转向 reference-method extension：仍在星地相干 FSO 总伞内，优先选择一个可复现的外部 reference baseline，先复现并观察具体缺陷，再增加一个可部署动作，并把廉价替代放进公平比较。

本专题只冻结入口合同，不选择具体科学对象。下一轮最多比较 3 个 research object / reference baseline，选出至多 1 个正式入口。单一胜者可获 3–7 天最小 testbed 预算；每个对象最多 2 个 method-bearing package，两个机制不同对象均无方法增量时必须回用户做战略范围决策。

T001 回传后，主控复核发现规则本身造成过早停止：G3 允许低成本 defect reproduction，却在同轮禁止实验并要求目标 FSO defect 已成立；同时把两个 entry-screening 候选未过门误算成“两个 research object 已失败”。R001 的事实结论保留——Paillier/K01 是 exact collision，LBS-RDE 的 FSO defect 仍未知——但战略耗尽强度由 D003 取代。

用户批准纠偏后，当前范围改为一次有界 candidate-source expansion。T002 只从外部 reference baseline 中比较 2–4 个机制不同对象，最多选 1 个进入“以 defect reproduction 为目标的 Groundwork”。入口期允许用“外部已发表 defect + FSO 迁移物理机制 + 0.5–1 天可证伪 smoke 合同”通过准备门；不在 T002 内真正运行 smoke。下一轮仍须从 GW Step 1 开始，不能把预注册 smoke 提前到 Step 3/4a 之前。

## 决策引用

- D001：冻结 Ch4 reference-method extension 执行合同（新建）。
- D002：本地入口池无直接 survivor；候选事实保留，战略耗尽强度被 D003 取代。
- D003：入口审计不计对象失败，改设 defect-reproduction gate（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（见 D003 scope change；只准备 T002，不进入科学执行）。

## 后续

下一对话执行 T002：允许一次有界检索与本地索引复用，只做 reference-source expansion 和未来 defect-smoke 合同入口选择；不实现、不仿真、不进入 Groundwork。若选中入口，再开新对话按 `stages/groundwork.md` 从 Step 1 推进。
