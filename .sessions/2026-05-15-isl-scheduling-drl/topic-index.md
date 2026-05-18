# 专题：ISL 调度 DRL（阶段 1）

> 创建：2026-05-15 | 状态：**closed** | 描述：ILP 标签失败后转向 route-aware labeling，续接至 05-16 目录

## 进展线索

### Handoff 文件（H001–H021）

- **H001-initial** — Round 1。GW Step 2-3 进行中。合并 4 组检索（108 篇去重），下载 23 篇成功 8 篇，11 篇 IEEE 付费墙失败。4 篇关键竞品需手动获取（Wang TCOM/Pi ICC/Guo TWC/Wang TWC 联邦RL）。

- **H002-step2** — Round 2。GW Step 3 完成。8 篇精读完成，`literature_notes.md` 已写入。综合分析：确定性优化为主（5/8），DRL 仅 SatFlow 1 篇，创新空白为细粒度在线 ISL 建立/拆除/切换 DRL 决策。Wang TCOM MADRL 为最直接竞品。

- **H003-step3** — Round 3。GW Step 3.5 完成。4 篇竞品补充精读（L09-L12）+ 定向补充检索（7 组 + 引用链分析）。共 12 精读 + 3 浅读。确认 GNN+DRL 细粒度 ISL 调度为文献空白：所有 DRL 论文均为粗粒度动作空间 + FC 网络，无逐链路三态决策。

- **H004-step35** — Round 4。GW Step 4a 完成。撰写 `feasibility_report.md`（A/B/D 三维度），执行 MVE（GNN vs FC 图匹配），结果 Pass：GNN 97.3% vs FC 79.5%（+22.4%），GNN 仅 11 epoch 收敛。Go 决策待用户确认。

- **H005-step4a** — Round 5。GW Step 4b + Step 5 完成。Baseline 选定：B1=+Grid/Fixed（领域共识），B2=Wang TCOM MADRL（最直接 DRL 竞品）。仿真条件(C)+资源风险(E)评估完成，全维度 Go。

- **H006-step4a-2** — Round 6。GW Step 6 sim 完成。仿真器设计规格产出：8 模块、28 参数溯源（0 ASSUMPTION）、奖励函数 r = 1.0*R_tput - 0.3*C_switch - 0.2*C_setup、跨规模泛化设计。B2 路由从 LP 改为 Dijkstra（D006）。待用户确认。

- **H007-step6-sim** — Round 7。GW Step 6 sim 用户已确认。仿真器核心参数锁定：Starlink 1584 (24x66), LISL 3000km, Gaussian beam + Rayleigh jitter, GHS-POP 100 GS, Setup delay Uniform(2,30)s, 决策间隔 10s。准备 Step 7 impl。

- **H008-step7-impl** — Round 8。GW Step 7 Part A 完成。仿真器 8 模块实现（orbit/visibility/channel/traffic/environment/router/reward/metrics/config），验证全部通过（解析/统计/退化/自相关/MDP 试运行）。已知限制：Keplerian 两体（非 SGP4），Python 循环 O(n^2) 需优化。

- **H009-baseline-b1** — Round 9。GW Step 7 Part B — B1 完成。B1 (+Grid/Fixed) ~100 行实现并验证通过。B1 Fixed M1=0.048, 显著优于 Random(+1231%)。低吞吐量（~5%）为 24x8=192 星规模问题，非算法缺陷。B2 Wang MADRL 待实现。

- **H010-baseline-b2** — Round 10。GW Step 7 Part B — B1+B2 均完成。B2 (Wang MADRL) ~330 行实现，训练验证通过（24x20, 50ep）。B2 未优于 B1（M1 0.118 vs 0.173），原因：少 1 条固定链路、候选不足、训练不充分。GW Step 7 框架门槛全部满足，可进入 Contract。

- **H011-gw-complete** — Round 11。**GW 全部完成**。性能优化完成（visibility 6.4x, traffic 63x, B1 episode 2.1x）。全规模 24x66=1584 B1 M1=28.2%。待决策：28% 吞吐量是否足够、核心方法能否超过 B1、是否需优化路由。

- **H012-lct-constraint** — Round 12。**问题重设定（D012）**。原问题 B1 无限 ISL（4752 边）M1=28.19%，DRL 无优化空间。多路径路由仅 +5.3%。引入 N_LCT 终端约束：N_LCT=3 为甜点（gap=11.1%），参数鲁棒性扫描 9/9 配置 gap>5%。推荐 Contract 默认参数：N_LCT=3, demand=10Gbps, N_GS=100, Z_MAX=3000km。

- **H013-contract-frozen** — Round 13。**Contract 冻结**。方案：GAT-PPO 拓扑感知 ISL 调度（逐边评分 + top-3），目标 M1>=25%。假设、Baseline（B1/B2）、奖励函数、消融计划（A1-A4）、实验列表（E01-E06）全部锁定。给出 Execute Step 0 实现任务清单（GATv2ActorCritic + PPO 训练循环）。

