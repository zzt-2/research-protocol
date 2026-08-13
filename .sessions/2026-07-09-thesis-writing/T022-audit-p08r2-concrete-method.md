# Task Brief: P08-R2 具体方法只读审计

> 来源: S023 | 产出位置: 回传主线程，不写文件 | 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读证据

## 0. TL;DR

只读审计 `Prefix-LS-Calibrated Coded FSO Receiver (P08-R2)`；禁止任何执行或写入。

## 1. 背景

D032 接受场景迁移和小型 calibration recipe。旧 P08/P08-R 的 hidden-SNR 结论不得继承，必须只看 R2 corrected chain。

## 2. 任务与输出

回传实际 prefix-LS→MMSE/LLR→LDPC 步骤、corrected B0 baseline、FER 数字/条件、信息边界、chronology 影响、最小场景差别、有限命题和三态结论。外部重复=`NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。所有数字给路径。

## 3. 陷阱与验收

不得引用旧 hidden-gamma 结果；不得因 delta 小于旧 MDE 而自动否决。
