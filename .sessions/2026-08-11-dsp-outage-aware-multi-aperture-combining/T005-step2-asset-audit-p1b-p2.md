# Task Brief: Step 2 P1-B/P2 已有全文资产与 C26 identity 审计

> 来源: S002 | 产出位置: 回传主线程，不写文件
> 日期: 2026-08-11
> 唯一文档: 本任务书 + worktree/shared-root papers/search archives

## 0. TL;DR

只读审计以下 4 个 DOI 的既有全文，并在本地索引中尝试闭合 C26 NT-GSC/TV+NT-GSC 正式 identity；不联网、不下载、不转换。

1. `10.1364/OFC.2024.W2A.31`
2. `10.1109/JPHOT.2020.2977955`
3. `10.1109/ACCESS.2020.3035748`
4. `10.1364/OL.511941`

最高纪律：只报告 availability/identity/content quality；不做方法结论、collision 或 comparator 强弱裁决。

## 1. 背景

这些是 P1 comparator 或 P2 strong neighbors；不能用它们替代 2019 P0。

## 2. 任务详情

- 审计 worktree/shared-root `papers/`、downloads、metadata；计算 source/content bytes/lines/SHA256。
- qualified 初判同 T004。
- 对 C26 只在现有 search-archive/index 内找 title/year/venue/DOI，无法闭合即 UNKNOWN；不得新增搜索。

### 产出格式

表格：DOI/C26 | found paths | provenance | source bytes/SHA | content lines/SHA | identity | qualified | missing/reason。

## 3. 已知陷阱

- OFC 全局索引已知 abstract 错配，不能将错配摘要当全文或 identity 之外的证据。
- 网页摘要/ResearchGate/read-note 不算 fulltext。

## 4. 验收

- [ ] 4/4 DOI 明确 AVAILABLE/UNAVAILABLE。
- [ ] C26 identity 明确 CONFIRMED/UNKNOWN。
- [ ] 无 Step3 语义输出。

## 附：产出回传位置

直接回传主线程，限 1500 中文字。
