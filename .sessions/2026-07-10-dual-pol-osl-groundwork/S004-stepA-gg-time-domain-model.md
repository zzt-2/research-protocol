# [S004] Step A 完成：GG 时间域衰落模型（FR-20 前置门控）

> 2026-07-11 | GW Step 4a 维度 D MVE（Q-CMA-FADE）| 状态: Step A 完成

## 目标

执行 PROMPT-003 Step A：建 GG 时间域衰落模型，补 FR-20 缺口（现有 `gg_block` 块间独立，无时间动力学），为 Step B（CMA 发散扫描）和 Step C（ML vs CMA MVE）提供物理驱动的衰落生成器。

## 记录

### FR-20 参数溯源（本地 + 外部子 agent 查证）

派 2 个子 agent 查证物理参数（主对话禁 WebSearch，子 agent 消化）：
- **Explore agent**（本地论文库）：发现**全部本地论文都用块衰落/准静态**（sat.1553 L167 "will not model coherence time, quasi-static"），τ_c 量级有 2 篇本地来源（sat.1553:167 >1ms, s24248036:872 1-100ms），Cn²/横风有来源，但 f_G 公式/时间功率谱/LCR 缺。
- **general-purpose agent**（外部教材）：交叉验证 Greenwood 1977 JOSA 67(3):390（f_G=2.31·λ⁻⁶ᐟ⁵·[∫Cn²V⁵ᐟ³dh]³ᐟ⁵）、Conan 1995 JOSA A 12(7):1559（τ_c=1/(2πf_G)，强度闪烁，**非** AO 的 0.314·r₀/V）、Tatarskii/Clifford 1971（强度谱 f⁻¹¹ᐟ³）、Stefanović 2021（GG LCR/AFD）。

**关键澄清**：τ_c=1/(2πf_G) 是强度闪烁相干时间；0.214/f_G 是 AO 相位校正带宽特定定义。CMA 均衡器跟踪强度闪烁，应用前者。

### 实现（守 sim-preflight 场景 B：新算法=1新文件+0改动现有）

1. **`common/_gg_time.py`**（新文件）：`gg_time_envelope` — 块内恒定，块间 AR(1) 相关（ρ=exp(-block·t_s/τ_c)）。两方法：
   - `gar`（默认）：标准正态 AR(1) + quantile matching → 精确 Gamma 边缘
   - `lognormal`：对数域 AR(1) → log-ACF=ρ 精确（与 F3.28 既有公式同构）
2. **`params.py`** 加 `GGTimeParams`（10 字段全标 FR-20 来源 + audit_flag），f_G 扫描 {30,100,300,1000}Hz（守 C1）
3. **`explore/cma-fade-divergence/gg_time_fading_model.py`**（验证脚本）：边缘 PDF / log-ACF / 衰落统计
4. **`formulas-master.md`** 加 F33b（Greenwood 频率 + τ_c=1/(2πf_G)），2487→2499 行（<2500）。**发现 F3.28/F3.29 AR(1) 时变模型已存在**（与 lognormal 法同构），只补湍流 τ_c 物理锚定（F3.29 原引 T_coh=1/f_D 是多普勒非湍流）

### 验证结果（PASS）

| 验证项 | 结果 |
|--------|------|
| 边缘 PDF (GAR 独立块 KS) | **PASS**：KS<0.006 全湍流档（精确 Gamma 边缘）|
| log-ACF[1] (lognormal) | **PASS**：误差 0.00%（log-ACF=ρ 精确）|
| 文献 τ_c 范围 | **PASS**：1.59/5.31ms 落 sat.1553/s24248036 1-100ms 区间 |
| lognormal 边缘 (强湍) | CHECK（KS=0.149，β<1 重尾矩匹配偏差，已知近似局限）|

**方法选择**：默认 `gar`（边缘精确跨湍流稳健），lognormal 用于弱中湍且需 log-ACF 精确时。

### 物理发现（影响 Step B/C 设计）

**τ_c ≫ block·t_s**：τ_c=1.59ms（f_G=100Hz）vs block·t_s=0.04µs → ρ=0.99997（连续块几乎完全相关）。这意味着：
- 单帧内（≪τ_c）信道近似准静态（与 sat.1553 L167 物理一致）
- 要看到完整衰落动力学，序列需长 ≫ τ_c/t_s ≈ 4×10⁶ 符号
- **Step B CMA 发散扫描需长序列**（≥10⁷ 符号）才能覆盖多个衰落周期
- n_eff 警示：高 ρ 序列 KS 检验失效（n_eff≈3），边缘准确性须用独立块模式验证

## 决策引用

- 无新决策（Step A 是 D005 候选合并后的执行，不涉及方向变更）
- 复用 D002（Q-DP2 Conditional Go 的 FR-20 缺口）→ Step A 补此缺口

## 范围确认

- 本轮是否在 scope boundary 内：**是**（PROMPT-003 Step A 明确范围）
- 守单对话 3 步上限：本对话只做 Step A（Step B/C 开新对话）

## 后续

**Step B（下个对话）**：
1. 先扩 CMA 均衡器到 `common/_cma.py`（P4 只扩不改）
2. CMA 发散概率扫描 vs {衰落深度, 步长, 均衡器阶数}——用 `gg_time_envelope` 生成长序列（≥10⁷ 符号）
3. 补 sat.1553 自认空白："probability of the equalizer diverging has not been analyzed"
4. 守 C6-C8（CMA 公式标 Godard 1980 来源；三方对照：CMA / naive 消融 / oracle）

**Step C（再下个对话）**：
1. 实现 ML 均衡器（参考 Qin VAE / Nasr ANN 精读笔记）
2. vs CMA 对比：发散概率 + BER + 收敛速度 + 深衰落恢复时间
3. 守 Freire2022 6 陷阱 checklist + FR-14/FR-15（先验 CMA + 贡献目标 Qin/Nasr baseline）

**已知债务**：
- `AR1_METHOD` 字段用 tuple 而非 list（Pydantic frozen 兼容），GREENWOOD_FREQ_SWEEP 是 tuple
- Python 环境：AGENTS.md 指定 `~/.venvs/torch/bin/python`（py3.14 无 pydantic），实际用 scoop py311（有 pydantic+numpy+scipy）。torch venv 需补装 pydantic 才能跑仿真
- 衰落统计 LCR/AFD 用数值估计（Stefanović 2021 解析 Meijer-G 复杂，MVE 阶段数值足够）
