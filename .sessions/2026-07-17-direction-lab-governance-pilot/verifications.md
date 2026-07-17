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
