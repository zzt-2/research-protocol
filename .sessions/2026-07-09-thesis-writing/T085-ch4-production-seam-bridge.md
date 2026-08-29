# Task Brief: Ch4 fixed A2 production-seam bridge

> 来源: S028 / D064 / V039 / T081–T084 | 产出位置: Ch4 scaled-unitary corrected-anchor artifacts、独立验证与 worker log
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 26
  action_class: CH4_PRODUCTION_SEAM_BRIDGE
  mission_checkpoint: CP026
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在 T084 production core 上实现并运行一次固定 A2 bridge，用新的严格配对随机总体判断：corrected-demapper 下的 C4 信号能否迁移，以及是否仍显著超过同导频信息预算的 B3_PSC。A2 是前置 stop gate，不是正式论文数据。

## 开始前强制读取

1. active topic CP026、D064/V039、本 brief、production design Stage A2 与 plan Task 4；
2. `sim-preflight`、`thesis-lessons.md` 速查表与最近三条、`code-quality.md`；
3. T083 receipt/verification、T084 core/tests/log/final verification；
4. fresh task-control validator；失败立即停止。

## 文件白名单

允许新建：

1. `corrected_anchor_manifest.json`；
2. `run_corrected_anchor.py`；
3. `corrected_anchor_reducer.py` 与 `reduce_corrected_anchor.py`；
4. `tests/test_corrected_anchor.py`；
5. generated `corrected_anchor_raw.json`、`corrected_anchor_aggregate.json`、`corrected_anchor_receipt.json`；
6. `projects/thesis-fso/worker-logs/step-085-ch4-production-seam-bridge.md`。

允许仅为四个 canonical JSON 在 seam `.gitattributes` 增加稳定 EOL。允许 runner 使用单一任务专属 checkpoint 临时文件；成功生成 canonical raw 后必须原子收口，不把不完整 checkpoint 暂存或写入论文包。

不得修改 production core/tests、common/scaled-unitary、params、T071/T083 artifacts、chapter package 或治理文件。

## 冻结 manifest

- schema/action/authority=`T085/D064/V039/CP026`，base commit 必须是包含 T084 PASS 的当前 HEAD；
- scene=`moderate`，resolved `(alpha,beta)=(4.0,1.9)` 与 central authority pointer；
- cells 恰为 `14/18 dB × Np=2/4`；每格 64 windows；payload symbols/pol=`4096`，max pilots=`4`；
- canonical latent IDs 恰为 `20000..20063`，四格共享同一组 IDs；one-latent smoke 只用 `19999` 且写临时目录，不进入 canonical raw/aggregate；
- arms=`B0/B2/B3_PSC/C4/O1`；B2/B3_PSC tau=`1.0`，其他无参数；O1 只由 runner 的 truth-only oracle 路径构造，不进入 deployable `receiver_action`；
- paired bootstrap：PCG64 seed=`2026083006`、5000 resamples、95% CI、每 named comparison reset；
- hashes 至少绑定 manifest、production_core、corrected common demapper、scaled_unitary；receipt 另绑定 runner/reducer/tests/raw/aggregate/base commit；
- 禁止 grid/seed/arm/tau override、adaptive samples 与结果后改 manifest。

## Runner 与 raw 合同

1. TDD 先冻结 manifest/schema/hash/truth-firewall/checkpoint-resume；运行 one-latent-per-cell smoke，只验证 finite/schema/pairing，输出位于临时目录且数字标记 non-thesis。
2. canonical run 恰执行 64 个 latent IDs，每个 latent 只生成一次并被四格共用；同 SNR 的 Np2/Np4 必须有相同 payload observation hash，O1 metrics 必须逐 latent bit-exact 相同。
3. 每 window 记录 latent ID、七路 namespace/component hashes、observation hashes、arm parameter、bit errors/bits/BER、channel NMSE、inverse residual、rho、public scale/PSC scale、validity；deployable arms 不得读取 truth。
4. checkpoint/resume 必须幂等：重复已完成 latent 不复制，manifest/code/base hash 不一致 fail closed；canonical raw 通过项目 `save_results()` 原子写入。
5. canonical 4×64 batch 只运行一次；不得因运行中数字改变样本、cell、tau 或 arm。

## Raw-only reducer 与统计门

- reducer 只读 raw+manifest，不导入/读取旧 aggregate 作为科学输入；pooled BER 使用 total bit counts。
- cell paired D 以 64 latent windows 为单位。pooled Np2 的两个 SNR cells 共享 latent IDs，因此 bootstrap cluster 恰为 64 个 latent IDs；每次抽中一个 ID时同时带入该 ID 的 14/18 dB 两行，不能按 128 rows 独立抽样。
- 分别计算 `D_B2=BER_C4-BER_B2` 与 `D_B3=BER_C4-BER_B3_PSC`；每 named comparison 重置冻结 RNG。
- `PRODUCTION_SEAM_BRIDGE_PASS`：pooled Np2 的 D_B2、D_B3 CI upper 均 `<0`；两个 Np4 cells 对 B2/B3_PSC 的 CI lower 均 `<=0`；schema/hash/pairing/raw-only/truth firewall/independent review 全 PASS。
- `CHEAP_COMPARATOR_NOT_CLEARED`：measurement 合法但任一科学门失败；停止 full production，不调参/扩样/换 cell。
- `PRODUCTION_SEAM_BRIDGE_INVALID`：任一 measurement/provenance/schema/hash/pairing/firewall/复算失败；只修 seam，不解释 BER。

## 验证

实现者报告 smoke 结构与 canonical 四格/pooled B2+B3 数字，但不写正式论文结论。未参与实现的 reviewer 不导入 reducer，直接从 raw 独立复算 counts、64-cluster bootstrap、O1/Np pairing、hash/firewall 与 terminal。运行 focused tests、py_compile、task-control、JSON counts、历史 immutable、精确 scope 与 `git diff --check`。

一次任务不 commit、不 push。只有经独立验证的 PASS 才允许主控另开 Task 5；其他 terminal 按 D064 强制停机。
