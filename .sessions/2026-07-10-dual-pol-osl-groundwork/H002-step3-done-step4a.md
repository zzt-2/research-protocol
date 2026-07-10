# Handoff: Step 3 精读完成 → Step 4a 可行性 Go/No-Go（3 Q# 双偏振子方向）

> 来源: S001 | 交接目标: 新对话执行 GW Step 4a（Q-DP1/2/3 可行性评估）
> 文件名: H002-step3-done-step4a.md
> 日期: 2026-07-10

## 已完成边界

**GW Step 1-3 全部完成（双偏振 OSL 子方向）**：

1. **Step 1 检索穷举**：15 查询 + 综述补搜，43 核心候选 8 子方向，质量门槛全通过
2. **Step 2 下载**：9 篇成功 + sat.1553 = 10 篇精读（6 篇付费墙未获取）
3. **Step 3 精读**：9 篇新精读 + sat.1553 §6 补读，全过 title 自检。产出 `papers/_read_notes/` 9 篇笔记 + `projects/thesis-fso/literature_notes.md` 双偏振 OSL 沉淀节（含 5 类角度素材跨篇聚合视图 + 3 Q#）
4. **D002 角度素材 schema 验证通过**（3 批 9 篇试用，字段可用信号充分，可进 gw-read.md）

**3 个过四判据的 Q#**（Step 4a 假设合法来源）：
- **Q-DP1**（动态 SOP 跟踪均衡器）：5 篇独立静态建模=最强共识缝。M=动态SOP跟踪均衡器 C=双偏振星地湍流 A=现有CMA/MIMO假设准静态SOP
- **Q-DP2**（CMA fade 发散分析+鲁棒增强）：sat.1553 点名盲区 + L-DP8 实证。M=CMA fade发散分析 C=GG湍流深衰落 A=CMA发散概率未被分析
- **Q-DP3**（湍流深衰落跨帧 DSP 恢复）：L-DP5 明确 open + L-DP6 DSP outage。M=跨帧恢复机制 C=帧间湍流衰落 A=深衰落跨帧挂起

**最强根方向**：信道建模层×假设错（9 篇共性准静态信道假设，SOP-湍流耦合/动态相干时间未建模），覆盖 Q-DP1/2/3 三个现象。

**最强共识缝**：动态 SOP 跟踪（sat.1553§6 + L-DP1 + L-DP2 + L-DP5 + L-DP6 五篇独立静态建模）。

## 不要做什么

1. **不跳 Step 4a 直接试方法**（TL-30/FR-22）—— Q# 要走完 gw-feasibility A0/A'/A/B/D 维度
2. **不用 oracle 上界当 Go 判据**（TL-32/FR-25）—— Go=赢传统未优化 baseline 几 dB；oracle 上界只做 Step 4a 维度 D Kill 工具
3. **不预设方向**（守 D018——3 个 Q# 全评估完才排优先级，不先挑一个跑）
4. **不碰载波同步 v2 的 35 Q#**（那是单偏振搜索空间的产物，双偏振是独立搜索空间。两批 Q# 不混，分别评估）
5. **A1 归属检查**（D017 红线3）—— A 多孔径子方向 Ju 团队主导，Q-DP1 如果落在多孔径+动态SOP 要验是否已被 Ju 占完
6. **9 次 Kill 是物理事实**（不变量1）—— Q-DP1/2/3 是双偏振新空间，但要检查是否与 9 次 Kill 的单偏振结论冲突

## 必读

按优先级：
1. `stages/gw-feasibility.md`（Step 4a A0/A'/A/B/D 维度流程——FR-22 转步骤必须读）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（不变量 8 条 + 当前位置）
3. `projects/thesis-fso/literature_notes.md` 双偏振 OSL 精读沉淀节（Q-DP1/2/3 + 角度素材聚合视图 + 方法分类）
4. `.sessions/2026-06-20-problem-driven-redirection/decisions.md` D009（靠谱方向 checklist）+ D005（务实路线 Go 判据）
5. `stages/glossary.md`（问题四判据定义）
6. `thesis-lessons.md` TL-30/TL-32/TL-22/TL-27（框架门控/Go标准分离/物理前提/量级核算）

## 失败数据附录

无（本轮无路线失败。9 次 Kill 在上游专题，见 scenario-transfer-pivot topic-index 9 次 Kill 清单）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条）
- [ ] 已验证至少 3 条关键事实声称：
  - Q-DP1/2/3 过四判据（核查 `projects/thesis-fso/literature_notes.md` 双偏振 OSL 研究问题清单表）
  - 动态 SOP 跟踪是 5 篇独立共识缝（核查 5 篇笔记的 SOP 建模方式：sat.1553§6 + L-DP1 + L-DP2 + L-DP5 + L-DP6）
  - 9 篇精读笔记存在于 `papers/_read_notes/`（核查 `ls papers/_read_notes/10.1109_JLT.2023.3276637.md` 等）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**GW Step 4a 可行性 Go/No-Go**（gw-feasibility.md §4a）：
1. 读 `stages/gw-feasibility.md`（FR-22 必须读对应框架文件）
2. 对 Q-DP1/2/3 逐个走维度 A0（问题四判据复核）→ A'（空白零假设检查）→ A（方法产出形态+A1归属）→ B（baseline 可得性）→ D（oracle 上界/MVE 前置门控）
3. 守 FR-25（Go/Kill 对手标准分离）：Go=赢传统未优化 baseline；Kill=oracle 上界<0.5dB 或 MVE FAIL
4. 守 D018：3 个 Q# 全评估完才排优先级，不边评边 Kill
5. 产出 `feasibility_report.md`（双偏振子方向 A/B/D 维度）
