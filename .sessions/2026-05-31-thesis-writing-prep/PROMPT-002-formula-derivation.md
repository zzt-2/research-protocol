# PROMPT-002: 公式推导验证

> 专题: thesis-writing-prep | 优先级: P0
> Python: `~/.venvs/torch/bin/python`

## 背景

学位论文需要 Ch2-Ch5 每章的公式推导。现有材料分散且需验证：
- `formulas-ch2-system-model.md` — Ch2 旧格式
- `formulas-ch3ch4-sync.md` — Ch3/Ch4 旧格式
- S002 推导 — Ch3 BER 闭合解
- 仿真代码中隐含的公式

需要: 统一格式、按章节组织、标注来源（引用/自推）、验证正确性。

## 产出

**文件**: `毕设/写作材料/formulas-master.md`（新建）

结构：
```markdown
# 学位论文公式推导

> 创建: YYYY-MM-DD | 与 TERMS.md 符号约定保持一致

## 第二章 公式

### 2.2 信号模型
#### 2.2.1 QPSK 接收信号模型
[公式] r[k] = ...
[来源] 引用 Zhang2018 Eq.(3) / 自推 / 教科书标准
[验证] 仿真代码 sim_xxx.py L42 对应

#### 2.2.2 信噪比定义
...

### 2.3 Gamma-Gamma 分布
...

## 第三章 公式
...
## 第四章 公式
...
## 第五章 公式
...
```

**每个公式条目包含**:
1. 公式本身（LaTeX）
2. 来源标注：`[引用: 文献key Eq.(N)]` / `[自推: 基于...推导]` / `[教科书: Proakis Ch.X]`
3. 变量说明（引用 TERMS.md 符号编号）
4. 验证方式：仿真代码对应行 / 解析验证 / 数值验证
5. 适用条件/假设

## 必读

1. `毕设/写作材料/formulas-ch2-system-model.md`
2. `毕设/写作材料/formulas-ch3ch4-sync.md`
3. `.sessions/2026-05-30-ch3-direction-exploration/S002-ber-closed-form-derivation.md`
4. `毕设/写作材料/thesis-framework.md`
5. `毕设/写作材料/TERMS.md`（符号约定）
6. `projects/thesis-figures/simulation/SPEC.md`
7. 以下仿真代码（提取公式实现）:
   - `projects/thesis-figures/simulation/sim_ch3_ber_closed_form.py`
   - `projects/thesis-figures/simulation/sim_ch3_strengthening.py`
   - `projects/thesis-figures/simulation/sim_cascade_robustness.py`
   - `projects/thesis-figures/simulation/sim_ch4_systematic_analysis.py`

## 子 Agent 策略（自适应）

**不要一开始全定死。** 分阶段推进：

### Phase 1: 探索（2-3 个 agent 并行）

**Agent E1**: 扫描现有公式文档 + framework，评估：
- formulas-ch2/ch3ch4 各有多少公式
- 哪些公式已经完整（可直接搬运），哪些需要补充推导
- 哪些章节缺公式（特别是 Ch4/Ch5）
输出: 公式现状评估 + 每章充足度评级

**Agent E2**: 扫描 S002 推导 + 仿真代码，评估：
- S002 中有多少公式需要提取
- 仿真代码中隐含的公式（信号生成、均衡、VV/DPLL 实现）
- 代码与现有公式文档的重叠度
输出: 补充来源评估

**Agent E3**: 扫描 references.bib，检查：
- 哪些引用文献是公式来源（教科书、经典论文）
- 是否有文献缺失（需要补充检索）
输出: 文献覆盖评估

### Phase 2: 根据发现规划提取

Phase 1 完成后，主对话决定：
- 按章节还是按主题分组提取
- 每章需要几个 agent（基于充足度评级）
- 哪些公式可以直接搬运 vs 需要重新推导验证
- 是否需要分多个对话完成

### Phase 3+: 提取 + 验证 + 写入

根据 Phase 2 规划派 agent。大致原则：
- 一次最多 3 个 agent 并行
- Ch2 可能 1-2 个（公式较成熟），Ch3/Ch4 可能 3-4 个（公式多且复杂）
- 最后留 1-2 个 agent 做交叉验证和写入

## 质量检查

- [ ] 每个公式有来源标注（引用/自推/教科书）
- [ ] 自推公式有验证方式（代码行号/数值对比）
- [ ] VV 公式是修正版: unwrap(angle)/M
- [ ] ω_n 单位统一为 rad/s
- [ ] h 是实值归一化辐照度（不是复信道系数）
- [ ] 无符号冲突（对照 TERMS.md）
- [ ] Ch3→Ch4 衔接: 级联公式中 h_hat 的使用方式明确

## 已知陷阱

1. **VV 公式 bug**: 旧版代码 unwrap(angle*M)/M 是错的，正确是 unwrap(angle)/M。S002 已修正。
2. **ω_n 单位**: 仿真代码用 rad/s，framework 曾误写 MHz。已修正。
3. **h 的含义**: 实值辐照度，不是复信道。均衡公式中 √h 才是电场幅度。
4. **SNR 定义**: γ=γ̄·h（线性关系），不是 γ=γ̄·h²（RF 风格）。
5. **GG 参数化**: α,β 从 Rytov 方差推导，不是直接给定。

## 不要做什么

- 不推导论文中不需要用到的公式
- 不修改仿真代码
- 不写论文正文
- 不修改 TERMS.md（只引用）
