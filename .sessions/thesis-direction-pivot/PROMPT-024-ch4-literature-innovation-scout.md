# PROMPT-024: Ch4 创新点文献驱动全自动搜索

> 用途：新对话中全自动执行文献精读，寻找 Ch4 创新点
> 专题：thesis-direction-pivot
> 模式：全自动，不中断用户，每批完成后更新日志
> 来源：S021 讨论结论

---

## 一、背景：为什么需要这次搜索

### 论文概况

硕士论文"星地激光通信信号处理关键技术研究"，6 章结构：

```
Ch1 绪论
Ch2 系统模型与信道估计（建模+LS/MMSE/KF估计+链路预算）
Ch3 湍流与相位误差联合链路性能分析（BER闭合解+中断概率+设计准则）← 已稳定
Ch4 低轨星地载波同步算法（频偏估计+载波相位恢复+DPLL）← 需要重新找创新点
Ch5 FPGA设计与实现
Ch6 总结
```

**Ch3 状态：已稳定。** BER 闭合级数解、BER floor、中断概率、分湍流强度设计准则、估计误差鲁棒性——全部推导完成、12-agent 验证通过（21/21 PASS）、MC 验证匹配。创新点（中断概率+相位误差联合框架）被 H002 评估为"明确新颖"。

**Ch4 状态：核心方案失败。** 详见下一节。

### Ch4 三公式自适应方案失败始末

#### 原始方案（R016 推导）

推导了三个湍流自适应公式：
- FOE 自适应窗口：$N_\text{opt} = 80 / (\bar\gamma \cdot h^2)$（修正后指数）
- VV 自适应窗口：$M_\text{opt} = (\bar\gamma \cdot h)^{-1/5}$
- DPLL 环路带宽：$B_{L,opt} = B_0 \cdot h$

声称"三种不同 h 依赖形态覆盖弱到强湍流"。

#### 信号模型修正（S019 D011）

12-agent 交叉验证发现全文 SNR 约定不一致。相干检测物理上：

$$r[k] = \sqrt{h[k]} \cdot s[k] \cdot e^{j\phi[k]} + n[k], \quad \gamma = \bar\gamma \cdot h$$

（不是 IM/DD 的 $\gamma = \bar\gamma \cdot h^2$）

全部 8 个仿真文件、4 个公式文件已修正。修正后公式指数降低（h⁻⁴→h⁻²），论证链变弱：
- E[1/h] 仅强湍流发散（β=0.8<1），中湍流（β=1.8>1）收敛
- DPLL B_L∝h 抵消论证变成设计选择，非 Wiener 最优

#### 仿真验证失败（S018 PROMPT-009）

修复仿真后跑全三公式自适应，结果全面更差：

| 方案 | 弱湍流 | 中湍流 | 强湍流 |
|------|--------|--------|--------|
| 去 MMSE + 三公式自适应 | 更差 | 更差 | 更差 |
| 恢复 MMSE + 三公式自适应 | 更差 | 更差 | 更差 |
| MMSE + DPLL-only 自适应 | +4.8 dB | +0.8 dB | +0.25 dB |

**根因分析**：三个公式是对瞬时 h 推导的逐符号最优参数。但实际操作中只有帧级 h_med。当 h_med≈0.3-0.8（典型值）时，FOE 和 VV 公式给出比固定参数更短的窗口 → 性能更差。只有 DPLL 碰巧方向正确。

**结论**："三公式自适应框架"的创新声称被事实否定。2/3 公式自适应后反而更差，强湍流增益仅 0.25 dB，远不够支撑 L2 创新声称（需 ≥1 dB）。

### 死胡同列表（不要重复尝试）

