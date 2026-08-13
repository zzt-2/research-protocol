# Task Brief: P02 具体方法只读审计

> 来源: S023 | 产出位置: 回传主线程，不写文件 | 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读证据

## 0. TL;DR

只读审计 `Low-SNR Reference-Calibrated CCISP (P02)`；禁止任何执行或写入。

## 1. 背景

D032 允许阈值/参数/场景差别形成方法，不得以“只是 ref 9→11”直接拒绝。

## 2. 任务与输出

回传问题、离线冻结与运行期步骤、baseline、+0.4539/+0.0961 dB 等数字条件、truth-defined slice 与 deployable action 边界、最小 recipe 差别、有限命题和三态结论。外部重复=`NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。

## 3. 陷阱与验收

不得谎称 runtime region selector；不得因方法简单而否决。数字给路径。
