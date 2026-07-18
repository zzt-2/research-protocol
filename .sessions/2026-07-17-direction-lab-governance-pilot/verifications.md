# Verification Records — Direction Lab 可遵守性与控制器试运行

## V001: 首版最小控制器 RED/GREEN 与独立复核

> date: 2026-07-17
> 关联：S001

### 验证项

- [x] RED：控制器模块不存在时测试收集失败，补齐包入口后仍因 `controller` 缺失失败。
- [x] GREEN：`python -m pytest projects/simulation/tests/test_direction_lab_controller.py -q` → `9 passed`。
- [x] 行为覆盖：缺 manifest/run_id、未知或 fingerprint 不匹配、BOARD_READY 前 GO/KILL、PARTIAL 晋级、组件变化 STALE、合法 RUN。
- [x] 审计覆盖：合法 RUN 与缺 manifest 拒绝均写入可解析 JSONL；控制器实现统一 `_record` 路径。
- [x] 独立 verifier：复核测试是否触发行为拦截并指出漏测；补测后最终结论 PASS。

### 证据

```text
RED 1: ModuleNotFoundError: No module named 'verify.direction_lab_pilot'
RED 2: ModuleNotFoundError: No module named 'verify.direction_lab_pilot.controller'
GREEN: .........                                                        [100%]
9 passed in 0.30s
manifest PASS
```

独立 verifier 首轮结论为 PARTIAL，具体指出 run_id 缺失、组件 fingerprint 在 RUN 下拒绝及 JSONL 覆盖风险；补测后最终结论为 PASS，确认未见关键行为漏测。

### 结论

PASS

### 后续（FAIL/PARTIAL 时）

无。首轮只覆盖五个硬门，未扩张到其余 schema 或正式研究流程。

## V002: 首轮控制器边界复核

> date: 2026-07-17
> 关联：V001 / S001

### 复核范围

- 独立运行 V001 测试：`9 passed`。
- 查看 HEAD 提交边界：仅包含 pilot 专题文档、manifest、controller 和测试共 7 个文件；未修改 canonical baseline。
- 对未被测试覆盖的动作和字段做黑盒探针。

### 发现

1. `PROMOTE` 缺少 `evidence_status` 时仍可放行；当前实现只拒绝值恰好为 `PARTIAL`，没有拒绝缺失、`NONE` 或未知证据等级。
2. 未知动作名仍可放行；控制器没有动作枚举硬门。
3. `REUSE_RESULT` 的 stale 特殊处理只覆盖 component fingerprint 变化；baseline fingerprint 变化会直接抛错，尚未统一成失效传播记录。
4. 当前测试证明“直接调用控制器时五个门有效”，尚未证明真实运行入口无法绕过控制器，也未覆盖上下文恢复和重复轮次。

### 结论

`PARTIAL`：V001 的单元级硬门 PASS 保留；整体治理 pilot 不得标记为完全 PASS。以上问题进入下一轮，不立即扩展更多 schema。

### 下一步

- 先补动作枚举和证据等级缺失/非法值的 RED 测试；
- 统一 baseline/component 变化的 STALE 处理或明确两者差异；
- 增加一个真实入口 smoke test，证明绕过 controller 的运行会被拦截；
- 再做一次中断恢复和重复违规测试。

## V003: 最小硬门修复与独立复核

> date: 2026-07-17
> 关联：V002 / S001

### 修复内容

- 动作名改为白名单；
- 晋级证据改为显式白名单，缺失或未知值拒绝；
- `sandbox_only` 或缺失 `promotion_allowed=true` 时禁止晋级；
- baseline/component 非 canonical 的正式动作拒绝；历史复用统一返回 `STALE`；
- `execute()` 检查 `blocked/STALE` 后才调用 operation；
- 增加真实 B5 manifest smoke test、双 fingerprint 漂移、非 canonical 复用和审计恢复/重复违规测试。

### 证据

```text
pytest projects/simulation/tests/test_direction_lab_controller.py -q
22 passed in 0.33s
compileall: PASS
git diff --check: PASS（仅 CRLF 提示，无 whitespace error）
```

独立 verifier 复核结论：`PASS`。未发现本轮最小硬门可绕过。

### 结论

PASS（仅针对本轮最小治理边界）。

### 已知债务

manifest 仍由调用方提供，尚无签名或不可变来源绑定。若调用方同时伪造 `sandbox_only=false`、`promotion_allowed=true`、FULL 和匹配 fingerprints，理论上仍可走 PROMOTE。该问题留到正式 registry/manifest schema 阶段，不扩大本轮 pilot。

## V004: receipt provenance 与 replay 黑盒复核（修复前）

> date: 2026-07-17
> 关联：S002 / D001

### 验证项

- [x] 独立 verifier fresh 运行原有 31 项定向测试：全部通过。
- [x] 黑盒替换合法 envelope 的 `result`：gate 错误 ACCEPTED 并写入 ledger。
- [x] 黑盒仅用 `check()` receipt 拼接 envelope：gate 错误 ACCEPTED。
- [x] 黑盒重复提交同一 receipt：可重复写入同一 destination。

### 证据

