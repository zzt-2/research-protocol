# Step 204 — D0 S2 sequential reducer repair and run

STATUS=BACKGROUND_RUNNING

## Bounded repair

- `statistics.py`：新增 `S2DamageHeadroomPoint` 与 `reduce_s2_damage_headroom`，只接受 exact 1620 typed rows；每 cluster 必须是 9×B1-on + 9×O1-on + 9×B1-off，拒绝 B2、缺失、重复、额外 row，并保持 9-to-1 off owner sharing。
- `science.py`：新增 exact 60-cluster S2 plan、逐 cluster atomic checkpoint/resume、B1/O1 execution、10,000-replicate seed-cluster bootstrap与两门原 gate；B2 固定 `NOT_RUN`。
- `test_d0_science_s2.py`：窄/full reducer metamorphic equivalence、非法 coverage、exact plan与 local verify binding。

## RED / GREEN

初始 RED：

```text
3 failed in 1.87s
```

失败点为缺 `reduce_s2_damage_headroom` 与缺 `s2_plan`。GREEN：

```text
3 passed in 1.89s
```

metamorphic equivalence 已逐项 PASS：对同一 1620 B1/O1 rows补入任意合法 synthetic B2 rows交给旧 full reducer，新旧 damage、recoverability、三个 cell 的整数 counts与 `physical_off_computations` exact equal；否决条件未触发。

合并 S1/S2 focused regression：

```text
9 passed in 4.00s
```

第一次后台 PID `39396` 在 0 rows暴露 CLI import 顺序问题：`verify` 错绑到 `projects/simulation/verify` package。只调整 local D0 module path优先级后重启；未改科学代码、owner/schema/gate。

## 正式后台执行

- PID：`50036`
- 命令：`python -B science.py --stage S2 --contract .../d0-defect-smoke-contract.yaml --output .../s2-damage-headroom`
- checkpoint：`projects/simulation/explore/coded-decoder-feedback/artifacts/science/s2-damage-headroom/checkpoint.jsonl`
- stdout/stderr：同目录 `run2.stdout.log` / `run2.stderr.log`
- PID file：同目录 `run2.pid`
- 首次监控：`81/1620 rows`，即 `3/60 base clusters`；进程 alive，stderr 0 bytes。
- raw/summary/receipt：完整 60 clusters 后由 runner 原子生成。

## 当前科学状态

- damage：RUNNING
- recoverability：RUNNING
- invalid replicates/terminals：RUNNING
- `S2_VERDICT=RUNNING`
- `B2=NOT_RUN`
- `formal_science_disposition=S2_DAMAGE_HEADROOM_RUNNING`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`

完整 1620 rows结束后若 damage 或 recoverability 任一 FAIL，runner只给 S2 FAIL，不运行 B2。

## 保护

- owner/schema/common/S1 artifacts 未修改；唯一 schema兼容的窄 reducer在 `statistics.py`。
- 未实现 S3/S4/C1；未 stage/commit/push；P05 未触碰。
