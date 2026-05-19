# Handoff: Contract 冻结，进入 Execute

> 来源: Contract Step 0-6 | 交接目标: 进入 Execute 阶段
> 文件名: H008-contract-frozen.md

## 已完成边界

### Contract 全部完成并冻结 (2026-05-19)

- **Step 0**: 新颖性确认（简化路径，复用 GW 检索）
- **Step 1**: 假设形成 — MatchingGAT R2C ≥5% over DualGAT+，scope ≥50 节点网络
- **Step 2**: Contract 草稿 — 含假设/信号/baseline/指标/公平规则/消融/实验列表/仿真配置/声称-证据映射
- **Step 3**: 参数溯源验算 — 17 参数全部溯源，无 [ASSUMPTION]
- **Step 4**: 端到端推演 — data-flow.md 8 步无断层，FR-13 全部 ≥
- **Step 5**: 压力测试 + 反模式 — Tier 1+2 全 pass，反模式 4 项全 pass
- **Step 6**: 冻结（用户已确认）

### 风险调整（冻结前）

基于 code-quality.md 失败模式审查：
1. 假设 scope 收窄至 ≥50 节点（排除 GEANT 小规模场景）
2. GEANT 降级为补充验证
3. 增加 E6 SFC ratio 灵敏度实验
4. 增加 R1-R5 已知风险与缓解节

### 核心实验清单

| 编号 | 实验 | 优先级 |
|------|------|--------|
| E1 | MatchingGAT vs B1-B5, WX100, 30ep, 3 seeds | P0 |
| E2 | 跨拓扑泛化 (BRAIN/WX500 主 + GEANT 补充), 30ep, 3 seeds | P0 |
| E3 | 消融 A1-A3, WX100, 30ep, 3 seeds | P0 |
| E4 | 收敛分析（训练曲线） | P1 |
| E5 | 推理复杂度 | P2 |
| E6 | SFC ratio 灵敏度 (0.3/0.6/0.9) | P3 |

### Success Signal

1. R2C ≥5% over DualGAT+ (WX100/BRAIN/WX500, 3 seeds)
2. AC ≥0.95
3. 各消融组件 ≥1.5% R2C

### Failure Signal

1. R2C <3% (边际)
2. R2C <2% on BRAIN/WX500 (拓扑特异)
3. 无组件贡献 >2% R2C

## 不要做什么

- 不要改假设/信号/公平规则/消融计划 — Contract 已冻结，改了要 Amendment
- 不要用 5ep/10ep 结果写论文 — 必须 30ep + 3 seeds
- 不要跳过 E3 (30ep 消融) — GW 消融仅 10ep，必须补 30ep
- 不要把 GEANT 结果纳入核心论证 — scope 限定 ≥50 节点
- 不要对单个 baseline 单独调超参 — 共享 Virne 默认（Fairness Rules #2）
- 不要先看结果再调整 success signal — 这是 Contract 最核心的约束

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态恢复
2. `projects/nfv-sfc-vne/contract.md` — **冻结的 Contract**（Execute 阶段圣经）
3. `stages/execute.md` — Execute 阶段流程
4. `projects/nfv-sfc-vne/data-flow.md` — 端到端数据流参考

## 下一轮

1. **读 `stages/execute.md`** — 进入 Execute 阶段
2. **Execute Step 0**: 准备工作（环境确认、脚本准备）
3. **E1 主对比实验**: MatchingGAT vs B1-B5, WX100, 30ep, 3 seeds — 这是第一步
4. **GEANT 快速预验证**: 5ep 快速确认趋势（风险 R1 缓解）
5. **E3 消融**: 30ep 严格消融（E2 可与 E1 并行）