```text
31 passed
合法 receipt + 替换 result -> accepted=True / TRUSTED
check-only receipt + 自行拼 envelope -> accepted=True
same receipt replay -> accepted=True twice
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

先补三条 RED 回归，再增加 execution audit event、result hash 与 destination replay gate；原始失败运行目录保留在 `runs/stage2-2026-07-17/`。

## V005: execution provenance/replay 修复后独立复核

> date: 2026-07-17
> 关联：S002 / D002

### 验证项

- [x] `python -m pytest projects/simulation/tests/test_direction_lab_controller.py projects/simulation/tests/test_direction_lab_evidence_gate.py -q` → `34 passed`。
- [x] `python -m compileall -q projects/simulation/verify/direction_lab_pilot` → exit 0。
- [x] 黑盒：result 替换 → `UNTRUSTED`；check-only 拼包 → `UNTRUSTED`；同 receipt 重放 → 首次 `ACCEPTED`、第二次 `REPLAY`；正常 execute → `ACCEPTED/TRUSTED`；stale 后旧 envelope → `STALE`。
- [x] final 运行目录 ledger 仅 1 条 accepted；Round 1/2/3 分别 PASS；Round 4 语义评分 8/8（阈值 7/8）。
- [x] receipt 绑定 `decision_id`、`run_id`、`action`、`manifest_hash`、`allowed`、`blocked`，并有 result hash/execution event。
- [x] B5 manifest 的 `performance_numbers_are_formal_material=false`，未发现写入论文/正式材料。

### 证据

```text
34 passed in 1.10s
compileall exit 0
Round 1 ledger accepted=1
Round 2/3 destination counts unchanged
Round 4 score=8/8, threshold=7/8
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

核心 gate 行为 PASS；Round 4 raw answer-key hash 记录沿用了旧目录值（旧 `76EA...`，final `F950...`，canonical JSON `20ec...`），文本语义未变但 canonical bytes 未冻结。manifest 来源/JSONL 不可变 registry/签名和 destination path 边界继续作为债务，不在 pilot 扩展。

## V006: 5-cycle 真实 shadow 可遵守性观察

> date: 2026-07-17
> 关联：H003 / S003

### 验证项

- [x] 观察窗口：`observation-summary.json` 标记 `5 cycles`；`cycle-records.jsonl` 含 cycle 1–5 五个主循环。
- [x] P0 违规进入证据链：`evidence_ledger` 2 条、`promotion_board` 1 条 accepted，均 TRUSTED；PROMOTE、STALE、ORPHAN 均未写入目标证据链 → 0。
- [x] 未经提醒的 controller 路由：5/5 主循环 `reminder_count=0`（100%，阈值 ≥90%）；每轮均有 controller audit receipt。
- [ ] 上下文恢复：未覆盖至少 3 次恢复；`recovery-check.json` 仅证明新 controller 实例可重载 audit，不计作跨上下文恢复。
- [x] STALE/ORPHAN：各 1 次，分别标为 `STALE`、`ORPHAN + UNTRUSTED`，均 rejected。
- [x] 正式材料边界：`formal_materials_written=false`、`performance_numbers_written=false`；结果摘要未写性能数字。
- [x] 新型绕过/P0 暂停条件：未发现；无目录越界或 P0 完整性漏洞。

### 证据

- `projects/simulation/verify/direction_lab_pilot/runs/stage3-2026-07-17-shadow/observation-summary.json`
- 同目录 `cycle-records.jsonl`、`controller-audit.jsonl`、`evidence-gate-audit.jsonl`、`evidence_ledger.jsonl`、`promotion_board.jsonl`、`recovery-check.json`
- `projects/simulation/verify/direction_lab_pilot/controller.py` 的 ALLOWED_ACTIONS、PROMOTE sandbox gate、STALE/ORPHAN gate
- 独立 verifier fresh 审核：5 个主循环、P0=0、主动路由 100%，恢复样本不足；结论与本记录一致。

### 结论

PARTIAL：核心 5-cycle 行为、P0 隔离、主动路由和正式材料边界 PASS；恢复能力未覆盖，不能宣称整体 PASS。

### 后续（PARTIAL 时）

不改 controller/schema；若继续观察，补足至少 3 次跨上下文恢复（成功率 ≥90%）后再评估正式 registry/schema。当前无暂停条件。

## V007: B001 真实地基 paired batch sandbox integrity

> date: 2026-07-17
> 关联：S004 / D004

### 验证项

- [x] pre-run CandidateMap 与 BatchQueue gate 均为 `PASS`；canonical sandbox 状态为 `BOARD_READY`，formal research state 仍为 `BLOCKED`。
- [x] 运行经过 controller `RUN` 与 `EXECUTE` receipt；EvidenceGate 为 `accepted=true`、`ACCEPTED/TRUSTED`，无 replay/stale admission。
- [x] manifest、result、receipt、execution event 的 manifest/result hash 一致；17/17 source closure 文件存在且 SHA 一致；component fingerprint 与 registry 一致。
- [x] 30 paired cells、30 baseline calls、46,860 行 block 结果；train seeds 11–20 与 test seeds 41–45 不重叠；共享 standard-CMA/Godard-with-z baseline 未被修改。
- [x] 特征只使用 12 个 causal CMA trace transforms；fixed-label BER 与 permutation-invariant BER 均存在；历史单阈值仅作 `candidate=false` negative control。
- [x] 阈值只由 control-rate train scores 标定；无 test-row 训练或阈值选择；AE 的 train-label clean-row 过滤被 verifier 明确标为预注册 oracle-label supervision，而非 test leakage。
- [x] 最小信息满足：4 个 persistent test event cells、6,279 个 positive train blocks。
- [x] 局部规则结果：`C24-SL-LINEAR=ADVANCE_SPECIFIC`，`C24-SL-MLP=ADVANCE_SPECIFIC`，`C24-SSL-AE=RETIRE_SPECIFIC`。
- [x] 未发生 family-wide kill、canonical baseline 变更或 paper/material 自动写入。

