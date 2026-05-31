# PROMPT-003: 设计决策提取

> 专题: thesis-writing-prep | 优先级: P1
> 预计: 1-2 个对话完成
> Python: `~/.venvs/torch/bin/python`

## 背景

学位论文在过去 2 周的方向探索中产生了大量技术决策（D001-D014），分散在 thesis-status.md、各 session notes 和专题文件中。需要提取为结构化设计决策文档。

设计决策文档的作用：
1. 写论文时知道"为什么选A不选B"，不用重新找原因
2. 答辩时能回答"为什么不这样做"的问题
3. 防止后续写作中无意识推翻已锁定决策

## 产出

**文件**: `毕设/写作材料/design-decisions.md`（新建）

**每条决策包含**:
1. 决策内容（1句话）
2. 理由（为什么选这个）
3. 否决方案（被否决的替代方案 + 否决原因）
4. 来源（哪个session/导师哪次说的）
5. 强度标签（INVARIANT / DECIDED / TENTATIVE / REJECTED）
6. 状态（LOCKED / SUPERSEDED）

## 必读

### 核心来源（决策密集区）
1. `毕设/写作材料/thesis-status.md` — D001-D014 + 风险清单
2. `.sessions/thesis-direction-pivot/S012-thesis-toc-survey.md` — 目录设计调研
3. `.sessions/2026-05-30-ch3-direction-exploration/S002-ber-closed-form-derivation.md` — Ch3方向推导+验证
4. `.sessions/thesis-direction-pivot/S030-ch4-kf-deep-search.md` — Ch4 KF方向深入检索

### 补充来源（散落决策）
5. `.sessions/thesis-direction-pivot/H004-ch3-mve.md` — Ch3 MVE 设计
6. `.sessions/thesis-direction-pivot/H006-cascade-robustness-mve.md` — 级联鲁棒性
7. `.sessions/thesis-direction-pivot/PROMPT-010-simulation-prototype.md` — 仿真原型设计
8. `.sessions/thesis-simulation-consolidation/PROMPT-002-ch3-ch4-bridge-experiment.md` — 桥接实验设计
9. `毕设/写作材料/TERMS.md` §6.2 — Ch5 目录决策（S012 结论）

### 参考格式
10. 项目根目录下其他 project 的 `decisions.md`（参考格式）

## 子 Agent 策略（自适应）

**不要一开始全定死。** 分阶段推进：

### Phase 1: 探索（2-3 个 agent 并行）

派 2-3 个 agent 分头读核心来源，目标是：
- 搞清楚一共有多少条决策
- 搞清楚决策的分布密度（哪些文件决策密集，哪些只有零散几条）
- 搞清楚决策的粒度差异（方向级 vs 参数级 vs 措辞级）
- 参考其他 project 的 decisions.md 格式

基于 Phase 1 发现，再规划：
- 决策的分类体系（可能不是预设的5类）
- 后续提取需要多少 agent
- 是否需要多轮对话（如果决策量超出预期）

### Phase 2+: 根据发现动态规划

Phase 1 完成后，由主对话决定：
- 提取批次和 agent 数量
- 合并策略
- 写入格式
- 是否需要开第二个对话继续

### Phase 1 agent 建议

**Agent E1**: 读取 thesis-status.md + TERMS.md §6.2，输出：
- D001-D014 的完整列表（含理由和否决方案）
- 风险清单中的隐含决策
- Ch5 目录决策
- 决策总数统计

**Agent E2**: 读取 S002 + S012 + S030 三个核心 session，输出：
- 每个文件中的技术决策、方向判定、否决记录
- 特别注意 S002 的 VV bug 及其连锁影响
- 特别注意 S012 的 v4 vs v5 对比
- 文件中还有哪些决策被 D001-D014 遗漏

**Agent E3**: 找 1-2 个其他 project 的 decisions.md，总结格式参考。浏览补充来源（H004/H006/PROMPT-010/PROMPT-002），评估散落决策量。

## 质量检查

- [ ] 每条决策有明确的否决方案（不是空）
- [ ] REJECTED 决策有否决证据（仿真数据/导师原话/文献结论）
- [ ] LOCKED 决策与 framework 现状一致
- [ ] 无遗漏的重要决策（framework 中有但决策文档中没有）
- [ ] 导师指示类决策标注日期和场合
- [ ] 仿真结论类决策关联具体代码/数据

## 已知关键决策（必须覆盖）

| ID | 内容 | 来源 |
|----|------|------|
| D001 | 方向G（BER闭合解）选为Ch3 | thesis-status |
| D003 | 原Ch3并入Ch2 | 导师指示 |
| D004 | 功率预补偿不独立成章 | S013 WEAK PASS |
| D008 | Ch4→KF统一载波同步 | S030 |
| D013 | Ch4→系统性分析路线 | 导师反馈+代码审查 |
| D014 | KF不作为主贡献 | S002重验 |
| — | VV公式bug修正 | S002 |
| — | 目录v4定稿 | S012+导师确认 |
| — | Ch5删符号定时同步 | TERMS.md §6.2 |
| — | ω_n单位rad/s | 代码验证 |
| — | 防御性写作策略 | R003 |

## 不要做什么

- 不修改 thesis-status.md / thesis-framework.md
- 不做新的技术决策（只提取已有决策）
- 不写论文正文
- 不评判决策正确性（只记录）
- 不在一开始就定死所有子 agent（Phase 1 先探索）
