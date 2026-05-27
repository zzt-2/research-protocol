# 专题：三章论文全面质量审计

> 创建: 2026-05-22 | 状态: dormant（审计核心完成，修复执行转至 thesis-chapter-fixes 专题）
> 对三章论文（Ch1路由/Ch2切换/Ch3拥塞路由）做系统性质量审计，确保新颖性、实验完备性、指标完整性、跨章一致性均达标

## 审计维度

### A. 文献新鲜度 & 新颖性
- 每章最后检索距今的文献增量
- 核心声称 vs 最新 SOTA 实质性重叠检查
- 输出：每章的新颖性判定（SAFE / AT RISK / COMPROMISED）+ 具体竞品对比

### B. 实验完备性对标
- 该领域 top 论文（ToN/TWC/JSAC）的实验章节逐项提取
- checklist 项：基线数量、消融覆盖、统计检验、可视化类型、指标集合、泛化范围
- 输出：每章的实验覆盖度 checklist（PASS / MISSING / WEAK）

### C. 指标完整性
- 每章领域常用全指标盘点
- 缺失指标能否从现有数据计算 vs 需补实验
- 输出：指标矩阵（已有/可补/需新实验）

### D. 三章一致性 & 互不撞车
- Ch1 vs Ch3 差异化论证是否经得起追问
- 星座参数、实验设置、符号体系是否统一
- 输出：一致性报告 + 矛盾清单

### E. 数据自洽性
- paper-materials 每个数字追溯原始实验结果
- 同一指标在不同文档/表格中是否矛盾
- 输出：数据溯源表 + 矛盾修复清单

## 进展线索

### S001-setup.md — 专题建立与交接文档编写（2026-05-22）

建立审计专题，派 3 个 opus 子 agent 并行收集三章核心信息（paper-materials / literature_notes / contract / master-state），编写 4 份交接文档。

**Ch1 修复执行**：A1-A7 代码改造 ✅（thesis-chapter-fixes S001），P0 多 seed GPU 重跑 ✅（thesis-chapter-fixes S004，实测 ~6 min/seed vs 审计估 2h/seed，差 10x）。paper-materials 重写待进行。

**Ch2 修复执行**：M4 Jain 修复 ✅（thesis-chapter-fixes S001）。其他 P0-P3 修复项未开始 → 移至 thesis-chapter-fixes。

**Ch3 修复执行**：审计小改动(E03/E10/E12/CV+Overflow) ✅（thesis-chapter-fixes S001），拓扑升级 ✅（S002），GPU 重跑 E01-E12 ✅（S003），paper-materials 全面重写 ✅。Ch3 修复全部完成。

### H001-ch1-handoff.md — Ch1 路由 Size Gen 审计交接

Ch1 质量审计执行指南。核心风险：单 seed、4 实验未做(E06-E09)、PE 叙事调整、M2/M3/M5 未报。4 Phase 子 agent 调度计划（文献检索→竞品核查→实验对标→数据验证）。

### H002-ch2-handoff.md — Ch2 切换 Size Gen 审计交接

Ch2 质量审计执行指南。核心风险：GNN 贡献仅+0.8%、top-K 贡献分配悬殊、50UE 处 GNN 不如 MLP、消融编号混淆。额外输出：GNN 贡献叙事论证方案。

### H003-ch3-handoff.md — Ch3 拥塞/故障弹性路由审计交接

Ch3 质量审计执行指南。核心风险：TELGEN 泛化指标领先、DTAR/GMR 未直接对比、288 节点异常值、Ch1 同质化。额外输出：Ch1 差异化论证方案 + TELGEN 统一处理策略。

### H004-cross-chapter-handoff.md — 跨章一致性 & 最终汇总交接

三章独立审计完成后的跨章检查指南。Phase 1 三 agent 并行（参数/符号/实验设置一致性），Phase 2 Ch1 vs Ch3 差异化压力测试，Phase 3 竞品统一处理，Phase 4 最终汇总。

### S002-ch1-audit.md — Ch1 质量审计报告（2026-05-22）

Ch1 全面审计完成。新颖性 SAFE（4/4 核心声称无竞争），实验完备性 54%（14/26，低于 80% 阈值），指标完整性 PARTIAL（核心覆盖，统计严谨性缺失），数据自洽性 WARN（核心 PASS+3 处 LOW 矛盾）。3 项 P0（多 seed/p-value/M2 链路利用率），7 项 P1（E06/E07/E08/E09/推理延迟/CDF/收敛曲线）。6 个子 agent 并行执行。

### S003-ch2-audit.md — Ch2 切换 Size Gen 质量审计报告（2026-05-22）

Ch2 全面审计完成。新颖性 SAFE（310篇扫描，四要素组合无先例），实验完备性 WEAK（结构80%+但统计量/可视化缺失），指标完整性 FAIL（M3部分/M4缺失→60%），数据自洽性 FAIL（2 HIGH+2 MEDIUM矛盾）。GNN叙事三级递进方案。修复行动清单 P0-P4 共 19 项（~16h+6h GPU），分 3 个对话执行。**等待统一规划**。

