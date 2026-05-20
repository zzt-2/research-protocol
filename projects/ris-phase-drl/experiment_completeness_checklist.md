# 实验完备性自检清单 — ris-phase-drl

> Contract Step 5 产出

## 压力测试（4 问）

### 1. 结构性优势

CCAN vs MLP 的结构性优势：
- **问题结构**：H_eff = H2^H @ diag(e^{jθ}) @ H1 是双线性结构，θ_i 的最优值取决于 H1 的第 i 行和 H2 的第 i 行的交互
- **MLP 失效根因**：展平 obs（2600维）→ 首层压缩到 400 维，丢失了逐元素的行对齐关系
- **CCAN 优势**：per-element attention 保留了 (N, 2M+2K+2) 结构，每个元素 attend 其他元素捕获空间关联
- **非通用"DL 更好"**：是架构归纳偏置匹配问题结构，不是简单用 DL 替代传统方法

**结论**：结构性优势明确 → 低风险

### 2. 边际结果

若 CCAN 仅提升 5-10%：
- MLP 失效分析（avg ≈ Fixed）本身是有价值的负结果贡献
- κ-sweep (E4) 展示 CCAN 在不同信道复杂度下的表现梯度
- 失败信号已显式覆盖此情况
- 仍有发表价值：识别 MLP 失效模式 + 验证信道感知架构的方向性价值

**结论**：边际结果仍有贡献 → 低风险

### 3. 信号独立性

| 信号 | 定义 | 独立性 |
|------|------|--------|
| Success | CCAN avg ≥ 1.10 × MLP-TD3 avg (κ=10dB) | 主场景下的定量阈值 |
| Failure 1 | CCAN avg < 1.05 × MLP-TD3 avg | 改进不足（非 success 否定） |
| Failure 2 | 训练不收敛（loss 发散/NaN） | 算法稳定性（与改进幅度无关） |
| Failure 3 | CCAN 在 κ≤5dB 仍 ≈ Fixed | 架构优势非信道条件依赖 |

三个 failure 信号各自独立，不是 success 的简单否定。→ ✓

### 4. Baseline 共识性

| Baseline | 田野调查出现率 | 精读论文覆盖 | 复现状态 |
|----------|-------------|-------------|---------|
| TD3 | 24% (6/45) | F3 (AB-TD3) | 已复现 |
| SAC | 22% | 领域共识 | 已复现 |
| DDPG | 40% | L02 | 已复现 |
| PSO | 1/8 竞品 | — | 已复现 |

DRL baseline (TD3+SAC+DDPG) 合计覆盖 86% 田野调查，领域共识充分。→ ✓

## 反模式审查

| # | 反模式 | 检查内容 | 状态 |
|---|--------|---------|------|
| 1 | 信息泄露 | 所有方法使用相同 obs (2600d)；CCAN 通过内部 attention 处理，不引入额外信息；消融 A3 验证改进非来自信息差异 | ✅ pass |
| 2 | 仿真过于简化 | κ=10dB LoS 主导风险（B3 pattern）；通过 E4 (κ∈{3,5,10}) 对冲；sum rate 跨 episode 方差 std≈100 (vs avg≈1290)，足够产生差异化 | ✅ pass |
| 3 | 确定性信道 + DL 强行优越 | 块衰落：每 episode 新信道，DRL 需泛化到未见信道实现；CCAN 优势来自建模信道关联而非记忆；PSO 上界证明优化空间存在 | ✅ pass |
| 4 | 跨实验数据不一致 | 所有实验共用同一 simulator + config + seeds；评估使用独立种子 (seed_base=10000+) | ✅ pass |

## 实验完备性自检

### Tier 1: 必做（门控条件）

| # | 维度 | 要求 | 状态 | 说明 |
|---|------|------|------|------|
| T1-1 | 多 seed + error bar | ≥3 seeds, mean±std | ✅ pass | Contract 规定 seed 0,1,2；报告 avg±std |
| T1-2 | Baseline 来源声明 | 每个标注实现来源 | ✅ pass | B1-B6 全部标注来源论文+复现状态+交叉验证 |
| T1-3 | Baseline 公平调参 | 声明调参预算/方式 | ✅ pass | Fairness rules: 相同超参(lr,γ,τ,batch,buffer)；参数量≤2×约束 |
| T1-4 | 逐模块消融 | 逐一移除/替换 | ✅ pass | A1(w/o attention), A2(w/o sharing), A3(w/o encoder) |
| T1-5 | 信道模型溯源 | 参数引用文献 | ✅ pass | α₂→F4, PL₀→L02, σ²→计算, 其余设计选择附文献交叉引用 |
| T1-6 | 声称 scope 控制 | bounded 限定词 | ✅ pass | C1-C5 全部 bounded，无 universal 声称 |

### Tier 2: 应做

| # | 维度 | 要求 | 状态 | 说明 |
|---|------|------|------|------|
| T2-1 | 统计显著性检验 | 配对 t, p<0.05 | ✅ pass | Contract 声称-证据映射表中已要求 |
| T2-2 | Alt-explanation 排除 | 排除参数量影响 | ✅ pass | A3 消融：同参数量无 encoder ≈ baseline |
| T2-3 | 声称-证据审计 | claim→experiment 映射 | ✅ pass | Contract 含 5 行映射表 |
| T2-4 | 跨场景验证 | ≥2 种配置 | ✅ pass | E3(N变化), E4(κ变化), E5(K变化) |
| T2-5 | 复杂度报告 | 推理延迟或理论 O() | ✅ pass | M4: 推理延迟(ms/step) |

### Tier 3: 加分

| # | 维度 | 状态 | 说明 |
|---|------|------|------|
| T3-1 | Red-teaming | ✅ pass | κ=10dB LoS 主导作为已知限制讨论 |
| T3-2 | 真实数据验证 | ☐ NA | 仿真研究，无实测数据 |
| T3-3 | 因果分析 | ☐ NA | 非因果研究 |
| T3-4 | 最优解对比 | ✅ pass | PSO 作为近最优上界 |
| T3-5 | 极端条件测试 | ✅ pass | κ=3dB（强 NLoS）+ N=200（大规模）|

**门控结果**：Tier 1 全部 pass → 可以进入 Step 6 冻结。
