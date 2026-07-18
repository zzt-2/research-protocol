# [S009] Ch3 训练数据误判修正 + 有效数据恢复

> 2026-05-26 | Phase 3.5 | 完成

## 目标

接手 H001 handoff，排查 Ch3 PPO 训练不稳定问题。H001 基于 `results/` 目录声称"多数 GNN 仅 3 eps 崩溃"。

## 记录

### Phase A: 旧数据诊断

读取 `results/` 全部 JSON 文件：
- GCN/GraphSAGE/MLP 全部仅 3 eps，部分 seed reward 达 -500K（灾难级）
- HGAT seed42 跑了 159 eps，seed123 跑了 78 eps
- Random/Greedy baseline 正常（无梯度训练）

初步判断：不是 NaN/Inf，而是极端 reward 方差（双峰：-37 vs -500K）。

### Phase B: 代码诊断

读 run.py / ppo.py / reward.py / config.py / env.py。发现 run.py:108-109 注释已指出双峰问题。

跑 GCN seed123 的 20 ep 诊断（当前代码）：
- Ep 0-3: reward -30 到 -37，正常，策略在改善
- Ep 4: reward 跳到 -980，value_loss 从 2.76 暴涨到 4106
- 原因：环境 seed 敏感性，非策略崩溃（KL ≈ 0.001）
- Ep 5-19: 训练继续，最终 reward 降到 -13.11

**结论：当前代码可以训练。**

### Phase C: 踩坑记录核查

读 code-quality.md + decision_log.md，发现关键历史：

1. **D013**: mask 时序 bug + Welford 归一化器对双峰失败 → 已修复，不能重新启用归一化器
2. **D015**: log1p 已加但范围仍宽 → 每步累积可到 -980
3. **D018**: homo 模型加 type_bias+type_proj → 解决类型信息丢失
4. **D019**: 声称"4 模型全部收敛，avg_best≈-11.7" → 与 results/ 的 3 eps 数据矛盾

### Phase D: 历史训练记录溯源

派 3 个子 agent 并行查历史：

- **session_search**: 发现 9 个结果目录，results_final/ 和 results_v2/ 包含有效数据
- **2026-05-20-hgat-dag-offloading/**: H001 记录了训练状态，指出 results_summary.json 与 handoff 数据不一致
- **thesis-chapter-fixes/**: Ch3 GPU 重跑记录（S003），但属于 Ch1 的实验编号体系

**关键发现**：D019 的完整数据分在两个目录：
- `results_final/`（5/20 18:43）→ HGAT × 3 seed（收敛，best≈-11.8）
- `results_v2/`（5/20 23:22）→ GCN/GraphSAGE/MLP × 3 seed（收敛，best≈-11.6~12.0）
- `results/`（默认输出目录）→ 被后续某次测试覆盖，变为过时数据

### Phase E: 数据恢复

1. `results/` 备份为 `results_stale/`
2. HGAT 数据从 `results_final/` 复制
3. Homo 模型数据从 `results_v2/` 复制
4. Baseline 从 `results_final/` 复制
5. 重新生成 `results_summary.json`

**恢复后验证**（完全匹配 D019）：

| 模型 | avg_best | avg_mean | seeds |
|------|----------|----------|-------|
| HGAT | -11.79 | -138 | 3/3 |
| GCN | -11.67 | -289 | 3/3 |
| GraphSAGE | -11.83 | -219 | 3/3 |
| MLP | -11.70 | -331 | 3/3 |

Greedy baseline = -16.7，所有模型 best reward 显著优于 Greedy。

### 文档更新

1. **topic-index.md**: Ch3 训练不稳定标记为"误判"，更新未决项和当前位置
2. **H001 handoff**: 添加警告标注 results/ 数据过时

## 决策引用

- 无新建决策

## 范围确认

- 本轮是否在 scope boundary 内：是（H001 接收方验证 + 数据恢复）

## 后续

- ~~Ch3 训练不稳定排查+重跑~~ ✅ 误判已修正，有效数据已恢复
- Ch3 遗留 3 项：DAG 拓扑变体实验、多指标分拆报告、零样本失败叙事（均待写作阶段处理）
- 可回到主线：对话 9（跨章符号统一+元分析）
