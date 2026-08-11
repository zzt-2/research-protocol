# Task Brief: D0 I02 owner-taxonomy final denylist repair (iteration 2)

> 来源: step-114 FAIL / S001 iteration counter / I02 repaired candidate | 产出位置: `projects/thesis-fso/worker-logs/step-115-d0-i02-taxonomy-final-repair.md`
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

## Hypothesis / mandatory exit

- iteration=`2`，本路线最后一次允许修复。
- 假设：将 owner 四类 forbidden 语义写成 token-combination taxonomy，而非枚举具体字符串，可同时拒绝 step114 八类及合理未见同类，又保留显式 receiver-visible safe controls。
- 否决条件：fresh re-verifier 后仍有任一 owner-equivalent alias 通过，必须标 `DENYLIST_ROUTE_REJECTED` 并转 typed/allowlisted metadata；禁止第四轮词表补丁。

## 冻结输入

```text
contract.py=b61b26c3488ff4cc851b5c57b00827a3895a896473f0db7e8f29692348ff6c50
test=c3948e072213afe23bca0700f77b3feb354a0516a7de4549842a34fccd97f9b5
step-113=2f170dce2da26871a96033fe2ab952f5dd6a562ae665a64242dd37d361556470
step-114=505dc4bc42f37d880e954a85ddc93ef7b085b2718551893aa302c6f11b4f4324
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

- Modify `projects/simulation/tests/test_d0_contract_views.py`
- Modify `projects/simulation/explore/coded-decoder-feedback/contract.py`
- Create `projects/thesis-fso/worker-logs/step-115-d0-i02-taxonomy-final-repair.md`

## TDD task

1. 完整读 T069、step114、S001 counter、owner views、current predicate/tests；核 hashes/protection。
2. **先扩 CV05 tests**：step114 八类的 raw/UPPER/hyphen variants全部拒绝，并额外加入至少以下未见组合：`info_bit_vector`, `coded_bit_vector`, `data_symbol_vector`, `actual_channel`, `oracle_channel_gain`, `injection_fixture`, `natural_event_fixture`, `codeword_final_status`。嵌套深度至少3。safe controls必须包含 `received_samples/equalized_samples/known_prefix/periodic_pilots/receiver_noise_estimate/common_cpr_phase_trace/global_rotation_state/bps_state/source_sha256/code_sha256/content_sha256/channel_source_sha256` 并保持接受。
3. production 修改前跑 CV04/CV05/CV09 exact nodes，记录 target RED 与完整缺失 rows到 step115。
4. 以四类 owner taxonomy 实现组合规则，规则本身必须短且可审计：
   - TX：payload；info/information + bit(s)；coded + bit(s)；data + symbol(s)；tx/transmitted + bits/info/coded/symbols/data。
   - physical truth：snr/cfo/fade；exact `h`；channel + true/physical/actual/oracle/realization/gain/coefficient/response/state/fade/h；phase + true/truth/physical/channel/oracle/actual。
   - event/slip：slip/event；injected/injection/natural + label/fixture/boundary/rotation/event。
   - correctness：correct/correctness；final + cw/codeword/frame/bit(s) + error(s)/status/correct(ness)。
   normalization 必须覆盖 case 与 punctuation；safe whitelist 优先级只限明示 receiver-visible names，不得用宽泛 `*_hash` 免检。
5. 保持 plain ndarray gate与 action subset语义不变。不改 CV06–08。
6. unchanged tests exact GREEN、whole file 6/6、I01 3/3；inline 回放本 task truth variants+safe controls；终检 protection。

## 边界/返回

Windows Python `-B`/no-cache/no-bytecode；禁止 benchmark/science/web/search/download/commit/push。目标8分钟，15分钟硬上限。

返回 `PASS/FAIL/INCOMPLETE`、iteration=2、RED/GREEN、taxonomy/safe counts、SHA/protection；terminal=`I02_ITERATION2_READY_FOR_FRESH_REVERIFICATION` 或 named blocker。
