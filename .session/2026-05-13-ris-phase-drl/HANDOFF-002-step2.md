# Handoff 2026-05-13 #2

## 当前进度
- 阶段：GW Step 4a 完成，**用户已确认 Go**，准备进入 Step 5（Baseline 选定）
- 状态：正常推进
- 本轮完成：
  - Step 1-3 全部完成（检索 89 条 / 下载 15 篇 / 精读 8 篇）
  - Step 4a 方向可行性报告已撰写，用户确认 Go
  - 用户确认主攻方向：大规模 RIS + 连续相移 + 高级 DRL

## 关键决策
- **主攻方向**：空白 1 — 大规模 RIS（100+ 元素）+ 连续相移 + 高级 DRL（TD3/SAC）
- **可选扩展**：空白 2（不完美 CSI 鲁棒性）
- 用户未选择叠加空白 2，聚焦空白 1

## 核心文件路径
- `projects/ris-phase-drl/literature_notes.md` — 8 篇精读 + 综合分析 + Baseline 交叉验证
- `projects/ris-phase-drl/feasibility_report.md` — Step 4a 可行性报告
- `projects/ris-phase-drl/decision_log.md` — 决策记录
- `projects/ris-phase-drl/coverage-gap-report.md` — 文献覆盖面报告
- `search-archive/2026-05-13/ris-phase-drl-merged.json` — 89 条搜索结果

## Baseline 候选（已预选，待 Step 5 正式评估）
| 候选 | 来源 | 算法 | 优先级 |
|------|------|------|--------|
| B1: DDPG | L02 | 连续动作空间，长期CSI | 1 |
| B2: AB-TD3 | F3 | attention+BN，超参最完整 | 1 |
| B3: DDQN+GA | L06 | 离散相移+贪心细化，大RIS | 2 |
| B4: SAC | F4 | 最大熵，连续动作 | 2 |
| B5: Random phase | 通用 | 最基础对照 | 4 |

## 注意事项
- 所有论文均未开源代码，全部需自实现
- 奖励函数归一化普遍缺失，复现时需自行设计
- 大规模 RIS 连续相移的动作空间维度爆炸是核心挑战，L06 的列级压缩思路可参考
- 信道模型参数很多 [NOT_FOUND]，仿真器设计时需做 [ASSUMPTION] 并标注

## 下一步
1. 读 `stages/gw-validate.md` 执行 Step 5：Baseline 候选正式选定
2. 读 `stages/gw-feasibility.md` §4b 执行 Step 4b：执行可行性验证
3. 两步可并行准备
