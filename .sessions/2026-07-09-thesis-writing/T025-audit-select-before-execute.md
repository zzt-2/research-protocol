# Task Brief: Select-before-execute 具体方法只读审计

> 来源: S023 | 产出位置: 回传主线程，不写文件 | 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读证据

## 0. TL;DR

只读审计 `Select-Before-Execute Single-Branch CPR`；禁止任何执行或写入。

## 1. 背景

D032 接受执行顺序/调度差别作为工程方法，不要求新 selector 或 FPGA PPA。

## 2. 任务与输出

回传 route-A/route-B recipe、等价性、调用量/operation/timing 数字、baseline 公平性、软件与硬件边界、最小差别、有限命题和三态结论。外部重复=`NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。

## 3. 陷阱与验收

不得外推 FPGA/PPA/总接收机 74.6%；不得因使用 CCISP selector 而拒绝调度方法身份。
