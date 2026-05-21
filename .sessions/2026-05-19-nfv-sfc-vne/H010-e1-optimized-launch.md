# Handoff: E1 优化后待启动

> 来源: D023+D024 | 交接目标: 启动优化后的 E1 实验，等待结果后判定
> 文件名: H010-e1-optimized-launch.md

## 已完成边界

### 架构修复 ✅
- `matching_policy.py:123` 从 `p + curr_cross` 改为 `p + p * curr_cross`（方案 B）
- 5ep 验证通过：R2C 0.48→0.75 陡升，eval R2C=0.762

### 训练加速优化 ✅
- **PPO 配置**：batch_size 128→256, repeat_times 10→4（PPO 更新 40→6 次/ep）
- **实验参数**：VNRs 500→300, Epochs 30→15
- **收敛依据**：旧 30ep 日志显示两模型 ep8-10 均进入平台区
- **范围缩减**：仅 MatchingGAT vs DualGAT+（2 solver × 3 seed = 6 runs）
- **实测加速**：148s/ep vs 200s/ep（26%），总预估 ~3.7h vs ~16h

### environment deepcopy 优化失败
- `nx.Graph.copy()` 不保留 PhysicalNetwork 类级属性，已回退
- 不影响实验，仅影响训练速度

### 已有结果
- `results/sfc_pg_mlp_seed0.txt`：AC=0.908, R2C=0.5985
- `results/sfc_ppo_dual_gat+_seed0.txt`：AC=0.958, R2C=0.8006
- 旧 buggy MatchingGAT seed=0 已删除

## 不要做什么

- 不要恢复 environment.py 的 deepcopy 改动（会崩溃）
- 不要恢复 30ep/500VNRs——收敛数据支持 15ep/300VNRs
- 不要在 E1 跑完前启动 E3 消融——E3 依赖修复后的 MatchingGAT
- 不要改 Contract 的 success/failure signal

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 当前状态
2. `projects/nfv-sfc-vne/decision_log.md` — D023（架构修复）+ D024（加速优化）
3. `projects/nfv-sfc-vne/verify/run_e1.sh` — E1 启动脚本（已更新：15ep, 300VNR, 2 solvers）
4. `projects/nfv-sfc-vne/verify/run_sfc_baselines.py` — 训练脚本（已更新：bs=256, rt=4）
5. `projects/nfv-sfc-vne/contract.md` — 冻结的 Contract（success: R2C ≥5% over DualGAT+）

## 下一轮

1. **启动 E1**: `cd /mnt/d/code/study/research-protocol/projects/nfv-sfc-vne && bash verify/run_e1.sh`
2. **等待 ~3.7h**: 6 runs（MatchingGAT + DualGAT+ × 3 seeds）+ GRC baseline
3. **汇总结果**: `python verify/summarize_e1.py`
4. **判定 Contract signal**:
   - PASS: MatchingGAT R2C ≥5% over DualGAT+（即 ≥0.84）
   - MARGINAL: 3-5%
   - FAIL: <3%
5. **如果 PASS**: 启动 E3 消融（30ep × 3 seeds × 4 variants），E2 跨拓扑
6. **如果 MARGINAL/FAIL**: 分析原因，考虑进一步优化或转向框架贡献
