# Portfolio scheduler 控制面迁移审计

> 日期：2026-07-20
> 性质：只读迁移审计；不授权修改、搬运、运行或删除旧控制面
> 旧源：`D:/code/study/research-protocol/.worktrees/p03-residual-headroom/projects/thesis-fso/direction-lab/tools/`

## 1. 审计结论

旧 `campaign_core.py` 与 `campaignctl.py` 共有 23 个模块级 public function、1 个 public property 和 4 个 CLI command。文件不含通信或 OSL 项目专词，但这不等于它们都是通用 utility：候选排名、science slot 匹配、portfolio 完整性、work-conservation、固定最小批次/机制覆盖和 stop legality 都是开放式科研判断。

控制链 `validate_campaign → reduce_campaign → next_action / may_stop` 及其 `preflight / next / record / close` CLI 必须归为 `DELETE_SCHEDULER`。V035、V037 均为独立终验 `FAIL`：前者发现第二 runnable truth，后者复现固定 `min_valid_batches` 不可完成以及唯一资源 slot 被消费后仍保留 runnable 候选的反例。

`KEEP_AS_UTILITY` 只表示某个确定性行为可在新安全小工具中独立重实现或对照，不表示可 import 旧 module、复制旧文件或继续运行旧 scheduler。当前没有任何 public function 应 `MOVE_TO_ADAPTER`；Project Adapter 只拥有项目事实规范化，不承接候选选择、资源匹配、完整性证明或停机权。

## 2. 证据与分类口径

- 目标决策：`.sessions/2026-07-20-research-direction-lab-system/decisions.md` D001、D005。
- 旧设计：`.sessions/2026-07-10-dual-pol-osl-groundwork/S078-portfolio-autopilot-design.md`。
- 独立失败证据：旧工作树 `verifications.md` V035（第 927 行）、V037（第 994 行）。
- 新目标面：`.agents/skills/research-direction-lab/scripts/` 中 `hash_bundle.py`、`validate_receipt.py`、`append_event.py`、`rebuild_state.py`、`render_status.py`。
- `domain_terms` 同时记录项目词和研究调度词；“项目词为无”不能覆盖 candidate、portfolio、branch、slot、critic、minimum、stop 等控制语义。
- `scientific_judgment=YES` 表示函数直接或间接选择候选/资源/停止，或把固定批次、机制覆盖、critic/disposition、portfolio exhaustive 当作科研准入或完成判据。

旧证据在审计时的 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `campaign_core.py` | `a75c997323b7e55eb755939e9b5c4126f59f381c8c46a90aba6686ef12b6884a` |
| `campaignctl.py` | `54b106568f999b1bd2fc7356af5ca06b1ca8d2235f6bf594d51f9b2095b4bde1` |
| `S078-portfolio-autopilot-design.md` | `07590f79150569f30f8164ed71172a375453724eda1e84c80b331b47c9a96f54` |
| `verifications.md` | `1b4bec1d3e2f4aad5cc53f3eb32f37fc7c4ea12c913d72e0360991088f6ad3e1` |

## 3. Public API 逐项审计

下表固定列依次为 file、symbol、line、callers、domain terms、state mutation、scientific judgment 和 disposition。`tests` 指旧工作树的 `test_campaignctl.py`；`CLI` 指 `campaignctl.py` handler。

