# Task Brief: P01 具体方法只读审计

> 来源: S023 | 产出位置: 回传主线程，不写文件 | 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读证据

## 0. TL;DR

只读审计 `Pilot-SNR-Calibrated CCISP (P01)`。禁止实验/脚本/联网/检索/Groundwork/写文件。经典或差别小不构成否决。

## 1. 背景

D032 标准：正确经典 baseline；明确场景真实改善；完整 recipe 非完全相同即可。场景、估计量、阈值或配置有差别均可形成 extension。外部 exact duplicate 本轮不查。

## 2. 任务与输出

读 P01 worker log、result JSON、2A authority 和必要 caller。回传：①实际问题；②逐步 input-action-output；③ baseline 公平性；④逐项数字/条件/证据路径；⑤四条真实性检查；⑥与原 CCISP/P02 的最小差别；⑦可直接写的有限方法命题；⑧结论 `DIRECTLY_PACKAGABLE / PACKAGABLE_WITH_CAVEAT / NOT_SUPPORTED_BY_EXISTING_RESULT`。外部重复状态写 `NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。

## 3. 陷阱与验收

不得因 global ref=11 更强而 Kill；不得把 4/5 recovery 写成全域成功。所有承重数字必须给路径。
