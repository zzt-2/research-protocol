# [S003] 第一阶段实现收口

> 2026-07-20 | Task 1–3 实施 | 完成

## 目标

把已认可的 `Skill-first, code-guarded` 蓝图落实为最小可验证实体：需求溯源、一个精简主 Skill、一个通信领域 Profile 和一个闭合 Project Adapter 合同；不进入项目实例迁移或科学实验。

## 记录

### Task 1：需求与责任冻结

- U01–U15 均有来源指针、依据类别和唯一 Primary owner；supporting/storage owner 与主 owner 分开。
- 无独立来源的精确数值全部降为 shadow heuristic；`10%` 退出规则只因直接继承 `AGENTS.md` P2 而保留。
- 首轮独立审查发现多 owner、自指依据和无来源阈值，整改后复审 `APPROVED`。

### Task 2：精简 Skill

- 用官方 initializer 创建 `.agents/skills/research-direction-lab/`。
- 四个无 Skill 压力场景均已正确判断，因此没有把历史案例复制成 if/then scheduler；Skill 聚焦恢复、连续循环、artifact 归位、证据边界、harvest/status 和 reference routing。
- `SKILL.md` 为 71 行；详细内容分为七个顶层 reference，没有 README、CHANGELOG 或平行流程文档。
- 隔离 RED 复现为 `3 failed, 2 passed`；整改后的结构门和官方 validator 均通过，独立复审 `APPROVED`。

### Task 3：领域与项目边界

- `profiles/communications.md` 只保存跨通信项目稳定的信息访问、指标/单位、常见 axes、comparator 合法性、coded/uncoded 与 hard/soft claim 边界和论文贡献形态。
- `project-adapter-schema.yaml` 只定义十个 ProjectAdapterV1 顶层事实字段；所有对象边界递归 `additionalProperties: false`，不含候选排名、slot matching、完备性计数或 next-candidate solver。
- `project-layout.md` 是 Profile/schema 的单一发现入口；没有把领域内容复制到核心 Skill。
- 整改后 Task 2+3 回归为 `10 passed`，官方 validator 通过，独立复审 `APPROVED`。

本阶段没有创建双偏振 OSL 的实际 project adapter，没有迁移历史状态，没有运行 B004、ML、shadow 或任何新科学实验，也没有修改 controller、campaign core、canonical baseline 或 B001–B003/P03 证据。

## 决策引用

- D001：目标体系采用 Skill-first、code-guarded。
- D002：U01–U15 必须有真实来源与唯一 Primary owner。
- D003：本轮只授权 Task 1–3 的隔离实施。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

V001 已独立终验 PASS；下一步完成一次统一提交。Task 4–5（确定性小工具、历史 replay）尚未获本轮实施授权；更未进入 project adapter 实例、shadow 或科学运行。
