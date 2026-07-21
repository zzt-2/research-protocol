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
