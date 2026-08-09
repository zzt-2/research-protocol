# Step 047 — P08/T010 lineage recovery

> 2026-08-09 | T001 | action_class=`RECOVER` | control=`CP001 / epoch 1`
> task-control validator：`PASS`
> 边界：只读恢复；未运行科学实验，未修改源码、owner、artifact 或四个 `p05_run*.log`

## Authority chain

| lineage | disposition | superseded by | current ceiling | evidence |
|---|---|---|---|---|
| P08 / D047 / V073 | **科学层 INVALID**；D047 的 coded-chain scope-change 与 baseline 入口授权仍是历史有效入口事实 | D048 / V074 | 只保留 source-auditable codec/AWGN 骨架；旧 Phase A、物理归因、有效包计数和旧 interleaver 身份均不得继承 | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2927-2949`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:3853-3871` |
| P08-R / D048 / V074 | **科学层 INVALID**；H1-H6 的 GG/oracle/identity/metric/trajectory 修复保留为 **PARTIAL engineering asset** | D049 / V075 | 不继承 V074 的 terminal、Phase A 数字、G 族关闭或 `accepted_valid=8`；只继承被 D049 明确保留的工程修复 | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2975-2988`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:3915-3923` |
| P08-R2 / D049 / V075 | receiver 边界、AST、统计合同的实现事实保留；其确认性科学终态和“恢复第 8 包”效力降为 **PARTIAL** | D051 / V077 | corrected-chain/receiver/oracle 工程资产 + 本地诊断；不得作为有效科学包、Q#/Go 或论文结论 | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3089-3119`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:4007-4033` |
| chronology correction / D051 / V077 | **VALID current authority**：无独立 pre-test freeze receipt/hash/commit，confirmatory evidence fail-closed | D058 仅作 campaign 总收口，不推翻本纠正 | G 族=`STOPPED_WITH_PARTIAL_ASSET`；`counts_as_valid_package=False`；禁止 P08-R3 或 coded/interleaving 换名恢复旧 G 轴 | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3100-3127`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:4019-4035` |
| campaign final / D058 / R010 | **VALID final projection** | 无 | P08/R/R2 全部为 `STOPPED_WITH_PARTIAL_ASSET`，不计 7 个有效包，不产生 METHOD_SIGNAL/active carrier | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3592-3609`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/R010-campaign-final-effect-and-root-cause-audit.md:13-16,28-39,56-62` |

完整 supersession 根因是：P08 漏 H1-H6；P08-R 漏 H7-H9；P08-R2 缺 immutable pre-test chronology。后一个节点只撤回前一个节点的科学有效性，不删除其被 authority 明确保留的工程资产。

## Reusable facts

