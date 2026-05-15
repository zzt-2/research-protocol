# Baseline Report

> Groundwork Step 6 产出：仿真器验证 + Baseline 复现结果。

## 1. 仿真器验证

### 1.1 模块验证结果

| 检查项 | 结果 | 详情 |
|--------|------|------|
| FSPL 解析 | PASS | d=550km f=12GHz → 168.83 dB，与公式精确匹配 |
| 大气衰减 | PASS | 20°=0.585dB, 45°=0.283dB, 90°=0.200dB，单调递减 |
| 阴影衰落 σ | PASS | 20°=4.0dB, 45°=1.5dB, 90°=1.0dB，按 TR 38.811 单调递减 |
| Shannon 容量 | PASS | SINR=10dB B=250MHz → 864.9 Mbps，精确匹配 |
| R_norm 归一化 | PASS | SINR=10dB → 0.4728，符合 log₂(1+SINR)/log₂(1+SINR_max) |
| 仰角计算 | PASS | 正上方卫星 → 90.0° |
| 可见卫星统计 | PASS | 平均 4.4 颗/UE，范围 2-6 颗 |
| 自相关预警 | PASS | lag-1 = 0.197，远低于 0.95 警戒线 |
| 退化测试 | PASS | 阴影模型重置功能正常 |

### 1.2 MDP Checkpoint（奖励合理性）

| 策略 | 吞吐量项 | 负载项 | 阻塞项 | 切换项 | 总奖励 |
|------|---------|--------|--------|--------|--------|
| Random | 60.9% | 31.0% | 0.0% | 8.1% | +586.7 |
| Greedy | 58.2% | 5.2% | 36.0% | 0.5% | -118.0 |

- **无单一项独占**：最大项 60.9% < 95% → PASS
- **策略区分度**：Random vs Greedy 差距 120% > 10% → PASS
- **关键指标可优化**：Greedy 阻塞率远高于 Random → DRL 有优化空间

### 1.3 仿真器参数

| 参数 | 值 |
|------|------|
| 星座 | 18面×22星=396，550km，53° |
| 频段 | Ku 12 GHz，250 MHz |
| 最小仰角 | 20° |
| 决策间隔 | 10s |
| 卫星容量 | 10 信道/星 |
| UE | 15 个，北京地区 ±3° |
| 仿真时长 | 2h (720 步) |

## 2. Baseline 复现结果

### 2.1 B4 Random（下界）

| 指标 | 均值 ± 标准差 (5 seeds) |
|------|----------------------|
| 吞吐量 | 36,105 Mbps |
| 阻塞率 | 0.02% |
| 切换次数 | 8,435 |

**分析**：随机策略通过均匀分散 UE 到不同卫星，几乎不产生阻塞。但切换频繁（每步 ~1.2 次/UE）且不优化信道质量。

### 2.2 B1 HHS（传统启发式 SOTA，L08）

| 指标 | 均值 ± 标准差 (5 seeds) |
|------|----------------------|
| 吞吐量 | 20,911 Mbps |
| 阻塞率 | **37.4%** |
| 切换次数 | 877 |

**分析**：
- 切换次数仅 877（比 Random 的 8,435 减少 90%）→ 稳定性奖励有效
- 但阻塞率 37.4% 极高 → **根因**：HHS 原为单 UE 算法（L08），多 UE 独立决策导致聚集效应
- 稳定性奖励（logistic ψ）和切换惩罚（P_ho=0.03）使 UE 粘滞在同一卫星，超过容量限制
- **这是 HHS 在多 UE 场景的结构性局限，也是 DRL 的核心改进空间**

### 2.3 B2 Dueling DDQN（DRL baseline 1，L02 修正）

| 指标 | 验证结果 (5 episodes) |
|------|---------------------|
| Episode reward | 3,345 - 4,241 |
| Transitions/episode | 10,800 (15 UE × 720 步) |
| Training loss | 0.31 → 0.19（下降趋势）|
| CUDA | 正常使用 |

**验证状态**：架构正确（Dueling Q = V + A - mean(A)），训练收敛趋势正常。完整 300 episode 训练待 Execute 阶段执行。

### 2.4 B3 PPO（DRL baseline 2，L01/L10 参考）

| 指标 | 验证结果 (3 episodes) |
|------|---------------------|
| Value loss | 10.5 → 0.5（快速下降）|
| Entropy | ~1.4（持续探索）|
| Eval step reward | 0.199 |
| Eval blocking rate | 45.5% |

**验证状态**：Actor-Critic 共享层正确，PPO-clip 损失正常。仅 3 episode 未充分收敛，45.5% 阻塞率是训练不足的表现。完整训练估计 ~10h。

## 3. 与论文对比

### 复现定义（按框架规定）

> "复现"在本项目中定义为：在自己的仿真环境中实现论文的算法架构和核心设计，验证相对趋势。

| Baseline | 论文方法 | 本项目修正 | 验证方式 |
|----------|---------|-----------|---------|
| B1 HHS | L08 Algorithm 1 | 星座从 Starlink 1584 降至 396 | 结构验证：三级决策+效用函数正确 |
| B2 DDQN | L02 Dueling DDQN | **rate 归一化到 [0,1]**（原论文未归一化，F5 根因） | 趋势验证：loss 下降，reward 合理 |
| B3 PPO | L01/L10 PPO | 无修正 | 趋势验证：value loss 下降 |
| B4 Random | — | — | 下界确认 |

### 不直接对比绝对数值的理由

1. 星座规模不同（396 vs L02 的 298/L07 的 1584）
2. 信道模型不同（本项目简化 vs L08 完整 ITU-R 模型）
3. UE 数量/分布不同（15 vs L02 的 10-30）
4. 奖励函数修正（L02 的 rate 未归一化，本项目已修正）

