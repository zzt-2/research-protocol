# Decision Log

## 阶段摘要
- [Direction Scouting] 方向侦察完成，作为备选第二研究方向
- [Groundwork] Step 1-2 检索+初筛完成，Step 3 精读完成（7 篇），Step 3.5 待启动

## 决策记录

### D003: Step 3 精读 7 篇完成 (2026-05-16)
- **输入**: L01 Yang Tyche JSAC, L02 Zhang DynHGNN TWC, L03 Geng Meta-GNN TVT, L04 Lin Graph+GAN ICT Express, L05 Gong QPLEX TWC, L06 Lin QMIX-BH TVT, L07 Wang Cooperative BH TWC
- **结论**: 7 篇精读完成，综合分析已撰写，质量门槛全部通过
- **关键发现**:
  - MA-DRL >40小区收敛困难实证确认（L01 Tyche JSAC）
  - GNN 在卫星干扰/功率分配已成熟（L02 DynHGNN 超图, L03 Meta-GNN 泛化）
  - graph mapping 首次引入 BH（L04）但非 GNN
  - 分层 MA-DRL 是主流（L05 QPLEX 分层, L06 QMIX 两阶段, L07 三层解耦）
  - 所有 MA-DRL 均用 FC 网络，无图结构感知，这是可超越的关键点
  - GNN+BH 仍为零，创新空白确认
- **质量门槛**: 4/4 全部通过（精读7≥5✓, Baseline非空✓, 核心贡献≥2句✓, 综合分析✓）
- **产物**: `literature_notes.md` 精读笔记 L01-L07 + 综合分析

### D001: AI 候选审查完成 (2026-05-16)
- **输入**: 5个JSON检索文件，~150条原始结果
- **结论**: 去重后~70篇相关论文，13篇必读，4个子方向覆盖
- **关键发现**:
  - GNN+BH=0 完全空白（二轮深搜119条追加确认）
  - MA-DRL>40小区收敛困难（Yang 2025 Tyche JSAC确认）
  - 唯一图方法BH论文（Lin 2025 graph+GAN）为切入点参考
- **质量门槛**: 全部通过（去重70≥20, 必读13≥5, 4个子方向≥2, 正式发表~75%≥50%）
- **产物**: `literature_notes.md`
