# [S011] Consumer deployment cutover

> 2026-07-20 | 部署收口 | 状态: PASS (pending independent verifier 终验)
> 来源: 用户 2026-07-20 执行提示词（"shadow 分支已 PASS，但普通项目入口还没有真正接通"——消费者部署断链修复）
> 2026-07-20 续接 | baseline 充分性 Skill 修订 | 状态: V008/V009 PASS，全局同步完成

## 目标

按用户授权修复"shadow 分支 V005/V006 已 PASS 但消费者入口断链"问题。本轮不重做 Task 9/10 科学内容，不创建 B004，不修改 protected history，不 push。

## 记录

### 1. 根因诊断（消费者部署断链）

事实核验结论：

- 普通根目录 `feat/title-consistency-check`（HEAD `97473a2`）只含到 `afeb553 chore: package research protocol framework and skills` 的资产，**不包含** research-direction-lab Skill 本体、通信 Profile、Project Adapter 投影、STATUS、Portfolio、Harvest、Task 8 forward tests、Task 9 shadow artifacts、Task 10 cutover 改动（FR-27 路由、process.md/README 头、architecture doc）、fr-27、docs/architecture 等。
- 普通 worktree `.agents/skills/` 下只有 `external-output/`、`sim-preflight/`，**缺** `research-direction-lab/`。
- 全局 `C:/Users/zzt/.agents/skills/` 下 `research-direction-lab/` **不存在**，但 `method-family-batch-exploration/SKILL.md` 已加 `superseded_by: research-direction-lab` frontmatter——**悬空 superseded 指针**。
- Shadow 分支 `codex/research-direction-lab-shadow`（HEAD `6ca142e`）的所有 Task 1-10 工作、V001-V006 全部 PASS，但只在 shadow worktree 内可达。

根因：shadow worktree 是 isolated commit，从未合并/ Cherry-pick 回消费者可达路径，全局 Skill 也从未安装。

### 2. 集成策略（fast-forward，无需 merge）

关键发现：`merge-base(97473a2, 6ca142e) = 97473a2`——shadow 是 current root 的严格 fast-forward 后代。`git diff --name-only HEAD 6ca142e` 显示 shadow 比 current root 多 114 文件、少 0 文件，**无任何 merge/rebase/cherry-pick 冲突**。

策略：

- 不在 dirty 普通根目录直接合并（用户提示词 §二禁止）。
- 用 `using-git-worktrees` skill 从 `6ca142e` 创建新隔离 worktree `.worktrees/research-direction-lab-integration`，分支 `codex/research-direction-lab-integration`。
- 由于 fast-forward 关系，integration worktree 天然包含 Task 1-10 完整历史链（cfb29f0 → 61b623d → e2f42e8 → f79cb1b → 6ca142e）和全部资产。
- 用户 dirty 普通根目录完全未触动。

### 3. Integration worktree 建立

```
git worktree add .worktrees/research-direction-lab-integration -b codex/research-direction-lab-integration 6ca142e
```

验证：

