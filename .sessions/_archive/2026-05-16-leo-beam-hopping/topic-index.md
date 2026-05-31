# LEO 波束跳跃（续）

> 创建：2026-05-16 | 状态：closed | 描述：MVE 失败，战略转向

## 进展线索

- **H001-search-review** — Groundwork Step 1-2 检索+初筛完成。5个JSON文件150条原始结果，去重后约70篇相关，13篇必读。确认 GNN+BH 完全空白（119条二轮深搜验证），MA-DRL>40小区收敛困难（Yang 2025 Tyche JSAC 实证），唯一切入点为 Lin 2025 graph mapping+GAN。提出精读优先级建议。

- **H002-deep-reading** — Groundwork Step 3 精读完成。7篇论文（L01-L07）结构化提取+适配性分析。核心发现：GNN+BH=0完全空白；MA-DRL可扩展性瓶颈；所有MA-DRL竞品均用FC网络无图结构感知；GNN在卫星通信已成熟（超图干扰/meta-learning泛化/graph mapping）；分层/分解是主流策略。质量门槛全部通过。

- **H003-mve-fail** — Groundwork Step 4a 可行性评估，MVE 未通过。Step 3.5 补充检索发现1篇竞品（M14, AIAC 2024, 1cit），GNN+BH 从"零"下调为"近乎零"。A0/A/B 分析全部通过。MVE 三版均FAIL：v1干扰因子太弱、v2信道模型bug、v3环境正确但GNN+REINFORCE训练不稳定（IA-Greedy比Greedy高50%证明环境有效，但GNN排名最差）。提出修复方向（换PPO/SAC、reward shaping、增大规模）。

## 已确认结论

1. GNN+BH 方向近乎完全空白，唯一竞品仅1引用，差异化空间充足
2. MA-DRL方法在>40小区规模存在收敛困难，所有竞品均用FC网络无图结构感知
3. GNN在卫星通信其他场景（干扰建模、功率分配）已有成熟先例可迁移
4. 干扰拓扑确实是关键因素（IA-Greedy比Greedy高50%），验证了GNN切入点
5. A0/A/B 可行性分析全部通过，无致命信号
6. MVE 三版失败，根本原因是GNN+REINFORCE在C(19,3)=969动作空间上训练不收敛

## 未决项

1. MVE修复方向已明确（换PPO、reward shaping、37 cells规模），但尚未执行
2. 如MVE修复后仍失败，需考虑战略转向（GNN作为辅助模块或转向监督学习）
3. 专题已关闭，后续是否重新启动待定

## 当前位置

Groundwork Step 4a 可行性评估阶段，MVE三版失败后专题关闭，战略转向。