### S004-ch3-audit.md — Ch3 拥塞/故障弹性路由质量审计报告（2026-05-22）

Ch3 全面审计完成。新颖性 SAFE（6组检索零覆盖，故障弹性+跨规模泛化组合仍为空白），实验完备性 8.0/10（12实验全有数据，E12未纳入paper-materials），指标完整性 7.5/10（CV/Overflow零成本可补），数据自洽性 6/10（3个必须修复的数字错误：E03表格数据错误、E12未纳入、E10"0.803"不可复现）。Ch1差异化 PASS（六维差异经得起追问）。TELGEN对比策略：正面讨论+互补定位。DTAR/GMR降级合理。6 个子 agent 并行。

### S005-consolidation.md — 跨章一致性 & 最终汇总审计报告（2026-05-22）

Phase 1-4 全部完成 + 代码验证。参数一致性 FAIL（Ch3 是纯抽象网格，无轨道力学；Ch1/Ch2 有完整轨道力学）。**关键代码验证发现**：Ch3 config.py 的 `altitude_km=780.0 # Iridium` 从未被代码引用，topology.py 全部 `distance_km=1.0`；Ch1 config.py 的 `GNN_LAYERS=2` 是过时值，实际训练用 3 层（train.py AC_LAYERS=3）。符号一致性 WARN（4 HIGH）。差异化 CONDITIONAL PASS。竞品处理 PASS。9 个子 agent + 主线程 7 项代码验证。

## 已确认结论

（从前置专题 thesis-structure-research / S003 继承的结论）

### 不变量
1. 三章主题：Ch1 路由 size gen → Ch2 切换 size gen → Ch3 拥塞/故障弹性路由
2. 方法统一叙事："GNN 结构化编码使零样本规模迁移成为可能"
3. 每章必须独立可发表（问题建模→算法设计→实验验证闭环）

### 其他结论
- S003 审查：Ch1 核心 PASS + 中文引用 FAIL；Ch2 核心 WARN(GNN+0.8%)；Ch3 核心 WARN(数据版本) + E12 缺失
- 修复完成：E10/E11 多seed ✅、E12 故障模式 ✅、数据统一 ✅、中文引用 ✅
- 跨章：Ch1 和 Ch3 都做卫星节点数泛化，需显式区分"路由策略泛化 vs 负载均衡能力泛化"
- TELGEN 是三章共同最强竞品

## 未决项

1. Ch2 是否补 N=30-40 拐点数据（可跳过，Limitations 中承认）→ 移至 thesis-chapter-fixes
2. ~~Ch2 文献新鲜度~~：2026-05-22 检索通过，SAFE（S003）
3. ~~Ch3 文献新鲜度~~：2026-05-22 检索通过，SAFE（S004）
4. ~~Ch3 数据修复~~：✅ E03/E10/E12 小改动已修复（thesis-chapter-fixes S001）
5. ~~Ch3 指标补充~~：✅ CV+Overflow 已纳入（thesis-chapter-fixes S001）
6. ~~三章符号体系/术语是否已统一~~：审计确认有冲突（S005），需在论文写作时统一 → 移至 thesis-chapter-fixes
7. ~~Ch3 Walker F=0 需代码确认~~：✅ 已验证，topology.py 无 F 参数，纯 4-regular 网格
8. ~~Ch1 GNN_LAYERS=2(config) vs 3层(论文)~~：✅ 已验证，train.py AC_LAYERS=3，config.py 过时
9. ~~Ch3 config.py 清理~~：✅ 拓扑升级后已解决（thesis-chapter-fixes S002）
10. ~~Ch3 paper-materials~~：✅ 全面重写，含"4-regular grid（Walker delta F=0 连通模式）"（thesis-chapter-fixes S003 后续）
11. ~~拓扑建模深度差异~~：Ch3 已升级为 Walker-Delta 物理仿真（thesis-chapter-fixes S002），声明仍需写入论文 → 移至 thesis-chapter-fixes

## 当前位置

审计专题全部完成（含代码验证）。S001 专题建立 → H001-H004 交接 → S002 Ch1 审计 → S003 Ch2 审计 → S004 Ch3 审计 → S005 跨章汇总+代码验证完成。9 个子 agent + 主线程 7 项代码验证。

**修复执行已转至 thesis-chapter-fixes 专题**：
- Ch1：A1-A7 ✅, P0 多 seed ✅, paper-materials 待重写
- Ch2：M4 Jain ✅, P0-P3 未开始
- Ch3：全部修复完成（小改动+拓扑升级+GPU 重跑+paper-materials 重写）

本专题转 dormant，如需回溯审计发现可随时激活。
