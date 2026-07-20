# [S010] Task 10 cutover execution

> 2026-07-20 | Task 10 cutover | 状态: PASS (pending independent verifier终验)
> 来源: 用户 2026-07-20 执行提示词 §七 + V005 PASS 授权

## 目标

按 V005 PASS 授权执行 Task 10 cutover：把开放式研究方向探索的流程拥有者固化到 research-direction-lab Skill，旧路由收敛到唯一 owner，AGENTS.md 只加最小路由索引。

## 记录

### 1. Cutover 改动清单（最小化原则）

| 文件 | 改动类型 | 内容 |
|------|---------|------|
| `AGENTS.md` | 加 1 行 | 跨阶段护栏表加 FR-27 路由索引：开放式研究方向探索用 research-direction-lab Skill；Direction Lab 是晋级前候选发现层；Scout/Sandbox 不等于 GW 完成；旧 method-family-batch-exploration Skill 已 superseded |
| `projects/thesis-fso/direction-lab/process.md` | 加头 + 入口段 | 标 SUPERSEDED 2026-07-20（D008/V005）；加"进入入口（推荐路径）"段指向 STATUS/Skill/Profile/Adapter/scripts/batches；历史 DL-Process v0.4 内容保留为"历史内容（仅供参考，不再拥有流程）" |
| `projects/thesis-fso/direction-lab/README.md` | 加"流程入口"段 | 指向 Skill + STATUS + project.v1.yaml + batches + process.md（已 superseded 标注）；保留旧"当前状态"段为项目实例事实 |
| `C:/Users/zzt/.agents/skills/method-family-batch-exploration/SKILL.md` | 加 frontmatter + 头 | `superseded_by: research-direction-lab`；`superseded_date: 2026-07-20`；`superseded_evidence: D008+V005`；正文加 SUPERSEDED 注记指向新 Skill；原文保留不删 |
| `docs/architecture/research-direction-lab.md` | 新建 | doc-steward mode 架构文档：每个 entity/relationship 锚定到真实文件；包含 Purpose / Top-level responsibilities / Process boundary / 不编码什么 / V001-V005 证据 / 与 superseded artifacts 的关系 / 已知非阻塞债务 |

### 2. 解决的 FR-22 vs Direction Lab 表面冲突

用户提示词 §七明确要求："必须解决 AGENTS.md 当前'stages/groundwork 是唯一合法研究路径'与 Direction Lab 的表面冲突。"

正确解释（写入 FR-27 + process.md + README + architecture）：

- **Direction Lab** = 正式晋级前的候选发现/批量筛选层（Scout/Sandbox/harvest/portfolio）。
- **Groundwork → Contract → Execute** = 正式科学证据形成层。
- **每个微候选不需要完整 GW**；Scout/Sandbox 的批量筛选发生在 GW 之前。
- **晋级候选不能绕过 GW/Contract/Execute**（FR-22 不变）。
- **Scout/Sandbox 数字不自动进入论文或 canonical baseline**。

这不是矛盾，是分层：候选发现层 ≠ 证据形成层。

### 3. 测试结果

cutover 改动后全部测试 PASS：
- pytest skill + adapter = 77 passed + 1 skipped
- quick_validate = Skill is valid!
- compileall = exit 0
- STATUS.v1.md = 58 lines / 4790 bytes / CRLF=0 / LF=58（renderer 输出，与 HEAD 一致）

### 4. 范围控制

- 没有复制 Skill 内容到 AGENTS.md/process.md/README（只加路由索引行）
- 没有删除旧 method-family-batch-exploration Skill（用户要求保留历史）
- 没有运行新科学实验、没有创建 B004、没有修改 protected history 18 文件
- 没有修改 baseline 源代码、canonical-state、completion-events、receipts
- `C:/Users/zzt/.agents/skills/method-family-batch-exploration/SKILL.md` 在 worktree 外（独立 skill 安装目录），不在 shadow 分支的 git tree 内——这是预期，cutover 改动的是用户机器上 skill 目录的状态。

### 5. 下游影响

新对话进入开放式研究方向探索时：
1. 读 AGENTS.md 看到 FR-27 路由 → 知道用 research-direction-lab Skill
2. 读项目 STATUS.v1.md（renderer 输出八问）→ 一页恢复全局
3. 加载 Skill → 7-phase loop + 7 references
4. 通信领域读 references/profiles/communications.md
5. 项目事实读 project.v1.yaml
6. 不再读 process.md（已 SUPERSEDED）；旧 method-family-batch-exploration Skill 已标 SUPERSEDED

## 决策引用

- D008：本轮 cutover 的授权依据；范围扩展到 AGENTS.md 最小路由是用户提示词 §七明确要求。
- V005：Task 9 PASS 是 cutover 的前置门控。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。Task 10 cutover 已在 V005 PASS 后由 D008 §5 授权；改动严格限制在路由/索引/superseded 标记/架构文档；未复制 Skill 内容，未删旧资产，未触 protected history 或 baseline。

## 后续

- Task 10 独立 verifier 终验（分离上下文）。
- 若 PASS：本对话收尾，单次 consolidated commit（不 push）。
- 若 PARTIAL/FAIL：按 verifier 缺陷列表修。
- 残留非阻塞债务（不在本 cutover 范围）：canonical-state 内部 stale hash 清理；STATUS CRLF Windows autocrlf 脆弱性；Windows symlink/POSIX flock 动态测试覆盖；forward-test scorer B6/B1 词表外局限。
