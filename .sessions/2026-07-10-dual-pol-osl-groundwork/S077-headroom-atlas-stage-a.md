# [S077] Headroom Atlas Stage A：唯一强门入口 + QPSK 代表域 baseline-only 诊断

> 2026-07-19 | Direction Lab Atlas 阶段 | completed
> 来源: S076（claim-scope 纠错收尾后接续）

## 目标

完成 S076/D058 列为下一对话硬前置的三件事：
1. 用 TDD 建立唯一的 Headroom Atlas preflight/assessment 强门入口（绑定 claim-scope gate + 新鲜 PASS receipt + append-only 审计 + 反例阻断）。
2. 做能力闭合，跑 staged baseline-only Stage A Headroom Atlas，回答 strongest legal non-ML baseline 在可运行代表域是否仍有可测 headroom。
3. 若找到 headroom 区域只对这些区域做 Stage B；若没找到，给出带灵敏度注释的 LOCAL_NEGATIVE + 次级结果 + 下一步。

不训练 ML、不启动 B004、不创建 Queue/Registry、不写论文数字、不退候选/族。

## 记录

### 宏步骤 1：唯一的 Atlas 强门入口（TDD）

新建 `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py`，提供：

- `authorize(...)` → CELL_RUN token；`authorize_closeout(...)` → CLOSEOUT token（token 类型分离，cell-run token 不能授权 Atlas 级退出）。
- 强制（i）batch-plan.v2.yaml 的 6 个 guard 全开，（ii）receipt 的 `assessment_sha256`/`validator_sha256` 与磁盘实时字节一致，（iii）**对实时 assessment 字节重新运行 validate_claim_scope**（不信任 PASS receipt 本身，防手写 receipt 漂白 FAIL 评估），（iv）receipt 缺失/过期/状态非 PASS 全阻断。
- `AtlasRunner.run_cell / write_summary / write_closeout` 都要求 token 且校验 `audit_identity`（绑定审计文件 canonical path，防 workspace-A 的 token 写到 workspace-B 的审计）。
- 审计 append-only（`"a"` 模式，从不 truncate），每个 authorize/run/summary/closeout 一行 JSON。

TDD：先写 `tests/test_headroom_atlas_gate.py`（11 个反例测试，覆盖 10 类绕过 + 一条 happy path），全部失败 → 实现 → 全部通过。再派独立 code-review 子 agent 加了 8 个对抗测试（CLOSEOUT↔CELL_RUN 交叉误用、`audit_path=None` 静默跳过、schema 篡改、手算 `receipt_id` 漂白 FAIL 评估、跨 workspace token、append-only 跨多次 authorize 保持），最终 **19 passed**。

宏步骤 1 通过 V033。

### 宏步骤 2：能力闭合 + staged baseline-only Stage A

**能力闭合**（直接读 frozen closure 的源码）：
- 可运行：QPSK（generator 硬编码 QPSK）/ SNR（gamma_bar）/ 动态（f_g_hz + sop_rate）/ 观测长度（N）/ CSI_NONE / uncoded hard decision。
- **INFRASTRUCTURE_BLOCKED**（轴级阻断，不是候选失败）：
  - 16QAM — `_dual_pol_channel.py` 硬编码 QPSK；历史 `ber_16qam_vs_fg.py`/`sup_stress_test.py` 存在但**不在** P03 source closure 的 hash 绑定里，借用要么改 canonical baseline（`anchor.yaml` 禁）要么新建 closure（大重建）。
  - receiver-estimated CSI / explicit pilot budget — closure 只暴露 CSI_NONE adapter。
  - soft/coded output（LLR/GMI/FER）— evaluator 是 hard-decision QPSK only；`HARD_DECISION_DOES_NOT_CLOSE_CODED_PATH` 反例仍 open。

