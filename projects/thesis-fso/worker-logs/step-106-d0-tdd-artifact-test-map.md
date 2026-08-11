# Step 106 — D0 v3 TDD、artifact 与非科学 benchmark test map

> 2026-08-10 | T060 / D011 / V005 / CP012 / epoch 12 | CONTRACT_STATIC_CHECK
> 证据 worktree：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
> 边界：只读 owner、step-096/097/099/101/102/103、H004、code-quality 与既有测试/verify模板；唯一写入本日志。未 import 项目、未运行 pytest、D0、benchmark 或 science。

## 1. Findings first / verdict

~~~text
VERDICT = TDD_TEST_MAP_READY
UNAUTOMATABLE_FROZEN_INVARIANTS = 0
TRUTHVIEW_REQUIRED_BY_RECEIVER_TESTS = NO
ORDER_DEPENDENT_FLOAT_REQUIRED = NO
TEST_TIME_REFIT_REQUIRED = NO
SCIENTIFIC_SEED_OR_ESTIMAND_REQUIRED_BY_BENCHMARK = NO
TEST_BATCH_OVER_15_MIN_REQUIRED = NO
HARD_BLOCKER = NO
~~~

1. v3 的 physical、receiver、B1、B2、typed raw、dev-freeze、artifact、S4 与 cost invariant 均能落成 exact、metamorphic、negative-control、roundtrip、hash 或 chronology oracle；没有只能靠人工判断的冻结项。
2. ReceiverView/TruthView 可用 frozen dataclass、字段白名单、签名边界和“只变 Truth、Receiver 输出不变”的 metamorphic test 四层隔离。deployable 测试不需要把 TruthView 传入 receiver。
3. HMM winner 可由 canonical binary64 的 exact integer/power-of-two aggregate复算；ordinary float sum是明确 negative control。
4. test runner 只接收 ResolvedDevFreeze，fit API只接收8000–8009；类型、seed guard、tripwire与静态调用图可共同证明test-time refit不可达。
5. 12分钟benchmark可只用root seed 900000001、合成ReceiverView/ResolvedDevFreeze与工程estimand，不读取8000–8349注册seed，不生成S1–S4 raw，也不计算scientific gate。
6. deterministic/unit test可拆八个小批，单批预估低于90秒；实际benchmark独立720秒，仍低于15分钟。

## 2. 文件树与依赖边界

未来production root固定为：

~~~text
projects/simulation/explore/coded-decoder-feedback/
  contract.py       # frozen config、ReceiverView/TruthView、seed/cell/manifest
  waveform.py       # prefix/pilot/data-time-map、Gray-16QAM
  channel.py        # GG/Wiener/AWGN named SeedSequence
  receiver.py       # prefix LS、scalar equalizer、BPS、four-state resolve
  codec.py          # P08 mapping/demapping、fresh LDPC wrapper
  methods.py        # B0/B1/O1、controlled fixture
  b2.py             # state model、posterior、LLR、one-way decode
  schemas.py        # strict raw/dev/ledger validators
  freeze.py         # five BPS + five statistic + one tuple
  statistics.py     # S1/S2/S3 deterministic reduction/bootstrap
  artifacts.py      # canonical JSONL、atomic write、SHA/receipt
  benchmark.py      # engineering-only throughput/projection
  verify.py         # S4 evidence、artifact/cost checks
~~~

测试文件精确冻结为：

~~~text
projects/simulation/tests/test_d0_contract_views.py
projects/simulation/tests/test_d0_waveform_channel.py
projects/simulation/tests/test_d0_receiver_codec_methods.py
projects/simulation/tests/test_d0_b2_math.py
projects/simulation/tests/test_d0_schemas_statistics.py
projects/simulation/tests/test_d0_dev_freeze.py
projects/simulation/tests/test_d0_artifacts_cost_s4.py
projects/simulation/tests/test_d0_engineering_benchmark.py
~~~