- **H014-execute-step01** — Round 14。Execute Step 0-1 完成。**PPO 未能超越先验**。5 轮 Quick Test（v1-v5）：最佳 v5 先验 M1=0.0774，PPO 微调后仅 +0.0006。根因：先验策略本质为"保持活跃ISL+选最短边"≈ 简化版 B1，剩余优化空间<2%。KL 爆炸（小std）和随机探索失败（大std）为 PPO 适配问题。全规模 65664 候选边有内存/显存风险。

- **H015-execute-deadend** — Round 15。**死胡同确认**。REINFORCE 验证同样失败（M1 -3.7%），随机 swap 诊断改善 <=0.0015（噪声级）。三方法（PPO/REINFORCE/噪声探索）全败，共同根因为先验已捕获物理结构。与 beam-hopping 失败模式匹配。未验证：全规模 24x66 候选更多、流量感知定向 swap。需要方向决策。

### Handoff 文件 — 新对话提示词（H016–H021）

- **H016-gw-scheduling** — GW Step 2-3 起步。定义 ISL 调度 + DRL 方向，提供 4 组检索资产（101 篇），指令执行合并/下载/精读/定向检索。

- **H017-step35** — GW Step 3.5 补充检索 + 竞品精读。4 篇竞品已下载就绪（Wang TCOM/Guo TWC/Wang TWC 联邦RL/Pi ICC），指令补充精读 + 定向检索弥补盲区。

- **H018-step4a** — GW Step 4a Go/No-Go。预加载 5 篇关键文献证据，指令撰写 feasibility_report.md（结构优势/新颖性/MVE）。

- **H019-step7-impl** — GW Step 7 impl Part A。仿真器搭建详细指令：8 模块实现顺序、验证清单、MDP 试运行。预加载全部仿真参数。

- **H020-contract-to-execute** — Contract → Execute 连续执行。从 GW 完成+问题重设定状态恢复，指令一路执行到 Execute 完成。核心参数已验证。

- **H021-execute-deadend** — Execute 死胡同方向决策。读 decision_log D017-D022 + code-quality.md 失败模式 + beam-hopping 先例，分析根因（方法/建模/方向），给出明确建议。

## 已确认结论

1. **GNN+DRL 细粒度 ISL 调度为文献空白**：15 篇文献确认，所有 DRL ISL 论文均为粗粒度动作空间 + FC 网络，无逐链路建立/拆除/切换三态决策。

2. **N_LCT=3 约束创造了 DRL 优化空间**：原问题 B1 无限 ISL M1=28.19% 无优化空间。N_LCT=3 使固定贪心 M1=17.09%，与无限 ISL gap=11.1%，9/9 参数配置鲁棒。

3. **MVE 验证 GNN > FC**：图匹配调度任务中 GATv2 达 97.3% vs FC 79.5%（+22.4%），GNN 11 epoch 收敛。

4. **PPO/REINFORCE 均无法超越先验**：先验策略（active_bias + distance_bias）本质上实现了"保持活跃ISL+选最短边"，已捕获物理结构，剩余优化空间 <2%。连续分数 + Normal 分布 + top-K 映射导致 KL 爆炸或退化为随机。

5. **与 beam-hopping 失败模式匹配**：两项目均为"先验捕获物理结构，DRL 无法额外学习"的模式，属 code-quality.md 记录的失败模式 A2。

6. **仿真器基础设施完整**：8 模块仿真器（orbit/visibility/channel/traffic/environment/router/reward/metrics）、B1/B2 baseline、验证套件全部实现并验证通过。

## 未决项

1. **方向决策**：ISL 调度方向是否归档。三个选项——继续 ISL（改方法/改动作空间/全规模验证）、归档换子问题、换方向。

2. **全规模 24x66=1584 未充分验证**：候选边从 5K 增至 65K，每星候选更多，优化空间可能不同。但 env.step=0.6s + 65664 边的内存/显存风险未解决。

3. **流量感知定向 swap 未测试**：不是随机换边，而是根据 obs 的 supply/demand 选择方向。理论上可能突破先验瓶颈，但未实现。

4. **学位论文方向约束**：导师要求 1 方向 -> 3 个关联问题。当前方向 A（LEO 星座优化）中路由已完成、切换已完成，ISL 如归档需找替代子问题。

## 当前位置

项目已完成 GW Step 1-7 + Contract 冻结 + Execute Step 0-1（Quick Test），在 Execute 阶段确认死胡同（PPO/REINFORCE/噪声探索三方法均无法超越先验），需要方向决策——归档 ISL 调度或尝试替代方案。最终决策在 `.session/2026-05-16-isl-scheduling-drl/` 续接。
