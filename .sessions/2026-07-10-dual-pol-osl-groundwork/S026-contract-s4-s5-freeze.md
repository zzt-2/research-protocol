# [S026] Contract S4-S5 + 冻结执行（端到端推演 + 压力测试 + 冻结）

> 2026-07-15 | Contract 阶段 S4-S5-Step6 | 状态：完成
> 2026-07-15 续接 S025

## 目标

续 S025（Contract S0-S3 完成）。本轮完成 stages/contract.md S4（端到端推演）+ S5（压力测试 + 反模式 + 实验完备性）+ Step 6（冻结），完成 Q-CMA-FADE Contract 冻结。

## 记录

### Session Start + Handoff 验证

续 S025 同一专题同一对话序列（上轮 S025 完成后本轮续接）。topic-index 不变量 8 条确认，无 active topic 冲突。S### 文件数 25（>=15 inflation），补 scope record 确认非范围漂移（25 S = GW Step1-4a + Contract 全流程自然深度）。

### S4 端到端推演（data-flow.md）

**适配说明**：contract.md 的 8 步推演模板是为网络路由设计（星座配置→节点坐标→…→评估）。Q-CMA-FADE 是 DSP 信号处理非网络，8 步适配为 DSP 信号流。

**关键代码核查**（确保推演忠实于真实实现非脑补）：
- `ml_long_seq_failure.py:154` gen_channel：双偏振信号生成（Jones 矩阵 SOP 旋转 + GG 包络 + AWGN）
  - rX = sqrt(h)·(cos(θ)·sX + sin(θ)·sY) + n_X
  - rY = sqrt(h)·(-sin(θ)·sX + cos(θ)·sY) + n_Y
  - θ = sop_rate·arange(N)（SOP 累积旋转）
- `_cma.py:100` CMAEqualizer2x2.equalize：块级 2×2 蝶形（block_size=64，4 复 FIR，Godard 1980 含 z 因子）
- `_ml_equalizer.py:104` ButterflyCNNEqualizer2x2：8 实值 1D-CNN 蝶形（Qin 2025 L275/283，MSE 监督）
- `prompt012_longseq_audit.py:98` evaluate_outputs：双口径 BER（fixed-label + PI 2!×4×4 消歧）+ abs_corr swap 诊断

**8 步推演**（每步标代码来源）：
1. 信道配置 → 双偏振接收信号（gen_channel）
2. 均衡器输入对齐（F1 数据同源，三方共用 gen_channel）
3. 均衡器处理（CMA / ML / oracle 三方并行）
4. 均衡器输出 → 判决 → 比特
5. BER 计算（双口径 D018 强制）
6. 评估指标（M1-M4）
7. 统计聚合 + 假设检验（Wilcoxon exact p）
8. 跨参数泛化（N/f_G/SOP_RATE/SNR/调制 变化 → 适用域边界）

**FR-13 均衡能力表达力审计**（适配 DSP：非 RL 动作空间→均衡能力）：
| Baseline | ML 能做什么 | ML ≥ Baseline？ |
|---|---|---|
| B1 standard-CMA | 固定权重 vs 在线块级梯度更新 | 可比（ML<CMA 跟踪但 ML>CMA swap 免疫，窄域 D023）|
| B2 CMMA | 不限星座阶数 | ≥（16QAM）/ 等价（QPSK）|
| B3 oracle | 有限训练数据 vs 完美 CSI | <（预期，FR-25 不做判据）|

门控通过：B1 可比窄域已在 Contract H2 适用边界 + E5 标注。B3 < oracle 是预期差距（FR-25）。

**FR-16 架构信息增量审计**：
- 训练前 ML（identity 通道）zX=rX；训练后 zX=wxx∗rX+wxy∗rY（均衡后）
- 信息增量真实存在（BER 从 0.5 降到 0.005-0.01）
- 但增量来源是监督学习数据非架构创新（D022 ML-original vs ML-aligned 无差，初始化不是性能来源）
- 架构是 Qin 迁移（F4 诚实标注"场景迁移 + 分析增量"）

门控通过：信息增量真实，属性诚实标注。

### S5 压力测试 + 反模式 + 实验完备性（experiment_completeness_checklist.md）

