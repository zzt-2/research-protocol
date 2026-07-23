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

- 正式研究：当前 formal Groundwork 工作线 = **Pilot-Jones**，`Step 3.5 PARTIAL/BLOCKED`（D061）。唯一正式入口为 [`../master-state.md`](../master-state.md)。Direction Lab Scout campaign 已 dormant（D022 SCIENCE_FREEZE），无当前科学执行授权。
- Sandbox 历史：B003 已完成并独立验证；批次事实见 [`state/completion-events.jsonl`](state/completion-events.jsonl) 与 [`state/projections/`](state/projections/)。
- Pilot-Jones formal GW（D061）：Step 1/2/3 ✅；**Step 3.5 PARTIAL/BLOCKED**——backward-chain 独立终验 V035 PASS（JLT 2022 Crossref refs=21 / screened=7 / new=0，gw-supplement 判据 #3 闭合），但 D056 要求的 4 篇直接竞品全文获取 BLOCKED（TCOMM `10.1109/TCOMM.2024.3522036` / JLT2025 `10.1109/JLT.2025.3640695` / JLT2022 `10.1109/JLT.2022.3224805` / JLT2023 `10.1109/JLT.2023.3284489`，non-OA IEEE paywalled，`tools/download` all_failed，OA scout 4 源均 closed）。已全文精读 OE 2021 + LCOMM 2026 两篇。**Step 4a 未授权**（FR-22 + D056 全文门）。
- P03 状态（D061 选项①，已选定）：`PAUSED_RETURNED_TO_PORTFOLIO`——P03 暂停回候选池，**不是 Kill**（family 不关闭，沿用 D057/D058 `P03_DOMAIN_ADEQUACY_UNRESOLVED`）。Sandbox `NOT_ENTERED`，ML 仍禁止训练，Stage B 不触发。
- 历史 P03 Stage A 证据（2026-07-19，S077/D059/V033）保留：runnable 代表子域（11 cells × 10 paired seeds）`LOCAL_NEGATIVE`，exit=`NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`；16QAM/receiver-CSI/coded-output 三轴 INFRASTRUCTURE_BLOCKED → DOMAIN/CANDIDATE/FAMILY 仍 UNRESOLVED/OPEN。
- B004：不存在，也不允许启动。

`canonical-state.yaml` 只物化 Direction Lab Sandbox 的机器投影，不代表正式研究授权，也不能单独充当批次历史证据。其 `BOARD_READY` 仅表示全局 board/controller 基础设施可用，不授予当前 P03 创建 Queue、Registry 或执行 Sandbox batch；批次 provenance 以 completion events 和不可变 projection 为准，正式状态与研究入口始终以 `../master-state.md` 为准。

## 已完成批次

- B001：历史 sandbox，存在协议偏差，只保留探索证据。
- B002：sandbox verified。
- B003：sandbox verified；主要价值是治理链验证，与 B002 的 U24 exact contract 研究信息重复。

B001–B003 的任何数字都不能进入论文、正式 Groundwork 或 canonical baseline。

## 当前阻断

当前 formal blocker = Pilot-Jones Step 3.5 的 D056 全文门：4 篇直接竞品（TCOMM `10.1109/TCOMM.2024.3522036` / JLT2025 `10.1109/JLT.2025.3640695` / JLT2022 `10.1109/JLT.2022.3224805` / JLT2023 `10.1109/JLT.2023.3284489`）non-OA IEEE paywalled，`tools/download` all_failed，OA scout 4 源均 closed。只有 OE 2021 + LCOMM 2026 两篇全文精读。backward-chain 门已闭合（V035 PASS），但全文门 BLOCKED → Step 3.5 维持 PARTIAL，**不进 Step 4a**（FR-22 + D056）。

历史 P03 阻断保留：Stage A 在 runnable 代表子域 LOCAL_NEGATIVE，但 3 轴 INFRASTRUCTURE_BLOCKED（16QAM / receiver-estimated CSI / coded output）+ 历史反例落在被阻轴上，不能形成 domain/candidate/family 退出。没有 ML 训练许可、PASS Queue、新 Registry 或 Sandbox 批次许可。

## 下一合法边界

用户裁决 Pilot-Jones 4 篇直接竞品全文获取路径（D061 / H017）：(a) 机构 VPN/proxy 获取 IEEE 全文；(b) 邮件联系通讯作者；(c) 带债豁免（显式豁免 D056 全文门）；(d) 等 OA / 换近似竞品。**本轮不豁免、不进 Step 4a**。不启动 B004，不训练 P03 ML，不创建 Queue/Registry，不复活 dormant science-scout。

历史 P03 Headroom Atlas 入口保留（P03 PAUSED，artifact 不删）：唯一 receipt-bound 入口 [`scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py`](scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py) 已建立并通过 19 tests（含独立对抗审查）；Stage A artifact 在 [`scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/`](scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/)。不得把 LOCAL_NEGATIVE 改写成候选退出，也不得启动 B004、ML 训练或正式性能结论。

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
