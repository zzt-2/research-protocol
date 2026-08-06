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

## V005: Task 9 live shadow 独立终验

> date: 2026-07-20
> 关联：S009 / D008 / Plan Task 9 Step 4

### 验证项（11 项，全部独立复核）

- [x] V-1 worktree 隔离 + 父 worktree 保护：shadow 分支从 f79cb1b 派生；research-direction-lab-system 父 worktree clean，HEAD 不变；main + p03 + unified-batch-runner 均未触动。
- [x] V-2 protected history 18/18 hash 匹配：独立重算 SHA-256 全部与 adapter identity_digest 一致（含 baseline + shared channel）。
- [x] V-3 B004 不存在：batches/ 只含 B001/B002/B003。
- [x] V-4 无新科学计算：git diff 只在 .sessions/、shadow/、STATUS.v1.md、_registry.yaml；无 B004、无 completion-events.jsonl 改动、无 raw artifact 改动。
- [x] V-5 全套测试：pytest 77 passed + 1 skipped；quick_validate PASS；compileall exit 0；STATUS.v1.md 确认 LF（CRLF=0），renderer 测试 PASS。
- [x] V-6 通用 Skill/code 领域中立：SKILL.md / scripts/ / references/（除 profiles/communications.md）对 BER/SNR/CMA/pilot/OSL/QPSK/Jones 0 命中。
- [x] V-7 无 scheduler 回潮：test_no_scheduler_contract.py 8 passed；science_slots/completeness_solver/resource_match/fixed_min_batch grep 0 命中。
- [x] V-8 五类行为证据：OBS-BLOCK（6 真实 blockers 含 repair_condition）；OBS-ROTATE（R1-R5 完整 trace，100% 续跑率）；OBS-SCOPE（所有 SHADOW-H010..H017 ceiling ∈ {CONTRACT, SLICE}，0 DOMAIN/FAMILY）；OBS-HARVEST（8 entries 抽 3 条 verbatim quote 核对 PASS）；OBS-RECOVER（session 启动恢复文档化 + 3 handoff 事实 PASS）。
- [x] V-9 PASS 标准（Plan Task 9 Step 4，verbatim 8 条）：全部 PASS（详见 verifier 报告 V-9 表）。
- [x] V-10 scope 边界：未触 AGENTS.md/process.md/README/method-family-batch-exploration SKILL.md/B001-B003/canonical-state/completion-events/baseline/receipts；shadow/harvest-derived.v1.yaml 全部 promotion_block=not yet promoted；main ledger 仍只含 H001-H009。
- [x] V-11 反模式审计：未加 scheduler patch；未宣称长期可靠；未把 shadow 数字写入论文；未 push/merge（git rev-list f79cb1b..HEAD = 0，未提交）。

### 证据

```text
git rev-parse HEAD: f79cb1bc77ad1a20fb0b8334be6dac19124f214c
git rev-parse --abbrev-ref HEAD: codex/research-direction-lab-shadow
parent worktree (research-direction-lab-system) git status: clean, HEAD f79cb1b
worktree list: 4 worktrees, shadow 是新增的，其他 3 个未受影响

pytest: 77 passed, 1 skipped
quick_validate: Skill is valid!
compileall: exit 0
STATUS.v1.md: 58 lines, CRLF=0, LF=58, bytes=4790 (renderer output, matches HEAD blob)

protected history hashes: 18/18 + baseline + channel all match adapter
domain grep outside profile/tests: 0 hits
scheduler grep: 0 hits; test_no_scheduler_contract: 8 passed

shadow/harvest-derived.v1.yaml: 8 entries, all promotion_block=not yet promoted
main ledger.v1.yaml: H001-H009 only (no leak)

git diff --stat: only .sessions/ + STATUS.v1.md
git rev-list f79cb1b..HEAD: 0 (uncommitted, single consolidated commit pending)
```

### 结论

PASS。Task 9 live shadow 行为证据合法成立，无治理边界被越过。Task 10 cutover 获授权推进。

### 已知证据债

- _registry.yaml 行尾正常化（Windows autocrlf 环境产物，与 STATUS CRLF debt 同类）：pre-existing，非阻塞，Task 10 cutover 时可一并清理。
- canonical-state 内部 stale self-checksums（event_log_sha256 / simulator.sha256）：pre-existing，FC caveat 1-2 已记录。
- canonical-state.last_completed_batch pointer 仍指 B002：pre-existing process debt，B003 verifier-report 已自文档化。
- B6/B1 fallback 词表外局限：V004 已知债务，shadow 范围外。

## V006: Task 10 cutover 独立终验

> date: 2026-07-20
> 关联：S010 / D008 / Plan Task 10 Step 1-5
> Live-activation decision: authorized

### 验证项（11 项，全部独立复核）

