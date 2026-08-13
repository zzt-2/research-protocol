# Task Brief: P06 具体方法只读审计

> 来源: S023 | 产出位置: 回传主线程，不写文件 | 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读证据

## 0. TL;DR

只读审计 `Cross-Frame Persistence State Predictor (P06)`；禁止任何执行或写入。

## 1. 背景

D032 允许把简单 classic rule 迁移到本场景；persistence 胜复杂 history 不是“没方法”，可直接审计 persistence recipe。

## 2. 任务与输出

回传预测对象、input-action-output、current-only/history baselines、R²/条件、下游输出边界、最小场景差别、有限命题和三态结论。外部重复=`NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。

## 3. 陷阱与验收

不得把预测 R² 写成 BER 增益；不得因方法简单而拒绝。数字给路径。