| kind | file | symbol | line | callers | domain terms | state mutation | scientific judgment | disposition |
|---|---|---|---:|---|---|---|---|---|
| API | campaign_core.py | canonical_json | 129 | content_hash, validate_campaign, admit_batch, append_events, reduce_campaign, tests | 项目词无；调度词无 | 无，纯确定性 bytes | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | content_hash | 142 | event_hash, receipt checks, tests | 项目词无；调度词无 | 无，纯 hash | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | campaign_root | 147 | campaign_path, CLI wrapper | 项目词无；仅 campaign 路径名 | 只读文件系统元数据 | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | campaign_path | 161 | append_events, atomic_write_state, ensure_state_consistent, CLI, tests | 项目词无；仅 campaign 路径名 | 只读路径与文件系统元数据 | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | validate_campaign | 351 | command_preflight, tests | 项目词无；portfolio, ranking, science slots, minimums, resource requirements | 读 config 与 normalized portfolio，不落盘 | YES | DELETE_SCHEDULER |
| API | campaign_core.py | admit_batch | 548 | command_record, tests | 项目词无；candidate, branch, critic, disposition, resource slot | 读 receipt/review/attestation 指针与 reducer state，返回待写 event | YES | DELETE_SCHEDULER |
| API | campaign_core.py | event_hash | 683 | event chain, CLI preview, tests | 项目词无；调度词无 | 无，纯 hash | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | load_events | 740 | append_events, CLI live/record/close, tests | 项目词无；旧 campaign event types | 读 JSONL，不写 | NO | ARCHIVE_UNUSED |
| API | campaign_core.py | append_events | 764 | append_event, command_close | 项目词无；旧 scheduler event schema | 锁定并追加 events.jsonl，fsync，失败回滚 | NO | ARCHIVE_UNUSED |
| API | campaign_core.py | append_event | 845 | command_record, tests | 项目词无；旧 scheduler event schema | 追加 events.jsonl | NO | ARCHIVE_UNUSED |
| API | campaign_core.py | reduce_campaign | 906 | CLI state paths, next_action, recursive close validation, tests | 项目词无；candidate disposition, branch coverage, slot usage, ranking, terminal state | 读 frozen config/events，生成 scheduler state | YES | DELETE_SCHEDULER |
| API | campaign_core.py | next_action | 1170 | command_next, tests | 项目词无；ranking, branch coverage, slot matching, work-conservation, stop | 读 scheduler state，返回控制动作 | YES | DELETE_SCHEDULER |
| API | campaign_core.py | may_stop | 1287 | next_action, reduce_campaign, command_close, tests | 项目词无；minimums, runnable candidates, exhaustion certificate, terminal conditions | 读 scheduler state 与 stop request | YES | DELETE_SCHEDULER |
| API | campaign_core.py | render_state_bytes | 1339 | atomic_write_state, ensure_state_consistent, tests | 项目词无；调度词无 | 无，纯确定性 YAML bytes | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | atomic_write_state | 1350 | CLI preflight/record/close, ensure_state_consistent, tests | 项目词无；旧 campaign state 文件名 | 原子覆盖写 state.yaml | NO | KEEP_AS_UTILITY |
| API | campaign_core.py | ensure_state_consistent | 1366 | CLI live loader, tests | 项目词无；继承全部 scheduler projection | 读 events/state；漂移时重写 state.yaml 并抛错 | YES | DELETE_SCHEDULER |
| API | campaign_core.py | ValidationReport.passed | 125 | command_preflight, tests | 项目词无；仅旧 preflight report | 无，读取 errors | NO | ARCHIVE_UNUSED |
| API | campaignctl.py | campaign_path | 45 | private CLI loaders, tests | 项目词无；仅 campaign 路径名 | 只读文件系统元数据 | NO | ARCHIVE_UNUSED |
| API | campaignctl.py | command_preflight | 142 | argparse preflight | 项目词无；portfolio completeness, policy, slots | 读 config/portfolio，touch events，写 state | YES | DELETE_SCHEDULER |
| API | campaignctl.py | command_next | 162 | argparse next | 项目词无；next candidate/action | 读 config/events/state；漂移时可重写 state；输出 action | YES | DELETE_SCHEDULER |
| API | campaignctl.py | command_record | 168 | argparse record | 项目词无；admission, candidate, critic, slot, disposition | 读证据/评审，append event，写 state | YES | DELETE_SCHEDULER |
| API | campaignctl.py | command_close | 223 | argparse close | 项目词无；stop reason, exhaustion, governance review | 读 review/certificate，append control events，写 state | YES | DELETE_SCHEDULER |
| API | campaignctl.py | build_parser | 275 | main, tests | 项目词无；公开 preflight, next, record, close | 无，构造 scheduler CLI surface | YES | DELETE_SCHEDULER |
| API | campaignctl.py | main | 312 | module entrypoint, tests, shell | 项目词无；继承全部 scheduler CLI | 取决于所选 handler | YES | DELETE_SCHEDULER |