- [x] T-1 V005 前置：verifications.md V005 verdict=PASS，Task 10 推进合法。
- [x] T-2 cutover deliverables：AGENTS.md FR-27 单行路由（指向 Skill 唯一拥有者）；process.md 加 SUPERSEDED 头 + 进入入口段（DL-Process v0.4 历史内容保留）；README.md 加流程入口段；method-family-batch-exploration SKILL.md 加 superseded frontmatter（保留原文）；docs/architecture/research-direction-lab.md doc-steward 锚定 13 个真实路径。
- [x] T-3 未复制 Skill 内容：FR-27 单行；process.md/README 仅 pointer list；architecture doc 无 phase contract 复制。
- [x] T-4 FR-22 vs Direction Lab 冲突解决：AGENTS.md / process.md / README.md / architecture doc 四处一致声明 Direction Lab 是晋级前候选发现层 + 晋级仍必须走 GW/Contract/Execute。
- [x] T-5 全套测试：pytest 77 passed + 1 skipped；quick_validate PASS；compileall exit 0。
- [x] T-6 owner/terminology scans：通用 Skill/scripts/references（除 profiles/communications.md）对领域词 0 命中；test_no_scheduler_contract 8 passed；test_domain_separation 5 passed；唯一 process owner（method-family-batch-exploration 已 SUPERSEDED）。
- [x] T-7 protected history + scope：18 protected + baseline + channel 全部 hash 匹配；git diff 只在授权路径（AGENTS.md/process.md/README.md/STATUS.v1.md/.sessions/docs/architecture/shadow）；无 B004、无 canonical-state/completion-events/baseline 改动；main ledger 仍只 H001-H009；STATUS.v1.md LF 4790 bytes。
- [x] T-8 architecture doc 真实：13 个 owner path 全部存在；V001-V005 表与 verifications.md 一致；superseded artifacts 关系表与实际文件一致。
- [x] T-9 V006 recordable：本条目满足 PASS/PARTIAL/FAIL + 命令 + 输出 + 已知债务 + live-activation 决策字段。
- [x] T-10 无 push/merge：git rev-list f79cb1b..HEAD = 0（未提交）；git branch -r 只 origin/main。
- [x] T-11 反模式审计：未加 scheduler；未复制 Skill；未改 protected history；旧 Skill 保留历史（未删）；shadow 数字未进论文材料。

### 证据

```text
verifications.md V005 verdict: PASS（precondition）

AGENTS.md FR-27 row: line 190，单行，指向 .agents/skills/research-direction-lab/SKILL.md
process.md: line 5 SUPERSEDED 头 + line 9-18 进入入口段；DL-Process v0.4 §1-9 历史内容保留
README.md: line 5-15 流程入口段；旧"当前状态"段保留
method-family-batch-exploration SKILL.md: frontmatter superseded_by/superseded_date/superseded_evidence；SUPERSEDED 头注；原文保留
docs/architecture/research-direction-lab.md: 81 行，13 个 owner path 全部存在，V001-V005 表一致

pytest: 77 passed, 1 skipped
quick_validate: Skill is valid!
compileall: exit 0
domain grep outside profile/tests: 0 hits
test_no_scheduler_contract: 8 passed
test_domain_separation: 5 passed

protected history: 18 protected + baseline + channel = 20/20 match
git status: AGENTS.md / process.md / README.md / STATUS.v1.md / .sessions/ / docs/architecture/ / shadow/ only
batches/: B001/B002/B003 only (no B004)
ledger.v1.yaml: H001-H009 only
STATUS.v1.md: 4790 bytes / 58 LF / 0 CRLF

git rev-list f79cb1b..HEAD: 0 (uncommitted)
git branch -r: origin/main only (no shadow on remote)
```

### 结论

PASS。Task 10 cutover 全部 deliverable 合规，FR-22 vs Direction Lab 冲突已解决，Skill 内容未被复制，旧 Skill 已标 superseded 但保留历史，protected history 完整，scope 边界守住。**Live-activation authorized**。

### 已知证据债

- canonical-state 内部 stale self-checksums（event_log_sha256 / simulator.sha256）：pre-existing，FC caveat 1-2；正式激活前清理。
- canonical-state.last_completed_batch pointer 仍指 B002：pre-existing process debt，B003 verifier-report 已自文档化。
- Windows symlink / POSIX flock 动态测试覆盖（V002/V003 debt）：跨平台 CI 前补跑。
- forward-test scorer B6/B1 词表外局限（V004 debt）：检测器局限。
- STATUS.v1.md / _registry.yaml Windows autocrlf 行尾脆弱性：pre-existing，STATUS 在本 worktree 已确认 LF-clean（0 CRLF）。
- runner.direction_lab.b003.snapshot RETIRED snapshot digest stale：有意 out-of-guard（V005 已记录"18/18 + baseline + channel all match"）。

## V007: 消费者部署收口独立终验

> date: 2026-07-20
> 关联：S011 / D009 / 用户 2026-07-20 执行提示词 §七
> verifier 上下文: 独立 subagent（与实现分离）
> FINAL VERDICT: PASS（11/11）
> Deployment status authorized label: **DEPLOYED**

### 验证项（11 项，全部独立复核）