### 证据

- `projects/thesis-fso/direction-lab/batches/B001-20260717-live/manifest.json`
- 同目录 `controller-audit.jsonl`、`evidence-gate-audit.jsonl`、`verifier-report.md`、`batch-synthesis.md`
- 同目录 `result.json` 与 `evidence_ledger.jsonl`（大体量原始证据，保留在隔离目录）
- `projects/thesis-fso/direction-lab/candidate-map.yaml`、`batch-queue.yaml`、`component-registry.yaml`

### 结论

PASS：B001 作为 sandbox evidence 的完整性、来源、指标边界与独立复核均通过。该 PASS 不等同正式 Go/Kill、Step 4a 结论、方法族结论或论文材料资格。

### 已知债务

| 债务 | 当前状态 | 触发解决条件 |
|------|----------|-------------|
| unified runner 仍来自未提交 worktree 快照 | sandbox-only | 新一轮复验前形成可复现、经审查的 canonical runner 变更 |
| 两个监督式检测器尚未测试 causal safe fallback | 仅有 detector signal | 新 gate 批次完成 fallback/BER/PI-BER 联合评估 |
| master-state 与最新 D/V 存在 formal Step 3.5/4a 漂移 | formal state BLOCKED | 独立解决状态冲突并补足所需文献/基线证据 |

### 后续

对两个监督式候选做新的独立门控 paired revalidation，或选择不同机制的下一候选；不得直接复用 B001 数字扩大有效域。

## V008: B001 完成性深审查

> date: 2026-07-17
> 关联：S004 / D005

### 验证项

- [x] runtime evidence：独立复算 30 cells、30 baseline calls、46,860 rows、17/17 source closure、controller/EvidenceGate hashes → PASS。
- [x] standard-CMA 与双口径：runner 调用 `run_cma_diagnostic(mode="standard")`，每行 fixed-label/PI-BER 均存在且 finite → PASS。
- [ ] CandidateMap 算术：按声明 weights 重算 shortlist scores 与文件值不一致，排序也受影响 → FAIL。
- [ ] `C24-SSL-AE` 合同：实现以 train labels 筛 `y==0` clean rows，与“不需要 event labels”的预注册假设不一致 → FAIL（无 test leakage，但有 protocol deviation）。
- [x] 生命周期：后补 `execution-status.yaml` 可区分冻结 queue contract 与运行后状态 → PASS；`implementation-plan.md` 和 infra failure 状态仍待同步。
- [x] 两次独立审查出现结论差异：快速小文件审查判 PASS，深审查逐项复算后判 PARTIAL；以能复现算术/代码路径缺陷的深审查为准。

### 证据

```text
U24: recorded=4.15, recomputed=4.20
U05: recorded=3.55, recomputed=3.65
U20: recorded=3.55, recomputed=3.65
U18: recorded=3.00, recomputed=3.25
U08: recorded=3.10, recomputed=3.05
run_b001.py passes fixed-label y_fit into detector
ml_detector_batch.py selects clean = (y == 0)
14 passed in 3.59s (independent verifier)
```

### 结论

PARTIAL：B001 runtime sandbox evidence integrity PASS；CandidateMap/Queue governance closure PARTIAL；旧 AE protocol conformance FAIL。不得宣称“完整流程跑完一整批”，直至 v2 门控与替代批次独立复核完成。

### 后续（FAIL/PARTIAL 时）

新建不可变 CandidateMap/Queue v2；增加确定性评分测试；实现真正不使用 event labels 的 clean-control AE；pre-run gate PASS 后运行替代批次并写新的 verifier/synthesis。

## V009: v2 Candidate Universe/Map 与 replacement runner pre-Queue 复审

> date: 2026-07-18
> 关联：S004 / D005

### 验证项

- [x] Candidate Universe v2 继承 v1 并扩为 34 个 archetype；F1、G2、U32 改为带 scene gate/evidence gap 的 `RETAINED_NEUTRAL`，未提前 Go/Kill。
- [x] CandidateMap v2 精确绑定 Universe v2 与 v1 SHA；34/34 唯一覆盖；权重和、1–5 因子范围、score 算术、v1 tie-break 与排序均由确定性 gate 校验。
- [x] 对抗变异 `U01→UX`、交换同分 `U05/U20`、v1 SHA 漂移均被 gate 拒绝。
- [x] 无标签 reconstruction detector 的 `fit(x, cell_ids)` 与 threshold API 不接收 label；并列 cell maxima 时采用保守阈值，实际 control false-alarm 不超过预算。
- [x] replacement runner 默认使用冻结 shared generator 与 standard-CMA；SNR 显式传 `gamma_bar`，验证真实 QPSK 输出，拒绝 train/test seed overlap、任意 contract override 与默认执行对象注入。
- [x] 静态 registry 分别约束 baseline、detector、runner、metric fingerprints；source closure 覆盖 31 个实际运行源码，默认 import trace 缺失为 0；contract snapshot 明列 Universe/Map/Queue/registry/anchor/canonical-state。
- [x] 真实最小 production path 不使用 test doubles，经 controller 与 EvidenceGate 通过；test doubles 必须显式标 `TEST_DOUBLE/test_only=true`。
- [x] 旧 v1 Universe/Map/Queue 与 `run_b001.py` 相对 HEAD 无差异。