每个测试文件自行将D0 root加入sys.path，不修改全局conftest.py或common/。复用测试pattern只限：oversampled smoke的frozen view/truth与fresh output hash；adaptive phase的legal pi/2与truth denylist；B10的order-independent tie、PK与atomic replace；prompt013的write-failure preservation；JSON encoding的UTF-8。既有save_results不是D0完成态writer。

## 3. 精确 test-case map

RED指生产行为尚缺导致的目标assertion/NotImplementedError；collection、路径、依赖或fixture错误不算RED。新module首个test可有一次ModuleNotFoundError bootstrap RED。

### 3.1 test_d0_contract_views.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| CV01 test_contract_control_is_cp012_implementation_only | v3 YAML | schema v3；epoch12/CP012/D011/V005；implementation/unit/benchmark true；execution/science false | control未执行或误放science | schema/control | <0.2s |
| CV02 test_population_manifest_has_exact_twelve_cells | 4×3 grid | 12唯一cell；1024/1536/16/384/6144/20 exact | manifest/default漂移 | population | <0.2s |
| CV03 test_seed_registry_exact_and_pairwise_disjoint | 八ranges | inclusive exact、交集空、错归属拒绝 | seed guard缺失 | seed_plan | <0.2s |
| CV04 test_receiver_truth_frozen_disjoint | 最小views | frozen；Receiver只allowed、无forbidden；Truth evaluator-only完整 | mutable联合对象 | views/invariants | <0.2s |
| CV05 test_receiver_rejects_truth_and_extra_fields | forbidden参数化 | tx bits、true phase/h/snr、slip/correctness/extra全拒绝 | permissive schema | views/receiver denylist | <0.2s |
| CV06 test_truth_mutation_cannot_change_receiver_result | 同Receiver、两Truth | output、BPS选择、score、receipt bytes/hash相同 | closure/global读truth | invariants/front-end | <0.5s |
| CV07 test_deployable_signatures_have_no_truth | inspect APIs | 参数/annotation/nested type无truth/h/snr/phase/payload/correctness | truth藏context | views/local posterior | <0.2s |
| CV08 test_resolved_freeze_required_by_evaluators | freeze/None | S1/S2/S3dev/S3test/S4缺freeze或hash错拒绝，同hash绑定receipt | optional freeze | chronology_lock | <0.5s |
| CV09 test_scientific_actions_disabled_cp012 | action classes | DEFECT_SMOKE/S1–S4/C1/MVE/heldout拒绝；仅四工程类允许 | control仅文本 | control/post-D0 | <0.2s |

### 3.2 test_d0_waveform_channel.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| WC01 test_registered_prefix_bytes_hashes | PCG64(987654321) | bits/labels/symbol/even/odd SHA为1168a4…6d85、31c73f…16b0、69989b…3c0、81350b…a4bc、436cdb…62a；energy1.025 | dtype/order错 | prefix | <0.2s |
| WC02 test_registered_pilot_hashes_counts | N10/20/100/200 | cycle+expanded SHA exact；pilots684/325/64/32；symbols6860/6501/6240/6208 | terminal pilot/cycle错 | periodic pilot/B2 waveform | <0.2s |
| WC03 test_data_time_map_bijective | all layouts | 6144 ranks一次；known=-1；boundary1536/3072/4608 suffix含pilots | puncture/off-by-one | layout/fixture | <0.5s |
| WC04 test_named_seedsequence_spawn_receipt | seed999901 | named order六项；spawn key/pool/state4稳定互异 | shared RNG | rng | <0.2s |
| WC05 test_stream_consumption_isolation | extra payload_x draws | GG/Wiener/AWGN X/Y首批bytes不变 | streams耦合 | rng | <0.2s |
| WC06 test_shared_gg_wiener_independent_awgn | 16 symbols | X/Y共享GG/Wiener hash，AWGN不同，重跑byte-identical | sharing matrix错 | physical sharing | <0.5s |
| WC07 test_gamma_gamma_wiener_formulas | explicit params | tau/rho与三innovation variance exact；theta0=首innovation | linewidth翻倍/Ts错 | GG/carrier | <0.2s |
| WC08 test_controlled_jump_copy_on_write | 2-pol frame | target suffix含pilots旋转；base/preboundary不变；sentinel byte-identical | in-place/只旋data | controlled fixture | <0.5s |

