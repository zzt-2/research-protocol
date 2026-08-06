# Task Brief: Step 3.5 双向引用链与 JOCN 2026 有界获取

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-sync-citations-jocn.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取本 worktree 与使用项目工具

---

## 0. TL;DR（执行方先读）

**你的任务**：对最高相关已获全文竞品 Sun 2025 (`10.1109/JLT.2025.3533197`, arXiv `2409.14400`) 做前向/后向引用链，并对 JOCN 2026 (`10.1364/JOCN.587273`) 做不超过协议止损线的合法获取重试。
**产出**：写入指定 worker log；合法获取成功时仅通过 `tools/download`/`tools/blit`/`tools/convert` 进入 `papers/` canonical 路径。

**最高纪律（违反一条就废了）**：
1. 引用链用 `tools/search --citations ... --citations-source both`；S2-only 条目不得当成真实引用，必须核验。
2. JOCN 最多按 `gw-acquire.md` 三条合法路径重试；不绕过访问控制，不抓 ResearchGate/Scholar/Xplore HTML，不从摘要伪造全文结论。
3. 若仍无全文，保留 exact-action novelty blocker，并记录每次命令、结果与 receipt；不得因失败继续循环。
4. 不修改 canonical 会话/项目状态，不进入 Step 4a，不实现、不仿真、不提交。

## 1. 背景

Sun 2025 已知边界：同一 training unit 中 TS-A/Godard clock recovery 与 TS-B frame/FOE 顺序分区，不是 joint `(frame, τ, CFO)` estimator。JOCN 2026 摘要声称 single preamble 同时支持 clock/frame/FOE，是 exact-action novelty 的最高风险 blocker，但此前三路径未取得全文。

## 2. 任务详情

### 2.1 要回答的问题

- Sun 2025 的前向、后向引用链中是否出现更直接的 joint estimator 或早期技术基础？
- JOCN 2026 本轮能否合法获得可读全文（≥50 行且 title/identity 通过）？
- 若只能取得摘要，它支持到哪一层 action claim，哪些结论必须继续 blocked？

### 2.2 执行方式

1. 读 `stages/gw-supplement.md`、`stages/gw-acquire.md` 与 `tools-guide.md`。
2. 双向引用链分别存档到 `search-archive/2026-08-06/`，逐条按 title/DOI/year/abstract 过滤。
3. JOCN 获取严格执行 dry-run→download/OA/arXiv→blit（若合法可用）的有界链；成功后核 identity、SHA、行数。
4. 只写 worker log与工具自动生成的检索/论文产物。

### 2.3 产出格式（强制）

```markdown
# Step 3.5 citation chains and JOCN acquisition
## 前向引用链
## 后向引用链
| title | year | DOI/arXiv | direction/source | verified citation | action class | relevance |
## JOCN 获取 receipt
| attempt | command/path | result | access boundary |
## JOCN identity/content gate
## 新高相关论文 acquire→read 清单
## 结论与 blocker
```

## 3. 已知陷阱

- S2 citation API 可能混入假阳性，尤其时间逻辑不可能的条目。
- 同一 burst preamble 的资源复用不自动等于同一联合 estimator。
- 可访问摘要、元数据或引用片段都不是全文。

## 4. 验收

- [ ] Sun 2025 双向引用链均已执行并落盘。
- [ ] 引用候选逐条核验，S2-only 未冒充真引用。
- [ ] JOCN 重试未超过止损线且无访问控制绕过。
- [ ] 成功全文有 identity/SHA/行数；失败有精确 blocker receipt。
- [ ] 没有修改 canonical 状态、代码、实验或 protected paths。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-3-5-sync-citations-jocn.md`