### 证据

```text
python -m pytest projects/thesis-fso/direction-lab/tests -q
50 passed in 5.58s (independent verifier)
CandidateMap v2 CLI: PASS
default production path: PASS / PRODUCTION / test_only=false
actual import trace vs closure: 31 files / missing=[]
```

- `projects/thesis-fso/direction-lab/candidate-universe.v2.yaml`
- `projects/thesis-fso/direction-lab/candidate-map.v2.yaml`
- `projects/thesis-fso/direction-lab/component-registry.v2.yaml`
- `projects/thesis-fso/direction-lab/tools/run_v2.py`
- `projects/thesis-fso/direction-lab/tools/unlabeled_control_reconstruction.py`
- `projects/thesis-fso/direction-lab/tools/validate_candidate_map.py`

### 结论

PASS：只覆盖 v2 Candidate Universe/Map 与 replacement runner 的 pre-Queue 技术门控。该 PASS 不代表 Queue v2、B002、正式 Groundwork 或论文晋级已通过。

### 历史声明校正

V007/V008 的“17/17 source closure”只证明手工列出的 17 个文件 hash 一致，不是真实 import closure；该表述由本条的 31-file closure + actual import trace 核验取代。B001 数值不因此自动失效，但其整体流程状态继续是 `COMPLETED_SANDBOX_WITH_PROTOCOL_DEVIATION`。

### 后续

生成并独立门控 Queue v2；只有 Queue gate PASS 后才允许 B002 使用默认 production runner 执行。synthesis 必须排除 `test_only=true` receipt。

## V010: BatchQueue v2 独立 pre-run gate

> date: 2026-07-18
> 关联：S004 / D005 / V009

### 验证项

- [x] Queue v2 精确绑定 v1 Queue、Universe v2、Map v2、runner 与 registry SHA；Map status/independent review/verdict 均为 PASS。
- [x] B002 绑定 U24/F05/BATCH_1_FAMILY，包含 supervised linear、supervised nonlinear、unlabeled reconstruction 三种不同机制。
- [x] 共享 30 个 standard-CMA cells、train/test seed 隔离、fixed/PI 双指标、主指标、预算、valid domain、minimum-information 与机制级 Go/Kill 条件均冻结。
- [x] `no_family_wide_kill=true`、`sandbox_only=true`、`promotion_allowed=false`；controller 固定 `RUN/BATCH_READY/EXPLORATORY/evidence_ledger`。
- [x] 13 类对抗变异全部被拒绝：family-wide kill、promotion/sandbox、Map family/archetype 偷换、缺必要合同字段、空规则、junk metrics、完成态、current-CMA/no-z、seed overlap、candidate override、旧 AE ID、错误 controller 状态。
- [x] 未运行 B002；批次目录仅有历史 B001。

### 证据

```text
python -m pytest projects/thesis-fso/direction-lab/tests -q
90 passed in 12.92s (independent verifier)
python projects/thesis-fso/direction-lab/tools/validate_batch_queue.py projects/thesis-fso/direction-lab/batch-queue.v2.yaml
PASS
13 adversarial mutations: all REJECT
```

- `projects/thesis-fso/direction-lab/batch-queue.v2.yaml`
- `projects/thesis-fso/direction-lab/tools/validate_batch_queue.py`
- `projects/thesis-fso/direction-lab/tests/test_batch_queue_gate.py`

### 结论

PASS：只授权将 Queue v2 写为 PASS 并进入 B002 启动前检查；不代表 B002 已运行、结果有效或可晋级论文。

### 后续

使用默认 production runner（禁止 test doubles）执行 B002；所有产物进入新的隔离目录，经 controller receipt 与 EvidenceGate 后再交独立 verifier。任何异常按具体机制登记，不扩大为家族 Kill。

## V011: B002 independent post-run verification

> date: 2026-07-18
> 关联：S004 / D005 / V010

### 验证项

- [x] B002 默认 production runner 完成；未注入 test doubles、未使用 contract override；manifest 为 `PRODUCTION`, `test_only=false`, `sandbox_only=true`, `promotion_allowed=false`, `EXPLORATORY`。
- [x] controller RUN/EXECUTION receipt、EvidenceGate 与 ledger 均 `ACCEPTED/TRUSTED`；normalized manifest/result hashes 一致。
- [x] 30 cells（20 train + 10 test）、30 baseline calls、46,860 rows；train seeds 11–20 与 test seeds 41–45 不交叉；每 cell 一次 baseline call。
- [x] source snapshot/import closure 31/31、code closure 25；全部文件存在且 SHA 匹配；registry.v2 与 baseline/detector/runner/metric fingerprints 匹配。
- [x] fixed-label BER、permutation-invariant BER、PI assignment 与 12 causal features 全部 finite；mininfo 为 4 event cells、6,279 positive train blocks。
- [x] C24-SL-LINEAR 与 C24-SL-MLP 满足 exact-contract `ADVANCE_SPECIFIC`；C24-SSL-AE-UNLABELED 因 recall=0 满足 exact-contract `RETIRE_SPECIFIC`。
- [x] AE fit/threshold 路径不接收或读取 event labels；labels 只用于监督模型和统一 post-hoc evaluation。AE 结论不扩大到 SSL/UL/generative 家族。