- [x] V-1 普通消费者能发现新 Skill：`C:\Users\zzt\.agents\skills\` 下 `research-direction-lab/` 与其他 skills 并列；integration worktree `.agents/skills/research-direction-lab/` 存在。
- [x] V-2 新 Skill 不再只存在于 shadow worktree：`git worktree list` 含 integration worktree HEAD `6ca142e` + shadow worktree HEAD `6ca142e`；Skill dir 在 integration worktree 内可达。
- [x] V-3 旧 Skill 没有悬空 superseded 指针：`method-family-batch-exploration/SKILL.md` frontmatter 含 `superseded_by: research-direction-lab`，目标 `C:\Users\zzt\.agents\skills\research-direction-lab\SKILL.md` 存在。
- [x] V-4 integration branch 包含 Task 1–10 完整资产：`git log cfb29f0..HEAD` 链 cfb29f0 → 61b623d → e2f42e8 → f79cb1b → 6ca142e 完整；`.agents/skills/research-direction-lab/` 下 36 文件。
- [x] V-5 dirty 普通根目录没有被修改：普通根 HEAD 仍 `97473a2184c72e3246db2a4053b962c0b36ed1dd`；dirty 文件 52 个保持不动。
- [x] V-6 B004 不存在：batches/ 只含 B001-20260717-live / B002-20260718-live / B003-20260718-live。
- [x] V-7 没有科学实验：integration worktree git status 只含 S011/D009/voice/topic-index 新增 + STATUS.v1.md renderer 重渲染；无 batch artifacts、无 completion-events、无 canonical-state 科学字段改动。
- [x] V-8 protected history 未变：18 文件 SHA-256 全部独立重算并匹配 foundation-certificate.v1.yaml（0 mismatch）。
- [x] V-9 通信和非通信 smoke 均通过：通用 Skill/code（SKILL.md + 8 references 除 profiles/communications.md + scripts/*.py + agents/openai.yaml）扫描 `CMA|BER|SNR|QPSK|OSL|Jones|pilot` = 0 命中；非通信 fixture `non-comms-baseline-extension.yaml` 存在且 `artifacts: []`。
- [x] V-10 FR-22/FR-27 没有冲突：AGENTS.md FR-27（line 190）明确写"Direction Lab 是正式晋级前的候选发现/批量筛选层，不等于 GW 完成"+"正式候选晋级后仍必须走 Groundwork → Contract → Execute（继续遵守 FR-22）"；AGENTS.md 只保留 FR-27 单行路由索引，无 Skill 内容复制。
- [x] V-11 所有定向测试和 quick_validate 通过：
  - `pytest skill tests + 4 project files` = **139 passed, 1 skipped**
  - `compileall` exit 0
  - `quick_validate`（integration worktree）= Skill is valid!
  - `quick_validate`（global install）= Skill is valid!
  - 36 文件 sha256 hash 全等（integration vs global install，0 mismatch）
  - STATUS.v1.md = 4790 bytes / LF-only（与 V006 anchor 一致）

### 证据

```text
git worktree list:
  D:/code/study/research-protocol                                               97473a2 [feat/title-consistency-check]
  D:/code/study/research-protocol/.worktrees/p03-residual-headroom              29b330c [codex/p03-residual-headroom]
  D:/code/study/research-protocol/.worktrees/research-direction-lab-integration 6ca142e [codex/research-direction-lab-integration]
  D:/code/study/research-protocol/.worktrees/research-direction-lab-shadow      6ca142e [codex/research-direction-lab-shadow]
  D:/code/study/research-protocol/.worktrees/research-direction-lab-system      f79cb1b [codex/research-direction-lab-system]
  D:/code/study/research-protocol/.worktrees/unified-batch-runner              65db35b [codex/unified-batch-runner]

git -C D:/code/study/research-protocol rev-parse HEAD: 97473a2184c72e3246db2a4053b962c0b36ed1dd
git -C D:/code/study/research-protocol status --short | wc -l: 52

git -C .../research-direction-lab-integration log --oneline cfb29f0..HEAD:
  6ca142e feat(research-direction-lab): Task 9 shadow + Task 10 cutover (V005/V006 PASS)
  f79cb1b feat(research-direction-lab): Task 8 forward-test round 1 PASS
  e2f42e8 Add read-only Direction Lab project projection
  61b623d Add Direction Lab safety tools and replay fixtures

git -C .../research-direction-lab-integration status --short:
 M .sessions/2026-07-20-research-direction-lab-system/decisions.md
 M .sessions/2026-07-20-research-direction-lab-system/topic-index.md
 M .sessions/2026-07-20-research-direction-lab-system/voice.md
 M projects/thesis-fso/direction-lab/STATUS.v1.md
?? .sessions/2026-07-20-research-direction-lab-system/S011-consumer-deployment-cutover.md

pytest: 139 passed, 1 skipped
compileall: exit 0
quick_validate (integration): Skill is valid!
quick_validate (global install): Skill is valid!
hash compare 36 Skill files: checked=36 mismatches=0
STATUS.v1.md: 4790 bytes LF-only

