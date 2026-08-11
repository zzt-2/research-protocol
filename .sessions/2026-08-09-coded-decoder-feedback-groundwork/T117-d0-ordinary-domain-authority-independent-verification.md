# Task Brief: D0 ordinary domain authority repair — independent verification

> 来源: D019 / V015 / T116 / step-162 | 产出位置: `projects/thesis-fso/worker-logs/step-163-d0-ordinary-domain-authority-independent-verification.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_UNIT_TEST
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Independence / terminal

- 独立验收T116 final bytes；禁止用author helper/mutation/PASS为oracle。只写step-163，其他文件只读。
- 目标10分钟、12分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_ORDINARY_DOMAIN_AUTHORITY_REPAIR_INDEPENDENTLY_VERIFIED`；不等于I05/FULL完成。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
owner_domain_seal=15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69
contract=cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a
schemas=1d782ea4fdf187ad8c57646a65bd025de0b8a3c588c03f5e939d94063ac79a20
contract_tests=ea37c7707db3f8a22ba0a6a9b97a6a88a7b458e474b906b001a0751f3b7ee4e5
ordinary_tests=fdf9d8c1454d748d8b6eb681abc5f2ef2b783cf361f3610ce81c490542a7c19e
step162=5b59821262d54fc010d6e7e1b46b22d02c6a154052defb1a6de8fa5e1fa848b5
step161=8014dbbcdd93bbfdc63b7f2c5a3afff50fbfcf4eb725ffc3deab7683e2e80071
```

## Fresh independent matrix

1. 直接从raw owner YAML既有字段独立提取domain，不调用production projection helper；canonical复算必须精确命中seal。逐项核对aliases/pol/fixtures/candidates/S2 methods/S4 checks/tuples/B/Nw及ordinary record types/order。
2. 证明owner YAML bytes及原owner/science/identity三个seals未改；D0Contract仍四字段，loader explicit-I/O only，new domain exact frozen/typed。
3. Fresh runtime attack：独立替换至少`CANDIDATES/S2_METHODS/FIXTURES/POL/TUPLES/S4_CHECK_IDS`及等基数alias/B/Nw shadow；每种情况下build与baseline逐对象相同、assert不共同漂移。恢复后仍相同。
4. Fresh dataclass/seal mutations至少16项；domain tuple reorder/substitute/type drift、record-type swap、seal spoof、owner wrapper replace均fail closed，wrong accept/reject=0/0。
5. 独立枚举七 projection并逐条复算typed PK/work/logical ID：counts=`42967/27487`，per projection exact；S2/BPS goldens exact；shared grouping exact；fresh graph nonprimitive sharing=0。
6. 静态AST/source：ordinary compiler不得引用parallel domain globals/literals；不得新增import-time I/O；旧FULL/provenance/HMM路径无语义改动。
7. pytest：contract+ordinary=`22/22`、显式旧四文件=`54/54`，0 fail/error/skip/xfail/warning。
8. begin/end HEAD/staging/P05/cache/frozen artifacts/diff-check保护。

要求 assertions>=400、mutations>=16、global attacks>=6、all counts/goldens/tests exact、P0/P1/P2=0/0/0；否则FAIL或INCOMPLETE。step-163记录命令/exit/stdout SHA/耗时/final SHA。
