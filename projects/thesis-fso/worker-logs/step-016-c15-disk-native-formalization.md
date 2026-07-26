# Step 016 — C15 disk-native formalization — Phase A

> executor: `/root/t016_phase_a_executor_retry`
> worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> phase: `A0–A1`（A1 identity hard-block 后按合同停止，未执行 A2/A3）
> start: `2026-07-27T05:44:43.4145823+08:00`
> stop: `2026-07-27T05:50:11.3496868+08:00`
> elapsed: `327.94 s`
> HEAD: `c4062c8c969a6aa4a098cfbd0a013eb9e572a4a5`
> control: `epoch 40 / CP015 / C15_FORMALIZATION_PHASE_A_READY`

## Status

```text
phase_a_status=BLOCKED_IDENTITY_CONFLICT
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
formal_active_scientific_carrier=NONE
```

A1 五项数值门均达到阈值，但 identity merge 出现 3 组“同
`normalized_title`、两个不同非空 DOI”。T016 明确要求该情况立即
`BLOCKED_IDENTITY_CONFLICT`，所以本 executor 在 A1 停止，没有把数值门 PASS
误写为 Phase A 完成，也没有进入 A2/A3 或 Phase B。

## A0 起飞门

### command 1 — task control

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T016-c15-disk-native-formalization.md
```

stdout:

```text
PASS
```

stderr: `EMPTY`

exit: `0`

### command 2 — initial worktree state

```powershell
git status --short
```

stdout: `EMPTY`

stderr: `EMPTY`

exit: `0`

### command 3 — HEAD

```powershell
git rev-parse HEAD
```

stdout:

```text
c4062c8c969a6aa4a098cfbd0a013eb9e572a4a5
```

stderr: `EMPTY`

exit: `0`

### read-only preflight audit

执行了以下确定性只读核对：

```powershell
Get-Content <live/formal decisions sections D019,D020,D030,D031>
Test-Path <seven exact T011 archives, T011/T012 receipts, shared index, five recent targets>
Get-Item D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl
Get-FileHash -Algorithm SHA256 D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl
Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match '^(python|python3|wsl|bash)(\.exe)?$' -and
  $_.CommandLine -match '(?i)(projects[\\/]simulation|(?:^|[\\/\s_-])mve(?:[\\/\s_.-]|$)|(?:^|[\\/\s_-])seed(?:s|[\\/\s_.-]|$))'
}
```

结果：

- `D020 status=active`：PASS。
- `D031 status=active`：PASS。
- `D019 status=superseded`：PASS。
- `D030 status=superseded`：PASS。
- 七份指定 T011 archive：`7/7` 存在。
- T011/T012 receipt：`2/2` 存在。
- 五个 recent target 目录：`5/5` 存在。
- shared index size：`39099216`，PASS。
- shared index sha256：
  `7530fa6fb9ae0234eee8d98902c8bcc936e278401dc61d0daded300542a4d27a`，
  PASS。
- 精准 simulation/MVE/seed workload process count：`0`，PASS。没有采用会把
  Chromium `--variations-seed-version` 误报为科学 seed 的宽泛子串判定。
- live control：`epoch 40 / CP015 /
  C15_FORMALIZATION_PHASE_A_READY`，PASS。
- A0 总结论：`PASS`。

## A1 candidate view

### 执行方式

使用 `python -` 运行一次 disk-only inline generator。七份 archive 以普通 JSON
读取；39,099,216-byte shared index 使用：

```python
with open(shared_index, encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        # 当行相关性判断、provenance 解析和 identity merge 输入
```

shared index 未整文件加载到内存或模型上下文。程序按 T016 冻结的 NFKC/lowercase/
non-alphanumeric removal 和 lowercase DOI 规则构造 union identity，保留 archive/
index key、query、原始 `source_api/source_apis`，并把复合 provenance 按 `+`
拆为 atomic family；singleton family 只由原始 singleton provenance 计入。

generator stdout:

```text
A1_FAIL {"unique_identities":{"value":326,"threshold":20,"status":"PASS"},
"actual_source_families":{"value":8,"families":["exa","firecrawl","openalex",
"openalex_citations","s2_citations","semantic_scholar","serpapi_scholar","tavily"],
"required":["openalex","semantic_scholar","serpapi_scholar"],"status":"PASS"},
"published_ratio":{"value":0.588957,"numerator":192,"denominator":326,
"threshold":0.5,"status":"PASS"},"must_read":{"value":10,"threshold":5,
"status":"PASS"},"route_coverage":{"value":5,"routes":{
"coherent_optical_fso":245,"learned_vae_jrcma":50,"square_qam_cost":217,
"staged_switching":85,"normalization_adaptive_collapse":75},"threshold":2,
"status":"PASS"}}
```

generator stderr: `EMPTY`

generator exit: `20`（本 executor 为 identity hard-block 预留的非零停止码）

### 五项门

| gate | value | threshold | conclusion |
|---|---:|---:|---|
| unique identities | 326 | ≥20 | PASS |
| qualified actual source families | 8；必需三源均有 singleton | ≥3，且含 semantic_scholar / serpapi_scholar / openalex | PASS |
| published ratio | 192/326 = 58.8957% | ≥50% | PASS |
| 必读 | 10 | ≥5 | PASS |
| route coverage | 5 | ≥2 | PASS |

这些数值只说明覆盖门达到阈值；它们不能覆盖 identity conflict 硬阻断。

### Identity hard-block

| normalized-title identity | conflicting non-empty DOI values |
|---|---|
| Hardware-efficient adaptive equalizer for inter-satellite coherent laser communication systems | `10.1117/1.oe.63.1.018103`; `10.1117/1.oe.63.1.018103.short` |
| Widely Linear Filtering for Multi-Impairment Compensation in Coherent Optical Systems | `10.36227/techrxiv.14775957`; `10.36227/techrxiv.14775957.v1` |
| Differential phase-shift keying and channel equalization in free space optical communication system | `10.1117/1.oe.57.1.015107`; `10.1117/1.oe.57.1.015107.short` |

这里不擅自把 `.short` 或 `.v1` 解释成可合并 alias，因为 T016 冻结规则没有授权
DOI canonicalization repair。按合同立即停止，未继续 A2/A3。

### Candidate artifact

| path | bytes | sha256 | purpose |
|---|---:|---|---|
| `search-archive/2026-07-27/c15-formalization-candidate-view.json` | 549702 | `177e20384be334fcb00dc3c9a6bb1f789f6f427baa9da3740f4a5ec79e6acd39` | A1 streaming candidate/provenance/identity audit；包含 3 组 conflict |

未创建：

- `search-archive/2026-07-27/c15-step1-acquisition-pool.json`
- `search-archive/2026-07-27/c15-recent-fulltext-identity.json`

原因均为 A1 identity hard-block，不是遗漏。

## Recent/canonical 8 项矩阵

A1 硬阻断后合同禁止进入 A2/A3；下表只记录执行状态，不冒充 identity/content
结论。

| item | class | Phase A/B state |
|---|---|---|
| `10.1109/JLT.2025.3547459` | recent | `NOT_EVALUATED_A3_NOT_ENTERED` |
| `10.1109/JPHOT.2021.3062727` | recent | `NOT_EVALUATED_A3_NOT_ENTERED` |
| `10.1109/TCCN.2025.3631007` | recent | `NOT_EVALUATED_A3_NOT_ENTERED` |
| `10.1109/ACP66871.2025.11350394` | recent | `NOT_EVALUATED_A3_NOT_ENTERED` |
| `10.1109/JSAC.2022.3191346` | recent | `NOT_EVALUATED_A3_NOT_ENTERED` |
| Sato 1975 | canonical | `NOT_STARTED_PHASE_B_FORBIDDEN` |
| Godard 1980 | canonical | `NOT_STARTED_PHASE_B_FORBIDDEN` |
| Yang–Werner–Dumont 2002 | canonical | `NOT_STARTED_PHASE_B_FORBIDDEN` |

没有任何 `STAGED_NOT_PROMOTED` 或 promoted 项。

## Integrity boundaries

1. disk-only：未调用网络、search、blit、download、convert 或 web 工具。
2. 未运行 seed/MVE/simulation，未进入 Step 3，未精读，未写 Q#。
3. 未执行 A2/A3、Phase B 或 Phase C。
4. 未修改 `.sessions/**`、control/formal owner、mission-log、master/current、
   `simulation/common/params`、旧任务或旧 worker log。
5. 未修改 shared main repo papers/index；只读 shared index 与 shared papers 路径。
6. 未提交 git。

## Anomaly

三组同标题 DOI 仅差 `.short`/`.v1`，很可能是 bibliographic alias，但冻结规则
要求把它们作为不同非空 DOI 冲突处理；executor 无权原地 canonicalize 或 repair。