protected history SHA-256 independent recompute: 18/18 match (0 mismatch)
communications scan in generic Skill/code: 0 hits
non-comms fixture present, artifacts: []
```

### 结论

PASS（11/11）。消费者部署断链已修复，integration worktree + 全局 Skill 安装 + 悬空 superseded 指针消除 + dirty 普通根目录保护 + protected history 未变 + B004 absence + FR-22/FR-27 边界 + 通用/领域隔离全部验证通过。**Deployment status authorized label: DEPLOYED**。

### 已知证据债（沿用 V005/V006 + 本轮新增）

- canonical-state 内部 stale self-checksums（event_log_sha256 / simulator.sha256）：pre-existing，FC caveat 1-2；正式激活前清理。
- canonical-state.last_completed_batch pointer 仍指 B002：pre-existing process debt，B003 verifier-report 已自文档化。
- Windows symlink / POSIX flock 动态测试覆盖（V002/V003 debt）：跨平台 CI 前补跑。
- forward-test scorer B6/B1 词表外局限（V004 debt）：检测器局限。
- STATUS.v1.md Windows autocrlf 行尾脆弱性：pre-existing；本轮 renderer 重渲染保持当前 copy LF-clean，但跨 worktree checkout 时仍可能被 autocrlf 转 CRLF——长期修复需要在 .gitattributes 显式声明 `text=auto eol=lf` 或类似策略（非阻塞，不属本轮范围）。
- dirty 普通根目录 `_registry.yaml` 仍停在 `S001/D001` 旧描述：用户工作目录改动，本轮按授权不动；用户若把普通根并入 integration 分支时需要手动 reconcile（建议直接以 integration 分支为准）。
- dirty 普通根目录 `canonical-state.yaml` 已与 shadow 版本对齐（之前已被同步过）：用户工作目录改动，本轮按授权不动。
- 全局 Skill 安装无 git 跟踪：安装元数据记录在 S011/D009/V007；新机器/克隆需重新安装。

## V008: 务实 baseline 充分性 Skill 修订独立终验

> date: 2026-07-20
> 关联：S011 续接 / D010 / 科学专题 D005-H002
> verifier 上下文：独立 subagent，与实现和 RED/GREEN agents 分离
> FINAL VERDICT: PASS

### 验证项

- [x] RED/ GREEN 文件包含相同 blind prompt、fresh-agent 标识和完整逐字回答。
- [x] 独立 scorer 只解析封闭的 `## Raw response` 区段；RED=`FAIL`，GREEN=`PASS`（6/6）。
- [x] Skill 全套测试：`67 passed, 1 skipped`；skip 为 Windows symlink 环境限制。
- [x] UTF-8 `quick_validate.py`：`Skill is valid!`。
- [x] `git diff --check`：exit 0，仅 Windows LF→CRLF 提示。
- [x] 通用 core 无具体通信项目术语；领域解释仍位于 Communications Profile。
- [x] baseline 原则满足：不默认要求 SOTA；必须正确、任务适配、广泛采用、公平且足以支撑有限主张；有明确停止条件。
- [x] `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 前不授权 ML/new-method Scout；baseline 裁决期间 Portfolio 可继续。
- [x] 治理血缘一致：D010 → 科学 D005 → D004 superseded → H001 superseded → H002 唯一续接入口。
- [x] `_registry.yaml` 两个专题已同步更新并通过 YAML 解析。

### 结论

PASS。此前首轮 verifier 的 P1（无逐字行为证据/可执行 scorer）和 P2（注册表落后）均已关闭；未发现残留 P0/P1/P2。允许同步全局消费者 Skill，并从 H002 开启下一正式研究对话。

## V009: baseline 修订全局消费者同步复核

> date: 2026-07-20
> 关联：V008 / D010
> verifier 上下文：独立 subagent
> FINAL VERDICT: PASS（部署通过）

### 证据

- repo source 与 `C:/Users/zzt/.agents/skills/research-direction-lab/`：42 个非缓存文件路径集合一致，SHA256 mismatch=0。
- 全局 `quick_validate.py`：PASS。
- 全局可移植结构/forward/domain 测试：`17 passed`。
- repo worktree Skill 全套：`67 passed, 1 skipped`。
- 全局路径直接跑全套：`64 passed, 3 failed, 1 skipped`；3 项均为 `EXPECTED_REPO_CONTEXT_FAILURE`，同三项在 repo worktree 为 `3 passed`。

### 失败边界

全局 3 项失败来自测试按 Skill 文件位置反推 research-protocol 仓库根：历史 replay artifact 和 `control-migration-audit.md` 在 canonical repo 中存在，但全局安装位置不包含项目 artifacts。它们不涉及 Skill 内容、hash、forward gate、行为规则或领域隔离，因此不阻断部署；不得把全局全套宣称为全绿。

### 结论

PASS。全局消费者 Skill 已与 repo 验证版本字节一致且可发现。非阻断 P2：未来可给 3 项 source-integration tests 增加 `repo_context` marker 或显式 repo-root 参数。

## V010: 两层 baseline 公平性与有界候选扩图独立终验

> date: 2026-07-21
> 关联：S011 续接 / D011 / science-scout D007-H004
> verifier 上下文：独立 subagent，与实现和 GREEN agent 分离
> FINAL VERDICT: PASS

### 验证项

- [x] 共同系统锚点与任务专属 comparator 已分离；不同 detection/control/correction 主张不再机械共用同一列表。
- [x] 公平性明确为 `equal tuning opportunity`，不是强制 identical hyperparameters；信息、验证、收敛和 held-out 冻结边界均保留。
- [x] 候选过窄时触发 bounded mechanism-level refresh；明确不设固定全局数量、不要求实现全池，随后立即进入小型 `READY` 批次。
- [x] readiness 使用 `READY / NEEDS_SMALL_ADAPTER / INFRASTRUCTURE_BLOCKED / HYPOTHESIS_ONLY`，共享输入或代码复用不能冒充 runnable。
- [x] detector observability 与 downstream system gain 明确分开。
- [x] 真实 RED artifact 被 scorer 判 `FAIL`，fresh-agent GREEN 判 `PASS`；P1 行为回归缺口关闭。
- [x] 通用 Skill、全部通用 references 与 scripts 的 domain-neutral test 通过；`receiver` 已移入领域 Profile 语义，P2 关闭。
- [x] Skill 全套：`71 passed, 1 skipped`；UTF-8 quick_validate PASS；compileall PASS；git diff-check exit 0。
- [x] 全局消费者同步：46 个非缓存文件，missing=0、extra=0、SHA256 mismatch=0；全局定向 tests `16 passed`，quick_validate PASS。

### 已知非本轮失败

Skill + 4 个项目文件组合回归为 `145 passed, 1 failed, 1 skipped`。唯一失败是未修改 `STATUS.v1.md` 的 Windows checkout CRLF 与 renderer LF 不一致；该文件不在本轮 diff，属于既有行尾债务。因此本轮 Skill 修订 PASS，但不得宣称组合套件全绿。

### 结论

PASS。两项真实失效已由最小 Skill/reference 修订、fresh-agent 行为证据、自动 scorer 和独立复验闭合；未引入 scheduler、固定候选数量、全池实现义务或通信项目语义。

## V011: Probe 分层、current view 与抗膨胀记录体系独立终验

> date: 2026-07-21
> 关联：S012 / D013 / T001
> verifier 上下文：独立 subagent；只审查、未参与实现
> FINAL VERDICT: PASS

### 验证历程

首轮为 PARTIAL（P0=0、P1=3、P2=1）：forward evidence 只有摘要；disposition replacement 可悬空/跨实体；STATUS 未强制 current harvest。修复后复验又发现两处旧文案仍无条件要求 Scout receipt/verifier。最终修复全部四类问题，并用结构、行为、对抗和端到端测试闭合。

### 最终证据

- Probe 默认一个 compact record；无 receipt/verifier/synthesis/session/强制 harvest；PASS 仅 DIAGNOSTIC。
- semantic smoke 先于 integrity/扩算力；integrity PASS 明确不等于 scientific validity。
- verbatim fresh-agent 行为：Probe RED FAIL→GREEN PASS；semantic partial RED FAIL→GREEN PASS；recovery GREEN PASS；post-hoc scorer 实际执行。
- recovery historical RED：H009 SHA256 `61ea49edeb8fb6c7cd1ac1278e47775c9f17616357478f520d9267ff51c5041b` 与磁盘完全一致。
- reducer 四类非法 replacement（dangling/cross-entity/non-current/missing）均拒绝；合法 CLOSED→INVALIDATED→UNRESOLVED 投影通过。
- adapter 声明 `harvest_current` 时 legacy `--harvest` 被拒；匹配 `--harvest-current` 通过；inactive harvest 先过滤后截断。
- Scout receipt/verifier 在 core phase contract 与 layout ownership 中均为 conditional；Deep Evidence full chain required；旧无条件串有测试禁止回归。
- 完整 Skill：`90 passed, 1 skipped`；skip 为既有 Windows symlink 环境限制。
- UTF-8 quick validation：`Skill is valid!`；compileall exit 0；git diff-check exit 0。
- repo/global 非缓存 Skill 文件：56/56，SHA256 difference=0；全局可移植测试 `30 passed`。
- 通用核心未引入通信项目语义、固定候选数、science slots、scheduler 或科学选择。

### 范围外既有债务

项目实例组合测试仍有一项 STATUS LF/CRLF 字节差异；这是既有 Windows checkout 行尾债务，不是 D013 Skill 逻辑失败，不计入本轮 P2。

### 结论

PASS。D013 本轮范围内 P0=0、P1=0、P2=0。允许从 H004/T001 启动新的连续科学 campaign；本验证不代表长期自动运行永不偏离，也不把任何 Scout 结果自动晋级论文。

## V012: 方法生产 v2 与三层长程记录独立终验

> date: 2026-07-26
> 关联：D018 / phase-1 audit `4af6f9d..aab425d`
> verifier 上下文：独立只读 subagent，未参与实现
> FINAL VERDICT: PASS

### 验证项

- [x] 正向方法合同与 formal science disposition / mission method delta 分账。
- [x] `topic-index.md`、固定 `mission-log.md`、T/worker-log/artifact 三层记录成立。
- [x] 每轮回看原始 mission 与整链，并检查同轴、repair、no-method、UNDERWEIGHT。
- [x] 未新增 scheduler、controller、评分器、固定包数或日常 S 流水账。
- [x] v1 control 向后兼容；v2 task 绑定 epoch 与 mission checkpoint。
- [x] phase-1 科学结论与 `projects/` 科学产物未改，且未创建 T008。
- [x] C15 只作为 phase-2 推荐入口；当前 control 仍禁止科学实验。

### 初审 P2 与关闭

- CP001–CP007 初版缺 worker-log/commit 指针：已补 `log-NNN` 与 commit，并给出 artifact 下钻规则。
- registry 初版仍写 epoch 10：已同步为 epoch 11 / `PHASE2_ENTRY_SELECTION`。

### 结论

PASS。P0=0、P1=0、P2=0。本验证只证明 v2 实现与 phase-2 入口控制一致，不宣称长程方法生产已被真实运行证明。

## V013: T001–T026 审计后的 RDL v2.1 最小修订独立终验

> date: 2026-07-29
> 关联：D019 / live R009 / live D034 / CP025
> verifier 上下文：独立只读 subagent，未参与实现
> FINAL VERDICT: PASS

### 验证项

- [x] 恢复三问只检查下一动作与 streak 路由，不新增 scheduler/controller。
- [x] `READY=0 / NEEDS_SMALL_ADAPTER=0` 时工厂/战略 gate 为硬路由，不再串行 formalize hypothesis-only candidate。
- [x] accepted `METHOD_SIGNAL` 后 promotion preflight 只产生 bounded workline、harvest 或 strategic gate；setup incident 不计 accepted checkpoint。
- [x] recovery receipt 只在真实压缩/fork/主控替换时记录，不进入普通包。
- [x] live `topic-index.md` 保留逐字冻结原目标、当前 control、范围和不变量；package history 仍由 mission-log、D/V、worker-log 恢复。
- [x] T026 正确登记 CP025：`mission_method_delta=NONE / artifact=WRITING_MATERIAL / active-carrier=0`，G1 claim ceiling 未升级。
- [x] system control 已从 stale D018 修到 D019；live/system scope、voice、registry 与 R009 一致。

### 初审 P1 与关闭

- live frozen goal 曾被瘦身改写：已恢复“T 路径和四项完成索引”“fork 主控”“原 system design”逐字原文。
- system control 曾仍指向 D018/等待 phase 2：已递增 epoch、指向 D019 并绑定 v2.1 实施/验证/同步。

### 验证证据

- repo Skill：`102 passed, 1 skipped`。
- `quick_validate.py`：PASS。
- system/live control YAML 与 registry YAML：PASS；`git diff --check`：PASS。
- repo→个人 Skill：60 个非缓存文件 SHA256 全等。
- 个人 Skill quick validation：PASS；全套 `99 passed, 1 skipped`，另 3 项为既有 repo-context 测试在个人目录缺项目 artifacts 的预期 failure，同项在 canonical repo 全部 PASS。

### 结论

PASS。P0=0、P1=0、P2=0。v2.1 可部署并进入下一轮 live-test 入口选择；本验证不宣称已经产生 formal thesis method。

## V014: 三类 Skill 最小 patch 与历史回归独立终验

> date: 2026-08-02
> 关联：R004 / D020 / H003
> verifier 上下文：独立 fresh-context subagent；只读审查，未参与实现
> FINAL VERDICT: PASS

### 验证项

- [x] 三类 patch：五门 executable semantic contract、三层 contribution tiers、三层 lightweight persistence 均进入既有 owner，无第四类规则。
- [x] 六案行为：scale/action、hidden truth、real action/cost、局部 Probe、parameter injection/cluster、negative/partial packaging 均按行为通过；真实 B 级工程组件保留入口且不制造 P12。
- [x] 回归身份：RED 固定 Git object 与可复算 bundle；六对同 prompt、`fork_turns=none`、独立 agent/output provenance；受 later marker 污染的两次尝试废弃后由 clean agent 重跑。
- [x] receipt fail-close：空 contract、空 source、空 mapping、非空组但零 seed、hash mismatch 均拒绝；非空 seed 正常。
- [x] 静态与消费者：全套测试、双端 quick validation、canonical/runtime 全文件 hash、YAML/reference/diff/pollution 检查通过。
- [x] 范围：未启动 AMC/科学仿真，未修改 P07–P11/G1 科学资产、formal owner 或其他 Skill；dormant longitudinal topic 未回写。

### 证据

```text
pytest .agents/skills/research-direction-lab/tests -q
110 passed, 1 skipped in 2.27s

