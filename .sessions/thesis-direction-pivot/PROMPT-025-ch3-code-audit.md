# PROMPT-025: Ch3 仿真代码审计

> 专题: thesis-direction-pivot | 目标: 验证 Ch3 仿真代码的正确性和可靠性
> Python: `~/.venvs/torch/bin/python`
> 工作目录: `projects/thesis-figures/simulation/`

## 背景

Ch3（大气湍流信道下的 BER 分析）的推导和仿真在 S002 单次对话中完成，**当时 thesis-lessons.md 尚不存在**。后续 Ch4 工作中发现了大量代码问题（信号模型错误、评估方法不一致、共享信道问题等），但 Ch3 代码从未对照这些教训做过审计。

**必须验证的核心问题**：Ch3 的结果是否可信？有没有被 Ch4 同源 bug 污染？

## 待审计文件

| 文件 | 用途 | 大小 |
|------|------|------|
| `sim_ch3_ber_closed_form.py` | BER 闭合解验证（6 组实验） | 19K |
| `sim_ch3_strengthening.py` | 设计准则 + 估计误差鲁棒性 | 15.4K |
| `sim_ch3_ber_bounds.py` | BER 界（上界/下界对比） | 11.5K |

## 审计清单（逐项检查）

### A. 信号模型（最高优先级）

对照 TL-01，检查每个文件：

1. **SNR 关系**：代码中 γ=γ̄·h（相干检测）还是 γ=γ̄·h²（IM/DD）？
   - 搜索关键词：`gamma_bar`、`snr`、`h*gamma`、`h**2`
   - 如果出现 `h**2` 或 `h*h*gamma`，标记为 **FATAL**

2. **信号幅度**：接收信号中 h 的幂次是 0.5（√h）还是 1（h）？
   - 搜索关键词：`np.sqrt(h)`、`h**0.5`、`*h*`
   - 如果信号是 `tx*h` 而非 `tx*np.sqrt(h)`，标记为 **FATAL**

3. **噪声功率**：噪声方差是 1 还是与 h 相关？
   - 正确：E[|n|²]=1（独立于 h）
   - 错误：噪声功率随 h 变化

### B. 参数一致性

4. **Gamma-Gamma 参数**：α/β 值是否与 thesis-status.md 一致？
   - weak: α=4.0, β=3.0
   - moderate: α=2.5, β=1.8
   - strong: α=1.5, β=0.8

5. **系统参数**：
   - R_SYM = 2.5e9 (Gsps)
   - T_S = 400e-12 (s)
   - BLOCK = 100
   - γ̄ 默认 20dB（100 线性）

6. **BER 公式**：
   - QPSK BER = Q(√(2γ)) 还是其他形式？
   - 如果用 erf/erfc，检查系数是否正确

### C. 评估方法

7. **BER 计算**：Ch3 用的是什么方法？
   - 如果是解析公式（不涉及仿真 BER），此项 PASS
   - 如果有蒙特卡洛仿真，检查是 ber_count 还是 resolve_qpsk

8. **GG 分布采样**：如何生成 h？
   - 正确：从 GG(α,β) 分布采样归一化辐照度
   - 检查：`np.random.gamma` 的参数形状是否正确（shape=α, scale=1/β 或等价形式）

### D. 数值验证

9. **特殊值检查**：
   - AWGN 无湍流（h≡1）时，BER 是否回归标准 QPSK AWGN 公式？
   - 如果代码支持 h≡1 测试，验证数值
   - 如果不支持，检查公式在 h→1 极限下是否正确

10. **BER floor**：
    - 代码是否计算 BER floor？
    - floor 值是否与理论预期一致？

### E. 代码质量

11. **随机种子**：是否固定种子？结果可复现？
12. **Meijer-G 实现**：如果用 `scipy.special.meijerg` 或其他实现，检查参数是否正确
13. **数值稳定性**：极端参数下（强湍流+低 SNR）是否出现 NaN/Inf？

## 审计方法

1. 先通读每个 .py 文件，逐项对照上述清单
2. 对每个检查项给出明确结论：✅ PASS / ⚠️ WARNING / ❌ FAIL / 💀 FATAL
3. FATAL 项意味着 Ch3 结果不可信，需要重写代码
4. FAIL 项需要说明影响范围和严重程度

## 不要做什么

- **不要修改代码**——本对话只审计，不修复
- **不要跑完整仿真**——验证关键公式和参数即可，可以跑小的测试片段确认行为
- **不要开发新方法或新实验**
- **不要读 Ch4 相关代码**——专注于 Ch3

## 输出格式

```
# Ch3 代码审计报告

## 审计摘要
- 审计文件数：X
- FATAL：X 项
- FAIL：X 项
- WARNING：X 项
- PASS：X 项

## sim_ch3_ber_closed_form.py

### A. 信号模型
| # | 检查项 | 结论 | 证据（代码行号） |
|---|--------|------|-----------------|

### B. 参数一致性
...

## sim_ch3_strengthening.py
...

## 整体结论
[Ch3 结果是否可信？需要修复什么？]
```

## 必读参考

审计前先读：
1. `thesis-lessons.md` — TL-01（信号模型）到 TL-19
2. `projects/thesis-figures/simulation/SIMULATION_SPEC.md` §1-2（信号模型和参数定义，作为正确参考）

## 完成后

写 handoff 到 `.sessions/thesis-direction-pivot/H025-ch3-audit-result.md`，包含：
- 审计结论（PASS/FAIL 汇总）
- 需要修复的问题清单（如有）
- 对 Ch3 写作的影响评估
