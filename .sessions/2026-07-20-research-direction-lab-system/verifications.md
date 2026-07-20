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

## V002: Phase 2 Task 4–5 独立终验

> date: 2026-07-20
> 关联：S004 / S005 / D004

### 验证项

- [x] 通用安全工具：完整 Skill tests 与对抗探针 → hash/path/receipt/event/reducer/status 通过；同 head 并发写入恰有一个成功。
- [x] 失败原子性：不存在 ledger + wrong head 聚焦回归 → 抛错后路径仍不存在。
- [x] 历史 replay：逐项对照绑定 report、Git tracking 与 SHA-256 → 四个案例的事实、时间边界和 claim ceiling 合法。
- [x] 通用/项目隔离：禁词、项目路径和科研调度 API 扫描 → 0 命中。
- [x] 历史保护与范围：Git diff 审计 → B001–B003、P03 Atlas、canonical state 无改动；Task 6+ 与科学运行未发生。
- [x] 回归：旧 Direction Lab targeted baseline → 62 passed。

### 证据

```text
python -m pytest .agents/skills/research-direction-lab/tests -q
48 passed, 1 skipped

python -m pytest projects/thesis-fso/direction-lab/tests/test_claim_scope_gate.py projects/thesis-fso/direction-lab/tests/test_state_reducer.py projects/thesis-fso/direction-lab/tests/test_headroom_atlas_gate.py -q
62 passed

PYTHONUTF8=1 python C:/Users/zzt/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/research-direction-lab
Skill is valid!

python -m compileall -q .agents/skills/research-direction-lab
exit 0

git diff --check
exit 0

independent review: P0=0, P1=0, P2=0
```

### 结论

PASS

### 已知证据债

- Windows symlink 动态测试因当前主机权限 skip；实现与测试保留，需在可创建 symlink 的 Windows/POSIX 环境补跑。
- POSIX `flock` 分支在当前 Windows 主机仅完成静态临界区复核；需在 POSIX CI 首次启用前动态验证。