quick_validate.py canonical
Skill is valid!

quick_validate.py runtime
Skill is valid!

canonical/runtime non-cache comparison
canonical=94 runtime=94 only_canonical=0 only_runtime=0 mismatch=0

reproducible RED baseline
commit=53085bb5d1b7cc3e759e62af5c55397979402acc
files=60
bundle_sha256=fbd44ac762114e54f2f6fae90226487ff0748a43c1fa6e8ba57ff9b521274a87

independent verifier final
P0=0 P1=0 P2=0
verdict=PASS; allow V014 PASS and unified commit

git diff --check
exit=0
```

### 结论

PASS。D020 三类最小 patch、六案可审计 RED/GREEN、receipt 边界与个人 Skill 同步全部闭合，P0=0、P1=0、P2=0。该结论不改变既有科学 verdict，不代表产生了新的 thesis method，也不授权在本轮启动 AMC。

## V015: 论文方法章保留门最小修订独立终验

> date: 2026-08-03
> 关联：R005 / S015 / D021 / T002 / T003
> verifier 上下文：独立只读 subagent；未参与 Skill 实施或行为样本生成
> FINAL VERDICT: PASS

### 验证项

- [x] 科学主方法门、`METHOD_SIGNAL`、active scientific carrier 与 formal promotion 标准未降低。
- [x] 每个 evidence-valid accepted package 都必须另做 `THESIS_METHOD_READY / NEEDS_ONE_BOUNDED_PACKAGE / SUPPORTING_ONLY / REJECT` 判定。
- [x] 混合包按可分离 real-action lineage 裁决；一个候选被传统方案吸收不抹掉另一条独立动作链。
- [x] `NEEDS_ONE_BOUNDED_PACKAGE` 只允许一个决定性闭包，失败即降级，不形成无限包装链。
- [x] invalidated、unauthorized、privileged 或 artifact 证据只能 `REJECT`，不得借包装门复活。
- [x] 确定性 RED receipt 含修改前 commit/blob identity 与失败摘录。
- [x] GREEN prompt 不含评分答案；scorer 独立；2/2 fresh-context 原始响应均自动保留 adapter，保持 `METHOD_SIGNAL=0`、active carrier=0，并优先唯一 bounded closure。
- [x] D021 明确为 D020 的局部扩展，D020 其余三类契约继续 active。
- [x] T002/T003 为只读包装诊断，task-control 与前台 epoch/action class 一致。

### 验证证据

```text
pytest .agents/skills/research-direction-lab/tests -q
111 passed, 1 skipped