## 4. 关键代码路径

```
v2/projects/leo-ntn-handover-drl/
├── config.py                  # 全局参数
├── simulator/
│   ├── orbit.py               # M1: 轨道力学（向量化预计算）
│   ├── channel.py             # M2: 信道模型（FSPL+大气+阴影）
│   ├── reward.py              # M5: 归一化奖励计算
│   └── environment.py         # M4+Env: Gymnasium 环境
├── baselines/
│   ├── hhs.py                 # B1: HHS（L08 Algorithm 1）
│   ├── b2_dueling_ddqn.py     # B2: Dueling DDQN（L02 修正）
│   ├── b3_ppo.py              # B3: PPO（L01/L10 参考）
│   └── random_policy.py       # B4: Random
├── verify/
│   ├── test_simulator.py      # 验证测试（8 项全部 PASS）
│   └── reward_check.py        # MDP checkpoint（全部 PASS）
└── results/
    ├── b1_hhs_results.json
    ├── b2_ddqn_results.json
    ├── b3_ppo_results.json
    └── b4_random_results.json
```

## 5. 发现与后续建议

1. **HHS 高阻塞率是结构性问题**：多 UE 独立决策导致聚集。DRL 的核心价值是学习负载均衡。
2. **奖励函数 v2 有效性已验证**：稳态 R=61%/L=31%，无单项>95%，策略区分度 120%。
3. **完整训练待 Execute 阶段**：B2/B3 仅验证了架构正确性，300 episode 训练约需 10h。
4. **观测空间优化**：当前 obs_dim=1585（396×4+1），可考虑 top-K 候选压缩到 41 维加速训练。

## 6. 竞争格局与代码生态（Batch Search 2026-05-09）

> 三组并行检索：前向引用扫描（6 篇核心论文）、相似论文+后向引用、GNN 锚点+代码搜索。
> 详细结果：`search-archive/batch_baseline_search_results_1_2.md` + `search-archive/agent3_gnn_anchor_results.md`

### 6.1 竞品代码

**结论：LEO 切换+DRL 领域零开源代码论文。** 核心 6 篇前向引用中 0 篇附带代码。

最接近的可复用仓库（非直接竞品）：

| 仓库 | Stars | 场景 | 可借鉴内容 |
|------|-------|------|-----------|
| Shadab442/dqn-leo-handover-python | 57 | DQN LEO 切换 | Gym 环境可直接复用 |
| XuyangCaoUCSD/LeoEM | 133 | LEO 网络仿真器 | 实时仿真 testbed |
| SatCom-TELMA/MA-DRL_Routing_Simulator | 143 | MA-DRL 卫星路由 | 多 Agent DRL 架构参考 |
| kit-cel/HandoverOptimDRL | 16 | PPO 地面切换 | 训练 pipeline 参考 |

### 6.2 GNN 方法锚点

支撑 size generalization 叙事的有代码仓库：

| 仓库 | 论文 | GNN 类型 | Size Generalization | 可用性 |
|------|------|---------|---------------------|--------|
| LSJ-BUAA/GNN-Scheduling-Precoding | IEEE TWC 2026 | 二部图 GNN | 有专门 `generalization/` 测试代码 | **高** |
| GraphmindDartmouth/DISGEN | ICML 2024 | 模型无关框架 | 核心贡献 | **高** |
| UNIC-Lab/GNN-Routing | arXiv 2510 | GAT+LSTM+RL | 验证大规模拓扑泛化 | **中高** |

无代码但高度相关的理论工作：Shen 2020 (c=460, GNN 无线泛化奠基)、Wu 2024 (c=13, GNN 规模泛化机制分析)、Zhou 2025 CL-GNN (小网训大网部署)。

### 6.3 补充高相关论文（batch search 新发现）

| 论文 | 来源 | 核心方法 | 与本研究关系 |
|------|------|---------|-------------|
| Li et al. JSAC 2026 (LLM+DRL 多层 LEO) | 前向引用 L018 | LLM 协调器+DRL | JSAC 顶刊，方法前沿 |
| Tong et al. IEEE TAES 2025 (A2C 切换) | find-similar | A2C 五因素切换，-58% 切换 | 航空顶刊，对比基线候选 |
| Lee et al. 2025 (GNN 分布式 LEO 切换) | GNN 搜索 | GNN 切换+负载均衡 | **高重叠但无 DRL** |
| Eydian et al. 2025 (二部图+KM) | GNN 搜索 | 二部图匹配切换 | **二部图建模思路** |
| Zhu & Pan 2026 (Graph+RL 波束管理) | GNN 搜索 | Graph+RL 6G 卫星 | 最新，方向一致 |
| Sun et al. Comm Letters 2024 (多目标 RL 切换) | find-similar | MODQN 多目标 | 多目标切换直接相关 |
| Jang et al. WiOpt 2025 (CNN-LSTM 预测) | find-similar | CNN-LSTM+MADDQN | 预测+多 Agent 新颖 |
| DS-PPO arXiv:2603.16470 | find-similar | 双阶段 PPO | MARL 多卫星方法论 |

### 6.4 引用格局

核心论文前向引用分布：

| 论文 | 前向引用 | 说明 |
|------|---------|------|
| L018 EMODRL (JSAC 2024) | 47 | **唯一有效引用中枢**，多数来自同组扩展 |
| L024 IMPALA DHO | 1 | — |
| L004/L029/L016/L022 | 0 | 太新或未被索引 |

BGNN (Kim 2022, IEEE TWC) 前向引用 50 篇（via S2），其中 3 篇有代码（ICGNN TMC 2025、Recursive GNNs TMLCN 2024、GNN Beamforming TWC 2024），均为波束赋形方向。