### 3.3 test_d0_receiver_codec_methods.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| RM01 test_prefix_ls_rss_over_31_not_32 | 32手算点 | gain闭式；Cpre=RSS/31；/32 negative control不同 | mean /32 | prefix LS | <0.2s |
| RM02 test_scalar_equalizer_per_pol_bounded | 两pol power | per-pol、max(P-Cpre,0)、公式exact、amplitude≤3、拒绝h | 2×2/truth | equalizer/polarization | <0.2s |
| RM03 test_noiseless_equalizer_no_epsilon | Cpre0 | pure inverse sqrt，finite exact | epsilon | noiseless branch | <0.2s |
| RM04 test_bps_grid_six_edge_rule | capture | (32/64)×(31/61/127)全且仅；same zero-pad/full denominator | defaults/少格 | BPS/grid | <0.5s |
| RM05 test_global_symmetry_four_states_tie | even-prefix tie | 0..3、negative pi/2、低state；八态helper tripwire不触发 | illegal resolver | symmetry | <0.2s |
| RM06 test_cpost_odd_never_equalizer | even/odd不同 | state只even、Cpost只odd；改odd不改equalizer但改demapper receipt | circular feedback | post-BPS | <0.3s |
| RM07 test_gray16_roundtrip_rotation | 16 labels | bit order全roundtrip；四pi/2 coordinate rotation保持label mapping | Gray/bit序错 | bit order/axis | <0.2s |
| RM08 test_ldpc_noiseless_roundtrip_one_cw | 1024 fixed bits | encode1536、decode原1024、无truth修正 | interleaver/layout错 | code/P08 | <5s |
| RM09 test_every_decode_fresh_state | counting factory | 每call新empty state；B1每frame8 batches、B2为2；reuse tripwire失败 | message cache | decoder contracts | <0.5s |
| RM10 test_b1_exact_reencode_nll | hand c_hat/L | mean softplus((1-2c_hat)L) exact、同bit denominator | hard error/sign错 | B1 formula | <0.2s |
| RM11 test_b1_rotation_lexicographic | 四candidate tie | 全frame单一k；低NLL/tie低k；四fresh decode | 粒度/tie错 | B1 | <0.5s |
| RM12 test_o1_evaluator_only_suffix_inverse | 9 fixtures | suffix含pilots精确逆、零error；Receiver不可调用O1 | oracle泄漏 | O1/S4 | <1s |

### 3.4 test_d0_b2_math.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| B201 test_transition_kernel_distance | p_s,d grid | rowsum1、changed=p_s、T^d=T(q_d)、row-prev/col-next | q/power错 | transition | <0.2s |
| B202 test_ps_zero_identity_no_epsilon | p_s0 | diag0/offdiag-inf；epsilon拒绝 | hidden epsilon | transition | <0.2s |
| B203 test_variance_factor_two_no_double_count | Cpost/Ecal/sigma | mu、N0、N0/2、Vx exact；phase一次 | unit/double count | variance | <0.2s |
| B204 test_single_state_p08_wrong_scale_half | nonclip sample | B2=P08(N0/2)逐值；错误N0幅值恰半且不同 | sign-only | identities | <0.5s |
| B205 test_dirac_zero_or_negative_inf | Vx0 | match0/nonmatch-inf、无NaN/epsilon | divide zero | emission | <0.2s |
| B206 test_state_permutation_llr | asymmetric posterior | T/rotation/posterior同构重排，LLR不变 | natural relabel | identity | <0.5s |
| B207 test_received_rotation_inverse_shift | received×rk | posterior u-k，LLR不变 | shift/double compensate | identity | <0.5s |
| B208 test_coordinate_rotation_no_shift | all refs×rk | label不移，LLR不变 | extra shift | identity | <0.5s |
| B209 test_uniform_state_bit_identity | multiradius | b0=b2=0、b1=b3、至少一b1非0 | all-zero错误 | identity | <0.5s |
| B210 test_local_posterior_nearest_earlier | equidistant pilots | absolute time、tie earlier、query once、normalized | data rank tie | local posterior | <0.5s |
| B211 test_llr_state_exact_inner_maxlog | hand metrics | state logsumexp、inner max、A1-A0、clip30/clamp20 | inner exact/sign错 | data LLR | <0.5s |
| B212 test_b2_one_way_no_feedback | spies | LLR decode前冻结、每polfresh一次、无callback/redecode | feedback | decoder interaction | <0.5s |

