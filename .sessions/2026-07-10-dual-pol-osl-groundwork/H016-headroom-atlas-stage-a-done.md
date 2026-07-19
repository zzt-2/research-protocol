# Handoff: P03 Headroom Atlas Stage A 完成，runnable 子域 LOCAL_NEGATIVE 但 DOMAIN/CANDIDATE/FAMILY 仍开放

> 来源: S077 | 交接目标: 决定 P03 的下一步——回候选池 / 扩 closure / 换候选族
> 文件名: H016-headroom-atlas-stage-a-done.md
> 日期: 2026-07-19

## 到哪了（状态）

- **宏步骤 1**（唯一强门入口）：`projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py` 已建立并通过 19 tests（11 functional + 8 独立 code-review 对抗反例）。该入口是 Direction Lab 任何 Headroom Atlas cell 运行或状态更新的唯一授权点；强制 batch-plan guard + 实时 assessment/validator SHA 匹配 + 对实时 assessment 字节重跑 `validate_claim_scope`（不信任 PASS receipt 本身）+ append-only 审计 + token 类型分离（CELL_RUN ≠ CLOSEOUT）。
- **宏步骤 2**（Stage A）：baseline-only 11 cells × 10 paired seeds 跑完。runnable 代表子域（QPSK × SNR 5/10/15/20/25 dB × f_G 30/100/1000 Hz × SOP 4e-6/4e-5 × N 512/8192 × CSI_NONE × uncoded hard decision）**0/11 cells 达到预注册 MDE 0.005**；max visible headroom = 0.00039（`qpsk-snr15-fg1000-long`，比 MDE 低 ~13×，`SUB_MDE_HEADROOM / NON_DECISIVE`）；6/11 灵敏度受限（零错误但 rule-of-three UB > MDE on 10 seeds）；4/11 测得 negative（非零错误但 oracle affine 不胜 nearest on PI-SER）。exit = `NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`。**Stage B 不触发**（无 headroom 区域）。
- **宏步骤 3**（综合 + closeout + 验证）：人类综合 `artifacts/headroom-atlas-v1/stage-a-synthesis.md`；独立 verifier 子 agent 5 区全 PASS（B001–B003/canonical 未触、B004 不存在、gate SHA binding 一致、3 cells 重算逐位一致含 P03 v1 anchor 精确复现、aggregation 自洽）；新鲜 closeout assessment + receipt 通过 validator；通过 gate `authorize_closeout` 写入审计。
- **P03 当前 status 不变**：`P03_DOMAIN_ADEQUACY_UNRESOLVED`；ML 仍禁止；B004/Queue/Registry 仍禁止；论文晋级仍禁止。
- B001–B003 / canonical-state / `common/_dual_pol_channel.py` / `common/_gg_time.py` / P03 v1 raw artifacts 全部未触（V033 独立核对）。

## 下一步干什么

**用户决策点（未选定）—— 下一对话第一件事是和用户确认走哪条**：

1. **P03 暂停回候选池**：接受 runnable 子域 LOCAL_NEGATIVE，P03 不再单独推进；回到 BatchPlan 选择既有候选族（U20 coded-LLR / U36 residual-aware / pilot-Jones 系）。
2. **建一条干净 source closure 扩域重跑 Stage A**（最有杠杆是 **16QAM**，因 D008–D014/D023 明确显示调制驱动排序变化）：先建一个 hash-bound 的 16QAM closure（不能借用未绑定的 `ber_16qam_vs_fg.py`/`sup_stress_test.py`，否则污染 canonical baseline），再扩 Stage A contract 跑 16QAM × SNR sweep。这是基础设施投资，不是 Scout 工作。
3. **换候选族**：例如 U36（residual-aware evidence），换机制不再追 residual-aware detection。

如果用户选 (2)，下一对话第一步是设计 16QAM closure 的 hash 绑定方案，而不是直接跑 cell。如果用户选 (1) 或 (3)，本 handoff 即是 P03/U19 的收尾，新候选走自己的 GW 链。

无论选哪条，**不得**：(a) 把 runnable 子域 LOCAL_NEGATIVE 外推成 candidate/family 退出；(b) 在没有 scope certificate 的情况下关 DOMAIN；(c) 启动 B004 / P03 ML / Queue/Registry / 论文晋级。

## 纪律（和下一步直接相关的约束）

