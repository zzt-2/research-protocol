# Handoff 2026-05-16

## 当前进度

- 阶段：Groundwork Step 1-2（检索+初筛）
- 状态：完成
- Contract 状态：未启动（尚在 GW 阶段）
- 本轮完成：
  - AI 候选审查：5个JSON文件150条原始结果，去重后~70篇相关
  - 13篇必读、30篇建议读、5篇待确认、7篇备选
  - 4个子方向覆盖：MA-DRL for BH / 非DRL优化 / GNN卫星通信 / 综述
  - 所有质量门槛通过
  - JSON文件已标注 priority/priority_reason
  - literature_notes.md 完整审查列表

## 关键上下文

- **GNN+BH = 0** 完全空白（119条二轮深搜确认）
- **MA-DRL>40小区收敛困难**：Yang 2025 Tyche (JSAC) 明确指出
- **唯一切入点**：Lin 2025 graph mapping+GAN (ICT Express)，用图但非GNN
- 与 ISL 调度方向组合形成博士论文"星间+下行覆盖"互补结构
- 项目目录：`projects/leo-beam-hopping/`

## 精读优先级建议

1. M1 Yang 2025 Tyche (JSAC) — 痛点论证
2. M2 Lin 2025 Graph+GAN (ICT Express) — 图方法首次尝试
3. M10 Zhang 2025 DynHGNN (IEEE) — GNN+卫星下行干扰
4. M11 Geng 2024 Meta-GNN (IEEE) — GNN+卫星功率分配

## 下一步

1. 读 `stages/gw-read.md`（精读阶段框架文件）
2. 精读上述4篇论文（需先下载 content.md）
3. 填充 `literature_notes.md` 精读笔记部分
4. 完成后进入 Step 3.5 方向综合评估

## 关键文件路径

- 审查列表：`projects/leo-beam-hopping/literature_notes.md`
- 决策日志：`projects/leo-beam-hopping/decision_log.md`
- 检索结果：`search-archive/2026-05-16/satellite-beam-hopping-*.json`, `leo-satellite-beam-hopping-*.json`, `hts-beam-hopping-*.json`, `leo-satellite-time-slot-allocation-*.json`
- 方向侦察日志：`.sessions/direction-scouting/LOG-001-candidates.md §候选方向2`
