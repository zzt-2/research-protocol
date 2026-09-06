# T086: Ch4 方向—尺度解耦方法族生产冻结

> 2026-08-30 | authority: D065 / V040 / CP027 | 仅 development tuning、结构 smoke 与 formal scientific manifest freeze

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 27
  action_class: CH4_DIRECTION_SCALE_FAMILY_FREEZE
  mission_checkpoint: CP027
```
<!-- RDL-TASK-CONTROL:END -->

## 目标

把 T085 后的 Ch4 方法身份转成一次可执行且不看结果改靶的生产合同：C4 与 B3_PSC 是同一结构约束方向—尺度方法族的两种准则；先用独立 development 集冻结 tuned-B2 强基线，再做最小结构 smoke，最后冻结 formal scientific manifest 与后续 execution-lock 接口。本任务不运行 formal production，不生成论文数字。

## 启动前必读

1. `.agents/skills/sim-preflight/SKILL.md` 全文；
2. `T085-ch4-production-seam-bridge.md`、D065、V040；
3. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/production-evidence-plan.md`；
4. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/production-evidence-design.md`；
5. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_core.py` 与 T085 manifest/raw/receipt；
6. `thesis-lessons.md` 速查表与最近三条。

## 冻结方法与比较器

- `B0`: plain pilot-LS inverse；
- `B2_TUNED`: SVD-floor baseline，tau 从 development 唯一冻结；
- `C4_FWD`: `Q_hat=UV^H`，inverse scale `2/(s1+s2)`，forward-channel Frobenius 准则；
- `B3_PSC`: 固定 `tau=1`，等价于 `W=c_hat Q_hat^H`，`c_hat` 最小化 receiver-domain pilot reconstruction residual；不得继承 tuned-B2 tau；
- `O1`: truth-only upper bound，永不进入 deployable `receiver_action`。

Manifest 必须同时记录 public role 与 frozen runtime arm ID，映射恰为：`B0→B0`、`B2_TUNED→B2`、`C4_FWD→C4`、`B3_PSC→B3_PSC`、`O1→O1_TRUTH_ONLY`。public role 不得直接传入 `receiver_action`；O1 不得进入该函数。

C4/B3 是一个方法族的两个 scale criteria，不作彼此 Kill gate；正式 claim 由它们各自相对 B0/B2_TUNED 的结果限制。不得删除任一强邻居。

## Development tuning 合同

- artifacts：`b2_tuning_manifest.json`、`b2_tuning_raw.json`、`b2_tuning_aggregate.json`、`b2_tuning_receipt.json` 与专属 runner/reducer/tests；
- tuning preflight smoke ID=`20999`；canonical tuning latent IDs=`21000..21031`；formal-structure smoke ID=`21999`；三者与 T085 `19999/20000..20063`、formal `30000..30127` 零重叠；
- scenes=`weak/moderate/strong`，Np=`2/4/8/16`，SNR=`15/25/35 dB`，tau=`0/0.25/0.5/0.75/1.0`；同一 scene 内所有 SNR/Np/tau 共用同一 32-ID cluster set；
- 每个 scene×Np×tau×SNR 先汇总 32 windows 的 total errors/total bits，再算 Jeffreys BER `(errors+0.5)/(bits+1)`；三个 SNR 的 `log10(BER)` 等权平均，最小者为唯一 tau；精确相等取较小 tau；invalid window 不得丢弃或改分母；
- tuning raw 在同一 scene×Np×SNR×latent 上还必须各记录一次 C4 与固定 tau=1 的 B3；它们不参与 tau 选择，只用于可计算的 development dominance stop；
- 任一预期 row 缺失、invalid、非 finite、bits不一致或 census/hash/pairing失败，整个 tuning artifact=`CH4_FAMILY_FREEZE_INVALID`，不得把该 row 丢弃、赋 `+inf` 或继续选 tau；
- 每个 scene×Np 必须独立冻结一个 tau，不设 global fallback、不按 SNR 调参、不用 A2/smoke/formal 数字调参；
- `TUNED_BASELINE_DOMINATES_DEVELOPMENT` 的唯一定义：对全部 12 个 scene×Np，所选 B2 tau 的三 SNR 等权 mean-log10-Jeffreys objective 都同时 `<=` C4 与 B3 的同口径 objective，且至少一个比较严格 `<`；除此以外不得使用“系统性支配”终态；
- tuning receipt 必须 raw-only 复算 objective、ID census、零重叠、hash/truth firewall；development 数字明确 non-thesis。
- canonical tuning 支持唯一任务专属 checkpoint/resume：checkpoint 必须绑定 tuning manifest、runner、frozen core/common/scaled、params authority 与 base commit；已完成 latent 需确定性重建/校验后才可复用，重复不得复制。崩溃后只允许继续同一 frozen run，不得生成第二套 IDs/manifest；成功原子写 raw 后清理 checkpoint。任何 binding/record mismatch 均为 `CH4_FAMILY_FREEZE_INVALID`。