### 3.5 test_d0_schemas_statistics.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| SS01 test_raw_tables_strict_fields | valid+mutations | strict、extra forbid、finite、no NaN、互斥字段absent | loose union | serialization/tables | <1s |
| SS02 test_pk_fk_bijection_fail_closed | duplicate/bad keys | PK、seed/cell FK、fixture↔boundary/k、method/role exact | row-only | FK/invariants | <1s |
| SS03 test_s1_coverage_event | synthetic20/50 | 480/1200；event iff count；array length；controlled absent | renormalize | S1 | <0.5s |
| SS04 test_s2_off_projection_cost_separation | 1 off→9 | one computation/content/random；9 rows；charge once；on3/off1 methods | cost duplicate | twin/S2 | <0.5s |
| SS05 test_s2_pool_then_equal_cells | unequal denominators | per-cell pooled then equal3；reject row mean/global pool | order错 | estimands | <0.5s |
| SS06 test_s2_denominator_ci_boundaries | 500/9500,501 | 500 pass、501 fail、NA不填、CI unclipped | bound/impute错 | zero denom | <1s |
| SS07 test_bootstrap_local_pcg64_linear | fixed blocks | per-stratum new PCG64(2026081001)、10000、linear、stable | global RNG | uncertainty | <2s |
| SS08 test_s3_ten_cost_tie | one tied case | fixed order；changed vector和88；cache reads72 | cache decode | S3 | <0.5s |
| SS09 test_s3_lambda_chronology | dev/test | dev-only五lambda；MRR→top1→small；test false/read freeze | test leakage | lambda freeze | <0.5s |
| SS10 test_s3_case_cell_seed_bootstrap | hand miniature | case→cell→equal3、cluster seed、paired same case | candidate clustering | S3 estimands | <1s |
| SS11 test_s4_schema_seven | pass/missing/dup | IDs7/7、passed iff failed0、无seed/cell/boundary | reused schema | S4 | <0.5s |

### 3.6 test_d0_dev_freeze.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| DF01 test_manifest_grid_float_hex | manifest | 10seed、12cell、5tuple、6BPS、122+6 float.hex、enums/cardinality/双账 | only logspace text | dev manifest | <0.5s |
| DF02 test_bps_cardinality_duplicate_n | keys only | 7200 PK、两个N100逻辑row；cache不删 | exposure drop | BPS table | <0.5s |
| DF03 test_bps_selector_goodput_chain | integer counts | delivered=1024×perfect CW；reject bit-goodput；goodput→CWER→B→Nw；order independent | estimand/tie错 | common BPS | <0.5s |
| DF04 test_binary64_exact_order_chunk | catastrophic floats | integer/power2 across order/chunk identical；ordinary float不同且reject | sum/np.sum | HMM aggregate | <0.5s |
| DF05 test_hmm_members_complete_once | chunks/mutations | member/computation hash、count、normalize-before-sum、float.hex mapping | rounded mean | chunk invariants | <0.5s |
| DF06 test_hmm_excludes_sentinel_preserves_work | 10/90/90 | 0.5clean+0.5target；sentinel excluded但logical/receipt/cost存在；tie small p/sigma | 0.75/0.25或drop | B2 statistic | <0.5s |
| DF07 test_tuple_exact_key_roles | manifests | clean1200；controlled21600=10800+10800；fixture两pol；affected target only | sentinel wrong | tuple tables | <1s |
| DF08 test_final_tuple_full_chain | five candidates | goodput→pilot fraction→target ACWER→M→legal order；refs preexist | float tolerance | tuple selector | <0.5s |
| DF09 test_freeze_five_five_one_all_candidates | tables | 5+5+1；all candidate exact key/raw hash stored | winner-only | freeze | <0.5s |
| DF10 test_fit_seed_guard_nondev | all ranges+900000001 | fit仅8000–8009 | arbitrary fit | chronology | <0.2s |
| DF11 test_runner_call_graph_no_fit | tripwire+AST | evaluators/benchmark不触发三fit，无dynamic import bypass | hidden refit | chronology | <1s |
| DF12 test_receipts_one_freeze_hash | five phase receipts | identical SHA，wrong/missing reject，test rows false | unbound freeze | chronology | <0.5s |

