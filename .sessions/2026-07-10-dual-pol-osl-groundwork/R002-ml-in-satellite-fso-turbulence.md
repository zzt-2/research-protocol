# [R002] ML 在星地激光湍流通信的全谱调研

> 2026-07-10 | 关联：专题 2026-07-10-dual-pol-osl-groundwork（并行开放调研，不阻塞 Step 4a 主线）
> 起因：用户追问"对于星地激光湍流的题目，机器学习有啥可行方向"。R001 只查了"调制切换"一个点，本调研扩到全谱。

## 调研问题

用户原话："对于我的，星地激光湍流的题目，机器学习有啥可行方向？我不管别的，只要是相关的。"
补充直觉："这种东西，能用到的地方不应该少才对啊？"

要回答：
1. ML 在星地激光/FSO 湍流里**到底有哪些应用点**？（全谱）
2. 哪些跟"相干接收机物理层 DSP"对口？
3. 各应用点的成熟度——做透了（换皮风险）还是空白（有切入空间）？
4. 有没有跟我们场景（星地相干 FSO + 湍流 + DSP）真正对口的可行方向？

## 检索执行记录

两轮（先广后窄），英文 `tools/search`（11 查询）+ 中文 `tools/blit CNKI`（5 查询），3 子 agent 消化。

| 轮次 | 查询范围 | 工具 | S2 命中峰值 | 存档前缀 |
|---|---|---|---|---|
| 1 英文 | 6 角度广搜（ML+FSO+湍流 / DL 补偿 / NN 信道估计均衡 / ML 卫星预测 / DL 跟瞄 / RL 资源分配） | search | 4497 / 2510 / 4822 | `r002-q1~q6` |
| 1 中文 | 5 角度（ML+FSO / DL+湍流 / NN+光信号 / ML+卫星激光 / DL+激光信道） | blit/cnki | 去重 40 篇学位论文 | `cnki-r002-q1~q5` |
| 2 英文 | 5 收敛深查（LSTM 衰落预测 / NN 载波恢复 / ML 均衡湍流 / fade 检测恢复 / Kalman+NN） | search | 全部命中 19-20 | `r002-r2-q1~q5` |

全部存 `search-archive/2026-07-10/`。守 FR-22（不立 Q#、不判 Go/Kill、不预设、主对话禁 WebSearch、子 agent 消化）。

## 发现

### 调研问题 1：ML 应用点全谱

用户直觉被证实——**应用点又多又散，6 个英文角度全部有可观语料**（最低 S2 命中 1211）。

| # | 应用点 | 成熟度 | 主流方法 | 跟"物理层 DSP"对口度 |
|---|---|---|---|---|
| 1 | AO/波前校正/相位补偿 | ⭐最大最成熟（Guo 2022 综述 200引，Liu 2019 130引） | CNN/GNN/Transformer/KAN | 中（若 AO 已做好则正交） |
| 2 | 信道估计/衰落预测 | 成熟（有低引小群体） | LSTM/ESN/FNN/CNN | **高**（星地链路预测直接相关） |
| 3 | 均衡/载波恢复/非线性补偿 | 光纤多，FSO 少 | MLP/CNN/VQ-VAE/VAE/model-based NN | **高**（物理层 DSP 同层） |
| 4 | 调制格式识别 | 中等 | SVM/监督ML | 低（发什么自己知道） |
| 5 | 调制切换/AMC | 中等（R001 已验物理天花板） | LSTM/DRL | ❌ ③+N1 oracle 封死 |
| 6 | 资源分配/RMSA | 最大但偏网络层 | DRL/Q-Learning | 低（层级不对） |
| 7 | 光束跟踪/pointing/捕获 | 2024-26 爆发 | DRL/CNN | 中（跟瞄层非 DSP） |
| 8 | BER/QoT/链路质量预测 | 中等 | ANN/回归ML | 中 |
| 9 | 端到端 autoencoder | 新兴/空白 | — | 低（基建不兼容） |

### 调研问题 2+3：物理层 DSP 对口的应用点深查（第二轮）

聚焦三个对口点。**关键发现：这三个点在"湍流场景"下几乎都是空白。**

#### 应用点 A：信道估计/衰落预测（LSTM/ESN）

