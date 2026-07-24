# Worker Log: Pilot-Jones component temporal-semantics adjudication (T005)

> 阶段: formal GW Step 4a 维度 D (temporal-semantics adjudication)
> 授权: D065 / V039 / T005 (epoch 7, PILOT_JONES_TEMPORAL_SEMANTICS_ADJUDICATION_PACKAGE)
> worktree: .worktrees/research-direction-lab-longitudinal-test
> branch: codex/research-direction-lab-longitudinal-test | start HEAD: 46866aa3 | T004 commit (immutable): 9a250e15

## Input authority and immutable baseline

- branch `codex/research-direction-lab-longitudinal-test`, start HEAD `46866aa37bfc`, worktree clean（初始）。
- T003 immutable: `explore/pilot-jones-complex-salvage/`、`results/pilot-jones-complex-salvage/`、`tests/test_pilot_jones_complex_salvage.py` — 全程零改动。
- T004 immutable: `explore/pilot-jones-complex-repair/`、`results/pilot-jones-complex-repair/`、`tests/test_pilot_jones_complex_repair.py`、S081、本 worker-log 的 step-004 前身 — 全程零改动。
- protected 未改: `projects/thesis-fso/direction-lab/`（STATUS.v1.md / project.v1.yaml / canonical-state.yaml / state/completion-events.jsonl）、`.agents/skills/`、shared canonical generator `common/_dual_pol_channel.py`、`common/_gg_time.py`、`params.py`。
- D061–D065、V036–V039、S079–S081（含主控 amendment）、T005 任务书已完整读取并遵守。最高纪律 1–8 全部遵守：止于 Step 4a 维度 D，未进 Step 5/Contract/Execute；不找新方法；不改 protected/shared/Skill/controller；不 push。

## Phase A — V039 failure reproduction (T004 immutable, import-only)

`t004-temporal-failure-reproduction.json` 记录四项 old_behavior / expected / reproduced / source_line：

1. **per-block temporal redraw**（`semantic_channel.py:106-133` `build_jones_truth` 每 block 独立抽 U/V）→ 相邻 block Jones 不同，每 25.6 ns 无来源跳变。**reproduced**。
2. **hash() non-determinism**（`run_repair.py:163` `int(1e6 + seed*31 + hash(model_id) % 997)`）→ 两个独立 subprocess 同 seed=7500/model=M2 fingerprint 不同（`0318bcd6…` vs `1faa60a4…`，hash `8784…` vs `-4384…`）。**reproduced**。
3. **contract closure**（contract N=50000 vs runner N=20000；contract 10 test seeds vs runner 8；raw `contract_sha256`=`"repair-contract.yaml"` 字面字符串）。**reproduced**。
4. **fixed-component counterfactual**（保持 h/theta/noise/PDL 不变，固定 1 个 component Jones 跨 frame）→ 5 val seeds 平均 impairment-added headroom = **0.066 dB**，远低于 0.77 dB iid-block 伪影。**reproduced**，方向与 V039 一致。

## Phase B — T005 fixed-component semantic gates (all PASS)

- passive PDL σmax=1 / σmin=10^(-PDL/20)（V038 defect #2 fix 继承）。
- component Jones 跨整个 frame 固定（单一 2×2 矩阵，非 per-block）。
- deterministic hash-free seed `1e6 + 31·seed + MODEL_ID_INT[model]`（V039 fix）；跨进程 bit-identical（`51977d12…` ×2 不同 PYTHONHASHSEED=0/99999）。
- DGD=0 degeneracy（M3 DGD=0 → clean_component==clean_original，err=0）。
- noise 未被 component 触碰（err=1.6e-16，V038 defect #1 fix 继承）。
- **noiseless reference recovery**: M0 err=0、M2 err<1e-9、M3 err<1e-4 → reference 是合法 ceiling。
  - **关键修复**：M2 forward ordering 必须是 rotation-then-component（`clean_atm=sqrt(h)R(theta)s`，`r=J@clean_atm`）；初版误写 component-then-rotation，靠 J≈I + grid 选择仍偶发 BER=0 但 reference 不合法。已修并加 `test_reference_forward_ordering_m2` regression。

## Phase C — baseline adjudication (validation only)

B2 λ validation 扫 [1e-3,1e-2,1e-1,1.0]（M0/M2/M3 × 2 cond × 2 pilots × 5 val seeds）→ 冻结 λ=0.1（mean BER 0.0112 最低）。B\* 在 12 cell 全部 = **B1 (EMA09)**（B2 Tikhonov 一致更差；fixed 1 dB PDL cond=1.12 接近恒模，EMA 平滑占优，物理预期）。

## Phase D — formal headroom (test, B\* frozen)

12 primary cell（2 条件 × 2 pilots × M0/M2/M3），每 cell 10 fresh test seeds，per-seed paired impairment-added over M0，bootstrap 95% CI（2000 resamples）。

