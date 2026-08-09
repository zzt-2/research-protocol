# [R002] RML-FSTS Step 2 获取与覆盖面

> 2026-08-08 | 关联：2026-08-08-rml-fsts-groundwork / D002

## 调研问题

Step 1 shortlist 能否形成至少 5 篇合格 CORE 全文，并覆盖 C1 source、C2 2019+ task-matched comparator、C3 multi-lag/stepwise prior art、C4 coherent-FSO transfer 四类门？

## 发现

- 12 篇 shortlist 均为正式发表身份；5 篇经 fresh-context agent 完整读取并通过 identity/provenance/正文/有效行数门：Wang 2023、Enhanced 2024、Morelli 2009、Paillier 2020、Yu 2023。
- 四类覆盖分别为 C1=1、C2=2、C3=2、C4=3（论文可跨类）。
- Tang 2022 与 WiSEE 2024 有正文但 metadata/provenance 自相矛盾，不计入五篇；另 5 篇在 OA/正式稿/IEEE 专用止损链后仍缺失。
- Morelli 2009 是本轮唯一新增合格全文；其 Unpaywall PDF 与题名校验闭合。其余合格全文来自只读共享库。
- 全文只支持 source defect、task-matched comparator、multi-stage/multi-correlation prior art 与 FSO transfer physics；不支持目标 lag-ranking crossover、conditioned-single-lag failure 或 novelty closure。

## 结论

`STEP2_READY_FOR_USER_CONFIRMATION`。5 篇合格 CORE 且四类齐全；覆盖面报告后硬停止，等待用户确认，Step 3 仍为 `NOT_STARTED`。

## 对决策的影响

新建 D002 记录 Step 1 PASS 与 Step 2 READY terminal；不改变 source/target defect 分离、不改变 strongest conditioned lookup、不改变 object/package failure=`0/0`，也不授权任何 Step 3+ 或 smoke。