| fact | VALID/PARTIAL/INVALID | exact pointer | allowed use |
|---|---|---|---|
| corrected coded identity：`k=1024, n=1536, rate=2/3` 的 5G NR BG2 rate-matched LDPC component，`num_bits_per_symbol=4` 启用真实 3GPP §5.4.2.2 bit interleaver；20 为 configured decoder iterations | **PARTIAL**（实现身份事实有效；标准一致性 ceiling 仅 source-auditable Sionna component，无独立第二 codec） | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:90-120,123-150`; `projects/simulation/results/p08r_coded_chain_repair/p08r_identity_freeze.md:6-22,30` | 作为 adapter 的 codec/BICM 起点和身份约束；只能称 generic 5G NR component，不称完整 DVB-S2 或已完成第三方 conformance |
| receiver-visible prefix：32-symbol known prefix 的 2x2 complex LS 残差给出 `sigma2_pre`，再形成 `gamma_vis=1/sigma2_pre`；equalize deployable path 不读隐藏 `gamma_bar` | **PARTIAL engineering asset** | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_chain.py:77-145,236-277`; `projects/simulation/results/p08r2_receiver_info_repair/p08r2_metamorphic_gate.json:272-273` | 作为 receiver information-boundary、prefix estimator 和 metamorphic test 起点；不把它本身包装成方法 |
| decoder 当前保证的公开返回面是 final hard bits + `num_iter_configured`；仅当 backend 返回 tuple 时才附可选 `iterations_per_cw`，没有 posterior/extrinsic、syndrome trajectory 或中途 callback | **VALID source/API fact** | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:142-178`; `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md:24-33` | 作为 adapter gap 与接口审计起点；不得把 configured iterations 或可选最终 diag 写成实际 iteration trajectory/callback |
| P08-R2 deployable 调用链的递归 AST 与隐藏-SNR metamorphic 门 | **PARTIAL engineering asset** | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:3936-3954`; `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_verify.py:90-115,235-245,368-372` | 复用为信息边界测试模式；不能证明 pre-test chronology |
| P08-R2 统计合同结构：trajectory/seed 为独立单位，预登记单一 B2 comparator、`mde_fer=0.05`、独立 delta 与可达 `EVIDENCE_INSUFFICIENT` | **PARTIAL engineering asset** | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py:45-87,101-121`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:3948-3954` | 可复用字段/schema 与统计门；本次执行没有 immutable freeze，不能继承其 confirmatory verdict |
| O0/O1/O2 oracle ladder 实现（global/block/finer local truth，scoring/headroom only） | **PARTIAL engineering asset** | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py:197-216`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2988,3103-3104` | 仅作 privileged upper-bound/headroom 接口；绝不进入 deployable decide，也不单独构成 Go |
| P08-R2 raw 局部诊断：40 trajectories；B0/B1/B2/O0/O1/O2 mean FER=`0.1546875/0.1546875/0.1484375/0.1546875/0.153125/0.1390625`；B2-O2=`0.009375 [0.0015625,0.01953125]`；B0/O2 all-codeword-fail=`3/2` | **PARTIAL diagnostic only** | `projects/simulation/results/p08r2_receiver_info_repair/p08r2_phaseA_gate.json:166-212`; D051 ceiling：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3102-3111` | 只允许定位旧 testbed/adapter 行为与复现撤回链；不得进入本轮 Q#、Go/No-Go、论文、有效包计数或“问题不存在”声称 |
| T010 callback readiness：extrinsic、syndrome/failure causal state、decoder→CPR/recovery callback 三项均 `NEW_INFRASTRUCTURE`；统一 iteration/latency/net-rate ledger 为 `NEEDS_SMALL_ADAPTER` | **VALID historical caller/source audit** | `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md:24-33`; `.sessions/2026-07-20-research-direction-lab-system/verifications.md:1000-1008` | 作为旧资产基线；classification 绑定旧 ≤1 天预算，不能因新 3–7 天范围自动改成 READY |

## Forbidden revivals

| claim/number | why invalid | authority pointer |
|---|---|---|
| P08 `PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE`、13/15/17/19 dB FER、19 dB oracle 增益、不可恢复深衰落归因、`accepted_valid=8` | H1-H6 同时失效：GG 三档错位、deployable sigma2 读循环 SNR、oracle 粒度不足、metric fallback 未冻结、interleaver 身份谎报、codeword 被当独立样本 | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2927-2949`; `projects/thesis-fso/worker-logs/step-036-p08-coded-chain.md:91-131` 仅为被撤回历史 |
| 旧 P08 “已启用 3GPP triangle interleaver” | 原调用未传 `num_bits_per_symbol=4`；后来 P08-R option A 才真正启用 | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2948`; `projects/simulation/results/p08r_coded_chain_repair/p08r_identity_freeze.md:19-22` |
| P08-R terminal、B0/B1/B2/O0/O1/O2=`0.115/0.115/0.113/0.115/0.115/0.109`、`MDE=0.2347`、`4/40`、`0.55%` headroom、V074 scientific ACCEPT | H7 equalizer 间接读隐藏 true SNR；H8 AST 不递归；H9 MDE post-hoc、CI 边界误读和 `min(B1,B2)` cherry-pick | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2975-2998`; `projects/thesis-fso/worker-logs/step-037-p08r-coded-chain-science-repair.md:58-101` 仅为被撤回历史 |
| P08-R2 definitive terminal=`PROBLEM_ABSENT...`、`counts_as_valid_package=True`、G 族科学关闭、`accepted_valid=8` | D051/V077 证明 test seeds 8000-8039 首次观察前没有独立 contract/source hash + `test_started=false` receipt/commit；confirmatory chronology fail-closed | `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3089-3119`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:4019-4033` |
| 把 P08-R2 mean FER、delta、oracle headroom、`3/40`/`2/40` 写入本轮 Q#/Go 或论文 | 数字有 raw 支持，但 current ceiling 只是 PARTIAL local diagnostic，不能承担 confirmatory scientific claim | `projects/simulation/results/p08r2_receiver_info_repair/p08r2_phaseA_gate.json:171-212`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3102-3111` |
| “V075 19/19 ACCEPT 已证明 chronology” | V075 只验证 seed 与历史不相交，未验证 pre-test receipt/hash；其 verifier `:332-335` 只算集合交集 | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_verify.py:326-335`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:4020-4025` |
| 把 T010 `CODED_CHAIN_ASSET_BLOCKED` 当 decoder-feedback 科学 Kill，或因 3–7 天新预算自动翻成 READY | D040 明定它只是旧 ≤1 天合同下的 asset-readiness blocker；当前新 topic 仍要求先完成 canonical GW，且 adapter/MVE 未授权 | `.sessions/2026-07-20-research-direction-lab-system/decisions.md:1502-1517`; `projects/thesis-fso/master-state.md:38-47` |
| 把 `hard_out=True`、configured 20 iterations 或最终 diag 当作 extrinsic/syndrome trajectory/callback | 当前 decoder 只保证最终 hard bits 与配置迭代字段；single-pass caller 没有中途 decoder→CPR/recovery 接口 | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:142-178`; `.sessions/2026-07-20-research-direction-lab-system/decisions.md:1513-1517` |

## C1/C2/C3 inherited record

| card | old class | action | collision | reopen condition | readiness gap |
|---|---|---|---|---|---|
| C1 Decoder-Aided Phase-Hypothesis Feedback | `REJECT`（旧 ≤1 天 T010） | decoder extrinsic/syndrome 重评分有限 phase hypotheses，至多一次 switch/relock，再以固定总 BP budget re-demap/re-decode | 与 D047 causal detection→relock/state-switch 动作族碰撞；若 rollback 历史 CMA state 又命中 D028 stale snapshot / 持续 SOP dwell-BER 边界 | 公开因果 extrinsic/syndrome + 分段 decoder callback + 合法 hypothesis bank；相对 receiver-only causal switch 证明 action increment，并同时守住 dwell/BER，不复用历史 snapshot | extrinsic/syndrome、hypothesis bank、分段 callback、switch state machine、latency ledger；至少 3 项 `NEW_INFRASTRUCTURE` | `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md:40-61` |
| C2 Extrinsic Soft-Symbol Iterative CPR | `REJECT`（旧 ≤1 天 T010） | `L_ext=L_post-L_apriori` 反交织为 soft-symbol expectation/reliability，驱动一次 phase/frequency update 后重译码 | 真 extrinsic CPR action 与旧 gate/scalar calibration 不同；但退化为 temperature/clip 即撞 P08 B2/F4-A，退化为 hard-DD online update 即被 P05 standard CMA 吸收 | decoder 暴露可验证 `L_ext`、coded-symbol mapping 与受控外层 callback；先证明 CMA/B2 未吸收同一 failure | soft-output/extrinsic decoder、coded-bit→symbol mapping、外层 CPR callback、两轮 latency ledger；至少 3 项 `NEW_INFRASTRUCTURE` | `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md:66-87` |
| C3 Syndrome-Triggered Recovery Control | `REJECT`（旧 ≤1 天 T010） | early syndrome/CRC failure trajectory 在因果时点触发一次 bounded relock-and-hypothesis-switch/recovery | 与 D047 detection→recovery 动作族碰撞；final CRC relabel 撞 F4-C；history rollback 撞 D028 dwell/BER Kill | 明确因果时点的 syndrome/CRC trajectory + 一次受控 recovery；相对 receiver-only trigger 证明 lead-time/action increment，在持续 SOP 下守住 dwell/BER 并排除不可恢复 deep fade | syndrome/CRC trajectory、中途 callback、recovery state machine、latency ledger；至少 3 项 `NEW_INFRASTRUCTURE` | `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md:92-113` |

三张卡的统一旧 terminal 是 `CODED_CHAIN_ASSET_BLOCKED`，不是科学 Kill；D040/V023 确认三卡均 gate 5 FAIL、C1/C3 还 gate 3 FAIL（`.sessions/2026-07-20-research-direction-lab-system/verifications.md:987-1008`）。以上只恢复旧记录，不是本轮重新分类或方法建议。

## Artifact/source map

| layer | path | current authority/use |
|---|---|---|
| P08 source | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_{coded_chain,correctness_gate,phaseA_gate}.py` | 只用于追溯 H1-H6；科学结果 INVALID。当前 worktree 与 git tracked history 均未找到任务书所指的原始 `p08_phaseA_gate.json` / raw / correctness artifacts，因此旧数字只能按 INVALID 处理，不能作 raw-backed fact。 |
| P08-R source | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_{chain,phaseA,run,verify}.py` | H1-H6 修复的部分资产来源；H7-H9 前科学结果 INVALID。 |
| P08-R artifacts | `projects/simulation/results/p08r_coded_chain_repair/` | `INVALIDATED_BY_P08R2.md:1-17` 标明科学层被替代；identity/source/schema 中被 D049/D051 保留的部分为 PARTIAL。 |
| P08-R2 source | `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_{chain,phaseA,run,verify,metamorphic_gate,h7_reproduce}.py` | 当前可复用工程起点；未实现 extrinsic/syndrome/callback，也没有 immutable pre-test receipt。 |
| P08-R2 artifacts | `projects/simulation/results/p08r2_receiver_info_repair/` | metamorphic、raw、metric 与 verifier 可作 PARTIAL engineering/local diagnostic；不可恢复 confirmatory terminal。 |
| T010 design record | `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`; system D040/V023/CP023 | C1/C2/C3 的旧卡、collision、reopen 与 ≤1 天 readiness authority。 |
| Current owner | `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`; `projects/thesis-fso/master-state.md:38-47` | 当前仅 `RECOVER_MAP / STEP1_ENTRY`；不恢复 P08 LLR science，不授权 adapter/MVE。 |

## Facts the master must independently verify

1. 先读 D051/V077，再读 D049/V075；确认 D051 只保留 engineering/local diagnostic ceiling，未恢复有效科学包（`decisions.md:3089-3125`; `verifications.md:4007-4033`）。
2. 独立运行 `git show --stat a21fdba`：应看到 runner、dev、test raw、verifier、result 与治理共 22 文件同一 commit；`git log -- .../p08r2_receiver_info_repair` 应只有 `a21fdba`。
3. 独立读 `p08r_chain.py:142-178` 与 `p08r2_phaseA.py:150-213`：确认 `hard_out=True`、final bits + diag，以及每种方法 single-pass `codec.decode(llr)`，无 extrinsic/syndrome/callback。
4. 独立读 `p08r2_chain.py:77-145,236-277` 并核 `p08r2_metamorphic_gate.json:272-273`：确认 prefix-LS/gamma-vis 工程事实与 Δ=0；这项核验不替代 chronology。
5. 独立读 T010 preflight `:24-33,37-134` 与 V023 `:987-1008`：确认三卡旧 classification、collision、reopen 和 readiness，而不是从卡名推断。

## Anomalies

1. 仓库内不存在 `scripts/validate_task_control.py`；首次按仓库相对路径调用失败。改用 Skill canonical path `C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py` 后对 T001 校验为 `PASS`。未修改项目文件来掩盖路径差异。
2. 当前 worktree 与 `git log --all --name-only` 均未找到原始 P08 的 `p08_phaseA_gate.json`、`p08_phaseA_raw_rows.json`、`p08_correctness_gate.json`、`p08_awgn_waterfall.json`；只有源码和被撤回的 worker-log/D/V。故旧 P08 数字全部标 INVALID，未伪造 raw pointer。
3. `projects/simulation/results/p08r_coded_chain_repair/INVALIDATED_BY_P08R2.md:27` 仍写“只有 P08-R2 数字可被引用”，但后续 D051/V077/D058 已把 P08-R2 降为 PARTIAL；该句是 stale snapshot，不是 current authority。
4. `projects/thesis-fso/worker-logs/step-038-p08r2-receiver-info-repair.md:38-50` 仍记 definitive terminal、G 族关闭和恢复计数；这些均被 D051/V077 压过，只可作历史执行记录。
5. D051/V077 的“grep `freeze|...` 零命中”措辞不精确：`p08r2_run.py:7,168-219` 确有文字/进程内 freeze。可复现的承重事实是对 `receipt|sha256|hashlib|test_started|prefreeze|pre_freeze|pre_test|pre-test` 的全体 `p08r2_*.py` 检索为零，且无独立 pre-test commit；不以“freeze 字样零命中”作为证据。
6. 收尾验证时，共享 worktree 在本任务启动基线之后新增 5 个 tracked `tools/litsearch/__pycache__/*cpython-312.pyc` modified 状态。task-control validator 只导入 `argparse/collections/Path/yaml`，本任务也未运行 litsearch；这些并发缓存变化不属于本任务，未清理、覆盖或纳入产出。

## Terminal

RECOVERY_COMPLETE