| 方案 | 否决原因 | 来源 |
|------|---------|------|
| 三公式全自适应（N+M+B_L 同时调） | 仿真验证全面更差 | S018 |
| 去掉 MMSE 预补偿 | 载波恢复算法需要恒幅信号 | S018 |
| 方向 E（信道跟踪预测） | τ_rx/T_coh < 10⁻⁶，预测≡估计 | S020 |
| 方向 B（AMC 自适应调制） | 与 Ch4 循环依赖 | S020 |
| 方向 C（Doppler 预补偿） | 创新空间窄+中文文献少 | S020 |
| 新方向6（多孔径合并） | 创新增量薄+与 Ch4 重叠 | S019 |
| 功率预补偿独立成章 | S013 WEAK PASS | S019 |
| "首次"/"提出"措辞 | H002 审查后明确禁用 | H002 |
| γ∝h²（IM/DD）信号模型 | 相干检测物理错误 | D011 |

---

## 二、任务目标

**在"湍流信道下的 LEO 星地载波同步"这个大范围内，通过大量文献精读，找到 2-3 个可行的 Ch4 创新点。**

要求：
- 每个创新点必须有明确的文献缺口支撑（"这个问题没人解决过"或"这个方法没被应用到这个场景"）
- 每个创新点必须能在现有仿真框架（Python + QPSK + GG 湍流 + 块衰落）内验证
- 创新级别至少 L1（增量创新），理想 L2（方法级创新）
- 不改变论文 6 章框架和 Ch3 已有成果

---

## 三、搜索范围

按 Ch4 技术栈拆 5 个子方向，每个子方向独立搜索：

### 子方向 A：频偏估计（FOE）

- FFT-based FOE 在衰落信道下的改进
- 湍流感知的 FOE 窗口选择策略
- 残余频偏补偿的替代方案
- 关键词建议：frequency offset estimation FSO, OFE fading channel, FFT-based carrier recovery turbulent

### 子方向 B：载波相位恢复（CPR）

- Viterbi-Viterbi / BPS 在快变衰落信道下的改进
- 自适应窗口/加权 CPR
- 判决引导 vs 盲 CPR 在 FSO 下的对比
- 关键词建议：carrier phase recovery FSO, Viterbi-Viterbi adaptive, BPS QPSK fading

### 子方向 C：DPLL / 锁相环

- 湍流下环路参数优化（带宽/阶数/阻尼系数）
- 自适应 DPLL 设计
- 非线性 DPLL / 深衰落下的锁相策略
- 关键词建议：DPLL optical communication, phase-locked loop fading, adaptive PLL satellite

### 子方向 D：联合/端到端架构

- FOE + CPR + DPLL 非级联联合优化
- Turbo 接收机（信道估计与载波同步迭代）
- 深度学习预测最优参数
- 关键词建议：joint carrier recovery, turbo synchronization, ML carrier recovery optical

### 子方向 E：低复杂度 / 工程约束

- FPGA 友好的载波同步算法
- 定点化设计对同步性能的影响
- 硬件资源约束下的参数选择
- 关键词建议：FPGA carrier synchronization, fixed-point DPLL, low complexity phase recovery

---

## 四、方法论

### 搜索策略

每个子方向的 agent 执行以下步骤：

1. **本地库筛选**：从 `material-chapter-literature.md`（165 篇文献清单）中找出与子方向相关的论文
2. **精读本地论文**：对筛选出的论文读 `content.md`（路径在 `papers/` 下），重点关注：
   - 引言中指出的未解决问题
   - 实验中暴露的性能瓶颈
   - 结论中的"future work"
   - 方法中采用的简化假设（可以放松的）
3. **补充检索**：用 `tools/search` 搜索更多相关论文（命令：`cd /mnt/d/code/study/research-protocol && bash tools/search --query "关键词" --max 20`）
4. **Web 搜索**（仅子 agent 内）：用 WebSearch 搜索近期文献，每个子 agent 最多 2 次 WebSearch
5. **Gap 分析**：汇总发现，按以下格式输出

### 每个 agent 输出格式

```markdown
## 子方向 X：[名称]

### 已读论文（列出实际读了哪些）
- [citekey] [标题] — 一句话核心发现

### 发现的缺口/机会
1. **[缺口描述]**
   - 来源：哪篇论文指出的 / 哪两篇论文之间的空白
   - 可行性：能在现有仿真框架内验证吗？
   - 创新级别预估：L1 / L1→L2 / L2
   - 风险：主要不确定因素

### 无缺口（如果该方向确实 barren）
- 理由：为什么判断该方向没有好的创新机会
```

