# Handoff: Step 4a 可行性评估完成 → 交用户确认 Go/No-Go + 进维度 D MVE

> 来源: S002 | 交接目标: 用户确认 Q-DP1 Kill / Q-DP3 首选 / Q-DP2 备选，确认后新对话进维度 D MVE
> 文件名: H003-step4a-done-user-confirm.md
> 日期: 2026-07-10

## 到哪了（状态）

**GW Step 4a 可行性评估完成**（双偏振 OSL 子方向 Q-DP1/2/3）。2 个子 agent 做了物理量级核查（TL-27）+ FR-20 参数溯源，3 个 Q# 全部走完 A0/A'/A/B/D，写进 `projects/thesis-fso/feasibility_report.md` 双偏振章节。

**结论**：
- **Q-DP1（动态 SOP 跟踪均衡器）：No-Go（Kill）**——A0 §1 致命。均衡器跟踪上限 300 krad/s 高出真实湍流致 SOP 速率（kHz-几十 krad/s）1-2 数量级，A 假设"动态 SOP 下跟踪滞后致失效"在"湍流致 SOP"C 条件下物理基础不足。SOP 快变真实来源是机械振动/热漂移，不是湍流。（D001）
- **Q-DP2（CMA fade 发散分析）：Conditional Go**——空白真实（sat.1553 综述自认"未被分析"），但需自建 GG 时间域衰落模型（现有文献只给幅度 PDF，衰落持续时间/频率全篇缺失）。（D002）
- **Q-DP3（跨帧 DSP 恢复）：Conditional Go（首选）**——物理基础最扎实（跨帧+挂起+恢复 open 三点文献直接支撑），竞争维度先验覆盖度最低。需 MVE 验证恢复机制有效性。（D003）

## 下一步干什么

**先交用户确认**（本轮产出已交，等用户拍板）：
1. Q-DP1 No-Go 是否认可（或讨论 Pivot 出口：C 改"机械振动致 SOP"）
2. Q-DP3 作为首选 Conditional Go 进维度 D MVE 是否认可
3. Q-DP2 作为备选是否认可

**用户确认 Q-DP3 首选后**，新对话第一步：
1. 补 FR-20 参数溯源：查大气湍流时间模型（Greenwood 频率 / 横风速度 / 功率谱）建 GG 时间域衰落模型——这是 Q-DP2/DP3 共享基建
2. 验证 L-DP5 跨帧结论的预期性（L-DP5 湍流未显式仿真，跨帧是预期分析）——用真实时间模型确认跨帧真实
3. 进维度 D MVE：验证跨帧恢复机制有效性（恢复时间 / outage 概率 vs L-DP5 被动冻结 baseline）
4. MVE 必须含架构摘要（FR-11）+ 先验对照（FR-14，L-DP5 被动冻结）+ 贡献目标 baseline 对照（FR-15，L-DP5）

## 纪律（和下一步直接相关的约束）

1. **守 FR-22**：现在在 GW Step 4a，用户确认后进维度 D（MVE）。Q-DP1 已 Kill 不复活。
2. **守 FR-25/TL-32**：Q-DP3 的 Go 判据 = 赢 L-DP5 被动冻结（传统未优化 baseline）几个 dB；oracle 上界（outage ~50%→0）只确认不触发 Kill，**不当 Go 判据**。
3. **守 TL-27/FR-20**：MVE 执行前必须先补 GG 时间模型物理参数（Greenwood 频率等），标文献来源，禁止"为了让方法有用"拍参数。
4. **守 TL-22**：MVE 前先建理论预期——恢复机制在什么衰落条件下能赢被动冻结，偏离即查。
5. **GG 时间模型是共享基建**：Q-DP2 和 Q-DP3 都依赖，先建一次两个方向受益。
6. **单对话 ≤3 步 + 主对话禁 WebSearch**：物理参数查证用 tools/search 或子 agent。

## 不要做什么

1. **不复活 Q-DP1 当贡献**（不变量1 适配版——Q-DP1 是 A0 物理致命 Kill，不是思路素材，Pivot 出口需用户确认才探索）
2. **不用 oracle 上界当 Q-DP3 的 Go 判据**（TL-32——outage 量级改善是 Kill 工具确认，Go 要赢 L-DP5 被动冻结）
3. **不跳维度 D 直接进 Contract**（FR-22——Conditional Go 要走完 MVE 才进 Step 5）
4. **不忽视 L-DP5 跨帧的预期性**（L-DP5 湍流未显式仿真，进 MVE 前要用真实时间模型确认跨帧真实，不能拿预期论述当实测证据）
5. **不碰载波同步 v2 的 35 Q#**（单偏振搜索空间，独立评估不混）

## 失败数据附录

Q-DP1 Kill 核心数据（D001）：
- 均衡器跟踪上限 300 krad/s（DA-LMS+CMA，sat.1553§6 L778）
- 真实湍流致 SOP 速率：4 篇精读论文均无实测数值；湍流相干时间 >1ms（sat.1553 L167）→ kHz-几十 krad/s 量级
- 差距：均衡器上限高出 1-2 数量级
- sat.1553 作者原话："OSL 的 SOP 旋转可能较慢 → MMSE 可行"（MMSE 上限仅 1-10 krad/s）
- SOP 真实来源：机械振动/热漂移/光学元件双折射（sat.1553 L563），不是湍流

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| GG 时间域衰落模型缺失 | FR-20 参数溯源 | 全篇无衰落持续时间/频率数据 | Q-DP3 进 MVE 前必须补（查 Greenwood 频率/横风模型） |
| L-DP5 跨帧结论预期性 | FR-26 证据链 | L-DP5 湍流未显式仿真，跨帧是预期分析非实测 | MVE 前用真实时间模型验证跨帧真实 |
| Q-DP2/DP3 发散/恢复 dB 量级未知 | D005 务实路线需 dB | Conditional Go 但量级未验证 | MVE 验证 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| Q-DP3 恢复机制有效性 | 恢复时间 < L-DP5 被动冻结；outage 概率显著降低 | D005 赢传统 baseline + FR-15 贡献目标对照 | 待 MVE |
| GG 时间模型物理参数溯源 | 每个关键参数（衰落深度/持续时间/频率）标文献来源 | FR-20 / TL-26 | 待补 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条）
- [ ] 已验证至少 3 条关键事实声称：
  - Q-DP1 Kill 依据（核查 `feasibility_report.md` Q-DP1 A0 §1 节 + sat.1553§6 L778/L745 跟踪速度数值）
  - Q-DP3 Conditional Go 首选（核查 `feasibility_report.md` Q-DP3 节 + L-DP5 L766-771 跨帧挂起原文）
  - 3 Q# 与 9 次 Kill 不冲突（核查 scenario-transfer-pivot/decisions.md D001 L16/L165 单偏振 vs 双偏振正交）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**新对话第一件事**：读 H003 + topic-index + feasibility_report.md 双偏振章节 → 确认用户已拍板 → 如 Q-DP3 首选，补 FR-20 大气湍流时间模型参数 → 建共享 GG 时间域衰落模型 → 进维度 D MVE。
