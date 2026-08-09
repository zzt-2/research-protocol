# Step 055 — Coded decoder-feedback post-repair terminal verification

> 2026-08-09 | T009 | action class: `VERIFY`
> start: `2026-08-09T20:08:37.954+08:00`
> end: `2026-08-09T20:13:20.953+08:00`
> elapsed: `00:04:43.000`
> hard limit: 8 minutes

## Findings first

计数：**P0=0 / P1=1 / P2=0**。

### P1-1 — 四个受保护 `p05_run*.log` 的当前 SHA256 与 T009 冻结值不符

四个文件均存在，仍为 untracked/unstaged，且本 verifier 未修改它们；但 fresh `Get-FileHash -Algorithm SHA256` 得到：

| 文件 | T009 冻结 SHA256 | fresh SHA256 |
|---|---|---|
| `p05_run.log` | `7843F079267293E8C1DF0EA063B63C0925BC48122B3890F664B6F5B59C93CF11` | `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11` |
| `p05_run2.log` | `735E67765338986AE89B356E6FD986E8B0CAFF1FD5D9F75AC3D35DB14153338B` | `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B` |
| `p05_run3.log` | `C7681D64E7C44C58199A27B37E8F072941EC71C5DA22C021E57A96BB6505B34D` | `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D` |
| `p05_run4.log` | `95A154CC631E9EBF27D21583562A75F7D82FF871A9DE5658BAEE0CEEC0C221DE` | `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE` |

**最小修复**：主控只读核查冻结 SHA 的权威来源与这四个现存文件的 provenance。若冻结值有误，先修正权威任务合同；若文件确被外部改动，从已验证的受保护副本恢复。随后另起 fresh-context verifier 重跑 D。不得由本 verifier 猜测或覆盖文件。

## 四组冻结检查

### A. Task-control、JSON 与 coverage — PASS

- task-control validator=`PASS`；reviewed mirror、integrated v2、原镜像三份 JSON 均可解析。
- reviewed mirror=`28/28`，逐条具备 priority/reason、合法 disposition、relation、claim ceiling、原路径与 1-based row provenance。
- disposition=`duplicate 8 / irrelevant 10 / strong neighbor 4 / baseline 2 / unknown 4`；原镜像无 review 字段。
- 输入恰为 17 份：8 个 C1 route、8 个 C2 route、1 个 reviewed mirror；`raw=93`、`records=66`，raw/record provenance 均为 `93/93` 唯一 pair 且集合一致。
- fresh 重算 `published=50`、`must-read=6`、`sources=7`、C1/C2 R2=`2/2`。
- `Phase Estimation by Message Passing` 为独立 `title:phase estimation by message passing` strong-neighbor record；仅保留 DOI `10.1007/978-3-540-27824-5_22` possible alias，未合并。

### B. Collision、replacement 与 claim ceiling — PASS

- C1=`CORE_ACTION_EXACT`（arXiv `2511.21340`）；C2=`CORE_ACTION_EXACT`（DOI `10.1109/TWC.2004.837407`）；TSP 2006=`STRONG_NEIGHBOR`。
- UNKNOWN rows `12/19/24/27` 忠实保留且 `replacement_blocking=false`；现有 metadata/abstract 无可识别 carrier-recovery action。
- actionable mirror rows `13/14/20/22` 均为 C2/message-passing/iterative synchronization 邻域；rows `7/17` 仅为 baseline。
- `replacement=0`、terminal=`STEP1_NO_METHOD_ACTION_SURVIVOR`、canonical=`NO_VALID_PROBLEM`、adapter=`false`；报告明确只限 Step-1 action identity，不扩大成领域负面、B2 已解决或 testbed 不可建。

### C. Governance consistency — PASS

- registry、topic、S001、D003、CP003 mission、master 均反映 `T007 FAIL → T008 repair → T009 pending`。
- 权威数字一致：`93→66`、`50/66`、must-read `6`、sources `7`、replacement=`0`。
- Step 2、adapter、MVE、Contract、Execute 与论文方法声称保持冻结。

### D. Git 与 protected files — FAIL

- HEAD=`1d76f917a89c719614aeefd7a165ab9819425978`；staging=`0`。
- 5 个 tracked `tools/litsearch/__pycache__/*cpython-312.pyc` 仍仅为 unstaged noise。
- 除四个既有 untracked `p05_run*.log` 外，无 `source/common/adapter` 或 scientific-experiment artifact 改动。
- 四个 `p05_run*.log` 的 SHA256 均不等于冻结值，见 P1-1。

## Command / exit-code ledger

| 组 | 命令 | Exit | 说明 |
|---|---|---:|---|
| A | `python .agents/skills/research-direction-lab/scripts/validate_task_control.py .../T009-post-repair-terminal-verification.md --repo-root .` | 0 | `PASS` |
| A | inline Python：三 JSON 结构探查 | 1 | Windows GBK 输出 U+FB01 失败；只读诊断，不影响文件 |
| A | inline Python：首版冻结断言 | 1 | verifier 自身 f-string 语法错误；未形成证据 |
| A | inline Python：修正版 28/28、17 inputs、93/66、provenance、计数、alias 冻结断言 | 0 | `A_PASS` |
| B | inline Python：collision/mirror/replacement evidence dump | 0 | 只读 |
| B | inline Python：collision、UNKNOWN、action-neighbor、terminal 与 scope-ceiling 断言 | 0 | `B_PASS` |
| C | inline Python：治理一致性首版断言 | 1 | verifier 对 `CONTRACT/EXECUTE` 大小写误判；未形成仓库 finding |
| C | inline Python：大小写修正后的六 owner 一致性与下游冻结断言 | 0 | `C_PASS` |
| D | PowerShell：HEAD/staging/hash/status 首版断言 | 1 | 错把日志假定在根目录且过滤过宽；未形成仓库 finding |
| D | PowerShell：使用实际日志路径重跑 HEAD/staging/SHA256/pyc/protected-path 断言 | 1 | `D_FAIL`：四个 SHA256 不符 |

## Verdict

`FAIL`

该 verdict 仅阻断 terminal package 的正式接收；A/B/C 的科学与治理检查通过，不授权 Step 2、adapter、实现、实验或论文方法声称。
