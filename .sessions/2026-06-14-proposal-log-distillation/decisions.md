# Decisions — 开题报告写作日志蒸馏

## D001: 专题定位、范围、repo、提取维度决策

> 2026-06-14 | 强度：INVARIANT(1,3,4) / DECIDED(2,3,4) | 新建 | 取代：无

### 决策内容

**1. 专题定位**（INVARIANT）
proposal-log-distillation 是 paper-eval/paper-write 的**上游真实素材生产者**，只产出素材，不直接实施下游改动（如 paper-eval S033）。S033 等下游实施等本专题产出后由各自专题决定。

**2. repo 归属**（DECIDED）
落 research-protocol/.sessions/2026-06-14-proposal-log-distillation/。
理由：日志源~300文件全在 research-protocol + 当前对话在此 + 治理规范成熟。
跨 repo produces（下游在 thesis-platform）用绝对路径指针。

**3. 范围边界**（DECIDED，详见 topic-index）
- 扫描源：research-protocol 写作过程类 .md（.sessions 四专题 + 毕设/写作过程文件 + 根目录散落）
- 明确不含：公式表/README/表格模板/纯理论验证/non-writing 文件；不修改原文；不扫 thesis-platform 日志
- 排除非写作过程类：用户明确"不像写作过程的就不弄了"

**4. 提取维度**（DECIDED）
A写作痛点 / B真实评估标准 / C写作范例 / D工作流可用性反馈，**全选分批**。
下游对应：A→paper-eval S033 / B→S025-S028 / **C→good-examples(S016-S020)〔superseded，见 D002〕** / **D→paper-write管线〔superseded，见 D002〕**

> ⚠️ C/D 下游映射已被 D002 取代（C→S033 改写 few-shot；D→手搓流程逆向工程→paper-write 设计输入）。本条仅 A/B 映射仍有效。

### 否决记录（防压缩丢失）
- **否决"文件名/元信息偷懒"方案**：曾提议用文件名+前缀建索引v0跳过部分阅读。用户否决，理由：日志多样性高、文件名不反映内容深度、外部文件+中间规范大量、靠文件名跳过必然漏。**必须全量实读。**
- **否决"专题落 thesis-platform"**：曾基于"下游在 thesis-platform"倾向落那边。修正：日志源全在 research-protocol，落 research-protocol 更合理。

### 触发推翻条件
- 若 thesis-platform 的写作日志也需纳入 → 扩 scope（需 scope change record）
- 若发现下游 paper-eval/paper-write 已弃用 → 重评 produces 关系
- 若"全量实读"在执行中被证明对某类文件低效（如纯格式笔记）→ 可针对性调整，但需显式记录

## D002: 下游接口契约锁定 + C/D 维度落点修正

> 2026-06-14 | 强度：DECIDED | 新建 | 取代：D001 第4条(C/D 部分)

### 决策内容

下游接口契约（本专题产什么、thesis-platform 消费方要什么）已与消费方对齐锁定。四维产出文件 + 每条字段形态详见 topic-index 范围边界>产出落点。

**两处维度落点修正**（取代 D001 第4条的 C/D 映射）：

1. **C 写作范例**：从"喂 good-examples(S016-S020)"改为"喂 paper-eval S033 改写 few-shot"。
   - 否决理由：S016-S020 是 PhD 论文范例库（194 篇 PhD 语料，S017 质疑审查删 16 条改 11 条），门槛/格式/用途与用户开题报告范例不兼容。
   - 新落点：用户自己语境下的好写法，适合做 S033 改写 prompt 的 ❌原文→✅改后 few-shot 示范。

2. **D 工作流**：从"paper-write 可用性反馈"改为"手搓写作流程逆向工程 → paper-write 管线设计输入"。
   - 否决理由：用户因时间紧未用 thesis-platform paper-write 管线，手搓完成开题报告；原"可用性反馈"无产出源。
   - 新落点：用户手搓的相对固定写作流程，经实践检验，逆向工程成 paper-write 管线设计的真实需求模型（步骤/顺序/卡点）。

