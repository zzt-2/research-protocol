# Decision Log — ris-phase-drl

## 阶段摘要
- [Groundwork] 进行中 — Step 3 文献精读
- [Contract] 待开始
- [Execute] 待开始

## 决策记录
[D001] 研究方向确定为 RIS/IRS 辅助通信中的相移优化 + DRL 方法 | 理由: 用户指定 | 阶段: GW
[D002] 检索策略：3 组关键词（RIS phase shift DRL / IRS RL beamforming / RIS DRL resource allocation MIMO），academic mode + scenario-method preset | 理由: 覆盖不同术语体系 | 阶段: GW
[D003] 精读优先级：语义筛选而非纯关键词匹配 | 理由: 脚本 relevance_score 是纯词频匹配，会系统性低估用不同术语的高相关论文 | 阶段: GW
[D004] 精读范围：8 篇（Tier 1 核心相移+DRL × 3 + Tier 2 DRL+RIS × 3 + Tier 3 相关变体 × 2）| 理由: 覆盖 DQN/DDPG/TD3/PPO/混合动作空间 + 被动/主动/空中 RIS 变体 | 阶段: GW
[D005] 4a Pivot：用户认为空白 1（大规模 RIS + 连续相移 + 高级 DRL）的新颖性未被充分验证，现有检索可能遗漏直接竞争论文 | 理由: 需确保真有新颖性/差异性/可实现性 | 阶段: GW Step 4a
[D006] 补充检索方向：针对空白 1 定向扩展检索，关键词聚焦 large-scale/massive RIS + continuous phase shift + TD3/SAC/PPO/scalable DRL | 理由: 验证空白是否真实存在 | 阶段: GW Step 1（回退）
[D007] 补充检索完成，空白 1 新颖性确认"高"：5 组检索 + 3 篇候选竞争论文精读。最直接竞争者 L002 (arXiv:2506.10815, Extremely Large Scale RIS + A2C) 已撤稿。RISnet (L017) 用无监督学习不是 DRL。无已发表竞争者 | 理由: Pivot 后定向验证完成 | 阶段: GW Step 4a
