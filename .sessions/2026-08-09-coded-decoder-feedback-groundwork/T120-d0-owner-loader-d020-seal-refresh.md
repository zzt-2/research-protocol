# Task Brief: D0 owner loader D020 seal refresh

> 来源: D020 / T118–T119 / step-164–165 | 产出位置: `projects/thesis-fso/worker-logs/step-166-d0-owner-loader-d020-seal-refresh.md`
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

## Scope / terminal

- 只改 `projects/simulation/explore/coded-decoder-feedback/contract.py`、`projects/simulation/tests/test_d0_contract_views.py` 与 step-166；owner/session/其他code/tests/P05/cache只读。
- 目标10分钟、15分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_OWNER_LOADER_D020_SEAL_REFRESH_READY_FOR_INDEPENDENT_VERIFICATION`；不等于owner独立终验、sidecar实现或I05完成。

## Frozen input

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
scientific_projection=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
identity=08a90d7efe7879a238771997ffae4afad5bdf23444845ae688f9f4e1a3e2143e
ordinary_domain=15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69
contract=cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a
contract_tests=ea37c7707db3f8a22ba0a6a9b97a6a88a7b458e474b906b001a0751f3b7ee4e5
step165=a0346cef7f4a5189501f35a3b174d20a2c802e973f624e8b5c91dea0cbbe747b
```

## Minimal TDD patch

1. RED first: update test-side frozen owner/identity hashes and add one focused exact D020 loader-view test before changing production constants. Run selected owner-loader nodes; failure must be caused by stale production owner seal and be captured with command/exit/stdout SHA.
2. Production change is exactly two string constants:
   - `_FROZEN_OWNER_SHA256` -> final owner above;
   - `_FROZEN_IDENTITY_BINDING_SHA256` -> final identity above.
   Do not change dataclasses, loader logic, identity keys, science/domain/grid seals, signatures, or any other production line.
3. Focused test must prove the generic typed/frozen view exposes final D020 content without aliases:
   - exact 11 new payload-schema version literals and exact field orders/constants;
   - exact runtime hard-output/provenance/group/source/count/sidecar/write-anchor values;
   - 20 total golden groups and the 10 new literal roots;
   - nested immutability and fresh-load non-aliasing for at least one new subtree.
4. Extend existing fail-closed owner mutation list from 28 to at least 40, including the previously missed `decoder_hard_output.version`, hard-output field order/base64, provenance entry order/source rule, count, sidecar filename, write order, new golden input/root, and validator obligation. All reject through public loader.
5. GREEN commands (Windows):
   - set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`;
   - run the selected RED nodes, then full `test_d0_contract_views.py`;
   - run explicit four-file regression: contract views + ordinary identity + schemas statistics + receiver codec methods + waveform channel (report exact count; no broad discovery).
6. Static/diff gate: production diff must be exactly two constants; owner/science/domain hashes unchanged; HEAD/staging/P05/cache protected.

## Receipt

- step-166 records RED/GREEN commands, exit codes, pytest counts, mutation count, hashes, protection and P0/P1/P2.
- No retries beyond one syntax/copy correction. Any semantic failure or scope drift => FAIL; timebox => INCOMPLETE.