### 证据

```text
run_id: B002-15309cc700804776a45740786101a6ae
decision_id: decision-30e66bbf8b5f4373813d5c7007c5bb19
manifest_hash: 3004a354ddaa107e609d0bb736d99c5fc06a03e38487484ffc0311ad00e35c76
result_hash: a492e00e986ec352e4b01f10c7b32f3cc43c0a9603bf5bc2f75f27ad6924f019
evidence_gate: ACCEPTED/TRUSTED
```

- `projects/thesis-fso/direction-lab/batches/B002-20260718-live/verifier-report.md`
- `projects/thesis-fso/direction-lab/batches/B002-20260718-live/batch-synthesis.md`

### 结论

PASS：B002 artifact/contract/evidence integrity 与预注册机制级判定通过；不等于正式 Groundwork Go、跨域泛化、方法族结论或论文材料资格。

### 已知债务

| 债务 | 当前状态 | 后续触发 |
|---|---|---|
| source snapshot 含本机绝对 Windows 路径 | 当前机器 SHA 闭合 | 跨机器复现/长期 runner 封装时改为相对路径并记录 workspace identity |
| B002 原始 result/evidence 约 240MB/77MB 级 | 隔离目录保留，未进入代码提交 | 归档或外部对象存储时保留 hash/receipt |
| AE control-rate train 域含少量真实 event blocks | 设计上不读取 labels，属于完整参考域 | 后续若比较 clean-manifold 机制，另立无标签/污染鲁棒性假设 |

### 后续

只继续其他机制或下一候选批次；不因两条 supervised advance 自动晋级论文，不因 AE exact retire 否决整个 ML 家族。

## V012: B003 v3 governance gate independent verification

> date: 2026-07-18
> 关联：S004 / D006 / V011

### 验证项

- [x] v3 queue 显式绑定 `B003`，拒绝隐式 batch 选择与 `contract_override`；六个运行字段均存在并通过 `runtime_field_effects` 真值检查。
- [x] `channel_block`、`t_s`、`method` 由 v3 channel adapter 实际传入并消费；`r2` 进入 standard-CMA config；`fade_threshold_h` 与 `clip_norm` 在 canonical prompt013 中不被消费，已明确标记为 `audit_only/non-operative`，不作性能归因。
- [x] Queue、Registry、Runner、Validator、Controller 及 run_v2/run_b001 helper 指纹逐字节一致；baseline 唯一为 canonical，候选组件保持 sandbox-candidate。
- [x] 治理 smoke 通过：strict EvidenceGate 要求 artifact pointer，ledger 只保存 receipt/result_hash/artifact_pointer，完整结果独立存放；非接受 gate 会在写结果前硬失败；source closure 覆盖实际加载的 v3/v2/B001/validator/controller 模块。
- [x] B002 manifest/result/status/ledger、v2 queue/registry、canonical baseline 未被修改、删除、覆盖或重跑。
- [x] CandidateMap 限制已保留：v2 Map 只证明 34 archetype 到 8 families 的分区与排序，不证明 ML 方法空间穷尽；该限制不阻断本次仅绑定 U24 exact-contract 的 v3 sandbox 治理门控。

### 证据

```text
queue_sha256: 830acb8888583f0128687a54b7349c90c6cde6b9a8796008c47bfcf4c9de19c5
post_gate_queue_sha256: 62cabb989e269af28697c5e4092cc9d984c92d15d7565d1bf0c461c3f0df5917
registry_sha256: 82fdb419de785568a3afe13666200aa17cde0abf56d9ae55848c70508bcddce9
runner_sha256: 6f21dfe023ccb8e74876730bee8789353ef649ad2b976be63317420f298a9caf
validator_sha256: 5a6ac4ee89c05f660e9ab7f5b5ef18e7e2d6ed8b5231c1ddc2125e84578d9002
controller_sha256: 95a153fe893f5df1c83ab2436de1829c2bd36a1e76e730a2c53d4401a58cf2a8
tests: test_v3_governance.py 13 passed; controller/evidence tests included
queue_validator: PASS
```

### 结论

PASS：B003 v3 技术治理门控通过，允许进入新的隔离目录执行小型 sandbox paired batch；不等于 Candidate Universe 完整性证明、formal Groundwork Go、跨域泛化结论或论文材料资格。

### 已知债务

| 债务 | 当前状态 | 后续触发 |
|---|---|---|
| CandidateMap 方法空间完整性 | 仅 archetype 分区覆盖 | 新增候选族前需做独立 Universe/Map 复核 |
| fade_threshold_h/clip_norm 非 operative | canonical baseline 不消费 | 若未来需要其影响性能，必须另建非 canonical 合同并重新门控 |
| source snapshot 的本机路径 | 当前机器闭合 | 跨机器复现时改相对路径并记录 workspace identity |

### 后续

将 Queue 状态更新为 `PASS` 后，才允许在 `B003-20260718-live` 新目录用标准 CMA 跑三机制小批次；运行结果须经独立 post-run verifier 和统一 synthesis，任何数字不得自动进入论文或正式材料。

## V013: B003 independent post-run verification and synthesis gate

> date: 2026-07-18
> 关联：S004 / D006 / V012

### 验证项

