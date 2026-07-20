# Direction Lab：双偏振星地 OSL 研究探索入口

Direction Lab 用共享地基批量筛查"ML 在双偏振星地 OSL 接收链上是否有真实信息增量"。它分为 Scout、Sandbox 和 Promotion 三层；这里的结果不会自动修改 canonical baseline、正式 Groundwork 或论文材料。

## 流程入口（2026-07-20 cutover 后）

开放式研究方向探索的**流程拥有者**已迁移到 `.agents/skills/research-direction-lab/SKILL.md`（D008/V005）。本目录的角色：

- **日常恢复与人类决策**：[`STATUS.v1.md`](STATUS.v1.md)（renderer 输出的八问一页）
- **流程拥有者**：`../../.agents/skills/research-direction-lab/SKILL.md`（7-phase loop、candidate portfolio、batch/atlas、evidence/claims、harvest、recovery/rotation、project-layout）
- **当前项目事实（adapter 唯一拥有者）**：[`project.v1.yaml`](project.v1.yaml)（mode: READ_ONLY_MIGRATION_PREVIEW）
- **历史批次证据（protected，不可改字节）**：[`batches/`](batches/)（B001-B003）
- **本目录的旧 `process.md`**：已标 SUPERSEDED；保留为项目实例历史记录，不再拥有流程

Direction Lab 是正式晋级前的候选发现/批量筛选层；Scout/Sandbox 数字不等于 GW 完成；正式候选晋级后仍必须走 Groundwork → Contract → Execute（FR-22）。

## 当前状态

## 当前状态

- 正式研究：`BLOCKED`，唯一正式入口为 [`../master-state.md`](../master-state.md)。
- Sandbox 历史：B003 已完成并独立验证；批次事实见 [`state/completion-events.jsonl`](state/completion-events.jsonl) 与 [`state/projections/`](state/projections/)。
- 当前 Scout：P03/U19 residual-aware detection 的 Headroom Atlas Stage A 已完成（2026-07-19，S077/D059/V033）；runnable 代表子域 LOCAL_NEGATIVE；candidate 当前仍为 `P03_DOMAIN_ADEQUACY_UNRESOLVED`。
- P03 状态：历史机器出口 `P03_ANALYTIC_COVERAGE_GE_90` 只描述 10 个 QPSK/20 dB/CSI_NONE/短序列 cells。claim-scope adjudication 为 cell=`NO_VISIBLE_HEADROOM`、slice=`LOCAL_NEGATIVE`、domain=`UNRESOLVED`、candidate/family=`OPEN`。Stage A 把 LOCAL_NEGATIVE 扩展到 11 cells × 10 paired seeds 的 runnable 代表子域（QPSK × SNR 5–25 dB × f_G 30/100/1000 Hz × SOP 4e-6/4e-5 × N 512/8192 × CSI_NONE × uncoded hard decision），0/11 cells 达 MDE 0.005，exit=`NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`；但 16QAM/receiver-CSI/coded-output 三轴 INFRASTRUCTURE_BLOCKED → DOMAIN/CANDIDATE/FAMILY 仍 UNRESOLVED/OPEN。Sandbox 仍 `NOT_ENTERED`，ML 仍禁止训练，Stage B 不触发。
- B004：不存在，也不允许启动。

`canonical-state.yaml` 只物化 Direction Lab Sandbox 的机器投影，不代表正式研究授权，也不能单独充当批次历史证据。其 `BOARD_READY` 仅表示全局 board/controller 基础设施可用，不授予当前 P03 创建 Queue、Registry 或执行 Sandbox batch；批次 provenance 以 completion events 和不可变 projection 为准，正式状态与研究入口始终以 `../master-state.md` 为准。

## 已完成批次

- B001：历史 sandbox，存在协议偏差，只保留探索证据。
- B002：sandbox verified。
- B003：sandbox verified；主要价值是治理链验证，与 B002 的 U24 exact contract 研究信息重复。

B001–B003 的任何数字都不能进入论文、正式 Groundwork 或 canonical baseline。

## 当前阻断

P03 Stage A 在 runnable 代表子域给出 LOCAL_NEGATIVE，但 3 轴 INFRASTRUCTURE_BLOCKED（16QAM / receiver-estimated CSI / coded output）+ 历史反例（`MODULATION_DYNAMICS_LENGTH_ORDERING_SIGNAL` D008–D015/D023、`HARD_DECISION_DOES_NOT_CLOSE_CODED_PATH` U20）落在被阻轴上，不能形成 domain/candidate/family 退出。没有 ML 训练许可、PASS Queue、新 Registry 或 Sandbox 批次许可。

## 下一合法边界

用户决策点（未选定）：① P03 暂停回候选池；② 建一条干净 source closure（最有杠杆是 16QAM，因 D008–D014/D023 明确显示调制驱动排序变化）扩域重跑 Stage A；③ 换候选族（U36 等）。要关闭 DOMAIN/CANDIDATE 必须先扩 closure 并带 scope certificate 处置历史反例。Headroom Atlas 的唯一 receipt-bound 入口 [`scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py`](scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py) 已建立并通过 19 tests（含独立对抗审查）；Stage A artifact 在 [`scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/`](scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/)。不得把 LOCAL_NEGATIVE 改写成候选退出，也不得启动 B004、ML 训练或正式性能结论。

## 入口文件

- 正式项目状态：[`../master-state.md`](../master-state.md)
- Direction Lab 机器投影（非授权、非批次历史事实源）：[`canonical-state.yaml`](canonical-state.yaml)
- 批次状态事实源：[`state/completion-events.jsonl`](state/completion-events.jsonl) 与 [`state/projections/`](state/projections/)
- 当前 Scout 分诊：[`scout/capability-triage.v1.yaml`](scout/capability-triage.v1.yaml)
- P03 当前合同：[`scout/P03-U19-residual-headroom/scout-contract.v2.yaml`](scout/P03-U19-residual-headroom/scout-contract.v2.yaml)
- P03 readiness：[`scout/P03-U19-residual-headroom/readiness-report.yaml`](scout/P03-U19-residual-headroom/readiness-report.yaml)
- P03 probe 状态：[`scout/P03-U19-residual-headroom/residual-headroom-probe-status.yaml`](scout/P03-U19-residual-headroom/residual-headroom-probe-status.yaml)
- P03 claim-scope adjudication：[`scout/P03-U19-residual-headroom/claim-scope-assessment.v1.yaml`](scout/P03-U19-residual-headroom/claim-scope-assessment.v1.yaml)
- P03 Headroom Atlas 唯一 receipt-bound 入口：[`scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py`](scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py)
- P03 Headroom Atlas Stage A artifact：[`scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/`](scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/)（atlas JSON + summary + synthesis + verifier report + append-only audit）
- 详细流程规范：[`process.md`](process.md)
- 当前实施摘要：[`implementation-plan.md`](implementation-plan.md)
- 工作树只读审计：[`worktree-audit-20260718.md`](worktree-audit-20260718.md)