- **规模**：第二轮命中 19 篇，高引仅 1 篇（Chen 2022 DL 信道建模 48 引），其余 2025-2026 新作引用 0-16
- **代表论文**：
  - Nguyen 2022 Echo state network for turbulence-induced fading channel prediction（9引，ESN 预测 FSO 衰落）
  - Li 2023 Multistep ahead atmospheric turbulence forecasting（16引，EMD-Seq2Seq-LSTM）
  - Islam 2025 FSO channel turbulence prediction: A ML approach（11引）
  - Lapsiwala 2025 Link handling for atmospheric turbulence using LSTM（8引）
- **成熟度**：新兴方向，无高引奠基，多为仿真
- **⚠️ 关键空白信号**：预测出的 CSI **目前只用来喂 AMC/链路处理/信道建模**——**未见明确把 CSI 用于驱动相干 DSP 参数（CMA 步长/载波环带宽/恢复触发）的工作**

#### 应用点 B：ML 增强载波恢复/频偏估计

- **规模**：第二轮命中 20 篇，但高引是 Ip&Kahn 2007（524引，传统 feedforward 基线非 ML）和 Freire 2022（106引，光纤警示性）。ML-CPR 真正高引缺位
- **代表论文**：
  - Hu 2025 Noise-Tolerant CPR for Inter-Satellite Coherent（0引，星间相干，针对多普勒非湍流——**唯一卫星/FSO 场景**）
  - Blatter 2025 Transparent CPR Based on ANN（0引，光纤，对手 2S-BPS）
  - Davey 2022 Seq2Seq for CFO Estimation（3引）
- **成熟度**：光纤侧零散低引（2023-2025），未做透；**湍流/星地场景基本空白**
- **⚠️ 关键空白信号**：ML 载波恢复在湍流场景下**基本无人做**（Hu 只做多普勒/相位噪声不涉湍流）

#### 应用点 C：ML 增强均衡（湍流下）

- **规模**：第二轮命中 20 篇，高引 2 篇（Giacoumidis 2018 聚类均衡 101引光纤、Agarwal 2024 湍流修正 36引）。**FSO 相干湍流均衡的 ML 工作仅 3 篇且全 0 引**
- **代表论文（最对口）**：
  - Nasr 2026 ANN-based equalization of polarization mixing... dual-pol self-coherent FSO（0引，ANN 替换 MI，双偏自相干 FSO 湍流）
  - Qin 2026 Blind Nonlinear MIMO VQ-VAE Equalizer for FSO（0引，VQ-VAE，湍流板 r0=0.4mm）
  - Qin 2025 Bootstrapping Blind Equalizer for DP Coherent FSO via Modulus-Rings VAE（0引，VAE，双偏相干 FSO）
- **成熟度**：FSO 相干湍流 ML 均衡是**空白带**，仅 Qin/Nasr 小组在做，全 0 引；光纤侧 ML 非线性均衡是成熟大方向
- **⚠️ 关键空白信号**：Qin 的 VAE 盲均衡在湍流深衰落下对标传统盲均衡，**但无与 CMA 的正面对比，深衰落优势未证**

### 调研问题 4：跟我们场景对口的判断

#### 中文缺口（重要信号）
**没有一篇中文学位论文同时含"星地激光+湍流+ML"**。最接近的是分裂的两组：
- 星地+调制识别（2023），但无湍流
- 大气/DL 自适应光学（2021/2023），但无星地

#### 跨两轮最对口 Top 10