- [x] B003 通过显式 `batch_id=B003` 的 v3 runner 完成；未使用 `contract_override`，未改写或重跑 B002；`test_only=false`、`sandbox_only=true`、`promotion_allowed=false`。
- [x] 30 paired cells（20 train + 10 test）、30 次 standard-CMA baseline call；train/test seed 不交叉；baseline 身份为 canonical standard-CMA Godard-Z。
- [x] manifest/result/artifact/status/ledger/gate 链一致：manifest hash `42d806...b6b5e6`，result hash `c17ab9...c8e3cc`，artifact SHA `a395ec...43df6e0`、107,859,566 bytes，EvidenceGate `ACCEPTED/TRUSTED`。
- [x] source import closure 33/33，实际加载模块均存在且 SHA 匹配；ledger 与 gate audit 仅保存 receipt/hash/pointer，完整结果只在独立 artifact。
- [x] 46,860 行 fixed-label BER、PI-BER、assignment 与 12 causal features finite；具体候选结果已由独立 verifier 复核并写入 B003 verifier report/synthesis。

### 结果（仅 exact contract）

- `C24-SL-LINEAR`: `ADVANCE_SPECIFIC`（AUROC 0.9622865，AUPRC 0.8469339，event recall 1.0，control FA 0.20）。
- `C24-SL-MLP`: `ADVANCE_SPECIFIC`（AUROC 0.9577760，AUPRC 0.8440742，event recall 1.0，control FA 0.00）。
- `C24-SSL-AE-UNLABELED`: `RETIRE_SPECIFIC`（AUROC 0.8213859，AUPRC 0.3363064，event recall 0，control FA 0.40）。

### 结论

PASS：B003 artifact/contract/evidence integrity 与统一 exploratory synthesis 完成。两条 supervised 结论仅保留为 exact-domain 机制观察；AE 只否决该具体机制/合同，不扩大到 SSL/UL/generative 家族。没有任何数字自动进入论文或正式材料。

### 已知债务

| 债务 | 当前状态 | 触发解决条件 |
|---|---|---|
| canonical-state last_completed_batch | 仍指 B002；避免事后改源快照污染 B003 provenance | 新建状态快照/下一批前完成状态对账，不回写 B003 来源 |
| CandidateMap 完整性 | 只证明 archetype 分区 | 新候选族进入运行前重新做 Universe/Map 复核 |
| exact-domain only | 无跨 SNR、f_g、调制、长度泛化 | 新合同与 paired revalidation |

### 后续

继续下一候选或新机制的独立 Queue/Registry 快照；不得把 B003 数字复用为正式 baseline 或论文证据。

## V014: B003 completion-event reconciliation and mechanism coverage audit

> date: 2026-07-18
> 关联：S009 / D008 / V013

### 状态链验证

- [x] B003 的旧 canonical bytes 以 `state/projections/821415346437f47de064966fdaa768242c63d2d660ea189e88a4a0dfb51995b0.yaml` 保存，SHA 与 B003 source snapshot 预期值一致。
- [x] `state/completion-events.jsonl` 追加一条 `batch_completion_verified`，sequence=1、prev hash=null、event hash=`39d85d029a90cf6719d4b03cffc4cce811006d8faec4663c3d2ef3889e8de976`；事件绑定 B003 manifest/result/artifact/status/ledger/verifier/synthesis hashes。
- [x] `tools/reduce_state.py` 纯 reducer 生成 projection SHA=`5967ea38e676b46cb092c98060bec5b470b5a03625f21e65218cf3b2ae3a88af`，top-level canonical-state 与 projection 字节一致；B003 `last_completed_batch` 与 completion history 均可查询。
- [x] reducer tests 5 passed；fresh combined governance/controller/evidence/state tests 53 passed；py_compile PASS。
- [x] baseline、metric、simulator、formal research state 和 B002/B003 历史目录未被 reducer 事件修改。

### Candidate Universe 覆盖审计

- [x] v2 的 28 application points、34 archetypes、8 families、13 method tags 已核对；结论为 `PARTIAL_MECHANISM_COVERAGE`，不是完整性 PASS。
- [x] 发现 AP×method 差集、U10/U15 反向 tag 不一致、缺少 input source/causal time/oracle boundary/output action/runtime IO/fingerprint 等接口字段。
- [x] 新增 U35–U44 机制级 retained-neutral interface 候选；记录 U05/U11、U12/U26、U17/U30、U19/U20、U23/U24、U25/U31 等合并判据。
- [x] D031–D039 历史负证据缺口已列为 lineage correction；未把局部 Kill 扩大为方法族禁令。

### BatchPlan

- [x] 生成 `batch-plan.v1.yaml`，包含 P01 U25 action-contract Scout、P02 U10 event-library Scout、P03 U19 residual-headroom Scout、P04 U20 coded-LLR Scout、P05 U25 safe-fallback Sandbox。
- [x] 每批均列真实问题证据、已有/缺失实现、baseline、输入合同、指标、预算、kill/block 条件与依赖；当前全部 `NOT_RUNNABLE` 或 `BLOCKED_PENDING`。
- [x] B004 仿真禁止；未创建新 Queue/Registry/Runner，也未启动任何后续性能批。

### 结论

PASS：B003 状态对账和 provenance 循环修正通过；PARTIAL：Candidate Universe 机制级覆盖仍不完整；PLAN_ONLY：后续 5 个批次已排序但没有任何批次获得 Sandbox-ready 或 Promotion 资格。

## V015: P01 U25 action-contract Scout gate

> date: 2026-07-18
> 关联：S006 / D009
> status: superseded by V016 after strict trace whitelist/provenance extension

