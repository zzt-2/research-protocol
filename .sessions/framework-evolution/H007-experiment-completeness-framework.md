# [H007] 实验完备性框架增强实施

> 来源: R001 | 交接目标: 将调研结论落地为框架文件改动
> 文件名: H007-experiment-completeness-framework.md

## 背景

R001 完成了 5 角度 web 调研 + 6 角度竞品论文实证分析（33 个子 agent，24 篇论文）。核心发现：

1. **不存在 design-level 的实验完备性框架**——所有现有工具都是 reporting-level checklist
2. **领域统计规范性极差**（1.35/5），baseline 合规性差（2.35/5）
3. **可借鉴组件**：GRADE 升降级机制、Walton critical questions、Hermes claim-experiment-evidence 表、NERVE-ML 验证策略匹配、VVUQ 分层结构

已提炼三层框架维度：
- **Tier 1 必做**：多 seed+error bar、baseline 来源/公平调参声明、逐模块消融、信道模型溯源、声称 scope 控制
- **Tier 2 应做**：统计检验、alt-exp 排除、声称-证据审计、跨拓扑验证、复杂度报告
- **Tier 3 加分**：red-teaming、真实数据验证、因果分析、最优解对比、极端条件测试

## 必读（按优先级）

1. `.sessions/framework-evolution/R001-experiment-completeness-research.md` — 完整调研结果
2. `stages/gw-read.md` — 现有精读流程（增加"实验完备性提取"的位置）
3. `stages/contract.md` — Contract 阶段流程（增加"对标检查"的位置）
4. `templates.md` — 文档模板（增加声称-证据映射模板）
5. `stages/gw-feasibility.md` — 可行性评估（检查是否需要联动修改）
6. `stages/execute.md` — Execute 阶段（检查审计层位置）
7. `domain-comms.md` — 通信领域定制（增加通信特有维度检查）
8. `code-quality.md` — 代码质量经验（增加实验代码质量相关条目）
9. `overview.md` — 核心原则（确认改动不违反框架哲学）

## 实施任务

### 任务 1：gw-read.md — 增加"实验完备性提取"维度

在现有"写作架构提取"（H004 引入）旁增加平行的"实验完备性提取"维度。

**具体改动：**
- 在精读模板中增加提取字段：
  - **声称清单**：intro/conclusion 中所有 main claims（编号）
  - **声称→证据映射**：每个 claim 对应的实验/表/图/证明
  - **声称 scope 标注**：bounded（"up to X%"）vs universal（"all/practical"）
  - **统计规范性**：seeds 数、error bar 类型、统计检验、运行次数
  - **Baseline 矩阵**：数量、类型（经典/DL/DRL/启发式/消融）、来源声明、公平调参声明
  - **消融设计**：消融对象、方式（删除/替换/零化）、粒度（逐模块/整块）
  - **通信特有维度**：信道模型类型+参数来源、拓扑多样性、复杂度报告
  - **VVUQ 三层评分**：Verification/Validation/Uncertainty 各 1-3 分
- 提取模板格式参考 R001 中 24 篇论文的分析格式
- **控制篇幅**：模板不超过 30 行，提取结果不超过 20 行/篇

### 任务 2：contract.md — 增加"实验对标检查"步骤

**位置决策依据**（R001 结论）：
- 声称-证据映射应在 **Contract Step 2（起草贡献声明）** 就建立雏形
- 完整的对标检查应在 **Contract Step 5（压力测试）** 执行——此时实验计划已成型

**具体改动：**

#### Step 2 增加输出：声称-证据初步映射
- 格式：Hermes 三列表（Claim | Planned Experiment | Expected Evidence）
- 规则：每个 claimed contribution 必须有对应实验行
- 融入现有贡献声明起草流程，不单独成步

