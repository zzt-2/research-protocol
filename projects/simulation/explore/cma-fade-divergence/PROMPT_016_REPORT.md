# PROMPT-016 研究报告：扩参数域鲁棒性 + 改动1新颖性

## TL;DR

**段 1（扩参数域）**：N=2M / 5 seeds / 6 唯一 cell（f_G 扫 3 + SNR 扫 3 去重基准点 + 16QAM 1）跑完。**核心反预期**：ML 相对 standard-CMA 的 PI-BER 优势在 N=2M 下**不成立**——6 cell 里 ML 仅 2 cell 均值更优，配对胜场 4/5、3/5、1/5、2/5、2/5、2/5。与 PROMPT-015（N=5M/f_G=30, ML 29/30 赢）方向相反。**根因是 late_slice 的 SOP 累积旋转量差异**（陷阱3实证）：N=5M late 在序列末尾 SOP 漂移大→CMA 漂错解→ML 优势显著；N=2M late 的 SOP 漂移小→standard-CMA 能完美锁定（好 seed 下 PI≈0）→ML 监督残余误差反而更差。结论：**"ML 优于 standard-CMA"强依赖 N 和 late_slice 位置，不是参数域内普适**。

**段 2（改动1 新颖性）**：**改动1 有真创新空间**。"用物理发散判据当 ML 重训练触发信号"在 FSO/卫星光和广义通信均无先例（Qin/Kulmer/Li 冻结训练；Nasr 是固定网格预训练非触发；Freire-TL 是光纤非 FSO）。最硬创新点 = 把 B2 FOE-freeze / JR-CMA 误差阈值那种"物理量 gating"思想从经典估计器移到 ML 训练调度。但须守边界陷阱（触发太频繁=退化全程在线训练，触发太少=等于固定训练），且写作须显式区分"信道状态触发"vs Nasr 的"固定网格预训练"。

## 段 1：扩参数域鲁棒性（5 seeds）

### 实验设置

- N=2,000,000（P012 已审计 f_G=30/100/1000 的 N=2M；**新参数点 SNR 扫/16QAM 用 2M 未独立审计适用性**——陷阱3）
- late_slice = test 段（后 50%）的后 1/4 = [1,750,000, 2,000,000)
- strong 湍流（α=1.5 β=0.8），SOP=4e-7（1krad/s），tap=11，block=100
- seeds 1000-1004（5 seeds，用户明确非最终版够用）
- 四方法：current-CMA / standard-CMA / ML-original / oracle（ML-aligned 省略，P015 已证初始化不敏感）
- 双口径：fixed-label BER + PI-BER（D018 规定并报）
- ⚠️ **grid 去重说明**：PROMPT-016 §2 文字描述"35 cells"把基准点 f_G=30/SNR=20/QPSK 算了两次（f_G 扫+SNR 扫），实际去重后 6 唯一 cell × 5 seeds = 30 trials。基准点只跑一次共享。

### f_G 扫描（QPSK, 20dB）

| f_G (Hz) | ML PI-BER | stdCMA PI-BER | curCMA PI-BER | oracle PI-BER | ML/stdCMA 胜场 |
|---:|---:|---:|---:|---:|:---:|
| 30 | 0.0699 | 0.0853 | 0.2268 | 0.0198 | **4/5** |
| 100 | 0.0837 | 0.0911 | 0.2502 | 0.0220 | 3/5 ⚠️ |
| 1000 | 0.0417 | 0.0021 | 0.2479 | 0.0007 | **1/5** ⚠️ |

**趋势**：f_G=30 时 ML 略优（4/5），但 f_G 增大 ML 优势消失并反转——f_G=1000 时 standard-CMA 碾压 ML（stdCMA 接近 oracle 0.002，ML 0.042 差 20×）。**反预期**：原假设"高动态信道 ML 优势更大"被数据否证。

per-seed 核验（f_G=1000）：stdCMA 在 4/5 seed 接近完美（PI 0.0001-0.005），ML 在 0.02-0.07。高 f_G 下 standard-CMA 反而锁定良好，ML 监督残余误差更显著。

### SNR 扫描（QPSK, f_G=30）

| SNR (dB) | ML PI-BER | stdCMA PI-BER | curCMA PI-BER | oracle PI-BER | ML/stdCMA 胜场 |
|---:|---:|---:|---:|---:|:---:|
| 20 | 0.0699 | 0.0853 | 0.2268 | 0.0198 | 4/5 |
| 15 | 0.1158 | 0.1086 | 0.2498 | 0.0661 | 2/5 ⚠️ |
| 10 | 0.1753 | 0.1456 | 0.2815 | 0.1208 | 2/5 ⚠️ |

**趋势**：降 SNR 时 ML 优势消失。SNR=20 ML 4/5 赢，SNR=15/10 仅 2/5。低 SNR 下噪声主导，standard-CMA 与 ML 都远离 oracle，差距小且不稳定。

