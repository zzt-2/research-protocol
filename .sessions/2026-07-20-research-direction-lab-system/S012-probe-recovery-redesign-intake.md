# [S012] Probe 分层与恢复记录体系重设计立项

> 2026-07-21 | 设计、实现与压力测试 | V011 PASS

## 目标

登记下一阶段的明确顺序：先把轻量科学筛选、长期恢复、日志索引和文件组织完整设计出来，经过失败场景推演并固定，再修改 `research-direction-lab` Skill，最后才启动大规模科学运行。

## 记录

真实 SCIENCE_SCOUT 暴露了两个相互关联的问题：

1. 所谓“极小探针”最终经常扩张为合同、全量 cells × seeds、hash/receipt、独立 verifier 和多份治理文档；科学运行只需秒级，治理和实现却占绝大部分时间。
2. 完整可复现链没有阻止错误训练目标被解释成机制负面。旧 V004 能验证数字和来源，却没有用最小反例审查目标函数语义。

因此下一版不能简单继续加硬门，也不能把长期循环再写成复杂 scheduler。设计对象至少包括：

- `Probe → Scout → Deep Evidence` 三层成本与晋级边界；
- 语义门先于证据门：identity/no-harm、常数输出、输出分布、单样本过拟合、简单 comparator 等廉价检查；
- 一个面向恢复的 current projection，只显示当前有效结论、撤回链、下一动作和硬边界；
- 历史 lineage 与当前视图解耦，旧日志不删除但不污染恢复；
- harvest 的当前状态索引，能区分 active / amended / retracted / diagnostic；
- 热路径目录数量上限、批次归档和大 artifact 指针化；
- 在 Skill 修改前，用历史反例和 fresh-agent 恢复场景做 forward simulation；
- 记录成本和科学计算成本分开计量，防止“治理完成”冒充科研推进。

本轮立项时不直接改 Skill、不运行科学实验；设计通过后，用户明确要求由当前对话继续完成实施并给出下一工作提示词。

### 固定后的体系

- 工作强度改为 `Probe → Scout → Deep Evidence`。Probe 只回答一个前置问题，默认只留一份 `probes/<id>/record.yaml`；不默认生成 receipt、verifier、synthesis、session note 或 harvest 条目，结论上限为 DIAGNOSTIC。
- 扩算力前先过科学语义检查：目标/标签/输出/指标对齐、常数或平凡解、no-op/identity、输出支撑、最小过拟合、简单 comparator、因果与信息边界。来源完整只证明证据可信，不证明实验问题有意义。
- 恢复热路径固定为 `STATUS → Project Adapter → state/current → portfolio/current → harvest/current`。显式 `amends/supersedes/invalidates/restores` 关系优先于文件修改时间和旧交接文字；只有冲突、审计或复现时才读 append-only lineage。
- harvest 仍必须逐工作单元评估，但不再强制每轮造条目；没有耐久价值时记录 `no_durable_harvest_reason`。现行索引区分 active/amended/retracted/diagnostic。
- session 只承载用户原话、战略决策、重大失败和跨对话交接；普通 Probe 不再膨胀为 S/D/V/H 全套。
- 通用代码只校验闭合 schema、路径边界、hash/lineage 和项目已明确记录的 disposition；不做候选选择、科学 Go/Kill、固定候选数或调度求解。

### RED → GREEN 推演

- Probe 成本边界：无 Skill fresh agent 为一个 paired-input 问题提出 5 份治理产物；GREEN 只保留一个 compact record，拒绝全量 batch 链。
- 语义/完整性分离：GREEN 能把 artifact integrity PASS 与 objective mismatch 分开，先要求常数解、identity、输出支撑和最小过拟合，不升级候选负面。
- 恢复优先级：GREEN 只读五个热路径入口，按显式 amendment 撤回旧 thesis-grade 解释，同时保留 raw artifact 的可复现价值；不做全历史考古。
- 代码 TDD：state reducer 新增显式 disposition 投影和 STALE 去除 completed 语义；adapter schema 新增可选 current-view 路径；STATUS 优先展示 current harvest 并保留 ledger 指针。

设计与实施说明：

- `docs/superpowers/specs/2026-07-21-direction-lab-probe-recovery-design.md`
- `docs/superpowers/plans/2026-07-21-direction-lab-probe-recovery-plan.md`
- `.agents/skills/research-direction-lab/tests/forward-test-log.md`

### 独立终验修复

独立 verifier 首轮给 `PARTIAL`，发现三项 P1：forward runs 只有摘要、disposition replacement 可悬空、STATUS 仍可消费 raw harvest ledger。修复后第二轮又发现 Scout conditional 与旧 phase/ownership 文案冲突。所有问题均先补 RED/对抗测试再修：

- 保存 blind prompt、agent 标识和逐字 raw response，增加 post-hoc behavior scorer；Probe 与 semantic 均为 RED→GREEN，recovery historical RED 用 H009 精确 SHA 指针。
- reducer 拒绝 dangling、cross-entity、non-current 和 missing replacement；合法 lineage 才能改变 current disposition。
- adapter 声明 `harvest_current` 后，STATUS 强制匹配 `--harvest-current`；inactive harvest 先过滤再截断。
- Scout receipt/verifier 在 phase contract、目录和 ownership 三处统一为 conditional；Deep Evidence 才要求 full chain。

V011 最终独立结论：PASS，P0=0、P1=0、P2=0（限 D013 本轮范围）。

## 决策引用

- D012：大规模运行前，先完成 Probe/恢复/文件体系设计、推演和固定
- D013：正式采用三层工作强度、语义先行和单一当前投影（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。Skill 实施来自用户对 D012 顺序的明确继续授权；没有运行科学实验或改写历史科学证据。

## 后续

体系实现、全局同步和 V011 已完成。下一科学对话读取 H004/T001，从 current view 恢复后用 Probe 低成本扫多个机制分支，只有信号稳定时才升级 Scout/Deep Evidence。