### 3.7 test_d0_artifacts_cost_s4.py

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| AC01 test_seven_dev_artifacts_named | manifest | 七文件exact | missing/opaque | required files | <0.2s |
| AC02 test_canonical_jsonl_roundtrip | Unicode/float/None | UTF8、sort/compact、allow_nan false、bytes/hash stable | noncanonical | serialization | <0.5s |
| AC03 test_validate_before_write | invalid rows | temp前fail，old target intact | validate after | artifact | <0.5s |
| AC04 test_atomic_order_replace_failure | fake FS | same-dir temp→flush→file fsync→replace→dir fsync；failure preserves/cleans | direct open | write protocol | <0.5s |
| AC05 test_receipt_hashes_all | bundle | contract/source/code/manifest/raw/freeze/selection/seed/summary/ledger byte-match | path-only | hashes | <0.5s |
| AC06 test_receipt_last_torn_bundle | interruptions | no receipt=incomplete；old complete readable；receipt lists landed files | receipt first | artifact | <0.5s |
| AC07 test_ledger_exec_cache_bp | rows | cache source/nonmaterialized/content same；exec source null；BP=20CW；PK unique | duplicate charge | ledger | <0.5s |
| AC08 test_ledger_frozen_totals | aggregates | logical69360/1032000/20640000；materialized48900/704640/14092800；HMM8344800/16689600/7027200 | account mix | costs | <0.5s |
| AC09 test_s3_cache_no_exposure_drop | two cases | 20 computations stay；unchanged only lowers CW；no cross case/candidate | cache steals rows | S3 cost | <0.5s |
| AC10 test_s4_evidence_one_to_one | unit receipts | seven independent evidence SHAs；suite PASS不能代替 | checklist | S4 | <0.5s |
| AC11 test_s4_reducer_fail_closed | 7/6/fail/hash mismatch | only7/7+ledger gets engineering diagnostic PASS；no scientific verdict | missing pass/overreach | S4/gates | <0.5s |
| AC12 test_no_common_p05_paths | source paths/diff | only D0/test_d0；common、old P08、p05 zero | scope creep | H004 | <0.2s |

### 3.8 test_d0_engineering_benchmark.py

以下是fake clock/worker unit tests，不执行真实benchmark。

| ID / test name | fixture | oracle | RED原因 | owner path | 时长 |
|---|---|---|---|---|---:|
| EB01 test_manifest_engineering_only | seed900000001/synthetic freeze | class exact；无scientific fields；registered seeds reject | S1 mini-run | runtime/D011 | <0.2s |
| EB02 test_decoder_batches_4_8_12_16 | histogram | four sizes each executed、fresh restarts=calls | best batch only | runtime | <0.2s |
| EB03 test_one_waveform_six_bps | one waveform | six pairs，one hash，cache不删grid | incomplete grid | slice | <0.2s |
| EB04 test_one_tuple_ten_unique_views | 10 views | count10、hashes10 unique、synthetic freeze/no fit | duplicated views | slice | <0.2s |
| EB05 test_hmm_primitive_exact_aggregate | one chunk | primitive/aggregate/hash/wall separate，ordinary float reject | hidden primitive | slice | <0.2s |
| EB06 test_atomic_jsonl_receipt_io | rows | real atomic writer，bytes/rows/hash/fsync/wall/memory | omit IO | slice | <0.2s |
| EB07 test_watchdog_no_partial_pass | fake >720s | INCOMPLETE_WATCHDOG，无PASS，old receipt intact | partial pass | watchdog | <0.2s |
| EB08 test_projection_full_work_no_drop | manifest/rates | all operations/counts回算owner；missing axis reject | sample as full | forbidden adjustments | <0.5s |
| EB09 test_adjustments_preserve_logical | variants | only materialized changes；logical keys/count/hash same；no state reuse | hidden drop | allowed adjustments | <0.5s |
| EB10 test_projection_pass_fail_records | artificial rates | nine fields；projected+engineering≤7d PASS、>7d hard blocker、exact7d pass | unit/threshold错 | pass/fail | <0.2s |
| EB11 test_no_scientific_rows_verdicts | writer tripwires | never raw_s1..s4/CI/gate/C1 | mixed science | flags/H004 | <0.2s |