### 验证项

- [x] `test_u25_action_contract.py` 6 项通过：未来信息拒绝、固定安全策略确定性、NO_OP 恒等性、连续 replay、动作集合/fingerprint 和未知动作拒绝。
- [x] 与状态 reducer、v3 governance、controller、evidence gate 的相关回归合计 `59 passed`。
- [x] `u25-action-contract.v1.yaml` 的实现 fingerprint 与模块计算值一致：`4359429931d5d2da849045e658968cac677f78cb2dabe2d8d429d1034363b3f7`。
- [x] contract 明确列出 `channel_block`、`r2`、`fade_threshold_h`、`clip_norm`、`t_s`、`method`，`values: null`，不提供隐藏默认值。
- [x] `u25_action_contract.py` 与 `reduce_state.py` 编译通过。

### 未通过/未覆盖

- [ ] 真实 causal event generator：未实现。
- [ ] 共享 fork-replay dataset：未实现。
- [ ] Queue/Registry/Runner binding 与 source closure：未创建/未验证。
- [ ] 任何性能、恢复、false intervention 或 safety 数字：未运行。

### 结论

PARTIAL：P01 的 Scout contract gate PASS；Sandbox gate 仍 BLOCKED，U25 不得标记为可运行，B004 继续禁止启动。

## V016: P01 complete Sandbox-ready decision and P02 fallback audit

> date: 2026-07-18
> 关联：S007 / D010

### Causal adapter

- [x] adapter 输入绑定 B003 immutable artifact 的真实 `cells[0].trace`，不是手写 synthetic dict；流式读取 `1562` 条 trace 并生成 `1562` 条 event。
- [x] 严格白名单只接受 `output_start/output_end/cm_error/output_power/update_norm`；未知字段以及 `h/true_h/true_jones/theta/bitsX/bitsY/fixed_label_ber/pi_ber/oracle/post_hoc/future_state` 均 hard reject。
- [x] `sequence_id/step/available_at_step/trigger` 与四个 observable 均有 source pointer；step pointer 同时记录 `output_start/output_end` 对齐样本索引和 end-exclusive 语义。
- [x] nested unsupported observables 拒绝测试通过；`lock_score=1/(1+cm_error)` 明确标记为 receiver-only proxy，不称为已验证物理 lock state。

### Fork-replay / action effect

- [ ] receiver state snapshot：缺失。
- [ ] per-decision action hook：缺失；真实 runner 签名仍为 `(realization, cfg, variant='baseline', return_blind_trace=True)`。
- [ ] NO_OP bit-exact、fixed safe policy、single action、3 event-like/3 clean fork：未到达。
- [ ] action latency/recovery delay/worst-cell degradation：不可计算。

### Runner / registry / source closure

- [ ] `run_v3.py` generic candidate dispatch：失败，仍硬编码 U24。
- [ ] U25 component IDs/fingerprints、Queue/Registry snapshot、真实 source closure：未创建。
- [x] governance preflight 在前置条件未闭合时硬阻断，没有写 ledger、completion event 或 canonical state。

### 独立复核与历史保护

- [x] 独立 verifier 复核：contract/adapter PASS，Sandbox BLOCKED。
- [x] 相关回归：`77 passed`。
- [x] preflight 退出码 `2`，阻断项：`STATE_SNAPSHOT_MISSING`、`ACTION_EFFECT_NOT_OBSERVABLE`、`RUNNER_U24_HARDCODED`。
- [x] B002/B003 历史文件 SHA 与冻结值一致；无 B004 目录、无新 Queue/Registry。

### P02/U10 fallback audit

- [x] FOE/DPLL/VV/BPS、phase-noise channel 和邻接 lock tracker 资产已找到。
- [x] 当前双偏振 standard-CMA generator 仍无 carrier phase/CFO/CPR 状态；无 cycle-slip/lock-loss event library、persistence 或 warning-lead validator。
- [x] P02 状态：`P02_SCOUT_CONTRACT_ASSETS_PARTIAL`，不允许直接建立性能批次。

### 结论

**B / P01_BLOCKED**：causal adapter 已闭合，但 fork-replay/action effect 和 runner/registry/source closure 未闭合。U25 只在当前 exact standard-CMA implementation domain 被阻断，不扩大为整个 U25/U42 方法族禁令；下一候选转 P02/U10 轻门控，若其 carrier/CPR/event contract 仍不能闭合，再转 P03/U19。

## V017: P02/U10 与 P03/U19 Capability Triage

> date: 2026-07-18
> 关联：S008 / D011
> status: PASS（分诊结论为两个候选均 NOT_RUNNABLE）

### 核验范围

- [x] DL-Process v0.3 的三层边界已应用：Universal Core、Communications Profile、dual-pol OSL Project Adapter。
- [x] P01/U25 保持 `DEFERRED_ARCHITECTURE`；没有修补 U24 runner、伪造 state/action/replay、创建 Queue/Registry/fingerprint 或启动 B004。
- [x] P02/U10 能力、输入、因果边界、输出、state mutation、runner 缺口和 smoke 阻断已记录；当前双偏振链没有 carrier impairment/CPR/event trace，状态 `NOT_RUNNABLE`。
- [x] P03/U19 能力、输入、因果边界、输出、state mutation、runner 缺口和 smoke 阻断已记录；standard-CMA 真实 runner 有内存 `zX/zY`，但 v3/B003 不持久化，合法 CSI/noise 和 same-information analytic comparator 未闭合，状态 `NOT_RUNNABLE`，资产层 `PARTIAL`。
- [x] `scout/capability-triage.v1.yaml`、P02/P03 Scout contract 均可 YAML 解析；合同没有 Queue、Registry 或 fingerprint 字段。
- [x] P03 被标记为最短闭合路径，但没有被提前标记 READY/SCOUT_CONTRACT_READY；下一候选 U23 仅作为 Universe 回退检查项，未默认可运行。
- [x] 独立只读 verifier 复核 PASS：三层绑定与三个 triage/scout YAML 可解析，P02/P03 源码证据支持 `NOT_RUNNABLE`，无 B004、无本轮新 Queue/Registry/fingerprint，git status 未发现 B002/B003 目录改动。

