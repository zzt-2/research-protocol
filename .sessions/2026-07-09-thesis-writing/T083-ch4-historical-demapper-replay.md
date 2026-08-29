# Task Brief: Ch4 A1 historical-observation corrected-demapper replay

> 来源: S028 / D062 / V037 / T081–T082 | 产出位置: Ch4 scaled-unitary seam 的 `demapper_replay_*` artifacts 与 worker log
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 24
  action_class: CH4_HISTORICAL_DEMAPPER_REPLAY
  mission_checkpoint: CP024
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格重建 T071 的 4×64 historical observations，在逐窗 `realization_hash/observation_hash` 完全一致的前提下，仅用 T082 corrected global-ML demapper 重新计算各 arm BER，并按预冻结 A1 gate 判断 Ch4 承重信号是否仍存在。

## 开始前强制读取

1. active topic CP024、D062/V037、本 brief、T081 design/plan Task 2、T082 correction note/worker log；
2. `sim-preflight`、`thesis-lessons.md` 速查表与最近三条、`code-quality.md`；
3. `confirmation_manifest.json`、`confirmation_raw.json`、`run_confirmation.py`、`confirmation_reducer.py`、`development.py` 与 tests；
4. fresh task-control validator；失败立即停止。

## 冻结输入与隔离合同

- source manifest/raw 为 T071 canonical `confirmation_manifest.json` / `confirmation_raw.json`，先记录 SHA-256；不修改它们或其他 `confirmation_*`/`development_*`。
- cells、seed bases、64 windows/cell、payload symbols、B0/B1/B2/C4/O1 arms 与每 cell 参数必须从 source manifest 解析并逐项与 source raw 对照；禁止手抄后改变。
- 重用旧 `development.make_realization`、`receiver_action`、`oracle_action`、`score_action`；不引入新 RNG、B3_PSC、SNR/Np/scene 或参数。
- 对全部 256 windows，重建后的 seed、gain、realization_hash、observation_hash、payload_bits 必须等于 source raw；每 arm 的 channel NMSE、inverse residual、rho 在数值容差内等于 source raw。runtime 可变，bit_errors/BER 允许因 corrected demapper 改变。

## 文件与实现

允许新建：

1. `demapper_replay_manifest.json`：authority、source hashes、corrected demapper/code hashes、cells、arms、bootstrap seed=`2026083005`、resamples=`5000`、95% CI 与 frozen gate；
2. `run_demapper_replay.py`：启动前验证 source hashes/identity；使用项目 `save_results()` 写 `demapper_replay_raw.json`；不得接受网格/seed/arm override；
3. `reduce_demapper_replay.py`：只从 raw + manifest 复算，使用项目 `save_results()` 写 `demapper_replay_aggregate.json` 与 `demapper_replay_receipt.json`；
4. `tests/test_demapper_replay.py`：schema/source hash、single-window identity、full 256 identity census、raw-only reducer、paired bootstrap/gate unit tests；
5. generated `demapper_replay_raw.json`、`demapper_replay_aggregate.json`、`demapper_replay_receipt.json`；
6. seam `.gitattributes`：仅为上述四个新 JSON 冻结与实际生成格式一致的 `eol`，防止 checkout 后字节 SHA 漂移；
7. `projects/thesis-fso/worker-logs/step-083-ch4-historical-demapper-replay.md`。

不得修改 T082 files、common demapper、development/confirmation code、params、chapter package 或治理文件。

## 统计与 terminal

`D_window=BER_C4-BER_B2`；bootstrap 以 window 为 paired unit，每个 named comparison 重置 PCG64 seed `2026083005`，5000 resamples，报告 mean 与 2.5%/97.5% quantiles。

- `DEMAPPER_REPLAY_PASS`：256/256 observation identity、mechanism identity、schema/hash/truth firewall 全 PASS；pooled Np2 D CI upper `<0`；两个 Np4 cells 的 D CI lower 均 `<=0`。
- `DEMAPPER_CORRECTION_SIGNAL_LOST`：identity/measurement 均合法，但上述科学 gate 任一失败。
- `DEMAPPER_REPLAY_INVALID`：任一 source/hash/identity/schema/raw-only/复算失败；不得解释 BER。

不得因 terminal 调参、追加样本、换 seed、删 cell 或扩场景。

## 验证

1. 先写 tests 并验证 identity/reducer unit tests，再执行一次固定 4×64 replay；不得把测试内生成的数据写 canonical artifacts。
2. 实现者从 raw 报告四格 B2/C4 BER、paired difference/CI、pooled Np2 与 terminal，但不得写成正式论文结论。
3. 未参与实现的 reviewer 不导入 reducer，独立解析 raw 复算 256 identities、counts、CI 与 terminal；实现与审查分离。
4. 运行 focused tests、py_compile、task-control、JSON parse/hash/count、历史 artifact immutable、精确白名单与 `git diff --check`。

一次任务不 commit、不 push。PASS 只允许主控另开 A2；SIGNAL_LOST 必须停止完整 production。
