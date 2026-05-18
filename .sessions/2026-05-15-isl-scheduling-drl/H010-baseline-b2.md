# Handoff 2026-05-15 (Round 10)

## 当前进度
- 阶段：GW Step 7 §impl Part B — B1 + B2 均已实现
- 状态：Part B 完成
- Contract 状态：未开始
- 本轮完成：
  - B2 (Wang TCOM MADRL) 实现：`baselines/wang_madrl.py`（~330 行）
  - B2 训练循环验证通过（24×20, 50 episodes）
  - B1 vs B2 对比完成
  - Baseline 报告更新：`baseline_report.md`
  - Decision log 更新：[D011]

## 关键结论

### B2 测试规模结果（24×20, 50ep 训练）
| 方法 | M1 吞吐量 | M4 阻塞率 | M5 公平性 |
|------|---------|---------|---------|
| B1 Fixed | 0.173 | 0.827 | 0.519 |
| B2 Trained | 0.118 | 0.882 | 0.422 |

B2 未优于 B1（-31.9% throughput），原因：
1. B1 有 4 固定 ISL vs B2 的 3+1 结构，B2 少 1 条固定跨轨链路
2. 测试规模候选不足（3 个/星 vs 全规模预期 >7）
3. 训练不充分（50ep × 20 步 vs L09 原始更充分）
4. [D011] 已记录，不阻塞——全规模预期改善

### GW Step 7 框架门槛
- ✅ 仿真器验证清单全部通过
- ✅ MDP 试运行检查通过
- ✅ 至少 1 个 baseline 成功复现（B1）
- ✅ 路径合规（simulator/ + baselines/）

**GW Step 7 完成，可进入 Contract 阶段。**

## 下一步
1. **进入 Contract 阶段** — 读 `stages/contract.md` 开始
2. **全规模测试**（Execute 阶段）：在 24×66=1584 上重评估 B1+B2
3. **可见性优化**：向量化候选边计算（为 1584 星加速）

## 文件路径
- B1 代码：`baselines/grid_fixed.py`
- B2 代码：`baselines/wang_madrl.py`
- 验证脚本：`verify/verify_baselines.py`
- Baseline 报告：`baseline_report.md`
- 决策日志：`decision_log.md`（含 [D010] B1, [D011] B2）
- 仿真器设计规格：`simulator_spec.md`
