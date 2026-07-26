# Step 012 — C15 source recovery and canonical acquisition

## Status

- task_control: PASS
- final_status: BLOCKED_PREFLIGHT
- formal_science_disposition: PENDING_PACKAGE_COMPLETION
- mission_method_delta: NONE
- simulation_or_seed_run: false

## Raw command transcripts and exits

### command 1 — combined Phase A preflight
command:
```powershell
$ErrorActionPreference = 'Continue'
$repo = 'D:\code\study\research-protocol\.worktrees\rdl-method-production-v2'
$main = 'D:\code\study\research-protocol'
$failures = [System.Collections.Generic.List[string]]::new()
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Output 'GATE task_control'
python 'C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py' --repo-root . '.sessions\2026-07-23-research-direction-lab-longitudinal-test\T012-c15-source-recovery-and-acquire.md'
if ($LASTEXITCODE -ne 0) { $failures.Add("task_control_exit=$LASTEXITCODE") }
Write-Output 'GATE worktree_clean'
$wtStatus = @(git status --short)
$wtStatus | ForEach-Object { Write-Output $_ }
if ($LASTEXITCODE -ne 0) { $failures.Add("worktree_status_exit=$LASTEXITCODE") }
if ($wtStatus.Count -ne 0) { $failures.Add('worktree_not_clean') }
Write-Output 'GATE owners_active'
$d024 = Select-String -LiteralPath '.sessions\2026-07-06-step4a-mve-execution\decisions.md' -Pattern '^## D024|status:\s*active|状态[:：]\s*active' -Context 0,8
$d013 = Select-String -LiteralPath '.sessions\2026-07-23-research-direction-lab-longitudinal-test\decisions.md' -Pattern '^## D013|status:\s*active|状态[:：]\s*active' -Context 0,8
Write-Output "D024_markers=$(@($d024).Count)"
Write-Output "D013_markers=$(@($d013).Count)"
if (@($d024).Count -lt 2) { $failures.Add('D024_active_not_confirmed') }
if (@($d013).Count -lt 2) { $failures.Add('D013_active_not_confirmed') }
Write-Output 'GATE ancestry'
git merge-base --is-ancestor '700864de9ac2d928681201312121d178ff243ccb' HEAD
Write-Output "ancestry_exit=$LASTEXITCODE"
if ($LASTEXITCODE -ne 0) { $failures.Add('t011_commit_not_ancestor') }
Write-Output 'GATE t011_inputs'
$t011Archives = @(Get-ChildItem -LiteralPath 'search-archive\2026-07-26' -Filter 'c15-*.json' -File -ErrorAction SilentlyContinue)
$t011Archives | Sort-Object Name | ForEach-Object { Write-Output ("archive=" + $_.FullName) }
Write-Output "archive_count=$($t011Archives.Count)"
if ($t011Archives.Count -ne 7) { $failures.Add("t011_archive_count=$($t011Archives.Count)") }
$t011Log = 'projects\thesis-fso\worker-logs\step-011-c15-search-coverage.md'
Write-Output "worker_log=$t011Log exists=$(Test-Path -LiteralPath $t011Log -PathType Leaf)"
if (-not (Test-Path -LiteralPath $t011Log -PathType Leaf)) { $failures.Add('t011_worker_log_missing') }
Write-Output 'GATE forbidden_processes'
$forbidden = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(python|python3|wsl|bash)(\.exe)?$' -and $_.CommandLine -match '(?i)(simulation|mve|seed)' })
$forbidden | ForEach-Object { Write-Output ("pid=$($_.ProcessId) name=$($_.Name) cmd=$($_.CommandLine)") }
Write-Output "forbidden_process_count=$($forbidden.Count)"
if ($forbidden.Count -ne 0) { $failures.Add("forbidden_process_count=$($forbidden.Count)") }
Write-Output 'GATE main_repo_target_diffs'
$mainTargets = @('papers/index.json','papers/doi/10.1109_jlt.2025.3547459','papers/doi/10.1109_jphot.2021.3062727','papers/doi/10.1109_tccn.2025.3631007','papers/doi/10.1109_acp66871.2025.11350394','papers/doi/10.1109_jsac.2022.3191346','papers/downloads/2026-07-27','papers/manual/c15-sato-1975','papers/manual/c15-godard-1980','papers/manual/c15-yang-2002')
$mainDiff = @(git -C $main status --short -- $mainTargets)
$mainDiff | ForEach-Object { Write-Output $_ }
Write-Output "main_target_diff_count=$($mainDiff.Count)"
if ($LASTEXITCODE -ne 0) { $failures.Add("main_status_exit=$LASTEXITCODE") }
if ($mainDiff.Count -ne 0) { $failures.Add('main_targets_have_existing_diff') }
if ($failures.Count -eq 0) { Write-Output 'COMBINED_PREFLIGHT=PASS'; exit 0 }
Write-Output ('COMBINED_PREFLIGHT=FAIL ' + ($failures -join ','))
exit 1
```
stdout:
```text
GATE task_control
PASS
GATE worktree_clean
GATE owners_active
D024_markers=11
D013_markers=4
GATE ancestry
ancestry_exit=0
GATE t011_inputs
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-broad-cma-mma.json
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-broad-rca-sato.json
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-broad-rde-optical.json
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-deep-fso-taskfit.json
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-deep-lineage.json
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-deep-normalized-cost.json
archive=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\search-archive\2026-07-26\c15-deep-staged-optical.json
archive_count=7
worker_log=projects\thesis-fso\worker-logs\step-011-c15-search-coverage.md exists=False
GATE forbidden_processes
forbidden_process_count=0
GATE main_repo_target_diffs
main_target_diff_count=0
COMBINED_PREFLIGHT=FAIL t011_worker_log_missing
```
stderr:
```text
EMPTY
```
exit_code: 1

## Multi-source recovery audit

未执行。组合起飞门非 PASS 后立即停止。

## Candidate table and acquisition pool

未创建。

## Existing-fulltext closure

未执行；主仓五个 DOI 目录与 `papers/index.json` 均未修改。

## Canonical acquisition audit

未执行；未调用 blit/download/convert。

## Coverage gap report

Phase A 起飞阻塞：预期 T011 worker log
`projects/thesis-fso/worker-logs/step-011-c15-search-coverage.md` 不存在。

## Novelty collision flags

未评估。

## Integrity boundaries

- 未修改 `.sessions/**`、owner、control、master-state 或 mission-log。
- 未运行 search/blit/download/convert、Step 3、仿真、seed 或 MVE。
- 未修改共享论文库 metadata/index。
- `mission_method_delta=NONE`。

## Next gate

主控需确认 T011 worker log 的精确路径或补齐缺失 receipt，再重新派发 Phase A。
