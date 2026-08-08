# [S001] Ch4 reference-method extension 范围与执行合同

> 2026-08-08 | 立项 | 完成

## 目标

把“为 Ch4 产出一个真实方法章”的意图固化成轻量、可恢复、可停止的执行合同，避免继续在 supporting 审计、概念期预算预杀和同一小范围循环中偏航。

## 记录

经三路独立分析与交叉复核，CCISP 能成方法的关键不是先做完整治理闭包，而是已有可复现 baseline、实际性能缺陷、receiver-visible action 与成熟 testbed；近期长程流程则常在方法构造前投入过重 collision、provenance 与基础设施门控。用户接受转向 reference-method extension：仍在星地相干 FSO 总伞内，优先选择一个可复现的外部 reference baseline，先复现并观察具体缺陷，再增加一个可部署动作，并把廉价替代放进公平比较。

本专题只冻结入口合同，不选择具体科学对象。下一轮最多比较 3 个 research object / reference baseline，选出至多 1 个正式入口。单一胜者可获 3–7 天最小 testbed 预算；每个对象最多 2 个 method-bearing package，两个机制不同对象均无方法增量时必须回用户做战略范围决策。

## 决策引用

- D001：冻结 Ch4 reference-method extension 执行合同（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（新专题立项，未进入科学执行）。

## 后续

下一对话按 H001 恢复，只做入口选择；不直接检索、实现或仿真。