**Stage A 合同**（`headroom-atlas/stage-a-contract.v1.yaml`）：
- MDE = 0.005 per-symbol；rule-of-three 零错误上界；sequential 10→40 seeds；INSUFFICIENT_SENSITIVITY fallback。
- 11 cells × 10 paired seeds（seeds 11–20，与 P03 v1 同），covering-array-with-anchors 设计（锚 = P03 v1 cell），跨 SNR 5/10/15/20/25 dB × f_G 30/100/1000 Hz × SOP 4e-6/4e-5 × N 512/8192。
- baseline = standard-CMA（Godard-with-z）+ nearest-QPSK；comparators = nearest/blind-affine/oracle-affine（与 P03 v1 同一组 strongest legal non-ML comparators）。

**cell runner**（`stage_a_cell_runner.py`）：复用 P03 frozen closure；窗口几何 generalize 到任意 N 并对齐 `(eval_start - half) % block_size == 0`（N=512 精确复现 P03 v1 的 133/261/389；N=8192 给出 2181/2309/2437）。

**Stage A 结果**（`artifacts/headroom-atlas-v1/stage-a-atlas.json` + summary + synthesis）：
- 0/11 cells 达到 MDE；max visible headroom = 0.00039（`qpsk-snr15-fg1000-long`，比 MDE 低 ~13×，`SUB_MDE_HEADROOM / NON_DECISIVE`）。
- 10/11 cells `NO_VISIBLE_HEADROOM / LOCAL_NEGATIVE`。
- 6/11 cells 灵敏度受限（零错误，rule-of-three UB > MDE on 10 seeds：全 SNR-20 短/长 + SNR-25 短 + sop=4e-5）。
- 4/11 cells 测得 negative（非零错误但 oracle affine 不胜 nearest：SNR 5/10/15 short + SNR-10 f_G=100 long）。
- exit = `NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`；**Stage B 不触发**（无 headroom 区域）。

### 宏步骤 3：综合 + closeout + 独立验证

- 人类可读综合 `artifacts/headroom-atlas-v1/stage-a-synthesis.md`（per-cell 表 + 五级 verdict + 次级发现 + 下一步）。
- 独立 verifier 子 agent（V033）：5 区全 PASS —— B001–B003/canonical 未触、B004 不存在、gate SHA binding 一致、3 cells 重算逐位一致（含 P03 v1 anchor 零错误精确复现）、aggregation 自洽。
- 新鲜 closeout assessment `atlas-closeout-assessment.v1.yaml` 过 validator 并写 receipt；通过 gate `authorize_closeout` + `write_closeout` 在审计里留下 CLOSEOUT_WRITTEN 记录。
- P03 当前 status 仍 `P03_DOMAIN_ADEQUACY_UNRESOLVED`：runnable 子域 LOCAL_NEGATIVE，但 16QAM/receiver-CSI/coded 三轴 INFRASTRUCTURE_BLOCKED，历史反例（D008–D015/D023）恰好落在被阻轴上 → DOMAIN/CANDIDATE/FAMILY 仍 UNRESOLVED/OPEN。

## 决策引用

- D059：建立唯一 Headroom Atlas 强门入口 + Stage A runnable 子域 LOCAL_NEGATIVE 但 DOMAIN/CANDIDATE/FAMILY 仍开放（新建）
- D058（沿用）：五级结论范围门；本 session 不推翻

## 范围确认

- 本轮是否在 scope boundary 内：是。属 D045 候选族批量探索的 P0 延续；不改变 formal GW/Contract/Execute 授权，不启动新研究方向，不退候选/族。

## 后续

- P03 在 runnable 子域 LOCAL_NEGATIVE；要关 DOMAIN/CANDIDATE 需先建 {16QAM, receiver-CSI, coded-output} 中至少一条干净 closure 并带 scope certificate 处置历史反例。这是基础设施投资，不是 Scout 工作。
- 用户决策点：① P03 暂停回候选池；② 建一条新 closure（最有杠杆是 16QAM）扩域重跑 Stage A；③ 换候选族（U36 等）。
- Stage B 不触发；ML 仍禁止；B004/Queue/Registry 仍禁止。
- 治理债：37 个 Direction Lab pre-existing test 失败（V030 已记录的 Windows CRLF/linked-worktree 债），不构成本轮回归，不假装"全 Direction Lab suite 全绿"。