### 批次安排

**核心原则：每个子方向至少 3 个 agent，分多角度深挖。** 不要一个方向只派 1 个 agent——覆盖面不够容易遗漏关键信息。

每个子方向的 3 个 agent 分工：

| Agent 角色 | 搜索角度 | 关键词风格 |
|-----------|---------|-----------|
| Agent α（理论深度） | 本地库精读 + 补充检索，找理论基础和方法论缺口 | 学术精确词（"Viterbi-Viterbi fourth-power phase estimator turbulent channel"） |
| Agent β（跨领域迁移） | Web 搜索，找相邻领域（光纤/RF/卫星微波）的同类问题解法 | 跨领域词（"adaptive carrier recovery fading" "phase tracking deep fading"） |
| Agent γ（工程/最新） | Web 搜索近 2 年文献，找最新进展和工程实践 | 时间限定词（"2024 2025 carrier synchronization LEO satellite"） |

**执行顺序（按子方向逐个深入，每次 3 agent 并行）：**

**Phase 1：子方向 A（频偏估计）** — 3 agent 并行
- A-α：本地库 FOE 相关论文精读 + tools/search 补充
- A-β：Web 搜索 RF/光纤领域的自适应 FOE 方法
- A-γ：Web 搜索 2024-2025 年 LEO/FSO 载波同步最新论文

**Phase 2：子方向 B（载波相位恢复）** — 3 agent 并行
- B-α：本地库 VV/BPS/CPR 论文精读 + tools/search 补充
- B-β：Web 搜索自适应窗口 CPR、加权 CPR 方法
- B-γ：Web 搜索 2024-2025 年 CPR 最新进展

**Phase 3：子方向 C（DPLL / 锁相环）** — 3 agent 并行
- C-α：本地库 DPLL 相关论文精读 + tools/search 补充
- C-β：Web 搜索深衰落/快变信道下的 PLL 设计
- C-γ：Web 搜索 2024-2025 年自适应 PLL 最新进展

**Phase 4：子方向 D（联合/端到端架构）** — 3 agent 并行
- D-α：本地库联合同步论文精读 + tools/search 补充
- D-β：Web 搜索 Turbo 同步 / 联合估计与检测
- D-γ：Web 搜索 ML/DL 辅助载波同步最新论文

**Phase 5：子方向 E（低复杂度 / 工程约束）** — 3 agent 并行
- E-α：本地库 FPGA/定点化论文精读 + tools/search 补充
- E-β：Web 搜索硬件友好载波同步算法
- E-γ：Web 搜索 2024-2025 年 FSO DSP 实现最新论文

**总计：15 个 agent，5 个 Phase，每 Phase 3 个并行。**

**每个 Phase 完成后必须做的事**：
1. 汇总该方向 3 路 agent 发现
2. 立即写日志，不要等下一个 Phase。日志文件：
   - Phase A 完成 → `.sessions/thesis-direction-pivot/S023-ch4-scout-direction-a.md`
   - Phase B 完成 → `.sessions/thesis-direction-pivot/S024-ch4-scout-direction-b.md`
   - Phase C 完成 → `.sessions/thesis-direction-pivot/S025-ch4-scout-direction-c.md`
   - Phase D 完成 → `.sessions/thesis-direction-pivot/S026-ch4-scout-direction-d.md`
   - Phase E 完成 → `.sessions/thesis-direction-pivot/S027-ch4-scout-direction-e.md`
3. 日志格式见下方"日志协议"
4. 如果某方向发现非常有希望，可以在下一 Phase 开始前加派 1-2 个补充 agent 深挖

**全部 Phase 完成后必须做的事**：
1. 汇总 A-E 五个方向的全部发现
2. 写综合报告到 `.sessions/thesis-direction-pivot/S028-ch4-innovation-scout-final.md`
3. 综合报告必须包含"候选创新点排序表"和"建议"

**扩展协议**（如果 A-E 全部 barren）：
- 扩展搜索范围到：
  - F：信道编码与载波同步联合设计
  - G：导频图案优化对同步性能的影响
  - H：多载波/OFDM FSO 下的载波同步
  - I：星间激光通信（ISL）载波同步的启示
  - J：在阅读过程中发现的任何新角度