### 16QAM（f_G=30, 20dB）

| 调制 | ML PI-BER | stdCMA PI-BER | curCMA PI-BER | oracle PI-BER | ML/stdCMA 胜场 |
|---|---:|---:|---:|---:|:---:|
| 16QAM | 0.2532 | 0.1327 | 0.3453 | 0.0736 | **2/5** ⚠️ |

**反预期（与 D008/D012 一致）**：16QAM 下 ML/CMA gap 不放大反而 ML 更差。per-seed 核验：ML 赢的 2 seed（1000/1003）oracle 本身高（0.22/0.14，信道难）；输的 3 seed oracle≈0（信道好，stdCMA 完美 PI≈0.0001，ML 反而 0.23）。确认 D012 的"高阶星座同时伤 ML 和 oracle"结论。

### Sanity 验证（P6 独立复核）

- ✅ current-CMA 全 6 cell 最差（PI 0.22-0.35），standard 补 z 因子后全 6 cell 更好——与 P015 一致
- ✅ 双口径并报（fixed + PI），PI 需 pilot/帧头消歧（D018）
- ✅ per-seed 数据经独立重算，胜场计数与 JSON 一致

### 跨 cell 汇总

| 指标 | 值 |
|---|---|
| ML excess PI-BER 跨 cell 均值 | 0.0727 |
| stdCMA excess PI-BER 跨 cell 均值 | 0.0437 |
| ML 均值更优的 cell 数 | **2/6** |

### 小结：ML 优势的适用边界

**ML 相对 standard-CMA 的 PI-BER 优势在 N=2M 参数域内不普适**。6 cell 里仅 f_G=30/SNR=20（基准点）ML 4/5 赢且均值略优，其余 5 cell 要么胜场接近（2-3/5）要么反转（f_G=1000 仅 1/5）。

**与 PROMPT-015 的关键差异（陷阱3实证）**：同一 seeds 1000-1004、f_G=30/QPSK/20dB——
- N=5M（P015）：ML 5/5 赢，excess 都很小（std 0.00005-0.031）
- N=2M（本扫描）：ML 4/5 赜（seed 1004 翻转），excess 大得多（std 0.0001-0.16），seed 1004 ML=0.03 vs std=0.0001

根因：**late_slice 的 SOP 累积旋转量不同**。N=5M late=[4.375M,5M)，SOP 累积旋转大→CMA 已漂到错解（D014 极化串扰）→ML 固定权重优势显著。N=2M late=[1.75M,2M)，SOP 累积旋转小→standard-CMA 还没漂太远，好 seed 下能完美锁定→ML 监督残余误差反而更差。

**对论文的影响**：
1. PROMPT-015 的"ML 优于 standard-CMA"结论**严格限于 N=5M/f_G=30/SNR=20/QPSK 参数域**，不能外推到 N=2M 或其他参数点
2. 论文若展示鲁棒性，须诚实呈现"ML 优势依赖 late_slice 的 SOP 漂移量"这一条件，不能画成普适曲线
3. f_G=1000 的反转尤其值得注意——高动态信道下 standard-CMA 反而更稳，这挑战"ML 更适合动态信道"的直觉叙事

## 段 2：改动1 新颖性快查

### Q-new-1：自适应重训练 ML 均衡器（FSO/卫星光）

- **FSO/卫星光场景先例：无（核心触发机制层面）**
- 代表论文：
  1. **Nasr 2026**（10.1109/ACCESS.2026.3683348，已入库）：双偏振自相干 FSO ANN 均衡。做了"重训练"但**不是信道状态触发**——是在固定 θ 角网格（10° 步进）上预训练，ANN 训 120° 泛化 ±4°。是"降低重训练频次"的静态网格策略，无信道状态感知、无触发判据。**最危险的邻近占点**，写作须显式区分。
  2. **Qin 2025/2026**（TCCN，已入库）：VAE/CNN 盲均衡，固定训练（train once），无重训练。明确是改动1要突破的对象。
  3. **JR-CMA**（ACP 2025，L-DP8 已入库）：FSO+深衰落，调 CMA 在线步长 μ_CMA + 误差阈值重置，不调 ML 训练。无 ML。
  4. Web 查证：Kulmer 2026（Optics Express，卫星光 ANN 非线性补偿）= 静态 ANN 训练后冻结；Li 2021（WOCC，DNN FSO 均衡）= 静态。均非自适应重训练。
- **非 FSO 场景邻近工作（场景不同）**：Freire 2021 TL for NN equalizers（JLT，光纤 Kerr）= 迁移学习降低 NN 均衡器重训练开销，触发是离散系统参数变化（launch power/调制/速率），非物理发散判据；Online Meta-Learning hybrid receiver（光纤，2023）= 光纤在线元学习接收机。两者均光纤非 FSO。
- **改动1 能否区分：能**。FSO 场景下"ML 均衡器训练后冻结"是现状，Nasr 是固定网格重训练非触发，无 FSO 工作做"信道状态触发 ML 重训练"。

