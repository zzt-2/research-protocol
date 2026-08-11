# Task Brief: D0 I05 P1-1b — FULL artifact manifest formulas and validator

> 来源: step-124 P1-1 / step-132 P1-1a closed / independent completeness design | 产出位置: `projects/thesis-fso/worker-logs/step-134-d0-i05-full-relational-manifest.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：FULL manifest 可由冻结 contract 轴、显式 S1 extent、**预执行** HMM chunk plan 与 computation plan 生成，不读 observed rows；FULL validator 可复用已验证的 exact table/key/multiplicity gate。
- 否决：必须从 observed rows 反推 manifest；需要 count-only/`require_complete`；无法区分 FIRST_STAGE/MAXIMUM；无法在写前绑定 HMM member/computation identities 或 ledger plan；需改 contract/owner/artifact I/O；或 15 分钟未收敛。

## 冻结输入

```text
schemas.py=fb90d5c36288e226142eeb9464c1109f68db20df41a51575ad985d63514fe682
test_d0_schemas_statistics.py=03dd5dda11c79a72cc45f768c00b5969acd9834d21b6bbbd040b0409f10c36a4
step-124=b9fbdb0fe4ae27b6e98ed34b8876a3716a06057d89aa80acdf198974f4cb216f
step-129=6c8422213affdb0c1470c73b408796c4aca19822908a186786758600a9128285
step-131=86e4b831e5195c97562d3c16dc8b8fd1c2f1d75e209a6af77274526b040abca8
step-132=40e5bbb4f967b96d75152c86f2a967ff38f5a4be60f5af47e9623be36ae8ad48
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_schemas_statistics.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/schemas.py`
3. Create `projects/thesis-fso/worker-logs/step-134-d0-i05-full-relational-manifest.md`

不得修改 contract/owner/artifacts/statistics；不得创建 runner/artifact/result/cache。

## Test-first scope

1. 完整读本任务、T086/step-132、owner `seed_plan`、population、schema tables、expected cardinality/dev-freeze/HMM membership/ledger 段及 plan I05。先核 hashes/保护。
2. production 前新增 exact nodes（名称可等价但语义不可弱化）：
   - `test_full_manifest_formula_exact_coverage`
   - `test_full_manifest_required_tables_fail_closed`
   - `test_full_manifest_rejects_bad_preexecution_plans`
   旧 production 必须取得有效 RED（缺 factory/validator pending）；立即先写 step-134 RED receipt，才改 production。
3. `build_full_relational_manifest(...)` 只接 owner contract + `s1_extent` + typed/frozen **preexecution** HMM plan + typed/frozen computation plan；不得接 rows、row mappings、artifact paths或 count-only complete flag。API 命名可等价，但必须可静态看出 FULL 与 preexecution plan。
4. FULL exact table set 必须恰为 10 张：
   `s1_trajectory,s2_method,s3_candidate,s3_lambda_freeze,s4_check,computation_ledger,bps_dev_score,b2_hmm_grid_chunk,b2_tuple_clean_dev,b2_tuple_controlled_dev`。
5. factory 从 owner 轴独立枚举 exact identities，至少以 PK projection 锁定；不得只锁 row count：
   - S1 FIRST_STAGE=`20 seeds×12 cells×2 pol=480`；MAXIMUM=`50×12×2=1200`，两者互斥且未知 extent 拒绝。
   - S2=`10 seeds×3 aliases(hard/mid/clean)×2 target pol×9 fixtures×(ON 3 methods + OFF B1)=2160`；每个 60 group 恰 36。
   - S3 DEV 与 TEST 各 `10×3×2×9=540 cases×10 candidates=5400`，同表合计10800；record_type/seed set不可互换。
   - lambda freeze exact 1；S4 exact owner 7 check IDs。
   - BPS=`5 tuples×6 B/Nw pairs×10 seeds×12 cells×2 pol=7200`。
   - B2 clean=`5×10×12×2=1200`。
   - B2 controlled=`5×10×12×2 target pol×9 fixtures×2 row pol=21600`，target/sentinel各10800。
   - HMM exact groups=`5 tuples×122 p_s×6 sigma×3 roles×12 cells×2 pol=263520`；preexecution plan 还必须锁 `chunk_id/member_count/member_key_manifest_sha256/computation_ids_manifest_sha256`，roles member counts exact `10/90/90`，sentinel objective false、其余 true。错误 grid/role/cell/pol/count/duplicate/member binding 全拒绝。
   - ledger identity来自非空 typed preexecution computation plan；至少锁 `computation_id,phase,operation,cache_status,source_computation_id` 的 exact key/multiplicity，不得从 consumer rows 回推。
6. FULL coverage digest必须包含 `scope=FULL_D0_ARTIFACT`、全部 domain/seed/table projections与 preexecution-plan binding；不能复用/伪装 partial digest。FULL/PARTIAL factory与 validator交叉调用均拒绝。
7. `validate_relations`：先 exact 10-table set，再每个 projection exact key/count/multiplicity，再原 row/PK/FK/group/ledger relations；missing/empty任一表、extra table、FIRST_STAGE rows 对 MAXIMUM manifest、S2/S3/controlled 整组等量替换、HMM/ledger等量 identity 替换均须 fail closed。可抽出 shared exact-coverage helper，但 partial 行为和 tests 必须保持。
8. 测试不可从 produced rows生成期望。公式 oracle用测试常量/owner轴；如完整 263520 identities 不宜全部构造 raw rows，可测试 manifest 的独立公式投影与 fail-fast table/plan gates，并复用 step-132 已 GREEN 的 exact coverage kernel；日志必须诚实说明未构造 full scientific rows。
9. 跑新增节点、全部 schema tests、I02 regression；mutation census至少含逐表 delete/empty 20、extra、scope cross-call、两 extent mismatch、HMM/ledger plan mutations和上述 count-preserving substitutions。不得声称 I05 READY，除非 P1-1b 全关闭且 full/old regressions 全绿。
10. Windows 命令、三目标保护、≤15分钟；无 benchmark/science/web/install/commit/push/stage。到时按 test-ID boundary INCOMPLETE。

## 返回

RED/GREEN、FULL counts/digests、mutation counts、三 SHA、P1-1 状态；terminal=`I05_READY_FOR_INDEPENDENT_REVERIFICATION`、`INCOMPLETE` 或 blocker。