### 结论

`B_ALL_CANDIDATES_NOT_RUNNABLE`。这是接口/证据闭合阻断，不是对 U10/U19 方法族的 Kill；可复用资产和具体缺口均已写入 triage 文件。B001–B003 与 canonical baseline 保持只读，B004 继续禁止。

## V018: P03/U19 Interface Closure independent verification

> date: 2026-07-18
> 关联：S008 续接 / D012
> status: PASS

### 核验范围

- [x] 35 项 P03 专项测试通过（adapter 20、comparator 5、residual 6、interface smoke 2、readiness 2）；全 Direction Lab 测试另有 4 个既有 v2 Queue runner/registry fingerprint 失败，未修改以免越界。
- [x] 真实链路为 frozen dual-pol generator → `run_b001._default_runner` standard-CMA → z-window adapter；runtime 仅传 `rX/rY` 给接收机入口，TX truth/true h/Jones/future/BER/post-hoc 字段均有边界拒绝。
- [x] `CSI_NONE` 已真实接通；receiver-estimated CSI schema 仅声明未绑定，comparator 对该等级 fail closed。
- [x] residual 定义、conditional moments、显式 tail threshold 和 `NOT_ESTIMABLE_ONE_CELL` stability 状态可复现；fixed-label BER 与 PI-BER 是独立 evaluation-only 字段，本次未计算且不影响 runtime hash。
- [x] comparator 只消费同一 z-window 与显式 QPSK amplitude；确定性、有限值、tie 规则、monotonicity 和非法 comparator identity 拒绝通过。
- [x] source closure 由实际运行时加载模块生成，共 23 个项目文件，逐文件 SHA-256 匹配；4 个 candidate component ID/fingerprint 均真实匹配，状态为 `scout-candidate`。
- [x] smoke 为 512-symbol、单 realization、单 cell 的 interface-only 运行；三个 artifact 报告 hash 与磁盘字节 hash 一致；未写 manifest、evidence ledger、Queue、Registry、canonical state 或论文材料。
- [x] B002/B003/canonical 冻结文件 18 项 hash 全部匹配；B004 不存在；Queue/Registry 无 P03/U19 绑定。

### 结论

`P03_SCOUT_CONTRACT_READY`。这只允许下一轮实现真实 U19 ML mechanism 和新的 contract 设计；不等于 Sandbox PASS、性能结果或论文资格。receiver-estimated CSI、multi-cell stability、正式 fixed/PI-BER evaluator、机制级 shared Sandbox queue 仍为前置条件。

### 纠错附录

独立核验先发现 Windows newline hash 漂移和 residual comparator identity 漏门；修复后重跑 smoke 与回归测试，最终复核 PASS。历史 B002/B003 未修正。

## V019: Direction Lab control-plane closure

> date: 2026-07-18
> 关联：S010 / D013
> status: PASS

### 状态对账

- [x] formal research 仍为 `BLOCKED`；`master-state.md` 只保留 formal blocker、sandbox pointer、current Scout 和唯一下一动作。
- [x] canonical reducer projection 指向 `B003 / COMPLETED_SANDBOX_VERIFIED`；completion event、canonical projection 和 B003 execution status 一致。
- [x] P03 interface-smoke-v2 与 readiness 均为真实 `PASS` / `P03_SCOUT_CONTRACT_READY`；active Scout contract 为 v2。v1 保留为 `SUPERSEDED` lineage，不再作为当前状态。
- [x] capability triage 已修正为 P02/U10 `NOT_RUNNABLE`、P03/U19 `P03_SCOUT_CONTRACT_READY`；旧 P03 `NOT_RUNNABLE` 保留在 lineage。
- [x] `P03` 测试与 state-reducer 相关回归：`40 passed, 137 deselected`；smoke 与历史 guard 均 PASS。
- [x] B002/B003/canonical 受保护文件 hash 与 smoke history guard 全部匹配；B004 不存在。

### Session 与工作树

- [x] governance pilot 的 S 标签为 S001–S010，各唯一；确定性引用扫描无悬空 S 引用。较早 `S005-process-spec-freeze.md` 保留，后创建机制覆盖文件为 `S009`。
- [x] governance pilot 转为 `dormant`；后续 P03 研究状态归项目目录，不再向该专题追加 Scout 微步骤。
- [x] dirty worktree 只读盘点已写入 `projects/thesis-fso/direction-lab/worktree-audit-20260718.md`：1540 文件级条目，未执行清理、restore、reset、stage 或批量提交。

### 结论

`PASS`：控制面收口完成。当前唯一合法研究动作是 P03 residual headroom probe；它不是 B004、不是正式性能批次，也不自动产生论文材料。
