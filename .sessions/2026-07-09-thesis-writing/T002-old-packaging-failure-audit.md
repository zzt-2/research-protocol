# Task Brief: 旧“看别人怎么包装”工作的失败复盘

> 来源: S018 | 产出位置: 回传主线程结构化摘要（主线程写 `peer-thesis-method-packaging-audit.md`）
> 日期: 2026-08-03
> 唯一文档: 执行方只需本 brief 与工作树中的历史 `.sessions/`、旧 survey/review notes

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。
**你的任务**：用文件证据复盘此前“参考同门/硕士论文包装方式”为什么没有产出可执行方法。
**产出**：一份不超过 2500 字的结构化摘要，回传主线程；不要修改任何文件。

**最高纪律（违反一条就废了）**：

1. facts-first，每条核心结论给 `文件:行号`；无证据标 `[未证实]`。
2. 区分“全文方法章”“摘要/目录/创新点”“标题印象”，不得把三者混写。
3. 不提出新方法论，只诊断旧流程的输入、提取深度、映射和执行断点。
4. 不使用 WebSearch，不读外部网页，不改仓库。
5. 单次工作不超过 15 分钟。

## 1. 必读范围

- `.sessions/2026-05-30-ch3-direction-exploration/`
- `.sessions/2026-05-31-thesis-writing-prep/`
- `.sessions/2026-06-17-thesis-method-redirection/`
- `.sessions/2026-06-17-thesis-method-redirection/R001-survey-peer-master-theses.md`
- `.sessions/thesis-structure-research/`（若不存在则按 registry 定位实际路径）
- 关键词：`同门论文|硕士论文|包装|创新点|方法章节|baseline|增量`

## 2. 必答问题

1. 当时实际看了多少篇、每一批读到什么深度？
2. 是否精读核心方法章，还是主要停留在摘要/目录/创新点？
3. 是否拆出 baseline→method delta？
4. 是否映射到本项目资产？
5. 是否形成可直接执行的 packaging recipe / 最小补实验？
6. 为什么最后没有帮助产出方法？
7. 哪些旧结论仍有证据，哪些只是标题/摘要印象？

## 3. 产出格式（强制）

```markdown
## Coverage Facts
- 批次/篇数/读取深度/证据指针

## Seven Answers
1. ...

## Root-Cause Table
| symptom | verified root cause | evidence | consequence | still valid? |

## Valid vs Impression-only
| old conclusion | evidence grade | keep/reject | pointer |

## Minimal Conclusion
不超过 5 条。
```

## 4. 已知陷阱

- R001 声称“32 篇”不等于 32 篇全文方法章精读，必须逐项核深度。
- 旧文档可能把“创新点标题”当“真实方法动作”，必须看有没有 baseline delta。
- 不要因为旧方向后来 Kill 就把包装调研本身判无效；只判断它是否生成过可执行 recipe。

## 5. 验收

- [ ] 七个问题全部回答，且每个答案有证据指针。
- [ ] root-cause table 简短、没有新造方法论。
- [ ] 明确区分全文、摘要/目录、标题印象。
- [ ] 不修改文件。
