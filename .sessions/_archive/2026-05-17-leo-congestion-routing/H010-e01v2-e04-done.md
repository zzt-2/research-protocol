# Handoff 2026-05-17

## 当前进度
- 阶段：Execute Step 2
- 状态：E01-v2 + E04 全部完成，核心假设验证通过
- Contract 状态：amended（K-path 离散动作空间）
- 本轮完成：E01(500ep) → E04(泛化) → E01-v2(800ep)，双指标 PASS

## 关键结果

### E01-v2 (800ep, entropy=0.02, 3 seeds, 87.9min)
- GNN: MLU = 1.9810 ± 0.0300
- ECMP: MLU = 2.4230 ± 0.8469
- MLP: MLU = 2.4106 ± 0.0104
- **GNN/ECMP = 0.8176 PASS** (目标 ≤0.90)
- **GNN/MLP = 0.8218 PASS** (目标 ≤0.85)

### E04 (66→48 zero-shot, 1.7min)
- GNN zero-shot: MLU = 1.9554 (仍优于 ECMP)
- MLP zero-shot: MLU = 2.8335 (比 ECMP 差 33.9%, **崩溃**)
- GNN/MLP zero-shot = 0.69 (跨规模优势 31%)

### 修复路径
- E01 原始 GNN/MLP=0.8632 FAIL → 增训练轮次 500→800ep + entropy 0.01→0.02 → GNN/MLP=0.8218 PASS
- 根因: seed 敏感性来自训练不充分, GNN std 从 0.12 降至 0.03

## 产出文件
- `simulator/results/e01_results.json` — E01 原始结果
- `simulator/results/e01_v2_results.json` — E01-v2 结果
- `simulator/results/e04_quick_results.json` — E04 泛化验证
- `run_e01.py` — E01 脚本
- `run_e01_v2.py` — E01-v2 脚本
- `run_e04_quick.py` — E04 脚本
- `master-state.md` — 已更新
- `decision_log.md` — D17(分析) + D18(E01-v2+E04 结论)

## 下一步
1. E02: 无故障场景对比 (failure_rate=0)
2. E03: 突发流量场景 (surge_factor 增大)
3. E04-E06: 完整泛化实验 (48/288/720 节点, 正式版)
4. E07-E11: 消融实验

## 恢复读取顺序（新对话）
1. 本 HANDOFF 文件
2. `master-state.md`
3. `contract.md`（amendment 版本）
4. `simulator/results/e01_v2_results.json` + `e04_quick_results.json`
5. `stages/execute.md` — 了解后续 E02-E11 的定义
