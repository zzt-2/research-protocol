# Handoff: 精读溯源机制落地 + 方向探索精读前置阻断

> 来源: S001(read-traceability) + V001/V002 + 干预 research-direction-exploration | 交接目标: 新对话续 read-traceability 改进 或 research-direction-exploration 精读
> 文件名: H001-read-traceability-and-exploration-blocker.md

## 已完成边界

**read-traceability 专题（本轮主体）**：
- S001 设计两层架构：全局 `papers/_read_notes/{paper_id}.md`（客观精读，全局共享）+ 项目级 `read-log.md`（适配+日志）
- architect 评估补 4 处遗漏（关键：paper-materials-workflow Step5 同步改否则写作阶段断链）
- **executor 改 4 框架文件 13 处**（CLAUDE.md / templates.md / gw-read.md / paper-materials-workflow.md），主线程独立验证 PASS（grep+Read 交叉）
- V001 dry-run（1篇端到端）：**机制 PASS**——双向溯源实测通，字段/命名/read-log 都对
- V002 定向审计（**反转预期**）：R002 留选/存疑 6 方向 9 篇关键论文 **0 篇下载**，已下载抽样错配率约 20%（属少数），**不需全量审计**
- 固化 memory：`feedback_paper-download-tools`（IEEE/CNKI→blit）+ 重写 `reference_cnki-tools`（扩 IEEE）

**research-direction-exploration（干预）**：
- S002 粗筛完成（TENTATIVE 摘要级）：留 E1/B1/A3，存疑 A2/C2/D2，砍 16
- D001 评判框架 + D002 凑创新点抛弃 定稿
- ⚠️ topic-index 已加"精读前置阻断"：9 篇论文未下载 + title 核验要求

## 不要做什么

1. **不要全量审计 index.json title**——V002 已证 R002 方向论文没下载（审计无对象），已下载错配是少数
2. **不要跳过 Groundwork 前置直接 MVE**（research-direction-exploration 跳步红线，见其 H001/S002）：正确链 D001筛→Groundwork前置（精读/综述/baseline合法性/空白零假设）→合规MVE（FR-11~15）→Contract→Execute
3. **不要笼统写 `tools/download` 拉论文**——IEEE(`10.1109/`)/CNKI 走 `blit --download`（不写 index.json 需手动追加），arXiv/OA 才走 download（见 `feedback_paper-download-tools`）
4. **不要信 `download_status:success`**——photonics10080914 案例证明可能是假象（title↔content 错配）
5. **不要重新设计精读溯源机制**——两层架构已落地 5 文件 + dry-run PASS，只待 P0/P1 改进

## 必读（按优先级）

1. `.sessions/2026-06-15-read-traceability/topic-index.md` + `S001-design.md`（§6 architect定稿 / §7 实施 / §8 dry-run）+ `verifications.md`（V001+V002）
2. `.sessions/2026-06-10-research-direction-exploration/topic-index.md`（重点："精读前置阻断"+"S002 粗筛"+"跳步红线"+"凑创新点抛弃D002"）+ `decisions.md`（D001+D002）+ `S002-*.md`
3. memory（已加载）：`feedback_paper-download-tools` + `reference_cnki-tools`（IEEE/CNKI blit 分工）
4. 若续 P0/P1 改进：`tools-guide.md` §4（blit/download 分工，line 173-175）+ `stages/gw-read.md` + `CLAUDE.md` 目录结构（line 24/46/77-78/86/154）

## 接口变更（框架文件改动，非代码）

read-traceability 落地的 5 文件 13 处（源文件路径 [MUST] 字段 + 全局 `_read_notes` + `read-log`）：

| 文件 | 改动位置 |
|------|---------|
| CLAUDE.md | 目录结构(24/46行)、文件路径规则表(77-78)、跨阶段护栏表(154)、禁止事项(86) |
| templates.md | L01模板(318) + 新增"源文件路径字段规则[MUST]"小节(369-380) + 浅读(394) |
| stages/gw-read.md | 派遣清单表#1(16, 13+→14+字段) + L01模板(34) + 质量门槛(176, 含read-log 7字段) |
| stages/paper-materials-workflow.md | Step5 核心条目(109) + 文献索引(114) + 质量门槛(196) |