- **Atlas 强门**：任何 Atlas cell 运行或 readiness/triage/canonical 状态更新必须先过 `atlas_gate.authorize` 或 `authorize_closeout`，并保存 fresh PASS receipt。直接调用 runner、伪 receipt、旧 receipt、改 assessment 后 replay 均被阻断（19 tests 含这些反例）。
- **三轴 INFRASTRUCTURE_BLOCKED 不是候选失败**：16QAM / receiver-estimated CSI / coded-output 在 P03 frozen closure 上无法运行；这是轴级 block。要扩域必须先建干净 closure，不能借未绑定的历史脚本。
- **诚实标灵敏度**：6/11 cells 灵敏度受限（零错误但 UB > MDE on 10 seeds）——这些 cells 上不能宣称"baseline 完美"，只能宣称"未观测到 headroom"。
- **不因 provenance 小问题停在文档层**：本轮发现并立即修了若干小 bug（validator 路径、cell runner seed 字段、长 N 窗口对齐），不停下汇报。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条继承 + SC-001 双偏振放宽 + 不变量 9/10/11 修正）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - Stage A artifact 存在且 SHA 在审计中绑定：查 `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/stage-a-atlas.json` + `atlas-audit.jsonl`
  - gate 19 tests 通过：跑 `/c/Users/zzt/scoop/apps/python311/current/python -m pytest projects/thesis-fso/direction-lab/tests/test_headroom_atlas_gate.py -q`
  - B001–B003/canonical 未触：跑 `git diff --quiet HEAD -- projects/thesis-fso/direction-lab/batches/B001-20260717-live projects/thesis-fso/direction-lab/batches/B002-20260718-live projects/thesis-fso/direction-lab/batches/B003-20260718-live projects/thesis-fso/direction-lab/canonical-state.yaml projects/simulation/common/_dual_pol_channel.py projects/simulation/common/_gg_time.py`
- [ ] 已检查 _registry.yaml 中本专题 `2026-07-10-dual-pol-osl-groundwork` 的 depends_on 和 conflicts_with（无 conflicts；depends_on scenario-transfer-pivot + problem-driven-redirection 均 active/closed 非 blocking）
- [ ] 已确认当前范围未违反"明确不含"（不跳框架 / 不复活 9 Kill / 不预设方向 / F1 硬件 + G2 协议排除 / 不外推 16QAM 结论）

## 接口变更（如有代码改动）

新增模块（未修改任何既有代码；不改 canonical baseline / common/ / B001-B003 / canonical-state）：

```yaml
- name: atlas_gate.authorize
  signature: "authorize(*, assessment_path: Path, receipt_path: Path, audit_path: Path, batch_plan_path: Path, validator_path: Path | None = None) -> AuthorizationToken"
  returns: AuthorizationToken(authorized, reason, assessment_sha256, validator_sha256, receipt_id, audit_identity, token_type='CELL_RUN', nonce)
  side_effect: append one AUTHORIZED or BLOCKED record to audit_path JSONL

- name: atlas_gate.authorize_closeout
  signature: "same as authorize but token_type='CLOSEOUT'"
  rule: CLOSEOUT token cannot be reused for write_summary and vice versa

- name: AtlasRunner.run_cell
  signature: "run_cell(*, cell_id: str, payload: Mapping, token: AuthorizationToken, audit_path: Path) -> Any"
  raises: UnauthorizedAtlasRun if token invalid, token_type mismatch, or audit_identity mismatch

- name: AtlasRunner.write_summary / write_closeout
  signature: "write_summary(*, token, audit_path, summary) / write_closeout(*, token, audit_path, closeout)"
  rule: write_summary requires token_type='CELL_RUN'; write_closeout requires token_type='CLOSEOUT'

- name: stage_a_cell_runner.run_cell
  signature: "run_cell(cell: Mapping, contract: Mapping, *, generator, runner, adapter, evaluator, run_b001_path: Path) -> dict"
  returns: per-cell structured verdict per stage-a-contract.v1.yaml::per_cell_verdict_schema
  closure: materialize_closure(contract) yields a context manager; cell runs must happen inside the `with` block

- name: run_stage_a.main (CLI)
  invocation: "python run_stage_a.py --contract ... --assessment ... --receipt ... --audit ... --batch-plan ... --output-dir ..."
  exit_code: 0 success, 2 BLOCKED by gate
```

claim-scope 评估 schema（无 breaking change，沿用 `direction-lab.claim-scope.v1`）：
- `atlas-pre-run-assessment.v1.yaml` 和 `atlas-closeout-assessment.v1.yaml` 都 PASS validator；两者 SLICE=`LOCAL_NEGATIVE`、DOMAIN=`UNRESOLVED`、CANDIDATE/FAMILY=`OPEN`，`scope_certificate=null`。

