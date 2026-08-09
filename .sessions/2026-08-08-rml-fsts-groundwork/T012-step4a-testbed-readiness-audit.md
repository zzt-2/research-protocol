# Task Brief: RML-FSTS Step 4a testbed readiness 与信息边界审计

> 来源: S004 | 产出位置: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`
> 日期: 2026-08-09
> 唯一文档: 执行方先读本 T，再读取本 T 指定的代码/规范

---

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。
**你的任务**：只读审计现有仿真资产能否支持 PM-4/16QAM、320-symbol FSTS、弱/强湍流、paired fixed-lag sweep、normalized CFO-MSE/outage 与 observability，不得把“有脚本”当“科学 testbed ready”。
**产出**：只写 `projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`；不改代码/参数/治理 owner，不跑长实验。

**最高纪律**：
1. 沿 caller→callee 逐层核查参数是否真正注入 realization/estimator；字段名或标签一致不算注入证据。
2. 检查 deployable path 是否读取 truth SNR、true `h`、TX payload/目标标签；truth 只能用于 O1/scoring。
3. 检查 paired realization、state lifecycle、metric signature、raw→aggregate 和 seed ledger 能否闭合。
4. 对 existing asset 给 `READY / NEEDS_BOUNDED_ADAPTER / INVALID`，不能笼统说“可复用”。
5. 不实现、不修复、不下科学 Go/Kill；总耗时不超过 15 分钟。

## 1. 背景

冻结 ladder：B0 paper fixed action；B1 dev-global fixed action；B2 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup；O1 truth/oracle lag 仅作 headroom/Kill；C1 只有 B2 后稳定可观测残差才允许。

重点检查：
- `projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py`
- `projects/simulation/common/` 的 shared realization/channel/metrics API
- `projects/simulation/params.py`
- 相关 tests 与既有 `oversampled-coherent-sync-q1`/其他 Step4a asset 的可复用 pattern（只看基础设施，不继承科学结论）
- `projects/simulation/DESIGN-modular-split.md`
- `projects/simulation/tests/INTEGRATION_PLAN.md`
- `code-quality.md` 与 `reference/sim-template/` 中相关模板

## 2. 任务详情

### 2.1 必答问题

1. 是否已有 faithful Wang fine FOE fixed-lag estimator？若无，现有代码究竟只做什么。
2. 是否已有 PM-4/16QAM symbol/TS/channel generator，可否构造 320-symbol FSTS。
3. 弱/强湍流与 receiver-power/SNR 的真相源、注入路径与物理语义是否清楚。
4. paired realization 是否能保证同一样本/噪声供所有 action；seed lifecycle 如何。
5. normalized CFO-MSE 与 outage 的 population/numerator/denominator/threshold/aggregation 应如何落盘；现有工具能否支持。
6. B1/B2 dev/test freeze 所需 split 与 lookup key 能否合法实现；receiver-power 是可见测量还是 truth label。
7. observability 可用的 receiver-visible features；哪些特征含 truth 泄漏。
8. runtime hidden-truth metamorphic test 从哪个 caller 到哪个 callee。
9. 最小新增文件集合与预计执行成本；严格不建议修改 `common/`/`params.py`。

### 2.2 产出格式（强制）

```markdown
# RML-FSTS testbed readiness audit
## Status
READY / NEEDS_BOUNDED_ADAPTER / INVALID
## Asset map
| capability | file:line | status | gap |
## Caller-to-callee paths
## Parameter injection
## Information access card
## Metric signature
## State/seed lifecycle and pairing
## Raw-to-aggregate contract
## Runtime metamorphic test
## Minimal isolated file set
## Readiness terminal and blockers
```

## 3. 已知陷阱

- `frame_sync_fsts.py` 的模板相关是 frame synchronization，不是 fine CFO estimation。
- 旧 `b5` short-time-spectrum FOE 动作不同，只能供工程 pattern，不能成为 Q1 estimator。
- `params.py` 中 CRITICAL turbulence 参数不能静默复用为本 MVE physical truth。
- `receiver_power` 标签若由 true attenuation/h 直接传给 action，就是 oracle，不是 receiver-visible。

## 4. 验收

- [ ] file:line 级 asset map 与 caller→callee
- [ ] 参数注入、信息访问、metric、state 四卡齐全
- [ ] 给出不改 common/params 的最小 adapter 路径
- [ ] 明确真实 blocker，而非只列待办

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-4a-rml-fsts-testbed-readiness.md`
