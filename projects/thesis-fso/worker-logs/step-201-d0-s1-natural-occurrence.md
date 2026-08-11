# Step 201 — D0 S1 natural occurrence

STATUS=DONE

## 变更与设计

- `projects/simulation/explore/coded-decoder-feedback/science.py`：仅实现 S1 的 20 seeds × 12 cells × 2 polarizations runner、冻结 persistent-transition evaluator、逐 dual-pol frame 原子 checkpoint/resume，以及 raw/summary/receipt 落盘。
- `projects/simulation/tests/test_d0_science_s1.py`：覆盖事件无/单/32-symbol merge、first-stage exact plan、phase fail-closed、checkpoint 去重/冲突、Windows CLI import、原子 replace transient-lock retry。
- 未修改 owner YAML、`common/`、S2–S4/C1；未 stage/commit/push。

## RED / GREEN

初始入口 RED：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest 'projects/simulation/tests/test_d0_science_s1.py' -q
```

- RED：`4 failed in 0.39s`，均因 `ModuleNotFoundError: science`，是预期的缺入口失败。
- 初始 GREEN：`4 passed in 1.75s`。

同一 bounded repair 内，后台实跑暴露三个启动/落盘缺口，均先复现 RED 再最小修复：

- repo-root CLI import：RED `1 failed in 0.78s`（`ModuleNotFoundError: common`）；加入 simulation root 后 GREEN，全文件 `5 passed in 3.15s`。
- Windows checkpoint reader/AV replace race：RED `1 failed in 1.61s`（首个 `os.replace` 抛 `PermissionError`）；加入最多 100×50 ms bounded retry 后 GREEN，全文件 `6 passed in 3.40s`。
- canonical checkpoint JSON key order 与 strict typed schema order：RED `1 failed in 1.63s`；按 `schemas.TABLE_FIELDS['s1_trajectory']` 重建 mapping 后最终 GREEN：

```text
......                                                                   [100%]
6 passed in 3.67s
```

一次尝试把既有 `test_d0_schemas_statistics.py` 一并运行，约 60 s 无输出后按窄回归纪律主动终止；没有观察到测试失败，不将其计作 PASS。未重跑 I05 长链。

## 正式执行与恢复

正式命令：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B 'projects\simulation\explore\coded-decoder-feedback\science.py' --contract 'projects\thesis-fso\coded-decoder-feedback-groundwork\d0-defect-smoke-contract.yaml' --output 'projects\simulation\explore\coded-decoder-feedback\artifacts\science\s1-natural-occurrence'
```

- 首次后台 PID `36032`：CLI import RED，0 rows。
- 第二次后台 PID `50632`：在 24 frames / 48 rows 后遇到 Windows replace reader-lock；checkpoint 保留。
- 第三次后台 PID `6564`：从 48 rows 恢复，未重算前 24 frames，完成 480 rows；终态 serialization 暴露 mapping-order RED，完整 checkpoint 保留。
- 最终前台恢复从 240 个已完成 frame 起步，不重算任何 frame，只做 strict typed reduction 与最终 artifact。为避免把“已恢复 frame 数”误报成“resume 次数”，receipt 明确记录 `resumed_completed_frame_count=240`；由于前两次 pre-repair attempt 没有持久化 attempt ledger，`resume_count=null` 并标 `NOT_PERSISTED_ACROSS_PRE_REPAIR_ATTEMPTS`。
- 同理，不把最终归约的约 0.3 s 冒充完整实验 wall time：receipt 写 `wall_time_seconds=null`、`wall_time_status=NOT_CAPTURED_ACROSS_PRE_REPAIR_RESUMES`，另列 `final_invocation_wall_time_seconds=0.2974536000401713`。checkpoint 文件 CreationTime→LastWriteTime 的 `12.7518845 s` 仅为 filesystem observed span，不声称完整 wall time。

路径：

- checkpoint：`projects/simulation/explore/coded-decoder-feedback/artifacts/science/s1-natural-occurrence/checkpoint.jsonl`
- raw：`projects/simulation/explore/coded-decoder-feedback/artifacts/science/s1-natural-occurrence/s1-raw.jsonl`
- summary：`projects/simulation/explore/coded-decoder-feedback/artifacts/science/s1-natural-occurrence/summary.json`
- receipt：`projects/simulation/explore/coded-decoder-feedback/artifacts/science/s1-natural-occurrence/receipt.json`
- 后台诊断：同目录 `run*.stdout.log` / `run*.stderr.log` / `run2.pid`

## S1 数字与裁决

- `observed_trajectories=480`
- `event_count=262`
- `event_rate=0.5458333333333333`
- `distinct_event_seed_clusters=17`
- `distinct_event_physical_cells=12`
- gate：262 ≥ 12，17 ≥ 4，12 ≥ 2
- `S1_VERDICT=PASS`
- `formal_science_disposition=S1_NATURAL_OCCURRENCE_ESTABLISHED`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`

独立复算：从 `s1-raw.jsonl` 重新构造 480 个 typed `S1TrajectoryRow` 并调用 `statistics.reduce_s1`，得到相同的 `480 / 262 / 0.5458333333333333 / 17 seeds / 12 cells`。

SHA-256：

- owner contract：`f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`
- raw：`e9a5f2ad3e8ebea9d238ecfdac54b88160d4fbe4273314c9a1dcfd39fa5e75ad`
- summary：`51acd5afeb37507f0ffe6f60f24ec1f6df0e9d11eb79e60a7d15d4b5dda592b4`
- receipt：`318b80f75fa7707d2a34f8bb5a3be5977bd9ec7cef55bb100bdce02ab558be56`

## 工作树与保护

- `git status --short` 显示本任务新增 `science.py`、focused test、science artifacts 与本 step log；其余已有 session/paper/master-state/__pycache__ dirt 均未触碰或清理。
- 当前 `git_head=4e126c7fed28b0f3226f8b674c568dbc760a89fc`。这不是本 worker 创建的提交：`git reflog` 显示该提交时间为 `2026-08-11 15:03:12 +0800`、消息 `Complete coded decoder-feedback D0 hard terminal`，早于本 S1 runner 在约 15:54 首次写 checkpoint；本任务三个文件在当前仍为 `??`，证明没有被该提交纳入。本 worker 未执行任何 commit/stage/push。
- 四个 P05 文件均未修改/未 stage，SHA-256 4/4 与保护锚点一致：
  - `p05_run.log` `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log` `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log` `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log` `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`

## Concerns

- 本门只证明冻结定义下的自然 persistent-slip occurrence，不是方法 signal，不支持论文贡献声称。
- 最终 artifact 已完整；不应再次启动 S1 或升级 maximum。下一动作由主控按 S1→S2 顺序进入 B1 damage/O1 headroom。
