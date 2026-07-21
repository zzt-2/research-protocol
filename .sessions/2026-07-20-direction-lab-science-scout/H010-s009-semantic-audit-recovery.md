# Handoff: S009 科学语义审计收口

> 来源: S010 / D016 / V005 | 交接目标: 从可信状态启动方法体系重设计
> 文件名: H010-s009-semantic-audit-recovery.md

## 已完成边界

- C11 的 D012 局部结论保持有效。
- D013 只保留 `TX_TRUTH_ASSISTED_AFFINE_GAP_PRESENT / LOCAL_SLICE / DIAGNOSTIC`：truth-assisted affine bound 与 blind-affine 净负面数字有效，但不构成 learned-corrector target ready。
- C04/C09 原始坏结果有效，机制解释撤回：训练目标存在输入无关的常数最优解，状态为 `IMPLEMENTATION_CONFOUND_CONSTANT_COLLAPSE`，候选科学结论为 `UNRESOLVED`。
- V004 只保留 artifact fidelity、hash、seed、历史保护等验证；科学语义由 V005 判 FAIL。
- 旧 H009 已被本 handoff 修订，不得再作为当前恢复入口。
- 本轮没有重跑实验、改旧 artifact 或修改 Skill。

## 不要做什么

- 不得复述 H009 的“residual 非 affine / z_calib 无信息 / C04/C09 CLOSED / thesis-grade exists-vs-learnable gap”。
- 不得用追加超参数 sweep 修补常数塌缩；先修目标定义和最小语义对照。
- 不得把可复现性 PASS 当作科学解释 PASS。
- 不得在当前科学专题继续堆积流程设计文件；体系设计回到 `2026-07-20-research-direction-lab-system`。
- 不得在 Skill 与记录体系设计、推演和固定前启动大规模科学运行。

## 必读

1. `.sessions/2026-07-20-direction-lab-science-scout/S010-s009-scientific-semantic-audit.md`
2. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` 的 D016
3. `.sessions/2026-07-20-direction-lab-science-scout/verifications.md` 的 V005
4. `.sessions/2026-07-20-research-direction-lab-system/S012-probe-recovery-redesign-intake.md`
5. `.sessions/2026-07-20-research-direction-lab-system/decisions.md` 的 D012

## 接口变更（如有代码改动）

无代码改动。

## 失败数据附录（如涉及路线失败）

- soft-distance 常数解：每个实坐标约 `±0.6075`；一维 loss 约 `0.32710044`；四维合计约 `1.30840175`。
- artifact plateau：约 `1.3084`。
- C04/C09 raw PI-SER：约 `0.928`；相对 blind 约 `+0.624`；worst degradation 约 `+0.78`。
- 上述数字只支持“该实现/目标发生常数塌缩”，不支持方法族或候选机制负面。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| Probe 语义门缺失 | 小成本先排除显然实现伪象 | OPEN | D012 体系设计与 forward simulation |
| 恢复入口分散 | 一页可重建当前态 | OPEN | 新恢复投影设计固定 |
| harvest 历史状态易误读 | 旧结论保留但当前态唯一 | PARTIAL，v7 修订已建立 | current-view/index 固定 |
| 科学专题文件膨胀 | 热路径有界、历史归档 | 10 个 S 文件，已预警 | 目录抗膨胀方案固定 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 恢复正确性 | fresh agent 只读入口后不复述被撤回结论 | D016/D012 | 待推演 |
| Probe 常数塌缩门 | 常数输出不得通过 candidate-ready | S010 根因 | 当前旧批 FAIL |
| 科学语义独立复核 | reviewer 必须检查目标函数与最小反例 | V005 | 当前旧 V004 漏检 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 soft-distance 常数解、runner 单配置和 D013 双聚合口径三条事实
- [ ] 已检查 `_registry.yaml` 中两个专题的 depends_on / conflicts_with
- [ ] 已确认当前范围不含新科学运行和直接 Skill 修改

## 下一轮

进入体系专题，先设计而非立即编码：恢复/记录文件组织、Probe/Scout/Deep Evidence 分层、预算与停止规则、current-view/lineage 分离、恢复演练。设计经反例推演固定后，再更新 Skill 和测试，最后启动大规模 campaign。
