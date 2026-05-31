# Handoff: Ch3 HGAT 实验结论核实

> 来源: S011 | 交接目标: 新对话核实 Ch3 实验结论的真实性
> 文件名: H002-ch3-investigation.md

## 已完成边界

S011 跨章审查中，三个子 agent 基于 topic-index 和 decision_log 做出了以下 Ch3 相关结论，但这些结论**尚未与实际代码和结果文件交叉验证**：

1. **D019 声称**: 4 模型 × 3 seed 全部收敛，HGAT avg_best=-11.79，peak 性能四模型相当(-11.6~-12.0)，HGAT 训练稳定性领先(mean -138 vs MLP -331)
2. **D020 声称**: 零样本泛化 10→50 IoTD，GCN(-79) 优于 HGAT(-118)
3. **S009 声称**: S008 看 results/ 是旧残留，D019 有效数据在 results_final/(HGAT) + results_v2/(homo)，已合并回 results/
4. **贡献校准建议**: 从"HGAT 优于同构"改为"异构性需求实证分析"

## 不要做什么

- 不要只看 topic-index 就下结论——topic-index 可能是旧信息
- 不要假设 S009 的数据恢复操作完全正确
- 不要忽略代码中可能存在的 bug（D013 bugfix 之前的结果已无效）

## 必读（按优先级）

1. `projects/hgat-satellite-dag-offloading/decision_log.md` — D017-D020 是关键结果
2. `projects/hgat-satellite-dag-offloading/simulator/results/` — 查看实际结果文件，确认数据来源
3. `projects/hgat-satellite-dag-offloading/simulator/results_final/` 和 `results_v2/` — S009 恢复的数据
4. `projects/hgat-satellite-dag-offloading/simulator/eval_generalize.py` — 零样本泛化评估代码
5. `.sessions/thesis-final-review/topic-index.md` — S009 条目了解上下文

## 核心验证问题

### 问题 1: 4 模型收敛是否真实？

- 读 results/ 目录，查看每个模型的训练日志
- 确认 4 模型 × 3 seed = 12 个实验是否都有结果
- 验证 avg_best 数值是否与 D019 一致
- 特别关注 HGAT 的 3 个 seed 的 best 和 mean reward

### 问题 2: 训练稳定性差距是否真实？

- D019 声称 HGAT avg_mean=-138 vs MLP avg_mean=-331
- 验证方法：比较 3 seed 的 mean reward（不是 best reward）
- HGAT 的 mean 更接近 best 说明训练更稳定

### 问题 3: 零样本泛化结果是否真实？

- D020 声称 GCN=-79 优于 HGAT=-118
- 读 eval_generalize.py 了解评估方法
- 查看 10→50 IoTD 的评估结果文件
- 确认结果是否来自 D019 之后的有效数据

### 问题 4: homo 模型调参是否公平？

- D019 提到 homo 模型需要 lr=5e-5 + KL=1.0 + ppo_epochs=2 特殊调参
- HGAT 用标准超参 lr=3e-4
- 读 models_homo.py 和 run.py 确认调参差异
- 评估这是否影响"peak 性能相当"的结论

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| results/ 数据来源不明 | 数据溯源 | S009 声称已合并恢复 | 本轮验证 |
| 排队模型称 M/M/1 | 技术正确性 | 代码是确定性 FIFO | 论文写作时修正 |
| antenna_gain 未使用 | 技术完整性 | G2S 直连速率≈0 | 论文写作时说明 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落（注意不变量 #1 Walker-Delta 与 Ch3 无关）
- [ ] 已验证 D019 中的至少 3 个数值（best reward, mean reward, seed 数量）
- [ ] 已确认 results/ 目录结构
- [ ] 已确认"明确不含"范围：不做补实验（DAG 变体/环境扫描/重跑训练）

## 下一轮

1. 读 results/ 目录结构和文件
2. 读 decision_log D017-D020
3. 读 eval_generalize.py 代码
4. 逐一验证上述 4 个核心问题
5. 给出结论：Ch3 贡献定位建议是否成立