## 最小结构 smoke 与顺序

- 顺序固定为：tests/synthetic reducer RED→GREEN → tuning-runner ID `20999` 临时结构 smoke → canonical tuning grid 恰运行一次并冻结 12 个 tau → formal-structure smoke ID `21999`。不得在未选 tau 时伪造 `B2_TUNED` smoke，也不得先看 formal-structure smoke 数字再改 tau；
- 两个 smoke 均写临时目录，不进入 tracked scientific artifacts；
- formal-structure smoke cells 精确为：moderate Np2/4 at SNR `5/41`，moderate Np8/16 at `25`，weak/strong Np2 at `25`，moderate Np2@25dB mismatch `delta=0/0.4`；不跑其他笛卡尔积；
- arms 恰为 B0/B2_TUNED/C4_FWD/B3_PSC/O1；只验 finite、schema、pairing、O1 separation、unreached crossing 不崩溃，不报告或解读科学数字；
- synthetic reducer tests 同时覆盖 bracketed crossing 与合法 `UNREACHED`，smoke 无 crossing 不得触发改网格。

## Formal scientific manifest 冻结

- formal latent IDs=`30000..30127`；所有 scene/SNR/Np/mismatch 统一使用同一 128-ID census，whole-curve bootstrap cluster key=`latent_id`；
- payload symbols per polarization=`4096`；modulation=`DP-(8,8)-16APSK`；BER语义=`post-demux / pre-Ch3-CPR / uncoded pre-FEC`；工程参考阈值=`3.8e-3`，不得称编码后性能；
- 固定全 SNR 网格 `5:2:41 dB`，不设看结果后的延伸规则；
- slices：moderate Np=`2/4/8/16` 全 SNR；weak/strong Np=`2` 全 SNR；moderate Np2@25dB mismatch delta=`0/0.05/0.10/0.20/0.30/0.40`，delta=0 必须复用主曲线同一 cell而非重跑；
- mismatch 构造不得直接调用 core 的 independent left/right 形式冒充主信道连续轴。对每个 latent 冻结主方向 `Q=channel_q` 与一个独立 unitary `R=mismatch_right`，定义 `D_delta=diag(1+delta,1-delta)/sqrt(1+delta^2)`、`H_delta=g Q R D_delta R^H`。因此 `H_0=gQ` 必须与 moderate/Np2/25dB 主 cell bit-exact；所有 delta 共用 Q/R/g/bits/base pilot-noise/base payload-noise，仅改变 D_delta。`mismatch_left` 保留在 frozen latent namespace/census 中但本轴不消费，不得暗换 RNG；
- mismatch `delta=0` 只保存对主 cell 的引用，不生成第二份 observations/arm rows；tests 必须断言 H0、pilot/payload observation hash 与主 cell exact identity。delta>0 由后续 runner 在不修改 production_core 的前提下消费同一 latent window/base-noise构造；scientific manifest必须写明该 adapter公式和 component usage；
- arms 恰为 B0/B2_TUNED/C4_FWD/B3_PSC/O1；逐 scene×Np 披露 tuned tau；
- headline 固定为 C4_FWD 与 B3_PSC 各自相对 B2_TUNED 的 required-SNR gain@`3.8e-3`；C4-vs-B3 只作 scale-criterion ablation，不作显著性准入门；
- required-SNR gain 符号固定为 `SNR_required(B2_TUNED) - SNR_required(variant)`，正值表示 family variant 更好；
- crossing 由 raw total counts 的 Jeffreys BER 做 log-BER 线性插值。若最低 SNR 已 `<=threshold`，标 `BELOW_RANGE`；最高仍 `>threshold`，标 `UNREACHED`；恰好命中取最低命中 grid SNR；正常 crossing 取首个由 `>threshold` 到 `<=threshold` 的相邻区间。首个 crossing 后若再次上穿，或存在多个 downward crossings，标 `CROSSING_UNSTABLE`。这些状态都不得用 AUC/representative BER 事后替代；
- required-SNR uncertainty 使用整条曲线 joint-latent PCG64 bootstrap（scientific manifest 固定 seed=`2026083007`、5000 resamples、每 named comparison reset）；每次重采样同一 latent cluster必须携带该 slice 全 SNR rows。只在 baseline 与 variant 均为单一 stable crossing 的 replicate 上形成 gain；有效 replicates `>=4500/5000` 才计算 95% CI，否则 comparison=`CROSSING_UNSTABLE` 且不得进入 A/B grade；
- cell-level paired BER difference 固定为每个 latent 的 `BER_variant-BER_B2_TUNED`（每 window payload bits必须相等），PCG64 seed=`2026083008`、5000 resamples、每个 named `(scene,Np,SNR,variant)` comparison重置，以该 `(scene,Np)` slice 的128个 latent IDs为 paired clusters；其 CI 仅用于 grade C。不得用 total-count binomial CI 或跨cell独立样本替代；
- whole-curve与cell bootstrap的 pairing只在同一 `(scene,Np)` slice 内成立。不同 scene 由不同 scenario-code substreams生成，禁止跨 scene paired/pooled CI；scene summary逐 scene 报告，不合并伪造一个总增益；
- grade gate 必须穷尽且只读 formal raw：A=至少一个预先命名 variant 在 moderate Np2 与 Np4 的 required-SNR gain 95% CI lower都 `>0`；B=无A，但至少一个预先命名 variant 在其中一个 Np 的 lower `>0`，且同一 variant 在另一个 Np 为 stable crossing、point gain `>=0`、CI包含0；C=无A/B，但至少一个 variant 在任一 moderate Np2/4 grid cell 相对 tuned B2 的 paired BER-difference 95% CI upper `<0`；F=artifact valid但不满足A/B/C。Artifact/provenance/schema无效单列 `CH4_FORMAL_INVALID`，不得混入科学F。A/B 才进入章节定稿，C/F 返回论文结构讨论；机制图或边界图不得改变grade。