- **无 reference anomaly**（O 在所有 cell ≥ B\*，合法 ceiling）。
- impairment-added：最大点估计 **0.080 dB**、最大 CI 上界 **0.237 dB**，均 ≪ 0.5 dB。两个 operational p6 cell 为负（fixed PDL/DGD 不产生 headroom）。
- 独立 raw→aggregate 重算：全 12 cell 与存储一致；独立 KILL 判定 = 存储 verdict。

## Phase E — pre-registered verdict

裁决规则在 `contract.yaml §pre_registered_verdict` 先写死。全部 8 个 primary 非-M0 cell 的点估计 AND CI 上界均 <0.5 dB → **`KILL_COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY`**。

claim ceiling：complex-component PDL/PMD rescue axis 在 fixed/verified temporal model 下不重新引入方法级 gap；T002 `UNITARY_REAL_ROTATION_MCA_KILLED` 扩展到 fixed complex model。**不关闭整个 Pilot-Jones family**；4 篇 D056 全文债继续 BLOCKED；不进 Step 5。

## Integrity (self-verification, same context — status PARTIAL)

> 独立 science critic / integrity verifier 子 agent 未使用（单 GLM 对话）。按 T005 §6 规则，integrity/科学结论状态最高 PARTIAL；不得自称"双审查 PASS"。以下为执行方自验，可由主控独立复核。

- T003/T004/protected/shared 全零改动（`git status` 仅 2 个新 T005 路径：explore dir + test file）。
- fresh pytest：**T005 17 tests PASS** + legacy T003(13)+T004(25)=**38 tests PASS**（immutability）。
- 跨进程 determinism：T005 bit-identical / T004 disagree（regression 化：`test_t005_crossprocess_agrees` + `test_t004_crossprocess_disagrees`）。
- contract/result 闭包：`_assert_closure()` 跑前强制 contract N/seeds/pilots/cells = runner；`test_real_contract_sha` 验证真 SHA256。
- raw→aggregate 独立重算：全 12 cell B\*/O headroom 与存储一致；独立 verdict = 存储。
- actual SHA closure：8 源 SHA + contract SHA 全 match 实际文件。
- B\* validation 冻结（λ=0.1, B1），test 不调参。
- seeds disjoint：val{7400-7409} ∩ test{7500-7509} ∩ T002/T003/T004 excluded = empty（`test_seeds_disjoint_*`）。

## Commands and exact results

- `python projects/simulation/explore/pilot-jones-temporal-adjudication/run_probe.py` →
  A_blockwise_redraw=true / A_hash=true / A_contract=true / A_counterfactual=true (mean 0.066 dB) / B_all_pass=true.
- `python projects/simulation/explore/pilot-jones-temporal-adjudication/run_all.py`（~3 min，含 B2 λ-scan + 2 cond × 2 pilots × 3 cells × 10 val + 10 test seeds × 3 arms）→
  verdict `KILL_COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY`（max point 0.080 dB, max CI upper 0.237 dB）。
- `python -m pytest projects/simulation/tests/test_pilot_jones_temporal_adjudication.py -q` → **17 passed in 7.4s**。
- `python -m pytest projects/simulation/tests/test_pilot_jones_complex_repair.py projects/simulation/tests/test_pilot_jones_complex_salvage.py -q` → **38 passed in 1.8s**（immutability）。

## Changed files

新增（pilot-jones-temporal-adjudication/）：contract.yaml、temporal_channel.py、baselines_and_oracle.py、run_probe.py、run_all.py、_crossproc_fingerprint.py、synthesis.md。
新增 results/pilot-jones-temporal-adjudication/：t004-temporal-failure-reproduction.json、probe_val.json、probe_test.json、result.json。
新增 tests/test_pilot_jones_temporal_adjudication.py。
新增 worker-logs/step-005-pilot-jones-temporal-semantics-adjudication.md（本文件）。

## Protected/immutable verification

T003（explore/results/tests/salvage）、T004（explore/results/tests/repair、S081、step-004 worker-log）、protected（direction-lab/、.agents/skills/）、shared canonical generator（common/_dual_pol_channel.py、common/_gg_time.py）、params.py — `git status` 验证空 diff。

## Anomaly

- M2 reference forward ordering 初版误写（component-then-rotation），靠 J≈I 偶发 BER=0 但 reference 不合法；已修为 rotation-then-component 并加 regression。非数据异常，是实现 bug 修复。
- `git diff --check` 报 LF→CRLF 自动换行警告（Windows `core.autocrlf=true`，与 T004 commit 9a250e1 同基准，非内容 whitespace 错误，与 V038 `_registry.yaml` trailing whitespace 不同）。
- 独立审查不可用 → status PARTIAL（非数据异常，是 T005 §6 规则限制）。