paper_id 规则：取 `papers/{type}/{id}/` 目录 `{id}` 字面值（arxiv去版本号/doi转义字面值/manual slug），不二次处理。

## 失败数据附录

- **title↔content 错配案例**：DOI `10.3390/photonics10080914`，index/metadata title 标 "All-Digital OPLL for LEO Satellite"，content.md 正文实为 "Temporal Dynamics of Asymmetrical Dielectric Nanodimer Wrapped with Graphene"。grep 实证：OPLL 词 0 命中，graphene 词 71 命中。`download_status:success`/`content_quality:good` 全是假象。
- **错配率抽样**：papers/ 里 5 篇有 content.md 的 FSO 主题论文，4 对 1 错（≈20%，样本极小，非系统性失效）
- **R002 论文状态**：9 篇关键论文（7有DOI+2无DOI）在 papers/index.json(256条)+papers/doi/(230目录) 均 0 命中

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| P0 下载流水线 title 校验 | 治本（content 真实标题回填 index + 校验 status） | 未做 | 大量下载 IEEE/CNKI 前 |
| P1 gw-read abort 协议 | 治标（content title vs 派遣 title 关键词0重叠则 abort） | 未做 | 同上（P1 依赖 content 真实标题可提取，建议 P0 后） |
| P2 L01 模板去 RL 强绑定 | "实现关键细节"字段泛化 + Baseline/6子表按论文类型差异化 | 未做 | 精读非 RL 论文时 |
| content.md 清洗 | 转换管线（MDPI 噪声 / doi 补转144篇） | 已拆独立子任务，不急 | — |
| R002 9篇论文未下载 | 精读前置 | 0篇下载 | 启动6方向精读时 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 精读溯源机制 | 双向溯源通（笔记↔源文件↔read-log） | V001 dry-run | 1/1 PASS |
| title↔content 一致 | content 真实标题 = index title | V002 抽样 | 4/5（80%） |

## 接收方验证

- [ ] 读 read-traceability `topic-index.md` 不变量 + S001 §6/7/8
- [ ] 读 research-direction-exploration `topic-index.md` 的"精读前置阻断"+"跳步红线"
- [ ] 验证 V002 结论：`grep -c` R002 的 9 个 DOI 在 `papers/index.json` 应 0 命中
- [ ] 确认 memory `feedback_paper-download-tools` 已加载（IEEE/CNKI→blit）
- [ ] 检查 `_registry.yaml`：read-traceability active，depends_on research-direction-exploration

## 下一轮

新对话按用户意图二选一：

**A. 继续 read-traceability 改进（P0/P1，框架改动）**：
- P0 治本：`tools/download` / `gw-acquire` 加 title 一致性校验（下载后用 content.md 真实标题回填 index.json/metadata.json + 校验 `download_status:success` 时 title 必须匹配 content）
- P1 治标：`gw-read` 加 abort 协议（精读前读 content 真实标题，与派遣 title 关键词 0 重叠则 abort 不产出）
- 顺序：先 P0（下载流水线）再 P1（gw-read）

**B. 回 research-direction-exploration 主线（6方向精读，Groundwork 前置第一步）**：
- 第一步：按 DOI 来源下载 R002 9篇（IEEE→`blit --download`，OA→`tools/download`），blit 的手动追加 index.json
- 第二步：逐篇核 title↔content（P1 abort 协议还没做就手工核，像 dry-run 那样 grep 实证）
- 第三步：gw-read 精读，确认/推翻 E 三检验
- ⚠️ 这是 Groundwork 前置第一步，**不是 MVE**（跳步红线）

---

**本轮未提交**（用户说"暂不急"）。换对话前如要防丢失，本轮改动 = read-traceability专题(S001/V001/V002/topic-index/H001/voice) + research-direction-exploration topic-index + 5框架文件 + memory(feedback_paper-download-tools + reference_cnki-tools + MEMORY.md)。