## 失败数据附录（如涉及路线失败）

P03/U19 的 runnable 代表子域在 baseline-only Stage A 上 LOCAL_NEGATIVE。具体失败数据（来自 `stage-a-atlas.json::cells[].decision`）：

| cell_id | visible_headroom | nearest_pi_ser | oracle_pi_ser | n_error_events | status |
|---|---|---|---|---|---|
| qpsk-snr05-nominal-short | 0.00000 | 0.19805 | 0.19922 | 18 | NO_VISIBLE_HEADROOM |
| qpsk-snr10-nominal-short | 0.00000 | 0.04531 | 0.04961 | 16 | NO_VISIBLE_HEADROOM |
| qpsk-snr15-nominal-short | 0.00000 | 0.00430 | 0.00430 | 4 | NO_VISIBLE_HEADROOM |
| qpsk-snr20-nominal-short (P03 v1 anchor) | 0.00000 | 0.00000 | 0.00000 | 0 | NO_VISIBLE_HEADROOM |
| qpsk-snr25-nominal-short | 0.00000 | 0.00000 | 0.00000 | 0 | NO_VISIBLE_HEADROOM |
| qpsk-snr20-fg100-short | 0.00000 | 0.00000 | 0.00000 | 0 | NO_VISIBLE_HEADROOM |
| qpsk-snr20-fg1000-short | 0.00000 | 0.00000 | 0.00000 | 0 | NO_VISIBLE_HEADROOM |
| qpsk-snr20-sop40e-short | 0.00000 | 0.00000 | 0.00000 | 0 | NO_VISIBLE_HEADROOM |
| qpsk-snr10-fg100-long | 0.00000 | 0.05039 | 0.05312 | 14 | NO_VISIBLE_HEADROOM |
| qpsk-snr15-fg1000-long | 0.00039 | 0.00703 | 0.00664 | 4 | SUB_MDE_HEADROOM |
| qpsk-snr20-nominal-long | 0.00000 | 0.00000 | 0.00000 | 0 | NO_VISIBLE_HEADROOM |

**3-seed 冒烟 vs 10-seed 正式的差异**：3-seed 冒烟时 `qpsk-snr05-nominal-short` 曾显示 LOCAL_HEADROOM / ADVANCE（visible_headroom=0.0065），但 10-seed 正式跑后该 cell 变为 LOCAL_NEGATIVE（oracle_pi_ser 0.199 反而略高于 nearest 0.198 on PI-SER）。这是小样本噪声的典型表现，也是预注册 MDE + rule-of-three 的理由。**不得引用 3-seed 冒烟的 ADVANCE 数字**。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 6/11 cells 灵敏度受限（零错误但 rule-of-three UB > MDE on 10 seeds） | 零错误须给置信上界 | 已在 cell verdict 里记 `zero_error_upper_bound` + `INSUFFICIENT_SENSITIVITY` 注释；Stage A summary 已分类 | 若用户选扩 seeds，可走 sequential 10→40（Stage A′）；当前 0 cell 接近 MDE，扩 seeds 不改变结论 |
| 3 轴 INFRASTRUCTURE_BLOCKED（16QAM / receiver-CSI / coded-output） | 代表域覆盖须完整 | 已逐项写明 block 理由；历史反例 disposition=EXCLUDED_WITH_JUSTIFICATION | 用户选建新 closure 时解锁；否则 DOMAIN 永久 UNRESOLVED |
| Direction Lab 37 个 pre-existing test 失败 | suite 全绿 | V030 已记录为 Windows CRLF + linked-worktree 路径债，非本轮回归 | 单独的治理清理对话 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| gate 反例覆盖 | 至少 10 类绕过 + 跨类型 token 误用 + schema 篡改 + 手算 receipt_id + 跨 workspace + append-only | batch-plan.v2.yaml transition_rule + D058 五级结论门 | 19/19（本轮） |
| Stage A cell 确定性 | 任意 cell 重算逐位一致 | P03 v1 deterministic-rerun-report 惯例 | 3/3 独立重算（V033）|
| P03 v1 anchor 保真 | SNR-20/f_g-30/N-512/seeds 11-20 全零错误，eval window {133, 261, 389} | source-equivalence-contract.v1.yaml | 1/1（V033）|
| 历史 guards | B001-B003/canonical/common 未触 | batch-plan.v2.yaml guards | empty diff（V033）|

## 下一轮

见上方"下一步干什么"。下一对话第一件事：和用户确认走 (1) 暂停回候选池 / (2) 建 16QAM closure 扩域 / (3) 换候选族。在用户拍板前不得开新实验。