- 每个扩展方向也派 3 个 agent（α/β/γ），继续精读
- 扩展结果追加到单独日志文件

---

## 五、评估标准

### 创新级别定义

| 级别 | 含义 | 判据 |
|------|------|------|
| L2 | 方法级创新 | 新算法/架构，文献中无先例，仿真增益 ≥1 dB |
| L1→L2 | 边界 | 已有方法的显著改进或跨领域迁移，增益 0.5-1 dB |
| L1 | 增量创新 | 已有方法在新场景的应用，增益 >0 dB |
| L0 | 无创新 | 完全重复已有工作 |

### 好的创新点特征

1. **有明确的文献缺口**：能说"论文 X 指出了这个问题但没解决"或"方法 Y 在场景 Z 下性能恶化，没人提出改进"
2. **可仿真验证**：在现有框架（QPSK + GG 湍流 + 块衰落 + Python）内 1-2 天能出结果
3. **与 Ch3 有衔接**：Ch3 导出 σ_φ 设计准则 → Ch4 的算法应该响应这些准则
4. **不依赖 Ch4 已失败的三公式**：可以部分利用（如 DPLL-only），但不能以"三公式"为核心叙事

### 不好的创新点特征（应排除）

- 纯调参（"优化了参数 X"没有理论支撑）
- 与已失败方案本质相同（换个壳的"自适应窗口"）
- 需要大规模代码重构才能验证的
- 与 Ch3 循环依赖的
- 物理上不可行的

---

## 六、日志协议

### 为什么需要日志

此对话完全自动运行，可能跨越多批次 agent。上下文可能在任意时刻压缩（compaction）。**每批完成后必须写日志**，确保压缩后不丢失关键信息。

### 日志文件

每个 Phase 独立写日志（防止压缩丢失）：
- **Phase A 日志**：`.sessions/thesis-direction-pivot/S023-ch4-scout-direction-a.md`
- **Phase B 日志**：`.sessions/thesis-direction-pivot/S024-ch4-scout-direction-b.md`
- **Phase C 日志**：`.sessions/thesis-direction-pivot/S025-ch4-scout-direction-c.md`
- **Phase D 日志**：`.sessions/thesis-direction-pivot/S026-ch4-scout-direction-d.md`
- **Phase E 日志**：`.sessions/thesis-direction-pivot/S027-ch4-scout-direction-e.md`
- **最终报告**：`.sessions/thesis-direction-pivot/S028-ch4-innovation-scout-final.md`

### 每 Phase 日志格式

```markdown
# [S023] Ch4 创新点搜索 — 子方向 A（频偏估计）

> 2026-05-31 | 文献搜索 | 完成

## Phase A 汇总

### Agent A-α（理论深度）
[精读了哪些论文，发现了什么缺口]

### Agent A-β（跨领域迁移）
[从其他领域找到了什么可迁移的方法]

### Agent A-γ（工程/最新）
[最新文献中有什么新趋势或新方法]

### 交叉发现
[三个角度共同指向的机会]

### 候选创新点
1. [创新点描述] — 来源: [哪些论文] — 级别: L? — 风险: [高/中/低]
2. ...

### Barren 判断（如果没有好机会）
- 理由：为什么判断该方向没有好的创新机会
```

### 最终报告格式

```markdown
# [S028] Ch4 创新点搜索 — 最终报告

> 2026-05-31 | 文献搜索 | 完成

## 执行摘要

搜索了 5 个子方向，派出 15 个 agent，精读了 ~75-120 篇论文，发现 Z 个候选创新点。

## 候选创新点排序表

| 排名 | 创新点 | 子方向 | 级别 | 可行性 | 风险 | 支撑论文 |
|------|--------|--------|------|--------|------|---------|
| 1 | ... | ... | L? | 高/中/低 | ... | [citekeys] |
| 2 | ... | ... | ... | ... | ... | ... |

## 每个候选创新点详细分析

### 候选 1：[标题]
- **问题**：从文献中识别的缺口
- **方案**：拟采用的方法
- **创新性论证**：与最接近的已有工作对比
- **验证计划**：需要什么仿真
- **与 Ch3 的衔接**：如何承接 σ_φ 设计准则
- **风险**：主要不确定因素

### Barren 方向（如果某子方向确实没有好机会）
[列出 barren 的子方向和判断理由]

## 建议

[给用户的建议：哪些候选值得深挖，哪些可以快速排除]
```

