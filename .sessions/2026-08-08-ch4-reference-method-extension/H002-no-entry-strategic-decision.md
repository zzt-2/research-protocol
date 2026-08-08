# Handoff: Ch4 reference-method 无入口 survivor

> **SUPERSEDED CURRENT ACTION**：D003 已取代本文“立即战略耗尽 / 两对象失败”的强度。R001 的 C1 exact K01 collision 与 C2 FSO defect unknown 事实仍有效；当前动作以 T002 为准。

> 来源: S001（本轮执行 T001，并以 R001/D002 收口；未新建 S###）| 交接目标: 用户作战略范围决定
> 日期: 2026-08-08

---

## 到哪了（状态）

R001 比较两个机制不同 reference object。Paillier FG-DRC exact collision 于旧 K01 `REJECT`；LBS-RDE 缺星地 FSO observed/reproducible defect。D002 terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`，没有推荐对象，也没有形成方法。

## 下一步干什么

由用户决定是否改变 reference-object 来源，或在提供新证据并显式变更 scope/decision 后重开某个旧 rejected object。没有战略决定前停止，不进入 Groundwork。

## 纪律（续接者必须注意的）

- 不把 K01/FG-DRC 从旧 `REJECT` 改标为可进入 GW 的新入口；重开必须有新证据与显式决定。
- 不把 LBS-RDE 的 fiber PMD/SOP defect 当成星地 FSO 事实。
- 不补第三候选，不继续包装 supporting/rejected leftovers。
- 不检索、不实现、不仿真、不进入 Groundwork；不触碰四个 `p05_run*.log`。

## 失败数据附录

### Paillier FG-DRC / K01

- 核心失败机制：承重 post-fade NCO/state damage 未成立；现有 runner 不是 time-correlated fade-exit testbed。
- 具体证据：旧 K01 的方法名、三态动作、主图、消融和 comparator 与本轮 C1 exact 相同；旧 D027 已接受 `REJECT — PROBLEM_EVIDENCE_INSUFFICIENT`。见 `projects/thesis-fso/direction-lab/harvest/baseline-first-method-batch-001.md:117-148`、`.sessions/2026-07-20-research-direction-lab-system/decisions.md:917-951`。
- 已排除方向：无新证据时把 K01 改名或降门晋级。
- 可复用部分：Paillier reference identity 与本地 DPLL scaffold 仍可作为未来经授权的新问题背景，不能作为当前 method delta。

### LBS-RDE pilot-density switching

- 核心失败机制：论文 defect 属 fiber PMD/SOP；本地星地 FSO 没有直接 LBS-RDE/PS-QAM runner 或 defect receipt。
- 具体证据：`papers/manual/ieee-9492010-likelihood-rde/content.md:269-285`、`projects/simulation/explore/pilot-jones-step4a/synthesis.md:34-67`。
- 已排除方向：把论文原 likelihood gate 冒充新增 Ch4 action，或把 fiber defect 直接迁移为 FSO 事实。
- 可复用部分：reference baseline、fixed `N=32/128` comparator 设计与预算估计。

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：D002 terminal 为 `NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED` → [PASS/FAIL + `decisions.md` 证据]
  - 声称2：C1 exact collision 于旧 K01 `REJECT` → [PASS/FAIL + 旧 D027/K01 证据]
  - 声称3：当前不授权 Groundwork → [PASS/FAIL + `topic-index.md` 证据]
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”