## 4. RED → GREEN receipt

1. 先加一个nodeid，记test/owner SHA与source SHA或ABSENT。
2. 单node RED须exit非0、已执行目标test，失败为目标assertion、NotImplementedError或新module首个ModuleNotFoundError；SyntaxError、fixture typo、路径/依赖/collection error不合格。
3. stdout/stderr原bytes保存并SHA。对应GREEN前test SHA不得变；改test则旧RED作废重跑。
4. 只实现使该node通过的最小behavior；相同command/test SHA跑GREEN，记fresh output/source bundle SHA。
5. 每文件完成跑文件；全绿跑八文件。历史RED不可覆盖。

receipt至少含schema/id/time/phase、nodeid、exact command/cwd、Python与deps、owner/test/source SHA、exit code、expected/observed failure、output SHA、no-pyc/no-cache、git head、dirty paths before/after。它们是工程证据，不是scientific artifact。

## 5. Windows环境、命令与分批

Fresh fact：WSL Python3.12.3缺sionna；合法环境固定为 C:\Users\zzt\scoop\apps\python311\current\python.exe（Python3.11.9、numpy2.4.3、torch2.6.0+cu124、sionna2.0.1、yaml6.0.3、CUDA true）。

从证据worktree运行：

~~~powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <suffix>
~~~

禁止pytest cache、.pyc及coverage/cache写仓库。

| batch | suffix | wall目标 | 分点 |
|---|---|---:|---|
| U1 | projects/simulation/tests/test_d0_contract_views.py -q | <5s | 独立 |
| U2 | projects/simulation/tests/test_d0_waveform_channel.py -q | <10s | 独立 |
| U3 | projects/simulation/tests/test_d0_receiver_codec_methods.py -q | <30s | RM08若>5min单拆 |
| U4 | projects/simulation/tests/test_d0_b2_math.py -q | <10s | 独立 |
| U5 | projects/simulation/tests/test_d0_schemas_statistics.py -q | <30s | SS07若>5min单拆 |
| U6 | projects/simulation/tests/test_d0_dev_freeze.py -q | <30s | keys/small fixtures only |
| U7 | projects/simulation/tests/test_d0_artifacts_cost_s4.py -q | <15s | tmp_path |
| U8 | projects/simulation/tests/test_d0_engineering_benchmark.py -q | <10s | fake clock |
| UA | projects/simulation/tests/test_d0_*.py -q | <90s目标，12min hard | 超时按文件二分 |

## 6. 12分钟非科学 benchmark

fixtures：benchmark_id=ENGINEERING_THROUGHPUT_V1；root_seed=900000001且不在任何注册range；synthetic hash-bound ResolvedDevFreeze只固定路径，不fit/不声称winner；一个synthetic dual-pol waveform；decoder batch 4/8/12/16且fresh；同waveform六BPS；一个tuple十个hash互异ReceiverView；一个HMM chunk测primitive与lossless aggregate；JSONL+receipt走真实atomic writer。

禁止8000–8009、8050–8059、8100–8149、8150–8159、8160–8169、8170–8179、8200–8219、8300–8349；禁止S1 occurrence、S2 damage/recovery/coverage、S3 top1/MRR、S4 scientific rows、gate conjunction与C1 terminal。