---

## 七、约束（必须遵守）

### 绝对禁止

1. **禁止主对话使用 WebSearch / webReader**——只能在子 agent 中使用。违反会导致上下文爆炸。
2. **禁止使用"首次""提出"等地位声称**——H002 审查后明确禁用。
3. **禁止修改论文框架**（6 章结构不变）。
4. **禁止修改 Ch3 已有推导和结论**。
5. **禁止在子 agent 中运行仿真代码**——本轮只做文献搜索，不跑代码。
6. **禁止扩展到 Ch4 载波同步以外的范围**——除非 A-E 全部 barren 才按扩展协议执行。
7. **禁止向用户提问或等待确认**——全自动运行，所有决策自行判断。

### 必须遵守

1. **每批完成后写日志**——防止压缩丢失。
2. **并发上限 3 个 agent**——不超过。
3. **子 agent 单次执行不超过 15 分钟**——超时则截断并记录已获得的部分结果。
4. **每个子 agent 读 5-8 篇论文**——不要贪多，保证每篇读透。
5. **用 `tools/search` 做检索**——命令：`cd /mnt/d/code/study/research-protocol && bash tools/search --query "关键词" --max 20`。
6. **读论文优先读 content.md**——路径格式：`papers/arxiv/{id}/content.md` 或 `papers/doi/{doi_path}/content.md` 或 `papers/manual/{slug}/content.md`。如果 content.md 太长，优先读摘要、引言最后两段（问题陈述）、结论（future work）。
7. **使用 `~/.venvs/torch/bin/python`**——如果需要运行任何 Python 代码（但本轮不应该需要）。

---

## 八、必读文件

新对话开始时按以下顺序读取：

1. **本文件**（PROMPT-024）——完整上下文
2. **`毕设/写作材料/thesis-status.md`**——论文全局状态
3. **`毕设/写作材料/material-chapter-literature.md`**——165 篇文献清单（从这里筛选相关论文）
4. **`.sessions/thesis-direction-pivot/S018-ch4-sim-fix-log.md`**——仿真失败详细记录
5. **`.sessions/thesis-direction-pivot/S019-ch2-derivations-and-verification.md`**——信号模型修正详情（重点看 D011 和 12-agent 全局定论部分）

按需读取（遇到具体问题时查阅）：
- `毕设/写作材料/formulas-ch3ch4-sync.md`——Ch4 公式（含 D011 修正后的版本）
- `毕设/写作材料/formulas-ch3-link-performance.md`——Ch3 公式（已验证通过）
- `毕设/写作材料/formulas-ch2-system-model.md`——Ch2 系统模型（含 h 定义声明）
- `.sessions/thesis-sim-exploration/topic-index.md`——仿真探索表（20 个实验假设）

---

## 九、关键参数和约定

以下是论文中已锁定的技术参数，不要修改：

| 参数 | 值 | 说明 |
|------|-----|------|
| h 定义 | 归一化辐照度，GG 分布 | D011 决策 |
| 信号模型 | r = √h · s · e^{jφ} + n | 相干检测 |
| SNR | γ = γ̄ · h（线性） | 不是 γ̄ · h² |
| 噪声 | 恒定方差 σ² = 1/(2γ̄) | LO 散粒噪声主导 |
| 调制 | QPSK | s⁴ = -1 |
| 符号率 | 2.5 Gsps | |
| 激光线宽 | 10 kHz | |
| 残余频偏 | 1 MHz | Doppler 预补偿后 |
| 湍流参数（弱） | α=4.0, β=3.0 | Trinh 2017 |
| 湍流参数（中） | α=2.5, β=1.8 | Trinh 2017 |
| 湍流参数（强） | α=1.5, β=0.8 | Trinh 2017 |
| 块大小 | 100 符号/块 | 相干时间内 |

