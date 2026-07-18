# [S001] 开专题讨论与边界锁定

> 2026-06-14 | 开题 | 状态：进行中
> 2026-06-14 续接：下游接口契约锁定（与 thesis-platform 消费方对齐，详见 D002）

## 目标
开 proposal-log-distillation 专题前的对齐讨论：确认日志源、体量、范围边界、repo 归属，走治理流程建专题基础设施。

## 记录

### 日志源盘点（facts-first）
用户初始指令指向 `.sessions/2026-06-04-advisor-review-revision/` 和 `2026-05-31-thesis-writing-prep/`，并说"很多，外面还有别的文件"。盘点结果：

| 位置 | .md 数 | 行数 | 性质 |
|------|--------|------|------|
| .sessions/thesis-direction-pivot | 98 | 23653 | 大头，含43个PROMPT |
| .sessions/2026-05-31-thesis-writing-prep | 36 | 9059 | 含21个PROMPT |
| .sessions/2026-06-04-advisor-review-revision | 37 | 5971 | 含20个PROMPT，写作修订 |
| .sessions/2026-05-31-thesis-writing | 9 | 3181 | |
| 毕设/ | 124 | 37840 | 外部文件主体，含写作规范/决策/开题报告/PPT |
| 根目录散落 | ~3 | ~5000 | thesis-lessons.md(26.5K) 等 |

合计 ~300+ 文件 / ~86000 行。

### 关键纠正：否决"文件名偷懒"方案
我曾提出"用文件名+元信息建索引 v0，跳过部分阅读"的优化方案。**用户明确否决**（原话）："它们多种多样，你这么干肯定会漏很多。而且，外部有很多别的文件，还有很多中间弄的规范，很多都有能用上的地方。这些都是要看的。你这么搞肯定不行"

否决理由（记录，防压缩丢失）：
- 日志多样性高，文件名看不出内容深度（design-decisions.md 613行里有什么决策？导师批注215行批了什么？）
- 外部文件（毕设/124个）+ 中间规范（writing-patterns-*.md 千行级）大量，文件名不反映价值
- "靠文件名跳过=必然漏" → 必须**全量实读**

### 中间规范金矿（用户指引的"中间弄的规范"，已定位）
毕设/ 下千行级写作规范：
- writing-patterns-paragraph.md(1459) / -sentence.md(1019) / -ch2ch3.md(1016) → C 范例
- 写作质量规范.md(732) → D 工作流
- design-decisions.md(613)、开题报告v2-导师批注.md(215)、ai-trace-report.md(209) → A 痛点 / B 评估
- verification/ 下 V-NN 报告 → B 评估（边界待定：纯理论验证 vs 论证写作）

### 跨 repo 架构确认
- 日志源 + 本专题：research-protocol repo（/mnt/d/code/study/research-protocol/）
- 下游 paper-eval/paper-write：thesis-platform repo（/home/zzt/code/thesis-platform/）
- paper-eval S033 topic-index(104-109行) 已规划本专题：produces 给 paper-eval，slug=2026-06-14-proposal-log-distillation，S033 暂停等本专题产出
- 跨 repo produces 用绝对路径指针（thesis-platform H006 已有先例引用 research-protocol）

### 用户拍板的决策
1. 专门开专题（不塞现有专题）
2. 排除非写作过程类（公式表/README/表格模板/纯理论验证）
3. repo 归属 research-protocol（用户默许，未反对）

### 续接：下游接口契约锁定（2026-06-14）

与 thesis-platform 消费方（paper-eval S033/S025-S028、paper-write）对齐下游需求，锁定产出契约：

- **四维产出文件 + 字段形态**：详见 topic-index 范围边界>产出落点
- **C 维度修正**：从 good-examples(S016-S020) 改喂 S033 改写 few-shot（PhD 库门槛不兼容）
- **D 维度修正**：从"可用性反馈"改"手搓写作流程逆向工程→paper-write 设计输入"（用户未用过 paper-write 管线，时间紧手搓完成开题）
- **跨 repo 路径**：thesis-platform 引用用 `/mnt/d/...` WSL 路径，禁 `D:\`
- 决策记 D002（取代 D001 第4条 C/D 部分）

契约锁定后，扫描模板设计的约束变了：不再是"自上而下想提取字段"，而是"把日志原文映射到契约已锁定字段"，防 M1 管道断裂。下一步先 pilot 10-20 篇验证可合并性。

## 决策引用
- D001：专题定位/范围/repo/维度（新建）

## 范围确认
- 本轮是否在 scope boundary 内：是（开专题+锁边界即本轮目标）

## 后续
1. **设计扫描模板**：把日志原文映射到契约已锁定字段（A痛点/B标准/C范例/D流程，见 topic-index 产出落点），保证子 agent 产出可合并（防 M1 管道断裂）。**先 pilot 10-20 篇验证可合并性，再放大到全量**（分层试错法 P3）
2. **第0步建可列举索引**：基于扫描模板，分批实读建索引
3. **分批策略**：~300文件，用户初步"先两批6个粗扫摸底"，具体子 agent 数待扫描模板定后细算
4. **"写作过程类"边界**：毕设/124个里哪些纳入，第0步盘点时与用户确认