#### Step 5 增加：实验完备性对标检查
- **对标来源**：gw-read 阶段提取的竞品论文实验维度汇总
- **检查清单**（对标 Tier 1 维度）：
  1. 每个 claimed contribution 是否有对应实验？
  2. 声称 scope 是否匹配实验覆盖范围？（scope 控制审计）
  3. 统计规范性：是否计划多 seed + error bar？
  4. Baseline 选择是否合理？是否声明来源和公平调参？
  5. 消融实验是否覆盖每个核心组件？（逐模块，非参数扫描）
  6. 通信特有：信道模型参数是否可溯源？拓扑是否多样？复杂度是否报告？
- **输出**：`experiment_completeness_checklist.md`，每项标注 pass/fail/NA + 说明
- **门控**：Tier 1 项全部 pass 才能 Proceed 到 Execute

### 任务 3：templates.md — 增加实验完备性相关模板

**增加模板：**

#### 模板 A：实验完备性提取模板（gw-read 用）
- 融入现有精读模板，和写作架构提取并列
- 字段如任务 1 所述

#### 模板 B：声称-证据映射表（Contract 用）
```
| Claim | Type (bounded/universal) | Evidence (实验/表/图) | Scope Match |
|-------|-------------------------|---------------------|-------------|
| C1: ... | bounded ("up to X%") | Table 1: 性能对比 | ✅ match |
| C2: ... | universal ("泛化到...") | Fig 3: 仅同类拓扑 | ⚠️ overclaim |
```

#### 模板 C：实验完备性自检清单（Contract Step 5 / Execute 前审计用）
- Tier 1-3 维度的逐项检查表
- 格式：维度 | 要求 | 当前状态 | pass/fail

### 任务 4：domain-comms.md — 增加通信特有实验维度

**增加 §X：实验完备性通信特有维度**

内容：
- 信道模型真实性分级标准（真实/中等/理想化）+ 参数溯源要求
- 拓扑多样性最低要求（≥2 种星座配置或拓扑类型）
- DRL 收敛报告标准（曲线 + 稳定性声明）
- 复杂度报告最低要求（推理延迟或理论 O()）
- 数据来源：R001 角度 5 的通信特有维度覆盖率数据

### 任务 5：execute.md — 增加 Execute 前审计检查点

**位置**：Step 0（开始执行前）

**检查项**：
- Contract 中的声称-证据映射是否已建立
- experiment_completeness_checklist.md 是否 Tier 1 全 pass
- 如有 fail 项，必须修正后才能进入 Step 1

### 任务 6：overview.md — 更新原则索引

在现有原则列表中增加一条索引行：
- "实验完备性对标" → 定义所在：contract.md Step 5；提取模板：templates.md；通信特有：domain-comms.md

### 任务 7：CLAUDE.md — 更新跨阶段护栏索引表

在现有护栏表中增加：
- 实验完备性对标检查 | `contract.md` S5, `templates.md`

## 改动原则

1. **不重复现有内容**：声称-证据映射不与 gw-read 的写作架构提取重复（前者关注叙述，后者关注证据）
2. **不膨胀框架**：每个改动最小化，融入现有步骤而非新增步骤（Step 2 增加输出，Step 5 增加检查项）
3. **数据驱动**：所有检查项均来自 R001 的实证分析，不是拍脑袋
4. **分层设计**：Tier 1 是门控条件（必须 pass），Tier 2-3 是建议（提升质量但不阻塞）

## 不要做什么

- 不创建新的独立阶段或步骤——融入现有流程
- 不在 gw-read 的提取模板中加入过多字段——控制在 20 行/篇以内
- 不修改已有项目的文件——只改框架文件
- 不把 R001 的完整数据复制到框架文件——框架文件只引用结论
- 不在此对话中验证改动效果——改完即可，下一个使用框架的项目验证

## 执行方式

- 按任务 1-7 顺序执行（有依赖：templates 先改，contract 后改引用 templates）
- 每改一个文件，确认不破坏现有内容
- 改完后更新 R001 的"后续"段标注已完成
- 最后更新 topic-index.md