---

## 十、执行计划（主线程 Checklist）

```
[ ] 1. 读取本文件 + thesis-status.md + material-chapter-literature.md
[ ] 2. 从 material-chapter-literature.md 筛选 5 个子方向各自相关的论文（citekey 列表）
[ ] 3. Phase A：启动 3 个 agent（A-α/A-β/A-γ）搜索频偏估计方向
[ ] 4. 等待 Phase A 完成，汇总结果，写 S023 日志
[ ] 5. Phase B：启动 3 个 agent（B-α/B-β/B-γ）搜索载波相位恢复方向
[ ] 6. 等待 Phase B 完成，汇总结果，写 S024 日志
[ ] 7. Phase C：启动 3 个 agent（C-α/C-β/C-γ）搜索 DPLL 方向
[ ] 8. 等待 Phase C 完成，汇总结果，写 S025 日志
[ ] 9. Phase D：启动 3 个 agent（D-α/D-β/D-γ）搜索联合架构方向
[ ] 10. 等待 Phase D 完成，汇总结果，写 S026 日志
[ ] 11. Phase E：启动 3 个 agent（E-α/E-β/E-γ）搜索低复杂度方向
[ ] 12. 等待 Phase E 完成，汇总结果，写 S027 日志
[ ] 13. 汇总 A-E 全量结果，评估是否需要扩展（如果 0-1 个候选点 → 启动扩展）
[ ] 14. 写 S028 最终报告
[ ] 15. 更新 thesis-direction-pivot/topic-index.md 进展线索
[ ] 16. 输出最终结论给用户
```

---

## 十一、用户上下文

- 用户是硕士生，导师要求一周内交开题报告（从 2026-05-29 起算）
- 用户无激光通信背景，依赖 AI 做技术推导
- 用户当前正在另一对话并行优化写作质量
- 用户期望此对话全自动运行，不需要任何交互
- 用户对创新性有明确焦虑，但审慎——不急于出结果，先要找对方向
- 导师预期 L2（方法级创新），用户判断当前成果在 L1→L2 边界
- Ch3 是当前最稳固的贡献，Ch4 需要找到与 Ch3 有衔接的创新点

---

## 十二、对 Ch4 衔接的期望

Ch3 导出了 σ_φ 设计准则（不同湍流强度下载波同步精度要求不同）。Ch4 的创新点最好能与这个准则形成呼应：

- Ch3 说"强湍流下 σ_φ < 9.5° 才能保证 P_out < 10⁻⁵"
- Ch4 应该提供"达到这个 σ_φ 目标的算法方案"
- 理想叙事：Ch3 分析问题 → Ch4 提供解决方案

如果找到的创新点不直接与 σ_φ 准则衔接，也可以接受——只要在 Ch4 引言中能说清楚 Ch3→Ch4 的逻辑过渡即可。

---

## 十三、扩展搜索的触发条件

满足以下任一条件则触发扩展搜索：
1. A-E 五个子方向全部标记为 barren
2. 只找到 0 个 L1→L2 及以上的候选创新点
3. 找到的候选创新点全部需要大规模代码重构才能验证

扩展时优先搜索：
- F：信道编码与载波同步联合设计（LDPC/Turbo 码与同步迭代）
- G：导频图案优化（导频间距/功率分配对同步性能的影响）
- H：多载波 FSO 的载波同步（OFDM-FSO 下的 CFO/CPN 估计）
- I：星间链路（ISL）载波同步的启示（ISL 的特殊挑战能否迁移到星地）
- J：阅读过程中发现的任何新角度

---

## 十四、成功的定义

**最佳结果**：找到 ≥2 个 L2 级别的候选创新点，每个都有明确的文献缺口和可执行的验证计划。

**可接受结果**：找到 ≥2 个 L1→L2 边界的候选创新点，或 1 个 L2 + 1 个 L1。

**需要扩展**：找到 0-1 个候选，或全部是 L1 以下。

**需要报告给用户决策**：无论如何都写最终报告，由用户判断是否接受或调整方向。
