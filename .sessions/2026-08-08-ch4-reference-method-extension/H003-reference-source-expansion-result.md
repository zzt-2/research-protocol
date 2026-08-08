# Handoff: RML-FSTS defect-reproduction 入口已选

> 来源: S001（T002 回传，R002/D004 收口）| 交接目标: 下一对话按正式 Groundwork 从 Step 1 启动 RML-FSTS research object
> 日期: 2026-08-08
> 独立验证: V003 PASS，P0/P1/P2=`0/0/0`

---

## 到哪了（状态）

T002 用满 4/4 组机制定向 query，比较 RML-FSTS 与 BUM-CMA 两个外部 reference baseline。D004 terminal=`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`：唯一入口是 FSTS fixed lag/`BL` condition-dependence research object；BUM-CMA 因 published weak-branch defect 与 faithful smoke 不成立而不入场。当前 object/package failure 计数仍为 `0/0`，没有形成方法、defect 结论或 METHOD_SIGNAL。

## 下一步干什么

完整重读 `stages/groundwork.md`，核对项目 `master-state.md` 的 GW Progress 后，只从该 research object 的 **GW Step 1** 启动。Step 1–3 未完成前不得运行 R002 预注册 smoke；只有合法进入 Step 4a 后，才做 0.5–1 天 fixed-lag defect reproduction。

## 纪律（续接者必须注意的）

- source defect 只到“fixed lag/`BL` 条件依赖与低功率退化”；星地 lag-ranking crossover 仍是 UNKNOWN。
- future action 只占位为 receiver-visible reliability-weighted multi-lag circular fusion；当前不是方法，也不得在 GW 前实现。
- smoke 只复现 defect，不测试 future action；最强廉价替代是 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup，且它仍失败才可 PASS；per-cell best lag 只能作诊断/Kill 上界。
- 不并行启动 BUM-CMA，不补候选，不复活 K01/B10/B3-Q2/C3/P09 等 exact object。
- 不触碰四个 `p05_run*.log`，不修改旧 dormant topic 或 protected history。

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| future fixed-lag defect smoke | 同一 modulation/TS/power bin 内 ≥2 个 held-out turbulence/branch conditions 出现稳定 lag-ranking crossover，且 conditioned single-lag lookup 仍有 `≥20%` MSE 或 `≥10 pp` outage regret并超过 MDE；论文 fixed `BL` 单独失败不能过门 | R002 预注册；须在 GW Step 1–3 后复核冻结 | 未执行 |
| baseline identity | 1 天内忠实复现论文 fixed-`BL` FSTS 输入、时序与估计公式；否则退出 | R002 E4/E8 | 未执行 |

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：D004 terminal 为 `ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1` → [PASS/FAIL + `decisions.md` 证据]
  - 声称2：RML-FSTS source defect 不等于目标 FSO defect 已成立 → [PASS/FAIL + `R002` / paper note 证据]
  - 声称3：当前 object/package failure 计数为 `0/0` 且未授权 smoke → [PASS/FAIL + `R002` / `topic-index.md` 证据]
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”
