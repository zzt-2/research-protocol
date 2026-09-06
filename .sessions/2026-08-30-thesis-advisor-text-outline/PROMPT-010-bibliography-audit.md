# PROMPT-010: 参考文献批——审计现有库并规划补齐至 100+（外文 2/3、高水平）

> 来源: 用户 2026-09-06 指示（"弄一百多个，其中外文文献三分之二，且尽量高水平"）| 日期: 2026-09-06
> 关系: 与 PROMPT-009（组装批）可并行；本批不改正文

## 提示词正文（用户粘贴到新对话）

请审计我的学位论文参考文献库，并给出补齐到 100+ 条的执行计划。全程自主推进，不中途提问。

**工作目录**：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`（worktree，治理与章节稿在此；启动时必须使用 session-governance 报到，专题 `.sessions/2026-08-30-thesis-advisor-text-outline/`，读 topic-index、S005 末两节、voice.md）。

**资产现状：**

- 主库：`D:\code\study\research-protocol\毕设\写作材料\references.bib`（141 条，质量未审计）
- 模板库：`毕设/正文/latex/reference/main.bib`（6 条模板示例，组装批会替换）
- 正文实际引用：章节稿（`毕设/论文/导师讨论稿/章节稿/01—06*.md`）40 个唯一键
- 论文库：`papers/`（arxiv/doi/manual + index.json）、`search-archive/`（历史检索）
- 判据：`毕设/写作质量规范.md` §13（质量门槛：IEEE Trans. Commun./JLT/TWC/OL/JOCN 等为主；SPIE/OFC/OE/OL 顶会顶刊允许；低 IF 期刊逐条评估"不可替代才保留"）+ §14（GB7714-87 字段完整：作者/标题/期刊全称/卷期页年/DOI）

**目标（用户原话口径）：** 总量 100+ 条；外文 ≥2/3；尽量高水平（trans 级为主）。

## 任务（四步，每步产出落文件）

1. **审计现有 141 条**（subagent 分批，每批 ≤50 条，≤15 分钟/批）：
   - 字段完整性（§14 逐条对照：作者格式、期刊全称不缩写、卷/期/页/年、DOI）
   - 质量分级：A=trans/顶刊顶会；B=知名但非顶（如 Optics Express、中等会议）；C=低 IF/边缘期刊（Sensors、Photonics 等）；D=中文学位论文/标准/网页类
   - 重复条目（同文异键）、格式错误（braces、and 连接、中文条目 author 格式）
   - 产出：`毕设/写作材料/bib-audit-R1.md`（逐条行：键｜分级｜字段缺陷｜处置建议：保留/修字段/降级/删）
2. **正文 40 键对账**：逐键核对 references.bib 中条目是否存在、bibliographic 信息是否与论文库 papers/ 的 meta 一致（有 meta.json 的查证，没有的标注"未验证"）；列缺失键清单。
3. **补齐规划（到 100+，外文 ≥2/3）**：
   - 现有 141 条按处置建议折算"可保留数"，算缺口
   - 按章列候选补引位置与候选文献（Ch1 综述各小节扩引、Ch2 模型出处、Ch3/Ch4 方法相关工作、Ch5 FPGA 相关）：每处给"位置（文件:行）+ 建议引用的文献（具体到 DOI/标题）+ 一句引用理由"
   - 检索用项目工具：`bash tools/search --query "..."`（从仓库根目录调用，见 tools-guide.md §1）；**主对话严禁 WebSearch/webReader**，需要 web 验证时派 subagent（Semantic Scholar API / DOI 交叉验证，返回 ≤500 词摘要）——规范"web 事实性交叉验证"条款执行
   - 候选清单按 §13 质量门槛过滤：优先 trans；低 IF 仅在"该子领域唯一相关工作"时保留并注明理由
4. **执行边界**：本批**不改正文、不改 references.bib 主库**（审计与计划产出为准）；正文补引（每处一句话内插入 \cite 级改动）作为后续批，等用户拍板补引清单后执行。

## 产出与治理

- 产出：`bib-audit-R1.md`（审计）+ `bib-plan-R1.md`（对账+补齐计划，含总量/外文占比/质量分布预测表）；两文件落 `毕设/写作材料/`。
- 治理：S005 追加文献批记录（或按治理规则新开 S###）；发现需拍板的事项（如某低 IF 文献去留）记 D### 顺延；topic-index 更新；commit 一次。
- 交接：给用户一份简短总结（141 条里 A/B/C/D 各多少、建议删多少、缺口多少、补引位置多少处、候选质量分布），等用户拍板后进执行批。
