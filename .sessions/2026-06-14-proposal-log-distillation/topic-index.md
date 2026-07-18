# 开题报告写作日志蒸馏

> 状态：completed | 创建 2026-06-14 | 完成 2026-06-15 | 跨 repo produces → thesis-platform (paper-eval / paper-write)

## 定位

开题报告写作过程产出的 ~300 个 .md 日志/规范文件（research-protocol repo），蒸馏成可注入 paper-eval / paper-write 工作流的**真实素材**。是这两个下游专题的上游生产者，**不直接实施下游改动**（如 paper-eval S033 的改写管线），只产出素材供其消费。

## 范围边界

### 原始目标（冻结）
从开题写作过程日志蒸馏 A写作痛点 / B真实评估标准 / C写作范例 / D工作流可用性反馈 四维素材，产出到能被 thesis-platform paper-eval/paper-write 直接引用的文档。

### 当前范围
**扫描源**（research-protocol repo，写作过程类 .md）：
- `.sessions/` 四专题：thesis-direction-pivot(~80写作日志/98总) + 2026-05-31-thesis-writing-prep(~30/36) + 2026-06-04-advisor-review-revision(~37/37) + 2026-05-31-thesis-writing(9/9)
- `毕设/` 写作过程文件（写作规范 / 决策状态 / 开题报告本体+批注 / PPT / 正文 / 文献综述，~124个中写作过程子集）
- 根目录散落：thesis-lessons.md、figure-composition-analysis.md

**提取维度**（全选，分批）：A / B / C / D

**产出落点**（下游接口契约，2026-06-14 与 thesis-platform 消费方对齐锁定）：

本专题 `distilled/` 下四维产出文件，每条素材带原文回溯指针：

| 维度 | 产出文件 | 下游消费方 | 每条产出形态 |
|---|---|---|---|
| A 痛点 | `distilled/A-pain-points.md` | paper-eval S033 改写 | `{来源指针, 痛点, 归类[检测器ID\|新维度], 对S033哪个待讨论项有输入}` |
| B 标准 | `distilled/B-eval-criteria.md` | paper-eval S025-S028 评估盲区 | `{批注原文指针, 批评点, 是否已覆盖[是→哪条rubric\|否→新维度]}` |
| C 范例 | `distilled/C-rewrite-fewshot.md` | paper-eval S033 改写 few-shot（✏️修正：不喂 good-examples） | `{原文指针, 好在哪, 适合做哪个改写目标的few-shot}` |
| D 流程 | `distilled/D-writing-workflow.md` | paper-write 管线设计（✏️修正：手搓流程逆向工程） | `{手搓步骤清单, vs paper-write现状, 优化建议}` |

