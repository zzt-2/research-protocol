# 专题：RIS 相移优化 DRL

> 状态：dormant | 创建：2026-05-13 | last_updated：2026-05-13

## 进展线索

| 编号 | 文件 | 摘要 |
|------|------|------|
| H001 | H001-initial.md | GW Step 1-3 完成：检索 89 条候选（3 组关键词、5+ 搜索源），下载 15 篇论文（8 篇脚本 + 7 篇手动），精读 8 篇（DDQN/DDPG/TD3/SAC/PPO/混合 PPO/联邦 DRL），literature_notes.md 和 decision_log.md 已撰写，覆盖面缺口报告已生成。下一步进入 Step 4a 方向可行性。 |
| H002 | H002-step2.md | GW Step 4a 完成，用户确认 Go。主攻方向锁定：空白 1 — 大规模 RIS（100+ 元素）+ 连续相移 + 高级 DRL（TD3/SAC）。Baseline 候选预选 5 个（B1 DDPG、B2 AB-TD3、B3 DDQN+GA、B4 SAC、B5 Random），待 Step 5 正式选定。下一步并行推进 Step 5（Baseline 选定）和 Step 4b（执行可行性验证）。 |

## 已确认结论

1. **主攻方向**：大规模 RIS（100+ 元素）+ 连续相移 + 高级 DRL（TD3/SAC），用户已确认 Go
2. **精读覆盖 7 种算法**：DDQN/DDPG/TD3/SAC/PPO/混合 PPO/联邦 DRL，文献覆盖面达标
3. **Baseline 候选池**：B1 DDPG（优先级 1）、B2 AB-TD3（优先级 1）、B3 DDQN+GA（优先级 2）、B4 SAC（优先级 2）、B5 Random（优先级 4）
4. **所有论文均未开源代码**，复现需全部自实现
5. **奖励函数归一化普遍缺失**，复现时需自行设计，是已知陷阱
6. **大规模 RIS 连续相移的动作空间维度爆炸**是核心挑战，L06 的列级压缩思路可参考

## 未决项

1. GW Step 5：Baseline 候选正式选定与评估
2. GW Step 4b：执行可行性验证
3. 信道模型参数存在 [NOT_FOUND]，仿真器设计时需做 [ASSUMPTION] 并标注
4. Step 5 与 Step 4b 的并行推进安排

## 当前位置

GW Step 4a（方向可行性）已通过 Go 决策，主攻方向已锁定，待续接后并行推进 Step 5（Baseline 选定）和 Step 4b（执行可行性验证）。