实现后的单行PowerShell命令：

~~~powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'; & 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B 'projects/simulation/explore/coded-decoder-feedback/benchmark.py' --class ENGINEERING_THROUGHPUT_V1 --root-seed 900000001 --watchdog-seconds 720 --synthetic-resolved-freeze --output 'projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput'
~~~

内部watchdog=720s；实际执行前须独立code review PASS，本日志不授权运行。超时输出BENCHMARK_INCOMPLETE_WATCHDOG且无PASS；除非完成工作的保守下界已证实>7d，否则不冒充GREATER_THAN_7D_HARD_BLOCKER。

记录owner九字段device、dependency_versions、physical_api_invocations、logical_batches、cache_hits、wall_time、peak_memory、projected_full_D0_time，并附decoder batch、六BPS、十B2 view、HMM primitive/aggregate、I/O rows/bytes/fsync、work-manifest hash、已消耗工程时间、86400s/day。只可调vectorization、batch、content cache、chunk；logical manifest须回算owner。四slice齐、record齐、全work可投影且 projected+recorded engineering ≤7.00d才PASS；>7d为GREATER_THAN_7D_HARD_BLOCKER。缺slice/超时/缺record只INCOMPLETE，不授权science或删gate。

## 7. 独立 code-review checklist

1. Truth leakage：Receiver frozen/whitelist；signature、closure、logger、receipt无Truth；O1 evaluator-only。
2. Decoder state：B1每rotation、B0/B2每pol、S3 changed candidate均fresh；无singleton/warm/message cache/feedback。
3. Cache exposure：只降materialized；7200 BPS、两个N100、16,689,600 HMM、sentinel、S3十候选/每case均保留。
4. Exact aggregate：winner无ordinary float order-dependent reduction；integer/power2或等价superaccumulator；members不重不漏。
5. Test refit：runner只收ResolvedDevFreeze；三fit在AST/import/runtime不可达；非dev seed fail closed。
6. Physical units：RSS/31；Cpre/Cpost complex power；P08=N0/2；phase不double count；linewidth不翻倍；no SOP/2×2 LS。
7. Rotation/mapping：四pi/2；无八态helper；两个covariance不双补偿；uniform identity正确。
8. Atomic/provenance：validate-before-write；same-dir temp/fsync/replace/dir fsync；receipt最后；SHA逐byte。
9. Cost：cache materialized0；双账/HMM复算；S3不跨candidate/case；benchmark不删axis。
10. Scope：diff无common、旧P08、p05、scientific result、owner/governance越权；execution/science false。

PASS要求P0=0/P1=0，P2逐条处置。review PASS后才可benchmark；benchmark PASS后仍须新D/V/CP才能S1–S4。

## 8. Blocker audit / terminal

| 否决条件 | 结论 | oracle |
|---|---|---|
| invariant无oracle | 未触发 | CV/WC/RM/B2/SS/DF/AC |
| Receiver需Truth | 未触发 | CV04–07/O1 |
| winner需float order | 未触发 | DF04–06 |
| test可refit | 未触发 | CV08/DF10–12 |
| benchmark需science | 未触发 | EB01/EB11/seed900000001 |
| bus>15min | 未触发 | U1–U8/benchmark720s |

~~~text
TDD_TEST_MAP_READY
~~~

## 9. Protection receipt

- owner start SHA256=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d；asset report=ab091da7ce084435176916fc34f888e566a83f7e68a9831e6f6caa61f20e1798；H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4；T060=0f550365b4f67ec61ef1ea04463024ba6c73acad860632dd229d96bc00e3b4fb。
- p05 start SHA256=7843b048…4f11 / 735e4650…38b / c76887c6…34d / 95a1d184…21de。
- staging start=0；target initially missing。
- 唯一写入：projects/thesis-fso/worker-logs/step-106-d0-tdd-artifact-test-map.md。
- 未运行import/pytest/D0/benchmark/science/web/search/download；未修改owner、治理、源码、测试、结果、p05或pycache；未commit/push。
