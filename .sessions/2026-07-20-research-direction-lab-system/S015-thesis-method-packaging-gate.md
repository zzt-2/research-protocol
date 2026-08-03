# [S015] 论文方法包装门纠偏

> 2026-08-03 | Skill 最小修订 | V015 PASS，待派发 T002/T003

## 目标

记录长程运行“科学纠错有效、方法包装失效”的根因，并以 RED→GREEN 方式给 Research Direction Lab 增加最小的论文方法章保留门；随后派出 2A/2B 两个只读包装任务。

## 记录

长程审计与手工 CCISP 对照给出一致结论：现有 Skill 擅长判断结论能否相信，却把方法生产主要绑定到 `METHOD_SIGNAL → active carrier → formal promotion`。因此，未达到论文科学主方法门的 estimator、校准链、条件分支、单分支计算图和字长设计，常在形成方法章之前就被降为 supporting material。

这不是取消科学门。artifact、privileged truth、执行无效、伪造授权和错误成本记账仍不得贡献正向数字。需要修的是另一层：对语义有效的中粒度技术内核，在 formal science disposition 之外单独做章节能力判定，允许诚实进入 `NEEDS_ONE_BOUNDED_PACKAGE`，而不是等待 `METHOD_SIGNAL` 后才谈包装。

本轮采用双门设计：

1. 科学主方法门继续决定 `METHOD_SIGNAL`、active carrier 与 formal promotion；
2. 论文方法章门检查可命名方法、M-C-A、deployable input→action→output、充分传统 comparator、算法步骤/框图、消融、主结果图和 claim ceiling。

论文方法章门只产生 `THESIS_METHOD_READY`、`NEEDS_ONE_BOUNDED_PACKAGE`、`SUPPORTING_ONLY`、`REJECT` 四种状态。它不自动创建 active carrier，也不把 invalidated evidence 升级。当前 RED 对象为 2A 校准鲁棒 CPR 与 2B 单分支低复杂度/定点 CPR；G1/P09 等 invalidated 反例必须继续拒绝。

## 决策引用

- D021：增加独立的论文方法章保留门，并用 2A/2B 与 invalidated 反例做 RED→GREEN 回归（新建）

## 范围确认

- 本轮是否在 scope boundary 内：否；用户已明确授权，见 D021 与 topic-index scope change。

## 后续

R005 已完成可审计 RED→GREEN：修改前结构测试因缺少独立 chapter-capability checkpoint 而 RED；补四状态、action-lineage 分拆与 bounded-closure 优先路由后，2/2 保留原文的 blind fresh-context 样本 GREEN。未留 raw 的探索性样本不承担数量结论。V015 独立终验 PASS（P0/P1/P2=0）。T002/T003 已绑定 control epoch 10；统一提交后创建两个隔离任务。两任务只诊断 2A/2B 的方法包装与唯一 bounded package，不运行仿真、不写正式论文。
