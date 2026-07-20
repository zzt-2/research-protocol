# Verifications — Research Direction Lab 完整体系设计

## V001: 第一阶段 Task 1–3 独立终验

> 关联：S003 / D001–D003
> date: 2026-07-20
> verdict: PASS

### 验证范围

- U01–U15 来源、依据类别与唯一 Primary owner；
- Skill 结构、渐进披露、项目状态隔离和无 scheduler 重复；
- Communications Profile 与通用 core 的领域隔离；
- ProjectAdapterV1 十个顶层字段、递归闭合对象和无科学调度行为；
- Task 1–3 范围、session 状态一致性和历史研究资产保护。

### 新鲜证据

```text
Task 2 + Task 3 tests: 10 passed
official quick_validate.py (UTF-8): Skill is valid!
original Direction Lab baseline targeted tests: 62 passed
git diff --check: exit 0
U01–U15: 15/15 valid sources; exactly one Primary owner each
Skill: 71 lines; 7 top-level references; 1 allowlisted domain profile
ProjectAdapterV1: 10 exact top-level fields; 11/11 object schemas closed
changed paths: 24 expected, non-ignored paths
```

原始 baseline 命令：

```powershell
python -m pytest projects/thesis-fso/direction-lab/tests/test_claim_scope_gate.py projects/thesis-fso/direction-lab/tests/test_state_reducer.py projects/thesis-fso/direction-lab/tests/test_headroom_atlas_gate.py -q
```

### 结论

Critical、Important、Minor 均无未关闭项。没有修改科学 runner、controller、campaign core、canonical baseline、B001–B003、P03 或历史 receipt；没有运行新科学实验。允许形成一次 Phase 1 consolidated commit。Task 4–10 和 live activation 不在本验证授权内。

### 已知债务

- Windows 默认代码页不能直接读取 UTF-8 Skill，验证命令需 `-X utf8` 或 `PYTHONUTF8=1`；这是环境调用要求，不是 Skill 内容失败。
- 当前环境无可选 `jsonschema` 包；schema 已由 PyYAML 解析、精确字段集和递归闭合测试覆盖，正式消费 adapter 实例前可再加元模式验证。
