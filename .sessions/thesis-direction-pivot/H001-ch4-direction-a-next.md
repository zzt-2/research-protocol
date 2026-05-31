# Handoff: Ch4方向A推进 — 解析推导+Doppler模型+MVE

> 来源: S009 | 交接目标: 完成方向A的MVE前置3项闭环 + 执行MVE判定
> 文件名: H001-ch4-direction-a-next.md

## 已完成边界

1. **S009 Ch4方向侦察完成**：4方向（A/B/C/D）并行搜索，推荐方向A
2. **框架A0审计完成**：A0-1至A0-6逐项检查，无致命信号
3. **P1 Paillier精读完成**："湍流可忽略"仅限完整AO场景，无AO=真空白（通量惩罚-23dB vs -4.5dB）
4. **P2 负面证据搜索完成**：11次搜索80条结果，无致命负面证据
5. **方向A修正定位**："湍流强度自适应的LEO星地载波同步——从GG模型参数到最优FOE/CPR参数的解析设计与验证"

## 不要做什么

- 不要重新搜索方向A/B/C/D的文献对比（S009已完成）
- 不要重新读Paillier 2020（P1已完成，结论明确）
- 不要讨论Ch4是否应该换方向（已决定方向A）
- 不要把"联合"理解为物理耦合——Doppler和湍流是独立损伤源，研究的是叠加场景下的参数优化
- 不要在MVE前引入DL/DRL元素——纯传统信号处理（FFT+DPLL+VV）

## 必读

按优先级排列：

1. `.sessions/thesis-direction-pivot/S009-ch4-direction-scout.md` — 完整方向侦察+框架审计+P1+P2结论（**必读全部**）
2. `.sessions/thesis-direction-pivot/S008-a0-and-gap-analysis.md` — A0检查v5（Ch2/Ch3部分仍有效，Ch4部分已被S009替代）
3. `.sessions/thesis-direction-pivot/S007-ch4-ch5-deep-review.md` — Ch4/Ch5精读结果（参数溯源表）
4. `.sessions/thesis-direction-pivot/topic-index.md` — 专题进展总览

## 接口变更

无代码改动。R010仿真原型在 `projects/thesis-figures/simulation/sim_prototype.py`，需在其基础上扩展。

## 失败数据附录

- 方向B（FOE+CPR自适应参数）：A0未通过，增益<5%概率70%，2017年理论框架8年无人follow
- 方向C（位同步）：DLR组已系统覆盖
- 方向D（联合同步）：复杂度远超硕士范围
- Paillier 2020负面证据：已排除（仅限完整AO场景）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 解析公式未推导 | 必须有理论深度 | 未开始 | MVE前完成 |
| Doppler模型未实现 | R010原型缺此模块 | 未开始 | MVE前完成 |
| Ch3/Ch4边界未锁定 | 需明确正交分工 | 待导师确认 | 与导师沟通时确认 |

## 验证阈值

| 验证项 | PASS标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| MVE性能改善 | ≥2种联合场景改善>0.5dB | 框架审计建议 | N/A |
| 解析公式 | α,β→N_opt闭合解或近似解 | 避免工程调参降格 | N/A |
| Paillier回应 | 无AO场景影响量化 | A0-5闭环 | P1已部分完成 |

## 接收方验证

- [ ] 已读取S009的框架审计+P1+P2结论段落
- [ ] 已验证Paillier 2020论文位置（papers/arxiv/1911.11851/content.md）
- [ ] 已确认R010仿真原型位置（projects/thesis-figures/simulation/sim_prototype.py）
- [ ] 已检查topic-index中Ch4方向A的最新判定

## 下一轮

### 任务1：解析公式推导（理论）
推导GG湍流参数(α,β) → SNR分布 → FOE/CPR估计方差 → 最优FFT窗口长度N、DPLL带宽B_L、VV窗口M的解析关系。

参考起点：
- AWGN下VV窗口M最优值已知：M_opt ∝ (δν·T_s)^{-1/3}（Agrawal光纤通信教材）
- 扩展到非恒定SNR（GG分布）是新贡献
- 如果推导不出闭合解，给半解析经验公式+理论下界分析也够

### 任务2：Doppler时变模型实现（代码）
在R010原型（`projects/thesis-figures/simulation/sim_prototype.py`）基础上增加：
- 时变频偏模型：仰角→径向速度→f_D(t)，线性chirp或完整轨道力学
- FFT-based FOE模块：argmax(|FFT(r^4)|)/4，可调窗口长度
- 二阶DPLL模块
- 参数扫描框架

参数锚点（来自S007）：
- Doppler: ±8GHz总量，残余~100MHz，变化率150MHz/s（Zhao 2025）
- FFT: L=1024, 分辨率2.44kHz（Zhao 2025）
- DPLL: ω_n=8Mrad/s, ξ=√2/2（Zhao 2025）
- GG: 三档（Amirabadi 2019 α,β参数）
- 调制: SP-QPSK

### 任务3：MVE执行
对比固定参数（Zhao配置）vs 自适应参数，在6种联合场景（3湍流×2仰角/变化率）下：
- pass：≥2种场景改善>0.5dB → 方向A Go
- fail：所有场景<0.5dB → 降级为"首次系统研究"方法论贡献

### 任务4：与导师沟通准备
整理以下材料供用户带去见导师：
- 方向A修正定位的一句话描述
- 文献空白确认（0-1篇三联合）
- Paillier负面证据回应（无AO=真空白）
- MVE结果（如果任务3完成）
- 3项需确认决策：Ch4方向切换、是否需要DL元素、Ch5 FPGA衔接