### 跨 repo 路径风格
thesis-platform 引用本专题产出用 `/mnt/d/code/study/research-protocol/...`（WSL 路径），禁用 `D:\` Windows 风格。

### 触发推翻条件
- 若下游 S033 / good-examples / paper-write 弃用或大改 → 重评对应维度落点
- 若 pilot 阶段发现某维度产出形态无法填充（日志里无该类素材）→ 该维度降级或剔除

## D003: 扫描范围细化——排除 stages/thesis-materials.md

> 2026-06-15 | 强度：DECIDED | 新建 | 取代：无（范围细化）

### 决策内容
`stages/thesis-materials.md` 不纳入扫描范围，已从素材源排除（R002 排除项表已记）。

### 触发与理由
- 细扫B 曾判定该文件是"paper-write 设计蓝图"（§2 材料包映射 + §4 6 文件提取流程 + §引用质量 rubric），建议纳入 D 维度核心。
- **用户 2026-06-15 原话否决**："stages/thesis-materials.md 别管，它很旧。"
- 该文件 mtime 2026-05-21（pivot 前），内容陈旧，不反映当前写作流程。

### 影响
- D 维度"材料包蓝图"由 D1（S003 L1/L2/L3）+ D2（PROMPT-001 对话隔离）+ D5（数字审计三步法）覆盖，paper-write 设计输入不缺。
- B 维度"引用质量 rubric（中文期刊≥10 篇 / 核心引用预印本率≤30% / 全部预印本率≤40%）"暂无替代源，R002 B11 标"待补"。其余引用质量（GB7714 / DOI 验证）由 bib-quality-issues + citation-verification 覆盖。

### 触发推翻条件
- 若后续发现该文件有不可替代的素材 → 重评（需 scope change record）

## D004: verifier 交叉验证后的合并/互补定稿判断

> 2026-06-15 | 强度：DECIDED | 新建 | 取代：部分 H004 的语义近邻组判断

### 决策内容
对话 D 步骤 1 派 2 个独立 verifier agent 交叉验证后，对 H004 的 10 组语义近邻判断做最终定稿。**verifier 推翻了 H004 的 1 组判断**，其余 9 组采纳（含 2 组合并方向微调）。

#### 应合并（2 组，真冗余）
- **B-301 + B-511**：合并为 B-301 为主条目。B-511（design-decisions 否决记录）的 R08/R09/R14 三个声称否决案例作为 B-301 的实例化段并入。合并后删除 B-511 独立条目，避免 is_covered 自指循环（B-511 原 covered_by 指向 B-301）。
- **D-405 + D-512**：合并为 D-512（TL-21 完整版）为主条目，D-405（CONCLUSIONS-VERIFY Step3）作为"应用场景：CONCLUSIONS.md 数字反向溯源"并入。D-512 信息量 ⊃ D-405。

#### 应保留互补（8 组，勿合并）
1. **A-101 vs A-401**：根因（自回归机制）vs 量级（9/8/11/4/12）——互补
2. **B 铁律族 B-204/404/205/405**：4 条独立 grep 可检测铁律——保留 4 条
3. **B 增益真实性族 B-301/302/306/401/406/407**：6 条覆盖声称→基线→归因→方法→鲁棒性→自评全链路——保留
4. **B 引用可靠性族 B-303/408/409/412/413**：5 条不同抽象层级（单点失败案例/4维框架/内容匹配细化/诚信4条/DOI三件套）——保留
5. **C-101 vs C-507**：句子级单标签 8 类（R011）vs 句间逻辑关系链（S004）——两套不同粒度体系，互补
6. **C-102 + C-410 + C-413**：⚠️ **推翻 H004 的合并判断**。C-102 是抽象节奏公式，C-410 是旧 GNN 方向范文实例，C-413 是 FSO 当前方向范文实例。合并会丢失"新旧方向句式普适性对照验证"证据（C-413 的 why_good 明确指出新旧对照是价值所在）。保留 3 条，fewshot_target 交叉引用。
7. **C 符号参数族 C-402 vs C-518/519**：单条写法/冲突消歧/全文管理三层正交——保留
8. **D-303 vs D-429**：S003 模板设计层分层检查 vs 写作质量规范附录A 执行层 17 项清单——保留
9. **D-411 vs D-409**：时间紧迫度四级（引用错误修复）vs 缺陷类型五级（bib 元数据修复）——轴不同，保留互补（H004 未明确判断，verifier 补判）

### 触发与理由
- **P6 原则**：verifier 必须独立，不能由蒸馏 agent 自审。2 个 verifier 分别覆盖 A+B 和 C+D，抽查 source_ref 24/24 有效（13+11），语义近邻判断覆盖 10/10 组。
- **verifier 推翻 H004 的 1 组**（C-102+410+413）：H004 是主对话压缩前基于索引草稿的预判，verifier 实读 yaml 全字段后发现 C-413 的 why_good 显式依赖"新旧方向对照"，物理合并会丢证据。这正是 P6 独立验证的价值。

### 影响
- 四维草稿需更新为定稿：合并 2 组（B-301 吸收 B-511 / D-512 吸收 D-405），索引段修正 C-102/410/413 互补、C-101/507 互补（草稿 L106 原写"合并"自相矛盾）。
- B-102 is_covered=是 映射牵强（学术定位≠Popper 可证伪性）：verifier 建议改 is_covered=否 + 新维度"学术定位判据"。**采纳**，定稿时调整。

### 触发推翻条件
- 下游 paper-eval/paper-write 消费时发现某合并组实际需要拆分 → 重评



## D005: 跨 repo 交付方式变更——指针引用 → 物理拷贝（镜像）

> 2026-06-16 | 强度：DECIDED | 新建 | 取代：D002 不变量 2「跨 repo 用绝对路径指针引用，不物理复制」

### 决策内容
蒸馏产物 `distilled/`（16 文件）**物理拷贝一份**到 thesis-platform repo 的 `.sessions/distilled/`。推翻 D002 原定的"指针引用不复制"设计。

#### 现状（拷贝后）
- **蒸馏产物**（distilled/ 16 文件）：**两份**——research-protocol（主）+ thesis-platform（镜像）
- **原始日志**（source_ref 指向的 73 个源文件）：**一份**，仍只在 research-protocol。thesis-platform 那边的 agent 回溯 source_ref 原文时，仍走 `/mnt/d/code/study/research-protocol/...` 绝对路径指针（本机 WSL 可访问 /mnt/d/）

#### 真相源与同步规则
- **research-protocol 是单一真相源（SOURCE OF TRUTH）**。任何内容修改先改 research-protocol，再手动同步到 thesis-platform 镜像。
- **thesis-platform 的 `.sessions/distilled/` 是只读镜像**。下游 paper-eval/paper-write 消费时读这份，但**不得在此处修改**——修改请回 research-protocol。
- **分叉风险**：若两边内容不一致，以 research-protocol 为准。两边 PRODUCES.md 已标注镜像关系。

### 触发与理由
- **用户 2026-06-16 原话**："你直接整个文件夹复制到 .sessions/ 下面就行"——明确要物理拷贝，推翻 D002 指针引用设计。
- **理由**：thesis-platform 自包含、git 可跟踪、paper-eval/paper-write 的 agent 不必每次跨 repo 读 /mnt/d/ 取蒸馏产物（虽然原始日志仍需跨 repo）。

### 影响
- PRODUCES.md（research-protocol + thesis-platform 两份）均补"镜像标注"段落，说明真相源 + 同步规则。
- source_ref 指针**不改写**（保持 `/mnt/d/...` 指向 research-protocol 原始日志）——用户明确"不拷，保持指针回溯"。
- thesis-platform 那边后续若要改蒸馏产物，须回 research-protocol 改完再同步（防分叉）。

### 触发推翻条件
- 若 thesis-platform 要修改蒸馏产物内容 → 必须回 research-protocol 改 + 重新拷贝同步（不得直接改镜像）
- 若原始日志也要自包含到 thesis-platform → 再开决策（需拷 73 源 + 改写全部 source_ref，工作量大）