quick_validate.py canonical/runtime
Skill is valid! / Skill is valid!

canonical/runtime non-cache comparison
canonical=99 runtime=99 only_canonical=0 only_runtime=0 mismatch=0

validate_task_control.py T002 / T003
PASS / PASS

independent verifier final
PASS; P0=0 P1=0 P2=0
```

### 结论

PASS。D021 的轻量论文方法章保留门、可审计 RED/GREEN、个人运行副本和两个只读任务入口均闭合。该结论只证明可包装内核不会因 `METHOD_SIGNAL=0` 被自动丢弃；不证明 2A/2B 已成为论文方法，也不授权运行实验。

## V016: 2A/2B bounded closure 任务书独立终验

> date: 2026-08-03
> 关联：S015 / D022 / T004 / T005
> verifier 上下文：独立只读 subagent；未参与任务书设计
> FINAL VERDICT: PASS

### 验证项

- [x] D022 的授权原话真实，且只保证可信闭环，不承诺正面结果。
- [x] epoch 11、`THESIS_BOUNDED_PACKAGE_EXECUTION` 与 topic foreground control 一致；T004/T005 validator 均 PASS。
- [x] 每个任务仅一个 package、最多一次确定性 repair，并强制闭合到四类 terminal disposition。
- [x] T004 以 strongest static region retune 为 Go comparator，并用 shuffled/global-mean 消融验证 current information 是否 load-bearing。
- [x] T005 分开裁决 single-branch scheduling 与 Q(8,6) 子链；Q 子链失败不会抹掉已闭合的 scheduling action lineage。
- [x] T005 计完整 caller path，禁止先跑双支后少记成本；headline timing 有并发隔离、稳定阈值和 6 次/45 分钟有限边界。
- [x] 两任务只写各自 sandbox/results/worker-log/harvest/usage fragment，不并发修改共享月志、system topic、common/params 或 formal owner。
- [x] 越界终态统一为 `EXTERNAL_BLOCKED(reason=...)`，不存在隐式“再跑一轮”出口。

### 验证证据

```text
validate_task_control.py T004 / T005
PASS / PASS

