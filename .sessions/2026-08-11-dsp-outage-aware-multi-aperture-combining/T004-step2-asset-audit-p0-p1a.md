# Task Brief: Step 2 P0/P1-A 已有全文资产审计

> 来源: S002 | 产出位置: 回传主线程，不写文件
> 日期: 2026-08-11
> 唯一文档: 本任务书 + worktree/shared-root papers 目录

## 0. TL;DR

只读审计以下 5 个 DOI 的既有 PDF/content/metadata；不联网、不下载、不转换、不读方法内容。

1. `10.1016/j.optcom.2019.03.069`
2. `10.1109/WISEE61249.2024.10850117`
3. `10.1109/JPHOT.2023.3265847`
4. `10.1364/OE.24.012661`
5. `10.1109/ICCC56324.2022.10065885`

最高纪律：只报告 fulltext availability、identity、文件质量统计；不得提取 input-trigger-action-output，不判 collision。

## 1. 背景

Step1 已 PASS，但 2019 direct competitor exact collision 保持 UNRESOLVED。Step2 只负责 acquisition，不做精读。

## 2. 任务详情

### 2.1 检查

- `papers/doi/`、`papers/downloads/`、`D:/code/study/research-protocol/papers/` 共享根。
- 每篇列 source path、metadata status、PDF/HTML bytes、content.md lines、title/DOI identity 是否一致。
- 计算现有 source/content SHA256；只做文件级 hash。
- qualified 初判：content≥50有效行、非反爬/目录页、identity一致、无大面积乱码。

### 2.2 产出格式

表格：DOI | found paths | provenance | source bytes/SHA | content lines/SHA | identity | qualified | missing artifact / reason。

## 3. 已知陷阱

- read-note、abstract JSON、metadata-only 不等于 fulltext。
- shared root 与 worktree 可能不同，必须分别列出，不自行复制。
- 不因内容可读而开始方法总结。

## 4. 验收

- [ ] 5/5 DOI 都有明确 AVAILABLE/UNAVAILABLE。
- [ ] 每个 AVAILABLE 都有 path/hash/lines/identity/quality。

## 附：产出回传位置

直接回传主线程，限 1500 中文字。
