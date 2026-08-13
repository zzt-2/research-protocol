# Task Brief: P03 具体方法只读审计

> 来源: S023 | 产出位置: 回传主线程，不写文件 | 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读证据

## 0. TL;DR

只读审计 `Finite-Word-Length CCISP Selector (P03)`；禁止任何执行或写入。

## 1. 背景

D032 可接受性能—字长工程方法，但必须说明“优于 baseline”的指标到底是什么，不能用 proxy 冒充 PPA。

## 2. 任务与输出

回传 Q-format 步骤、float/宽字长 baseline、regret/identity/字长事实、动态范围问题、最小数值格式差别、可写命题和三态结论。外部重复=`NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。

## 3. 陷阱与验收

区分 64/40 bypass identity 与 Q(8,6)；不得声称 LUT/DSP/功耗/最优字长。