independent verifier initial
PARTIAL; P0=0 P1=2 P2=2

after deterministic task-contract repair
PASS; P0=0 P1=0 P2=0

git diff --check
PASS
```

### 结论

PASS。T004/T005 可分别派入隔离 worktree 并自主运行到可信终态。该结论证明任务合同可执行、正负结果均可用；不预判任一 package 将获得 `THESIS_METHOD_READY`。

## V017: 轻量方法构造双车道设计独立终验

> date: 2026-08-04
> 关联：R006 / D023 / CP001
> verifier 上下文：独立只读 subagent；未参与 R006 设计或治理文件修改
> FINAL VERDICT: PASS

### 验证项

- [x] 概念车道明确绑定现有 `PREFORMAL_METHOD_FACTORY`，且只在任务明确要求产方法、目标章节无 active carrier、inventory 无 `READY / NEEDS_SMALL_ADAPTER` 时进入。
- [x] 概念车道只产方法原型卡，不运行实验、不形成 Go/claim；survivor 必须返回正式 GW Step 1–3/3.5/4a。
- [x] 候选碰撞检查复用现有 inventory 和原型卡内嵌 receipt，没有新建 registry、controller 或逐卡治理链。
- [x] 检索后移、cheap-alternative、工作量熔断和“先核心比较、后证据加固”均有明确边界。
- [x] T004/T005 结果证据引用精确 commit，且 task brief 与结果证据分开。
- [x] foreground control 已升级为 v2；`mission_log_ref` 和 `CP001` 可解析，结构化校验通过。
- [x] registry YAML 无重复 slug；`git diff --check` 通过；四个既有 `p05_run*.log` 未纳入修改。

### 验证证据

```text
independent verifier initial
PARTIAL; P0=0 P1=2 P2=2

after deterministic design repair
PASS; P0=0 P1=0 P2=1

registry/control/mission-log parse
PASS

git cat-file -e T004/T005 commit and method-package path
4/4 exit 0

