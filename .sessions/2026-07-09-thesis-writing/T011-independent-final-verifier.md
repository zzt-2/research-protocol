# Task Brief: 方法包装审计独立终验

> 来源: S018 / D026 | 日期: 2026-08-03 | review base: `dd2aab4526a36a92a07bc6c7fd0a3eedaf7b6462`

## 0. 角色与边界

你是 fresh-context 独立 verifier，未参与作者工作。工作目录：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。只读审查 `git diff HEAD`、全部本轮 untracked T/S/harvest 文件与用户附件 `C:\Users\zzt\.codex\attachments\d905f776-e347-430e-83f5-9b801c4147a5\pasted-text.txt`；不得改文件、index、HEAD 或分支，不得跑实验/联网。四个 `projects/simulation/explore/cma-fade-divergence/p05_run*.log` 是用户既有 untracked 文件，必须确认未纳入本轮。

## 1. 主产物

- `projects/thesis-fso/direction-lab/harvest/peer-thesis-method-packaging-audit.md`
- `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
- `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`
- `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`
- `.sessions/2026-07-09-thesis-writing/S018-master-thesis-method-packaging-audit.md`
- `decisions.md` D023–D026、`topic-index.md`、`voice.md`、`.sessions/_registry.yaml`

## 2. 用户 13 项门（逐项 PASS/FAIL/PARTIAL）

1. “每个核心技术章有方法”已进入正式决策；
2. 旧同门/硕士调研失效原因有文件+行号证据；
3. 样本是 8–12 篇真实硕士且每篇至少读两个方法/技术章；
4. 抽取不是摘要/创新点列表，包含 baseline→actual delta；
5. 已接受 recipe 各有至少两篇真实实例；R6 若 0 例，必须明确经定向反证后拒绝而非伪造 recipe；
6. 内部资产未复活 invalidated/unauthorized claim；
7. 2A–2D 每个候选都有 action/baseline 或明确因没有 action 降级；
8. chapter-capable 方法能画框图、写流程、做实验/消融；
9. 两套 spine 均逐章审计，唯一推荐的每个技术章确有方法，conditional 状态未伪装完成；
10. 内部资产足够时不应创建 Phase G search target；不足时才需要具体 method-shaped target；
11. 未写正式论文正文、未跑实验、未改 Skill；
12. session/registry/voice/decision bloodline 正确，旧 dossier 有 supersession banner；
13. `git diff --check` exit 0，YAML 可解析，四个 p05 logs 未纳入改动/提交范围。

## 3. 强制核验动作

- 逐文件读取四个主产物；抽查至少 A1、A7、A11、A12 四篇本地全文的元数据、章节范围和 delta 是否与卡片相符。
- 检查 `### A` 数量、R1–R6 矩阵、candidate grades、D023→D025→D026 血缘、exact voice quote。
- `git diff --name-only` 与 `git ls-files --others --exclude-standard` 核范围；运行 `git diff --check`。
- 用 Python/PyYAML 解析 `.sessions/_registry.yaml` 和 `internal-method-kernel-inventory.yaml`；核 evidence path 存在。
- 搜索 `74.6%|P09|G1|9/27|5.1|6.7|26/29|3.1 dB`，确认只在 prohibited/invalidated/unauthorized 语境。

## 4. 输出格式

```markdown
## 13-Gate Verdict
| # | verdict | evidence | issue |

## Issues
### Critical
### Important
### Minor

## Assessment
READY_TO_COMMIT / WITH_FIXES / REJECT
```

每个 issue 必须给文件:行号和修法；没有写“无”。不要只说“看起来可以”。