## Scientific manifest 与 execution lock 双锁

1. 本任务只冻结 scientific manifest：cells、IDs、params、methods、metrics、statistics、grade/stop rules 与 frozen core/common/scaled hashes。
2. scientific manifest 必须写入 accepted tuning lineage：`b2_tuning_manifest/raw/aggregate/receipt` 四个 SHA256、receipt terminal=`CH4_B2_TUNING_ACCEPTED` 与完整 12-entry selected-tau map；formal B2_TUNED 只能读取这张 map，不能重算或覆盖。manifest 同时绑定 `projects/simulation/params.py` SHA 与 weak/moderate/strong resolved `(alpha,beta)` snapshot；后续执行必须同时核 current hash 与 runtime-resolved values。
3. 后续 formal runner/reducer/tests 在独立 T087 先 TDD 完成；首个 formal cell 前生成 execution lock，首先绑定 scientific-manifest SHA，再绑定 runner、reducer、tests、base commit 与环境快照。
4. 两层任一不匹配 fail closed；不得把尚不存在的 T087 code hash伪写进 T086 scientific manifest。

## 允许修改

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/` 下 T086 专属 tuning runner/reducer/tests/artifacts 与 scientific manifest；
- `projects/thesis-fso/worker-logs/step-086-ch4-direction-scale-family-freeze.md`；
- seam `.gitattributes` 仅增加本任务 tracked JSON 的稳定 EOL。

## 禁止

- 不运行 formal 128-window production；
- 不改 production_core、common demapper、scaled_unitary、T085 artifacts、Skill/controller、论文正文；
- 不检索/下载论文、不补 Groundwork、不新建候选、不恢复 Ch5；
- 不依据 tuning/smoke 数字改变场景、SNR、Np、tau grid、formal population、arms、threshold、grade或claim。

## 验收与终态

- 实现者按固定顺序先 TDD 与 tuning smoke，再只运行一次完整 tuning grid，最后运行 formal-structure smoke；独立 reviewer 不导入 reducer，从 raw复算全部 12 个 tau选择与 objective/overlap/hash；
- fresh tests、py_compile、task-control、scope whitelist、history immutable 与 `git diff --check` 全 PASS；
- `CH4_FAMILY_PRODUCTION_FREEZE_READY`：tuning artifact valid、smoke structural PASS、scientific manifest完整且双锁接口可执行；
- `TUNED_BASELINE_DOMINATES_DEVELOPMENT`：tuned B2 在三 SNR development 上系统性支配 C4/B3，停止 formal production；
- `CH4_FAMILY_FREEZE_INVALID`：任一 provenance/schema/pairing/truth/overlap/reducer错误，只修 seam，不解释数字。
