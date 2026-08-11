# Task Brief: D0 I05 fresh batch verification

> 来源: D022 / T120–T124 / step-166–170 | 产出位置: `projects/thesis-fso/worker-logs/step-171-d0-i05-fresh-batch-verification.md`
> 日期: 2026-08-11

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

## Independence / hard boundary

- 你是 T120–T124 final bytes 的唯一 fresh I05 batch verifier；不要采信 author 的 PASS/FAIL，只把 owner 和 production public API 当被验对象。
- production、owner、tests、session、P05、cache 全部只读；只可写 `step-171`。禁止 install、stage、commit、push、benchmark、science、MVE。
- 目标 12 分钟，15 分钟硬停止。到点仍无确定结论写 INCOMPLETE；不要发 follow-up readiness review。
- PASS terminal=`D0_I05_FRESH_BATCH_VERIFIED`；只关闭 CP012 的 I05 implementation/unit，不是 science PASS，也不授权 benchmark。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
contract=f6e000dcddd8661d2b52ea08de6c2a137cf7fd8f661d2ca415e9b56227ff1aaa
schemas=d5bb1bbc8e8bfeba1f057ea87f57b2fb4713fdd1f852bbe40df0a531f6cc29db
codec=5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331
contract_tests=8fa721a984f83b89c410dad93a6e061d381562268a2a72f57f42b20d5035ac8f
ordinary_tests=ef0b2b7e7b70d1add0fc0e45180455a857cf5d38f9eb58b7ce06d4ea4d04d234
codec_tests=28401d747ff13143ca828753cf910aac88974f52e0d672edc96d2916767a6d6e
statistics_tests=ad8065661452fd1f130c191404e9495f4d9d990a2f66286a5fb977925f278510
waveform_tests=f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1
step170=6a6a7c247ea57bd0a38102d2bec4dde7573feaca4410e0101317da5538435491
authority=6616784457eb4ae1fc3d1324ed12320aeb9a3cceb946f220c29615bc87b73484
```

## Fresh acceptance

1. 先核 SHA、HEAD、staging=0、P05 四日志、无新 bytecode/cache；不得清理用户工作树。
2. 独立静态/运行时 spot oracle，不复用 test helper：
   - loader final owner/identity/domain seals与 D020 exact fields；至少验证已存在的42项 loader mutation矩阵执行通过；
   - hard output恰为16x1024 binary、2048 bytes、RFC4648、CW-major/MSB-first，独立复算 zero/first-bit roots；opaque issued ref、store exact-set、codec immediate typed write anchor；
   - ordinary exact counts `27487/42967/30247/12720`、cache edges `480/1440/10800`、groups `12427/60/15000`、aggregate `26767/720`，独立复算8个 owner golden roots，验证 direct source/leaf和hard-store FK；
   - HMM exact `22800/263520/9600/13200`、4个 owner goldens、exact-rational sum；FULL exact `27487+22800=50287` 和 frozen authority；
   - unissued clone、deep entry/output/root、ledger content/status、hard store、counts、owner mismatch均 fail closed。fresh mutation/negative总数至少50，wrong_accept/reject=0/0；可把公开测试中实际执行的互异矩阵计入总数，但必须列类别和数量。
3. 用固定环境实际运行五个显式测试文件；这是唯一 final regression：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q -s projects/simulation/tests/test_d0_contract_views.py projects/simulation/tests/test_d0_ordinary_identity.py projects/simulation/tests/test_d0_receiver_codec_methods.py projects/simulation/tests/test_d0_schemas_statistics.py projects/simulation/tests/test_d0_waveform_channel.py
```

4. FULL positive必须真实完成；记录 tests pass/fail/skip、wall time、FULL incremental、authority、stdout SHA。若五文件因15分钟硬停未完成，写 INCOMPLETE，不把 focused tests 冒充 final。
5. 结束再次核 frozen production/tests/owner/P05/HEAD/staging，只有 step-171 可新增。

## Receipt

- step-171写 exact commands、exit codes、assertion/negative totals、wrong accepts/rejects、goldens/counts、pytest totals/timing/stdout SHA、所有 frozen SHA与保护结果、P0/P1/P2。
- 任一 seal/hash/count/root不符、mutation错收、FULL未完成、test fail、保护漂移 => FAIL/INCOMPLETE，不得软 PASS。
