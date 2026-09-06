# Task Brief: Ch4 formal execution seam

> 来源: S028 / D066 / V041 / T086 | 产出: formal runner/reducer/tests、ID29999 OS-temp smoke、唯一 execution lock
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 28
  action_class: CH4_FORMAL_EXECUTION_SEAM
  mission_checkpoint: CP028
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在不改 `ch4_scientific_manifest.json` 的前提下，TDD实现formal runner、raw-only reducer与execution-lock生成器；用hard-coded ID29999在OS temp贯通完整119-cell网格，代码/测试最终冻结后唯一生成tracked execution lock。本任务不得运行formal IDs `30000..30127`，不得生成论文数字。

## 必读

1. sim-preflight全文及references；
2. T086、D066、V041、step-086 log与independent verification；
3. `ch4_scientific_manifest.json`、T086 tuning四件套与production_core；
4. thesis-lessons速查表+最近三条、code-quality与task-control validator。

## 文件白名单

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_ch4_formal_production.py`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_reducer.py`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_ch4_formal_production.py`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/freeze_ch4_formal_execution_lock.py`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_ch4_formal_production.py`
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_execution_lock.json`（只在最终code/tests冻结后生成一次）
- seam `.gitattributes`仅增加execution-lock稳定EOL
- `projects/thesis-fso/worker-logs/step-087-ch4-formal-execution-seam.md`
- 独立验证报告由reviewer写入Ch4 package；实现者不得写。

## Formal runtime合同

### 固定总体与census

- scientific manifest SHA必须exact=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；任何字节变化立即INVALID。
- smoke ID恰为29999；formal IDs在本任务中hard-forbidden。runner不得提供ID/grid/arm/tau/scene/Np/delta override。
- 后续formal raw的exact census预冻结：128 top-level latent IDs；384 scene-latents；每ID 119 actual cells；总actual cells=15232；每cell 5 arms；总arm rows=76160；每ID另有1个delta0 reference且无duplicate rows。
- ID29999 smoke exact census：1 latent、3 scene-latents、119 actual cells、595 arm rows、1 delta0 reference。

### 场景与配对

- 每个latent ID分别构造weak/moderate/strong scene window；不同scene由scenario-code substream区分，禁止跨scene paired/pooled CI。
- 同一scene内所有SNR/Np/mismatch共用该latent的bits/Q/g/base noises；pilot noise只取max-pilot prefix；same scene+SNR跨Np的payload observation hash必须相同。
- moderate actual cells=76 full-curve cells +5 positive-delta cells=81；weak=19；strong=19；合计119。delta0只引用moderate/Np2/25dB主cell。
- mismatch严格为 `H_delta=g Q R D_delta R^H`，R=mismatch_right；delta0 H与三observation hashes必须bit-exact主cell，positive delta共享Q/R/g/bits/base noises。

### Arms与truth

- roles恰B0/B2_TUNED/C4_FWD/B3_PSC/O1；runtime mapping与scientific manifest exact。
- B2 tau只读12-entry tuning map；B3固定tau=1；不得重调。
- O1只走separate truth-only path。deployable receiver只收`x_pilots,y_pilots,y_payload,parameter`；bits/h_true仅离线score。
- 每row至少记录bit_errors/bits/BER、channel_nmse、inverse_residual、rho、public/PSC scale、validity、action hash；B3 channel_nmse标记pre-calibration inherited。

## Raw-only reducer合同

- 不导入runner，不读历史aggregate作科学输入；先核scientific manifest、execution lock、raw schema/census/IDs/cells/arms/hashes/pairing/truth marker。
- synthetic tests必须覆盖exact census、missing/duplicate/wrong-role/wrong-tau/truth/hash/scene-pooling/delta0 identity fail-close。
- per-cell BER由total counts；paired cell diff按manifest seed2026083008/5000/reset named comparison/128 latent clusters。
- required-SNR/crossing严格按manifest的BELOW_RANGE/UNREACHED/exact/stable/unstable；whole-curve bootstrap seed2026083007/5000，每sampled latent携全slice 19 SNR rows，valid<4500则CROSSING_UNSTABLE。
- grade只接受variants C4_FWD/B3_PSC、primary moderate Np2/Np4 exact keys；A/B/C/F穷尽，artifact invalid单列。
- reducer同时输出机制/场景/导频/mismatch的raw-derived summary，但这些不得改变grade。

## TDD、smoke与execution lock顺序

1. 先写tests取得真实RED，再最小实现到GREEN；不得运行ID29999。
2. 独立static reviewer对runner/reducer/truth/census/crossing/bootstrap审到P0/P1=0后，使用临时execution lock在OS temp运行一次ID29999完整119-cell smoke；输出目录必须位于`tempfile.gettempdir()`且不属于`git worktree list`任一root。
3. smoke reducer必须返回`FORMAL_SMOKE_STRUCTURAL_PASS`，允许真实曲线UNREACHED/CROSSING_UNSTABLE但不定grade、不报告科学数字；失败则只修seam并重新走RED/GREEN，tracked lock仍不得生成。
4. smoke后冻结runner/reducer/entry/tests，fresh tests+py_compile后唯一生成`ch4_formal_execution_lock.json`。lock绑定scientific-manifest SHA、runner/reducer-core/reducer-entry/tests、base commit=`d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`、Python/NumPy/platform environment与frozen core/common/scaled/params hashes。
5. tracked lock生成后不得再改上述代码/测试；独立reviewer现场复核actual hashes。任何变化令T087 INVALID，不得自动重签。

## 禁止

- 不运行IDs30000..30127，不生成formal raw/aggregate/receipt；
- 不改scientific manifest、T086 artifacts、production_core/common/scaled、Skill/controller、论文正文；
- 不检索/下载/补Groundwork/恢复Ch5/新建候选；
- 不因ID29999数字改网格、tau、阈值、bootstrap、grade、arm或claim。

## 终态

- `CH4_FORMAL_EXECUTION_SEAM_READY`：TDD、ID29999、execution lock与独立验证全部PASS；
- `CH4_FORMAL_EXECUTION_SEAM_INVALID`：任一hash/schema/census/pairing/truth/reducer/lock失败；只修seam，formal IDs继续禁止。