- HEAD `6ca142e`、分支 `codex/research-direction-lab-integration`、status clean。
- worktree list 含 6 个 worktree（root + 4 codex/* + 新 integration）。
- Skill 36 文件全部存在，无 `__pycache__`。

### 4. 全局 Skill 安装

按用户提示词 §三要求，从 V005/V006 验证过的 integration worktree 安装到 `C:\Users\zzt\.agents\skills\research-direction-lab\`。

- 安装前用 `quick_validate.py` 验证 integration worktree Skill 仍 valid（PASS）。
- 验证通用 Skill/code 无领域术语泄漏：扫描 SKILL.md / 9 个 references（除 profiles/communications.md）/ 5 个 scripts / 8 个 tests/test_*.py / score_forward_tests.py / agents/openai.yaml 中 `CMA|BER|SNR|QPSK|OSL|Jones|pilot|thesis-fso|dual.pol` 命中数 = **0**。
- `cp -r` 复制 Skill 目录（不含 Project Adapter、不含项目专属参数）。
- 字节级 hash 审计：36 文件 hash 全部一致，mismatch=0。
- 全局 `quick_validate.py` 再次 PASS。

安装元数据：

| 项 | 值 |
|---|---|
| 路径 | `C:\Users\zzt\.agents\skills\research-direction-lab\` |
| 来源 commit | `6ca142ea6c5fe6d81d8ef095af727bccd25b6597` |
| 文件数 | 36 |
| 聚合 hash（按 canonical 排序逐文件 sha256 后再 sha256） | `0f87f70d1114d1bf985b2fcf07baa6b9c3e88bc83ae3ac7a998f9ae34f31fa21` |
| 验证 | `quick_validate` PASS；integration worktree 与 global install hash 全等 |
| 回滚方式 | `rm -rf C:/Users/zzt/.agents/skills/research-direction-lab`；旧 `method-family-batch-exploration` SKILL.md frontmatter 改回无 `superseded_*` 字段（保留原文） |

旧 `method-family-batch-exploration/SKILL.md` 仍保持 superseded 状态——现在它指向的全局 `research-direction-lab/` 已存在且验证通过，悬空指针消除。

### 5. 消费者 smoke 测试

**A. 普通项目入口视角**（integration worktree）：

- AGENTS.md FR-27 单行路由存在并正确指向 Skill。
- `projects/thesis-fso/direction-lab/STATUS.v1.md` 存在，4790 bytes / 58 lines / LF。
- Project adapter 所有 13 个 `paths.*` 全部解析存在。
- 完整测试套件：`pytest skill tests + 4 project files` = **139 passed, 1 skipped**（与 V004 anchor 一致）。
- `compileall` exit 0。
- adapter 测试 75 passed（STATUS CRLF 债务用 renderer 重渲染修复，符合 S009/V005 已记录的最小修复）。
- protected history 18 文件独立重算 hash 全部 PASS。
- B004 不存在（batches/ 仅 B001/B002/B003）。
- 通用 Skill/code 领域中立扫描命中 = 0。
- scheduler scan 命中 = 0（除 test 文件中的 forbidden token list）。
- `test_no_scheduler_contract` 8 passed。
- superseded pointer 完整性：旧 Skill `superseded_by: research-direction-lab` 指向的目标存在。
- global install 与 integration worktree hash 全等（36/36 文件 mismatch=0）。

**B. 非通信 fixture 视角**：

- `tests/forward/non-comms-baseline-extension.yaml` 存在，`artifacts: []`，无项目指针。
- 通用 Skill 加载后对非通信场景输出无 CMA/BER/SNR/QPSK/OSL/Jones/pilot（fixture 中 intentionally 无这些词）。

### 6. Fresh agent discovery smoke

派发独立 fresh agent（agent_a702565b），**prompt 中不提供 SKILL.md 路径**，只给项目根和恢复指令。结果 PASS：

- 仅凭 AGENTS.md FR-27 自行发现 Skill 在 `C:\Users\zzt\.agents\skills\research-direction-lab\SKILL.md`。
- 自行定位并读取 STATUS。
- 5 个问题（formal state / Portfolio / runnable / blocked / 为什么不能直接写论文结论）全部正确回答。
- 显式确认"无需 AGENTS.md 之外的任何提示"。

关键回答亮点：

- 正确识别 `READ_ONLY_MIGRATION_PREVIEW` 授权 ceiling。
- 正确识别 6 个 blocked axes 的具体原因（H002/H005/H007 等）。
- 正确解释"不能写论文"的三重绑定（authorization ceiling + claim ceiling = SLICE + Direction Lab ≠ GW）。

### 7. AGENTS.md 与 FR-22 边界复核

- AGENTS.md 只保留 FR-27 单行路由索引（line 190），不复制 Skill 内容（满足"唯一拥有者"不变量）。
- FR-22（line 98/185/239）继续作为 GW 流程强制门控。
- FR-27 明确写"Direction Lab 是正式晋级前的候选发现/批量筛选层，不等于 GW 完成……正式候选晋级后仍必须走 Groundwork → Contract → Execute（继续遵守 FR-22）"——FR-22 与 FR-27 无冲突。
- 四层职责清晰：
  - Direction Lab（`research-direction-lab` Skill）：候选发现/Portfolio/Scout/Sandbox/批次轮换/claim scope/harvest。
  - Groundwork/Contract/Execute（`stages/*.md`）：正式研究晋级和论文证据。
  - sim-preflight：科学仿真前置。
  - deterministic code（`research-direction-lab/scripts/*.py`）：hash/receipt/schema/path/history protection，不负责开放式科学调度。

## 决策引用

- D009：新建（本轮）—— 消费者部署收口策略（integration worktree + 全局 Skill 安装 + 悬空 superseded 指针消除）。
- D008：继续有效（Task 9/10 PASS 授权）。
- D001-D007：继续有效（本轮未触动 Skill / Profile / schema 内容）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。用户提示词 §一~§九 明确授权消费者部署收口；未触 B004、ML 训练、新科学实验、protected history 修改、push/merge、Goal 开启、B001-B003/P03 Atlas/canonical baseline 修改。

## 后续

- 独立 verifier 终验（V007，11 项）。
- V007 PASS 后，integration worktree 单次 consolidated commit（不 push）。
- 用户正式使用开放式研究方向探索时，从 integration worktree（分支 `codex/research-direction-lab-integration`）开始；dirty 普通根目录保持不动。
- 残留非阻塞债务（沿用 V005/V006 已知）：
  - canonical-state 内部 stale self-checksums（FC caveat 1/2）。
  - STATUS CRLF Windows autocrlf 脆弱性（pre-existing；本轮 renderer 重渲染已修正当前 copy）。
  - Windows symlink / POSIX flock 动态测试覆盖。
  - forward-test scorer B6/B1 fallback 词表外局限（V004 已知债务）。
  - dirty 普通根目录 `_registry.yaml` 仍停在 `S001/D001` 旧描述、canonical-state.yaml dirty 与 shadow 已对齐——这些是用户工作目录改动，本轮不动。

## 2026-07-20 续接：务实 baseline 充分性裁决

### 目标

修复正式 SCIENCE_SCOUT 暴露的 Skill 判断缺口：正确但任务不适配或欠收敛的 baseline 不能制造 ML Go 信号；同时 baseline 仲裁不能默认膨胀为 SOTA 或传统方法穷举。

### 记录

- RED fresh-agent 正确阻断了 ML，却要求多个传统方法、多长度和后续全 Atlas，缺少“足以支撑有限主张即停止”的明确原则。
- 新增按需参考 `baseline-adjudication.md`，定义务实充分性、最小 baseline 梯子、`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 和 Portfolio 继续条件。
- GREEN fresh-agent 正确保持 `DIAGNOSTIC/SLICE`，明确不追默认 SOTA，并把下一批限制为一个主要传统 comparator、一个直接相关廉价扩展和公平收敛核验。
- 通用核心未写入通信项目术语；通信解释仅更新 Communications Profile。

### 决策引用

- D010：新建——Direction Lab 采用务实的 baseline 充分性裁决。

### 范围确认

- 本轮是否在 scope boundary 内：是。属于已部署 Skill 的真实使用反馈修订；不运行科学实验、不修改 protected history、不创建 B004、不训练 ML。

### 后续

- V008/V009 已 PASS；42 个非缓存文件全局同步且 hash mismatch=0。
- 从科学专题 H002 继续正式推进。