`CampaignError`（`campaign_core.py:113`）只是旧控制面的异常载体，不是 function；新小工具使用标准异常或自有异常即可，归档时不应继续 import。

## 4. CLI command 逐项审计

| kind | file | symbol | line | callers | domain terms | state mutation | scientific judgment | disposition |
|---|---|---|---:|---|---|---|---|---|
| CLI | campaignctl.py | preflight | 279 | argparse dispatch to command_preflight | 项目词无；portfolio completeness, minimums, slots | 初始化旧 events 与 state | YES | DELETE_SCHEDULER |
| CLI | campaignctl.py | next | 286 | argparse dispatch to command_next | 项目词无；candidate ranking, slot matching, work-conservation | 读或修复 projection，输出控制动作 | YES | DELETE_SCHEDULER |
| CLI | campaignctl.py | record | 290 | argparse dispatch to command_record | 项目词无；admission, critic, candidate, slot, disposition | 写 event 与 state | YES | DELETE_SCHEDULER |
| CLI | campaignctl.py | close | 300 | argparse dispatch to command_close | 项目词无；stop legality, minimums, certificate | 写 review/certificate/close events 与 state | YES | DELETE_SCHEDULER |

## 5. KEEP 与退役边界

以下行为可作为确定性 utility 独立重实现：canonical serialization/hash、路径 containment 与 symlink 防护、纯 event hash、确定性 YAML rendering、原子文件替换。现有 Task 4 scripts 已分别提供 bundle hash、receipt validation、append-only ledger、机械 state replay 和 status rendering；Task 7 不复制旧代码，也不修改新 scripts。

以下判断无条件不得 `KEEP_AS_UTILITY` 或转移到 Adapter：候选排名、slot 匹配、portfolio completeness、work-conservation、固定批次/机制族覆盖和 stop legality。`admit_batch` 也不能通过拆出 receipt 检查整体保留，因为其 public contract 把 critic、candidate status、slot 与 science question 绑定为科研准入。

新 `rebuild_state.py` 与 `render_status.py` 允许读取和显示事件中已经记录的 `next_action`，状态字段名为 `recorded_next_action`。这只是事实重放；不得新增 `def next_action`、候选 selector、资源 matcher、完整性证明或停机判定。测试因此允许 `.get("next_action")` 读取事实键，但拒绝 public API、属性调用、模块级绑定、旧 module import 和 scheduler CLI 子命令。

为防止把 scheduler 改成私有 helper 后绕过精确名称检查，测试还对 scripts 的 AST function 定义与 call site 做标识符分词组合检查：candidate 与 rank/select/score/order 等词组合视为候选排序选择，resource/slot 与 match/allocate/assign/reserve 等词组合视为资源匹配分配，portfolio 与 completeness/coverage/exhaustion 或 coverage proof 组合视为完整性证明，stop/close 与 legality/allow/can/should 等词组合视为停机合法性。该检查只扫描 Skill scripts，不扫描测试 fixture；`render_status`、`recorded_next_action` 和 `.get("next_action")` 保持合法。对于 `_render_recorded_candidate_ranking` 一类事实展示 helper，仅当标识符同时包含 `recorded` 与 render/display/format/report/show，且不含 select/match/prove/allow 等主动决策动词时豁免；把主动决策伪装进 render 名称仍会被拒绝。

## 6. 旧证据保持与最终退役门

1. 旧 `campaign_core.py`、`campaignctl.py` 当前均为 p03 工作树中的 untracked 文件；S078 与 V035/V037 是 dirty 历史证据。Task 7 不编辑、格式化、移动、删除或提交覆盖它们。
2. 新 Skill、Adapter、project scripts、tests 和 docs 不 import、不 shell-out、不复制旧 module；旧 CLI 不注册为入口，也不标成“deprecated but supported”。
3. V035/V037 的 `FAIL` 不因本次 no-scheduler test 通过而改变；本测试只证明新体系没有继承旧 scheduler。
4. 只有 Task 9 live activation PASS 后，才能按实施计划把旧文件标为 historical/archived。即便届时归档，也必须保留本审计哈希、V035/V037 指针和禁止运行说明；物理删除不属于 Task 7。
