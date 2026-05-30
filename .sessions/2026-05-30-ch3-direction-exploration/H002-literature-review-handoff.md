# Handoff: Ch3 方向 G 文献全面审查

> 来源: S002 | 交接目标: 多角度文献审查，确保无盲点
> 文件名: H002-literature-review-handoff.md

## 已完成边界

1. **方向 G 核心推导完成**：BER 闭合解 + BER floor + 中断概率 + 设计准则 + 鲁棒性证明
2. **数值验证通过**：MC 仿真 median 0.6%，GG CDF 交叉验证 < 10⁻⁸，SNR 惩罚独立性 9 组确认
3. **加强项完成**：设计准则表 + 估计误差鲁棒性（原计划3项，砍掉GG vs EGG）

## 不要做什么

- **不要重新推导**——公式已验证，不是数学错误的风险点
- **不要重复搜索已有文献**——S001 已完成 6 方向检索，R003 补充了 B/C
- **不要改方向**——G 已确认，文献审查是为了确认不踩坑，不是换方向
- **不要用主对话做 web search**——必须走子 agent

## 必读

1. `.sessions/2026-05-30-ch3-direction-exploration/topic-index.md` — 专题全貌
2. `.sessions/2026-05-30-ch3-direction-exploration/S002-ber-closed-form-derivation.md` — 完整推导+验证

## 核心问题：需要文献审查确认什么

### 审查角度 1：是否有"已经做过相同工作"的论文被我们遗漏？

**搜索策略**：
- 关键词组合："Gamma-Gamma" + "Gaussian phase error" + "QPSK" + "BER"
- 关键词组合："coherent FSO" + "phase noise" + "closed-form" + "BER"
- 关键词组合："atmospheric turbulence" + "carrier phase error" + "outage probability"
- 检查 Petkovic 2023 和 Hu 2025 的引用链（谁引用了他们）
- S001 已确认 0 篇精确匹配，但需复查 2025-2026 新发表

**如果找到**：评估重叠程度，确定我们的差异化点

### 审查角度 2：SNR 模型 γ = γ̄·h 是否有争议？

**搜索策略**：
- "coherent detection" + "free space optical" + "SNR model" + "irradiance"
- 检查是否有人用 γ ∝ h²（直接检测模型）分析相干检测
- 检查外差 vs 零差的 SNR 表达式差异

**如果发现有争议**：需要在论文中加一段讨论，引用多篇文献说明为什么用 γ ∝ h

### 审查角度 3：Fourier 级数法的适用范围和局限性

**搜索策略**：
- Petkovic 2023 之后是否有改进方法？
- 是否有文献指出 Fourier 级数法在某些参数下收敛困难？
- 与其他 BER 计算方法（Meijer-G 直接积分、moment generating function）的精度对比

### 审查角度 4：BER floor 公式 Q(π/(4σ_φ)) 是否有文献先例？

**搜索策略**：
- "BER floor" + "phase error" + "QPSK" + "closed-form"
- 检查微波通信领域是否有类似结果（QPSK + phase error floor 是经典问题）
- 如果微波领域已有此公式，我们需要强调 FSO 场景的特殊性（GG fading 使 floor 更难达到）

### 审查角度 5：DPLL B_L∝h 与 γ∝h 抵消这一结论是否新颖？

**搜索策略**：
- "adaptive PLL" + "fading channel" + "phase error variance" + "channel independent"
- "carrier synchronization" + "coherent detection" + "robustness" + "channel estimation error"
- 如果已有人发表过这个观察，我们的贡献要重新定位

### 审查角度 6：中断概率框架是否完整？

**搜索策略**：
- "outage probability" + "Gamma-Gamma" + "QPSK" + "coherent"
- 检查是否有人做过 GG 中断概率 + 相位误差的联合分析
- 与 Trinh 2023（GG 中断概率无相位误差）的关系

## 接口变更

新增文件：
- `projects/thesis-figures/simulation/sim_ch3_ber_closed_form.py`（6 实验）
- `projects/thesis-figures/simulation/sim_ch3_strengthening.py`（2 实验）
- `projects/thesis-figures/simulation/fig_ch3_*.png`（8 张图）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 线性化 DPLL 模型局限 | 完整性 | 论文中注明 | 审稿人要求更精确模型 |
| γ=γ̄·h 适用范围 | 准确性 | 论文中注明 | 审查发现争议 |
| 精确 BER 公式低 SNR max 85% 误差 | 精度 | 标注为非工作区域 | 审稿人要求解释 |

## 验证阈值

| 验证项 | PASS 标准 | 当前状态 |
|--------|----------|---------|
| MC vs 理论 BER | median < 5% | ✓ 0.6% |
| GG CDF Meijer-G | rel_err < 10⁻⁶ | ✓ < 10⁻⁸ |
| BER floor | MC vs Q(π/4σ) < 5% @ σ≥8° | ✓ |
| SNR 惩罚独立性 | spread = 0 | ✓ |
| 估计误差鲁棒性 | ratio < 1.01 @ NMSE=-5dB | ✓ 1.000 |

## 下一轮

1. **多角度文献审查**（子 agent 并行）：
   - Agent A: 角度 1+4（重复工作检查 + BER floor 先例）
   - Agent B: 角度 2+5（SNR 模型 + B_L∝h 抵消新颖性）
   - Agent C: 角度 3+6（Fourier 法局限性 + 中断概率框架）
2. 汇总审查结果，评估风险等级
3. 如有问题，调整 Ch3 叙事定位
4. 更新论文框架和开题报告
