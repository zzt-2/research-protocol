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

## V003: Phase 3 Task 6–7 与只读使用推演独立终验

> date: 2026-07-20
> 关联：S006 / S007 / D005–D007

### 验证项

- [x] ProjectAdapterV1：递归闭合 schema 子集、缺失/额外/类型负例 → 通过；十个顶层字段齐全。
- [x] 指针与历史保护：repo-relative/contained/exists、disk-byte guards、completion-vs-queue、raw-envelope 分层 → 通过；protected diff 为 0。
- [x] STATUS：真实 CLI、exact render、八问、六轴、三层授权、UTF-8 超长边界 → 通过；58 行 / 4,790 bytes。
- [x] 旧 scheduler 迁移审计：23 functions + 1 property + 4 CLI → 全部覆盖；科研调度均未 KEEP。
- [x] no-scheduler 语义门：候选选择、资源匹配、完整性证明、停止合法性 AST 变异 → 全部拒绝；被动事实展示未误伤。
- [x] 使用推演边界：S007 → 未执行 Task 8、未给行为 PASS、未运行科学实验。

### 证据

```text
python -m pytest .agents/skills/research-direction-lab/tests -q
60 passed, 1 skipped

python -m pytest projects/thesis-fso/direction-lab/tests/test_skill_adapter_v1.py -q
13 passed

Task 6 + Task 7 focused
58 passed, 1 skipped

original Direction Lab baseline
62 passed

render command probe
returncode=0; stdout=4790 bytes; stderr=0
stdout == STATUS.v1.md bytes
LAB file size/mtime map unchanged

portable pointer probes
D:/private/x.py -> REJECT
projects/ok/../escape.py -> REJECT

quick_validate: PASS
compileall: exit 0
YAML parse: 62 files
git diff --check: PASS
domain/scheduler/protected scans: PASS
independent review: P0=0, P1=0, P2=0
```

### 结论

PASS

### 已知证据债

- 沿用 V002：Windows symlink 动态测试因当前权限 skip；POSIX `flock` 分支尚无本机动态覆盖。Phase 3 未改相关路径/锁逻辑，债务未恶化。
- S007 是可理解性/组织推演，不是 Skill 长期行为证据；Task 8 forward tests 与 shadow 尚未执行。

## V004: Task 8 forward-test 独立终验

> date: 2026-07-20
> 关联：S008 / R001 / Task 8

### 验证项

- [x] V-1 prompt 盲性：5 个 blind prompt（HTML 注释存于各 round-1.md 顶部）只含 Skill 指针 + 原始事实 + decision point + artifact sha256 + 7 段输出格式；无 expected answer / ranking / mechanism / scorer keyword / S007 / 跨案例答案泄漏。
- [x] V-2 fixture 完整性：4 个历史 fixture + 非通信 fixture 描述行为天花板（allowed/forbidden_actions 是动词短语，claim_ceiling 是 level + 一句陈述），非固定候选答案；非通信 fixture `artifacts: []` 且无项目指针。
- [x] V-3 fresh-agent 独立性：5 个回答的 "Files read" 段显示每个 agent 只读自己案例的 artifact + Skill（最多一级 reference）；非通信 agent 未读任何项目文件。
- [x] V-4 scorer 公平性：scorer 只检查行为性质和 claim ceiling，从不要求固定候选答案；smoke 测试同时覆盖合成 PASS 和合成 FAIL（false-comparator-promotion 检测）路径。
- [x] V-5 修订纪律：`git diff HEAD -- SKILL.md references/` 为空（零 Skill/reference 编辑）；工作树改动仅限 scorer / fixtures / tests / session 文件。
- [x] V-6 无科学运行：batches/ 只有 B001-B003（无 B004）；5 个回答无任何 run/execute/train 声明；protected history 18/18 hash 一致。
- [x] V-7 全套测试：`pytest skill + 4 project files` = 139 passed, 1 skipped；`quick_validate` = Skill is valid!；`compileall` exit 0；`git diff --check` clean；scorer `--round 1` = verdict PASS / 5 hard gates true / 5 案例 8/8 非 B9 checks pass。
- [x] V-8 领域隔离：`scripts/*.py` 对 BER/SNR/CMA/pilot/OSL/QPSK/Jones 0 命中；scorer（在 tests/ 下）合法包含这些作为检测词。
- [x] V-9 scope 边界：未触 Task 9 shadow、B004、ML 训练、B001-B003/P03 Atlas/canonical state/baseline/receipt 修改、push/merge、把盲测回答写入论文。

### 证据

```text
git status:
 M .agents/skills/research-direction-lab/tests/test_structure.py
?? .agents/skills/research-direction-lab/tests/forward-test-log.md
?? .agents/skills/research-direction-lab/tests/forward/
?? .agents/skills/research-direction-lab/tests/score_forward_tests.py
?? .agents/skills/research-direction-lab/tests/test_forward_fixtures.py
?? .sessions/2026-07-20-research-direction-lab-system/R001-forward-test-design.md
?? .sessions/2026-07-20-research-direction-lab-system/S008-forward-test-round-1.md
(no projects/ changes; SKILL.md and references/ unchanged)

pytest: 139 passed, 1 skipped
quick_validate: Skill is valid!
compileall: exit 0
git diff --check: clean
protected history: protected=18 mismatches=0
scorer --round 1: verdict=PASS; HG1-HG5 all true; 5 cases × 8/8 non-B9 + C5 B9 PASS
B004 check: batches/ has only B001-20260717-live, B002-20260718-live, B003-20260718-live
```

### 结论

PASS。Task 8 round 1 行为证据合法成立。无治理边界被越过。

### 已知证据债

- round 1 PASS 依赖于 scorer 后修正（5+ 处实现 bug + 1 处合法性加固）；当前 scorer 已由 V004 独立复跑确认 PASS，合成 PASS+FAIL smoke 覆盖，债务是过程卫生而非正确性。
- forward test 只覆盖 5 类已注册行为，不构成长期自动化证据；Task 9 shadow 仍未开始，需独立授权。
- B6/B1 fallback 的 legality 现由 forbidden-overlap 守卫保证；若未来出现 forbidden_action 词表外的非法动作，scorer 可能漏检——这是检测器局限，非 round 1 缺陷。
- C4 "update canonical-status" 是 process 簿记，scorer P0/B8 未 scrutinize；当前判定为合法 bookkeeping，但未来若 canonical-status 写入科学结论需另立规则。