**跨 repo 路径风格**：thesis-platform 引用本专题产出用 `/mnt/d/code/study/research-protocol/.sessions/2026-06-14-proposal-log-distillation/distilled/`（WSL 路径，**禁用 `D:\` Windows 风格**——WSL agent 读不到）。C/D 修正详见 decisions D002。

### 明确不含
- **非写作过程类文件**：formulas-master.md 等公式表、README、表格模板、verification/ 纯理论验证（V-NN 理论推导类）、font-test、pandoc 配置
- **不修改原始日志**（只读蒸馏，原文不动）
- **不直接实施 paper-eval S033**（S033 等素材产出后由 paper-eval 专题决定推进）—— 防越界
- **不扫 thesis-platform repo 的日志**（用户明确日志源在 research-protocol；thesis-platform 写作专题不在范围）
- **不扫 stages/thesis-materials.md**（用户 2026-06-15 判定"很旧别管"，见 D003；该文件曾疑似 paper-write 蓝图，已否决）

### 范围变更记录
- **2026-06-16 D005**：跨 repo 交付方式从"指针引用"（D002）改为"物理拷贝镜像"。distilled/ 16 文件物理拷到 thesis-platform `.sessions/distilled/`。research-protocol 保持单一真相源，thesis-platform 为只读镜像。source_ref 指针不改写（原始日志仍只在 research-protocol）。

## 已确认结论

### 不变量
1. **只读不改**：原始日志文件不动，只产出蒸馏素材
2. **produces 跨 repo（D005 修正）**：本专题在 research-protocol（**单一真相源**），下游 paper-eval/paper-write 在 thesis-platform。~~原 D002 用绝对路径指针引用不物理复制~~ → **D005 改为物理拷贝镜像**：distilled/ 16 文件已拷到 thesis-platform `.sessions/distilled/`（只读镜像，修改须回 research-protocol 改完重新拷）。source_ref 指针不改写，仍指向 research-protocol 原始日志。
3. **全量实读**：不靠文件名/元信息跳过阅读（用户明确否决此偷懒路径——日志多样性高，文件名看不出内容深度）
4. **不越界实施**：本专题产素材，下游专题消费素材做实施

### 其他结论
- repo 归属锁 research-protocol（日志源全在这 + 当前对话 + 治理规范成熟）
- registry 查重通过（research-protocol + thesis-platform 两边均无重复）
- 与现有 active 专题（research-direction-exploration / simulation-foundation-rebuild）无冲突、无依赖
- 提取维度与下游对应（2026-06-14 修正，详见 D002）：A→paper-eval S033 改写 / B→S025-S028 评估盲区 / C→**S033 改写 few-shot**（原 good-examples 映射已否决，PhD 库门槛/格式不兼容） / D→**paper-write 管线设计**（原"可用性反馈"已否决，用户未用过该管线；改手搓写作流程逆向工程）
- 下游接口契约已锁定：四维产出文件 + 每条字段形态见范围边界>产出落点表

## 进展线索
- **S001** 开专题讨论+锁边界（2026-06-14）——日志盘点发现~300文件，用户否决文件名偷懒，确认开专题+排除非写作，锁 repo=research-protocol
- **R001** 写作材料价值盘点与漏点分析（2026-06-14）——扫描方法论（四个问题）+ 七漏点 + 日期约束
- **D001** 专题定位/范围/repo/维度决策（新建）
- **D002** 下游接口契约锁定 + C/D 维度落点修正（与 thesis-platform 消费方对齐）
- **R002** 粗扫+细扫全量发现清单（2026-06-15）——**6 agent（3粗扫+3细扫）整合 73 条素材源（A10/B22/C22/D19）**，扫描覆盖完整，pilot 12 份候选已定，关键洞察 7 条
- **D003** 扫描范围细化——排除 stages/thesis-materials.md（用户判定很旧）
- **S002** pilot 扫描模板设计 + 12 份验证（2026-06-15）——**设计 scan-template.md（7 形态→4 维 schema，FROZEN）+ 3 agent 并行提 56 条（A6 B21 C17 D12）+ 确定性 grep 验证 PASS（4/4 阈值：字段覆盖/可合并/回溯/日期）**。pilot 56 条并入全量不重做
- **S003** A+B 维全量蒸馏（2026-06-15）——**R002 行号回填 10 源 + 3 agent 并行提 57 条（A22 B35）+ 6 文件 113 条确定性 grep 验证 PASS（7/7：id 分区/枚举/行号/日期/回溯/A 维覆盖/B 维覆盖）**。产出 distilled/A-pain-points.md（28 条覆盖 A1-A10）+ distilled/B-eval-criteria.md（56 条覆盖 B1-B22）草稿。agent-B1 首轮只给摘要→重派成功（经验：prompt 须明确"完整内容放代码块"）
- **S004** C+D 维全量蒸馏（2026-06-15）——**Test-Path 校验 33 源修正 3 处路径 + 2 轮 4 agent 并行提 99 条（C45 D54）+ 10 文件 212 条确定性 grep 验证 PASS（7/7）**。产出 distilled/C-rewrite-fewshot.md（62 条覆盖 C1-C22）+ distilled/D-writing-workflow.md（66 条覆盖 D1-D19）草稿。**R002 全部 73 条素材源全覆盖，四维契约草稿全部就位**
- **D004** verifier 交叉验证后的合并/互补定稿判断（对话 D）——2 组合并（B-511→B-301 / D-405→D-512）+ 8 组保留互补，**推翻 H004 的 1 组预判**（C-102/410/413 改互补，verifier 实读 yaml 发现 why_good 依赖"新旧方向对照"证据）
- **S005** 四批合并交付 + 关专题（2026-06-15，对话 D 最终）——**2 个独立 verifier agent 交叉验证（P6 不自审）source_ref 24/24 有效 + 语义近邻 10 组判断 + 合并去重 2 组 + 四维定稿 210 条 + 5 类次一级产物（检测器/规则库/few-shot/rubric/流程蓝图）+ 跨 repo PRODUCES 声明 + 关专题**。B-102 is_covered 校准（Popper→学术定位判据）。专题达成原始目标：从开题写作日志蒸馏四维素材，跨 repo produces 给 thesis-platform

## 未决项
- 扫描模板设计：产出字段已由下游契约锁定（见产出落点），扫描模板需把日志原文映射到这些字段，保证子 agent 产出可合并（防 M1 管道断裂）
- pilot 门控（分层试错法 P3）：扫描模板定后，**先 pilot 10-20 篇验证可合并性，再放大到全量**——防模板缺陷在 300 篇跑完才暴露
- 分批策略：~300文件分几批、每批几个子 agent（用户初步：先两批6个粗扫摸底）
- "写作过程类"边界精确分类（毕设/124个里哪些算写作过程、verification/ 报告算不算）——第0步盘点时定

## 当前位置
**专题已完成（2026-06-15 对话 D 定稿）**。四维蒸馏 + verifier 交叉验证 + 合并去重 + 次一级产物挖掘 + 跨 repo produces 声明全部完成。累计 **210 条定稿**（A28 B55 C62 D65，2 组合并去重：B-511→B-301 / D-405→D-512）+ **5 类次一级产物**（检测器集 17 条 + 规则库 11 条 + few-shot 集 15 个改写目标 + rubric 集 12 已有+8 新维度族 + 流程蓝图 16 管线模块）。verifier 抽查 source_ref 24/24 有效，语义近邻 10 组判断（2 合并 + 8 互补），推翻 H004 的 1 组预判（C-102/410/413 改互补）。下游接口：`distilled/PRODUCES.md` 声明 thesis-platform 可按 WSL 路径取用。registry status → completed。