### Q-new-2：物理判据触发训练

- **先例：无（FSO 和广义通信均无）**
- 代表论文：
  - **最接近类比 = B2 FOE-freeze**（Matsuda 2020 SPIE，已入库笔记 _B2）："received power 下降时冻结 FOE 跟踪"。是"物理量（功率）阈值→gate 传统 DSP 估计器更新"。但 gate 的是经典 CFO 估计器，不是 ML 训练。
  - JR-CMA 的"误差阈值重置 CMA"也是物理阈值→触发算法动作，但动作是重置 CMA 权重非重训练 ML。
  - Web 查 "physics-informed training trigger / divergence-aware retraining / channel-state-aware learning rate" 在光学/通信无命中。
- **改动1 能否区分：能**。"用物理发散判据（μ×σ²×衰落频率阈值）当 ML 重训练触发信号"——核心创新点在 FSO 和广义通信均未见先例。这是改动1最硬的真创新点：把 B2/JR-CMA 那种"物理量 gating"思想从经典估计器移到 ML 训练调度。

### Q-new-3：JR-CMA 自适应步长 vs 改动1 训练调度

- **文献中已清晰区分，未被混为一谈**。Freire 2021/2022 + 综述（Srivallapanondh 2024）明确把两者列为不同机制：CMA 在线步长 = 盲、连续、低开销、tap 级实时跟踪；NN 重训练 = 监督、周期性、高开销（需训练序列+反传）。JR-CMA 自身定位即"调 CMA 在线 μ_CMA"，不涉 ML。
- **结论：Q-new-3 不构成新颖性威胁**。改动1 须在文中显式画此区分线即可。

### 小结：改动1 能升级为方法创新

**能升级——有真创新空间。** 致命判断：
1. "自适应重训练 ML 均衡器"在 FSO/卫星光无被覆盖（Qin/Kulmer/Li 冻结训练，Nasr 固定网格非触发，Freire-TL 光纤非 FSO）
2. "物理发散判据当 ML 重训练触发信号"在 FSO 和广义通信均无先例，是改动1最硬创新点

**但须守边界陷阱**（PROMPT-016 §5 陷阱5）：触发太频繁 = 退化为全程在线训练（Freire/Online-MetaLearning 的领域，光纤已做）；触发太少 = 等于固定训练（改动无意义）。Nasr 2026 的"角网格重训练"是最危险邻近占点，写作必须显式区分"信道状态触发"vs"固定网格预训练"。

## 对主控决策的建议

### 路线 A 的天花板（方法层）

段 1 数据表明：**Q-CMA-FADE 方法层（ML 优于 CMA）的天花板比 PROMPT-015 显示的更低**。P015 的 N=5M/f_G=30 单点 GO 不能外推——N=2M 下 ML 优势大部分消失甚至反转。论文方法层卖点应严格限定在"长序列（SOP 累积漂移大）条件下 ML 避免 CMA 极化串扰"，不能写成普适优势。

结合 D020"机制说不清"+ 段1"优势不普适"，路线 A 方法层**单独不足以支撑强贡献**，须靠分析层（发散概率界 + 条件判据，S005/D006）+ 场景迁移叙事补强。

### 改动1 值不值得投入

**值得，但有前置条件**：
1. 改动1 的创新点（物理判据触发 ML 重训练）新颖性扎实，是路线 A 方法层升级的最可行路径
2. **但段 1 的反预期给改动1 增加了紧迫性**——如果 ML 优势本身在多数参数点不显著（N=2M 下 2/6 cell），那"何时重训练 ML"的调度改进收益空间也受限。改动1 须先证明"在 ML 有优势的参数域（长序列/大 SOP 漂移）内，触发式重训练比固定训练更好"，而不是泛泛做
3. 边界陷阱（触发频率）须在设计阶段就定量化判据，否则容易退化

**建议主控**：改动1 的下一步不是直接实现，而是先用段 1 数据界定"ML 有优势的参数域边界"（N 和 SOP 累积旋转的临界点），在该域内再评估改动1 的增量空间。

## 产出路径

- 段 1 脚本：`projects/simulation/explore/cma-fade-divergence/prompt016_param_sweep.py`
- 段 1 画图脚本：`projects/simulation/explore/cma-fade-divergence/prompt016_plot_trends.py`
- 段 1 结果 JSON：`projects/simulation/results/cma-fade-divergence/prompt016_param_sweep.json`（30 trials + 6 cell summaries）
- 段 1 趋势图：`projects/simulation/results/cma-fade-divergence/prompt016_figures/fig{1,2,3}_*.png`
- 段 2 检索记录：见新颖性快查子 agent 报告（5 项目 query + 3 web query 交叉验证）
- 本报告：`projects/simulation/explore/cma-fade-divergence/PROMPT_016_REPORT.md`