git diff --check
PASS
```

### 结论

PASS。R006 足以进入用户审阅和后续 RED 设计，但不授权 Skill 修改或科学执行。残留 P2 是首个任务派发前需显式记录 `intent/mechanism/family` 与 streak 计数；CP001 已以零值字段前置关闭该操作债务，不增加新治理文件。

## V018: T007 P1 纠偏、Skill 最小回归与 T008 入口终验

> date: 2026-08-05
> 关联：S015 / D024 / CP005 / T008
> verifier 上下文：独立 fresh-context 只读 subagent；未参与修订
> FINAL VERDICT: PASS

### 首轮对抗审查

首轮为 `BLOCK`（P0=0、P1=2、P2=1），捕获三项真实缺陷：T008 Step 2 越入全文语义
精读、历史 GREEN prompt 未绑定旧 Git object、topic-index 缺 D024 scope-change。三项均做确定性
修复，没有放宽 P1 科学层级或增加新流程。

### 修复后验证项

- [x] caller 在 FOE 与 CPE 两个独立 NumPy 调用中真实执行两次 `rx**M0`；无已证 JIT/CSE trace。
- [x] 共享图的升幂域补偿 `raised*exp(-j*M0*omega*k)` 与原信号域 CFO 补偿数学一致。
- [x] P1 仅恢复为 `THESIS_ENGINEERING_COMPONENT` design survivor；P2–P5 继续 `REJECT`，无 `METHOD_SIGNAL`。
- [x] Skill 只补“廉价替代须存在于实际测量工具链”与“matched output 可作计算图非劣证据”两条。
- [x] RED/GREEN prompt 绑定 baseline commit `64a88db`、blob `2af13b1f...` 和可复跑 `git show` 命令。
- [x] T008 严格停在 GW Step 1 检索与 Step 2 acquisition/identity/SHA/内容质量门；全文方法语义留 Step 3。
- [x] D024→S015→CP005→topic-index→registry→T008 血缘及 scope-change 一致。
- [x] canonical/runtime Skill 非缓存文件 104/104 byte-identical；未触碰 common/params、旧 campaign 或四个 p05 logs。

### 验证证据

```text
independent verifier initial
BLOCK; P0=0 P1=2 P2=1

independent verifier after deterministic repair
ACCEPT; P0=0 P1=0 P2=0; 9/9 PASS

pytest
114 passed, 1 skipped

canonical/runtime SHA256 comparison
104/104; mismatch=0

validate_task_control.py T008 / registry YAML / git diff --check
PASS / PASS / PASS
```

### 结论

PASS。D024 对 T007 P1 的恢复有 caller、公式与可复跑历史输入支撑；Skill 修订没有降低正式
Groundwork 或科学晋级门。T008 可派发，但只授权 Step 1–2，不能据此实现、实验或宣称方法成立。

## V019: baseline-first method batch 001 独立终验

> date: 2026-08-06
> 关联：D027 / CP008 / `baseline-first-method-batch-001.md`
> verifier 上下文：独立 fresh-context 只读 subagent；未参与 baseline 精读、方法卡构造或治理修改
> FINAL VERDICT: PASS

### 首轮对抗审查

首轮为 `BLOCK`（P0=0、P1=3 类、P2=2 类），捕获三类实质问题：四篇 worktree-local 全文被
误写为 root 论文库路径；K01/K02 把抽象 controller 结构相似误判为 exact action collision；
master-state 历史背景残留旧 `CANDIDATE_ROTATION_REQUIRED` current。三类均做最小确定性修正，
没有增加候选、降低生产门或改变 terminal。

### 修复后验证项

- [x] 7 篇 baseline 均为 2019+ 正式发表，本地有效全文存在，方法身份可确认。
- [x] 自动解析 13 个全文引用实例，路径全部存在，行号/范围均未越界，关键段支持身份、方法链、输入输出、假设与限制。
- [x] Ch4 supersession banner、D025 P1 closed、D026 C3 closed 与 D027 active authority 的优先级正确。
- [x] C3、P1、P01–P11、G1、AMC 与 Ch4/Ch5 dead end 均未复活；survivor=0。
- [x] K01 明确无 exact collision，以 `PROBLEM_EVIDENCE_INSUFFICIENT` 停止；不声称 cheap alternative 已实证吸收。
- [x] K02 明确 controller 相似不作否决，以 `PROBLEM_ABSENT_IN_CURRENT_CALLER` 停止。
- [x] K03–K05 的历史/常规替代约束有 authority；半天 adapter 为静态工程估算，不冒充执行验证。
- [x] 五卡无人同时通过十门，`STRATEGIC_SHORTAGE_CONFIRMED` 是唯一合法 terminal。
- [x] D027、CP008、epoch 20 topic-index、registry 与 master-state 一致，旧 current 已消除。
- [x] 四个 `p05_run*.log` 仍为 untracked/未暂存；无 Skill/controller/common/params/formal-stage 越界修改。

### 验证证据

```text
independent verifier initial
BLOCK; P0=0 P1=3类 P2=2类

after deterministic repair
PASS; P0=0 P1=0 P2=0

full-text pointers
13/13 paths exist; all line ranges in bounds

git boundary
p05_run*.log untracked and unstaged; cached diff empty
```

### 结论

PASS。7 篇 baseline、5 张完整方法卡、逐卡碰撞收据与 0 survivor 终局均有可复核证据；本批不授权
Groundwork、检索、实现或实验。下一合法动作仍是用户显式选择改变 candidate source、target chapter
或 research object。
