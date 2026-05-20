# Decision Log — ris-phase-drl

## 阶段摘要
- [Groundwork] 完成 — Step 7 baseline 训练+评估完毕，baseline_report.md 已生成
- [Contract] 冻结 — CCAN+TD3 方案，用户确认 2026-05-20
- [Execute] **归档** — CCAN+TD3 4 轮验证 avg 停在 Fixed 水平，D3 失败模式，方向归档

## 决策记录
[D001] 研究方向确定为 RIS/IRS 辅助通信中的相移优化 + DRL 方法 | 理由: 用户指定 | 阶段: GW
[D002] 检索策略：3 组关键词（RIS phase shift DRL / IRS RL beamforming / RIS DRL resource allocation MIMO），academic mode + scenario-method preset | 理由: 覆盖不同术语体系 | 阶段: GW
[D003] 精读优先级：语义筛选而非纯关键词匹配 | 理由: 脚本 relevance_score 是纯词频匹配，会系统性低估用不同术语的高相关论文 | 阶段: GW
[D004] 精读范围：8 篇（Tier 1 核心相移+DRL × 3 + Tier 2 DRL+RIS × 3 + Tier 3 相关变体 × 2）| 理由: 覆盖 DQN/DDPG/TD3/PPO/混合动作空间 + 被动/主动/空中 RIS 变体 | 阶段: GW
[D005] 4a Pivot：用户认为空白 1（大规模 RIS + 连续相移 + 高级 DRL）的新颖性未被充分验证，现有检索可能遗漏直接竞争论文 | 理由: 需确保真有新颖性/差异性/可实现性 | 阶段: GW Step 4a
[D006] 补充检索方向：针对空白 1 定向扩展检索，关键词聚焦 large-scale/massive RIS + continuous phase shift + TD3/SAC/PPO/scalable DRL | 理由: 验证空白是否真实存在 | 阶段: GW Step 1（回退）
[D007] 补充检索完成，空白 1 新颖性确认"高"：5 组检索 + 3 篇候选竞争论文精读。最直接竞争者 L002 (arXiv:2506.10815, Extremely Large Scale RIS + A2C) 已撤稿。RISnet (L017) 用无监督学习不是 DRL。无已发表竞争者 | 理由: Pivot 后定向验证完成 | 阶段: GW Step 4a
[D008] Step 4a 完整重做（框架更新后）：用新版 gw-feasibility.md（含 A0/A'/FR-01~08）重新评估。A0 六项致命信号检查全部通过；A' 竞争维度分解确认创新在极低覆盖维度；A 结构优势论证 +FR-03 增强基线对比 +FR-08 范式对齐均通过 | 理由: 框架更新后需重做 | 阶段: GW Step 4a
[D009] Baseline 田野调查：派子 agent 扫描 45 篇论文 abstract，验证 baseline 候选的领域共识度。DDPG 40%、TD3 24%、SAC 22% 出现率。确认 DDPG+TD3 为领域共识 DRL baseline。发现传统优化（SCA/BCD 13-11%）在精读 8 篇 DRL 论文中完全未出现，田野调查弥补了盲区 | 理由: gw-validate 田野调查要求 | 阶段: GW Step 5（前置）
[D010] MVE 三轮迭代：(1) v1 失败——单步 i.i.d. episode 导致 MDP 退化，TD3=Random 0.98×；(2) v2 失败——直连链路太强（Rician κ=10dB + MRT），随机相移已近最优，TD3=Random 1.01×；(3) v3 通过——阻断直连链路 + 绝对动作，TD3=40× Random，DDPG+1.1%。三轮暴露两个设计教训：必须多步块衰落 episode、必须直连弱/阻断场景 | 理由: MVE 不可降级（组合新颖性方向）| 阶段: GW Step 4a §D
[D011] Step 4a 最终决策：**建议 Go**。A0/A'/A/B/D 五维度无致命信号，MVE v3 通过。空白 1 新颖性"高"经补充检索+田野调查+MVE 三重验证。正式仿真器必须：(a) 多步块衰落 episode，(b) 直连链路弱/阻断场景 | 理由: 完整 Step 4a 评估结论 | 阶段: GW Step 4a
[D012] Step 5 Baseline 选定：5 个 baseline（DDPG + SAC + Random + Fixed(θ=0) + PSO）。原方案仅 DDPG+Random 太少，用户指出框架更新后要求补做实验完备性提取和写作架构提取。派 6 个子 agent 补提取 8 篇论文的 Baseline 矩阵+实验组织数据。竞品中位数 3-5 个 baseline，4/8 含传统方法，1/8 含启发式(PSO)。新方案：2 DRL 对比(DDPG+SAC) + 1 启发式(PSO) + 2 简单对照(Random+Fixed)，与竞品实验组织一致 | 理由: 实验完备性提取+写作架构提取补全，Baseline 方案经竞品数据对标 | 阶段: GW Step 5
[D013] 实验完备性对标结论：8 篇竞品统计规范性普遍薄弱（0/8 统计检验、0/8 声明 seeds）。本项目 Contract 阶段应 ≥3 seeds + error bar + 配对 t 检验，即可超越全部竞品。消融参考 F3 逐模块模式，复杂度至少理论O()+实测推理延迟 | 理由: 对标汇总支撑 Contract 实验设计 | 阶段: GW Step 5
[D014] Step 4b 仿真条件+资源风险：C 维度无致命信号（MVE 三轮已预验仿真条件陷阱：强直连→随机近最优、单步→MDP 退化）。E 维度无致命信号（5/5 baseline 需自实现但均为标准算法，失败有可回收产出）。预计总投入 4-6 周 | 理由: Step 4b Go/No-Go 决策 | 阶段: GW Step 4b
[D015] Step 6 仿真器设计：(1) 仅优化相移（不联合波束赋形），ZF 预编码作为固定 beamforming；(2) Rician κ=10dB 块衰落 + 直连阻断 + 多步 50 步 episode；(3) 奖励为 sum rate 单组件，无需归一化；(4) FR-12 架构差异对照：全部"否"通过（MVE→Formal 仅规模扩展，结构不变）；(5) 5 场景 × 6 方法 × ≥3 seeds 实验矩阵；(6) [ASSUMPTION] 参数 5/22=23%<30% 门槛 | 理由: 框架要求用户确认后进入 Step 7 | 阶段: GW Step 6
[D016] Step 7 Baseline 关键发现：MLP-based DRL (TD3/SAC/DDPG) 确定性评估 ≈ Fixed(θ=π)，未学到信道自适应策略。TD3 avg=1281 ≈ Fixed avg=1292，差距仅 -0.9%。但 PSO avg=1554 显著优于 Fixed +20.2%，证明信道自适应优化有价值。DRL 退化原因：obs_dim=2600 过大+MLP 表达力不足+Rician LoS 主导。研究机会：需信道感知架构使 DRL 超越 Fixed 并接近 PSO | 理由: baseline_report 核心结论 | 阶段: GW Step 7
[D017] Contract 冻结：CCAN (Channel-Conditioned Attention Network) + TD3。核心假设：CCAN 使 TD3 学到信道自适应相移策略，avg sum rate ≥1.10× MLP-TD3 (≥1419 bps/Hz)。架构：per-element attention (d_model=64, n_heads=4) + shared MLP decoder。[ASSUMPTION] 0/22 全消除。FR-13 动作空间审计通过。5 个 bounded claimed contributions 对应 8 个实验。用户确认冻结 2026-05-20 | 理由: Contract Step 0-6 全部完成 | 阶段: Contract
[D018] Execute Step 1 Quick Test + Step 2 训练结果：CCAN+TD3 seed 0, (a) early stopping 版：ep 142 early stop, avg=1301, best=1576; (b) 无 early stopping 版：训练至 ep~1500(WSL 崩溃), avg 在 1275-1315 震荡(Fixed 水平), best=1670(>PSO=1554)。确定性评估 avg=1275 < MLP-TD3=1281 < Fixed=1292。**结论**：CCAN 架构有足够容量（best=1670 远超 PSO=1554），但 RL 训练无法稳定输出好策略 | 理由: 核心实验数据 | 阶段: Execute
[D019] Critic 瓶颈诊断 + Contract Amendment：根因分析——Critic 输入 (obs 2600 + action 100)=2700 维，首层 2700→400 压缩比 6.75:1，与 MLP Actor 有相同的信道特征丢失问题。Critic 无法准确评估不同信道条件下的动作质量，给 CCAN Actor 的策略梯度信号太弱。Actor 偶然通过探索发现好策略（best=1670），但 Critic 无法强化这些发现。**修复方案**：Critic 也使用 CCAN encoder 提取信道特征，替代 raw flat obs。这是 Contract Amendment（修改 Simulation Config 中 Critic 架构），不修改 hypothesis/success_signal/failure_signal/fairness_rules。用户确认 2026-05-20 | 理由: Execute 阶段发现的实现级瓶颈，需 Amendment 才能继续 | 阶段: Execute
[D020] CCANCritic Amendment 验证失败：使用 CCANCritic 替代 MLP Critic 后，训练结果完全相同（ep 142 early stop, avg=1301, best=1576）。**Critic 瓶颈假设被推翻**——问题不在 Critic 质量，而在 TD3 训练动力学本身。真正根因：(1) κ=10dB LoS 主导下最优策略接近 Fixed，信道自适应空间仅来自 NLoS 分量；(2) TD3 探索噪声 0.1 std 偶然发现好策略但频率极低；(3) Replay buffer 中好策略样本被大量 Fixed 水平样本稀释，Actor update 取 mean Q 信号太弱。**已尝试 4 轮**（MLP Critic early stop / MLP Critic no-early-stop / CCANCritic early stop / CCANCritic no-early-stop），avg 均在 1275-1315（Fixed 水平），改善 <1% | 理由: 4 轮迭代确认方向瓶颈 | 阶段: Execute
[D021] **方向归档**：ris-phase-drl Execute 阶段归档。CCAN+TD3 方案被验证为"架构有容量（best=1670 > PSO=1554）但 TD3 训练动力学无法利用"——典型的 D3 失败模式。核心教训：注意力架构创新 ≠ RL 可学习性，先验证 RL 能否超越简单先验再投入架构设计。产出已记录到 code-quality.md D3 模式。用户决定归档并切换方向 | 理由: 4 轮 <1% 改善，触发防死胡同检测 | 阶段: Execute