**5 问压力测试**（无致命风险）：
1. 结构性优势：分析层（第一性原理量化 sat.1553 空白，非 DL 替代）+ 方法层（固定权重免疫恒模多解，窄域 9× 优势）
2. 边际结果：窄域内量级优势（9×）非边际；跨域反转已诚实标 limitation
3. 信号独立性：H1/H2 success/failure 独立定义，failure 非 success 否定
4. Baseline 共识性：B1 standard-CMA 是领域最强共识（Godard 1980 + sat.1553 + 全精读论文）；B3 oracle 不做 Go 判据（FR-25）
5. 综合判定：无致命风险，方法层窄域+无架构创新是已知 limitation（导师接受窄域）

**反模式 4 项**（基于 data-flow.md 非凭空想象）：
1. 信息泄露 ✅ pass（F5 训练/测试无重叠，三方同信道 F1，oracle 不做处理组 FR-25）
2. 仿真过于简化 ✅ pass（GG AR(1)+SOP+AWGN 含目标方法擅长特征，SOP_RATE 仿真值债务已标）
3. 确定性信道+DL 强行优越 ⚠️ 注意（已诚实标注 D023 N=2M 反转，非致命，导师接受条件性优势）
4. 跨实验数据不一致 ✅ pass（全共用 gen_channel，ber_vs_snr_scan.py:8,273-276 确认三方同信道）

**实验完备性 Tier 1 六项**（全 pass）：
- T1-1 多 seed ✅（E3 30 seeds，其他 5 seeds，E8 待 Execute 补）
- T1-2 Baseline 来源 ✅（全标来源）
- T1-3 公平调参 ✅（F3 μ=1e-3 安全区非调优，F4 诚实声明监督 vs 盲）
- T1-4 逐模块消融 ✅（适配 DSP 单组件：D022 ML-original vs ML-aligned 初始化消融是组件级验证）
- T1-5 信道模型溯源 ✅（全标来源，真实性中等）
- T1-6 scope 控制 ✅（C3 bounded 窄域，C1/C2/C4/C5 universal/bounded 区分）

### Step 6 冻结

**FR-17 用户确认**：主指标从 PI-BER 改 fixed-label BER（领域首选 75%），PI-BER 降辅指标。用户确认"接受调整，冻结 Contract"。

**冻结操作**：
1. contract.md 头部 status: draft → frozen，frozen_date: 2026-07-15
2. contract.md 末尾"待下轮"段改为"冻结状态"（含已知债务 5 项 + Execute 下一步）
3. H011 handoff 写（交 Execute 阶段）
4. topic-index 更新（last_updated + 当前位置 + scope record 25 S + 进展线索 S026）

## 决策引用

- 无新建 D###（本轮是 Contract 流程执行 S4/S5/冻结，无架构/方向决策变更）
- **引用现有**：D014（SOP 真因）/ D022（ML 29/30，H2 + FR-16 初始化消融）/ D023（窄域收窄，FR-13 B1 可比标注）/ D018（双口径）/ D029（改动1 Kill，方法层定型弱）/ D008（公平性债务 F4）/ D012（seed-bias 债务）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。Contract S4/S5/冻结是 contract.md 定义的强制流程（FR-22），是原始目标"找到真问题+合法贡献形态"的形态定型最后一步。

## 后续

**Contract 冻结完成，专题使命（GW + Contract）基本达成**。

**下一步 = Execute 阶段**（H011 已写）：
1. 读 `stages/execute.md` 全文守 FR-22
2. E1-E7 实验在 GW Step 4a 维度 D MVE 已基本跑完，Execute 主要是补 E8（统计严谨性 ≥30 seeds）+ T2-5（复杂度报告）+ 整理论文数据 + 写论文
3. 论文按导师约束（不能只分析得加方法 / 特定条件优异就行 / 会议不给修改机会 / BER 10⁻⁵ 底线 / 没后路）

**未决项**：
- Execute 是否续本专题还是开新专题（25 S 已较多，但 Contract 冻结后 Execute 性质变了）——交用户决定
- E8 补 seed 的具体优先级（哪些关键点必须加到 30 seeds）——Execute 规划时定
