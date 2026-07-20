# [S009] Task 9 live shadow execution

> 2026-07-20 | Task 9 shadow | 状态: PASS (pending independent verifier终验)
> 来源: 用户 2026-07-20 执行提示词（Task 9 shadow 明确授权 + Task 10 条件性授权）

## 目标

按用户授权执行 Research Direction Lab Task 9 live shadow：在隔离 worktree 中驱动 Skill 7-phase loop 在既有 READ_ONLY_MIGRATION_PREVIEW 地基上运行，观察 5 类行为（blocker / rotation / scope / harvest / recovery），不运行新科学。Task 9 PASS 后条件性触发 Task 10 cutover。

## 记录

### 1. Session 启动与隔离

- **触发**: session-governance Trigger 1（session start），H003 handoff verification 完成（3 事实 PASS：READ_ONLY_MIGRATION_PREVIEW / Skill 基线 60 passed 1 skipped / B004 不存在）。
- **隔离 worktree**: `D:/code/study/research-protocol/.worktrees/research-direction-lab-shadow`，分支 `codex/research-direction-lab-shadow`，从 `f79cb1bc77ad1a20fb0b8334be6dac19124f214c` 创建。父 worktree clean。
- **加载**: research-direction-lab Skill 全部 references（core-loop / recovery-and-rotation / evidence-and-claims / thesis-harvest / candidate-portfolio / batch-and-atlas / project-layout / communications profile）+ sim-preflight（核心 5 条判定 shadow 不进入 Execute 阶段）+ thesis-lessons 速查表 + TL-28~TL-33。

### 2. Foundation Certificate（地基先于科学计算）

子 agent（agent_b4ce6461，独立上下文）做只读核验。结果 PASS：

- **A. Baseline identity**: standard-CMA 含 Godard z（line 300-306 `_cma_deltas` 函数 standard 分支）；forbidden alias current-CMA/no-z 未使用；forbidden alias `common._cma.CMAEqualizer`-as-standard 未使用（file 不 import CMAEqualizer）；shared dual-pol channel hash 匹配。
- **B. Protected history**: 18/18 文件 hash 与 adapter `identity_digest` 一致。
- **C/D/E/F**: B004 不存在；standard-CMA 语义正确；所有 batch comparator 合法（B001/B002/B003/P03 Atlas）；runnable vs blocked axes 一致。
- **G caveat**: completion-events.jsonl 只含 B003 一个 event（head_sequence=1 single-event bootstrap，B001/B002 provenance 在 canonical-state.completion_history）—— 项目设计如此，不是 corruption。

**发现两个非阻塞 stale hash**（Foundation Certificate caveat 1/2）：canonical-state.yaml 内部 `event_log_sha256` 和 `simulator.sha256` 与 disk hash 不一致，但 canonical-state 自己的 protected digest 和 completion-events.jsonl 的 protected digest 都和 disk 一致。这是内部 stale self-checksum，不是 protected file corruption。正式激活前可清理。

证书写入 `projects/thesis-fso/direction-lab/shadow/foundation-certificate.v1.yaml`。

### 3. Shadow Contract 冻结（边界、时间预算、PASS 标准）

写入 `projects/thesis-fso/direction-lab/shadow/S001-contract.yaml`。关键条款：

- shadow 只在 dual-pol OSL 现有地基及其合法 Project Adapter 范围内；
- 时间预算为本对话内连续推进，不规定固定批次数；
- 不进入正式论文晋级，不创建 B004，不修改 protected history；
- 5 类行为必须观察（OBS-BLOCK / OBS-ROTATE / OBS-SCOPE / OBS-HARVEST / OBS-RECOVER）；
- 自然科学工作未覆盖时可 replay（Plan Step 3 允许），不能伪造新科学 batch；
- PASS 标准 verbatim Plan Task 9 Step 4。

### 4. Shadow observation（驱动 Skill 7-phase loop）

Replay 模式（不运行新科学）：
- 子 agent（agent_68f4ad1e）并行读 B001/B002/B003 manifest+verifier+synthesis + Atlas closeout + stage-a synthesis/verifier + P01 preflight + P02 triage + failure-registry + canonical-state + 现有 ledger H001-H009。
- 子 agent 提出 8 个候选新 harvest（H010-H017），全部 CONTRACT/SLICE 级，无 DOMAIN/FAMILY 越界，每条带 artifact quote。
- 主线程做 Skill 判断：全部接受，每条符合 evidence-and-claims.md "smallest defensible claim ceiling"。

**关键修正（路 A vs 路 B）**：最初把 H010-H017 直接写进 `harvest/ledger.v1.yaml`，触发 3 个 V003-冻结测试 FAIL（`test_status_is_exact_renderer_output` / `test_harvest_is_bounded_pointer_only_*` / `test_declared_render_command_reproduces_status_*`）。根因：renderer 是 STATUS 的 single source of truth，main ledger V003-anchored 到 H001-H009。**修正**：所有 shadow 派生物移到 `shadow/harvest-derived.v1.yaml`，用 `SHADOW-` 前缀，每条加 `promotion_block: not yet promoted`。STATUS 通过 renderer 重新生成（保持 LF bytes 与 HEAD 一致）。修正后 77 passed + 1 skipped。