| # | 标题 | 年/引 | ML应用点 | 场景 | 增量(标题层) |
|---|------|------|------|------|------|
| 1 | Nasr ANN-based equalization of polarization mixing for DP self-coherent FSO | 2026/0 | ML均衡 | FSO双偏自相干湍流 | ANN 替换 MI |
| 2 | Qin Blind Nonlinear MIMO VQ-VAE Equalizer for FSO | 2026/0 | ML均衡 | FSO相干湍流 | VQ-VAE 盲均衡 |
| 3 | Qin Bootstrapping Blind Equalizer for DP Coherent FSO via VAE | 2025/0 | ML均衡 | FSO+光纤混合 | VAE 盲均衡 |
| 4 | Hu Noise-Tolerant CPR for Inter-Satellite Coherent | 2025/0 | 载波恢复 | 星间相干(多普勒) | 抗噪 CPR |
| 5 | Nguyen Echo state network for turbulence fading channel prediction | 2022/9 | 衰落预测 | FSO | ESN 衰落预测 |
| 6 | Islam FSO channel turbulence prediction: A ML approach | 2025/11 | 衰落预测 | FSO | ML 衰落预测 |
| 7 | Li Multistep ahead atmospheric turbulence forecasting | 2023/16 | 衰落预测 | FSO | 多步湍流预报 |
| 8 | Lapsiwala Link handling for atmospheric turbulence using LSTM | 2025/8 | 衰落预测 | FSO | LSTM 链路处理 |
| 9 | Agarwal DL approach for turbulence correction in FSO | 2024/36 | 湍流补偿 | FSO | DL 湍流修正 |
| 10 | Liu Applying DL to improve signal detection in FSO | 2024/1 | 信号恢复 | FSO湍流 | DL 信号检测 |

## 结论

### 对 4 个调研问题的回答

1. **全谱**：用户直觉正确。ML 在星地激光湍流有 9 类应用点，6 个英文角度全部可观语料（最低 1211 篇）。**不窄**。
2. **物理层 DSP 对口度**：三个点对口——信道估计/衰落预测、ML 增强载波恢复、ML 增强均衡。其余（AO/识别/资源分配/跟瞄/QoT/autoencoder）要么不同层要么不同问题。
3. **成熟度**：
   - 光纤侧 ML-DSP（非线性补偿/QoT）= 成熟大方向，做进去换皮
   - **FSO/湍流侧 ML-DSP = 几乎全空白**（均衡仅 Qin/Nasr 3 篇全 0 引，载波恢复湍流场景无人，衰落预测喂 DSP 参数无人）→ **有切入空间**
4. **跟我们场景对口**：有，但都在新兴空白带，没有成熟方法可直接对标。最对口的 10 篇里 7 篇是 0 引 2025-2026 新作。

### 一个重要的判断修正

本轮调研推翻了我之前（对话内）的口头判断"ML 方向大概率也窄"。那个判断的错误在于：把 ③ 的 oracle 天花板（只封死"用 ML 选调制"）外推到了整个 ML。实际上：
- ③ 的 oracle 只封死**调制切换**这条 ML 应用路径
- **ML 做 DSP 模块（均衡/载波恢复/预测）不受那个天花板约束**——因为问的是"ML 估计器比传统估计器好没好"，不是"选最优调制增益多少"
- 这两类问题物理性质完全不同。profile 警告的"急于收敛"再次应验。

### 与 Q-DP2/Q-DP3 的潜在结合点（观察，不立论）

- **Q-DP3（跨帧恢复）+ 衰落预测**：应用点 A 的 LSTM/ESN 衰落预测天然可做"fade 前瞻"，为跨帧恢复提供触发信号——**目前无人把两者接起来**。如果 Q-DP3 做下去，ML 预测 fade 来了提前挂起，可能是 ML 在我们场景的自然入口。
- **Q-DP2（CMA 发散）+ ML 均衡**：Qin 的 VAE 盲均衡在湍流深衰落下是否缓解 CMA 发散，未见正面对比——可观察空间。

**注意**：以上是观察不是结论。是否把 ML 结合进 Q-DP2/DP3 要回 Step 4a / Contract 评估，不是这里定。

## 对决策的影响

### 本调研是开放调研，不立 Q#，不判 Go/Kill（守 FR-22）

核心产出是**全谱地图**：用户现在知道 ML 在星地激光湍流有 9 类应用点，其中 3 个跟物理层 DSP 对口且都在空白带。

### 不需要新建 D###

本调研是 R### research note，结论是"全谱描述 + 空白识别"，不涉及推翻现有决策或确立新方向。不动 decisions.md。

### 留给后续的可能路径（不锁死）

1. 如果 Q-DP3 主线 Go：ML 衰落预测 + 跨帧恢复是自然结合点（应用点 A 的空白）
2. 如果想独立做 ML 方向：ML 湍流均衡（应用点 C）和 ML 载波恢复（应用点 B）在星地相干场景是空白，但缺成熟 baseline 对标，风险较高
3. 调制切换（R001）= 已验物理天花板，不重开