**STATUS CRLF 债务（pre-existing，非 shadow 引入）**：shadow worktree 创建时 git autocrlf 把 STATUS 转 CRLF，测试 `read_bytes()` 拿到 CRLF 与 renderer 输出的 LF 不等。parent worktree 上同测试 PASS（其 STATUS 已是 LF）。最小修复 = 用 renderer 重渲染 STATUS。这揭示 V003 测试在 Windows + autocrlf=true 下脆弱，属于 pre-existing 环境债务。

### 5. 五类行为证据（shadow observation log）

写入 `shadow/S001-observation.md`：

| Behavior | Evidence |
|----------|----------|
| OBS-BLOCK | 6 个 blocked axes（3 P03 axes + P01 + P02 + formal.promotion），全部按 Skill 纪律标 INFRASTRUCTURE_BLOCKED（不是 negative），有 repair_condition，无 overclaim |
| OBS-ROTATE | R1-R5 candidate rotation trace（P03 SLICE local negative → U24 family re-review → P01 architecture-blocked → P02 not-runnable → 战略耗尽 escalate）；continuation rate = 100% on legal alternatives |
| OBS-SCOPE | 每条 SHADOW-H010..H017 `claim_ceiling` 设为最小级别（CONTRACT 或 SLICE），无 DOMAIN/FAMILY overclaim；Stage A verdict ladder 显式枚举 DOMAIN-remains-open 原因 |
| OBS-HARVEST | 8 个新 SHADOW-H010..H017 entries 派生自 frozen artifacts，每条有 artifact quote + source_hashes + harvest_source；每个完成的 replay batch（B001/B002/B003/Atlas）至少 1 个 harvest |
| OBS-RECOVER | Session 启动恢复（topic-index → S008 → H003 → decisions → verifications → voice → plan → Skill + references → STATUS + adapter + portfolio + ledger + thesis-spines → Foundation Certificate）；3 个 handoff 事实已 PASS |

### 6. 治理成本

- 科学工作（replay + harvest 派生 + rotation trace + claim scope 判断）：约 60% 对话投入。
- 治理维护（contract + certificate + observation log + STATUS + session note + voice + decisions）：约 40%。
- 未新增 controller/scheduler/complexity 补丁。

### 7. PASS 标准 self-assessment（Plan Task 9 Step 4）

| 标准 | 状态 | 证据 |
|------|------|------|
| zero history/provenance P0 | PASS | Foundation Certificate B 18/18 |
| zero local-to-domain overclaim | PASS | 每条 harvest bounded at CONTRACT/SLICE |
| 100% automatic continuation when legal alternatives existed | PASS | R1-R4 rotated；只有 R5 在战略耗尽停止 |
| readable one-page STATUS | PASS | STATUS.v1.md 58 行 / 4790 bytes（renderer 输出） |
| ≥1 harvest per completed scientific batch | PASS | 8 新 SHADOW-H010..H017 from 4 replay batches |
| 5 类行为证据 | PASS | 见上表 |
| 通用 Skill/代码无通信/OSL 语义 | PENDING VERIFIER | rg scan 由独立 verifier 跑 |
| 无 scheduler 回潮 | PENDING VERIFIER | rg scan + test_no_scheduler_contract 由独立 verifier 跑 |

## 决策引用

- D008：新建（本轮）—— Task 9 shadow 授权 + 边界扩展到 Task 10 cutover 含 AGENTS.md 最小路由（用户提示词 §七）。
- D001-D007：继续有效（本轮未触动 Skill / Profile / schema）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。Task 9 shadow 已授权；未触 B004、ML 训练、新科学实验、protected history 修改、push/merge。
- 范围扩展：原 plan Task 9 Step 5 只提 process.md/README/旧 Skill superseded；本轮提示词 §七 把 cutover 扩到 AGENTS.md 最小路由（"只增加最小路由和边界索引，不复制 Skill 内容"）。已记入 D008。

## 后续

- Task 9 独立 verifier 终验（分离上下文，跑全套测试 + rg scan + hash 检查 + B004 absence + scope 边界）。
- 若 PASS：Task 10 cutover（process.md 短入口 + 旧 Skill superseded + doc-steward 架构文档 + AGENTS.md 最小路由）。
- 若 PARTIAL/FAIL：按 Plan Task 9 Step 5 失败处理（不正式激活，定位失败源，改正确 owner）。
- 残留债务（非阻塞）：canonical-state 内部 stale hash（FC caveat 1/2）；STATUS CRLF Windows autocrlf 脆弱性（pre-existing）；B6/B1 fallback 词表外局限（V004 已知）。
